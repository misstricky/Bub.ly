from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^_register/$', 'accounts.views.register'),
    (r'^_login/$', 'accounts.views.login'),
    (r'^_logout/$', 'accounts.views.logout'),
    (r'^_settings/$', 'accounts.views.settings'),
)
