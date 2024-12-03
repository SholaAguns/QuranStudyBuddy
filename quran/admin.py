from django.contrib import admin
from . import models

admin.site.register(models.Chapter)
admin.site.register(models.TranslatedName)
admin.site.register(models.Translation)
admin.site.register(models.Verse)
