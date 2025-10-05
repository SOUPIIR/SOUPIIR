import os
import requests
import yaml
import re
import unicodedata

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
                "title_slugify": slugify(v["name"]),
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
    print(f"✅ Generated {path} with {len(video_list)} videos")


def generate_category_pages(video_list):
    os.makedirs("pages/categories", exist_ok=True)
    tag_template = """---
layout: category
title: "__CATEGORY_TAG__"
tag: "__CATEGORY_TAG__"
permalink: "/__CATEGORY_TAG__/"
sitemap: true
---
"""
    all_slugs = set(slug for v in video_list for slug in v["tags_category"])
    for tag_slug in all_slugs:
        filename = f"pages/categories/{tag_slug}.md"
        with open(filename, "w", encoding="utf-8") as f:
            content = tag_template.replace("__CATEGORY_TAG__", tag_slug)
            f.write(content)
    print(f"✅ Generated {len(all_slugs)} files in /pages/categories/")


def generate_group_pages(video_list):
    os.makedirs("pages/groups", exist_ok=True)
    tag_template = """---
layout: group
title: "__GROUP_TAG__"
tag: "__GROUP_TAG__"
permalink: "/__GROUP_TAG__/"
sitemap: true
---
"""
    all_slugs = set(slug for v in video_list for slug in v["tags_slugs"])
    for tag_slug in all_slugs:
        filename = f"pages/groups/{tag_slug}.md"
        with open(filename, "w", encoding="utf-8") as f:
            content = tag_template.replace("__GROUP_TAG__", tag_slug)
            f.write(content)
    print(f"✅ Generated {len(all_slugs)} files in /pages/groups/")


def generate_showcase_page(showcase_id, data_file):
    os.makedirs("pages/showcases", exist_ok=True)
    data_file_no_ext = os.path.splitext(data_file)[0]
    content = f"""---
layout: showcase
title: "Showcase {showcase_id}"
data_file: "{data_file_no_ext}"
permalink: "/showcase/{showcase_id}/"
sitemap: false
---
"""
    filename = f"pages/showcases/showcase-{showcase_id}.md"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"✅ Generated page {filename}")


def generate_video_pages(video_list):
    os.makedirs("pages/videos", exist_ok=True)
    template = """---
layout: video
title: "__TITLE__"
video_id: "__VIDEO_ID__"
video_hash: "__VIDEO_HASH__"
permalink: "/videos/__VIDEO_URL__/"
sitemap: true
thumbnail_mobile: "__THUMB_MOBILE__"
thumbnail_desktop: "__THUMB_DESKTOP__"
thumbnail_large: "__THUMB_LARGE__"
tags_category: [__TAGS_CATEGORY__]
tags_photos: [__TAGS_PHOTOS__]
tags_slugs: [__TAGS_SLUGS__]
tags_videos: [__TAGS_VIDEOS__]
description: "__DESCRIPTION__"
---
"""

    count = 0
    for v in video_list:
        if v["tags_photos"]:
            continue

        filename = f"pages/videos/{v['id']}.md"

        content = template
        content = content.replace("__TITLE__", v["title"].replace('"', "'"))
        content = content.replace("__VIDEO_ID__", v["id"])
        content = content.replace("__VIDEO_HASH__", v["hash"])
        content = content.replace("__VIDEO_URL__", slugify(v["title"]))
        content = content.replace("__THUMB_MOBILE__", v["thumbnail_mobile"] or "")
        content = content.replace("__THUMB_DESKTOP__", v["thumbnail_desktop"] or "")
        content = content.replace("__THUMB_LARGE__", v["thumbnail_large"] or "")
        content = content.replace("__TAGS_CATEGORY__", ", ".join(v["tags_category"]))
        content = content.replace("__TAGS_PHOTOS__", ", ".join(v["tags_photos"]))
        content = content.replace("__TAGS_SLUGS__", ", ".join(v["tags_slugs"]))
        content = content.replace("__TAGS_VIDEOS__", ", ".join(v["tags_videos"]))
        content = content.replace("__DESCRIPTION__", (v["description"] or "").replace('"', "'"))

        with open(filename, "w", encoding="utf-8") as f:
            f.write(content)
        count += 1
    print(f"✅ Generated {count} files in /pages/videos/")


def main():
    if not VIMEO_API_KEY:
        print("❌ VIMEO_API_KEY manquant")
        exit(1)

    if SHOWCASE_SOUPIIR:
        videos = fetch_vimeo_videos(VIMEO_API_KEY, SHOWCASE_SOUPIIR)
        save_yaml(videos, "_data/videos.yml")
        generate_group_pages(videos)
        generate_category_pages(videos)
        generate_video_pages(videos)
        print(f"✅ Showcase SOUPIIR ({SHOWCASE_SOUPIIR}) completed")

    if SHOWCASE_CLIENTS:
        showcase_ids = [s.strip() for s in SHOWCASE_CLIENTS.split(",") if s.strip()]
        for sid in showcase_ids:
            videos_clients = fetch_vimeo_videos(VIMEO_API_KEY, sid)
            yaml_file = f"videos_{sid}.yml"
            save_yaml(videos_clients, f"_data/{yaml_file}")
            generate_showcase_page(sid, yaml_file)
        print(f"✅ Showcases CLIENTS ({len(showcase_ids)} IDs) completed")

if __name__ == "__main__":
    main()
