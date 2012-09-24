from django.conf.urls.defaults import patterns, include, url
                                                    
from django.contrib import admin
admin.autodiscover() 

from django.conf import settings

urlpatterns = patterns('',                     
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include('accounts.urls')),
    url(r'^app/', include('clients.urls')),
    url(r'^dashboard/', include('dashboard.urls')),
    url(r'^', include('common.urls')),
) 

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    )
