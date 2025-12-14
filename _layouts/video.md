---
layout: default
---

<div class="back-link-container"><a href="#" id="back-link">Back</a></div>
<div class="grid-item-mosaic simple-video videos" data-id="{{ page.video_id }}">
    <a
        href="https://player.vimeo.com/video/{{ page.video_id }}?h={{ page.video_hash }}&autoplay=1&color=000000&title=0&byline=0&progress_bar=1&controls=1&quality=1080p"
        data-title="{{ page.title }}"
        data-description="{{ page.description }}"
        lightbox="iframe">
        <img
            src="{{ page.thumbnail_desktop }}"
            srcset="
                {{ page.thumbnail_mobile }} 640w,
                {{ page.thumbnail_desktop }} 960w,
                {{ page.thumbnail_large }} 1280w"
            sizes="(max-width: 600px) 640px, (max-width: 1024px) 960px, 1280px"
            alt="Photo from {{ page.title }}"
            width="1280"
            height="720"
            loading="lazy" />
        <div class="overlay">
            <video muted loop preload="none" playsinline></video>
        </div>
    </a>

    {% if page.tags_category and page.tags_category != empty %}
        {% for category in page.tags_category %}
        <a href="{{ '/' | append: category | slugify: 'pretty' | append: '/' | relative_url }}">
            <span class="{{ category }}">{{ category }}</span>
        </a>
        {% endfor %}
    {% endif %}
</div>
<div class="simple-video">
    <h1 data-content="{{ page.title }}">{{ page.title }}</h1>
    {% include social-media-share.html %}
</div>