import json
import traceback

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import ListView, DetailView, UpdateView, DeleteView, TemplateView

from flashcard.forms import FlashcardSetForm, FlashcardSetUpdateForm
from flashcard.models import FlashcardSet
from flashcard.services.flashcard_service_factory import FlashcardServiceFactory

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
    print("inside views " +  service_type)
    try:
        service = FlashcardServiceFactory.get_service(service_type + "FlashcardService")
        print("service is " + service.service_type)
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

        if request_type == 'byRange':
            range_start = int(range_start) if range_start.isdigit() else None
            range_end = int(range_end) if range_end.isdigit() else None
        else:
            range_start = None
            range_end = None

        try:
            service = FlashcardServiceFactory.get_service(service_type + "FlashcardService")
        except ValueError:
            return JsonResponse({'error': 'Invalid service type'}, status=400)
        dispatch_table = {
            'byIds': lambda: service.get_flashcards_by_ids(new_flashcardset, amount, id_list),
            'byCategory': lambda: service.get_flashcards_by_category(new_flashcardset, amount, category),
            'byRange': lambda: service.get_flashcards_by_range(new_flashcardset, amount, range_start, range_end),
            'byJuz': lambda: service.get_flashcards_by_juz(new_flashcardset, amount, juz_list),
            'default': lambda: service.get_flashcards(new_flashcardset, amount),
        }

        if request_type not in dispatch_table:
            return JsonResponse({'error': 'Invalid request type'}, status=400)

        try:
            new_flashcardset = dispatch_table[request_type]()
            print("Back from service")
            #return HttpResponseRedirect(reverse('flashcards:flashcardset_detail', kwargs={'pk': new_flashcardset.id}))
            redirect_url = reverse('flashcards:flashcardset_detail', kwargs={'pk': new_flashcardset.id})
            return JsonResponse({'redirect_url': redirect_url})
        except Exception as e:
            traceback.print_exc()
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid request method'}, status=400)


def submit_flashcardset_answers(request, flashcardset_id):
    if request.method == 'POST':
        try:
            flashcardset = FlashcardSet.objects.get(pk=flashcardset_id)
            data = json.loads(request.body)

            for flashcard_id, user_answer in data.items():
                flashcard = flashcardset.flashcards.get(pk=flashcard_id)
                flashcard.user_answer = user_answer
                flashcard.correct_anwser_given = (flashcard.answer.strip().lower() == user_answer.strip().lower())
                flashcard.save()

            total_flashcards = flashcardset.flashcards.count()
            correct_answers = flashcardset.flashcards.filter(correct_anwser_given=True).count()
            flashcardset.score = round((correct_answers / total_flashcards) * 100, 2)
            flashcardset.save()

            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    return JsonResponse({'error': 'Invalid request method'}, status=400)
