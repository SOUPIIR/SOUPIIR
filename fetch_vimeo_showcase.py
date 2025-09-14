import os
import requests
import yaml
import re
import unicodedata

VIMEO_API_KEY = os.getenv("VIMEO_API_KEY")
SHOWCASE_ID = os.getenv("SHOWCASE_ID")


def slugify(value: str) -> str:
    value = str(value)
    value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode('ascii')
    value = re.sub(r'[^a-zA-Z0-9]+', '-', value)
    value = value.strip('-')
    return value.lower()


def fetch_vimeo_videos(api_key: str, showcase_id: str):
    url = f"https://api.vimeo.com/albums/{showcase_id}/videos"
    headers = {"Authorization": f"bearer {api_key}"}

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
                "tags_slugs": [slugify(t) for t in tags],
            })

        if data.get("paging", {}).get("next"):
            page += 1
        else:
            break

    return video_list


def save_yaml(video_list, path="_data/videos.yml"):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        yaml.dump(video_list, f, allow_unicode=True)
    print(f"✅ Généré {path} avec {len(video_list)} vidéos")


def generate_tag_pages(video_list):
    os.makedirs("tags", exist_ok=True)

    tag_template = """---
layout: tag
tag: "__TAG__"
permalink: "/__TAG__/"
---
"""

    all_tags = set(t for v in video_list for t in v["tags"])

    for tag in all_tags:
        tag_slug = slugify(tag)
        filename = f"tags/{tag_slug}.md"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(tag_template.replace("__TAG__", tag_slug))

    print(f"✅ Généré {len(all_tags)} fichiers dans /tags/")


def main():
    if not VIMEO_API_KEY or not SHOWCASE_ID:
        print("❌ VIMEO_API_KEY ou SHOWCASE_ID manquant")
        exit(1)

    videos = fetch_vimeo_videos(VIMEO_API_KEY, SHOWCASE_ID)
    save_yaml(videos)
    generate_tag_pages(videos)


if __name__ == "__main__":
    main()
