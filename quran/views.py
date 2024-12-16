from symtable import Class

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views.generic import DetailView, ListView, TemplateView

from quran.models import Chapter, Verse, VerseTranslation, Word
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

        for verse in verses:
            verse.selected_translation = (
                verse.translations.filter(resource_id=requested_resource_id).first().text
            )

        available_translations = VerseTranslation.objects.values("resource_id").distinct()
        context["available_translations"] = available_translations
        context["selected_resource_id"] = requested_resource_id
        context["verses"] = verses
        return context

class VerseDetail(DetailView):
    model=Verse

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        verse = self.object
        requested_resource_id = self.request.GET.get("translation", 131)
        verse.selected_translation = (
            verse.translations.filter(resource_id=requested_resource_id).first().text
        )
        context["words"] = Word.objects.filter(verse=verse)
        return context

class ChapterList(ListView):
    model = Chapter

#@login_required()
def populate_chapters(request):
    service = ChapterService()
    service.populate_chapters()
    return redirect('quran:chapter_list')

#@login_required()
def populate_verses(request):
    service = VerseService()
    service.populate_verses()
    return redirect('quran:chapter_list')