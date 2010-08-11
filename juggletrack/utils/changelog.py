from django.db import models

from datetime import datetime
from calendar import timegm

from juggletrack.models import Juggler, Achievement, JugglerAchievement, AchievementEvent, AchievementValueLog, JugglerScoreLog

def log_achievement_event(juggler, achievement, kind):
    event = AchievementEvent(juggler=juggler, achievement=achievement,
                             kind=kind, date_created=datetime.today())
    event.save()
    return event

def log_achievement_values(event, log_all):
    affected = []
    if log_all:
        affected = list(Achievement.objects.annotate(num_j=models.Count('juggler')).filter(num_j__gt=1))
    
    if event.achievement not in affected:
        affected.append(event.achievement)

    for a in affected:
        value = a.value()
        if value == 101:
            value = None
        log = AchievementValueLog(achievement=a, event=event, value=value,
                                  date_created=event.date_created)
        log.save()

def log_juggler_scores(event, log_all):
    if log_all:
        affected = list(Juggler.objects.annotate(num_ach=models.Count('achievement')).filter(num_ach__gt=0))
    else:
        jas = list(JugglerAchievement.objects.filter(achievement=event.achievement))
        affected = map(lambda x: x.juggler, jas)
    
    if event.juggler not in affected:
        affected.append(event.juggler)

    for j in affected:
        log = JugglerScoreLog(juggler=j, event=event, score=j.score(),
                              date_created=event.date_created)
        log.save()

def eventlog_data(dataset):
    data = []
    endingscores = []
    days = []
    prevlogday = None
    for log in dataset:
        day = log.date_created.date()
        if(day == prevlogday):
            prevlogday = day
            data[-1][1] += '<br />' + str(log.event)
            endingscores[-1] = log.datapoint()
            continue
        prevlogday = day
        logtime = timegm(log.date_created.timetuple()) * 1000
        days.append(day)
        endingscores.append(log.datapoint())
        data.append([logtime, str(log.event)])

    #prepend every data item with the ending score for that day
    for i in range(len(data)):
        score = '%.2f' % (endingscores[i],)
        day = days[i].strftime('%B %d')
        data[i][1] =  day + ' -- ' + score + '<br />' + data[i][1]
    return data

def changelog_data(dataset):
    data = []
    prevlogday = None
    for log in dataset:
        day = log.date_created.date()
        if (day == prevlogday):
            data[-1][1] = log.datapoint()
            continue
        prevlogday = day
        logtime = timegm(log.date_created.timetuple()) * 1000
        data.append([logtime, log.datapoint()])
    return data

