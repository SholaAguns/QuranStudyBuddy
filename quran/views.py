import traceback
from symtable import Class

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import DetailView, ListView, TemplateView, DeleteView

from quran.models import Chapter, Verse, VerseTranslation, Word, TranslatedName, AudioEdition, HostedVerseAudio, \
    VerseSelection
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

class ChapterWordList(TemplateView):
    template_name = 'quran/chapter_word_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        chapter_id = self.kwargs['pk']
        chapter = Chapter.objects.get(id=chapter_id)
        context['words'] = Word.objects.filter(verse__chapter=chapter)
        context['chapter'] = chapter
        context["translated_name"] = TranslatedName.objects.get(chapter=chapter)
        return context

class VerseSelectionWordList(TemplateView):
    template_name = 'quran/verseselection_word_list.html'
    model = VerseSelection

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        verseselection_id = self.kwargs['pk']
        verseselection = VerseSelection.objects.get(id=verseselection_id)
        context['words'] = Word.objects.filter(verse__id__gte=verseselection.start_verse_id, verse__id__lte=verseselection.end_verse_id)
        context['verseselection'] = verseselection
        return context

class VerseSelectionList(LoginRequiredMixin, ListView):
    model = VerseSelection

class VerseSelectionDetail(LoginRequiredMixin, DetailView):
    model = VerseSelection

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        start_id = self.object.start_verse_id
        end_id = self.object.end_verse_id
        verses = Verse.objects.filter(id__gte=start_id, id__lte=end_id)

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

        context['verses'] = verses
        context["available_audio_editions"] = AudioEdition.objects.all()
        available_translations = VerseTranslation.objects.values("resource_id").distinct()
        context["available_translations"] = available_translations
        context["selected_resource_id"] = requested_resource_id
        context["selected_audio_identifier"] = requested_audio_identifier
        return context

class CreateVerseSelection(LoginRequiredMixin, TemplateView):
    template_name = 'quran/verseselection_form.html'

class DeleteVerseSelection(LoginRequiredMixin, DeleteView):
    model = VerseSelection
    print("here")

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user_id=self.request.user.id)

    def get_success_url(self):
        return reverse('quran:verse_selection_list')

    def delete(self, *args, **kwargs):
        messages.success(self.request, "Verse Selection Deleted")
        return super().delete(*args, **kwargs)

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

@login_required()
def create_verse_selection(request):
    verse_selection = VerseSelection()
    if request.method == 'POST':
        verse_range_start = request.POST.get('verse_range_start', '')
        verse_range_end = request.POST.get('verse_range_end', '')
        title = request.POST.get('title', '')

        verse_range_start = int(verse_range_start) if verse_range_start.isdigit() else None
        verse_range_end = int(verse_range_end) if verse_range_end.isdigit() else None

        try:
            verse_selection.title = title
            verse_selection.start_verse_id = verse_range_start
            verse_selection.end_verse_id = verse_range_end
            verse_selection.user = request.user
            verse_selection.save()
        except Exception as e:
            traceback.print_exc()
            return JsonResponse({'error': str(e)}, status=500)

        redirect_url = reverse('quran:verse_selection_detail', kwargs={'pk': verse_selection.id})
        return JsonResponse({'redirect_url': redirect_url})
        #return redirect('quran:verse_selection_detail', pk=verse_selection.id)


    return JsonResponse({'error': 'Invalid request method'}, status=400)

@login_required
def delete_verse_selections(request):
    if request.method == 'POST':
        selected_verse_selections= request.POST.getlist('selected_verse_selections')
        VerseSelection.objects.filter(id__in=selected_verse_selections).delete()
    return redirect('quran:verse_selection_list')