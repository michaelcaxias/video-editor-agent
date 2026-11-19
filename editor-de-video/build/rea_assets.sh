#!/bin/bash
# Prepara os assets do vídeo "rea-video" (take_rea_01) para os dois projetos HyperFrames.
# uso (da pasta editor-de-video): bash build/rea_assets.sh
set -euo pipefail
R=referencias/rea-video
A=work/rea01/assets
mkdir -p "$A"
q() { ffmpeg -v error -y "$@"; }

# A-roll horizontal (2x do bruto) com keyframe a cada 1 s (seek do HyperFrames)
q -i work/rea01/source/aroll.mov -c:v libx264 -crf 16 -preset medium -g 60 -pix_fmt yuv420p -c:a aac -b:a 192k "$A/aroll.mp4"

# README do repositório (logo + descrição + selos), sem a nota sobre cripto
q -i "$R/Imagem colada (2).png" -vf "crop=967:300:0:40" "$A/readme.png"
q -i "$R/Imagem colada (2).png" -vf "crop=560:40:225:450" "$A/badges.png"

# Quadros das quebras plano a plano (sem a faixa de rótulo em chinês; o rótulo em PT é desenhado no HTML)
# grade: 6 colunas x 200 px; linha 1 y 0-355, linha 2 y 411-766
tile() { q -i "$1" -vf "crop=200:355:$(( $2 * 200 )):$(( $3 == 0 ? 0 : 411 ))" "$A/$4.jpg"; }
for c in 0 1 2 3 4 5; do tile "$R/thumb (1).jpg" $c 0 film_$c; tile "$R/thumb (1).jpg" $c 1 film_$((c + 6)); done
tile "$R/thumb.jpg" 1 0 ai_a      # #2 vídeo IA
tile "$R/thumb.jpg" 2 0 ai_b      # #3 vídeo IA
tile "$R/thumb.jpg" 3 1 code_a    # #10 render por código (GitHub)
tile "$R/thumb.jpg" 3 0 code_b    # #4 render por código

# Original x refeito (GIF -> MP4 com keyframes; rótulos chineses ficam fora do recorte)
q -i "$R/demo.gif" -vf "crop=218:352:1:38,scale=436:-2:flags=lanczos,fps=30" -c:v libx264 -crf 18 -g 30 -pix_fmt yuv420p -an "$A/demo_orig.mp4"
q -i "$R/demo.gif" -vf "crop=218:352:221:38,scale=436:-2:flags=lanczos,fps=30" -c:v libx264 -crf 18 -g 30 -pix_fmt yuv420p -an "$A/demo_ai.mp4"
q -i "$R/paper.gif" -vf "crop=258:122:1:24,scale=774:-2:flags=lanczos,fps=30" -c:v libx264 -crf 18 -g 30 -pix_fmt yuv420p -an "$A/paper_orig.mp4"
q -i "$R/paper.gif" -vf "crop=258:122:1:171,scale=774:-2:flags=lanczos,fps=30" -c:v libx264 -crf 18 -g 30 -pix_fmt yuv420p -an "$A/paper_remake.mp4"
q -i "$R/paper.gif" -vf "crop=258:122:261:171,scale=774:-2:flags=lanczos,fps=30" -c:v libx264 -crf 18 -g 30 -pix_fmt yuv420p -an "$A/paper_swap.mp4"
ls -la "$A"
