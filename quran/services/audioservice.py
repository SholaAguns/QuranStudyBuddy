import requests

from quran.models import Verse,  AudioEdition, HostedVerseAudio

class AudioService:
    BASE_URL = "https://api.alquran.cloud/v1/"

    def fetch_all_editions(self):
        edition_endpoint = "edition/format/audio"
        url = f"{self.BASE_URL}{edition_endpoint}"

        headers = {
            'Accept': 'application/json'
        }

        response = requests.get(url, headers=headers)

        if response.status_code != 200:
            print(f"Failed to fetch data for Editions")
        else:
            response_data = response.json()

            self.save_editions(response_data.get("data", []))

    def populate_hosted_audio_objects(self):
        for verse in Verse.objects.all():
            for edition in AudioEdition.objects.all():
                self.fetch_and_save_hosted_verse_audio_objects(verse.id, edition.identifier)

    def save_editions(self, editions):
        for edition_data in editions:
            edition, created = AudioEdition.objects.update_or_create(
                identifier = edition_data["identifier"],
                language = edition_data["language"],
                name = edition_data["name"],
                englishName = edition_data["englishName"],
                format = edition_data["format"],
                type =  edition_data["type"],
                direction = edition_data["direction"]
            )

    def fetch_and_save_hosted_verse_audio_objects(self, verse_id, edition_identifier):
        verse_endpoint = f"ayah/{verse_id}/{edition_identifier}"
        url = f"{self.BASE_URL}{verse_endpoint}"

        headers = {
            'Accept': 'application/json'
        }

        response = requests.get(url, headers=headers)

        if response.status_code != 200:
            print(f"Failed to fetch data for Editions")
        else:
            response_data = response.json()
            verse_data = response_data.get("data", [])
            edition = AudioEdition.objects.get(identifier=edition_identifier)
            verse = Verse.objects.get(id=verse_id)

            hosted_verse_audio, created = HostedVerseAudio.objects.update_or_create(
                edition=edition,
                verse = verse,
                audio_path=verse_data["audio"],
                audio_secondary_path=verse_data["audioSecondary"]
            )


