from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from models import Juggler, Achievement, JugglerAchievement

def index(request):
    jugglers = list(Juggler.objects.all().order_by('name'))
    jugglers.sort(cmp=lambda x,y: cmp(y.score,x.score))
    return render_to_response('index.html', {'jugglers': jugglers})

def juggler(request, juggler_id):
    juggler = get_object_or_404(Juggler, pk=juggler_id)
    achievements = JugglerAchievement.objects.filter(juggler=juggler).order_by('achievement__points')
    all_achievements = Achievement.objects.all()
    raw_ach = [x.achievement for x in achievements]
    unachieved = [x for x in all_achievements if x not in raw_ach]
    return render_to_response('juggler.html', {'juggler': juggler,
                                               'achievements': achievements,
                                               'unachieved': unachieved})

def juggler_alter_ach(request, juggler_id):
    j = get_object_or_404(Juggler, pk=juggler_id)
    if 'add' in request.POST:
        for ach_to_add in request.POST.getlist('add'):
            ach = get_object_or_404(Achievement, pk=ach_to_add)
            ja = JugglerAchievement(juggler=j, achievement=ach)
            ja.save()
    if 'remove' in request.POST:
        print "post remove: %s" % (request.POST.getlist('remove'),)
        for ach_to_rm in request.POST.getlist('remove'):
            ach = get_object_or_404(Achievement, pk=ach_to_rm)
            jaset = JugglerAchievement.objects.filter(juggler=j, achievement=ach)
            jaset[0].delete()
            
    return HttpResponseRedirect(reverse('juggletrack.views.juggler', args=(j.id,)))

