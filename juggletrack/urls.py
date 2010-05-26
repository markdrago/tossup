from django.conf.urls.defaults import *

urlpatterns = patterns('juggletrack.views',
    (r'^$', 'index'),
    (r'^juggler/(?P<juggler_id>\d+)/$', 'juggler'),
    (r'^juggler/(?P<juggler_id>\d+)/add$', 'juggler_add_ach'),
)
