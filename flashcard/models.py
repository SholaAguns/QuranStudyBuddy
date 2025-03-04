from django.db import models
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()


class FlashcardSet(models.Model):
    user = models.ForeignKey(User, related_name='flashcardset', on_delete=models.CASCADE)
    type = models.CharField(max_length=60)
    created_dt = models.DateTimeField()
    title = models.CharField(max_length=100)
    amount = models.IntegerField()
    score = models.DecimalField(null=True, blank=True, decimal_places=2, max_digits=5)

    def get_absolute_url(self):
        return reverse('flashcards:flashcardset_detail', kwargs={'pk': self.id})

    class Meta:
        ordering = ['-created_dt']
        unique_together = ['user', 'title']


class Flashcard(models.Model):
    flashcardset = models.ForeignKey(FlashcardSet, related_name='flashcards', on_delete=models.CASCADE)
    question = models.TextField()
    answer = models.TextField()
    info = models.JSONField(null=True, blank=True)
    audio_answer = models.FileField(upload_to='audio', null=True)
    image = models.ImageField(upload_to="images", null=True)
    created_dt = models.DateTimeField(auto_now=True)
    user_answer = models.TextField(null=True)
    correct_answer_given = models.BooleanField(null=True)
    selected_audio = models.TextField(blank=True, null=True)
    audio_filepaths = models.JSONField(null=True, blank=True)