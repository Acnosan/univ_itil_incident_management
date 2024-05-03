from django.shortcuts import render
from django.contrib.auth.password_validation import password_validators_help_texts
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.hashers import make_password
from django.shortcuts import render,redirect
from django.contrib import messages
from app_l3.forms import RegisterUserForm
from app_l3.models import UserModel,TechnicianModel,AdminModel,ObserverModel,SelfServiceModel

def login_user(response):
    if response.user.is_authenticated:
        return redirect("home",type_user=response.session.get('type_user'))
    
    if response.method == "POST":
        username = response.POST["username"]
        password = response.POST["password"]
        USER = authenticate(response,username=username,password=password)
        if USER is not None:
            user = UserModel.objects.get(username=username)
            if user.is_staff:
                login(response,user=USER)
                return redirect("home",type_user='staff')
            if user.is_technician:
                login(response,user=USER)
                return redirect("home",type_user='technician')
            if user.is_self_service:
                login(response,user=USER)
                return redirect("home",type_user='self_service')
            if user.is_observer:
                login(response,user=USER)
                return redirect("home",type_user='observer')
            
        else:
            messages.success(response,("there was Authentication error"))
            return redirect("login_form")
    else:
        return render(response, "templates/login_user.html", {})

def logout_user(response):
    logout(response)
    messages.success(response,("You Did Logout"))
    return redirect("login_form")

def register_user(response):
    type_user = response.session.get('type_user')
    
    if response.method == "POST":
        CreationForm = RegisterUserForm(response.POST)
        if CreationForm.is_valid():
            username = CreationForm.cleaned_data["username"]
            password = CreationForm.cleaned_data["password"]
            hash_pass = make_password(password=password)
            CreationForm.instance.password = hash_pass
            CreationForm.save()
            model = UserModel.objects.get(username=username)
            if CreationForm.instance.is_staff:
                AdminModel.objects.create(username=username, admin_as_user=model)
            if CreationForm.instance.is_observer:
                ObserverModel.objects.create(username=username, observer_as_user=model)
            if CreationForm.instance.is_self_service:
                SelfServiceModel.objects.create(username=username, self_service_as_user=model)
            if CreationForm.instance.is_technician:
                TechnicianModel.objects.create(username=username, tech_as_user=model)
            messages.success(response,("User Registered"))
            redirect('register_user_form')
            
        else:
            messages.success(response,("Unvalid Register Form"))
            for txt in password_validators_help_texts():
                messages.success(response,txt)
            redirect('register_user_form')
            
    else:
        CreationForm = RegisterUserForm()
        
    context={'register_user_form': CreationForm, 'type_user': type_user}
    return render(response, "templates/register_user.html",context)

def update_user(response,target_username):
    type_user = response.session.get('type_user')

    target_user = UserModel.objects.get(username=target_username)
    updated_user_form = RegisterUserForm(response.POST or None, instance=target_user)
    
    if response.method == "POST":
        if updated_user_form.is_valid():
            
            if updated_user_form.instance.is_staff:
                if AdminModel.objects.get(username=target_username):
                    pass
                else:
                    AdminModel.objects.create(username=target_username, admin_as_user=target_user)
            if updated_user_form.instance.is_observer:
                if ObserverModel.objects.get(username=target_user):
                    pass
                else:
                    ObserverModel.objects.create(username=target_username, observer_as_user=target_user)
                
            if updated_user_form.instance.is_self_service:
                if SelfServiceModel.objects.get(username=target_username):
                    pass
                else:
                    SelfServiceModel.objects.create(username=target_username, self_service_as_user=target_user)
            if updated_user_form.instance.is_technician:
                if TechnicianModel.objects.get(username=target_username) :
                    pass
                else:
                    TechnicianModel.objects.create(username=target_username, tech_as_user=target_user)
            
            updated_user_form.save()
            
            return redirect('user_display', type_user=type_user)
        
        print(updated_user_form.errors)
    context = {'updated_user_form':updated_user_form,'type_user':type_user}
    return render(response, "templates/users/user_update.html",context)

def display_users(response):
    type_user = response.session.get('type_user')
    users = UserModel.objects.all()
    context = {'type_user': type_user,'users_display': users}
    return render(response, "templates/users/users_display.html", context)