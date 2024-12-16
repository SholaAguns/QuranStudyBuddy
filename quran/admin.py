from django.contrib import admin
from . import models

admin.site.register(models.Chapter)
admin.site.register(models.TranslatedName)
admin.site.register(models.VerseTranslation)
admin.site.register(models.Verse)
admin.site.register(models.WordTranslation)
admin.site.register(models.Word)
admin.site.register(models.WordTransliteration)

