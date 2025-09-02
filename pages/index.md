---
layout: default
title: Home
permalink: /
---


<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px;">
  {% for video in site.data.videos %}
    <div style="border: 1px solid #ddd; border-radius: 8px; overflow: hidden; padding: 10px;">
      <a href="{{ video.url }}" target="_blank">
        <img src="{{ video.thumbnail }}" alt="{{ video.title }}" style="width:100%; border-radius: 6px;">
      </a>
      <h3>{{ video.title }}</h3>
      <p>{{ video.description | truncate: 100 }}</p>
    </div>
  {% endfor %}
</div>
