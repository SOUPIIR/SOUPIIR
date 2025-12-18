#!/bin/bash

SRC_DIR="./assets/videos"
OUT_DIR="./assets/videos/optimized"

mkdir -p "$OUT_DIR"

for file in "$SRC_DIR"/*.mp4; do
  [ -e "$file" ] || continue

  filename=$(basename "$file")

  output="$OUT_DIR/$filename"

  echo "🎬 Optimisation de $filename ..."
  ffmpeg -i "$file" -vcodec libx264 -crf 28 -preset veryfast -movflags +faststart "$output" -y

  echo "✅ Fichier optimisé : $output"
done
