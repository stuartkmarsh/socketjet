from django.conf.urls.defaults import patterns, include, url  

urlpatterns = patterns('clients.views', 
    url(r'^$', 'app_home', name="app_home"), 
)