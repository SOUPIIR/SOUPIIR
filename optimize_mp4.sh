#!/bin/bash

OUT_DIR="./assets/videos/optimized"

for file in "$SRC_DIR"/*.mp4; do
  [ -e "$file" ] || continue

  filename=$(basename "$file")
  temp_file="${file%.mp4}_tmp.mp4"

  echo "🎬 Optimisation de $filename ..."
  ffmpeg -i "$file" -vcodec libx264 -crf 28 -preset veryfast -movflags +faststart "$temp_file" -y

  mv "$temp_file" "$file"

  echo "✅ Fichier optimisé : $file"
done
