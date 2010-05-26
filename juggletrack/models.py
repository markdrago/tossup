from django.db import models

class Achievement(models.Model):
    KIND_CHOICES = (
        ('STUNT', 'Stunt'),
        ('PATTERN', 'Pattern')
    )

    name = models.CharField(max_length=255)
    points = models.IntegerField()
    kind = models.CharField(max_length=255, choices=KIND_CHOICES)
    date_created = models.DateTimeField('date created')
    
    def __unicode__(self):
        return self.name

class Juggler(models.Model):
    name = models.CharField(max_length=255)
    date_created = models.DateTimeField('date created')
    achievement = models.ManyToManyField(Achievement, through='JugglerAchievement')
    
    def __unicode__(self):
        return self.name
    
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

