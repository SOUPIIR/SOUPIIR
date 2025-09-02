import os
import requests
import yaml


ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
SHOWCASE_ID = os.getenv("SHOWCASE_ID")


if not ACCESS_TOKEN or not SHOWCASE_ID:
    print("❌ ACCESS_TOKEN ou SHOWCASE_ID manquant")
    exit(1)

url = f"https://api.vimeo.com/albums/{SHOWCASE_ID}/videos"
headers = {"Authorization": f"bearer {ACCESS_TOKEN}"}

video_list = []
page = 1

while True:
    response = requests.get(url, headers=headers, params={"page": page, "per_page": 50})
    if response.status_code != 200:
        print("❌ Erreur API:", response.text)
        break

    data = response.json()
    videos = data.get("data", [])

    if not videos:
        break

    for v in videos:
        video_list.append({
            "id": v["uri"].split("/")[-1],
            "title": v["name"],
            "description": v.get("description", ""),
            "url": f"https://vimeo.com/{v['uri'].split('/')[-1]}",
            "embed_url": f"https://player.vimeo.com/video/{v['uri'].split('/')[-1]}",
            "thumbnail": v["pictures"]["sizes"][-1]["link"] if v.get("pictures") else ""
        })

    if data.get("paging", {}).get("next"):
        page += 1
    else:
        break

os.makedirs("_data", exist_ok=True)
with open("_data/videos.yml", "w", encoding="utf-8") as f:
    yaml.dump(video_list, f, allow_unicode=True)

print(f"✅ Généré _data/videos.yml avec {len(video_list)} vidéos")
