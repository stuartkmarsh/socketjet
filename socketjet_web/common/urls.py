from django.conf.urls.defaults import patterns, include, url  
from django.views.generic import TemplateView 
                                   
urlpatterns = patterns('common.views',
    url(r'^$', 'home', name="home"),
    url(r'^func_test/$', 'test_index'),
    url(r'^chat/$', 'chat'),
    url(r'^test/$', TemplateView.as_view(template_name="test.html")),
    url(r'^websocket/auth/$', 'auth'),  
)
