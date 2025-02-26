from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views import View
from django.views.generic import CreateView, DetailView

from scorecard.models import Scorecard
from scorecard.forms import ScorecardManualCreationForm, ScorecardUpdateForm
from django.contrib.auth import get_user_model

User = get_user_model()


class SuperUserCheck(UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.is_superuser

class CreateScorecard(SuperUserCheck, CreateView):
    model = Scorecard
    form_class = ScorecardManualCreationForm
    template_name = 'scorecard/scorecard_manual_form.html'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        if not self.object.user:
            raise ValueError("A user must be selected for the Scorecard.")

        self.object.save()
        self.object.scorecard_manual_update()
        form.save()

        return super().form_valid(form)

    def get_success_url(self):
        return reverse('scorecard:scorecard_detail', kwargs={'pk': self.object.pk})


class ScorecardDetail(LoginRequiredMixin, DetailView):
    model = Scorecard
    template_name = 'scorecard/scorecard_detail.html'

    def get_context_data(self, **kwargs):
        scorecard = self.object
        context = {}
        context['scorecard'] = scorecard
        return context

def scorecard_manual_update(request):
    if request.method == "POST":
        form = ScorecardUpdateForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data["user"]
            scorecard = get_object_or_404(Scorecard, user=user)  # Get scorecard

            scorecard.scorecard_manual_update()  # Run update function
            messages.success(request, f"Scorecard updated for {user.username}!")

            return redirect("home")
    else:
        form = ScorecardUpdateForm()

    return render(request, "scorecard/update_scorecard.html", {"form": form})

def update_scorecard_stats(request):
    if request.method == "POST":
        form = ScorecardUpdateForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data["user"]
            scorecard = get_object_or_404(Scorecard, user=user)  # Get scorecard

            scorecard.update_stats()  # Run update function
            messages.success(request, f"Scorecard stats updated for {user.username}!")

            return redirect("home")
    else:
        form = ScorecardUpdateForm()

    return render(request, "scorecard/update_scorecard_stats.html", {"form": form})