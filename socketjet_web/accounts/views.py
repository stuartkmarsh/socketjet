from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext   
from django.contrib.auth import login, authenticate, logout
from django.http import HttpResponseRedirect 
from django.core.mail import send_mail  
from django.conf import settings
from django.core.urlresolvers import reverse 

from accounts.forms import *
from common.models import *

def register(request):
    if request.method == 'GET':
        form = RegistrationForm() 
    else:
        form = RegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            email = form.cleaned_data['email'] 
            app_name = form.cleaned_data['app_name']
            
            user = User.objects.create_user(username, email, password)
            ap = AccountPackage.objects.filter(is_starter=True)[0]
            up = AccountUserProfile.objects.create(user=user, account_package=ap)
            
            # create first api account
            api_account, user_perm = ApiAccount.objects.create_account(user, app_name) 
            
            # send user email
            send_mail('Socketjet Signup', 'http://%s/accounts/verify/%s/' % (settings.SITE_URL, up.auth_token), 
                      'support@socketjet.com', [email], fail_silently=True)
                   
            return render_to_response('wait_verification.html', {}, 
                                      context_instance=RequestContext(request))             
                   
    return render_to_response('registration.html', {'form':form}, context_instance=RequestContext(request)) 
    
def login_user(request):
    error = None
    
    if request.method == 'GET':
        form = LoginForm()
    else:
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data['username'], 
                                password=form.cleaned_data['password'])
            if user is not None:
                if user.is_active:
                    login(request, user) 
                    return HttpResponseRedirect(reverse('sites_list'))
                else:
                    error = 'inactive user'
            else:
                error = 'incorrect username or password'             
    
    return render_to_response('login.html', {'form':form, 'error':error}, 
                              context_instance=RequestContext(request))
   
def verify(request, auth_token):
    account_user  = get_object_or_404(AccountUserProfile, auth_token=auth_token)
    account_user.is_verified = True
    account_user.save()
    
    return render_to_response('verified.html', {}, context_instance=RequestContext(request)) 
    
def logout_user(request):
    logout(request)
    return HttpResponseRedirect(reverse('home'))
    