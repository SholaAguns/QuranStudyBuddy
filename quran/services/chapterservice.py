import requests
from quran.models import Chapter, TranslatedName

class ChapterService:
    def populate_chapters(self):
        url = "https://api.quran.com/api/v4/chapters/"

        payload = {}
        headers = {
            'Accept': 'application/json'
        }

        response = requests.request("GET", url, headers=headers, data=payload)

        data = response.json()


        for chapter_data in data["chapters"]:
            chapter, created = Chapter.objects.update_or_create(
                id=chapter_data["id"],
                defaults={
                    "revelation_place": chapter_data["revelation_place"],
                    "revelation_order": chapter_data["revelation_order"],
                    "bismillah_pre": chapter_data["bismillah_pre"],
                    "name_complex": chapter_data["name_complex"],
                    "name_arabic": chapter_data["name_arabic"],
                    "name_simple": chapter_data["name_simple"],
                    "verses_count": chapter_data["verses_count"],
                }
            )

            translated_name_data = chapter_data.get("translated_name", {})
            if translated_name_data:
                TranslatedName.objects.update_or_create(
                    chapter=chapter,
                    defaults={
                        "language_name": translated_name_data.get("language_name", "english"),
                        "name": translated_name_data["name"],
                    }
                )