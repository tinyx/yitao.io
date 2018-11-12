from django.contrib import admin

from chrome_homepage.models import Website

# Register your models here.
class WebsiteAdmin(admin.ModelAdmin):
    pass

admin.site.register(Website)
