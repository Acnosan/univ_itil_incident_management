from django.urls import path
from .views import user_views,ticket_views,classification_views

urlpatterns = [
    
    path("",user_views.login_user,name="login_form"),
    path("logout/",user_views.logout_user,name="logout_user"),
    path("register/",user_views.register_user,name="register_user_form"), 
    path("user/<int:user_id>",user_views.display_user,name="display_user"), 
    path("user/update/<int:user_id>/",user_views.update_user,name="update_user_form"), 
    path("user/delete/<int:user_id>/",user_views.delete_user,name="delete_user"), 

    path("home/<str:type_user>/",ticket_views.home,name="home"),
    
    path("ticket/create/",ticket_views.add_ticket,name="add_ticket_form"),
    path("ticket/display/<int:ticket_id>/",ticket_views.console_ticket,name="console_ticket"),
    path("ticket/update/<int:ticket_id>/",ticket_views.update_ticket,name="update_ticket_form"),
    path("ticket/delete/<int:ticket_id>/",ticket_views.delete_ticket,name="delete_ticket"),
    
    path("ticket/solution/<int:ticket_id>",ticket_views.add_solution,name="add_solution_form"),
    path("ticket/confirm/<int:ticket_id>/<int:solution_id>/",ticket_views.confirm_ticket,name="confirm_ticket"),
    
    path("ticket/solution/download-<str:ticket_title>-<int:solution_id>/",ticket_views.download_solution,name="download_solution"),
    path('download-attachment/<int:ticket_id>/', ticket_views.download_attachment, name='download_attachment'),
    path("export/<str:filename>",ticket_views.export_to_csv_by_me,name="export_to_csv"),
    
    path("category/create/",classification_views.add_category,name="add_category_form"),
    path("priority/create/",classification_views.add_priority,name="add_priority_form"),
    path("status/create",classification_views.add_status,name="add_status_form"),
    
    path('ticket/conversation/<int:ticket_id>',ticket_views.ticket_conversation,name='ticket_conversation')
]




