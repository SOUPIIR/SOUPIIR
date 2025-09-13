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
    response = requests.get(
        url,
        headers=headers,
        params={"sort": "manual", "page": page, "per_page": 50},
    )
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

        thumbnail_mobile = ""
        thumbnail_desktop = ""
        thumbnail_large = ""

        if v.get("pictures") and v["pictures"].get("sizes"):
            for s in v["pictures"]["sizes"]:
                if s["width"] == 640 and s["height"] == 360:
                    thumbnail_mobile = s["link"]
                elif s["width"] == 960 and s["height"] == 540:
                    thumbnail_desktop = s["link"]
                elif s["width"] == 1280 and s["height"] == 720:
                    thumbnail_large = s["link"]

        tags = [t["tag"] for t in v.get("tags", [])]

        video_list.append({
            "id": video_id,
            "hash": video_hash,
            "title": v["name"],
            "description": v.get("description", ""),
            "thumbnail_mobile": thumbnail_mobile,
            "thumbnail_desktop": thumbnail_desktop,
            "thumbnail_large": thumbnail_large,
            "tags": tags,
        })

    if data.get("paging", {}).get("next"):
        page += 1
    else:
        break

os.makedirs("_data", exist_ok=True)

with open("_data/videos.yml", "w", encoding="utf-8") as f:
    yaml.dump(video_list, f, allow_unicode=True)

print(f"✅ Généré _data/videos.yml avec {len(video_list)} vidéos")

# --- Génération des pages par tag ---
os.makedirs("tags", exist_ok=True)

tag_template = """---
layout: tag
tag: "__TAG__"
permalink: "/__TAG__/"
---
"""

# Récupération unique des tags
all_tags = set(t for v in video_list for t in v["tags"])

for tag in all_tags:
    filename = f"tags/{tag}.md"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(tag_template.replace("__TAG__", tag))

print(f"✅ Généré {len(all_tags)} fichiers dans /tags/")
