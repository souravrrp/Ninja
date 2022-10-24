from turtle import title
from django.db import models

# # Create your models here.
# class signup(models.Model):
#     name = models.CharField(blank=True, null=True, max_length=100, default="App Name")
#     title = models.CharField(blank=True, null=True, max_length=100, default="App Title")
#     description = models.TextField(blank=True, null=True, default="Description")


SITE_ID_CHOICES = [
    ("main", "main"),
]
class SiteSettings(models.Model):
    site_id = models.CharField(max_length=50, choices=SITE_ID_CHOICES, default="main", editable=False)
    name = models.CharField(blank=True, null=True, max_length=100, default="App Name")
    title = models.CharField(blank=True, null=True, max_length=100, default="App Title")
    description = models.TextField(blank=True, null=True, default="Description")
    
    def __str__(self):
        return self.name

    def save(self):
        count = SiteSettings.objects.all().count()
        save_permission = SiteSettings.has_add_permission(self)

        if count < 1:
            super(SiteSettings, self).save()
        elif save_permission:
            super(SiteSettings, self).save()

    def has_add_permission(self):
        return SiteSettings.objects.filter(id=self.id).exists()