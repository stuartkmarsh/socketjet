from django.shortcuts import render_to_response 
from django.http import HttpResponseForbidden, HttpResponse, HttpResponseRedirect  
from django.shortcuts import get_object_or_404
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt 
from django.core.urlresolvers import reverse

from common.models import ApiAccount, ClientUserPermissions      
import hmac
import hashlib
import urllib
import urllib2  
import json            

VALID_HOME = ('localhost',)

def home(request):
    if not request.site_name in VALID_HOME:
        return HttpResponseRedirect(reverse('app_home'))
    else:
        return render_to_response('home.html', {}, context_instance=RequestContext(request))

def test_index(request):
    if request.user.is_superuser:
        return render_to_response('test_index.html', context_instance=RequestContext(request))
    else:
        return HttpResponseForbidden()
        
def chat(request):
    if request.user.is_superuser:
        return render_to_response('chat.html', context_instance=RequestContext(request))
    else:
        return HttpResponseForbidden()

@csrf_exempt    
def auth(request):
    if not request.user.is_authenticated:
        return HttpResponseForbidden
        
    if not request.method == 'POST':
        return HttpResponseForbidden


    api_key = request.POST.get('api_key', None)
    conn_id = request.POST.get('conn_id', None)
    channel = request.POST.get('channel', None)
        
    if api_key == None or conn_id == None:
        return HttpResponseForbidden
    
    account = get_object_or_404(ApiAccount, api_key=api_key)
    not_auth = False 
    
    # get permissions for user
    try:
        perms = ClientUserPermissions.objects.get(client_user=request.user, api_account=account)
    except:
        perms = None       
    
    if channel:
        if channel.lower()[:7] == 'private':
            if not perms:
                not_auth = True
            else:            
                perm_channels = perms.private_channels.all()     
                for p in perm_channels:
                    if p.channel_name == channel:
                        break
                else:
                    not_auth = True 
                    
    if perms:
        if perms.is_admin:
            not_auth = False
                
    if not_auth:
        return HttpResponse(json.dumps({'message':'insufficient permissions'}), mimetype="application/json")
    
    secret = str(account.secret_key)     
    
    # data can be conn_id:channel for private, or just conn_id for non-private
    data = '%s:%s' % (conn_id, api_key)
    data = hmac.new(secret, msg=data, digestmod=hashlib.sha256).hexdigest() 
    params = urllib.urlencode({'api_key':api_key, 
                               'conn_id':conn_id, 
                               'channel':channel or 'none',
                               'action':'auth', 
                               'data':data}) 
    
    try:
        urllib2.urlopen('http://localhost:8002/socket_push/', data=params)
    except Exception as ex:
        print ex
    
    return HttpResponse(json.dumps({'message':'authenticating'}), mimetype="application/json")
