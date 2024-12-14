from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from .models import Phrase
from .forms import PhraseForm
from django.views.generic import CreateView, DetailView, ListView, DeleteView, UpdateView, TemplateView
from django.urls import reverse

class ArabicHome(TemplateView):
    template_name = 'arabic/arabic_home.html'

class CreatePhrase(LoginRequiredMixin, CreateView):
    model = Phrase
    form_class = PhraseForm
    template_name = 'arabic/phrase_form.html'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        #self.object.phrase = Phrase.objects.get(id=self.kwargs['pk'])
        self.object.save()
        form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('arabic:phrase_detail', kwargs={'pk': self.object.pk})

class PhraseDetail(LoginRequiredMixin, DetailView):
    model = Phrase

class PhraseList(LoginRequiredMixin, ListView):
    model = Phrase

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['phrase_list'] = Phrase.objects.filter(user=self.request.user)
        return context

class PhraseUpdate(LoginRequiredMixin, UpdateView):
    login_url = '/login'
    model = Phrase
    form_class = PhraseForm
    redirect_field_name = 'arabic/phrase_detail.html'

class DeletePhrase(LoginRequiredMixin, DeleteView):
    model = Phrase

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user_id=self.request.user.id)

    def get_success_url(self):
        return reverse('arabic:phrase_list')

    def delete(self, *args, **kwargs):
        messages.success(self.request, "Phrase Deleted")
        return super().delete(*args, **kwargs)

@login_required
def delete_phrases(request):
    if request.method == 'POST':
        selected_phrases= request.POST.getlist('selected_phrases')
        Phrase.objects.filter(id__in=selected_phrases).delete()
    return redirect('arabic:phrase_list')