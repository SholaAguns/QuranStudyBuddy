import requests

url = "https://api.quran.com/api/v4/verses/by_chapter/1"

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
response = requests.request("GET", url, headers=headers, data=payload, params=params)

print(response.text)