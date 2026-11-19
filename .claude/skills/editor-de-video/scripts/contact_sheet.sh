#!/bin/bash
# Folhas de contato com tempo, para estudar um vídeo quadro a quadro.
# uso: contact_sheet.sh video.mp4 saida_prefixo [qps=2] [colunas=6] [linhas=4] [largura=240]
set -euo pipefail
V="$1"; P="$2"; FPS="${3:-2}"; C="${4:-6}"; R="${5:-4}"; W="${6:-240}"
ffmpeg -v error -y -i "$V" -vf "fps=${FPS},scale=${W}:-1,drawtext=text='%{pts\:hms}':x=6:y=6:fontsize=20:fontcolor=yellow:box=1:boxcolor=black@0.6,tile=${C}x${R}" -q:v 3 "${P}_%02d.jpg"
ls "${P}"_*.jpg
