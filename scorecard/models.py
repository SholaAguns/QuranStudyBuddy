from itertools import chain
from msilib.schema import Class

from django.db import models

from django.contrib.auth import get_user_model
from django.urls import reverse

User = get_user_model()
from flashcard.models import FlashcardSet


class Scorecard(models.Model):
    user = models.OneToOneField(User, related_name='scorecard', on_delete=models.CASCADE)
    no_of_tests_completed = models.IntegerField(null=True, blank=True)
    correct_percent = models.DecimalField(null=True, blank=True, decimal_places=2, max_digits=5)
    strongest_chapter = models.CharField(null=True, blank=True, max_length=70)
    weakest_chapter = models.CharField(null=True, blank=True, max_length=70)

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
        if flashcardset.score:
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
            correct_verse_answers = VerseScore.objects.filter(correct_answer_given=True).count()
            correct_count = sum(1 for score in all_scores if score.correct_answer_given == True)
            self.correct_percent = (correct_count / self.no_of_tests_completed) * 100
            print(f"correct_count: {correct_count}, self.no_of_tests_completed: {self.no_of_tests_completed}, correct_verse_answers {correct_verse_answers}")
        else:
            self.correct_percent = 0
        self.save()

        count = 0
        for score in all_scores:
            score.included_in_stats = True
            score.save()
            count +=1
        print(f"score included count: {count}")



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