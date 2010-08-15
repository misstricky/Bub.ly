from django.contrib import messages
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils.hashcompat import md5_constructor
from forms import RegisterForm, LoginForm, SettingsForm, generate_password

from connect_redis import get_client
redis_ob = get_client()

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
            user_id = redis_ob.get("user:email:%s" %md5_constructor(form.cleaned_data['email']).hexdigest())
            request.session['user_id'] = user_id
            next = request.POST.get("next", "/")
            return HttpResponseRedirect(next)
    else:
        # if user is already logged in redirect to /
        if request.session.has_key('user_id'): return HttpResponseRedirect("/")
        form = LoginForm()
    return render_to_response("landing.html", {'form': form}, context_instance=RequestContext(request))

def logout(request):
    request.session.flush()
    return HttpResponseRedirect("/")

def settings(request):
    # if user is not logged in raise 404
    if not request.session.has_key("user_id"): raise Http404
    user_id = request.session["user_id"]
    user_data = redis_ob.hgetall("user:%s" %user_id)
    if not user_data: raise Http404
    if request.method == "POST":
        form = SettingsForm(request.POST)
        if form.is_valid():
            user_email = redis_ob.hget("user:%s" %user_id, "email")
            redis_pipe = redis_ob.pipeline()
            if user_email != form.cleaned_data['email']:
                if redis_ob.exists("user:email:%s" %md5_constructor(form.cleaned_data['email']).hexdigest()):
                    message = "Another account is already associated with that email"
                    return render_to_response('settings.html', {'form': form, 'user_data': user_data, 'message': message}, context_instance=RequestContext(request))
                redis_pipe.rename("user:email:%s" %md5_constructor(user_email).hexdigest(), "user:email:%s" %md5_constructor(form.cleaned_data['email']).hexdigest()).hset("user:%s" %user_id, "email", form.cleaned_data['email'])
            salt, hsh = generate_password(form.cleaned_data['password'])
            redis_pipe.hset("user:%s" %user_id, "password", "%s$%s" %(salt, hsh))
            redis_pipe.execute()
            messages.add_message(request, messages.INFO, 'Your account settings are updated!')
            return HttpResponseRedirect("/")
    elif request.method =="DELETE":
        # delete user related data from redis
        user_data = redis_ob.hgetall("user:%s" %user_id)
        url_ids = redis_ob.lrange("user:urls:%s" %str(user_id), 0, -1)
        redis_ob.delete("user:email:%s" %md5_constructor(user_data.get("email")).hexdigest(), "user:%s" %user_id, "user:urls:%s" %user_id, "user:api_key:%s" %user_data.get("api_key"))
        
        # logout the user
        request.session.flush()
        return HttpResponse("success", mimetype="application/javascript")
    else:
        form = SettingsForm(initial={'email': user_data.get("email")})
    return render_to_response('settings.html', {'form': form, 'user_data': user_data}, context_instance=RequestContext(request))
