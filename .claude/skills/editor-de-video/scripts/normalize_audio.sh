#!/bin/bash
# Normaliza o áudio de um MP4 para -14 LUFS / pico <= -1,5 dBTP em duas passadas, copiando o vídeo (sem reencodar).
# uso: normalize_audio.sh entrada.mp4 saida.mp4 [LUFS]
# (script em bash: no zsh, "$M:l" vira modificador e quebra o filtro; aqui usamos ${M})
set -euo pipefail
IN="$1"; OUT="$2"; I="${3:--14}"
J=$(ffmpeg -v info -i "$IN" -af "loudnorm=I=${I}:TP=-1.5:LRA=11:print_format=json" -f null - 2>&1)
M=$(printf '%s' "$J" | python3 -c "
import sys,json;t=sys.stdin.read();j=json.loads(t[t.rindex('{'):t.rindex('}')+1])
print(f\"measured_I={j['input_i']}:measured_TP={j['input_tp']}:measured_LRA={j['input_lra']}:measured_thresh={j['input_thresh']}:offset={j['target_offset']}\")")
ffmpeg -v error -y -i "$IN" -c:v copy -af "loudnorm=I=${I}:TP=-1.5:LRA=11:${M}:linear=true" -c:a aac -b:a 192k -ar 48000 "$OUT"
ffmpeg -v info -i "$OUT" -af loudnorm=print_format=summary -f null - 2>&1 | grep -E "Input (Integrated|True Peak)"
