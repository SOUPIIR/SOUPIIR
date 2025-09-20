import os
import requests
import yaml
import re
import unicodedata
from datetime import date

VIMEO_API_KEY = os.getenv("VIMEO_API_KEY")
SHOWCASE_SOUPIIR = os.getenv("SHOWCASE_SOUPIIR")
SHOWCASE_CLIENTS = os.getenv("SHOWCASE_CLIENTS")

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
            print(f"❌ Erreur API pour showcase {showcase_id}:", response.text)
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

            tags_slugs = []
            tags_category = []
            tags_photos = []
            tags_videos = []

            for t in v.get("tags", []):
                tag_text = t["tag"]

                if tag_text.startswith("categorie:"):
                    parts = tag_text.split(":", 1)
                    if len(parts) > 1:
                        tags_category.append(slugify(parts[1]))

                elif tag_text.startswith("photo:"):
                    parts = tag_text.split(":", 1)
                    if len(parts) > 1:
                        tags_photos.append(slugify(parts[1]))

                elif tag_text.startswith("video:"):
                    parts = tag_text.split(":", 1)
                    if len(parts) > 1:
                        tags_videos.append(slugify(parts[1]))

                else:
                    tags_slugs.append(slugify(tag_text))

            video_list.append({
                "id": video_id,
                "hash": video_hash,
                "title": v["name"],
                "description": v.get("description", ""),
                "thumbnail_mobile": thumbnail_mobile,
                "thumbnail_desktop": thumbnail_desktop,
                "thumbnail_large": thumbnail_large,
                "tags_slugs": tags_slugs,
                "tags_category": tags_category,
                "tags_photos": tags_photos,
                "tags_videos": tags_videos,
            })

        if data.get("paging", {}).get("next"):
            page += 1
        else:
            break

    return video_list

def save_yaml(video_list, path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        yaml.dump(video_list, f, allow_unicode=True)
    print(f"✅ Généré {path} avec {len(video_list)} vidéos")

def generate_category_pages(video_list):
    os.makedirs("categories", exist_ok=True)
    today = date.today().isoformat()
    tag_template = """---
layout: category
title: "__CATEGORY_TAG__"
tag: "__CATEGORY_TAG__"
permalink: "/__CATEGORY_TAG__/"
date: __DATE__
sitemap: true
---
"""
    all_slugs = set(slug for v in video_list for slug in v["tags_category"])
    for tag_slug in all_slugs:
        filename = f"categories/{tag_slug}.md"
        with open(filename, "w", encoding="utf-8") as f:
            content = tag_template.replace("__CATEGORY_TAG__", tag_slug).replace("__DATE__", today)
            f.write(content)
    print(f"✅ Généré {len(all_slugs)} fichiers dans /categories/")


def generate_group_pages(video_list):
    os.makedirs("groups", exist_ok=True)
    today = date.today().isoformat()
    tag_template = """---
layout: group
title: "__GROUP_TAG__"
tag: "__GROUP_TAG__"
permalink: "/__GROUP_TAG__/"
date: __DATE__
sitemap: true
---
"""
    all_slugs = set(slug for v in video_list for slug in v["tags_slugs"])
    for tag_slug in all_slugs:
        filename = f"groups/{tag_slug}.md"
        with open(filename, "w", encoding="utf-8") as f:
            content = tag_template.replace("__GROUP_TAG__", tag_slug).replace("__DATE__", today)
            f.write(content)
    print(f"✅ Généré {len(all_slugs)} fichiers dans /groups/")

def generate_showcase_page(showcase_id, data_file):
    os.makedirs("showcases", exist_ok=True)
    data_file_no_ext = os.path.splitext(data_file)[0]
    content = f"""---
layout: showcase
title: "Showcase {showcase_id}"
data_file: "{data_file_no_ext}"
permalink: "/showcase/{showcase_id}/"
sitemap: false
---
"""
    filename = f"showcases/showcase-{showcase_id}.md"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"✅ Généré page {filename}")

def main():
    if not VIMEO_API_KEY:
        print("❌ VIMEO_API_KEY manquant")
        exit(1)

    if SHOWCASE_SOUPIIR:
        videos = fetch_vimeo_videos(VIMEO_API_KEY, SHOWCASE_SOUPIIR)
        save_yaml(videos, "_data/videos.yml")
        generate_group_pages(videos)
        generate_category_pages(videos)
        print(f"✅ Showcase SOUPIIR ({SHOWCASE_SOUPIIR}) traité")

    if SHOWCASE_CLIENTS:
        showcase_ids = [s.strip() for s in SHOWCASE_CLIENTS.split(",") if s.strip()]
        for sid in showcase_ids:
            videos_clients = fetch_vimeo_videos(VIMEO_API_KEY, sid)
            yaml_file = f"videos_{sid}.yml"
            save_yaml(videos_clients, f"_data/{yaml_file}")
            generate_showcase_page(sid, yaml_file)
        print(f"✅ Showcases CLIENTS ({len(showcase_ids)} IDs) traités")

if __name__ == "__main__":
    main()
