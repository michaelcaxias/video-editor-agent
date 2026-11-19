#!/bin/bash
# Confere as ferramentas do editor-de-video (Linux). Rode da raiz do projeto.
ok(){ printf "  ok     %s\n" "$1"; }; no(){ printf "  FALTA  %s  →  %s\n" "$1" "$2"; }
command -v ffmpeg >/dev/null && ok ffmpeg || no ffmpeg "sudo dnf install ffmpeg"
command -v yt-dlp >/dev/null && ok yt-dlp || no yt-dlp "sudo dnf install yt-dlp"
node -v 2>/dev/null | grep -qE '^v(2[2-9]|[3-9])' && ok "node $(node -v)" || no "node >= 22" "nvm install 24"
PY=.venv/bin/python; [ -x "$PY" ] || PY=python3
$PY -c "import faster_whisper" 2>/dev/null && ok faster-whisper || no faster-whisper "python3 -m venv .venv && .venv/bin/pip install faster-whisper numpy"
$PY -c "import numpy" 2>/dev/null && ok numpy || no numpy ".venv/bin/pip install numpy"
(npx --no-install hyperframes --version >/dev/null 2>&1 || ls .claude/skills/hyperframes >/dev/null 2>&1) && ok hyperframes || no hyperframes "npx skills add heygen-com/hyperframes --all"
$PY -c "import playwright" 2>/dev/null && ok playwright || echo "  opcional playwright (prints/gravação de tela): .venv/bin/pip install playwright && .venv/bin/python -m playwright install chromium"
[ -x .venv-rea/bin/rea-video ] && ok rea-video || echo "  opcional rea-video (análise de referência): python3 -m venv .venv-rea && .venv-rea/bin/pip install \"\${CLONE}[ocr]\"  (CLONE = clone de github.com/JuneYaooo/rea-video)"
[ -d "$HOME/.cache/hyperframes/optional/onnxruntime-node@1.21.1/node_modules/onnxruntime-node" ] && ok "onnxruntime-node (matte)" || echo "  opcional matte: rode scripts/matte.sh uma vez (instala onnxruntime-node sem CUDA)"
