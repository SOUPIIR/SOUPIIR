---
layout: default
title: Home
permalink: /
---


<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px;">
  {% for video in site.data.videos %}
    <div style="overflow: hidden; padding: 10px;">
      <a href="{{ video.url }}" video-id="{{ video.id }}" video-hash="{{ video.hash }}" video-title="{{ video.title }}" video-text="{{ video.description }}" lightbox="iframe">
        <img src="{{ video.thumbnail }}" alt="{{ video.title }}" style="width:100%; border-radius: 6px;">
        <h3>{{ video.title }}</h3>
      </a>
    </div>
  {% endfor %}
</div>
