from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponseRedirect, Http404, HttpResponse, HttpResponseForbidden

from juggletrack.models import Juggler, Achievement, JugglerAchievement

def dashboard(request):
    def eventify(event):
        return { 'created': event.date_created, 'description': event.eventify() }
    def eventify_c(event, created):
        return { 'created': created, 'description': e.eventify() }

    recent_juggler_achievements = list(JugglerAchievement.objects.filter(challengeable_since__isnull=True).order_by('-date_created')[:5])
    recent_added_achievements = list(Achievement.objects.order_by('-date_created')[:5])
    recent_jugglers = list(Juggler.objects.order_by('-date_created')[:5])

    recent_challengeable_achievements = list(JugglerAchievement.objects.filter(challengeable_since__isnull=False).order_by('-challengeable_since')[:5])

    recent_events = reversed(sorted(
            [eventify(e) \
                for e in recent_juggler_achievements + recent_added_achievements + recent_jugglers] \
            + [eventify_c(e, e.challengeable_since) for e in recent_challengeable_achievements], \
        key=lambda e: e['created']))

    return render_to_response('dashboard.html', {'events': recent_events, 'request':request})
