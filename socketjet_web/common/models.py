from django.db import models
from django.contrib.auth.models import User

import uuid  

def upload_location(instance, filename):
    return 'user_data/%s/%s' % (instance.api_key, filename)

class ApiCreationException(Exception):
    pass   
    
class AccountManager(models.Manager):
    def create_account(self, user, site_prefix):
        api_key = ApiAccount.create_api_key()
        secret_key = ApiAccount.create_api_key()
        api_account = self.create(api_key=api_key, user=user, secret_key=secret_key, site_prefix=site_prefix)
        
        # also create a client user perm for this account
        user_perm = ClientUserPermissions.objects.create(client_user=user, api_account=api_account, is_admin=True)
        
        return api_account, user_perm 
                                          
class ActiveAccountManager(models.Manager):
    def get_query_set(self):
        return super(ActiveAccountManager, self).get_query_set().filter(disabled=False)                

class ApiAccount(models.Model): 
    site_prefix = models.CharField(max_length=50, unique=True, help_text='also the app name')
    api_key = models.CharField(max_length=50, db_index=True)
    user = models.ForeignKey(User)             
    created = models.DateTimeField(auto_now_add=True) 
    secret_key = models.CharField(max_length=50)
    callback_url = models.URLField(blank=True, null=True)
    disabled = models.BooleanField(default=False)
            
    objects = AccountManager()
    active_objects = ActiveAccountManager()
                                                  
    def __unicode__(self):
        return self.site_prefix
        
    class Meta:
        verbose_name_plural = 'Sites (Api Accounts)'
        verbose_name = 'Site'
        
    @staticmethod
    def create_api_key():
        for i in xrange(1000):
            api_key = ''.join(str(uuid.uuid4()).split('-'))
            if ApiAccount.objects.filter(api_key=api_key).count() == 0:
                return api_key
                
        raise ApiCreationException 
        
class UserCreatedChannel(models.Model):
    channel_name = models.CharField(max_length=100)  
    created_by = models.ForeignKey(User)
    site = models.ForeignKey(ApiAccount)   
    
    def __unicode__(self):
        return self.channel_name
        
    class Meta:
        verbose_name_plural = 'User Created Channels'
        unique_together = ('channel_name', 'created_by', 'site')
        
class ClientUserPermissions(models.Model):
    client_user = models.ForeignKey(User)
    api_account = models.ForeignKey(ApiAccount)
    db_del = models.BooleanField(default=False)
    private_channels = models.ManyToManyField(UserCreatedChannel, blank=True, null=True)
    is_admin = models.BooleanField(default=False)
    
    def __unicode__(self):
        return '%s: %s' % (self.client_user.username, self.api_account.site_prefix)
        
    class Meta:
        verbose_name_plural = 'Client User Permissions'   
        
class AccountPackage(models.Model):
    name = models.CharField(max_length=100)
    max_connections = models.IntegerField(help_text="simultaneous connections")
    max_messages = models.IntegerField(help_text="max messages per day")
    is_starter = models.BooleanField(default=False)  

    def __unicode__(self):
        return self.name      
        
def get_auth_token():
    return AccountUserProfile.create_auth_token()
        
class AccountUserProfile(models.Model):
    user = models.OneToOneField(User)
    current_monthly_messages = models.IntegerField(default=0) 
    account_package = models.ForeignKey(AccountPackage) 
    auth_token = models.CharField(max_length=100, blank=True, default=get_auth_token)
    is_verified = models.BooleanField(default=False)
    
    def __unicode__(self):
        return self.user.username 
        
    @staticmethod
    def create_auth_token():
        for i in xrange(1000):
            auth_token = ''.join(str(uuid.uuid4()).split('-'))
            if AccountUserProfile.objects.filter(auth_token=auth_token).count() == 0:
                return auth_token

        raise ApiCreationException   
        
        
class UserProfile(models.Model):  
    user = models.OneToOneField(User)
    account_created = models.DateTimeField(auto_now_add=True)   
    api_account = models.ForeignKey(ApiAccount)
    
    def __unicode__(self):
        return self.user.username  
        
class UsageTransaction(models.Model):     
    api_account = models.ForeignKey(ApiAccount)
    created = models.DateTimeField(auto_now_add=True)
    messages = models.IntegerField(default=0)
    connections = models.IntegerField(default=0)
    
    def __unicode__(self):
        return self.api_account.site_prefix
        
    class Meta:
        verbose_name_plural = 'Usage Transactions'
