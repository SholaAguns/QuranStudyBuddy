import random

from django.db.models import Q
from django.utils.timezone import now
from quran.models import Word, Chapter, WordTranslation
from flashcard.models import Flashcard
from flashcard.services.iflashcardservice import IFlashcardService

def populate_flashcards(amount, ids, flashcardset):
    selected_ids = random.sample(ids, min(amount, len(ids)))

    selected_words = Word.objects.filter(id__in=selected_ids)

    for word in selected_words:
        flashcard = Flashcard()
        flashcard.flashcardset = flashcardset
        flashcard.question = word.text_uthmani
        flashcard.answer = word.translation.text
        flashcard.save()


class WordFlashcardService(IFlashcardService):
    service_type = "Word"

    number_exclusion_filter = ~Q(text_uthmani__regex=r'^\d+$') & ~Q(translation__text__regex=r'^\(\d+\)$')

    def get_request_types(self):
        return ["default", "byIds", "byJuz", "byRange"]

    def get_id_options(self, user):
        all_chapters = Chapter.objects.all()
        options = []
        for chapter in all_chapters:
            label = f'{chapter.id} - {chapter.name_simple}'
            options.append({
                'label': label,
                'value': chapter.id
            })
        return options

    def get_juz_options(self, user):
        return [{'label': f'Juz {i}', 'value': i} for i in range(1, 31)]

    def get_category_options(self, user):
        pass

    def get_range_options(self, user):
        return self.get_id_options(user)

    def get_flashcards(self, flashcardset, amount):
        all_word_ids = list(
            Word.objects.filter(self.number_exclusion_filter)
            .values_list('id', flat=True)
        )

        date_now = now()
        flashcardset.type = self.service_type
        flashcardset.amount = amount
        flashcardset.created_dt = date_now
        flashcardset.title = f'{flashcardset.type}_{date_now}'
        print(self.service_type)
        print(flashcardset.type)
        flashcardset.save()
        populate_flashcards(amount, all_word_ids, flashcardset)
        flashcardset.save()
        return flashcardset

    def get_flashcards_by_category(self, flashcardset, amount, category):
        pass

    def get_flashcards_by_juz(self, flashcardset, amount, juz_list):
        word_ids = list(
            Word.objects.filter(verse__juz_number__in=juz_list)
            .filter(self.number_exclusion_filter)
            .values_list('id', flat=True)
        )

        date_now = now()
        flashcardset.type = self.service_type
        flashcardset.amount = amount
        flashcardset.created_dt = date_now
        flashcardset.title = f'{flashcardset.type}_by_juz_{date_now}'
        flashcardset.save()
        populate_flashcards(amount, word_ids, flashcardset)
        flashcardset.save()

        return flashcardset

    def get_flashcards_by_ids(self, flashcardset, amount, id_list):
        word_ids = list(
            Word.objects.filter(verse__chapter__id__in=id_list)
            .filter(self.number_exclusion_filter)
            .values_list('id', flat=True)
        )

        date_now = now()
        flashcardset.type = self.service_type
        flashcardset.amount = amount
        flashcardset.created_dt = date_now
        flashcardset.title = f'{flashcardset.type}_by_ids_{date_now}'
        flashcardset.save()
        populate_flashcards(amount, word_ids, flashcardset)
        flashcardset.save()

        return flashcardset

    def get_flashcards_by_range(self, flashcardset, amount, start, end):
        word_ids = list(
            Word.objects.filter(
                verse__chapter__id__gte=start,
                verse__chapter__id__lte=end
            )
            .filter(self.number_exclusion_filter)
            .values_list('id', flat=True)
        )

        date_now = now()
        flashcardset.type = self.service_type
        flashcardset.amount = amount
        flashcardset.created_dt = date_now
        flashcardset.title = f'{flashcardset.type}_by_range_{date_now}'
        flashcardset.save()
        populate_flashcards(amount, word_ids, flashcardset)
        flashcardset.save()

        return flashcardset
