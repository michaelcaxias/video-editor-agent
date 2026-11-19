#!/bin/bash
# Recorta o fundo de um vídeo (WebM com alpha) usando o remove-background do HyperFrames.
# uso (da raiz do projeto): .claude/skills/editor-de-video/scripts/matte.sh entrada.mp4 saida.webm
# Notas: CPU ~2-3 qps (53 s a 30 fps ~ 9-13 min); rode em segundo plano com nice. O modelo (u2net_human_seg) baixa na 1ª vez.
# Se o npm falhar com "Failed to download the binaries: 404", é o instalador tentando CUDA: o script já usa o skip.
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
L="$HERE/../../hyperframes/scripts/plugin-cli.mjs"
PFX="$HOME/.cache/hyperframes/optional/onnxruntime-node@1.21.1"
if [ ! -d "$PFX/node_modules/onnxruntime-node" ]; then
  (cd "$HOME" && npm install onnxruntime-node@1.21.1 --prefix "$PFX" --onnxruntime-node-install-cuda=skip)
fi
nice -n 15 node "$L" remove-background "$1" -o "$2" --quality best
