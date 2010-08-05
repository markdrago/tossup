from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponseRedirect, Http404, HttpResponse, HttpResponseForbidden
from django.core.urlresolvers import reverse
from tagging.models import Tag, TaggedItem

import json
from datetime import datetime

from juggletrack.models import Achievement, JugglerAchievement, AchievementValueLog

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
    return HttpResponseRedirect(reverse('juggletrack.views.achievement.achievement', args=(achievement_id,)))

def achievements_with_tag(request, tag_str):
    tag = Tag.objects.get(name=tag_str)
    raw_achievements = TaggedItem.objects.get_by_model(Achievement, tag)

    return render_to_response('achievements_with_tag.html', {'tag': tag, 
                                                            'achievements': raw_achievements,
                                                            'request': request})

def achievements(request):
    achievements = Achievement.objects.all()
    return render_to_response('achievements.html', {'achievements': achievements, 'request': request})

def achievement_add(request, achievement_id=None):
    if not request.user.is_authenticated():
        return HttpResponseForbidden()

    if request.method != 'POST':
        context = None
        attrs = ('id', 'name', 'kind', 'notation_type', 'notation')
        if achievement_id is None:
            context = dict([(attr, '') for attr in attrs])
            context['tags'] = ''
        else:
            ach = get_object_or_404(Achievement, pk=achievement_id)
            context = dict([(attr, getattr(ach, attr)) for attr in attrs])
            context['tags'] = ",".join([t.name for t in Tag.objects.get_for_object(ach)])

        context['request'] = request
        return render_to_response('achievement_add.html', context)
    
    name = request.POST['name']
    kind = request.POST['kind']
    tags = request.POST['tags']
    notation_type = request.POST['notation_type']
    notation = request.POST['notation']
    created_by = request.user.get_profile()
    
    if achievement_id is None:
        ach = Achievement(name=name, kind=kind, notation_type=notation_type,
                          notation=notation, date_created=datetime.today(),
                          created_by=created_by)
    else:
        ach = get_object_or_404(Achievement, pk=achievement_id)
        ach.name = name
        ach.kind = kind
        ach.notation_type = notation_type
        ach.notation = notation
    ach.save()
    Tag.objects.update_tags(ach, tags)
    
    return HttpResponseRedirect(reverse('juggletrack.views.achievement.achievement', args=(ach.id,)))

def achievement_value_chart_data(request, achievement_id):
    if not request.is_ajax():
        return Http404
    if request.method != 'GET':
        return Http404

    ach = get_object_or_404(Achievement, pk=achievement_id)
    
    #only include the last score log per day
    logs = changelog_data(AchievementValueLog.objects.filter(achievement=ach).order_by('date_created'))
    events = eventlog_data(AchievementValueLog.objects.filter(achievement=ach).order_by('date_created'))
    
    return HttpResponse(json.dumps({'info': events, 'data': logs}))
