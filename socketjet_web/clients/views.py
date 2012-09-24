from django.shortcuts import render_to_response 
from django.template import RequestContext

def app_home(request):
    return render_to_response('app_home.html', {}, context_instance=RequestContext(request))
