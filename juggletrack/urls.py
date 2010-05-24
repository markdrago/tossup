from django.conf.urls.defaults import *

urlpatterns = patterns('juggletrack.views',
    (r'^$', 'index'),
    (r'^juggler.html$', 'juggler'),
)
