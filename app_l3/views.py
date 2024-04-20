from django.shortcuts import render
from django.contrib.auth.password_validation import password_validators_help_texts
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.hashers import make_password
from django.shortcuts import render,redirect,HttpResponse,get_object_or_404
from django.contrib import messages
from .forms import RegisterUserForm,AddTicketsForm,AddTicketSolutionForm
from .forms import AddCategoryForm,AddPriorityForm,AddStatusForm
from .models import UserModel,TicketsModel,TicketSolutionModel
from .models import TechnicianModel,AdminModel,ObserverModel,SelfServiceModel
from .models import CategoryModel,PriorityModel,StatusModel
from datetime import date,datetime
# Create your views here.

def home(response,type_user):
    tickets_created_by_me = tickets_assigned_to_me = all_tickets = None 
    tickets_solution_confirmed = ticket_solution_date = None
    is_staff=is_observer=is_technician=is_self_service = None
    count_tickets_created_by_me=count_tickets_assigned_to_me=count_tickets_solution_confirmed=count_all_tickets=0
    username = response.user.username
    
    if type_user == 'staff' : 
        is_staff = True
        user = UserModel.objects.get(username=username)
        user.is_observer = user.is_self_service = user.is_technician =True
        user.save()
    elif type_user == 'technician' : is_technician = True 
    elif type_user == 'self_service': is_self_service = True 
    else: is_observer = True
    
    response.session['type_user'] = type_user
    try:
        all_tickets = TicketsModel.objects.all()
    except TicketsModel.DoesNotExist:
        pass
    
    try:
        tickets_created_by_me = TicketsModel.objects.filter(assigned_by=response.user)
    except TicketSolutionModel.DoesNotExist:
        pass
    
    try:
        tickets_assigned_to_me =  TicketsModel.objects.filter(assigned_to=TechnicianModel.objects.get(username=username))
    except TicketSolutionModel.DoesNotExist:
        pass
        
    try:
        status=StatusModel.objects.get(status_name='closed')
    except StatusModel.DoesNotExist:
        pass
    
    try:
        tickets_solution_confirmed = TicketsModel.objects.filter(status=status)
    except TicketSolutionModel.DoesNotExist:
        pass
        
    try:
        ticket_solution_date = TicketSolutionModel.objects.get(confirmed_solution=True).ticket_solution_date
    except TicketSolutionModel.DoesNotExist:
        pass
        
    try:
        count_tickets_created_by_me = tickets_created_by_me.count()
        count_tickets_assigned_to_me = tickets_assigned_to_me.count()
        count_tickets_solution_confirmed = tickets_solution_confirmed.count()
        count_all_tickets = all_tickets.count()
    except:
        pass
            
            
    context = {'type_user':type_user,'is_staff':is_staff,'is_self_service':is_self_service,'is_observer':is_observer,'is_technician':is_technician,
    'tickets_created_by_me':tickets_created_by_me,'tickets_assigned_to_me':tickets_assigned_to_me,
    'tickets_solution_confirmed':tickets_solution_confirmed,'ticket_solution_date':ticket_solution_date,
    'count_my_tickets':count_tickets_created_by_me,'count_to_me_tickets':count_tickets_assigned_to_me,'count_resolved_tickets':count_tickets_solution_confirmed,
    'count_all_tickets':count_all_tickets,'all_tickets':all_tickets}
    return render(response, "template/app_l3/home.html", context)

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
        return render(response, "template/app_l3/login_user.html", {})

def logout_user(response):
    logout(response)
    messages.success(response,("You Did Logout"))
    return redirect("login_form")

def register_user(response):
    type_user = response.session.get('type_user')
    if type_user == 'staff' : is_staff = True 
    
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
    return render(response, "template/app_l3/register_user.html", {'register_user_form': CreationForm, 
                                                        'type_user': type_user,
                                                        })

def update_user(response,target_username):
    type_user = response.session.get('type_user')
    if type_user == 'staff' : is_staff = True 
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
    context = { 'updated_user_form':updated_user_form}
    return render(response, "template/app_l3/users/user_update.html",context)

def display_users(response):
    type_user = response.session.get('type_user')
    users = UserModel.objects.all()
    context = {'type_user': type_user,'users_display': users}
    return render(response, "template/app_l3/users/users_display.html", context)

def add_ticket(response):
    type_user = response.session.get('type_user')
    is_staff = True if type_user == 'staff' else False
    add_ticket_form = AddTicketsForm(response.POST,response.FILES,assigned_by=response.user)
    
    if response.method == "POST":
        if add_ticket_form.is_valid():
            if add_ticket_form.instance.assigned_to is not None:
                add_ticket_form.instance.status =  StatusModel.objects.get(status_name='ongoing')
            else:
                add_ticket_form.instance.status = StatusModel.objects.get(status_name='pending')
            add_ticket_form.save()
            return redirect('home',type_user=response.session.get('type_user'))     
        print(add_ticket_form.errors)
        return render(response, "template/app_l3/ticket_creation.html", {'add_ticket_form': add_ticket_form,'type_user':type_user})
    else:
        add_ticket_form = AddTicketsForm(assigned_by=response.user)
        
    context=  {'add_ticket_form': add_ticket_form,'type_user':type_user,'is_staff':is_staff}
    return render(response, "template/app_l3/tickets/ticket_creation.html", context)

def console_ticket(response,ticket_title):
    type_user = response.session.get('type_user')
    ticket = get_object_or_404(TicketsModel, title=ticket_title)
    ticket_solution = TicketSolutionModel.objects.filter(targeted_ticket=ticket)
    context = {'type_user': type_user,'ticket_display': ticket,'ticket_solution':ticket_solution}
    return render(response, "template/app_l3/tickets/ticket_display.html", context)

def update_ticket(response,ticket_title):
    type_user = response.session.get('type_user')
    ticket = TicketsModel.objects.get(title=ticket_title)
    update_ticket_form = AddTicketsForm(response.POST or None,response.FILES, instance=ticket)
    
    if update_ticket_form.is_valid():
        if update_ticket_form.instance.assigned_to is not None:
            ticket.status = StatusModel.objects.get(status_name='ongoing')
        update_ticket_form.save()
        return redirect('home', type_user=type_user)

    print(update_ticket_form.errors)
    context = {'type_user': type_user, 'ticket_title': ticket.title, 'update_ticket_form': update_ticket_form}
    return render(response, "template/app_l3/tickets/ticket_update.html", context)

def delete_ticket(response,ticket_title):
    if response.method == "POST":
        try:
            ticket_deletion = TicketsModel.objects.get(title=ticket_title)
            ticket_deletion.delete()
            return redirect('home',type_user=response.session.get('type_user'))
        except TicketsModel.DoesNotExist:
            return HttpResponse("Object not found", status=404)
    else:
        # Handle GET requests or other methods
        return HttpResponse("Method not allowed", status=405)

def confirm_ticket(response,ticket_title,solution_id):
    ticket = get_object_or_404(TicketsModel, title=ticket_title)
    ticket_solution= TicketSolutionModel.objects.get(pk=solution_id)
    if response.method == "POST":
        try:
                ticket.status = StatusModel.objects.get(status_name='closed')
                ticket.save()
                ticket_solution.confirmed_solution = True
                ticket_solution.ticket_solution_date = datetime.now()
                ticket_solution.save()
                return redirect("home", type_user=response.session.get('type_user'))
        except ticket_solution.DoesNotExist:
            return HttpResponse("Object not found", status=404)
    else:
        # Handle GET requests or other methods
        return HttpResponse("Method not allowed", status=405)

def add_solution(response,ticket_title):
    type_user = response.session.get('type_user')
    ticket = get_object_or_404(TicketsModel, title=ticket_title)
    if response.method == "POST":
        targeted_ticket_form = AddTicketsForm(instance=ticket)
        solution_ticket_form =  AddTicketSolutionForm(response.POST)
        
        if solution_ticket_form.is_valid():
            solution_ticket_form.instance.targeted_ticket = ticket
            solution_ticket_form.instance.solution_by = TechnicianModel.objects.get(username=response.user.username)
            ticket.status = StatusModel.objects.get(status_name='solved')
            ticket.save()
            solution_ticket_form.save()
            return redirect('console_ticket',ticket_title=ticket_title)
    else:
        targeted_ticket_form = AddTicketsForm(instance=ticket)
        solution_ticket_form =  AddTicketSolutionForm()
        
    context = {'type_user':type_user,'ticket_title':ticket.title,'targeted_ticket_form':targeted_ticket_form,'solution_ticket_form':solution_ticket_form}
    return render(response,"template/app_l3/tickets/ticket_solution.html",context)

def add_category(response):
    type_user = response.session.get('type_user')
    if response.method == "POST":
        
        AddCategory = AddCategoryForm(response.POST)
        if AddCategory.is_valid():
            AddCategory.save()
            return redirect('home',type_user=response.session.get('type_user'))
        else:
            print("Category Form is invalid")
            return render(response, 'template/app_l3/ticket.html',context)
    else:
        AddCategory = AddCategoryForm()
        
    context={'add_category_form':AddCategory,'type_user':type_user}
    return render(response,'template/app_l3/tickets_details/category.html',context)

def add_priority(response):
    type_user = response.session.get('type_user')
    if response.method == "POST":
        
        AddPriority = AddPriorityForm(response.POST)
        if AddPriority.is_valid():
            AddPriority.save()
            return redirect('home',type_user=response.session.get('type_user'))
        else:
            print("Priority Form is invalid")
            return render(response, 'template/app_l3/ticket.html', context)
    else:
        AddPriority = AddPriorityForm()
        
    context= {'add_priority_form':AddPriority,'type_user':type_user}
    return render(response,'template/app_l3/tickets_details/priority.html',context )

def add_status(response):
    type_user = response.session.get('type_user')
    if response.method == "POST":
        
        AddStatus = AddStatusForm(response.POST)
        if AddStatus.is_valid():
            AddStatus.save()
            return redirect('add_ticket_form')
        else:
            print("Status Form is invalid")
            return render(response, 'template/app_l3/ticket.html', context)
    else:
        AddStatus = AddStatusForm()
    
    context={'add_status_form':AddStatus,'type_user':type_user}
    return render(response,'template/app_l3/tickets_details/status.html', context)
