from django.conf.urls.defaults import *
import os

urlpatterns = patterns('juggletrack.views',
    (r'^$', 'index'),
    (r'^jugglers', 'jugglers'),
    (r'^juggler/(?P<juggler_id>\d+)/$', 'juggler'),
    (r'^juggler/(?P<juggler_id>\d+)/alter_achievements$', 'juggler_alter_ach'),
    (r'^achievement/(?P<achievement_id>\d+)/$', 'achievement'),
    (r'^juggler_diff', 'juggler_diff'),
    (r'^achievements', 'achievements'),
    (r'^dashboard', 'dashboard'),
)
urlpatterns += patterns('',
    (r'^site_media/(?P<path>.*)$',
     'django.views.static.serve',
     {'document_root': os.path.join(os.path.abspath(os.path.curdir), 'juggletrack', 'static')}
    ),
)
