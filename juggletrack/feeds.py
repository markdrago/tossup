from django.contrib.syndication.views import Feed
from django.utils.feedgenerator import Atom1Feed
from django.core.urlresolvers import reverse

from juggletrack.utils.events import get_recent_events

class ActivityFeedRss(Feed):
    title = "JuggleTrack Activity"
    description = "Updates on available achievements, juggler achievements, etc."

    def link(self):
        return 'http://juggling.statshappen.com' + reverse('juggletrack.views.juggler.collection')

    def items(self):
        return get_recent_events()

    def item_link(self, item):
        return 'http://juggling.statshappen.com' + item['view']
    
    def item_pubdate(self, item):
        return item['created']

class ActivityFeedAtom(ActivityFeedRss):
    feed_type = Atom1Feed
    subtitle = ActivityFeedRss.description
    
