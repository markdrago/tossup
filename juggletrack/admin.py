from models import Juggler, Achievement, JugglerAchievement, JugglerAffiliation
from django.contrib import admin

class JugglerAdmin(admin.ModelAdmin):
    list_display = ('get_name', 'score')

class AchievementAdmin(admin.ModelAdmin):
    list_display = ('name', 'kind', 'value')

class JugglerAchievementAdmin(admin.ModelAdmin):
    list_display = ('juggler', 'achievement', 'date_created')

class JugglerAffiliationAdmin(admin.ModelAdmin):
    list_display = ('name',)

admin.site.register(Juggler, JugglerAdmin)
admin.site.register(Achievement, AchievementAdmin)
admin.site.register(JugglerAchievement, JugglerAchievementAdmin)
admin.site.register(JugglerAffiliation, JugglerAffiliationAdmin)

