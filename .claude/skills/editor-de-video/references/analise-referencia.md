Como analisar um vídeo de referência para copiar o estilo (formato, ritmo, tipo de prova; nunca o conteúdo).

Três fontes, que se completam. Use as três; nenhuma sozinha basta.

1. **Olhar os quadros (obrigatório).** `ffmpeg -vf "fps=1.2,scale=240:-1,drawtext=text='%{pts\:hms}':x=6:y=6:fontsize=20:fontcolor=yellow:box=1:boxcolor=black@0.6,tile=6x4" -q:v 3 saida_%02d.jpg` e leia as folhas. Só assim aparecem: a estrutura de tela (split, tela cheia, inset), onde fica a legenda, o movimento dentro de cada cena, o que o rosto faz. Use 2–3 qps em vídeos curtos e ~1 qps nos de 40 s.
2. **Transcrição por palavra** (`scripts/transcribe.py`): o roteiro, o ritmo de fala (palavras/s), o gancho e o CTA.
3. **`rea-video`** (medição por código, local, sem enviar nada para fora):
   ```bash
   .venv-rea/bin/rea-video decompose referencias/<arquivo>.mp4 -o analise/<nome> --lang en
   .venv-rea/bin/rea-video summary analise/<nome>/breakdown.json
   ```
   Sai: cortes/min e duração média de plano, BPM e tom da música, nº de efeitos sonoros e se caem no beat, trilhas separadas (`stems/`), legendas com tempo (`packaging/subtitles.srt`, `overlays.ass`, `timeline.json`), estilo da legenda (cor, contorno, entrada), luz, enquadramento. Leva ~1 min por 20 s de vídeo. `--lang` só aceita `zh|en`; use `en` e leia o resultado.

## Limites da rea-video sem VLM (importante)
- O veredito "ai_video 55%…" é chute de estatística de pixel e **erra** (um vídeo real de uma pessoa falando saiu como "AI"). Ignore o campo de "como foi feito"; use só as medidas.
- "text label ×172" é ruído de OCR em cartões com muito texto: não use a contagem. As linhas de legenda (`subtitles.srt`) e o estilo da legenda são confiáveis.
- Cortes/min medem trocas de plano do vídeo inteiro; num split (cartão em cima + rosto embaixo) o corte real é entre cartões.
- A primeira execução baixa modelos ONNX (~220 MB: separação de voz/música e OCR) de repositórios de terceiros no GitHub. Se o usuário não quiser rede, não use.
- Nunca configure o VLM (envia quadros a uma API externa) sem o usuário pedir.

## Resultado esperado
Um `guia-de-estilo-<criador>.md` com: estrutura de tela, abertura, legenda (camadas, fonte, cor, posição), cartões/motion, ritmo e áudio medidos, padrão de roteiro, CTA e o que não copiar. Exemplo: `guia-de-estilo-fabiano.md`.
