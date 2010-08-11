from django.conf.urls.defaults import *
from django.core.urlresolvers import reverse
import os

urlpatterns = patterns('juggletrack.views',
    (r'^jugglers$', 'juggler.collection'),
    (r'^jugglers/overall_score_chart_data', 'juggler.overall_score_chart_data'),
    (r'^juggler/(?P<juggler_id>\d+)/$', 'juggler.detail'),
    (r'^juggler/(?P<juggler_id>\d+)/alter_achievements$', 'juggler.alter_ach'),
    (r'^juggler/(?P<juggler_id>\d+)/score_chart_data$', 'juggler.score_chart_data'),
    (r'^juggler_diff/$', 'juggler.diff'),
    (r'^juggler_diff/diff_chart_data', 'juggler.diff_chart_data'),
    (r'^achievement/(?P<achievement_id>\d+)/$', 'achievement.detail'),
    (r'^achievement/(?P<achievement_id>\d+)/settags$', 'achievement.set_tags'),
    (r'^achievement/(?P<achievement_id>\d+)/value_chart_data$', 'achievement.value_chart_data'),
    (r'^achievement/add$', 'achievement.add'),
    (r'^achievement/(?P<achievement_id>\d+)/edit$', 'achievement.add'),
    (r'^achievements/tag/(?P<tag_str>\S+)', 'achievement.collection_with_tag'),
    (r'^achievements', 'achievement.collection'),
    (r'^sidebar/events', 'sidebar.events'),
    (r'^sidebar/achievement_tags', 'sidebar.achievement_tags'),
    (r'^register$', 'auth.register'),
    (r'^register/(?P<juggler_id>\d+)/$', 'auth.register'),
    (r'^login$', 'auth.login_view'),
    (r'^logout$', 'auth.logout_view'),
)

urlpatterns += patterns('django.views.generic.simple',
    ('^$', 'redirect_to', {'url': reverse('juggletrack.views.juggler.collection')}),
)

urlpatterns += patterns('',
    (r'^site_media/(?P<path>.*)$',
     'django.views.static.serve',
     {'document_root': os.path.join(os.path.abspath(os.path.curdir), 'juggletrack', 'static')}
    ),
)

