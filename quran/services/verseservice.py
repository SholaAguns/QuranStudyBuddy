import requests

from quran.models import Chapter, Verse, VerseTranslation, Word, WordTranslation, WordTransliteration


class VerseService:
    BASE_URL = "https://api.quran.com/api/v4/verses/by_chapter/"

    def populate_verses(self):
        for chapter in Chapter.objects.all():
            self.fetch_verses_by_chapter(chapter.id)

    def fetch_verses_by_chapter(self, chapter_id):
        current_page = 1
        next_page = True

        while next_page:
            # Build the URL with query parameters
            url = f"{self.BASE_URL}{chapter_id}"
            params = {
                "translations": 131,
                "fields": "text_uthmani,image_url",
                "page": current_page,
                "words": "true",
                "word_fields": "text_uthmani,verse_key"
            }
            headers = {
                'Accept': 'application/json'
            }

            response = requests.get(url, headers=headers, params=params)

            if response.status_code != 200:
                print(f"Failed to fetch data for Chapter {chapter_id}, Page {current_page}")
                break

            data = response.json()

            self.save_verses(chapter_id, data.get("verses", []))

            pagination = data.get("pagination", {})
            current_page = pagination.get("current_page", 1) + 1
            next_page = pagination.get("next_page") is not None

    def save_verses(self, chapter_id, verses):
        current_chapter = Chapter.objects.get(id=chapter_id)

        for verse_data in verses:
            verse, created = Verse.objects.update_or_create(
                id=verse_data["id"],
                defaults={
                    "verse_key": verse_data["verse_key"],
                    "verse_number": verse_data["verse_number"],
                    "chapter": current_chapter,
                    "hizb_number": verse_data["hizb_number"],
                    "juz_number": verse_data["juz_number"],
                    "manzil_number": verse_data["manzil_number"],
                    "page_number": verse_data["page_number"],
                    "rub_el_hizb_number": verse_data["rub_el_hizb_number"],
                    "ruku_number": verse_data["ruku_number"],
                    "sajdah_number": verse_data.get("sajdah_number"),
                    "text_uthmani": verse_data.get("text_uthmani"),
                }
            )
            translations = verse_data.get("translations", {})
            for translation in translations:
                VerseTranslation.objects.update_or_create(
                    id=translation["id"],
                    verse=verse,
                    resource_id=translation["resource_id"],
                    text=translation["text"],
                )
            words = verse_data.get("words", {})
            for word_data in words:
               word, created = Word.objects.update_or_create(
                    verse=verse,
                    id=word_data["id"],
                    audio_url=word_data["audio_url"],
                    char_type_name=word_data["char_type_name"],
                    line_number=word_data["line_number"],
                    page_number=word_data["page_number"],
                    position=word_data["position"],
                    text_uthmani=word_data["text_uthmani"],
                    text=word_data["text"],
                    verse_key=word_data["verse_key"],
                )

               word_translation_data = word_data.get("translation", {})
               if word_translation_data:
                   WordTranslation.objects.update_or_create(
                       word=word,
                       defaults={
                           "language_name": word_translation_data.get("language_name", "english"),
                           "text": word_translation_data["text"],
                       }
                   )
               word_transliteration_data = word_data.get("transliteration", {})
               if word_transliteration_data:
                   WordTransliteration.objects.update_or_create(
                       word=word,
                       defaults={
                           "language_name": word_transliteration_data.get("language_name", "english"),
                           "text": word_transliteration_data["text"],
                       }
                   )



