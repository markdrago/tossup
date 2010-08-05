from django.conf.urls.defaults import *
from django.core.urlresolvers import reverse
import os

urlpatterns = patterns('juggletrack.views',
    (r'^jugglers$', 'juggler.jugglers'),
    (r'^jugglers/overall_score_chart_data', 'juggler.jugglers_overall_score_chart_data'),
    (r'^juggler/(?P<juggler_id>\d+)/$', 'juggler.juggler'),
    (r'^juggler/(?P<juggler_id>\d+)/alter_achievements$', 'juggler.juggler_alter_ach'),
    (r'^juggler/(?P<juggler_id>\d+)/score_chart_data$', 'juggler.juggler_score_chart_data'),
    (r'^achievement/(?P<achievement_id>\d+)/$', 'achievement.achievement'),
    (r'^achievement/(?P<achievement_id>\d+)/settags$', 'achievement.achievement_settags'),
    (r'^achievement/(?P<achievement_id>\d+)/value_chart_data$', 'achievement.achievement_value_chart_data'),
    (r'^achievement/add$', 'achievement.achievement_add'),
    (r'^achievement/(?P<achievement_id>\d+)/edit$', 'achievement.achievement_add'),
    (r'^juggler_diff/$', 'juggler.juggler_diff'),
    (r'^juggler_diff/diff_chart_data', 'juggler.juggler_diff_chart_data'),
    (r'^achievements/tag/(?P<tag_str>\S+)', 'achievement.achievements_with_tag'),
    (r'^achievements', 'achievement.achievements'),
    (r'^dashboard', 'dashboard.dashboard'),
    (r'^register$', 'auth.register'),
    (r'^register/(?P<juggler_id>\d+)/$', 'auth.register'),
    (r'^login$', 'auth.login_view'),
    (r'^logout$', 'auth.logout_view'),
)

urlpatterns += patterns('django.views.generic.simple',
    ('^$', 'redirect_to', {'url': reverse('juggletrack.views.juggler.jugglers')}),
)

urlpatterns += patterns('',
    (r'^site_media/(?P<path>.*)$',
     'django.views.static.serve',
     {'document_root': os.path.join(os.path.abspath(os.path.curdir), 'juggletrack', 'static')}
    ),
)

