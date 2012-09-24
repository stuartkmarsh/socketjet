from django.contrib import admin

from common.models import *

class ApiAccountAdmin(admin.ModelAdmin):
    raw_id_fields = ('user',)
    list_display = ('user', 'disabled', 'api_key')
    list_filter = ('disabled',) 
    search_fields = ['user__username']
    
class ClientUserPermsAdmin(admin.ModelAdmin):
    raw_id_fields = ('client_user',) 
    
class AccountUserProfileAdmin(admin.ModelAdmin):
    raw_id_fields = ('user',) 
    
class UserProfileAdmin(admin.ModelAdmin):
    raw_id_fields = ('user',)  
    
class AccountPackageAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_starter',)

admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(ApiAccount, ApiAccountAdmin) 
admin.site.register(UsageTransaction)    
admin.site.register(ClientUserPermissions, ClientUserPermsAdmin)
admin.site.register(UserCreatedChannel) 
admin.site.register(AccountPackage, AccountPackageAdmin)
admin.site.register(AccountUserProfile, AccountUserProfileAdmin)

