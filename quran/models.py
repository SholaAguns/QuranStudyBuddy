from django.db import models
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.utils.translation.trans_real import translation

User = get_user_model()


class Chapter(models.Model):
    id  = models.IntegerField(primary_key=True)
    revelation_place  = models.TextField(max_length=100)
    revelation_order  = models.IntegerField()
    bismillah_pre = models.BooleanField()
    name_complex = models.TextField(max_length=100)
    name_arabic = models.TextField(max_length=100)
    name_simple = models.TextField(max_length=100)
    verses_count = models.IntegerField()

    def __str__(self):
        return self.translated_name.name

    def get_absolute_url(self):
        return reverse('quran:chapter', kwargs={'pk': self.id})

    class Meta:
        ordering = ['id']

class Verse(models.Model):
    id = models.IntegerField(primary_key=True)
    verse_number = models.IntegerField()
    verse_key = models.CharField(max_length=30)
    juz_number = models.IntegerField()
    hizb_number = models.IntegerField()
    rub_el_hizb_number = models.IntegerField()
    ruku_number = models.IntegerField()
    manzil_number = models.IntegerField()
    sajdah_number = models.IntegerField(null=True, blank=True)
    page_number = models.IntegerField()
    text_uthmani = models.TextField()
    image_url = models.TextField(max_length=500)
    chapter = models.ForeignKey(Chapter, related_name='verses', on_delete=models.CASCADE)
    selected_translation = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.verse_key

    def get_english_translation(self):
        english_resource_id =131
        return self.translations.filter(resource_id=english_resource_id).first().text

class TranslatedName(models.Model):
    language_name  = models.TextField(default="english", max_length=100)
    name = models.TextField(max_length=100)
    chapter = models.ForeignKey(Chapter, related_name='translated_name', on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Translation(models.Model):
    id = models.IntegerField(primary_key=True)
    resource_id = models.IntegerField()
    text = models.TextField()
    verse = models.ForeignKey(Verse, related_name="translations", on_delete=models.CASCADE)


