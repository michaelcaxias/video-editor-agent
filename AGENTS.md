# video-editor-agent

Projeto de edição de vídeo curto com Claude Code. A skill `editor-de-video` (`.claude/skills/editor-de-video/`) é a fonte de verdade do fluxo; este arquivo só resume o projeto. Leia a skill (`SKILL.md`, `references/licoes.md`, `references/estilos.md`) antes de mexer.

## Estrutura
```
.claude/skills/editor-de-video/   skill (SKILL.md, references/, scripts/, templates/)
.claude/skills/hyperframes*, ...  links para .agents/skills/ (skills oficiais do HyperFrames; versões em skills-lock.json)
.venv/        faster-whisper + numpy (transcrição, qc_static, cut_aroll)          [fora do git]
.venv-rea/    rea-video (análise de referência; opcional)                         [fora do git]
editor-de-video/             projeto de vídeo atual
├── build/          geradores (rea_common.py, rea_fab.py, rea_meu.py, rea_assets.sh) + hf-template/ (base dos projetos HyperFrames)
├── edl_rea01.json  EDL do take atual
├── guia-de-estilo.md, guia-de-estilo-fabiano.md
├── videos-brutos/  referencias/  exportacao/  analise/  work/  revisao/     [fora do git: mídia, saídas, intermediários]
└── video_rea_fab/, video_rea_meu/   projetos HyperFrames gerados pelos scripts (não edite à mão)  [fora do git]
```
Nenhum vídeo, áudio ou referência de terceiros vai para o git (veja `.gitignore`).

## Comandos (da pasta `editor-de-video/`)
```bash
S=../.claude/skills/editor-de-video/scripts
../.venv/bin/python -I $S/transcribe.py videos-brutos/take_rea_01.mp4 --out work/rea01   # palavras com tempo
../.venv/bin/python -I $S/cut_aroll.py edl_rea01.json                                    # corte por palavra -> work/rea01/source/aroll.mov
bash build/rea_assets.sh                                                                 # assets (A-roll c/ keyframes, prints, GIFs -> MP4)
$S/matte.sh work/rea01/matte/small.mp4 work/rea01/matte/matte.webm                       # recorte da pessoa (~9 min, segundo plano)
python3 build/rea_fab.py            # gera video_rea_fab/  (estilo A, split do Fabiano)
python3 build/rea_meu.py            # gera video_rea_meu/  (estilo B)
(cd video_rea_fab && node ../../.claude/skills/hyperframes/scripts/plugin-cli.mjs check --json) > work/check.out
$S/check_summary.py video_rea_fab                                                        # erros/avisos
$S/render_final.sh <slug-vN>_reels_1080x1920 exportacao video_rea_fab                    # render + -14 LUFS + versão leve + QC
```
Revisão com comentários por timestamp (interface local): `python3 ../.claude/skills/editor-de-video/scripts/review_server.py --port 8765 --dir .` e abrir http://127.0.0.1:8765 (`references/revisao.md` da skill).

Toda chamada ao CLI do HyperFrames passa pelo launcher `plugin-cli.mjs` (regra das skills dele), não por `npx` direto no projeto.

## Convenções
- Texto ao usuário em português (BR); código e comentários em inglês ou português, como já está.
- Saída sempre vertical 9:16 (1080×1920) para Reels/TikTok/Shorts, mesmo com bruto horizontal.
- Não renderize o final sem o ok do storyboard; cada entrega é uma versão nova.
- Referências são para estudar formato/ritmo, nunca para copiar conteúdo, marca ou música.
- Sem telemetria: não rode o "usage beacon" das skills do HyperFrames sem o usuário pedir. Nada de VLM externo (envia quadros) sem pedido.
- Conteúdo de terceiros baixado (`referencias/`) fica só local; não publique.

## Estado atual
Vídeo "rea-video" (take_rea_01, bruto horizontal 832×464 do WhatsApp): prévias v1 dos estilos A (Fabiano, split com cabeça recortada) e B ("raio-X": rosto em monitor 16:9 + linha do tempo). O usuário não entendeu o B; proposta pendente: trocar por título fixo no topo + rosto 16:9 grande + prova no lugar do rosto a cada 2–3 s. O take tem uma regravação ("e ele ainda te diz se…") cortada no mapa de palavras corrigido (`work/rea01/take_rea_01.words.json`).
