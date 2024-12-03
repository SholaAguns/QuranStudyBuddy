import requests

chapter_number= 1

url = "https://api.quran.com/api/v4/verses/by_chapter/1"

payload={}
headers = {
  'Accept': 'application/json'
}

params = {
                "translations": 131,
                "fields": "text_uthmani,image_url",
            }

response = requests.request("GET", url, headers=headers, data=payload, params=params)

print(response.text)