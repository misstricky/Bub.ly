from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from forms import RegisterForm, LoginForm

def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user_id = form.save()
            request.session['user_id'] = user_id
            return HttpResponseRedirect("/")
    else:
        form = RegisterForm()
    return render_to_response("register.html", {'form': form}, context_instance=RequestContext(request))

def login(request):
    form = LoginForm()
    return render_to_response("login.html", {'form': form}, context_instance=RequestContext(request))

def logout(request):
    pass