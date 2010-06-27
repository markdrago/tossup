from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from models import Juggler, Achievement, JugglerAchievement

def index(request):
    return HttpResponseRedirect(reverse('juggletrack.views.jugglers'))

def jugglers(request):
    jugglers = list(Juggler.objects.all().order_by('name'))
    return render_to_response('index.html', {'jugglers': jugglers, 'request':request})

def achievement(request, achievement_id):
    ach = get_object_or_404(Achievement, pk=achievement_id)
    jugglers = JugglerAchievement.objects.filter(achievement=ach).order_by('date_created')
    percent = achieved_percent(ach)
    return render_to_response('achievement.html', {'achievement': ach,
                                                   'jugglers': jugglers,
                                                   'percent': percent, 'request':request})

def achievements(request):
    raw_achievements = Achievement.objects.all().order_by('points')
    achievements = []
    for rawach in raw_achievements:
        achievements.append({"ach":rawach, "percent": achieved_percent(rawach)})
    
    print(achievements)
    return render_to_response('achievements.html', {'achievements': achievements, 'request':request})

def achieved_percent(achievement):
    total_jugglers = Juggler.objects.all().count()    
    jas = JugglerAchievement.objects.filter(achievement=achievement).count()
    if jas == 0:
        return 0
    return (float(jas) / float(total_jugglers)) * 100

def juggler(request, juggler_id):
    juggler = get_object_or_404(Juggler, pk=juggler_id)
    achievements = JugglerAchievement.objects.filter(juggler=juggler).order_by('achievement__points')
    all_achievements = Achievement.objects.all()
    raw_ach = [x.achievement for x in achievements]
    unachieved = [x for x in all_achievements if x not in raw_ach]
    unachieved.sort(cmp=lambda x,y: cmp(x.points, y.points))
    
    all_achieved_points = [x.achievement.points for x in achievements]
    all_unachieved_points = [x.points for x in unachieved]
    achieved_points = []
    unachieved_points = []
    for points in all_achieved_points:
        if points not in achieved_points:
            achieved_points.append(points)
    for points in all_unachieved_points:
        if points not in unachieved_points:
            unachieved_points.append(points)
            
    return render_to_response('juggler.html', {'juggler': juggler,
                                               'achievements': achievements,
                                               'unachieved': unachieved,
                                               'achieved_points': achieved_points,
                                               'unachieved_points': unachieved_points,
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
    ja1 = JugglerAchievement.objects.filter(juggler=juggler1).order_by('achievement__points')
    ja2 = JugglerAchievement.objects.filter(juggler=juggler2).order_by('achievement__points')
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

    recent_events = [eventify(e) for e in recent_juggler_achievements + recent_added_achievements + recent_jugglers]

    return render_to_response('dashboard.html', {'events': recent_events, 'request':request})
