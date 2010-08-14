from django.shortcuts import render_to_response
from django.template import RequestContext
from forms import RegisterForm

def register(request):
    form = RegisterForm()
    return render_to_response("register.html", {'form': form}, context_instance=RequestContext(request))

def login(request):
    pass

def logout(request):
    pass