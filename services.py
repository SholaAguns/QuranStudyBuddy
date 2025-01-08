import os

import django
from django.db import connections

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'qsbproject.settings')
django.setup()

from quran.models import Verse, TranslatedName, VerseTranslation, WordTranslation, WordTransliteration, Word

# Connect to the external database
external_cursor = connections['external'].cursor()


def copy_table_data(model, table_name, fields):
    """
    Copies data from an external table to the current database model.
    """
    query = f"SELECT {', '.join(fields)} FROM {table_name}"
    external_cursor.execute(query)
    rows = external_cursor.fetchall()

    # Bulk create objects
    model_objects = [model(**dict(zip(fields, row))) for row in rows]
    model.objects.bulk_create(model_objects, ignore_conflicts=True)
    print(f"Copied {len(model_objects)} rows into {model.__name__}")


# Copy data for all models

copy_table_data(Verse, 'verse', [
    'id', 'verse_number', 'verse_key', 'juz_number', 'hizb_number',
    'rub_el_hizb_number', 'ruku_number', 'manzil_number', 'sajdah_number',
    'page_number', 'text_uthmani', 'image_url', 'selected_translation', 'chapter_id'
])

copy_table_data(TranslatedName, 'translatedname', [
    'language_name', 'name', 'chapter_id'
])



copy_table_data(VerseTranslation, 'versetranslation', [
    'id', 'resource_id', 'text', 'verse_id'
])

copy_table_data(Word, 'word', [
    'id', 'audio_url', 'text_uthmani', 'text', 'page_number', 'line_number',
    'position', 'verse_key', 'char_type_name', 'verse_id'
])

copy_table_data(WordTranslation, 'wordtranslation', [
    'id', 'language_name', 'text', 'word_id'
])

copy_table_data(WordTransliteration, 'wordtransliteration', [
    'id', 'language_name', 'text', 'word_id'
])

print("Data transfer complete!")
