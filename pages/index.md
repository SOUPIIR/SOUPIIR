---
layout: default
title: Home
permalink: /
---

<div class="gallery gallery-home">
  {% for video in site.data.videos %}
    {% include block.html id=video.id hash=video.hash title=video.title image=video.thumbnail text=video.description %}
  {% endfor %}
</div>