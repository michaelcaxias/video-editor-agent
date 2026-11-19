Revisão com comentários por timestamp (interface local, nada sai da máquina).

## Subir
Da raiz do projeto de vídeo (a pasta com `exportacao/`):
```bash
python3 ../.claude/skills/editor-de-video/scripts/review_server.py --port 8765 --dir .   # segundo plano
# abra http://127.0.0.1:8765   (?v=exportacao/<arquivo>.mp4 abre uma versão específica)
```
Só escuta em 127.0.0.1 e só serve arquivos dentro da pasta. Lista os `.mp4` de `exportacao/` e de `work/` (por padrão abre o `_upload.mp4` mais novo). Para parar: encerre o processo (não use `pkill -f` com o nome do script na mesma linha de comando).

## Uso (usuário)
`Espaço` play/pausa · `←`/`→` 1 quadro (`Shift` = 1 s) · `C` comentar neste ponto (pausa e preenche o tempo) · `L` repetir o trecho (início–fim) · `Ctrl+Enter` salva. Cada comentário tem início, fim opcional, tipo (corte, legenda, cartão/motion, rosto/recorte, som, roteiro, cor/estilo) e texto. Clique no tempo da lista para ir ao ponto. "ok" marca como resolvido. "Copiar lista" gera markdown.

## Uso (Claude)
Os comentários ficam em `revisao/comentarios_<arquivo>.json`: lista de `{id, t0, t1, kind, text, done}`. Leia o arquivo, **agrupe por cena/tipo**, aplique no gerador (`build_*.py`) e rebuilde; depois renderize uma versão nova (nunca sobrescreva) e marque os resolvidos. Antes de editar, repita ao usuário os comentários que entendeu e o que vai mudar em cada um. Ambiguidade (ex.: "está feio") → pergunte.

## Outras opções (se quiser mais)
- **Preview editável do projeto HyperFrames:** `hyperframes preview --background` (Studio no navegador, edita as tags e vê ao vivo; não tem comentários por tempo). Pare com `preview --stop`.
- **Artefato hospedado** (página com comentários compartilhados): o vídeo sairia da máquina para o claude.ai; só com autorização explícita do usuário e com um rascunho leve.
