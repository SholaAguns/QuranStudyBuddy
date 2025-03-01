from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views import View
from django.views.generic import CreateView, DetailView

from scorecard.models import Scorecard, PhraseScore, VerseScore, VerseSelectionScore, WordScore
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
        all_scores = scorecard.get_all_scores()
        context = {}
        chapter_related_scores = [score for score in all_scores if not isinstance(score, PhraseScore)]
        category_related_scores = [score for score in all_scores if isinstance(score, PhraseScore)]

        context['scorecard'] = scorecard
        context['strongest_chapter'], context['strongest_chapter_total_count'], context['strongest_chapter_correct_count'] = scorecard.get_strongest_chapter(
            chapter_related_scores)
        context['weakest_chapter'], context['weakest_chapter_total_count'], context[
            'weakest_chapter_correct_count'] = scorecard.get_weakest_chapter(
            chapter_related_scores)

        context['strongest_category'], context['strongest_category_total_count'], context[
            'strongest_category_correct_count'] = scorecard.get_strongest_category(
            category_related_scores)
        context['weakest_category'], context['weakest_category_total_count'], context[
            'weakest_category_correct_count'] = scorecard.get_weakest_category(
            category_related_scores)

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

def get_phrase_stats(request):
    scorecard = Scorecard.objects.get(user=request.user)

def get_verse_stats0(request):
    scorecard = Scorecard.objects.get(user=request.user)

    all_verse_scores = list(VerseScore.objects.filter(scorecard=scorecard))
    context = {}

    context['verse_strongest_chapter_id'], context['verse_strongest_chapter_total_count'], context[
        'verse_strongest_chapter_correct_count'] = scorecard.get_strongest_chapter(
        all_verse_scores)
    context['verse_weakest_chapter_id'], context['verse_weakest_chapter_total_count'], context[
        'verse_weakest_chapter_correct_count'] = scorecard.get_weakest_chapter(
        all_verse_scores)

    return context

@login_required
def get_verse_stats(request):
    try:
        # Get the user's scorecard
        scorecard = Scorecard.objects.get(user=request.user)

        # Filter VerseScore linked to this scorecard
        all_verse_scores = VerseScore.objects.filter(scorecard=scorecard)
        verse_correct_count = len(all_verse_scores.filter(correct_answer_given=True))
        verse_overall_score = 0
        if len(all_verse_scores) >0:
            verse_overall_score = (verse_correct_count / len(all_verse_scores))* 100

        response_data = {
            "total_count":0,
            "verse_strongest_chapter": None,
            "verse_strongest_chapter_total_count": 0,
            "verse_strongest_chapter_correct_count": 0,
            "verse_weakest_chapter": None,
            "verse_weakest_chapter_total_count": 0,
            "verse_weakest_chapter_correct_count": 0,
        }

        if all_verse_scores.exists():
            response_data["verse_total_count"] = len(all_verse_scores)
            response_data["verse_overall_score"] = round(verse_overall_score,2)
            (response_data["verse_strongest_chapter"],
             response_data["verse_strongest_chapter_total_count"],
             response_data["verse_strongest_chapter_correct_count"]) = scorecard.get_strongest_chapter(all_verse_scores)

            (response_data["verse_weakest_chapter"],
             response_data["verse_weakest_chapter_total_count"],
             response_data["verse_weakest_chapter_correct_count"]) = scorecard.get_weakest_chapter(all_verse_scores)

        return JsonResponse(response_data)

    except Scorecard.DoesNotExist:
        return JsonResponse({"error": "Scorecard not found"}, status=404)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


@login_required
def get_phrase_stats(request):
    try:
        scorecard = Scorecard.objects.get(user=request.user)

        all_phrase_scores = PhraseScore.objects.filter(scorecard=scorecard)
        phrase_correct_count = len(all_phrase_scores.filter(correct_answer_given=True))
        phrase_overall_score = 0
        if len(all_phrase_scores) >0:
            phrase_overall_score = (phrase_correct_count / len(all_phrase_scores))* 100

        response_data = {
            "total_count":0,
            "phrase_strongest_category": None,
            "phrase_strongest_category_total_count": 0,
            "phrase_strongest_category_correct_count": 0,
            "phrase_weakest_category": None,
            "phrase_weakest_category_total_count": 0,
            "phrase_weakest_category_correct_count": 0,
        }

        if all_phrase_scores.exists():
            response_data["phrase_total_count"] = len(all_phrase_scores)
            response_data["phrase_overall_score"] = round(phrase_overall_score,2)
            (response_data["phrase_strongest_category"],
             response_data["phrase_strongest_category_total_count"],
             response_data["phrase_strongest_category_correct_count"]) = scorecard.get_strongest_category(all_phrase_scores)

            (response_data["phrase_weakest_category"],
             response_data["phrase_weakest_category_total_count"],
             response_data["phrase_weakest_category_correct_count"]) = scorecard.get_weakest_category(all_phrase_scores)

        return JsonResponse(response_data)

    except Scorecard.DoesNotExist:
        return JsonResponse({"error": "Scorecard not found"}, status=404)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


@login_required
def get_verse_selection_stats(request):
    try:
        # Get the user's scorecard
        scorecard = Scorecard.objects.get(user=request.user)

        # Filter VerseSelectionScore linked to this scorecard
        all_verse_selection_scores = VerseSelectionScore.objects.filter(scorecard=scorecard)
        verse_selection_correct_count = len(all_verse_selection_scores.filter(correct_answer_given=True))
        verse_selection_overall_score = 0
        if len(all_verse_selection_scores) >0:
            verse_selection_overall_score = (verse_selection_correct_count / len(all_verse_selection_scores))* 100

        # Prepare response data
        response_data = {
            "total_count":0,
            "verse_selection_strongest_chapter": None,
            "verse_selection_strongest_chapter_total_count": 0,
            "verse_selection_strongest_chapter_correct_count": 0,
            "verse_selection_weakest_chapter": None,
            "verse_selection_weakest_chapter_total_count": 0,
            "verse_selection_weakest_chapter_correct_count": 0,
        }

        if all_verse_selection_scores.exists():
            response_data["verse_selection_total_count"] = len(all_verse_selection_scores)
            response_data["verse_selection_overall_score"] = "{:.2f}".format(verse_selection_overall_score)
            (response_data["verse_selection_strongest_chapter"],
             response_data["verse_selection_strongest_chapter_total_count"],
             response_data["verse_selection_strongest_chapter_correct_count"]) = scorecard.get_strongest_chapter(all_verse_selection_scores)

            (response_data["verse_selection_weakest_chapter"],
             response_data["verse_selection_weakest_chapter_total_count"],
             response_data["verse_selection_weakest_chapter_correct_count"]) = scorecard.get_weakest_chapter(all_verse_selection_scores)

        return JsonResponse(response_data)

    except Scorecard.DoesNotExist:
        return JsonResponse({"error": "Scorecard not found"}, status=404)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

@login_required
def get_word_stats(request):
    try:
        scorecard = Scorecard.objects.get(user=request.user)

        all_word_scores = WordScore.objects.filter(scorecard=scorecard)
        word_correct_count = len(all_word_scores.filter(correct_answer_given=True))
        word_overall_score =0
        if len(all_word_scores) >0:
            word_overall_score = (word_correct_count / len(all_word_scores))* 100

        response_data = {
            "total_count":0,
            "word_strongest_chapter": None,
            "word_strongest_chapter_total_count": 0,
            "word_strongest_chapter_correct_count": 0,
            "word_weakest_chapter": None,
            "word_weakest_chapter_total_count": 0,
            "word_weakest_chapter_correct_count": 0,
        }

        if all_word_scores.exists():
            response_data["word_total_count"] = len(all_word_scores)
            response_data["word_overall_score"] = round(word_overall_score,2)
            (response_data["word_strongest_chapter"],
             response_data["word_strongest_chapter_total_count"],
             response_data["word_strongest_chapter_correct_count"]) = scorecard.get_strongest_chapter(all_word_scores)

            (response_data["word_weakest_chapter"],
             response_data["word_weakest_chapter_total_count"],
             response_data["word_weakest_chapter_correct_count"]) = scorecard.get_weakest_chapter(all_word_scores)

        return JsonResponse(response_data)

    except Scorecard.DoesNotExist:
        return JsonResponse({"error": "Scorecard not found"}, status=404)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)