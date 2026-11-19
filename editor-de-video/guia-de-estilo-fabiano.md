# Estilo "Fabiano" (5 Reels, 21–135 s, 1080×1920 @ 30 fps)

Fontes: `referencias/ref_fabiano_*.mp4`. Estudo visual quadro a quadro (1,2–2 qps com tempo) + `rea-video` (cortes, BPM, SFX, legendas) + transcrição por palavra. Tudo abaixo foi visto nos quadros; o que for hipótese está marcado.

## 1. Estrutura de tela: SPLIT quase o tempo todo
- **Topo ≈ 0–60%: "área de cartão"** em fundo creme (~#F4EFE6) com a ilustração da cena.
- **Rodapé ≈ 64–100%: rosto** (estúdio escuro, microfone, óculos de lente laranja), em corte horizontal, sempre visível.
- **A legenda principal fica na junção** (~55–60% da altura), logo acima do rosto.
- Rosto em **tela cheia** só em 2–3 momentos curtos (~1–1,5 s cada): virada ("tudo / pra você"), e o CTA final. Aí a legenda vira branca e vai para o peito.
- Diferença-chave para o meu v2: **o rosto nunca some**. No meu v2, os cartões cobrem a tela inteira e o rosto aparece só ~26% do tempo.

## 2. Abertura (0–4 s): título-promessa + visual real
- Linha de título pequena e escura ("O app que você paga todo mês") + **caixa laranja arredondada com texto em serifa itálica branca** ("tem versão grátis", "fazer jogo completo", "foi feito, plano por plano").
- Embaixo, o visual real do assunto (UI do produto, repositório, capturas de jogo).
- Pode entrar um carimbo sobre a UI ("PROIBIDA") e um pulso radial laranja.
- A fala já começa na palavra 0 (voz começa em 0,0–0,2 s).

## 3. Legenda em duas camadas
1. **Linha-frase no topo do cartão** (sans pequena, ~34 px, escura): a frase vai se construindo com a fala; palavras ainda não ditas ficam cinza-claro. A **palavra-chave da frase** aparece embaixo da linha em **serifa itálica grande** com **sublinhado laranja** ("alternativa grátis", "refazer", "código da legenda").
2. **Legenda falada embaixo** (na junção): sans **negrito preta**, 1–3 palavras por vez, trocando a cada ~0,3–0,5 s. Em tela cheia de rosto: branca, negrito, no peito.
- Fontes (hipótese): sans geométrica pesada (tipo Inter/SF) e serifa itálica elegante (tipo Instrument Serif/Playfair Italic).

## 4. Cartões / motion
- Fundo creme com pontilhado leve; **cartões de UI escuros** (#161616) com acento laranja (~#E8541B), sombra suave, cantos arredondados.
- **Linha laranja de "pipeline"** à esquerda, com bolinha, ligando uma cena à seguinte; pulso radial laranja atrás do elemento em foco.
- Muito movimento por cena: cursor clicando, itens sendo selecionados (borda laranja), número gigante em serifa laranja ("77") com grade de blocos atrás, mostrador "menos de 60", gráfico com anotação ("aqui as pessoas pulam"), diagrama hub-and-spoke ("seu produto" no centro), logos de ferramentas, linhas de código/terminal, miniaturas de rede social.
- Transições: slide horizontal + blur curto; zoom-in/out dentro da cena.
- **Mudança de cena a cada ~1–2,5 s**, sempre amarrada à frase falada; nada fica parado > 3 s.

## 5. Ritmo e áudio (medido pela rea-video em `DfnSx`, 21 s)
- 4 planos detectados, 8,5 cortes/min (o corte real é entre cartões, dentro do split).
- Voz + música **83,4 BPM (dó maior)**, 15 efeitos sonoros (todos amarrados à entrada de texto: "SFX hits on: text label in ×14").
- Câmera do rosto: plano médio fechado 88%, push-in lento.
- Fala: ~4 palavras/s, voz limpa e firme, sem música alta.

## 6. Roteiro (padrão repetido nos 4 vídeos)
1. **Gancho = promessa concreta** nos primeiros 2–3 s: "O Claude agora consegue fazer jogos completos…", "O app que você paga todo mês tem versão grátis", "Esse novo repositório permite você fazer a engenharia reversa de qualquer vídeo…".
2. **Credencial/novidade logo em seguida** ("Alguém no GitHub acabou de criar…").
3. **Entrega em passos concretos**, com número ("77 skills", "menos de 60 segundos", "Primeiro passo… Segundo passo…").
4. **CTA padrão** no último ~5 s, em tela cheia de rosto: "Comenta [palavra/código da legenda] que eu te mando o link e o guia completo no Direct."
- Duração típica: 40–45 s (um de 21 s e um de 2 min 15 s).

## 7. O que NÃO copiar
Conteúdo, textos, repositórios e prints dos Reels; a identidade visual exata (logo, rosto, cenário); a música.

## Medidas por vídeo (rea-video)
| Reel | Duração | Cortes/min | Plano médio | Música | Efeitos sonoros |
|---|---|---|---|---|---|
| DfnSx (engenharia reversa de vídeo) | 21 s | 8,5 | 5,3 s | 83,4 BPM, dó maior | 15 |
| DfnMG (apps pagos x grátis) | 41 s | 13,1 | 4,1 s | não detectada | 28 |
| DfpVm, DfpcRG, Dfnnj | (análise em andamento / ver `analise/`) | | | | |
