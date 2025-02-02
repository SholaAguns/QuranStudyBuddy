import secrets

from django.utils.timezone import now
import random
from flashcard.models import Flashcard
from flashcard.services.iflashcardservice import IFlashcardService
from quran.models import Chapter, Verse, HostedVerseAudio, VerseSelection


def populate_flashcards(amount, ids, flashcardset):
    print(ids)
    #random.shuffle(ids)
    #print(ids)
    #random.shuffle(ids)
    #print(ids)
    #selected_ids = random.sample(ids, min(amount, len(ids)))
    ids_copy = ids[:]
    secrets.SystemRandom().shuffle(ids_copy)
    selected_ids = ids_copy[:min(amount, len(ids))]
    print(selected_ids)

    selected_verses_selections = VerseSelection.objects.filter(id__in=selected_ids)


    for selection in selected_verses_selections:
        flashcard = Flashcard()
        flashcard.flashcardset = flashcardset
        verses = Verse.objects.filter(id__gte=selection.start_verse_id, id__lte=selection.end_verse_id)
        flashcard.question = f"{verses[0].text_uthmani}\n.\n.\n.\n{verses[len(verses)-1].text_uthmani}"
        flashcard.answer = verses[0].chapter.name_simple
        for verse in verses:
            flashcard.info += f"{verse.get_english_translation()} - {verse.text_uthmani}\n"
        #populate_audio_filepaths(verse, flashcard)
        flashcard.save()

def populate_audio_filepaths(verse, flashcard):
    hosted_audio_objects = HostedVerseAudio.objects.filter(verse=verse)

    if flashcard.audio_filepaths is None:
        flashcard.audio_filepaths = {}

    for hao in hosted_audio_objects:
        flashcard.audio_filepaths[hao.edition.identifier] = hao.audio_path

class VerseSelectionFlashcardService(IFlashcardService):

    service_type = "VerseSelection"

    def get_flashcards_by_category(self, flashcardset, amount, category):
        pass

    def get_category_options(self, user):
        pass

    def get_flashcards_by_tags(self, flashcardset, amount, tags):
        pass

    def get_request_types(self):
        request_types = [
            {
                'label': 'All verse selections',
                'value': 'default'
            },
            {
                'label': 'Select Verse Selection',
                'value': 'byIds'
            },
            {
                'label': 'Select by juz',
                'value': 'byJuz'
            },
            {
                'label': 'Select by chapter range',
                'value': 'byRange'
            },
            {
                'label': 'Select by verse range',
                'value': 'byVerseRange'
            }
        ]
        return request_types

    def get_juz_options(self, user):
        all_juz_numbers= VerseSelection.objects.filter(user=user).values_list('juz_number', flat=True).distinct()
        unique_juz_numbers = set(all_juz_numbers)
        options = []
        for juz in unique_juz_numbers:
            options.append({
                'label': juz,
                'value': juz
            })
        return options

    def get_id_options(self, user):
        all_verse_selections = VerseSelection.objects.filter(user=user)
        options = []
        for selection in all_verse_selections:
            label = f'{selection.title}'
            options.append({
                'label': label,
                'value': selection.id
            })
        return options

    def get_range_options(self, user):
        all_chapters = Chapter.objects.all()
        options = []
        for chapter in all_chapters:
            label = f'{chapter.id} - {chapter.name_simple}'
            options.append({
                'label': label,
                'value': chapter.id
            })
        return options

    def get_flashcards(self, flashcardset, amount):
        all_verse_selection_ids = list(VerseSelection.objects.values_list('id', flat=True))

        date_now = now()
        flashcardset.type = self.service_type
        flashcardset.amount = amount
        flashcardset.created_dt = date_now
        flashcardset.title =  f'{flashcardset.type}_{date_now}'
        flashcardset.save()
        populate_flashcards(amount, all_verse_selection_ids, flashcardset)
        flashcardset.save()
        return flashcardset


    def get_flashcards_by_juz(self, flashcardset, amount, juz_list):
        verse_selection_ids = list(
            VerseSelection.objects.filter(juz_number__in=juz_list).values_list('id', flat=True)
        )

        date_now = now()
        flashcardset.type = self.service_type
        flashcardset.amount = amount
        flashcardset.created_dt = date_now
        flashcardset.title = f'{flashcardset.type}_by_juz_{date_now}'
        flashcardset.save()
        populate_flashcards(amount, verse_selection_ids, flashcardset)
        flashcardset.save()

        return flashcardset

    def get_flashcards_by_ids(self, flashcardset, amount, id_list):
        verse_ids = list(
            VerseSelection.objects.filter(id__in=id_list).values_list('id', flat=True)
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
            VerseSelection.objects.filter(start_chapter_id__gte=start, end_chapter_id__lte=end).values_list('id', flat=True)
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

    def get_flashcards_by_verses_range(self, flashcardset, amount, start, end):
        verse_ids = list(
            VerseSelection.objects.filter(start_verse_id__gte=start, end_verse_id__lte=end).values_list('id', flat=True)
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