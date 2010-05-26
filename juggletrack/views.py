from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponseRedirect
from models import Juggler, Achievement, JugglerAchievement

def index(request):
    jugglers = Juggler.objects.all().order_by('name')
    return render_to_response('index.html', {'jugglers': jugglers})

def juggler(request, juggler_id):
    juggler = get_object_or_404(Juggler, pk=juggler_id)
    achievements = juggler.achievement.order_by('points')
    all_achievements = Achievement.objects.all()
    unachieved = [x for x in all_achievements if x not in achievements]
    return render_to_response('juggler.html', {'juggler': juggler,
                                               'achievements': achievements,
                                               'unachieved': unachieved})

def juggler_add_ach(request, juggler_id):
    j = get_object_or_404(Juggler, pk=juggler_id)
    for ach_to_add in request.POST['achieved']:
        ach = get_object_or_404(Achievement, pk=ach_to_add)
        ja = JugglerAchievement(juggler=j, achievement=ach)
        ja.save()
    return HttpResponseRedirect(reverse('juggletrack.views.juggler', args=(j.id,)))
