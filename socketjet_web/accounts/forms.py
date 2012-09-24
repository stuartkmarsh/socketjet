from django import forms  
from django.forms import ModelForm 
from django.contrib.auth.models import User   

from common.models import ApiAccount
#from accounts.models import SiteData

class RegistrationForm(forms.Form):
    username = forms.CharField(max_length=20) 
    email = forms.EmailField()
    password1 = forms.CharField(max_length=20, widget=forms.PasswordInput)
    password2 = forms.CharField(max_length=20, widget=forms.PasswordInput)
    app_name = forms.CharField(max_length=50)
        
    def clean(self):
        cleaned_data = self.cleaned_data
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        
        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError('Passwords do not match')
                
        return cleaned_data
        
    def clean_username(self):
        data = self.cleaned_data['username']
        user = User.objects.filter(username=data)
        
        if user.count() > 0:
            raise forms.ValidationError('Sorry, this username already exists')
            
        return data  
        
    def clean_email(self):
        data = self.cleaned_data['email']
        user = User.objects.filter(email=data)
        
        if user.count() > 0:
            raise forms.ValidationError('Sorry, this email address already exists')
            
        return data 
        
    def clean_app_name(self):
        data = self.cleaned_data['app_name']
        account = ApiAccount.objects.filter(site_prefix=data)
        if account.count() > 0:
            raise forms.ValidationError('Sorry, this app name already exists')
            
        return data  
        
class LoginForm(forms.Form):
    username = forms.CharField(max_length=30)
    password = forms.CharField(max_length=50, widget=forms.PasswordInput) 
    

    