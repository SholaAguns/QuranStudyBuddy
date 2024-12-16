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
        print("In looose")
        user_answer = self.normalize_text(user_answer)
        print(user_answer)
        correct_answer = self.normalize_text(correct_answer)

        if fuzz.partial_ratio(user_answer, correct_answer) >= threshold:
            return True
        return False

    def calculate_score(self, flashcardset):
        print("In service")
        flashcards = flashcardset.flashcards.all()

        for flashcard in flashcards:
            print("In service" + flashcard.user_answer)
            print("Correct answer: " + flashcard.answer)
            flashcard.correct_answer_given = self.is_loose_match(flashcard.user_answer, flashcard.answer)
            print("Correct: " + str(flashcard.correct_answer_given))
            flashcard.save()


        correct_answers = flashcardset.flashcards.filter(correct_answer_given=True).count()
        print("correct ans " + str(correct_answers))
        total_flashcards = flashcardset.flashcards.count()
        print("total ans " + str(total_flashcards))
        flashcardset.score = round((correct_answers / total_flashcards) * 100, 2)
        flashcardset.save()
        print("Score: " + str(flashcardset.score))


