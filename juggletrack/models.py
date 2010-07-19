from django.db import models
from django.core.urlresolvers import reverse

import tagging

class Achievement(models.Model):
    KIND_CHOICES = (
        ('STUNT', 'Stunt'),
        ('PATTERN', 'Pattern')
    )

    name = models.CharField(max_length=255)
    kind = models.CharField(max_length=255, choices=KIND_CHOICES)
    date_created = models.DateTimeField('date created')
    notation_type = models.CharField(max_length=255, choices=(('JML', 'JML'), ('SITESWAP','Siteswap')))
    notation = models.TextField()

    def __unicode__(self):
        return self.name
    
    def value(self):
        total = Juggler.objects.annotate(num_ach=models.Count('achievement')).filter(num_ach__gt=0).count()
        if total == 0: return 0
        achieved = self.juggler_set.count()
        if achieved == 0: return 101
        return max(1, 100 - ((float(achieved - 1) / total) * 100))

    def eventify(self):
        return 'There\'s a new achievement to be had: <a href="%s">%s</a>' % (self.view(), self.name)

    def view(self):
        return reverse('juggletrack.views.achievement', args=(self.id,))

class JugglerAffiliation(models.Model):
    name = models.CharField(max_length=255)
    date_created = models.DateTimeField('date created')

    def __unicode__(self):
        return self.name

class Juggler(models.Model):
    name = models.CharField(max_length=255)
    date_created = models.DateTimeField('date created')
    affiliation = models.ForeignKey(JugglerAffiliation, null=True)
    achievement = models.ManyToManyField(Achievement, through='JugglerAchievement')
    
    def __unicode__(self):
        return self.name

    def eventify(self):
        return 'A new juggler joins our ranks: <a href="%s">%s</a>' % (self.view(), self.name)

    def view(self):
        return reverse('juggletrack.views.juggler', args=(self.id,))

    def score(self):
        total = 0
        for ach in self.achievement.all():
            if ach.value() > 100:
                continue
            total += ach.value()
        return total

class JugglerAchievement(models.Model):
    juggler = models.ForeignKey(Juggler)
    achievement = models.ForeignKey(Achievement)
    date_created = models.DateTimeField('date achieved', auto_now_add=True)
    
    def __unicode__(self):
        return self.juggler.name + ": " + self.achievement.name

    def eventify(self):
        return '<a href="%s">%s</a> has achieved <a href="%s">%s</a>' % \
                (self.juggler.view(), self.juggler.name, self.achievement.view(), self.achievement.name)

class AchievementEvent(models.Model):
    KIND_CHOICES = (
        ('ADD', 'Added'),
        ('REMOVE', 'Removed')
    )
    
    juggler = models.ForeignKey(Juggler)
    achievement = models.ForeignKey(Achievement)
    kind = models.CharField(max_length=255, choices=KIND_CHOICES)
    date_created = models.DateTimeField('date')
    
    def __unicode__(self):
        return self.juggler.name + " " + self.get_kind_display().lower() + " " + self.achievement.name

class AchievementValueLog(models.Model):
    achievement = models.ForeignKey(Achievement)
    event = models.ForeignKey(AchievementEvent)
    value = models.FloatField(null=True)
    date_created = models.DateTimeField('date')
    
    def __unicode__(self):
        return self.achievement.name + " was worth: " + self.value + " at " + self.date_created

    def datapoint(self):
        return self.value

class JugglerScoreLog(models.Model):
    juggler = models.ForeignKey(Juggler)
    event = models.ForeignKey(AchievementEvent)
    score = models.FloatField()
    date_created = models.DateTimeField('date')
    
    def __unicode__(self):
        return self.juggler.name + " had " + self.score + " points at " + self.date_created

    def datapoint(self):
        return self.score
