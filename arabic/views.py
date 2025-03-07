from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import render, redirect
from .models import Phrase
from .forms import PhraseForm
from django.views.generic import CreateView, DetailView, ListView, DeleteView, UpdateView, TemplateView
from django.urls import reverse
from django.core.paginator import Paginator

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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        phrase = self.object
        all_users_phrases = list(Phrase.objects.filter(user=phrase.user).order_by('text'))
        phrase_index = all_users_phrases.index(phrase)

        try:
            context["next_phrase_id"] = all_users_phrases[phrase_index +1].id
        except  Exception as e:
            print('An exception occurred: ', e)

        try:
            context["previous_phrase_id"] = all_users_phrases[phrase_index - 1].id
        except  Exception as e:
            print('An exception occurred: ', e)

        return context

class PhraseList(LoginRequiredMixin, ListView):
    model = Phrase
    paginate_by = 20

    def get_queryset(self):
        queryset = Phrase.objects.filter(user=self.request.user)  # Filter by user
        search_query = self.request.GET.get('q')  # Get the search query from the URL
        if search_query:
            queryset = queryset.filter(
                Q(text__icontains=search_query) | Q(translation__icontains=search_query)
            )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
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