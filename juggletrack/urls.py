from django.conf.urls.defaults import *
import os

urlpatterns = patterns('juggletrack.views',
    (r'^$', 'index'),
    (r'^jugglers$', 'jugglers'),
    (r'^jugglers/overall_score_chart_data', 'jugglers_overall_score_chart_data'),
    (r'^juggler/(?P<juggler_id>\d+)/$', 'juggler'),
    (r'^juggler/(?P<juggler_id>\d+)/alter_achievements$', 'juggler_alter_ach'),
    (r'^juggler/(?P<juggler_id>\d+)/score_chart_data$', 'juggler_score_chart_data'),
    (r'^achievement/(?P<achievement_id>\d+)/$', 'achievement'),
    (r'^achievement/(?P<achievement_id>\d+)/settags$', 'achievement_settags'),
    (r'^achievement/(?P<achievement_id>\d+)/value_chart_data$', 'achievement_value_chart_data'),
    (r'^achievement/add$', 'achievement_add'),
    (r'^achievement/(?P<achievement_id>\d+)/edit$', 'achievement_add'),
    (r'^juggler_diff/$', 'juggler_diff'),
    (r'^juggler_diff/diff_chart_data', 'juggler_diff_chart_data'),
    (r'^achievements/tag/(?P<tag_str>\S+)', 'achievements_with_tag'),
    (r'^achievements', 'achievements'),
    (r'^dashboard', 'dashboard'),
    (r'^register$', 'register'),
    (r'^register/(?P<juggler_id>\d+)/$', 'register'),
    (r'^login$', 'login_view'),
    (r'^logout$', 'logout_view'),
)
urlpatterns += patterns('',
    (r'^site_media/(?P<path>.*)$',
     'django.views.static.serve',
     {'document_root': os.path.join(os.path.abspath(os.path.curdir), 'juggletrack', 'static')}
    ),
)
