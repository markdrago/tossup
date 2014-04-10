from django.conf.urls import patterns, url, include
from django.views.generic.base import RedirectView
from django.core.urlresolvers import reverse_lazy
import os

from juggletrack.feeds import ActivityFeedRss, ActivityFeedAtom

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
    (r'^other_stats', 'juggler.other_stats'),
    (r'^register$', 'auth.register'),
    (r'^register/(?P<juggler_id>\d+)/$', 'auth.register'),
    (r'^login$', 'auth.login_view'),
    (r'^logout$', 'auth.logout_view'),
)

urlpatterns += patterns('django.views.generic.simple',
    ('^$', RedirectView.as_view(url=reverse_lazy('juggletrack.views.juggler.collection'))),
)

rss_feeds = {'activity': ActivityFeedRss}
atom_feeds = {'activity': ActivityFeedAtom}
#urlpatterns += patterns('django.contrib.syndication.views',
#    (r'^feeds/rss/(?P<url>.*)$', 'feed', {'feed_dict': rss_feeds}),
#    (r'^feeds/atom/(?P<url>.*)$', 'feed', {'feed_dict': atom_feeds}),
#    (r'^feeds/(?P<url>.*)$', 'feed', {'feed_dict': atom_feeds}),
#)

urlpatterns += patterns('',
    (r'^site_media/(?P<path>.*)$',
     'django.views.static.serve',
     {'document_root': os.path.join(os.path.abspath(os.path.curdir), 'juggletrack', 'static')}
    ),
)

