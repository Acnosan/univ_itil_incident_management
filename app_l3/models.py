from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class UserModel(AbstractUser):
    
    username = models.CharField(max_length = 150,unique=True,blank=False,null=False)
    first_name = models.CharField(max_length = 100,blank=False,null=False)
    last_name = models.CharField(max_length = 150,blank=False,null=False)
    email = models.EmailField(blank=False,null=False)
    password = models.CharField(max_length = 100,blank=False,null=False)
    number = models.IntegerField(blank=False,null=False)
    is_observer = models.BooleanField(null=True,default=False)
    is_self_service = models.BooleanField(null=True,default=False)
    is_technician = models.BooleanField(null=True,default=False)

    is_active = models.BooleanField(null=True,default=True)
    is_superuser =  models.BooleanField(null=True,default=False)
    
    REQUIRED_FIELDS = ['password']
    USERNAME_FIELD = 'username'
    
    class Meta:
        db_table = 'user_table'
        
    def __str__(self):
        return self.username

class AdminModel(models.Model):
    username = models.CharField(max_length = 150,unique=True)
    admin_as_user = models.OneToOneField(UserModel,on_delete=models.PROTECT,primary_key=True)
    creation_date = models.DateField(null=True,blank=True) 
    
    class Meta:
        db_table = 'admin_table'

class TechnicianModel(models.Model):
    username = models.CharField(max_length = 150,unique=True)
    tech_as_user = models.OneToOneField(UserModel,on_delete=models.PROTECT,primary_key=True)
    creation_date = models.DateField(null=True,blank=True) 
    
    class Meta:
        db_table = 'technician_table'
        
    def __str__(self):
        if self.tech_as_user.first_name and self.tech_as_user.last_name:
            return f"{self.tech_as_user.first_name} {self.tech_as_user.last_name}"
        elif self.tech_as_user.first_name:
            return self.tech_as_user.first_name
        elif self.tech_as_user.last_name:
            return self.tech_as_user.last_name
        else:
            return self.username

class ObserverModel(models.Model):
    username = models.CharField(max_length = 150,unique=True)
    observer_as_user = models.OneToOneField(UserModel,on_delete=models.PROTECT,primary_key=True)
    creation_date = models.DateField(null=True,blank=True) 
    
    class Meta:
        db_table = 'observer_table'

class SelfServiceModel(models.Model):
    username = models.CharField(max_length = 150,unique=True)
    self_service_as_user = models.OneToOneField(UserModel,on_delete=models.PROTECT,primary_key=True)
    creation_date = models.DateField(null=True,blank=True) 
    
    class Meta:
        db_table = 'self_service_table'        

class CategoryModel(models.Model):
    
    CATEGORY_CHOICES = (
        ('hardware', 'Hardware'),
        ('software', 'Software'),
        ('network', 'Network'),
        ('printer', 'Printer'),
        ('phone', 'Phone'),
        ('laptop', 'Laptop'),
    )
    
    category_name = models.CharField(max_length = 150,unique=True,primary_key=True,choices=CATEGORY_CHOICES)
    description = models.TextField()
    category_creation_date = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    
    def __str__(self) -> str:
        return self.category_name
    
    class Meta:
        db_table = 'category_table'

class PriorityModel(models.Model):
    
    PRIORITY_CHOICES = (
        ('veryhigh', 'Very High'),
        ('high', 'High'),
        ('medium', 'Medium'),
        ('low', 'Low'),
    )
    
    priority_name = models.CharField(max_length = 150,unique=True,primary_key=True,choices=PRIORITY_CHOICES)
    description = models.TextField()
    priority_creation_date = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    
    def __str__(self) -> str:
        return self.priority_name
    
    class Meta:
        db_table = 'priority_table'

class StatusModel(models.Model):
    
    STATUS_CHOICES = (
        #('new', 'New'),
        ('pending', 'Pending'),
        ('ongoing', 'Ongoing'),
        ('solved', 'Solved'),
        ('closed', 'Closed'),
    )
    
    status_name = models.CharField(max_length = 150,unique=True,primary_key=True,choices=STATUS_CHOICES)
    description = models.TextField()
    status_creation_date = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    
    def __str__(self) -> str:
        return self.status_name
    
    class Meta:
        db_table = 'status_table'

class TicketsModel(models.Model):
    
    title = models.CharField(max_length = 150,unique=True,blank=False, null=False)
    category = models.ForeignKey(CategoryModel,on_delete=models.CASCADE,blank=False, null=False)
    priority = models.ForeignKey(PriorityModel,on_delete=models.CASCADE,blank=False, null=False)
    status = models.ForeignKey(StatusModel,on_delete=models.CASCADE,blank=False,null=False)
    assigned_by = models.ForeignKey(UserModel,on_delete=models.CASCADE)
    assigned_to = models.ForeignKey(TechnicianModel,on_delete=models.CASCADE,blank=True,null=True)
    description = models.TextField(blank=False,null=False)
    ticket_creation_date = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    
    class Meta:
        db_table = 'tickets_table'
        
    def __str__(self) -> str:
        return self.title

class TicketSolutionModel(models.Model):
    
    targeted_ticket = models.ForeignKey(TicketsModel,on_delete=models.CASCADE,blank=False,null=False)
    solution_by = models.ForeignKey(TechnicianModel,on_delete=models.PROTECT)
    solution_description = models.TextField(blank=False,null=False)
    ticket_solution_date = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    confirmed_solution = models.BooleanField(default=False)
    
    class Meta:
        db_table = 'tickets_solutions_table'

