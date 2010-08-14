from django.conf import settings
from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^$', 'shortener.views.home'),
    (r'^shorten_url/$', 'shortener.views.shorten_url'),
    (r'^file_upload/$', 'shortener.views.file_upload'),
    (r'^_register/$', 'accounts.views.register'),
    (r'^_login/$', 'accounts.views.login'),
    (r'^_logout/$', 'accounts.views.logout'),
    (r'^_settings/$', 'accounts.views.settings'),
    (r'^(?P<slug>[\w]+)/$', 'shortener.views.expand_url'),
)

if settings.DEBUG:
    urlpatterns +=  patterns('',
        (r'^static/(?P<path>.*)$', 'django.views.static.serve', { 'document_root': settings.MEDIA_ROOT }),
    )
