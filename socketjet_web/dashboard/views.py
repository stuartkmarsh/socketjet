from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext 
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse 
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseForbidden, Http404 
from django.contrib import messages 
from django.db.models import Sum  
from django.forms.util import ErrorList 

from common.models import ApiAccount, UserCreatedChannel, UsageTransaction, ClientUserPermissions 
from dashboard.forms import SiteForm, ChannelForm  

import datetime
from datetime import timedelta 
import os

class SpanErrorList(ErrorList):
    def __unicode__(self):
        return self.as_spans()
    def as_spans(self):
        if not self: return u''
        return u'%s' % ''.join([u'<span class="help-inline">%s</span>' % e for e in self])

@login_required(login_url='/accounts/login/')
def sites_list(request): 
    api_accounts = ApiAccount.active_objects.filter(user=request.user).order_by('site_prefix')
    accounts = []
    for a in api_accounts:
        data = {}
        data['api_key'] = a.api_key
        data['site_prefix'] = a.site_prefix 
        data['id'] = a.id
        trans = a.usagetransaction_set.filter(created__gte=datetime.datetime.today().date()-timedelta(days=30))
        try:
            data['messages'] = trans.aggregate(messages=Sum('messages'))['messages'] / 30
        except:
            data['messages'] = 0
            
        try:
            data['connections'] = trans.aggregate(connections=Sum('connections'))['connections'] / 30
        except:
            data['connections'] = 0
            
        accounts.append(data)
             
    return render_to_response('sites_list.html', {'accounts':accounts
                                                      }, context_instance=RequestContext(request))

@login_required(login_url='/accounts/login/')
def sites_edit(request, site_id):
    site = get_object_or_404(ApiAccount, pk=site_id, disabled=False)
    if not site.user == request.user:
        raise Http404()
               
    error = None
    
    if request.method == 'POST':
        form = SiteForm(request.user, request.POST, error_class=SpanErrorList, instance=site)
        if form.is_valid():
            form.save()    
            messages.success(request, "Your site '%s' was saved." % site.site_prefix)
            return HttpResponseRedirect(reverse('sites_list'))
    else: 
        form = SiteForm(request.user, initial={'site_prefix':site.site_prefix}, instance=site)
             
    return render_to_response('sites_edit.html', {'form':form,
                                                  'site':site,         }, 
                                context_instance=RequestContext(request))
                                
@login_required(login_url="/accounts/login/")
def sites_add(request):
    if request.method == 'POST':
        form = SiteForm(request.user, request.POST, request.FILES, error_class=SpanErrorList)
        if form.is_valid(): 
            acc = form.save(commit=False)
            api_key = ApiAccount.create_api_key()
            secret_key = ApiAccount.create_api_key()
            acc.api_key = api_key
            acc.secret_key = secret_key 
            acc.user = request.user   
            acc.save()
            user_perm = ClientUserPermissions.objects.create(client_user=request.user, api_account=acc, is_admin=True)
              
            messages.success(request, "Your site '%s' was added." % form.cleaned_data['site_prefix'])
            return HttpResponseRedirect(reverse('sites_list'))
    else:                                       
        form = SiteForm(request.user)
             
    return render_to_response('sites_add.html', {'form':form}, context_instance=RequestContext(request))
    
@login_required(login_url="/accounts/login/")
def sites_delete(request, site_id):
    site = get_object_or_404(ApiAccount, pk=site_id, disabled=False)
    if not site.user == request.user:
        raise Http404()
                                    
    site.disabled = True
    site.save()
    messages.success(request, "Your site '%s' has been deleted." % site.site_prefix)
    return HttpResponseRedirect(reverse('sites_list'))
    
    
@login_required(login_url='/accounts/login/')
def channels_list(request):
    channels = request.user.usercreatedchannel_set.all().order_by('site__site_prefix')
    return render_to_response('channels_list.html', {'channels':channels},
                                context_instance=RequestContext(request))  

@login_required(login_url='/accounts/login/')                                
def channels_edit(request, channel_id):
    channel = get_object_or_404(UserCreatedChannel, pk=channel_id)
    if not channel.created_by == request.user:
        raise Http404 
        
    if request.method == 'POST':
        form = ChannelForm(request.POST, error_class=SpanErrorList, instance=channel)
        if form.is_valid():
            chan_form = form.save(commit=False)
            chan_form.created_by = request.user
            chan_form.save() 
            messages.success(request, "Your channel '%s' was saved." % form.cleaned_data['channel_name'])
            return HttpResponseRedirect(reverse('channels_list'))
    else:
        form = ChannelForm(instance=channel)
    
    form.fields['site'].queryset = ApiAccount.objects.filter(user=request.user)
        
    return render_to_response('channels_edit.html', {'form':form},
                                                    context_instance=RequestContext(request)) 
                                                    
@login_required(login_url='/accounts/login/')
def channels_add(request):
    if request.method == 'POST':
        form = ChannelForm(request.POST, error_class=SpanErrorList)
        if form.is_valid():
            chan_form = form.save(commit=False)
            chan_form.created_by = request.user
            chan_form.save()
            messages.success(request, "Your channel '%s' was added." % form.cleaned_data['channel_name'])
            return HttpResponseRedirect(reverse('channels_list'))
    else:
        form = ChannelForm()
    
    form.fields['site'].queryset = ApiAccount.objects.filter(user=request.user)
        
    return render_to_response('channels_add.html', {'form':form},
                                                    context_instance=RequestContext(request)) 
                                                    
@login_required(login_url='/accounts/login/') 
def channels_delete(request, channel_id):
    channel = get_object_or_404(UserCreatedChannel, pk=channel_id)
    if not channel.created_by == request.user:
        raise Http404
    
    name = channel.channel_name    
    channel.delete()
    messages.success(request, "Your channel '%s' has been deleted." % name)
    return HttpResponseRedirect(reverse('channels_list')) 
                
