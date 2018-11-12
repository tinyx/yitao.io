from django.contrib import admin

from models import Event, EventClass

class EventAdmin(admin.ModelAdmin):
    pass

class EventClassAdmin(admin.ModelAdmin):
    pass

admin.site.register(Event)
admin.site.register(EventClass)
