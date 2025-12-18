---
layout: default
---
<h1 class="hidden">{{ page.tag | split: "-" | join: " " | capitalize }}</h1>
<div class="back-link-container"></div>
<div class="grid tag {{ page.url | slugify: 'pretty' }}">
    {% assign videos = site.data.videos | where_exp: "v", "v.tags_slugs contains page.tag" %}
    {% for video in videos %}
        {% include block-mosaic.html
            id=video.id
            hash=video.hash
            title=video.title
            title_slugify = video.title_slugify
            thumbnail_desktop=video.thumbnail_desktop
            thumbnail_mobile=video.thumbnail_mobile
            thumbnail_large=video.thumbnail_large
            description=video.description
            tags_category=video.tags_category
            tags_photos=video.tags_photos
            tags_videos=video.tags_videos %}
    {% endfor %}
</div>
