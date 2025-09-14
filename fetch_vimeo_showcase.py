import os
import requests
import yaml
import re
import unicodedata

VIMEO_API_KEY = os.getenv("VIMEO_API_KEY")
SHOWCASE_LIST = os.getenv("SHOWCASE_LIST")

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

            tags_slugs = [slugify(t["tag"]) for t in v.get("tags", [])]

            video_list.append({
                "id": video_id,
                "hash": video_hash,
                "title": v["name"],
                "description": v.get("description", ""),
                "thumbnail_mobile": thumbnail_mobile,
                "thumbnail_desktop": thumbnail_desktop,
                "thumbnail_large": thumbnail_large,
                "tags_slugs": tags_slugs,
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

def generate_tag_pages(video_list):
    os.makedirs("tags", exist_ok=True)
    tag_template = """---
layout: tag
tag: "__TAG__"
permalink: "/__TAG__/"
---
"""
    all_slugs = set(slug for v in video_list for slug in v["tags_slugs"])
    for tag_slug in all_slugs:
        filename = f"tags/{tag_slug}.md"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(tag_template.replace("__TAG__", tag_slug))
    print(f"✅ Généré {len(all_slugs)} fichiers dans /tags/")

def generate_showcase_page(showcase_id, data_file):
    os.makedirs("showcases", exist_ok=True)
    data_file_no_ext = os.path.splitext(data_file)[0]
    content = f"""---
layout: showcase
title: "Showcase {showcase_id}"
data_file: "{data_file_no_ext}"
permalink: "/showcase/{showcase_id}/"
---
"""
    filename = f"showcases/showcase-{showcase_id}.md"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"✅ Généré page {filename}")

def main():
    if not VIMEO_API_KEY or not SHOWCASE_LIST:
        print("❌ VIMEO_API_KEY ou SHOWCASE_LIST manquant")
        exit(1)

    showcase_ids = [s.strip() for s in SHOWCASE_LIST.split(",")]
    first_showcase = showcase_ids[0]
    other_showcases = showcase_ids[1:]

    # Premier showcase -> videos.yml
    videos = fetch_vimeo_videos(VIMEO_API_KEY, first_showcase)
    save_yaml(videos, "_data/videos.yml")
    generate_tag_pages(videos)
    generate_showcase_page(first_showcase, "videos.yml")

    # Autres showcases -> videos_<id>.yml
    for sid in other_showcases:
        videos_other = fetch_vimeo_videos(VIMEO_API_KEY, sid)
        yaml_file = f"videos_{sid}.yml"
        save_yaml(videos_other, f"_data/{yaml_file}")
        generate_tag_pages(videos_other)
        generate_showcase_page(sid, yaml_file)

if __name__ == "__main__":
    main()
