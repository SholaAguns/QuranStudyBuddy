from collections import Counter

from django.db import models

from django.contrib.auth import get_user_model
from django.urls import reverse

from quran.models import Chapter

User = get_user_model()
from flashcard.models import FlashcardSet



class Scorecard(models.Model):
    user = models.OneToOneField(User, related_name='scorecard', on_delete=models.CASCADE)
    no_of_tests_completed = models.IntegerField(null=True, blank=True)
    correct_percent = models.DecimalField(null=True, blank=True, decimal_places=2, max_digits=5)

    def get_absolute_url(self):
        return reverse('scorecard:scorecard_detail', kwargs={'pk': self.user.id})

    def get_all_scores(self):
        phrase_scores = self.phrasescore_scores.all()
        verse_scores = self.versescore_scores.all()
        verse_selection_scores = self.verseselectionscore_scores.all()
        word_scores = self.wordscore_scores.all()

        # Combine querysets lazily using itertools.chain
        #all_scores = chain(phrase_scores, verse_scores, verse_selection_scores, word_scores)

        all_scores = list(phrase_scores) + list(verse_scores) + list(verse_selection_scores) + list(word_scores)

        return all_scores

    def get_score_type(self, type):
        match type:
            case "Verse":
                return VerseScore()
            case "VerseSelection":
                return VerseSelectionScore()
            case "Word":
                return WordScore()
            case "Phrase":
                return PhraseScore()
            case _:
                raise ValueError(f"Invalid score type: {type}")


    def scorecard_manual_update(self):
        sets = FlashcardSet.objects.filter(user=self.user, score__isnull=False)

        for flashcardset in sets:
            flashcards = flashcardset.flashcards.all()
            for flashcard in flashcards:
                score = self.get_score_type(flashcard.flashcardset.type)
                score.scorecard = self
                print(f"Saving score: {score}, Scorecard User: {self.user.id}")
                score.save()
                score.set_details(flashcard)
                score.save()

        self.update_stats()

    def scorecard_update(self, flashcardset):
        if flashcardset.score is not None:
            flashcards = flashcardset.flashcards.all()
            for flashcard in flashcards:
                score = self.get_score_type(flashcard.flashcardset.type)
                score.scorecard = self
                score.set_details(flashcard)
                score.save()

        self.update_stats()

    def update_stats(self):
        all_scores = self.get_all_scores()
        #self.no_of_tests_completed = sum(1 for _ in all_scores)
        self.no_of_tests_completed = len(all_scores)

        if self.no_of_tests_completed > 0:
            correct_count = sum(1 for score in all_scores if score.correct_answer_given == True)
            self.correct_percent = (correct_count / self.no_of_tests_completed) * 100

        else:
            self.correct_percent = 0
        self.save()

        count = 0
        for score in all_scores:
            score.included_in_stats = True
            score.save()
            count +=1

    def get_strongest_chapter(self, scores):
        if not scores:
            return None, 0, 0

        # Separate correct and total counts
        correct_scores = [score.chapter_id for score in scores if score.correct_answer_given and score.chapter_id]
        total_scores = [score.chapter_id for score in scores if score.chapter_id]

        if not correct_scores:
            return None, 0, 0  # No correct scores available

        # Count occurrences
        correct_counts = Counter(correct_scores)
        total_counts = Counter(total_scores)

        # Find max correct count
        max_correct = max(correct_counts.values(), default=0)
        candidates = [chap_id for chap_id, count in correct_counts.items() if count == max_correct]
        print(f"max_correct: {max_correct}, candidates: {candidates}")

        # Break tie using total occurrences
        strongest_chapter_id = max(candidates, key=lambda chap_id: total_counts[chap_id])
        strongest_chapter = Chapter.objects.get(id=strongest_chapter_id).name_simple
        print(f"Strongest: {strongest_chapter}, total_strongest_count: {total_counts[strongest_chapter_id]}, correct_strongest_count: {correct_counts[strongest_chapter_id]}")

        return strongest_chapter, total_counts[strongest_chapter_id], correct_counts[strongest_chapter_id]

    def get_weakest_chapter(self, scores):
        if not scores:
            return None, 0, 0

        # Separate correct and total counts
        incorrect_scores = [score.chapter_id for score in scores if not score.correct_answer_given and score.chapter_id]
        total_scores = [score.chapter_id for score in scores if score.chapter_id]

        if not incorrect_scores:
            return None, 0, 0  # No correct scores available

        # Count occurrences
        incorrect_counts = Counter(incorrect_scores)
        total_counts = Counter(total_scores)

        # Find max correct count
        max_incorrect = max(incorrect_counts.values(), default=0)
        candidates = [chap_id for chap_id, count in incorrect_counts.items() if count == max_incorrect]
        print(f"max_correct: {max_incorrect}, candidates: {candidates}")

        # Break tie using total occurrences
        weakest_chapter_id = max(candidates, key=lambda chap_id: total_counts[chap_id])
        weakest_chapter = Chapter.objects.get(id=weakest_chapter_id).name_simple

        print(f"Weakest: {weakest_chapter_id}, total_weakest_count: {total_counts[weakest_chapter_id]}, correct_weakest_count: {incorrect_counts[weakest_chapter_id]}")

        correct_count = total_counts[weakest_chapter_id] - incorrect_counts[weakest_chapter_id]

        return weakest_chapter, total_counts[weakest_chapter_id], correct_count

    def get_strongest_category(self, scores):
        if not scores:
            return None, 0, 0

        # Separate correct and total counts
        correct_scores = [score.category for score in scores if score.correct_answer_given and score.category]
        total_scores = [score.category for score in scores if score.category]

        if not correct_scores:
            return None, 0, 0  # No correct scores available

        # Count occurrences
        correct_counts = Counter(correct_scores)
        total_counts = Counter(total_scores)

        # Find max correct count
        max_correct = max(correct_counts.values(), default=0)
        candidates = [cat for cat, count in correct_counts.items() if count == max_correct]
        print(f"max_correct: {max_correct}, candidates: {candidates}")

        # Break tie using total occurrences
        strongest_category = max(candidates, key=lambda cat: total_counts[cat])
        print(f"Strongest: {strongest_category}, total_strongest_count: {total_counts[strongest_category]}, correct_strongest_count: {correct_counts[strongest_category]}")

        return strongest_category, total_counts[strongest_category], correct_counts[strongest_category]

    def get_weakest_category(self, scores):
        if not scores:
            return None, 0, 0

        # Separate correct and total counts
        incorrect_scores = [score.category for score in scores if not score.correct_answer_given and score.category]
        total_scores = [score.category for score in scores if score.category]

        if not incorrect_scores:
            return None, 0, 0  # No correct scores available

        # Count occurrences
        incorrect_counts = Counter(incorrect_scores)
        total_counts = Counter(total_scores)

        # Find max correct count
        max_incorrect = max(incorrect_counts.values(), default=0)
        candidates = [cat for cat, count in incorrect_counts.items() if count == max_incorrect]
        print(f"max_correct: {max_incorrect}, candidates: {candidates}")

        # Break tie using total occurrences
        weakest_category = max(candidates, key=lambda cat: total_counts[cat])
        print(f"Weakest: {weakest_category}, total_weakest_count: {total_counts[weakest_category]}, incorrect_weakest_count: {incorrect_counts[weakest_category]}")

        correct_count = total_counts[weakest_category] - incorrect_counts[weakest_category]

        return weakest_category, total_counts[weakest_category], correct_count

class Score(models.Model):
    scorecard = models.ForeignKey(Scorecard, related_name="%(class)s_scores", on_delete=models.CASCADE)
    type = models.CharField(max_length=70)
    correct_answer_given = models.BooleanField(null=True)
    flashcard_id = models.IntegerField(null=True)
    included_in_stats = models.BooleanField(default=False)

    class Meta:
        abstract = True


class PhraseScore(Score):
    category = models.CharField(max_length=50, null=True)

    def __int__(self, *args, **kwargs):
        self.type = "Phrase"
        super().save(*args, **kwargs)

    def set_details(self, flashcard):
        self.correct_answer_given = flashcard.correct_answer_given
        self.flashcard_id = flashcard.id
        if flashcard.info:
            if flashcard.info['category']:
                self.category = flashcard.info['category']


class VerseScore(Score):
    chapter_id = models.IntegerField(null=True)

    def __int__(self, *args, **kwargs):
        self.type = "Verse"
        super().save(*args, **kwargs)

    def set_details(self, flashcard):
        self.correct_answer_given = flashcard.correct_answer_given
        self.flashcard_id = flashcard.id
        if flashcard.info:
            if flashcard.info['chapter_id']:
                self.chapter_id = flashcard.info['chapter_id']

class VerseSelectionScore(Score):
    chapter_id = models.IntegerField(null=True)
    verse_selection_id = models.IntegerField(null=True)

    def __int__(self, *args, **kwargs):
        self.type = "VerseSelection"
        super().save(*args, **kwargs)

    def set_details(self, flashcard):
        self.correct_answer_given = flashcard.correct_answer_given
        self.flashcard_id = flashcard.id
        if flashcard.info:
            if flashcard.info['chapter_id']:
                self.chapter_id = flashcard.info['chapter_id']

class WordScore(Score):
    chapter_id = models.IntegerField(null=True)


    def __int__(self, *args, **kwargs):
        self.type = "Word"
        super().save(*args, **kwargs)

    def set_details(self, flashcard):
        self.correct_answer_given = flashcard.correct_answer_given
        self.flashcard_id = flashcard.id
        if flashcard.info:
            if flashcard.info['chapter_id']:
                self.chapter_id = flashcard.info['chapter_id']