from symtable import Class

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views.generic import DetailView, ListView, TemplateView

from quran.models import Chapter, Verse, VerseTranslation, Word, TranslatedName, AudioEdition, HostedVerseAudio
from quran.services.audioservice import AudioService
from quran.services.chapterservice import ChapterService
from quran.services.verseservice import VerseService

class QuranAdmin(TemplateView):
    template_name = 'quran/quran_admin.html'

class ChapterDetail(DetailView):
    model= Chapter

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        chapter = self.object
        verses = chapter.verses.prefetch_related("translations").all()

        requested_resource_id = self.request.GET.get("translation", 131)
        requested_audio_identifier = self.request.GET.get("audio_edition", "ar.abdulbasitmurattal")


        for verse in verses:
            try:
                verse.selected_translation = (
                    verse.translations.filter(resource_id=requested_resource_id).first().text
                )
            except:
                print(f"No verse translation {requested_resource_id} found for {verse.verse_key}")
            try:
                verse_audio = HostedVerseAudio.objects.get(edition__identifier=requested_audio_identifier, verse=verse)
                verse.selected_audio = verse_audio
            except:
                print(f"No audio edition {requested_audio_identifier} found for {verse.verse_key}")

        context["available_audio_editions"] = AudioEdition.objects.all()
        available_translations = VerseTranslation.objects.values("resource_id").distinct()
        context["translated_name"] = TranslatedName.objects.get(chapter=chapter)
        context["available_translations"] = available_translations
        context["selected_resource_id"] = requested_resource_id
        context["selected_audio_identifier"] = requested_audio_identifier
        context["verses"] = verses
        return context

class VerseDetail(DetailView):
    model=Verse

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        verse = self.object
        requested_resource_id = self.request.GET.get("translation", 131)
        requested_audio_identifier = self.request.GET.get("audio_edition", "ar.abdulbasitmurattal")
        try:
            verse.selected_translation = (
                verse.translations.filter(resource_id=requested_resource_id).first().text
            )
        except Exception as e:
            print('An exception occurred: ', e)
            print(f"No verse translation {requested_resource_id} found for {verse.verse_key}")
        try:
            verse_audio = HostedVerseAudio.objects.get(edition__identifier=requested_audio_identifier, verse=verse)
            verse.selected_audio = verse_audio
        except Exception as e:
            print('An exception occurred: ', e)
            print(f"No audio edition {requested_audio_identifier} found for {verse.verse_key}")

        try:
            Verse.objects.get(id=verse.id + 1)
            context["next_verse_id"] = verse.id + 1
        except  Exception as e:
            print('An exception occurred: ', e)

        try:
            Verse.objects.get(id=verse.id - 1)
            context["previous_verse_id"] = verse.id - 1
        except  Exception as e:
            print('An exception occurred: ', e)


        context["available_audio_editions"] = AudioEdition.objects.all()
        context["available_translations"] = VerseTranslation.objects.values("resource_id").distinct()
        context["selected_resource_id"] = requested_resource_id
        context["selected_audio_identifier"] = requested_audio_identifier
        context["words"] = Word.objects.filter(verse=verse)
        return context

class AudioEditionDetail(DetailView):
    model = AudioEdition

class ChapterList(ListView):
    model = Chapter

class AudioEditionList(ListView):
    model = AudioEdition

@login_required()
def populate_chapters(request):
    service = ChapterService()
    service.populate_chapters()
    return redirect('quran:chapter_list')

@login_required()
def populate_verses(request):
    service = VerseService()
    service.populate_verses()
    return redirect('quran:chapter_list')

@login_required()
def populate_audio_editions(request):
    service = AudioService()
    service.fetch_all_editions()
    return redirect('quran:audio_edition_list')

@login_required()
def populate_hosted_audio(request):
    service = AudioService()
    service.populate_hosted_audio_objects_manual()
    return redirect('quran:chapter_list')