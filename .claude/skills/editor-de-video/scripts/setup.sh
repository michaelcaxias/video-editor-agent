#!/bin/sh
# Uso: setup.sh [diretório-base]
base="${1:-.}/editor-de-video"
mkdir -p "$base/videos-brutos" "$base/referencias" "$base/exportacao"
echo "Criado: $base"
