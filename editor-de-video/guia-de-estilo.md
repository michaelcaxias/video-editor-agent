# Guia de estilo (v0, a partir de 2 referências)

Referências: `referencias/ref_01_final.mp4` (33,2 s, edição de produto/GitHub, rosto + cartões) e `referencias/ref_02_tutorial.mp4` (58,9 s, rosto + infográficos desenhados). Formato 9:16. Medido por código (ffmpeg scene score > 0,25) e lido em folha de contato.

## Ritmo
| | ref_01 | ref_02 | Meta para o nosso |
|---|---|---|---|
| cortes | 16 em 33 s (~1 a cada 2 s) | 9 em 59 s (~1 a cada 6 s; o resto é movimento dentro do cartão) | rosto ↔ cartão a cada 2–4 s; movimento dentro de cartões longos |
| abertura | cartão com prova no quadro 0 ("o código", repositório); rosto entra em ~1,4 s | rosto + título, depois cartões | começar na 1ª palavra; cartão de prova/título até ~1,5–3 s |
| alternância | rosto → cartão em tela cheia (fundo claro) → rosto | rosto → infográfico → rosto | igual: cartão cobre a tela inteira, nunca por cima do rosto |

## Cartões (motion)
- Fundo cinza muito claro/bege, tela cheia (1080×1920), conteúdo centralizado.
- ref_01: prints reais com borda azul, contador de estrelas 43.535 → 75.304 (número se mexendo), cartão de interface "Simulando", rede de agentes.
- ref_02: desenho à mão (traço preto grosso, sublinhado coral, anotações manuscritas coral), cada elemento entra na palavra falada; ícone coral do Claude; setas desenhadas.
- Um elemento novo a cada ~0,5–1 s dentro do cartão; fade/slide suave entre cartões; elementos antigos desbotam antes dos novos.

## Legenda
- Palavra por palavra, 1–2 palavras por vez, posição no peito (rosto) ou no pé do cartão.
- ref_01: branca, negrito, **caixa cinza arredondada translúcida** atrás; destaque em itálico serifado para a frase do CTA ("código da legenda").
- ref_02: texto simples abaixo do cartão.
- **Decisão pendente:** a skill recomenda branca com contorno preto e sem caixa; a referência usa caixa cinza. Proposta: seguir a referência (a skill diz que a estrutura da referência manda).

## Cor e tipografia
- Neutros claros nos cartões, coral/laranja do Claude (#D97757-ish) como acento, preto grosso nos desenhos, azul claro nas bordas de print (ref_01).
- Sans geométrica pesada para títulos/legenda; manuscrita coral para anotações; serifa itálica para destaque de CTA.

## Áudio
- ref_01: voz a −14,4 LUFS, pico −2,0 dBTP. O nosso bruto está a −22,6 LUFS: +8 dB de ganho, com limitador, para chegar a −14 LUFS / pico ≤ −1 dBTP.
- Sem música de fundo audível; sons curtos de transição só nas viradas (decisão pendente).

## Gancho e CTA
- ref_01: afirma o fato com número ("73 mil estrelas") e entrega a prova na tela já no começo; CTA final por DM, com palavra-chave em itálico serifado e em destaque.
- Aplicação aqui: o gancho do take afirma ("todo mundo tá editando com o Claude, mas ninguém te ensina como"); a prova é o diagrama passo a passo.

## O que NÃO copiar
- Conteúdo, textos, prints e marca do MiroFish; a gravação de piscina; a música/áudio; o rosto do outro criador.

## Limitações desta v0
- Estudei contact sheets (1 quadro a cada 2 s) e cortes por score; não medi duração por cartão nem fontes exatas. Refino quando você aprovar a direção.

---

# Atualização v1 (análise quadro a quadro, 3 qps na ref_01 e 2 qps na ref_02)

## ref_02 (tutorial, lousa desenhada)
- **Abertura:** colagem de miniaturas de vídeo "caindo" com o ícone do Claude no centro; na palavra "como" desenha um círculo coral em volta do ícone e escreve "como?" à mão. O rosto só entra em ~3 s.
- **Cada passo é uma lousa cumulativa.** Título pequeno ("passo N") + nome do passo com sublinhado coral. Elementos aparecem desenhados e se acumulam: laptop → seta curva → pasta (o nome é digitado letra a letra) → linhas de árvore → subpastas, cada um na palavra falada.
- **Ferramentas:** 4 caixas tracejadas começam vazias, com "grátis" manuscrito em coral. Cada uma vira ícone + nome + nota manuscrita ("motion", "cortes", "legendas", "baixar") na palavra falada, com seta até o ícone do Claude.
- **Estilo:** fan de celulares, corações rabiscados, setas convergindo no Claude e um cartão "guia de estilo" que se preenche linha a linha.
- **Edição:** faixa de 5 quadros de storyboard, círculo à mão no quadro 1, balão de feedback, celular com "play".
- **Transições:** blur com esticamento (~0,3 s) entre cartões. O rosto entra em cartão arredondado com margem e abre até a tela cheia.
- **Legenda:** 1 palavra por vez, pequena, sem contorno (preto sobre cartão claro), na faixa inferior.
- **CTA:** campo de comentário sobre o rosto com "EDIT" digitado, e logo abaixo o cartão da resposta automática ("te enviou...").

## ref_01 (produto, split)
- Três layouts alternados a cada 1–2 s: **split** (cartão no topo, rosto embaixo, legenda na junção), **cartão em tela cheia** (fundo claro radial, legenda abaixo) e **rosto** com zooms.
- Prints reais com borda azul brilhante, contador subindo (9.026 → 75.304), cursor e emojis animados: sempre há movimento dentro do cartão.
- Legenda: caixa cinza arredondada translúcida, 1–2 palavras; destaque em serifa itálica no CTA.

## Decisões na v2 (feitas)
- Legenda: **branca com contorno preto** (escolha sua), mas agora de **1–2 palavras** por vez.
- Lousa desenhada à mão (traço com tremida, animação de desenho, fonte manuscrita Caveat), colagem de abertura, transições com blur, rosto "abrindo" a cada volta, CTA com campo de comentário e resposta.
- Sons: pico bruto −31 dBFS (RMS −57), bem abaixo da voz.

## Ainda não replicado
- Layout split (cartão em cima / rosto embaixo) da ref_01.
- Prints reais com contador subindo e cursor.
- Pan/zoom de câmera dentro da lousa.
- Cartão de CTA sobre o rosto (hoje é um cartão em tela cheia).
