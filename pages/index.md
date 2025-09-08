---
layout: default
title: Home
permalink: /
---

<div class="grid">
  {% for video in site.data.videos %}
    {% include block-mosaic.html id=video.id hash=video.hash title=video.title image=video.thumbnail text=video.description %}
  {% endfor %}
</div>