from django import template
from ninja.models import SiteSettings

register = template.Library()

@register.simple_tag
def site_name():
    try:
        site = SiteSettings.objects.values_list('name', flat=True).get(site_id='main')
    except SiteSettings.DoesNotExist:
        site = "App Name"
    return site

@register.simple_tag
def site_title():
    try:
        site = SiteSettings.objects.values_list('title', flat=True).get(site_id='main')
    except SiteSettings.DoesNotExist:
        site = "App Title"
    return site

@register.simple_tag
def site_description():
    try:
        site = SiteSettings.objects.values_list('description', flat=True).get(site_id='main')
    except SiteSettings.DoesNotExist:
        site = "Description"
    return site

@register.filter(name='zip')
def zip_lists(a, b):
  return zip(a, b)

