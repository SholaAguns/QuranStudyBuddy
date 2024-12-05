import random

from django.http import JsonResponse
from django.utils.timezone import now

from arabic.models import Phrase
from flashcard.models import Flashcard
from flashcard.services.iflashcardservice import IFlashcardService


def populate_flashcards(amount, ids, flashcardset):
    selected_ids = random.sample(ids, min(amount, len(ids)))

    selected_phrases = Phrase.objects.filter(id__in=selected_ids)

    for phrase in selected_phrases:
        flashcard = Flashcard()
        flashcard.flashcardset = flashcardset
        flashcard.question = phrase.text
        flashcard.answer = phrase.translation
        flashcard.image = phrase.image
        flashcard.save()


class PhraseFlashcardService(IFlashcardService):

    service_type = "Phrase"

    def get_category_options(self, user):
        phrase_categories = list(
            Phrase.objects.filter(user=user).values_list('category', flat=True)
        )
        unique_categories = list(set(category.lower() for category in phrase_categories))

        options = []
        for cat in unique_categories:
            options.append({
                'label': cat,
                'value': cat
            })
        return options

    def get_range_options(self, user):
        pass

    def get_juz_options(self, user):
        pass

    def get_id_options(self, user):
        all_phrases = Phrase.objects.filter(user=user)
        options = []
        for phrase in all_phrases:
            options.append({
                'label': phrase.text,
                'value': phrase.id
            })
        return options


    def get_request_types(self):
        return ["default", "byIds", "byCategory"]

    def get_flashcards(self, flashcardset, amount):
        all_phrase_ids = list(Phrase.objects.filter(user=flashcardset.user).values_list('id', flat=True))

        date_now = now()
        flashcardset.type = self.service_type
        flashcardset.amount = amount
        flashcardset.created_dt = date_now
        flashcardset.title = f'{flashcardset.type}_{date_now}'
        flashcardset.save()
        populate_flashcards(amount, all_phrase_ids, flashcardset)
        flashcardset.save()

        return flashcardset

    def get_flashcards_by_juz(self, flashcardset, amount, juz_list):
        pass

    def get_flashcards_by_ids(self, flashcardset, amount, id_list):
        phrase_ids = list(
            Phrase.objects.filter(id__in=id_list, user=flashcardset.user).values_list('id', flat=True)
        )

        date_now = now()
        flashcardset.type = self.service_type
        flashcardset.amount = amount
        flashcardset.created_dt = date_now
        flashcardset.title = f'{flashcardset.type}_by_juz_{date_now}'
        flashcardset.save()
        populate_flashcards(amount, phrase_ids, flashcardset)
        flashcardset.save()

        return flashcardset

    def get_flashcards_by_range(self, flashcardset, amount, start, end):
        pass

    def get_flashcards_by_category(self, flashcardset, amount, category):
        phrase_ids = list(
            Phrase.objects.filter(category=category, user=flashcardset.user).values_list('id', flat=True)
        )

        date_now = now()
        flashcardset.type = self.service_type
        flashcardset.amount = amount
        flashcardset.created_dt = date_now
        flashcardset.title = f'{flashcardset.type}_by_category_{date_now}'
        flashcardset.save()
        populate_flashcards(amount, phrase_ids, flashcardset)
        flashcardset.save()

        return flashcardset
