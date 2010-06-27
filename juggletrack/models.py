from django.db import models

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

class Juggler(models.Model):
    name = models.CharField(max_length=255)
    date_created = models.DateTimeField('date created')
    achievement = models.ManyToManyField(Achievement, through='JugglerAchievement')
    
    def __unicode__(self):
        return self.name
    
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

