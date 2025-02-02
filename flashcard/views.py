import base64
import json
import traceback

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.files.base import ContentFile
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views.generic import ListView, DetailView, UpdateView, DeleteView, TemplateView

from flashcard.forms import FlashcardSetForm, FlashcardSetUpdateForm
from flashcard.models import FlashcardSet, Flashcard
from flashcard.services.flashcard_service_factory import FlashcardServiceFactory
from flashcard.services.marking_service import MarkingService
from quran.models import Chapter, Verse, AudioEdition


class CreateFlaschcardSet(LoginRequiredMixin, TemplateView):
    template_name = 'flashcards/flashcardset_form.html'

class FlashcardSetList(LoginRequiredMixin, ListView):
    model = FlashcardSet
    template_name = 'flashcards/flashcardset_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['flashcardset_list'] = FlashcardSet.objects.filter(user=self.request.user)
        return context

class FlashcardSetDetail(LoginRequiredMixin, DetailView):
    model = FlashcardSet
    template_name = 'flashcards/flashcardset_detail.html'

    def get_context_data(self, **kwargs):
        requested_audio_identifier = self.request.GET.get("audio_edition", "ar.abdulbasitmurattal")
        flashcards = self.object.flashcards.all()
        for flashcard in flashcards:
            try:
                flashcard.selected_audio = flashcard.audio_filepaths[requested_audio_identifier]
                flashcard.save()
            except:
                print(f"No audio edition {requested_audio_identifier} found for flashcard {flashcard.id}")

        context = super().get_context_data(**kwargs)
        context['chapters']  = Chapter.objects.all()
        context['correct_answers_count'] = self.object.flashcards.filter(correct_answer_given=True).count()
        context['total_flashcards_count'] = self.object.flashcards.count()
        context["available_audio_editions"] = AudioEdition.objects.all()
        context["selected_audio_identifier"] = requested_audio_identifier
        return context

class FlashcardSetUpdate(LoginRequiredMixin, UpdateView):
    login_url = '/login'
    model = FlashcardSet
    form_class = FlashcardSetUpdateForm
    template_name = 'flashcards/flashcardset_edit_name.html'
    redirect_field_name = 'flashcards/flashcardset_detail.html'

class DeleteFlashcardSet(LoginRequiredMixin, DeleteView):
    model = FlashcardSet
    template_name = 'flashcards/flashcardset_confirm_delete.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user_id=self.request.user.id)

    def get_success_url(self):
        return reverse('flashcards:flashcardset_list')

    def delete(self, *args, **kwargs):
        messages.success(self.request, "FlashcardSet Deleted")
        return super().delete(*args, **kwargs)

def get_service_types(request):
    return JsonResponse({'service_types': FlashcardServiceFactory.list_services()})
    #return JsonResponse({'service_types': ['Phrase', 'Verse']})

def get_request_types(request, service_type):
    try:
        service = FlashcardServiceFactory.get_service(service_type + "FlashcardService")
        return JsonResponse({'request_types': service.get_request_types()})
    except ValueError:
        return JsonResponse({'error': 'Invalid service type'}, status=400)

def get_id_options(request, service_type):
    try:
        service = FlashcardServiceFactory.get_service(service_type + "FlashcardService")
        options = service.get_id_options(request.user)
        return JsonResponse({'options': options})
    except ValueError:
        return JsonResponse({'error': 'Invalid service type'}, status=400)

def get_juz_options(request, service_type):
    try:
        service = FlashcardServiceFactory.get_service(service_type + "FlashcardService")
        options = service.get_juz_options(request.user)
        return JsonResponse({'options': options})
    except ValueError:
        return JsonResponse({'error': 'Invalid service type'}, status=400)

def get_range_options(request, service_type):
    try:
        service = FlashcardServiceFactory.get_service(service_type + "FlashcardService")
        options = service.get_range_options(request.user)
        return JsonResponse({'options': options})
    except ValueError:
        return JsonResponse({'error': 'Invalid service type'}, status=400)

def get_verses_options(request, chapter_id):
    try:
        verses = Verse.objects.filter(chapter__id=chapter_id)
        options = []
        for verse in verses:
            options.append({
                'label': verse.verse_key,
                'value': verse.id
            })
        return JsonResponse({'options': options})
    except ValueError:
        return JsonResponse({'error': 'Invalid service type'}, status=400)

def get_category_options(request, service_type):
    try:
        service = FlashcardServiceFactory.get_service(service_type + "FlashcardService")
        options = service.get_category_options(request.user)
        return JsonResponse({'options': options})
    except ValueError:
        return JsonResponse({'error': 'Invalid service type'}, status=400)

def submit_flashcardset_form(request):
    new_flashcardset = FlashcardSet()
    new_flashcardset.user = request.user
    #new_flashcardset.save()

    if request.method == 'POST':
        service_type = request.POST.get('service_type')
        request_type = request.POST.get('request_type')
        amount = int(request.POST.get('amount'))
        id_list = json.loads(request.POST.get('idList', '[]'))
        juz_list = json.loads(request.POST.get('juzList', '[]'))
        category = request.POST.get('category', None)
        range_start = request.POST.get('range_start', '')
        range_end = request.POST.get('range_end', '')
        verse_range_start = request.POST.get('verse_range_start', '')
        verse_range_end = request.POST.get('verse_range_end', '')
        tags = request.POST.get('tags','')

        if request_type == 'byRange':
            range_start = int(range_start) if range_start.isdigit() else None
            range_end = int(range_end) if range_end.isdigit() else None
        else:
            range_start = None
            range_end = None

        if request_type == 'byVerseRange':
            verse_range_start = int(verse_range_start) if verse_range_start.isdigit() else None
            verse_range_end = int(verse_range_end) if verse_range_end.isdigit() else None
        else:
            verse_range_start = None
            verse_range_end = None

        try:
            service = FlashcardServiceFactory.get_service(service_type + "FlashcardService")
        except ValueError:
            return JsonResponse({'error': 'Invalid service type'}, status=400)
        dispatch_table = {
            'byIds': lambda: service.get_flashcards_by_ids(new_flashcardset, amount, id_list),
            'byCategory': lambda: service.get_flashcards_by_category(new_flashcardset, amount, category),
            'byRange': lambda: service.get_flashcards_by_range(new_flashcardset, amount, range_start, range_end),
            'byVerseRange': lambda: service.get_flashcards_by_verses_range(new_flashcardset, amount, verse_range_start, verse_range_end),
            'byJuz': lambda: service.get_flashcards_by_juz(new_flashcardset, amount, juz_list),
            'byTags': lambda: service.get_flashcards_by_tags(new_flashcardset, amount, tags),
            'default': lambda: service.get_flashcards(new_flashcardset, amount),
        }

        if request_type not in dispatch_table:
            return JsonResponse({'error': 'Invalid request type'}, status=400)

        try:
            new_flashcardset = dispatch_table[request_type]()
            #return HttpResponseRedirect(reverse('flashcards:flashcardset_detail', kwargs={'pk': new_flashcardset.id}))
            redirect_url = reverse('flashcards:flashcardset_detail', kwargs={'pk': new_flashcardset.id})
            return JsonResponse({'redirect_url': redirect_url})
        except Exception as e:
            traceback.print_exc()
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid request method'}, status=400)


def submit_flashcardset_answers(request, pk):
    marking_service = MarkingService()
    if request.method == 'POST':
        try:
            flashcardset = FlashcardSet.objects.get(pk=pk)
            data = json.loads(request.body)
            user_answers = data.get("answers", {})
            audio_answers = data.get("audio_answers", {})

            # for flashcard_id, user_answer in data.items():
            #     flashcard = flashcardset.flashcards.get(pk=flashcard_id)
            #     flashcard.user_answer = user_answer
            #     flashcard.save()
            #     print("Answer: " + flashcard.user_answer)

            for flashcard_id, user_answer in user_answers.items():
                flashcard = flashcardset.flashcards.get(pk=flashcard_id)
                flashcard.user_answer = user_answer
                flashcard.save()

            for flashcard_id, audio_data in audio_answers.items():
                if audio_data:
                    flashcard = flashcardset.flashcards.get(pk=flashcard_id)
                    format, audio_str = audio_data.split(';base64,')
                    ext = format.split('/')[-1]
                    audio_file = ContentFile(base64.b64decode(audio_str), name=f"flashcard_{flashcard_id}_audio_answer.{ext}")
                    flashcard.audio_answer = audio_file
                    flashcard.save()

            marking_service.calculate_score(flashcardset)
            return JsonResponse({'success': True})
        except Exception as e:
            print(f"Error: {str(e)}")
            return JsonResponse({'error': str(e)}, status=400)

    return JsonResponse({'error': 'Invalid request method'}, status=400)

class FlashcardDetail(DetailView):
    model = Flashcard
    template_name = 'flashcards/flashcard_detail.html'

@login_required
def delete_flashcardsets(request):
    if request.method == 'POST':
        selected_flashcardsets = request.POST.getlist('selected_flashcardsets')
        FlashcardSet.objects.filter(id__in=selected_flashcardsets).delete()
    return redirect('flashcards:flashcardset_list')


@login_required()
def self_correct_answer(request, pk):
    is_ajax_request = request.headers.get("x-requested-with") == "XMLHttpRequest"

    if request.method == 'POST' and is_ajax_request:
        flashcard = get_object_or_404(Flashcard, id=pk)
        flashcard.correct_answer_given = not flashcard.correct_answer_given
        flashcard.save()
        marking_service = MarkingService()
        marking_service.save_score(flashcard.flashcardset)

        return JsonResponse({'success': True})
    return JsonResponse({'success': False, 'message': 'Invalid request'})