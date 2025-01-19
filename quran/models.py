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
    selected_audio = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.verse_key

    def get_english_translation(self):
        english_resource_id =131
        return self.translations.filter(resource_id=english_resource_id).first().text

class Word(models.Model):
    id = models.IntegerField(primary_key=True)
    audio_url = models.TextField(null=True)
    text_uthmani = models.TextField()
    text = models.TextField()
    page_number = models.IntegerField()
    line_number = models.IntegerField()
    position = models.IntegerField()
    verse_key = models.CharField(max_length=30)
    char_type_name = models.CharField(max_length=30)
    verse = models.ForeignKey(Verse, related_name='words', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.verse_key} : {self.text_uthmani}'

class TranslatedName(models.Model):
    language_name  = models.TextField(default="english", max_length=100)
    name = models.TextField(max_length=100)
    chapter = models.ForeignKey(Chapter, related_name='translated_name', on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class VerseTranslation(models.Model):
    id = models.IntegerField(primary_key=True)
    resource_id = models.IntegerField()
    text = models.TextField()
    verse = models.ForeignKey(Verse, related_name="translations", on_delete=models.CASCADE)

class WordTranslation(models.Model):
    language_name = models.CharField(max_length=100)
    text = models.TextField()
    word = models.OneToOneField(Word, related_name="translation", on_delete=models.CASCADE)

class WordTransliteration(models.Model):
    language_name = models.CharField(max_length=100)
    text = models.TextField()
    word = models.OneToOneField(Word, related_name="transliteration", on_delete=models.CASCADE)

class AudioEdition(models.Model):
    identifier = models.TextField()
    language = models.TextField()
    name = models.TextField()
    english_name = models.TextField()
    format = models.TextField()
    type = models.TextField()
    direction = models.TextField(null=True)

class HostedVerseAudio(models.Model):
    edition = models.ForeignKey(AudioEdition, on_delete=models.DO_NOTHING)
    audio_path = models.TextField()
    audio_secondary_path = models.TextField(null=True, blank=True)
    verse = models.ForeignKey(Verse, related_name="audio", on_delete=models.DO_NOTHING)

class VerseSelection(models.Model):
    start_verse_id = models.IntegerField()
    end_verse_id = models.IntegerField()
    start_chapter_id = models.IntegerField()
    end_chapter_id = models.IntegerField()
    juz_number = models.IntegerField()
    title = models.CharField(max_length=80)
    user = models.ForeignKey(User, related_name='verse_selection', on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['start_verse_id']