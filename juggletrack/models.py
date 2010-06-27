from django.db import models
from django.core.urlresolvers import reverse

class Achievement(models.Model):
    KIND_CHOICES = (
        ('STUNT', 'Stunt'),
        ('PATTERN', 'Pattern')
    )

    name = models.CharField(max_length=255)
    points = models.IntegerField()
    kind = models.CharField(max_length=255, choices=KIND_CHOICES)
    date_created = models.DateTimeField('date created')
   
    notation_type = models.CharField(max_length=255, choices=(('JML', 'JML'), ('SITESWAP','Siteswap')))
    notation = models.TextField()

    def __unicode__(self):
        return self.name

    def eventify(self):
        return 'There\'s a new achievement to be had: <a href="%s">%s</a>' % (self.view(), self.name)

    def view(self):
        return reverse('juggletrack.views.achievement', args=(self.id,))

class Juggler(models.Model):
    name = models.CharField(max_length=255)
    date_created = models.DateTimeField('date created')
    achievement = models.ManyToManyField(Achievement, through='JugglerAchievement')
    
    def __unicode__(self):
        return self.name

    def eventify(self):
        return 'A new juggler joins our ranks: <a href="%s">%s</a>' % (self.view(), self.name)

    def view(self):
        return reverse('juggletrack.views.juggler', args=(self.id,))

    def score(self):
        score = 0
        for ach in self.achievement.all():
            score += ach.points
        return score

class JugglerAchievement(models.Model):
    juggler = models.ForeignKey(Juggler)
    achievement = models.ForeignKey(Achievement)
    date_created = models.DateTimeField('date achieved', auto_now_add=True)
    
    def __unicode__(self):
        return self.juggler.name + ": " + self.achievement.name

    def eventify(self):
        return '<a href="%s">%s</a> has achieved <a href="%s">%s</a>' % \
                (self.juggler.view(), self.juggler.name, self.achievement.view(), self.achievement.name)
