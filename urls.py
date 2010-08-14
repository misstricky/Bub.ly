from django.conf import settings
from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^$', 'shortener.views.home'),
    (r'^_register/$', 'accounts.views.register'),
    (r'^_login/$', 'accounts.views.login'),
    (r'^_logout/$', 'accounts.views.logout'),
    (r'^_settings/$', 'accounts.views.settings'),
)

if settings.DEBUG:
    urlpatterns +=  patterns('',
        (r'^static/(?P<path>.*)$', 'django.views.static.serve', { 'document_root': settings.MEDIA_ROOT }),
    )
