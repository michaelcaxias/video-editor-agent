#!/usr/bin/env python3
"""Resume o último relatório do `hyperframes check` (video/.hyperframes/artifacts/checks/*.json).
uso: check_summary.py [pasta-do-projeto-hyperframes=video] [--all]
Mostra contagem por código e lista os erros (e, com --all, todos os avisos de layout).
Dica: rode o check com a saída para um arquivo (`check --json > check.out`): um `| head` mata o processo antes de salvar o relatório."""
import collections, glob, json, os, sys
proj = next((a for a in sys.argv[1:] if not a.startswith('--')), 'video')
files = glob.glob(f'{proj}/.hyperframes/artifacts/checks/*.json')
if not files:
    sys.exit('nenhum relatório de check encontrado')
r = json.load(open(max(files, key=os.path.getmtime)))
f = []
def walk(o):
    if isinstance(o, dict):
        if 'code' in o and 'severity' in o: f.append(o)
        for v in o.values(): walk(v)
    elif isinstance(o, list):
        for v in o: walk(v)
walk(r)
print(dict(collections.Counter((x['severity'], x['code']) for x in f)))
show_all = '--all' in sys.argv
seen = set()
for x in f:
    if x['severity'] == 'error' or (show_all and x['code'] not in ('line_unread',)):
        k = (x['code'], x.get('selector'))
        if k in seen: continue
        seen.add(k)
        print(f"{x['severity']:7} {x['code']:28} {str(x.get('selector'))[:34]:34} | {x['message'][:110]}")
