from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from models import Juggler, Achievement, JugglerAchievement
from tagging.models import Tag, TaggedItem

def index(request):
    return HttpResponseRedirect(reverse('juggletrack.views.jugglers'))

def jugglers(request):
    jugglers = list(Juggler.objects.all().order_by('name'))
    return render_to_response('index.html', {'jugglers': jugglers, 'request':request})

def achievement(request, achievement_id):
    ach = get_object_or_404(Achievement, pk=achievement_id)
    jugglers = JugglerAchievement.objects.filter(achievement=ach).order_by('date_created')
    return render_to_response('achievement.html', {'achievement': ach,
                                                   'jugglers': jugglers,
                                                   'tags': ",".join([t.name for t in Tag.objects.get_for_object(ach)]),
                                                   'request':request})

def achievement_settags(request, achievement_id):
    ach = get_object_or_404(Achievement, pk=achievement_id)
    if 'tags' in request.POST:
        Tag.objects.update_tags(ach, request.POST.get('tags'))
    return HttpResponseRedirect(reverse('juggletrack.views.achievement', args=(achievement_id,)))

def achievements_with_tag(request, tag_str):
    tag = Tag.objects.get(name=tag_str)
    raw_achievements = TaggedItem.objects.get_by_model(Achievement, tag)

    return render_to_response('achievements_with_tag.html', {'tag': tag, 
                                                            'achievements': raw_achievements,
                                                            'request': request})

def achievements(request):
    achievements = Achievement.objects.all()
    return render_to_response('achievements.html', {'achievements': achievements, 'request': request})

def juggler(request, juggler_id):
    juggler = get_object_or_404(Juggler, pk=juggler_id)
    achievements = list(JugglerAchievement.objects.filter(juggler=juggler))
    achievements.sort(cmp=lambda x,y: cmp(x.achievement.value(), y.achievement.value()))
    all_achievements = Achievement.objects.all()
    raw_ach = [x.achievement for x in achievements]
    unachieved = [x for x in all_achievements if x not in raw_ach]
    unachieved.sort(cmp=lambda x,y: cmp(x.value(), y.value()))
    
    all_achieved_values = [x.achievement.value() for x in achievements]
    all_unachieved_values = [x.value() for x in unachieved]
    achieved_values = []
    unachieved_values = []
    for values in all_achieved_values:
        if values not in achieved_values:
            achieved_values.append(values)
    for values in all_unachieved_values:
        if values not in unachieved_values:
            unachieved_values.append(values)
            
    return render_to_response('juggler.html', {'juggler': juggler,
                                               'achievements': achievements,
                                               'unachieved': unachieved,
                                               'achieved_values': achieved_values,
                                               'unachieved_values': unachieved_values,
                                               'request': request})

def juggler_alter_ach(request, juggler_id):
    j = get_object_or_404(Juggler, pk=juggler_id)
    if 'add' in request.POST:
        for ach_to_add in request.POST.getlist('add'):
            ach = get_object_or_404(Achievement, pk=ach_to_add)
            ja = JugglerAchievement(juggler=j, achievement=ach)
            ja.save()
    if 'remove' in request.POST:
        for ach_to_rm in request.POST.getlist('remove'):
            ach = get_object_or_404(Achievement, pk=ach_to_rm)
            jaset = JugglerAchievement.objects.filter(juggler=j, achievement=ach)
            jaset[0].delete()
            
    return HttpResponseRedirect(reverse('juggletrack.views.juggler', args=(j.id,)))

def juggler_diff(request):
    juggler_ids = request.GET.getlist('juggler')
    juggler1 = get_object_or_404(Juggler, pk=juggler_ids[0])
    juggler2 = get_object_or_404(Juggler, pk=juggler_ids[1])
    (only1, only2) = do_juggler_diff(juggler1, juggler2)
    model = {'juggler1' : juggler1,
             'juggler2' : juggler2,
             'only1' : only1,
             'only2' : only2}
    model['request'] = request
    return render_to_response('juggler_diff.html', model)
                                                    
    
def do_juggler_diff(juggler1, juggler2):
    ja1 = JugglerAchievement.objects.filter(juggler=juggler1)
    ja2 = JugglerAchievement.objects.filter(juggler=juggler2)
    ach1 = [a.achievement for a in ja1]
    ach2 = [a.achievement for a in ja2]
    only1 = [a for a in ach1 if a not in ach2]
    only2 = [a for a in ach2 if a not in ach1]
    return (only1, only2)

def dashboard(request):
    def eventify(event):
        return { 'created': event.date_created, 'description': event.eventify() }

    recent_juggler_achievements = list(JugglerAchievement.objects.order_by('-date_created')[:5])
    recent_added_achievements = list(Achievement.objects.order_by('-date_created')[:5])
    recent_jugglers = list(Juggler.objects.order_by('-date_created')[:5])

    recent_events = reversed(sorted([eventify(e) for e in recent_juggler_achievements + recent_added_achievements + recent_jugglers], key=lambda e: e['created']))

    return render_to_response('dashboard.html', {'events': recent_events, 'request':request})
