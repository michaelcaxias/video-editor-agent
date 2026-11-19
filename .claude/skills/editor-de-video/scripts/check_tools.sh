#!/bin/sh
for t in ffmpeg yt-dlp node npx; do
  if command -v "$t" >/dev/null 2>&1; then echo "ok      $t"; else echo "FALTA   $t"; fi
done
python3 -c "import faster_whisper" 2>/dev/null && echo "ok      faster-whisper" || echo "FALTA   faster-whisper (use um venv)"
