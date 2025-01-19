import base64

from django.core.files.base import ContentFile
from django.http import JsonResponse
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import TemplateView, DetailView, CreateView

from flashcard.forms import FlashcardForm
from flashcard.models import Flashcard, FlashcardSet


class HomePage(TemplateView):
    template_name = 'index.html'

class AudioFileCreateView(CreateView):
    model = Flashcard
    form_class = FlashcardForm
    template_name = 'testpage.html'

    def form_valid(self, form):
        # Handle the recorded audio file from the request
        audio_data = self.request.POST.get('audio_data')
        if audio_data:
            try:
                format, audio_str = audio_data.split(';base64,')
                ext = format.split('/')[-1]
                audio_file = ContentFile(base64.b64decode(audio_str), name=f"recorded_audio.{ext}")
                form.instance.audio_answer = audio_file
            except Exception as e:
                print(f"Error processing audio data: {e}")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('flashcards:flashcard_detail', kwargs={'pk': self.object.id})


class AjaxSaveAudio(View):
    """Use ajax to save audio sent by user."""
    def get(self, request):
        return render(request, 'testpage.html')

    def post(self, request):
        """Save recorded audio blob sent by user."""
        audio_file = request.FILES.get('recorded_audio')
        flashcardset = FlashcardSet.object.get(id=1)
        flashcard = Flashcard()
        flashcard.flashcardset = flashcardset
        flashcard.audio_answer = audio_file
        flashcard.question = ""
        flashcard.answer = ""
        flashcard.save()
        #return JsonResponse({
         #   'success': True,
        #})
        redirect_url = reverse('flashcards:flashcard_detail', kwargs={'pk': flashcard.id})
        return JsonResponse({'redirect_url': redirect_url})

