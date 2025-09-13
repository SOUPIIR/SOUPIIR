---
layout: default
title: Home
permalink: /
---

<div class="grid">
  {%- assign shown_tags = "" | split: "" -%}

  {% for video in site.data.videos %}
    {% if video.tags == empty %}
      {% include block-mosaic.html
          id=video.id
          hash=video.hash
          title=video.title
          thumbnail_desktop=video.thumbnail_desktop
          thumbnail_mobile=video.thumbnail_mobile
          thumbnail_large=video.thumbnail_large
          description=video.description %}
    {% else %}
      {% assign first_tag = video.tags[0] %}
      {% unless shown_tags contains first_tag %}
        <div class="grid-item-mosaic link">
          <a href="{{ '/' | append: first_tag | relative_url }}">
            <img
              src="{{video.thumbnail_desktop}}"
              srcset="
                  {{video.thumbnail_mobile}} 640w,
                  {{video.thumbnail_desktop}} 960w,
                  {{video.thumbnail_large}} 1280w"
              sizes="(max-width: 600px) 640px, (max-width: 1024px) 960px, 1280px"
              alt="{{video.title}}"
              loading="lazy" />
            <div class="overlay">
              <h2>{{ first_tag }}</h2>
            </div>
          </a>
        </div>
        {%- assign shown_tags = shown_tags | push: first_tag -%}
      {% endunless %}
    {% endif %}
  {% endfor %}
</div>