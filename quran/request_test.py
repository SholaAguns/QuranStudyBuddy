import requests

#url = "https://api.quran.com/api/v4/verses/by_chapter/1"
url = "https://api.alquran.cloud/v1/ayah/262/ar.alafasy"
#url = "https://api.alquran.cloud/v1/edition/format/audio"

payload={}
headers = {
  'Accept': 'application/json'
}
params = {
                "translations": 131,
                "fields": "text_uthmani,image_url",
                "words": "true",
                "word_fields": "text_uthmani,verse_key"
            }
response = requests.request("GET", url, headers=headers, data=payload)

print(response.text)