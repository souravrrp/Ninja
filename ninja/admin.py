from django.contrib import admin

# Register your models here.
from .models import SiteSettings

class SiteSettingsAdmin(admin.ModelAdmin):
   list_display = ('site_id', 'name', 'title')
   search_fields = ('name',)
admin.site.register(SiteSettings, SiteSettingsAdmin)
