from django.template import RequestContext
from django.shortcuts import render_to_response

from connect_redis import get_client
redis_ob = get_client()

def home(request):
    try: 
        page = int(request.GET.get('page', 1))
        assert page >= 1
    except:
        page = 1
    if request.session.has_key("user_id"):
        user_id = request.session["user_id"]
        if redis_ob.hexists("user:%s" %str(user_id), "email"):
            url_ids = redis_ob.lrange("user:urls:%s" %str(user_id), (page-1)*50, page*50)
            if page > 1 and not url_ids: raise Http404
            urls = []
            for url_id in url_ids:
                urls.append(UrlModel.get_by_id(url_id=url_id))
            return render_to_response('home.html', {'urls': urls}, context_instance=RequestContext(request))
    return render_to_response('landing.html', {}, context_instance=RequestContext(request))
