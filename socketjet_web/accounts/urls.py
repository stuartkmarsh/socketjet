from django.conf.urls.defaults import patterns, include, url  

urlpatterns = patterns('accounts.views', 
    url(r'^register/$', 'register', name='register'),
    url(r'^login/$', 'login_user', name='login'),
    url(r'^verify/(?P<auth_token>[a-z0-9]+)/$', 'verify', name="verify"),
    url(r'^logout/$', 'logout_user', name="logout"), 
)