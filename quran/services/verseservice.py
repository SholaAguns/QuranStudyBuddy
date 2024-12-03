import requests

from quran.models import Chapter, Verse, Translation

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
                "page": current_page
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
                Translation.objects.update_or_create(
                    id=translation["id"],
                    verse=verse,
                    resource_id=translation["resource_id"],
                    text=translation["text"],
                )

