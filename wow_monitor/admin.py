from django.contrib import admin

from models import Character, SimcRank

class SimcRankAdmin(admin.ModelAdmin):
    readonly_fields = ('rating_time',)

admin.site.register(Character)
admin.site.register(SimcRank, SimcRankAdmin)
