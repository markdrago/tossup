from django.db import models

class Achievement(models.Model):
    name = models.CharField(max_length=255)
    points = models.IntegerField()
    kind = models.CharField(max_length=255)
    date_created = models.DateTimeField('date created')
    
    def __unicode__(self):
        return self.name

class Juggler(models.Model):
    name = models.CharField(max_length=255)
    date_created = models.DateTimeField('date created')
    achievement = models.ManyToManyField(Achievement, through='JugglerAchievement')
    
    def __unicode__(self):
        return self.name

class JugglerAchievement(models.Model):
    juggler = models.ForeignKey(Juggler)
    achievement = models.ForeignKey(Achievement)
    date_created = models.DateTimeField('date achieved')
    
    def __unicode__(self):
        return self.juggler.name + ": " + self.achievement.name

