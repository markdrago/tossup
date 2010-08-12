from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponseRedirect, Http404, HttpResponse, HttpResponseForbidden
from django.core.urlresolvers import reverse

from calendar import timegm
from datetime import datetime

from juggletrack.models import Juggler, Achievement, JugglerAchievement, JugglerScoreLog
from juggletrack.utils import changelog

try:
    import json
except ImportError:
    import simplejson as json

def collection(request):
    jugglers = list(Juggler.objects.all())
    return render_to_response('jugglers.html', {'jugglers': jugglers, 'request':request})
    
def detail(request, juggler_id):
    juggler = get_object_or_404(Juggler, pk=juggler_id)
    all = JugglerAchievement.objects.filter(juggler=juggler)
    achievements = list(all.filter(challengeable_since__isnull=True))
    challengeable = list(all.filter(challengeable_since__isnull=False))
    achievements.sort(cmp=lambda x,y: cmp(x.achievement.value(), y.achievement.value()))
    challengeable.sort(cmp=lambda x,y: cmp(x.achievement.value(), y.achievement.value()))
    all_achievements = Achievement.objects.all()
    raw_ach = [x.achievement for x in achievements]
    unachieved = [x for x in all_achievements if x not in raw_ach]
    unachieved.sort(cmp=lambda x,y: cmp(x.value(), y.value()))
    
    all_achieved_values = [x.achievement.value() for x in achievements]
    all_unachieved_values = [x.value() for x in unachieved]
    achieved_values = []
    unachieved_values = []
    challengeable_values = []
    for values in all_achieved_values:
        if values not in achieved_values:
            achieved_values.append(values)
    for values in all_unachieved_values:
        if values not in unachieved_values:
            unachieved_values.append(values)

    has_user_account = False
    if juggler.user is not None:
        has_user_account = True

    #decide if this user should see the controls to change their achievements
    editable = False
    if request.user.is_authenticated() and request.user == juggler.user:
        editable = True

    return render_to_response('juggler.html', {'juggler': juggler,
                                               'achievements': achievements,
                                               'challengeable': challengeable,
                                               'unachieved': unachieved,
                                               'achieved_values': achieved_values,
                                               'unachieved_values': unachieved_values,
                                               'has_user_account': has_user_account,
                                               'editable': editable,                                               
                                               'request': request})

def alter_ach(request, juggler_id):
    j = get_object_or_404(Juggler, pk=juggler_id)
    
    if not request.user.is_authenticated() or request.user != j.user:
        return HttpResponseForbidden()
    
    if 'add' in request.POST:
        for ach_to_add in request.POST.getlist('add'):
            ach = get_object_or_404(Achievement, pk=ach_to_add)
            ja = JugglerAchievement(juggler=j, achievement=ach)
            ja.save()
            fully_record_achievement_event(j, ach, 'ADD')
    if 'challenge' in request.POST:
        for ach_to_challenge in request.POST.getlist('challenge'):
            ach = get_object_or_404(Achievement, pk=ach_to_challenge)
            ja = JugglerAchievement.objects.filter(juggler=j, achievement=ach)[0]
            ja.challengeable_since = datetime.today()
            ja.save()
            fully_record_achievement_event(j, ach, 'CHALLENGE')
    if 'remove' in request.POST:
        for ach_to_rm in request.POST.getlist('remove'):
            ach = get_object_or_404(Achievement, pk=ach_to_rm)
            jaset = JugglerAchievement.objects.filter(juggler=j, achievement=ach)
            jaset[0].delete()
            fully_record_achievement_event(j, ach, 'REMOVE')
            
    return HttpResponseRedirect(reverse('juggletrack.views.juggler.detail', args=(j.id,)))

def fully_record_achievement_event(juggler, achievement, kind):
    #if the 1st achievement is being added (or the last achievement is being
    #removed) for this juggler we need to log a new value for EVERY achievement
    #(that has been achieved at least twice) and EVERY juggler (with at least
    #one achievement) because the total number of jugglers has changed and
    #that is used in the value calculation
    log_all = False
    isAdd = kind == 'ADD'
    if ((isAdd and juggler.achievement.count() == 1) or
        ((not isAdd) and juggler.achievement.count() == 0)):
        log_all = True

    event = changelog.log_achievement_event(juggler, achievement, kind)
    changelog.log_achievement_values(event, log_all)
    changelog.log_juggler_scores(event, log_all)
    
def diff(request):
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

def diff_chart_data(request):
    if request.method != 'GET':
        raise Http404

    juggler_ids = request.GET.getlist('juggler')
    juggler1 = get_object_or_404(Juggler, pk=juggler_ids[0])
    juggler2 = get_object_or_404(Juggler, pk=juggler_ids[1])

    #only include the last score log per day
    data1 = {'label': juggler1.get_name(), 'data': changelog.changelog_data(JugglerScoreLog.objects.filter(juggler=juggler1).order_by('date_created'))}
    data2 = {'label': juggler2.get_name(), 'data': changelog.changelog_data(JugglerScoreLog.objects.filter(juggler=juggler2).order_by('date_created'))}

    event1 = changelog.eventlog_data(JugglerScoreLog.objects.filter(juggler=juggler1).order_by('date_created'))
    event2 = changelog.eventlog_data(JugglerScoreLog.objects.filter(juggler=juggler2).order_by('date_created'))
    
    return HttpResponse(json.dumps({'info': [event1, event2], 'data': [data1, data2]}))

def score_chart_data(request, juggler_id):
    if request.method != 'GET':
        raise Http404

    juggler = get_object_or_404(Juggler, pk=juggler_id)
    
    #only include the last score log per day
    logs = changelog.changelog_data(JugglerScoreLog.objects.filter(juggler=juggler).order_by('date_created'))
    events = changelog.eventlog_data(JugglerScoreLog.objects.filter(juggler=juggler).order_by('date_created'))

    return HttpResponse(json.dumps({'info': events, 'data': logs}))

def overall_score_chart_data(request):
    if request.method != 'GET':
        raise Http404

    #only include the last score log per day
    data = []
    logs = JugglerScoreLog.objects.all().order_by('date_created')

    prevlogday = None
    daymap = {}
    for log in logs:
        day = log.date_created.date()
        daymap[log.juggler.id] = log.score
        daytotal = sum(daymap.values())
        if (day == prevlogday):
            data[len(data)-1][1] = daytotal
            continue
        prevlogday = day
        logtime = timegm(log.date_created.timetuple()) * 1000
        data.append([logtime, daytotal])
    
    return HttpResponse(json.dumps(data))

def other_stats(request):
    return render_to_response('other_stats.html', {'request': request})

