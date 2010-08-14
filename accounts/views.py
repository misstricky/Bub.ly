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
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            # get the id of the user and set session
            user_id = redis_ob.get("user:email:%s" %md5_constructor(form.cleaned_data['email']))
            request.session['user_id'] = user_id
            return HttpResponseRedirect("/")
    else:
        # if user is already logged in redirect to /
        if request.session['user_id']: return HttpResponseRedirect("/")
        form = LoginForm()
    return render_to_response("login.html", {'form': form}, context_instance=RequestContext(request))

def logout(request):
    request.session.pop('user_id', None)
    return render_to_response('logout.html', {}, context_instance=RequestContext(request))