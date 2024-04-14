from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

class CustomAuthMethod(ModelBackend):
    def authenticate(self,request,username=None,password=None,**kwargs):
        my_model = get_user_model()
        try:
            user = my_model.objects.get(email=username)
            if user.check_password(password): 
                return user
        except my_model.DoesNotExist:
            pass
        
        try:
            user = my_model.objects.get(username=username)
            if user.check_password(password): 
                return user
        except my_model.DoesNotExist:
            pass
        
        return None