#!/bin/bash
# Render final: HyperFrames (60 fps, baixa prioridade) -> áudio -14 LUFS -> versão leve -> QC de tela parada.
# uso (da raiz do projeto de vídeo, pasta com video/): render_final.sh <slug-versao> [pasta-saida=exportacao] [projeto-hyperframes=video]
# ex.: render_final.sh edicao-teste-v4_shorts_1080x1920
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
L="$HERE/../../hyperframes/scripts/plugin-cli.mjs"
NAME="$1"; OUT="${2:-exportacao}"; PROJ="${3:-video}"; mkdir -p work "$OUT"
df -h "$HOME" | tail -1
( cd "$PROJ" && nice -n 15 node "$L" render --fps 60 --quality looks --workers 3 -o ../work/render_raw.mp4 ) > work/render.out 2>&1 || { tail -20 work/render.out; exit 1; }
grep -E "MB ·" work/render.out | cut -c1-100
"$HERE/normalize_audio.sh" work/render_raw.mp4 "$OUT/$NAME.mp4"
ffmpeg -v error -y -i "$OUT/$NAME.mp4" -c:v libx264 -crf 24 -preset medium -c:a aac -b:a 128k "$OUT/${NAME}_upload.mp4"
ffprobe -v error -show_entries stream=codec_name,width,height,r_frame_rate -show_entries format=duration -of csv=p=0 "$OUT/$NAME.mp4"
PY=".venv/bin/python"; [ -x "$PY" ] || PY="../.venv/bin/python"; [ -x "$PY" ] || PY=python3
"$PY" -I "$HERE/qc_static.py" "$OUT/$NAME.mp4" 2>&1 | grep -v Warn || true
ls -la "$OUT/$NAME.mp4" "$OUT/${NAME}_upload.mp4"
