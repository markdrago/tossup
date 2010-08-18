from django.shortcuts import render_to_response

from juggletrack.utils.events import get_recent_events

def events(request):
    recent_events = get_recent_events()[0:10]
    return render_to_response('sidebar/events.html', {'events': recent_events})

def achievement_tags(request):
    return render_to_response('sidebar/achievement_tags.html')

