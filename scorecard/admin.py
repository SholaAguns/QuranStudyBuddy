from django.contrib import admin

from scorecard import models

admin.site.register(models.Scorecard)
admin.site.register(models.PhraseScore)
admin.site.register(models.VerseScore)
admin.site.register(models.VerseSelectionScore)
admin.site.register(models.WordScore)
