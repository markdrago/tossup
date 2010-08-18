from juggletrack.models import Juggler, Achievement, JugglerAchievement

def get_recent_events():
    recent_juggler_achievements = list(JugglerAchievement.objects.filter(challengeable_since__isnull=True).order_by('-date_created')[:5])
    recent_added_achievements = list(Achievement.objects.order_by('-date_created')[:5])
    recent_jugglers = list(Juggler.objects.order_by('-date_created')[:5])

    recent_challengeable_achievements = list(JugglerAchievement.objects.filter(challengeable_since__isnull=False).order_by('-challengeable_since')[:5])

    recent_events = sorted(
            [eventify(e) \
                for e in recent_juggler_achievements + recent_added_achievements + recent_jugglers] \
            + [eventify_c(e, e.challengeable_since) for e in recent_challengeable_achievements], \
        key=lambda e: e['created'])

    recent_events.reverse()
    return recent_events

def eventify(event):
    return { 'created': event.date_created,
             'description': event.eventify(True),
             'desc_no_link': event.eventify(False),
             'view': event.view() }

def eventify_c(event, created):
    return { 'created': created,
             'description': e.eventify(True),
             'desc_no_link': e.eventify(False),
             'view': event.view() }

