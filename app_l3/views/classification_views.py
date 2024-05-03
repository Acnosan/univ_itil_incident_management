from django.shortcuts import render
from django.shortcuts import render,redirect
from app_l3.forms import AddCategoryForm,AddPriorityForm,AddStatusForm

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
    return render(response,'templates/tickets_details/category.html',context)

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
    return render(response,'templates/tickets_details/priority.html',context )

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
    return render(response,'templates/tickets_details/status.html', context)