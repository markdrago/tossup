from django.core.management.base import NoArgsCommand
from sys import stdin
from juggletrack.models import Juggler, Achievement, JugglerAchievement, AchievementEvent, AchievementValueLog, JugglerScoreLog

def warn():
    print "Warning: This will remove all entries from the changelog."
    print "The affected models are AchievementEvent, AchievementValueLog,"
    print "and JugglerScoreLog.  The data in the logs will be reconstructed"
    print "from the achievements a juggler currently has.  Any data in the"
    print "logs regarding the removal of an achievement will be lost and"
    print "can not be recreated."
    print
    print "Hit ENTER to continue or Ctrl+C to quit."
    stdin.readline()

class Command(NoArgsCommand):
    def handle_noargs(self, **options):
        warn()
    
        #maps juggler ids to a list of achievements they have achieved
        self.j_map = {}
        
        #maps ach ids to a list of juggler ids that have achieved it
        self.ach_map = {}
        
        #delete all pre-existing log data
        AchievementEvent.objects.all().delete()
        AchievementValueLog.objects.all().delete()
        JugglerScoreLog.objects.all().delete()

        #generate achievementevents from juggler achievements
        all_ach = JugglerAchievement.objects.all().order_by('date_created')
        for ach in all_ach:
            #shorthand
            ach_id = ach.achievement.id
            j_id = ach.juggler.id

            #record achievement
            if ach_id in self.ach_map:
                self.ach_map[ach_id].append(j_id)
            else:
                self.ach_map[ach_id] = [j_id,]
            
            #increment juggler count
            new_juggler = False
            if j_id in self.j_map:
                self.j_map[j_id].append(ach_id)
            else:
                self.j_map[j_id] = [ach_id,]
                new_juggler = True

            #store achievement event
            ae = AchievementEvent(juggler=ach.juggler,
                                  achievement=ach.achievement,
                                  date_created=ach.date_created,
                                  kind='ADD')
            ae.save()
            
            #if the 1st achievement is being added for this juggler we need to
            #log a new value for EVERY achievement (that has been achieved at
            #least twice) and EVERY juggler (with at least one achievement)
            #because the total number of jugglers has changed and that is
            #used in the value calculation
            affected_ach = [ach.achievement.id,]
            affected_j = self.ach_map[ach_id]
            if new_juggler:
                affected_ach = [x for x in self.ach_map.keys() if len(self.ach_map[x]) > 1]
                affected_j = self.j_map.keys()

            if ach.achievement.id not in affected_ach:
                affected_ach.append(ach.achievement.id)

            #store achievement value log for all affected achievements
            for a in affected_ach:
                achievement = Achievement.objects.filter(id=a)[0]
                avl = AchievementValueLog(achievement=achievement, event=ae,
                                          value=self.get_ach_value(a),
                                          date_created=ach.date_created)
                avl.save()

            #store juggler score log for all affected jugglers
            for j in affected_j:
                juggler = Juggler.objects.filter(id=j)[0]
                jsl = JugglerScoreLog(juggler=juggler, event=ae,
                                      score=self.get_jug_score(j),
                                      date_created=ach.date_created)
                jsl.save()
        
    def get_ach_value(self, ach_id):
        numjug = len(self.j_map)
        achieved = len(self.ach_map[ach_id])
        return max(1, 100 - ((float(achieved - 1) / numjug) * 100))

    def get_jug_score(self, jug_id):
        total = 0
        for ach_id in self.j_map[jug_id]:
            total += self.get_ach_value(ach_id)
        return total

