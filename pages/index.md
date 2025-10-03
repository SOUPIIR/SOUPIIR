---
layout: default
title:
permalink: /
sitemap: true
---

<div class="grid">
    {%- assign shown_tags = "" | split: "" -%}

    {% for video in site.data.videos %}
        {% if video.tags_slugs == empty %}
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
        {% else %}
            {% for t in video.tags_slugs %}
            {% unless shown_tags contains t %}
                <div class="grid-item-mosaic link" data-id="{{ video.id }}">
                    <a href="{{ '/' | append: t | slugify: 'pretty' | append: '/' | relative_url }}">
                        <img
                            src="{{ video.thumbnail_desktop }}"
                            srcset="
                                {{ video.thumbnail_mobile }} 640w,
                                {{ video.thumbnail_desktop }} 960w,
                                {{ video.thumbnail_large }} 1280w"
                            sizes="(max-width: 600px) 640px, (max-width: 1024px) 960px, 1280px"
                            alt="{{ video.title }}"
                            width="1280"
                            height="720"
                            loading="lazy" />
                        <div class="overlay">
                            <video muted loop preload="none" playsinline></video>
                            <h2 data-content="{{ t }}" class="glitch">{{ t }}</h2>
                        </div>
                    </a>
                    {% if video.tags_category != empty %}
                        <a href="{{ '/' | append: video.tags_category | slugify: 'pretty' | append: '/' | relative_url }}">
                        <span  class="glitch {{ video.tags_category }}" data-content="{{ video.tags_category }}">{{ video.tags_category }}</span></a>
                    {% endif %}
                </div>
                {%- assign shown_tags = shown_tags | push: t -%}
            {% endunless %}
            {% endfor %}
        {% endif %}
    {% endfor %}
</div>
