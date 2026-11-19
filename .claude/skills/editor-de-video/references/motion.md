Motion graphics com HyperFrames: o piso de qualidade. Adaptado do `craft.md` e do `engines.md` da skill `motion-designer` (gabrielgreco1/skills, licença livre). Cada regra veio de uma versão reprovada. Quem manda no contrato de render é a skill `hyperframes` (leia primeiro); aqui ficam as regras de design e o fluxo com o nosso material.

Fluxo no HyperFrames.

1. Leia `/hyperframes` e `/hyperframes-cli`. Antes de construir à mão qualquer efeito nomeado (transição, scanlines, glitch, gráfico, legenda), procure no registro: `npx hyperframes catalog` / `add <bloco>` (`/hyperframes-registry`).
2. Projeto: `npx hyperframes init <pasta>`. Tamanho no `data-width`/`data-height` da raiz (1080×1920, 1080×1350, 1920×1080). Cada formato é composto nativo; nunca recortar nem preencher com fundo borrado.
3. Fontes fora da lista embutida precisam de `@font-face` apontando pra um arquivo em `assets/fonts/`; sem isso o `check` falha e o render cai numa fonte genérica.
4. Áudio como `<audio class="clip" data-start data-duration>`. As legendas vêm do `words.json` (`scripts/transcribe.py`) ou dos blocos de legenda do registro; transcrição e áudio em `/media-use`.
5. Confira: `npx hyperframes lint` / `inspect` e `snapshot --review` (leia os quadros). Render de rascunho antes do final; o usuário julga vídeo renderizado, não o preview.

História antes do visual.

- A trama se conta em uma frase por um estranho. Se não der, não anime ainda.
- Os 3 primeiros segundos dizem o que está em jogo e por quê. Slogan vago como gancho falha mesmo com visual lindo.
- Vídeo compartilhável não parece anúncio: a piada ou o formato lideram e o produto aparece como resposta.
- Termina dizendo o que o produto resolve + um CTA claro, dentro do mundo do vídeo.
- Com narração, o roteiro e a voz real vêm primeiro e mandam no desenho: tabela voz | imagem, voz final, e só então a folha de cortes, reveals e sons amarrados às palavras faladas. Precisa de mais tempo de imagem? Acrescente respiro no roteiro, não acelere a voz.

Legibilidade (o motivo nº 1 de reprovação).

- Um caminho de leitura por tela. Se o olho escolhe entre objeto, tela, fundo e legenda, está errado.
- Cada texto fica na tela ≥ palavras/3 + 1 s. Mais longo e claro vence curto e denso; um item por vez.
- Corte todo número, painel e rótulo que não serve à história.
- Corpo ≥ 34 px, rótulo mono ≥ 28 px, título ≥ 96 px (formatos de 1080 de largura). Números tabulares, alinhados, sem tremer.

Composição e encaixe.

- Nada sai do seu contêiner (card, moldura de celular, janela da câmera). Nada importante é cortado pela borda do quadro.
- Sem bonecos de palito nem humanos desenhados; represente pessoas por ações (cursor com nome, digitação, silhueta de costas).
- Três faixas por tela, sem sobreposição: título (HEAD) · hero visual (VIS) · legenda (CAP). Precisa de mais? Duas telas, não duas camadas.
- Legenda só na faixa dela; nunca sobre foto, objeto, gráfico ou título. Quando o título repete a fala, esconda a legenda.
- Rótulos posicionados a partir da caixa medida do título (≥ 24 px de folga), nunca num y fixo.
- Saídas terminam antes de a próxima entrada começar na mesma faixa.
- Câmera: push lento (1,00 → 1,04) em vez de elementos extras. Transições motivadas (whip, match cut, zoom em detalhe); nunca um quadro cinza/branco chapado entre cenas.

Áreas seguras (px da borda: topo · direita · base · esquerda).

| formato | margem |
|---|---|
| 9:16 Reels/TikTok/Shorts | 260 · 150 · 460 · 150 (caixa útil ≈ 780×1200, centrada) |
| 4:5 feed | 110 · 90 · 120 · 90 |
| 1:1 | 90 · 90 · 90 · 90 |
| 16:9 | 80 · 110 · 90 · 110 |

Só fundo e textura sangram. Em formato alto: centrado, empilhado, poucos elementos; corte conteúdo em vez de encolher.

Ritmo e acabamento "caro" (tempo, não efeito).

| o quê | tempo |
|---|---|
| entrada de card/painel/celular | 0,55 s, sobe 36–60 px, escala .94→1, leve overshoot |
| saída | 0,30 s, −18 px, sem overshoot |
| título | fade + 18 px por palavra, 0,5 s, 0,05 s entre palavras |
| mudança de seção | crossfade 0,45 s + 60 px |
| escurecer + borrar atrás de um print | 0,35–0,40 s, borrão 14 px, tinta 40 % |
| marca-texto num print | varre em 0,4 s na palavra falada |
| contadores | 0,5–0,8 s por passo, pulso 1,08 no pouso |
| cursor | mola, pressiona (escala .96, ~0,12 s) e a interface reage no mesmo quadro, com tique de som |

- Mola em forma fechada (função de t), nunca integrada quadro a quadro: o render por fatias quebra.
- Anime as bordas, não o retângulo: o indicador estica a borda da frente e depois a de trás.
- Contêiner primeiro, texto depois: o rótulo antigo some antes de a caixa crescer e o novo entra quando há espaço. Rótulos sobrepostos dentro de uma caixa que se transforma são o sinal nº 1 de animação de IA inacabada.
- Ritmo "calmo e cinematográfico" (movimento de câmera na duração da cena, entradas 0,5–0,8 s, exibir ≥ 1 s) ou "dinâmico" (entradas 0,3–0,4 s, whips no beat). Se o olho precisa perseguir o movimento, está rápido.
- Sem gradiente genérico de IA, sem brilho em excesso, cor contida, tipografia precisa.

Fidelidade e assets.

- UI, cores e fontes reais do produto, extraídas do site (`npx hyperframes capture <url>`); nunca aproximar. Parodiar outro meio (terminal, trailer, chat) é reestilizar no sistema da marca.
- Dados reais, verbatim, com a página de origem. Nunca inventar ranking, nota ou estatística. Respeite alegações proibidas da marca (confira com grep antes do render).
- Rótulo honesto: a legenda diz exatamente o que a imagem mostra.
- Ícones vetoriais soltos num quadro vazio foram reprovados ("cara de IA, sem gancho"). Gancho = lacuna de curiosidade + imagem real forte no quadro 0.
- Fontes de imagem: Wikimedia Commons, NASA/NIH, Poly Haven, ambientCG, Smithsonian 3D, Natural Earth. Evite NC, "uso editorial" em peça promocional e banco com marca d'água. Registre licença e autor; CC BY/BY-SA vão pros créditos do post.
- Foto em 9:16: card com a proporção própria da foto, largura segura cheia, sobre uma cópia escurecida e borrada dela; recorte rótulos de museu e marcas d'água.

Legendas (cada regra foi um bug visível).

- O layout do bloco é estático: todas as palavras já posicionadas quando ele aparece (as não faladas a 0 de opacidade); nunca recentralize nem adicione/remova palavra com o bloco na tela.
- Blocos de 1 linha, 2–4 palavras (ou até 6 / 30 caracteres no estilo de série), sem cruzar fim de frase, sem partir número falado; a última palavra fica ≥ 0,3 s; o bloco sai quando a próxima palavra falada começa.
- Estilo de série: branca, Inter 900, contorno preto ~7 px (`-webkit-text-stroke` + `paint-order: stroke fill`), sombra suave, sem caixa, sem mudar a cor da palavra nova.
- Carregue todos os pesos de fonte antes do início, ou o texto reflui no meio do vídeo.

Narração e som.

- Escreva pra voz: frases coloquiais e curtas, números e siglas como se fala, sem "…" nem vírgula no meio pra criar pausa (`narracao.md`).
- Cada efeito sonoro amarra a um evento visual (corte, pouso, toque, contagem). Master em −14 a −14,5 LUFS.
- Transcreva a voz gerada e compare com o roteiro antes de montar a imagem; um trecho pode ler a frase com sentido invertido.
- Renderize com educação: `nice -n 15`, poucos workers, apague quadros depois de codificar.

Mundo ilustrado para explicadores de processo ("como X funciona"): um mundo, um caminho (cano, estrada, cabo) que liga as estações, um objeto que viaja o vídeo todo mudando de estado, a câmera descendo o caminho com movimentos suavizados em vez de cortes secos, e um mapa recorrente dos passos. Invente o mundo para cada tema; não reutilize o de outro vídeo.
