from django import forms
from django.forms import ModelForm

from common.models import ApiAccount, UserCreatedChannel      
        
class SiteForm(ModelForm):                   
    class Meta:
        model = ApiAccount
        fields = ('site_prefix',)
    
    def __init__(self, user, *args, **kwargs):    
        super(SiteForm, self).__init__(*args, **kwargs)
        
        self.user = user         
            
class ChannelForm(ModelForm):
    class Meta:
        model = UserCreatedChannel
        exclude = ('created_by')
