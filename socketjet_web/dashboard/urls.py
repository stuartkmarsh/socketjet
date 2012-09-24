from django.conf.urls.defaults import patterns, include, url  

urlpatterns = patterns('dashboard.views',
    (r'^$', 'sites_list'),
    url(r'^channels/$', 'channels_list', name='channels_list'), 
    url(r'^channels/edit/(?P<channel_id>\d+)/$', 'channels_edit', name='channels_edit'),
    url(r'^channels/add/$', 'channels_add', name='channels_add'),
    url(r'^channels/delete/(?P<channel_id>\d+)/$', 'channels_delete', name='channels_delete'),
    url(r'^sites/$', 'sites_list', name='sites_list'),
    url(r'^sites/edit/(?P<site_id>\d+)/$', 'sites_edit', name='sites_edit'),
    url(r'^sites/add/$', 'sites_add', name='sites_add'),
    url(r'^sites/delete/(?P<site_id>\d+)/$', 'sites_delete', name='sites_delete'),
)