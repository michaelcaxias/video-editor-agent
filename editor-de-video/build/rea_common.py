"""Peças comuns aos dois estilos do vídeo "rea-video" (take_rea_01): palavras, legenda, sons, projeto HyperFrames.

Rode os geradores (build/rea_fab.py, build/rea_meu.py) da pasta editor-de-video.
"""
import json, math, os, shutil, wave
import numpy as np

SRC = 'work/rea01/source'
ASSETS = 'work/rea01/assets'
DUR = 24.046
ORANGE, CORAL, INK, CREAM = '#E8541B', '#D9573B', '#161412', '#EFEAE0'
GREEN, MAGENTA = '#2E9E4F', '#C23BD4'

W = json.load(open(f'{SRC}/words_final.json'))
FIX = {51: 'você.', 52: 'Depois', 61: 'é a vez', 72: 'EDIT,', 84: 'Direct.'}
for i, t in FIX.items():
    W[i]['w'] = t
for i, w in enumerate(W):
    w['i'] = i
    if i + 1 < len(W):  # o medium encurta o fim; estende até a próxima palavra (máx. +0,25 s)
        w['e'] = round(min(W[i + 1]['s'], max(w['e'], w['s'] + 0.12) + 0.25), 3)


def T(i, k='s'):
    return W[i][k]


# --- legenda falada: 1–2 palavras, grupo inteiro centralizado, branca com contorno preto --------------------------------
def captions(proj, top, size=70):
    groups, cur = [], []
    for w in W:
        if cur:
            gap = w['s'] - cur[-1]['e']
            if cur[-1]['w'][-1] in '.?!,' or gap >= 0.25 or len(cur) >= 2 or len(' '.join(x['w'] for x in cur + [w])) > 15:
                groups.append(cur); cur = []
        cur.append(w)
    groups.append(cur)
    html, js = [], []
    for g, grp in enumerate(groups):
        nxt = groups[g + 1][0]['s'] if g + 1 < len(groups) else DUR
        start = max(grp[0]['s'] - 0.02, 0.0)
        end = min(max(grp[-1]['e'], grp[-1]['s'] + 0.3) + 0.04, nxt - 0.01, DUR - 0.01)
        txt = ' '.join(w['w'].rstrip(',.') if n == len(grp) - 1 else w['w'] for n, w in enumerate(grp))
        html.append(f'<div id="cg{g}" class="clip cg" data-start="{start:.3f}" data-duration="{end - start:.3f}">{txt}</div>')
        js.append(f'tl.fromTo("#cg{g}",{{opacity:0,y:10,scale:.94}},{{opacity:1,y:0,scale:1,duration:0.12,ease:"power2.out"}},{start:.3f});')
        js.append(f'tl.set("#cg{g}",{{opacity:0}},{end - 0.001:.3f});')
    open(f'{proj}/compositions/captions.html', 'w').write(f'''<template>
<style>
#root {{ position:absolute; inset:0; }}
.cg {{ position:absolute; left:0; right:0; top:{top}px; text-align:center; white-space:nowrap;
  font-family:'Inter',sans-serif; font-weight:900; font-size:{size}px; line-height:1.1; color:#fff;
  -webkit-text-stroke:7px #000; paint-order:stroke fill; text-shadow:0 4px 14px rgba(0,0,0,.35); }}
</style>
<div id="root" data-composition-id="captions" data-width="1080" data-height="1920">
{chr(10).join(html)}
</div>
<script>
const tl = gsap.timeline({{ paused: true }});
{chr(10).join(js)}
window.__timelines["captions"] = tl;
</script>
</template>
''')
    return groups


# --- sons discretos (sintetizados; pico bruto ≈ −31 dBFS, ver licoes.md) ------------------------------------------------
SR = 48000
rng = np.random.default_rng(7)


def _env(n, a, d):
    t = np.arange(n) / SR
    return np.minimum(t / a, 1) * np.exp(-t / d)


def _whoosh():
    n = int(.4 * SR); x = rng.standard_normal(n); y = np.zeros(n)
    for k in range(1, n):
        y[k] = y[k - 1] + (.02 + .16 * math.sin(math.pi * k / n)) * (x[k] - y[k - 1])
    y *= np.sin(math.pi * np.arange(n) / n) ** 2
    return y / np.abs(y).max() * 0.028


def _pop():
    n = int(.1 * SR); t = np.arange(n) / SR
    return np.sin(2 * math.pi * np.cumsum(480 - 1200 * t) / SR) * _env(n, .003, .028) * 0.020


def _tick():
    n = int(.03 * SR); t = np.arange(n) / SR
    return np.sin(2 * math.pi * 1900 * t) * _env(n, .001, .007) * 0.012


def _ding():
    n = int(.6 * SR); t = np.arange(n) / SR
    return (np.sin(2 * math.pi * 1318 * t) + .3 * np.sin(2 * math.pi * 2636 * t)) * _env(n, .004, .16) * 0.018


def write_sfx(proj, events):
    snd = dict(whoosh=_whoosh(), pop=_pop(), tick=_tick(), ding=_ding())
    out = np.zeros(int((DUR + 1) * SR))
    for t, kind in events:
        if t < 0:
            continue
        s = snd[kind]; i = int(t * SR)
        out[i:i + len(s)] += s[:len(out) - i]
    with wave.open(f'{proj}/assets/sfx.wav', 'wb') as f:
        f.setnchannels(1); f.setsampwidth(2); f.setframerate(SR)
        f.writeframes((np.clip(out, -.9, .9) * 32767).astype(np.int16).tobytes())


def waveform(n=160):
    """RMS da voz em n barras (0–1), do wav 16 kHz do A-roll."""
    w = wave.open('work/rea01/chk/aroll16.wav')
    a = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(float)
    k = len(a) // n
    r = np.sqrt((a[:k * n].reshape(n, k) ** 2).mean(1))
    return (r / r.max()).round(3).tolist()


# --- projeto HyperFrames -------------------------------------------------------------------------------------------
def new_project(proj, assets):
    os.makedirs(f'{proj}/compositions', exist_ok=True)
    os.makedirs(f'{proj}/assets', exist_ok=True)
    for f in ('hyperframes.json', 'package.json'):
        shutil.copy(f'build/hf-template/{f}', f'{proj}/{f}')
    json.dump(dict(id=os.path.basename(proj), name=os.path.basename(proj), createdAt='2026-11-19T03:40:00.000Z'),
              open(f'{proj}/meta.json', 'w'))
    for src, dst in assets:
        if not os.path.exists(f'{proj}/assets/{dst}') or os.path.getmtime(src) > os.path.getmtime(f'{proj}/assets/{dst}'):
            os.makedirs(os.path.dirname(f'{proj}/assets/{dst}'), exist_ok=True)
            shutil.copy(src, f'{proj}/assets/{dst}')


def host(cid, start, dur, track, z):
    return (f'<div id="{cid}" data-composition-id="{cid}" data-composition-src="compositions/{cid}.html" '
            f'data-start="{start:.3f}" data-duration="{dur:.3f}" data-track-index="{track}" data-track-kind="graphics" '
            f'data-width="1080" data-height="1920" style="z-index:{z}"></div>')
