#!/bin/bash

OUT_DIR="./assets/videos/optimized"

for file in "$SRC_DIR"/*.mp4; do
  [ -e "$file" ] || continue

  filename=$(basename "$file")
  temp_file="${file%.mp4}_tmp.mp4"

  echo "🎬 Optimization of $filename ..."
  ffmpeg -i "$file" -vcodec libx264 -crf 28 -preset veryfast -movflags +faststart "$temp_file" -y

  mv "$temp_file" "$file"

  echo "✅ Optimized file : $file"
done
