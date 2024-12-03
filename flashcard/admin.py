from django.contrib import admin

from flashcard import models
from flashcard.services.iflashcardservice import IFlashcardService
from flashcard.services.phrase_flashcard_service import PhraseFlashcardService
from flashcard.services.verse_flashcard_service import VerseFlashcardService

admin.site.register(models.Flashcard)
admin.site.register(models.FlashcardSet)
