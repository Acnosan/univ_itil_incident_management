from django.shortcuts import render
from django.shortcuts import render,redirect,HttpResponse,get_object_or_404
from app_l3.forms import PriorityFilter,AddTicketsForm,AddTicketSolutionForm
from app_l3.models import UserModel,TicketsModel,TicketSolutionModel,TicketSolutionAttachmentModel
from app_l3.models import TechnicianModel,AdminModel,ObserverModel,SelfServiceModel,StatusModel
from datetime import date,datetime
import csv
from django.conf import settings
import os

def home(response,type_user):
    tickets_created_by_me = tickets_assigned_to_me = all_tickets = None 
    tickets_solution_confirmed = ticket_solutions = None
    is_staff=is_observer=is_technician=is_self_service = None
    count_tickets_created_by_me=count_tickets_assigned_to_me=count_tickets_solution_confirmed=count_all_tickets=0
    username = response.user.username
    
    search_input = response.GET.get('search_input')
    search_input_users = response.GET.get('search_input_users')

    if type_user == 'staff' : 
        is_staff = True
        user = UserModel.objects.get(username=username)
        if user.is_staff:
            try:
                AdminModel.objects.create(username=username, admin_as_user=user, creation_date=date.today())
                ObserverModel.objects.create(username=username, observer_as_user=user, creation_date=date.today())
                SelfServiceModel.objects.create(username=username, self_service_as_user=user, creation_date=date.today())
                TechnicianModel.objects.create(username=username, tech_as_user=user, creation_date=date.today())
                user.save()
            except:
                pass

    elif type_user == 'technician' : is_technician = True 
    elif type_user == 'self_service': is_self_service = True 
    else: is_observer = True
        
    response.session['type_user'] = type_user
    try:
        all_tickets = TicketsModel.objects.all()
        
        if 'search_all' in response.GET and search_input:
            all_tickets = all_tickets.filter(title__startswith=search_input) 
        if response.method == 'POST':
            priority_filter = PriorityFilter(response.POST)
            if priority_filter.is_valid():
                filter_value = priority_filter.cleaned_data['filter_value']
                all_tickets = all_tickets.filter(priority=filter_value).order_by('-ticket_creation_date')
        else:
            priority_filter = PriorityFilter()
            
    except TicketsModel.DoesNotExist:
        pass
    
    try:
        tickets_created_by_me = TicketsModel.objects.filter(assigned_by=response.user)
        if 'search_by_me' in response.GET and search_input:
            tickets_created_by_me = tickets_created_by_me.filter(title__startswith=search_input) 
    except TicketSolutionModel.DoesNotExist:
        pass
    
    try:
        try:
            tech = TechnicianModel.objects.get(username=username)
        except TechnicianModel.DoesNotExist:
            tech=None
            pass
        tickets_assigned_to_me =  TicketsModel.objects.filter(assigned_to=tech)
        if 'search_to_me' in response.GET and search_input:
            tickets_assigned_to_me = tickets_assigned_to_me.filter(title__startswith=search_input) 
    except TicketSolutionModel.DoesNotExist:
        pass
        

    try:
        try:
            status=StatusModel.objects.get(status_name='closed')
        except StatusModel.DoesNotExist:
            status=None
            pass
        tickets_solution_confirmed = TicketsModel.objects.filter(status=status)
        if 'search_closed' in response.GET and search_input:
            tickets_solution_confirmed = tickets_solution_confirmed.filter(title__startswith=search_input) 
    except TicketSolutionModel.DoesNotExist:
        pass
        
    try:
        ticket_solutions = TicketSolutionModel.objects.filter(confirmed_solution=True)
    except TicketSolutionModel.DoesNotExist:
        pass
        
    try:
        count_tickets_created_by_me = tickets_created_by_me.count()
        count_tickets_assigned_to_me = tickets_assigned_to_me.count()
        count_tickets_solution_confirmed = tickets_solution_confirmed.count()
        count_all_tickets = all_tickets.count()
    except:
        pass
    
    try:    
        users = UserModel.objects.all()
        count_all_users = users.count()
            
        if 'search_users_all' in response.GET and search_input_users:
                users = users.filter(last_name__startswith=search_input_users) 
    except:
        count_all_users=0
        pass
    

    context = {
    'type_user':type_user,'is_staff':is_staff,'is_self_service':is_self_service,'is_observer':is_observer,'is_technician':is_technician,
    'tickets_created_by_me':tickets_created_by_me,'tickets_assigned_to_me':tickets_assigned_to_me,
    'tickets_solution_confirmed':tickets_solution_confirmed,'ticket_solutions':ticket_solutions,
    'count_my_tickets':count_tickets_created_by_me,'count_to_me_tickets':count_tickets_assigned_to_me,'count_resolved_tickets':count_tickets_solution_confirmed,
    'count_all_tickets':count_all_tickets,'all_tickets':all_tickets,'priority_filter':priority_filter,
    'users_display': users,'count_all_users':count_all_users}
    return render(response, "templates/home.html", context)

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
        return render(response, "template/app_l3/tickets/ticket_creation.html", {'add_ticket_form': add_ticket_form,'type_user':type_user})
    else:
        add_ticket_form = AddTicketsForm(assigned_by=response.user)
        
    context=  {'add_ticket_form': add_ticket_form,'type_user':type_user,'is_staff':is_staff}
    return render(response, "templates/tickets/ticket_creation.html", context)

def console_ticket(response,ticket_id):
    type_user = response.session.get('type_user')
    ticket = get_object_or_404(TicketsModel, pk=ticket_id)
    ticket_solution = TicketSolutionModel.objects.filter(targeted_ticket=ticket)
    
    solution_ticket_form =  AddTicketSolutionForm(response.POST)
    
    context = {'type_user': type_user,'ticket_display': ticket,'ticket_solution':ticket_solution,'solution_ticket_form':solution_ticket_form}
    return render(response, "templates/tickets/ticket_display.html", context)

def update_ticket(response,ticket_id):
    type_user = response.session.get('type_user')
    is_staff = False 
    if type_user == 'staff' : 
        is_staff = True
        
    ticket = TicketsModel.objects.get(pk=ticket_id)
    if response.method == 'POST':
        update_ticket_form = AddTicketsForm(response.POST or None,response.FILES, instance=ticket)
        
        if update_ticket_form.is_valid():
            if update_ticket_form.instance.assigned_to is not None:
                ticket.status = StatusModel.objects.get(status_name='ongoing')
            update_ticket_form.save()
            return redirect('home', type_user=type_user)
        print(update_ticket_form.errors)
        
    else:
        update_ticket_form = AddTicketsForm(instance=ticket)
        
    context = {'type_user': type_user,'is_staff':is_staff,'ticket_id':ticket.id,'update_ticket_form': update_ticket_form}
    return render(response, "templates/tickets/ticket_update.html", context)

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
        return HttpResponse("Method not allowed", status=401)

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
            #return redirect("home", type_user=response.session.get('type_user'))
            return redirect('console_ticket',ticket_title=ticket_title)
        except ticket_solution.DoesNotExist:
            return HttpResponse("Object not found", status=404)
    else:
        # Handle GET requests or other methods
        return HttpResponse("Method not allowed", status=405)

def add_solution(response,ticket_id):
    type_user = response.session.get('type_user')
    ticket = get_object_or_404(TicketsModel, pk=ticket_id)
    if response.method == "POST":
        targeted_ticket_form = AddTicketsForm(instance=ticket)
        solution_ticket_form =  AddTicketSolutionForm(response.POST)
        
        if solution_ticket_form.is_valid():
            solution_ticket_form.instance.targeted_ticket = ticket
            solution_ticket_form.instance.solution_by = TechnicianModel.objects.get(username=response.user.username)
            ticket.status = StatusModel.objects.get(status_name='solved')
            ticket.save()
            solution_ticket_form.save()
            return redirect('console_ticket',pk=ticket_id)
    else:
        targeted_ticket_form = AddTicketsForm(instance=ticket)
        solution_ticket_form =  AddTicketSolutionForm()
        
    context = {'type_user':type_user,'ticket_id':ticket.id,'targeted_ticket_form':targeted_ticket_form,'solution_ticket_form':solution_ticket_form}
    return render(response,"templates/tickets/ticket_solution.html",context)

def download_solution(response,ticket_title,solution_id):
    ticket = get_object_or_404(TicketsModel, title=ticket_title)
    solution = get_object_or_404(TicketSolutionModel,confirmed_solution=True,targeted_ticket=ticket)
    if response.method == 'POST':
        readData = solution.solution_description
        filename = str(solution_id)+'_'+ticket_title+'.txt'
        
        if not os.path.exists(settings.MEDIA_SOL_ROOT):
            os.makedirs(settings.MEDIA_SOL_ROOT)
            
        file_path = os.path.join(settings.MEDIA_SOL_ROOT,filename)
        with open(file_path, 'w') as file:
            file.write(readData)
            
        TicketSolutionAttachmentModel.objects.create(targeted_solution=solution,attachment=filename)
        
        response = HttpResponse(readData, content_type='text/plain')
        response['Content-Disposition'] = f'attachment; filename={filename}'
        return response
    else:
        # Handle GET requests or other methods
        return HttpResponse("Method not allowed", status=405)   

def download_attachment(response, ticket_title):
    ticket = get_object_or_404(TicketsModel, title=ticket_title)

    response = HttpResponse(ticket.attachment.read(), content_type='application/octet-stream')
    response['Content-Disposition'] = f'attachment; filename="{ticket.attachment.name}"'
    
    if not os.path.exists(settings.MEDIA_ATT_ROOT):
        os.makedirs(settings.MEDIA_ATT_ROOT)
    
    file_path = os.path.join(settings.MEDIA_ATT_ROOT,ticket.attachment.name)
    with open(file_path, 'wb') as file:
        file.write(ticket.attachment.read())
        
    return response

def export_to_csv_by_me(request,filename):
    rows = ["id","title","description","creation date","assigned to","category","priority","status"]
    try:
        queryset = TicketsModel.objects.filter(assigned_by=request.user)
    except TicketSolutionModel.DoesNotExist:
        pass
    
    response = HttpResponse(content_type='text/csv; charset=utf-8')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    
    writer = csv.writer(response)
    writer.writerow(rows)  # Write header row
    
    for obj in queryset:
        writer.writerow([obj.pk,obj.title,obj.description,obj.ticket_creation_date,obj.assigned_to,obj.category,obj.priority,obj.status])

    return response
