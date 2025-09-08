import os
import requests
import yaml


VIMEO_API_KEY = os.getenv("VIMEO_API_KEY")
SHOWCASE_ID = os.getenv("SHOWCASE_ID")


if not VIMEO_API_KEY or not SHOWCASE_ID:
    print("❌ VIMEO_API_KEY ou SHOWCASE_ID manquant")
    exit(1)

url = f"https://api.vimeo.com/albums/{SHOWCASE_ID}/videos"
headers = {"Authorization": f"bearer {VIMEO_API_KEY}"}

video_list = []
page = 1

while True:
    response = requests.get(url, headers=headers, params={"sort": "manual", "page": page, "per_page": 50})
    if response.status_code != 200:
        print("❌ Erreur API:", response.text)
        break

    data = response.json()
    videos = data.get("data", [])

    if not videos:
        break

    for v in videos:
        uri_last = v["uri"].split("/")[-1]
        parts = uri_last.split(":")
        video_id = parts[0]
        video_hash = parts[1] if len(parts) > 1 else ""

        thumbnail = ""
        if v.get("pictures") and v["pictures"].get("sizes"):
            for s in v["pictures"]["sizes"]:
                if s["width"] == 640 and s["height"] == 360:
                    thumbnail = s["link"]
                    break

        video_list.append({
            "id": video_id,
            "hash": video_hash,
            "title": v["name"],
            "description": v.get("description", ""),
            "thumbnail": thumbnail
        })

    if data.get("paging", {}).get("next"):
        page += 1
    else:
        break

os.makedirs("_data", exist_ok=True)
with open("_data/videos.yml", "w", encoding="utf-8") as f:
    yaml.dump(video_list, f, allow_unicode=True)

print(f"✅ Généré _data/videos.yml avec {len(video_list)} vidéos")
