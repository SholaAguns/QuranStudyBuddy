import re
from rapidfuzz import fuzz

from flashcard.models import Flashcard


class MarkingService:

    def normalize_text(self, text):
        # Remove parentheses and normalize text
        if not isinstance(text, str):
            print(f"Expected a string, but got {type(text)}: {text}")
        text = re.sub(r'\(.*?\)', '', text)
        return text.strip().lower()

    def is_loose_match(self, user_answer, correct_answer, threshold=80):
        user_answer = self.normalize_text(user_answer)
        print(user_answer)
        correct_answer = self.normalize_text(correct_answer)

        if fuzz.partial_ratio(user_answer, correct_answer) >= threshold:
            return True
        return False

    def any_loose_match(self, user_answers, correct_answers, threshold=80):
        for anwser in user_answers:
            user_answer = self.normalize_text(anwser)
            for correct_answer in correct_answers:
                correct_answer = self.normalize_text(correct_answer)
                if fuzz.partial_ratio(user_answer, correct_answer) >= threshold:
                    return True
        return False

    def calculate_score(self, flashcardset):
        flashcards = flashcardset.flashcards.all()

        for flashcard in flashcards:
            user_answers = flashcard.user_answer.split(",")
            acceptable_answers = flashcard.answer.split(",")
            flashcard.correct_answer_given = self.any_loose_match(user_answers, acceptable_answers)
            flashcard.save()

        self.save_score(flashcardset)

    def save_score(self, flashcardset):
        correct_answers = flashcardset.flashcards.filter(correct_answer_given=True).count()
        total_flashcards = flashcardset.flashcards.count()
        flashcardset.score = round((correct_answers / total_flashcards) * 100, 2)
        flashcardset.save()


