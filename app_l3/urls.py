from django.urls import path,include
from . import views

urlpatterns = [
    path("home/<str:type_user>/",views.home,name="home"),
    path("",views.login_user,name="login_form"),
    path("logout/",views.logout_user,name="logout_user"),
    path("register/",views.register_user,name="register_user_form"), 
    path("users/",views.display_users,name="display_users"), 
    path("user/update/<str:target_username>/",views.update_user,name="update_user_form"), 
    
    path("ticket/create/",views.add_ticket,name="add_ticket_form"),
    path("ticket/<str:ticket_title>/",views.console_ticket,name="console_ticket"),
    path("ticket/update/<str:ticket_title>/",views.update_ticket,name="update_ticket_form"),
    path("ticket/delete/<str:ticket_title>/",views.delete_ticket,name="delete_ticket"),
    path("ticket/confirm/<str:ticket_title>/<int:solution_id>/",views.confirm_ticket,name="confirm_ticket"),
    path("ticket/solution/download-<str:ticket_title>-<int:solution_id>/",views.download_solution,name="download_solution"),
    path('download-attachment/<str:ticket_title>/', views.download_attachment, name='download_attachment'),
    
    path("category/create/",views.add_category,name="add_category_form"),
    path("priority/create/",views.add_priority,name="add_priority_form"),
    path("status/create",views.add_status,name="add_status_form"),
    
    path("ticket/solution/<str:ticket_title>/",views.add_solution,name="add_solution_form"),
    path("export/<str:filename>",views.export_to_csv_by_me,name="export_to_csv"),
]




