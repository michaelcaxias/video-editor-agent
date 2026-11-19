Lições aprendidas em campo (cada item custou uma volta de retrabalho). Leia antes de montar ou renderizar.

## Processo
- **Olhe os quadros antes de decidir o layout.** O estilo (split, inset, cabeça recortada, legenda em 2 camadas) só aparece em folhas de contato com tempo (`scripts/contact_sheet.sh`, 2–3 qps em vídeo curto, ~1 qps em 40 s). Só transcrição e métricas deram uma v1 e uma v2 erradas.
- **Mostre o bruto também.** Antes de planejar, olhe o enquadramento do bruto (selfie fechada sem espaço acima da cabeça inviabilizou o formato "yap" com cartões sobre a pessoa).
- **Gere tudo por script** (`templates/gerador-split.py`): tempos saem das palavras reais, então um ajuste de roteiro é um rebuild de segundos. Mantenha a versão anterior do gerador (`build_v2.py`) para comparar.
- **Loop de trabalho:** gerar → `hyperframes check --json > work/check.out` → `scripts/check_summary.py` → `snapshot --at <tempos>` e ler a folha de contato → corrigir → `scripts/render_final.sh <nome>`. Depois de renderizar, olhe quadros do arquivo final (o snapshot não prova o render).
- **Não renderize sem o ok do storyboard**, e entregue sempre uma versão nova (v2, v3…) sem sobrescrever a anterior.
- Quando o usuário dá um **link de GitHub/skill/ferramenta**, leia o repositório antes (clone em scratchpad), diga o que tem de diferente e o que não vale trazer, e instale só em venv isolado.

## Gotchas de ferramenta
- **zsh:** `$M:l` é modificador (minúsculas) e engole o `:l` de `:linear=true`; `"$R[ocr]"` vira subscrito de variável. Em scripts use bash e `${M}` / `"${R}[ocr]"`. (`scripts/normalize_audio.sh` já faz certo.)
- **`hyperframes check ... | head`** mata o processo antes de salvar o relatório. Sempre `> arquivo` e leia com `scripts/check_summary.py`.
- **`faster-whisper` + `av` recente:** `decode_audio` quebra (`metadata_errors`). Passe um array numpy (WAV 16 kHz mono) em vez do caminho. Sem `libcublas`, caia para CPU (`scripts/transcribe.py` já faz).
- **Palavras que somem do mapa de tempos:** `aroll_words.json` não tem todo índice original (bordas de corte). Use um `T(i)` que procura a palavra vizinha.
- **Vídeo no HyperFrames:** reencode com keyframes a cada 1 s (`-g 60`), senão trava no seek. O A-roll vem em 60 fps do `cut_aroll.py`; o matte pode ficar em 30 fps (alinha por tempo).
- **Desenho animado em SVG:** esconder o traço com `stroke-dasharray:1; dashoffset:1` deixa um ponto (round cap). Use `dasharray:"1 2"` e `dashoffset:1.05`.
- **Texto sob elemento opaco:** frase do topo que aparece enquanto o rosto está em tela cheia dá `text_occluded` (erro). Pule frases que caem dentro de janelas de tela cheia.
- **Matte (`remove-background`):** precisa de `onnxruntime-node`; o instalador tenta CUDA e dá 404 → `npm i onnxruntime-node@1.21.1 --prefix ~/.cache/hyperframes/optional/onnxruntime-node@1.21.1 --onnxruntime-node-install-cuda=skip` (`scripts/matte.sh` faz). ~3 qps na CPU. Deixa auréola clara no cabelo e restos do fundo (poltrona): em cartão escuro, suavize as bordas com `mask-image` e prefira um fundo limpo na gravação.
- **Legenda "palavra por palavra" com layout estático** deixa a palavra visível fora do centro quando o par está incompleto. Mostre o grupo inteiro de uma vez, centralizado (como nas referências).
- **Filtros CSS em vídeo** não são permitidos pelo contrato; `mask-image` num `<video>` funcionou, mas confira no render.
- **Sons sintetizados:** pico bruto de ~−20 dBFS ficou alto demais depois da normalização (+8 dB). Use pico bruto ≈ −31 dBFS (RMS ≈ −57) para efeitos "discretos"; ≥ 3 sons juntos soam alto.
- **Zona segura:** os checks do HyperFrames cobrem todas as plataformas e são rígidos (topo ≥ ~270 px, direita ≤ ~845 px, base: legenda a partir de ~1090). Avisos de safe zone da linha-frase do topo são escolha de estilo; erros (`text_occluded`) não.
- **Render:** ~1 min para 53 s a 60 fps com GPU do Chrome; `nice -n 15`, `--workers 3`. O render final deve passar por `scripts/normalize_audio.sh` (áudio do bruto sai em −22 LUFS).

## Instagram / referências
- `yt-dlp` baixa Reels públicos sem login (1080×1920, com áudio). Stories/privados exigem cookies do navegador: só com pedido do usuário.
- Baixar para estudar o estilo é uma coisa; reutilizar o vídeo de outra pessoa na edição exige autorização e crédito.

## rea-video (ferramenta de medição)
- Instalar: `python3 -m venv .venv-rea && .venv-rea/bin/pip install "${R}[ocr]"` (R = caminho do clone). Funciona no Python 3.14. 1ª execução baixa ~220 MB de modelos.
- Sem VLM, o veredito "ai_video…" e a contagem de "text label" são ruído. Confiável: cortes/min, plano médio, BPM, nº de SFX, legendas com tempo (`packaging/subtitles.srt`), trilhas separadas (`stems/`).
- Ainda não aproveitado: `subtitles.srt/.ass` (tempo/estilo de legenda) e `stems/` (música) como insumo direto do gerador.
