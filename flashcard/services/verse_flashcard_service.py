from django.utils.timezone import now
import random
from flashcard.models import Flashcard
from flashcard.services.iflashcardservice import IFlashcardService
from quran.models import Chapter, Verse


def populate_flashcards(amount, ids, flashcardset):
    selected_ids = random.sample(ids, min(amount, len(ids)))

    selected_verses = Verse.objects.filter(id__in=selected_ids)

    for verse in selected_verses:
        flashcard = Flashcard()
        flashcard.flashcardset = flashcardset
        flashcard.question = verse.text_uthmani
        flashcard.answer = verse.chapter.name_simple
        #flashcard.image.url = verse.image_url
        flashcard.save()

class VerseFlashcardService(IFlashcardService):
    service_type = "Verse"

    def get_request_types(self):
        request_types = [
            {
                'label': 'All verses',
                'value': 'default'

            },
            {
                'label': 'By chapter',
                'value': 'byIds'

            },
            {
                'label': 'By juz',
                'value': 'byJuz'

            },
            {
                'label': 'By chapter range',
                'value': 'byRange'

            }
        ]
        return request_types

    def get_juz_options(self, user):
        return [{'label': f'Juz {i}', 'value': i} for i in range(1, 31)]

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

    def get_range_options(self, user):
        return self.get_id_options(user)

    def get_category_options(self, user):
        pass

    def get_flashcards(self, flashcardset, amount):
        print("Inside get_flashcards ")
        all_verse_ids = list(Verse.objects.values_list('id', flat=True))

        date_now = now()
        flashcardset.type = self.service_type
        flashcardset.amount = amount
        flashcardset.created_dt = date_now
        flashcardset.title =  f'{flashcardset.type}_{date_now}'
        flashcardset.save()
        populate_flashcards(amount, all_verse_ids, flashcardset)
        flashcardset.save()
        return flashcardset


    def get_flashcards_by_juz(self, flashcardset, amount, juz_list):
        verse_ids = list(
            Verse.objects.filter(juz_number__in=juz_list).values_list('id', flat=True)
        )

        date_now = now()
        flashcardset.type = self.service_type
        flashcardset.amount = amount
        flashcardset.created_dt = date_now
        flashcardset.title = f'{flashcardset.type}_by_juz_{date_now}'
        flashcardset.save()
        populate_flashcards(amount, verse_ids, flashcardset)
        flashcardset.save()

        return flashcardset

    def get_flashcards_by_ids(self, flashcardset, amount, id_list):
        verse_ids = list(
            Verse.objects.filter(chapter__id__in=id_list).values_list('id', flat=True)
        )

        date_now = now()
        flashcardset.type = self.service_type
        flashcardset.amount = amount
        flashcardset.created_dt = date_now
        flashcardset.title = f'{flashcardset.type}_by_ids_{date_now}'
        flashcardset.save()
        populate_flashcards(amount, verse_ids, flashcardset)
        flashcardset.save()

        return flashcardset

    def get_flashcards_by_range(self, flashcardset, amount, start, end):
        verse_ids = list(
            Verse.objects.filter(chapter__id__gte=start, chapter__id__lte=end).values_list('id', flat=True)
        )

        date_now = now()
        flashcardset.type = self.service_type
        flashcardset.amount = amount
        flashcardset.created_dt = date_now
        flashcardset.title = f'{flashcardset.type}_by_range_{date_now}'
        flashcardset.save()
        populate_flashcards(amount, verse_ids, flashcardset)
        flashcardset.save()

        return flashcardset

    def get_flashcards_by_category(self, flashcardset, amount, category):
        pass

    def get_flashcards_by_verses_range(self, flashcardset, amount, start, end):
        pass