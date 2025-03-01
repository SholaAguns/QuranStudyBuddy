from collections import Counter

from scorecard.models import Scorecard
from django.contrib.auth import get_user_model
User = get_user_model()

scorecard = Scorecard.objects.get(id=1)
all_scores =scorecard.get_all_scores()

valid_scores = [score for score in all_scores if score.chapter_id]

if not valid_scores:
    print("No valid scores")

# Count occurrences of each chapter_id
chapter_counts = Counter(score.chapter_id for score in valid_scores)

print(f"Chapter Counts: {chapter_counts}")

# Get the most frequent chapter_id
#strongest_chapter_id = max(chapter_counts, key=chapter_counts.get)

# Get total count of scores for that chapter_id
#total_count = chapter_counts[strongest_chapter_id]

# Count correct answers for that chapter_id
#correct_count = sum(1 for score in valid_scores
                    #if score.chapter_id == strongest_chapter_id and score.correct_answer_given)



