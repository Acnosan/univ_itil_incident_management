
from django import forms
from .models import UserModel,TechnicianModel
from .models import TicketsModel,TicketSolutionModel
from .models import CategoryModel,PriorityModel,StatusModel

class RegisterUserForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Remove help text for the is_staff field
        self.fields['is_staff'].help_text = None
        
    class Meta:
        model = UserModel
        fields = ('username','first_name','last_name','number','email','password','is_staff','is_observer','is_self_service','is_technician')
        labels = {
            'username': '',
            'first_name': '',
            'last_name': '',
            'number':'',
            'email': '',
            'password': '',
            'is_staff': '',
            'is_observer': '',
            'is_self_service': '',
            'is_technician': '',
        }
        
        widgets = {
            'username': forms.TextInput(attrs={}),
            'first_name': forms.TextInput(attrs={}),
            'last_name': forms.TextInput(attrs={}),
            'number':  forms.NumberInput(attrs={}),
            'email': forms.EmailInput(attrs={}),
            'password': forms.PasswordInput(attrs={}),
            'is_observer':forms.CheckboxInput(),
            'is_technician': forms.CheckboxInput(),
            'is_self_service': forms.CheckboxInput(),
            'is_staff':forms.CheckboxInput(),
        }

class AddTicketsForm(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
        self.assigned_by = kwargs.pop('assigned_by', None)  # Retrieve the username from kwargs
        super(AddTicketsForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        instance = super(AddTicketsForm, self).save(commit=False)
        if self.assigned_by:
            instance.assigned_by = self.assigned_by
        if commit:
            instance.save()
        return instance
    
    category = forms.ModelChoiceField(
        queryset= CategoryModel.objects.all(),
        widget=forms.Select(attrs={'placeholder': "Système",'id':"systemtype"}),
        empty_label="Select Category",
    )
    
    priority = forms.ModelChoiceField(
        queryset=PriorityModel.objects.all(),
        widget=forms.Select(),
        empty_label="Select Priority",
    )
    
    status = forms.ModelChoiceField(
        queryset= StatusModel.objects.exclude(status_name='finished'),
        widget=forms.Select(attrs={'placeholder': "Status"}),
        empty_label="Select Status",
        required=False,
    )
    
    assigned_to = forms.ModelChoiceField(
        queryset= TechnicianModel.objects.all(),
        widget=forms.Select(attrs={'placeholder': "Nom de Technicien",'id':"technic"}),
        empty_label="Select Technician",
        required=False,
    )
    
    class Meta:
        model = TicketsModel
        fields = ('title','category','priority','status','description','attachment','assigned_to')
        labels = {
            'title': '',
            'category': '',
            'priority': '',
            'status': '',
            'description': '',
            'assigned_to': '',
            'attachment': '',
        }
        widgets = {
            'title': forms.TextInput(attrs={'placeholder':"Nom de Ticket",'id':"prob-name"}),      
            'description': forms.Textarea(attrs={'placeholder':"Description"}),
        }

class AddCategoryForm(forms.ModelForm):
    
    class Meta:
        model = CategoryModel
        fields = ('category_name','description')
        labels = {
            'category_name': '',
            'description': '',
        }
        widgets = {
            'description': forms.Textarea(attrs={'placeholder':"Description"}),
            'category_name': forms.TextInput(attrs={'placeholder':"Name"}),      
        }

class AddPriorityForm(forms.ModelForm):
    
    class Meta:
        model = PriorityModel
        fields = ('priority_name','description')
        labels = {
            'priority_name': '',
            'description': '',
        }
        widgets = {
            'description': forms.Textarea(attrs={'placeholder':"Description"}),
            'priority_name': forms.TextInput(attrs={'placeholder':"Name"}),      
        }

class AddStatusForm(forms.ModelForm):
    
    class Meta:
        model = StatusModel
        fields = ('status_name','description')
        labels = {
            'status_name': '',
            'description': '',
        }
        widgets = {
            'description': forms.Textarea(attrs={'placeholder':"Description"}),
            'status_name': forms.TextInput(attrs={'placeholder':"Name"}),      
        }

class AddTicketSolutionForm(forms.ModelForm):
    
    class Meta:
        model = TicketSolutionModel
        fields = ('solution_description',)
        labels = {
            'solution_description': '',
        }
        widgets = {  
            'solution_description': forms.Textarea(attrs={'placeholder':"Description"}),
        }