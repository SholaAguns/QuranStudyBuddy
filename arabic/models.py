from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse

User = get_user_model()

class Phrase(models.Model):
    user = models.ForeignKey(User, related_name='phrase', on_delete=models.CASCADE)
    text = models.TextField(max_length=300)
    category = models.CharField(max_length=60)
    tags = models.CharField(max_length=200, null=True)
    translation = models.TextField(max_length=300)
    image = models.ImageField(upload_to="images", null=True)
    created_dt = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        return reverse('arabic:phrase_detail', kwargs={'pk': self.id})

    class Meta:
        ordering = ['text']
        unique_together = ['user', 'text']

