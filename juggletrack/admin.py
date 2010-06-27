from models import Juggler, Achievement, JugglerAchievement
from django.contrib import admin

class JugglerAdmin(admin.ModelAdmin):
    list_display = ('name', 'total_value')

class AchievementAdmin(admin.ModelAdmin):
    list_display = ('name', 'kind')

class JugglerAchievementAdmin(admin.ModelAdmin):
    list_display = ('juggler', 'achievement', 'date_created')

admin.site.register(Juggler, JugglerAdmin)
admin.site.register(Achievement, AchievementAdmin)
admin.site.register(JugglerAchievement, JugglerAchievementAdmin)

