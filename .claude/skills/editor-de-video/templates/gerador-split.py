#!/usr/bin/env python3
"""EXEMPLO de gerador (copie e adapte): monta um projeto HyperFrames split (cartão em cima, rosto recortado embaixo) a partir de
work/source/aroll_words.json. Os índices de palavra (T(13), PHRASES, cenas) são do take de teste: troque pelos do seu vídeo.
Veja references/licoes.md e references/estilos.md. Original: editor-de-video/build/build_v3.py.

Topo: área de cartão creme com a linha-frase (palavra-chave em serifa itálica) + banner laranja + cena desenhada.
Base: rosto em cartão escuro arredondado; a cabeça recortada (matte) "vaza" por cima da borda do cartão.
Rosto em tela cheia só em janelas curtas (virada e pitch). Legenda branca com contorno (escolha do usuário).
uso: python build/build_v3.py   (rode da pasta editor-de-video; precisa de video/assets/matte.webm)
"""
import json, math, wave
import numpy as np

W = json.load(open('work/source/aroll_words.json'))
BY = {w['i']: w for w in W}
DUR = 53.133
CORAL, ORANGE, INK, BG = '#D9573B', '#E8541B', '#161412', '#EFEAE0'
rng = np.random.default_rng(11)

FIX = {7: 'Claude,', 37: 'Claude', 71: 'Claude', 117: 'Claude', 153: 'Claude', 48: 'com', 50: 'subpastas',
       91: 'ffmpeg', 93: 'os', 94: 'cortes', 96: 'Whisper', 205: 'PV.'}
MERGE = {85: ('HyperFrames,', 86), 103: ('yt-dlp', 104)}
SKIP = {86, 104}


def T(i, k='s'):
    for d in (0, 1, -1, 2, -2, 3, -3, 4, -4):  # palavra vizinha se o índice caiu num corte
        if i + d in BY:
            return BY[i + d][k]
    raise KeyError(i)


# --- janelas de rosto em tela cheia (resto do tempo: split) -----------------------------------------------------
FULL = [(T(111), T(125) - 0.06), (T(163, 'e') + 0.1, T(197) - 0.1)]


def in_full(t):
    return any(a <= t < b for a, b in FULL)


# --- palavras (com grafias corrigidas) -----------------------------------------------------------------------------
words = []
for w in W:
    i = w['i']
    if i in SKIP:
        continue
    t, s, e = FIX.get(i, w['w']), w['s'], w['e']
    if i in MERGE:
        t, j = MERGE[i]; e = BY[j]['e'] if j in BY else e
    words.append(dict(i=i, t=t, s=s, e=e))

# --- legenda falada: 1–2 palavras por vez --------------------------------------------------------------------------
groups, cur = [], []
for w in words:
    if cur:
        gap = w['s'] - cur[-1]['e']
        if cur[-1]['t'][-1] in '.?!,' or gap >= 0.25 or len(cur) >= 2 or len(' '.join(x['t'] for x in cur + [w])) > 16:
            groups.append(cur); cur = []
    cur.append(w)
if cur:
    groups.append(cur)
cap_html, cap_js = [], []
for g, grp in enumerate(groups):
    nxt = groups[g + 1][0]['s'] if g + 1 < len(groups) else DUR
    start = max(grp[0]['s'] - 0.02, 0.1)
    end = min(max(grp[-1]['e'], grp[-1]['s'] + 0.3) + 0.04, nxt - 0.01, DUR - 0.01)
    spans = ''.join(f'<span id="cw{g}_{n}" class="cw">{w["t"]}</span> ' for n, w in enumerate(grp))
    cap_html.append(f'<div id="cg{g}" class="clip cg" data-start="{start:.3f}" data-duration="{end - start:.3f}">{spans.strip()}</div>')
    base = 70 if in_full(start) else 0
    cap_js.append(f'tl.fromTo("#cg{g}",{{opacity:0,y:{base + 10}}},{{opacity:1,y:{base},duration:0.12,ease:"power2.out"}},{start:.3f});')
    cap_js.append(f'tl.set("#cg{g}",{{opacity:0}},{end - 0.001:.3f});')
open('video/compositions/captions.html', 'w').write(f'''<template>
<style>
#root {{ position:absolute; inset:0; }}
.cg {{ position:absolute; left:0; right:0; top:1088px; text-align:center; white-space:nowrap; overflow:visible;
  font-family:'Inter',sans-serif; font-weight:900; font-size:70px; line-height:1.1; color:#fff;
  -webkit-text-stroke:7px #000; paint-order:stroke fill; text-shadow:0 4px 14px rgba(0,0,0,.4); }}
.cw {{ display:inline-block; }}
</style>
<div id="root" data-composition-id="captions" data-width="1080" data-height="1920">
{chr(10).join(cap_html)}
</div>
<script>
const tl = gsap.timeline({{ paused: true }});
{chr(10).join(cap_js)}
window.__timelines["captions"] = tl;
</script>
</template>
''')

# --- linha-frase do topo (estilo do Fabiano): frase que se constrói + palavra-chave em serifa itálica ----------------
# (primeiro_índice, último_índice, palavra-chave ou None) em índices originais do take
PHRASES = [
    (0, 7, None), (8, 12, 'como'), (13, 18, 'tutorial completo'), (19, 21, 'passo a passo'), (22, 29, 'fluxo de edição'),
    (30, 32, 'configuração'), (33, 39, 'desktop'), (40, 47, 'pasta'), (48, 51, 'subpastas'), (52, 56, 'exportação'),
    (57, 60, 'ferramentas'), (61, 68, 'gratuitas'), (69, 74, 'pica'), (75, 81, None), (82, 89, 'HyperFrames'),
    (90, 94, 'cortes'), (95, 101, 'legendas'), (102, 110, 'baixar'), (111, 116, None), (117, 124, 'poderoso'),
    (125, 127, 'estilo'), (128, 137, 'bom gosto'), (138, 144, 'vídeos'), (145, 149, 'criadores'), (150, 157, 'estudar'),
    (158, 163, 'montar'), (180, 184, None), (185, 195, 'gratuito'), (196, 205, 'comenta'),
]
cap2_html, cap2_js = [], []
for p, (a, b, kw) in enumerate(PHRASES):
    ws = [w for w in words if a <= w['i'] <= b]
    if not ws:
        continue
    t0 = max(ws[0]['s'] - 0.05, 0.05)
    nxt = None
    for q in PHRASES[p + 1:]:
        nw = [w for w in words if q[0] <= w['i'] <= q[1]]
        if nw:
            nxt = nw[0]['s'] - 0.05; break
    t1 = min((nxt if nxt else DUR) - 0.02, DUR - 0.02)
    if t1 - t0 < 0.3 or any(t0 >= fa - .1 and t1 <= fb + .6 for fa, fb in FULL):
        continue  # frase que cairia debaixo do rosto em tela cheia
    chars = len(' '.join(w['t'] for w in ws))
    fs = max(28, min(38, int(760 / (chars * .56))))
    spans = ''.join(f'<span id="p{p}w{n}" class="pw">{w["t"]}</span> ' for n, w in enumerate(ws))
    kwhtml = ''
    if kw:
        kwhtml = f'<div id="p{p}k" class="kw">{kw}</div><svg class="ku" viewBox="0 0 1080 60"><path id="p{p}u" d="M0 0" /></svg>'
    cap2_html.append(f'<div id="ph{p}" class="clip ph" data-start="{t0:.3f}" data-duration="{t1 - t0:.3f}"><div class="ln" style="font-size:{fs}px">{spans.strip()}</div>{kwhtml}</div>')
    cap2_js.append(f'tl.fromTo("#ph{p}",{{opacity:0,y:14}},{{opacity:1,y:0,duration:.22,ease:"power2.out"}},{t0:.3f});')
    for n, w in enumerate(ws):
        cap2_js.append(f'tl.to("#p{p}w{n}",{{color:"#161412",duration:.12}},{w["s"]:.3f});')
    if kw:
        kws = kw.split()
        kwi = [w for w in ws if w['t'].strip(',.?!').lower() == kws[0].lower()]
        kt = (kwi[0]['s'] if kwi else ws[-1]['s'])
        cap2_js.append(f'tl.fromTo("#p{p}k",{{opacity:0,y:18,scale:.92}},{{opacity:1,y:0,scale:1,duration:.4,ease:"back.out(1.4)"}},{kt:.3f});')
        uw = max(150, len(kw) * 27)
        cap2_js.append(f'tl.fromTo("#p{p}u",{{attr:{{d:"M540 0 L540 0"}}}},{{attr:{{d:"M{540 - uw // 2} 0 Q540 -6 {540 + uw // 2} 0"}},duration:.35,ease:"power2.out"}},{kt + .12:.3f});')
    cap2_js.append(f'tl.to("#ph{p}",{{opacity:0,duration:.14}},{t1 - .14:.3f});')
open('video/compositions/cap2.html', 'w').write(f'''<template>
<style>
#root {{ position:absolute; inset:0; font-family:'Inter',sans-serif; }}
.ph {{ position:absolute; left:0; right:0; top:252px; text-align:center; opacity:0; }}
.ln {{ font-weight:700; white-space:nowrap; letter-spacing:-.01em; }}
.pw {{ color:#8d867a; }}
.kw {{ margin-top:6px; font-family:'EB Garamond',serif; font-style:italic; font-weight:500; font-size:66px; line-height:1.05; color:#161412; }}
.ku {{ position:absolute; left:-0px; top:122px; width:1080px; height:60px; overflow:visible; }}
.ku path {{ fill:none; stroke:{ORANGE}; stroke-width:6; stroke-linecap:round; }}
</style>
<div id="root" data-composition-id="cap2" data-width="1080" data-height="1920">
{chr(10).join(cap2_html)}
</div>
<script>
const tl = gsap.timeline({{ paused: true }});
{chr(10).join(cap2_js)}
window.__timelines["cap2"] = tl;
</script>
</template>
''')

# --- ferramentas de desenho ---------------------------------------------------------------------------------------
sfx = []  # (tempo, tipo)


def jit(v=2.2):
    return float(rng.uniform(-v, v))


def rr(x, y, w, h, r=18):
    p = [(x + r + jit(), y + jit()), (x + w - r + jit(), y + jit()), (x + w + jit(), y + r + jit()),
         (x + w + jit(), y + h - r + jit()), (x + w - r + jit(), y + h + jit()), (x + r + jit(), y + h + jit()),
         (x + jit(), y + h - r + jit()), (x + jit(), y + r + jit())]
    return (f'M{p[0][0]:.1f} {p[0][1]:.1f} L{p[1][0]:.1f} {p[1][1]:.1f} Q{x + w:.1f} {y:.1f} {p[2][0]:.1f} {p[2][1]:.1f} '
            f'L{p[3][0]:.1f} {p[3][1]:.1f} Q{x + w:.1f} {y + h:.1f} {p[4][0]:.1f} {p[4][1]:.1f} L{p[5][0]:.1f} {p[5][1]:.1f} '
            f'Q{x:.1f} {y + h:.1f} {p[6][0]:.1f} {p[6][1]:.1f} L{p[7][0]:.1f} {p[7][1]:.1f} Q{x:.1f} {y:.1f} {p[0][0]:.1f} {p[0][1]:.1f}')


def stroke(pid, d, w=7, color=INK, fill='none', extra=''):
    return (f'<path id="{pid}" d="{d}" pathLength="1" fill="{fill}" stroke="{color}" stroke-width="{w}" stroke-linecap="round" '
            f'stroke-linejoin="round" style="stroke-dasharray:1 2;stroke-dashoffset:1.05" filter="url(#rf)" {extra}/>')


def arrow(pid, x1, y1, qx, qy, x2, y2, color=INK, w=6):
    a = math.atan2(y2 - qy, x2 - qx); h = 22
    d = (f'M{x1} {y1} Q{qx} {qy} {x2} {y2} M{x2 - h * math.cos(a - .5):.1f} {y2 - h * math.sin(a - .5):.1f} L{x2} {y2} '
         f'L{x2 - h * math.cos(a + .5):.1f} {y2 - h * math.sin(a + .5):.1f}')
    return stroke(pid, d, w, color)


def folder(x, y, w, h):
    t = w * .36
    return (f'M{x + jit()} {y + h} L{x + jit()} {y + 18} Q{x} {y} {x + 18} {y} L{x + t:.1f} {y} L{x + t + 22:.1f} {y + 20} '
            f'L{x + w - 18} {y + 20} Q{x + w} {y + 20} {x + w} {y + 38} L{x + w} {y + h} Z')


STAR = (f'<svg viewBox="0 0 100 100" width="100%" height="100%"><rect width="100" height="100" rx="24" fill="{CORAL}"/>'
        + ''.join(f'<line x1="50" y1="50" x2="{50 + 30 * math.cos(a * math.pi / 4):.1f}" y2="{50 + 30 * math.sin(a * math.pi / 4):.1f}" '
                  f'stroke="#fff" stroke-width="7" stroke-linecap="round"/>' for a in range(8)) + '</svg>')
HEART = 'M0 -6 C-14 -22 -34 -2 0 24 C34 -2 14 -22 0 -6'


def heart(pid, x, y, sc):
    return stroke(pid, HEART, 5, CORAL, extra=f'transform="translate({x} {y}) scale({sc})"')


COMMON = f'''
@font-face {{ font-family:'Caveat'; font-weight:700; src:url('assets/fonts/caveat-700.woff2') format('woff2'); }}
#root {{ position:absolute; inset:0; font-family:'Inter',sans-serif; color:{INK}; }}
#wrap {{ position:absolute; inset:0; overflow:hidden; }}
#inner {{ position:absolute; left:58px; right:-58px; top:-30px; bottom:30px; }}
#sv {{ position:absolute; inset:0; width:1080px; height:1920px; overflow:visible; }}
.banner {{ position:absolute; left:0; right:0; text-align:center; }}
.banner span {{ display:inline-block; background:{ORANGE}; color:#fff; font-family:'EB Garamond',serif; font-style:italic; font-weight:500;
  font-size:62px; padding:6px 36px 12px; border-radius:22px; box-shadow:0 10px 24px rgba(232,84,27,.34); }}
.hand {{ position:absolute; font-family:'Caveat',cursive; font-weight:700; color:{CORAL}; white-space:nowrap; }}
.txt {{ position:absolute; font-weight:700; white-space:nowrap; }}
.ico {{ position:absolute; filter:drop-shadow(0 8px 12px rgba(0,0,0,.28)); }}
'''


def scene(cid, start, end, body, svg, anim, banner=None, push=False):
    dur = end - start
    bn = ''
    if banner:
        bn = f'<div class="banner" id="{cid}bn" style="top:392px"><span>{banner[0]}</span></div>'
        anim = f'P("#{cid}bn",{banner[1]:.3f});' + anim
    open(f'video/compositions/{cid}.html', 'w').write(f'''<template>
<style>{COMMON}
</style>
<div id="root" data-composition-id="{cid}" data-width="1080" data-height="1920">
<div id="wrap">
{bn}
<div id="inner">
<svg id="sv" viewBox="0 0 1080 1920"><defs><filter id="rf" x="-5%" y="-5%" width="110%" height="110%"><feTurbulence type="fractalNoise" baseFrequency="0.035" numOctaves="2" seed="4" result="n"/><feDisplacementMap in="SourceGraphic" in2="n" scale="3.5"/></filter></defs>
{svg}
</svg>
{body}
</div>
</div>
</div>
<script>
const tl = gsap.timeline({{ paused: true }});
const S = {start:.3f};
const P = (sel, t, d) => tl.fromTo(sel, {{ opacity: 0, y: 36, scale: .9 }}, {{ opacity: 1, y: 0, scale: 1, duration: d || .45, ease: "back.out(1.5)" }}, t - S);
const D = (sel, t, d) => tl.fromTo(sel, {{ strokeDashoffset: 1.05 }}, {{ strokeDashoffset: 0, duration: d || .55, ease: "power1.inOut" }}, t - S);
const F = (sel, t, d) => tl.fromTo(sel, {{ opacity: 0 }}, {{ opacity: 1, duration: d || .3, ease: "power2.out" }}, t - S);
tl.fromTo("#wrap", {{ opacity: 0, filter: "blur(14px)", x: 60 }}, {{ opacity: 1, filter: "blur(0px)", x: 0, duration: 0.26, ease: "power2.out" }}, 0);
{'tl.fromTo("#inner",{ scale: 1 },{ scale: 1.05, duration: ' + f'{dur:.2f}' + ', ease: "none" }, 0);' if push else ''}
{anim}
tl.to("#wrap", {{ opacity: 0, filter: "blur(14px)", x: -60, duration: 0.22, ease: "power2.in" }}, {dur - 0.24:.3f});
window.__timelines["{cid}"] = tl;
</script>
</template>
''')
    sfx.append((start - 0.04, 'whoosh'))
    return dict(id=cid, start=start, dur=dur)


scenes = []

# H · abertura: banner-promessa + colagem de vídeos + Claude circulado
s, e = 0.0, T(19) - 0.06
grads = [('#2a2f3a', '#5a2d2d'), ('#ffffff', '#e7e2d8'), ('#133b2f', '#0c1a16'), ('#c8542a', '#7a2a12'), ('#3d2a5c', '#1b1230'),
         ('#e9a8c8', '#c0568f'), ('#1f2a44', '#0f1524'), ('#f0d9a8', '#c79b4a'), ('#16423c', '#0b2420'), ('#b7d3f2', '#5d8fd0'),
         ('#2c2c2c', '#111111'), ('#f3c9b8', '#d9795a')]
body, anim = '', ''
cols, rows = [225, 482, 740], [690, 950]
for k in range(6):
    cx, cy = cols[k % 3] + jit(12), rows[k // 3] + jit(12)
    rot = float(rng.uniform(-8, 8)); g1, g2 = grads[k * 2]
    ink = '#1b1b1b' if (k * 2) in (1, 7, 9, 11) else '#ffffff'
    body += (f'<div id="h1c{k}" style="position:absolute;left:{cx - 95:.0f}px;top:{cy - 130:.0f}px;width:190px;height:260px;border-radius:22px;'
             f'background:linear-gradient(160deg,{g1},{g2});box-shadow:0 14px 28px rgba(0,0,0,.28);border:3px solid rgba(255,255,255,.5);overflow:hidden">'
             f'<div style="position:absolute;left:16px;top:20px;width:{90 + (k * 17) % 50}px;height:13px;border-radius:7px;background:{ink};opacity:.85"></div>'
             f'<div style="position:absolute;left:16px;top:44px;width:{60 + (k * 23) % 70}px;height:13px;border-radius:7px;background:{ink};opacity:.55"></div>'
             f'<div style="position:absolute;left:57px;top:118px;width:76px;height:76px;border-radius:38px;background:{ink};opacity:.25"></div></div>')
    anim += (f'tl.fromTo("#h1c{k}",{{y:{30 + (k * 13) % 40},rotation:{rot + 8:.1f},scale:1.1}},{{y:0,rotation:{rot:.1f},scale:1,duration:.7,ease:"power3.out"}},{0.04 * k:.2f});'
             f'tl.to("#h1c{k}",{{opacity:.3,duration:.35}},{T(11) - s:.3f});')
body += f'<div class="ico" id="h1i" style="left:392px;top:720px;width:180px;height:180px;border-radius:44px;border:7px solid #fff;overflow:hidden">{STAR}</div>'
body += '<div class="hand" id="h1q" style="left:545px;top:860px;font-size:100px">como?</div>'
svg = stroke('h1o', 'M482 600 C 600 590 650 700 640 810 C 630 920 540 960 470 960 C 360 960 300 880 310 800 C 320 700 390 610 520 612', 8, CORAL)
anim += (f'tl.fromTo("#h1i",{{scale:.7}},{{scale:1,duration:.5,ease:"back.out(1.6)"}},.15);'
         f'D("#h1o",{T(12):.3f},.5);tl.fromTo("#h1q",{{opacity:0,rotation:14,scale:.8}},{{opacity:1,rotation:8,scale:1,duration:.4,ease:"back.out(1.6)"}},{T(12) + .1 - s:.3f});')
scenes.append(scene('h1', s, e, body, svg, anim, banner=('ninguém te ensina como', 0.2), push=True))
sfx.pop()  # sem whoosh no quadro 0

# D · passo a passo: 3 caixas ligadas por setas
s, e = T(19), T(30) - 0.06
body, svg, anim = '', '', ''
boxes = [(1, 'configuração', 130, 560, T(19) + .2), (2, 'ferramentas', 520, 560, T(24)), (3, 'estilo', 130, 820, T(27))]
for n, lab, x, y, tt in boxes:
    svg += stroke(f'd1b{n}', rr(x, y, 330, 190, 24), 7)
    body += (f'<div class="txt" id="d1n{n}" style="left:{x + 40}px;top:{y + 28}px;font-size:84px;font-weight:900">{n}</div>'
             f'<div class="txt" id="d1l{n}" style="left:{x + 40}px;top:{y + 128}px;font-size:34px">{lab}</div>')
    anim += f'D("#d1b{n}",{tt:.3f},.5);P("#d1n{n}",{tt + .15:.3f},.35);F("#d1l{n}",{tt + .25:.3f});'
svg += arrow('d1a1', 470, 640, 495, 625, 515, 640) + arrow('d1a2', 640, 760, 600, 860, 470, 880)
anim += f'D("#d1a1",{T(24) + .3:.3f},.35);D("#d1a2",{T(27) + .05:.3f},.5);'
sfx += [(T(24), 'pop'), (T(27), 'pop')]
scenes.append(scene('d1', s, e, body, svg, anim, banner=('tutorial passo a passo', s + .05)))

# P · passo 1: laptop → pasta (digitada) → subpastas
s, e = T(30), T(57) - 0.06
body, svg, anim = '', '', ''
svg += stroke('p1s', rr(332, 540, 300, 150, 16), 7) + stroke('p1b', 'M292 706 L672 706 L650 726 L314 726 Z', 7)
svg += stroke('p1dl', 'M700 540 L700 580 M684 565 L700 582 L716 565 M682 600 L720 600', 5)
body += f'<div class="ico" id="p1i" style="left:437px;top:575px;width:90px;height:90px">{STAR}</div>'
anim += f'D("#p1s",{T(33):.3f},.5);D("#p1b",{T(33) + .3:.3f},.4);D("#p1dl",{T(34):.3f},.4);P("#p1i",{T(36):.3f},.4);'
svg += arrow('p1a', 610, 710, 690, 780, 640, 810) + stroke('p1f', folder(252, 790, 460, 150), 7)
body += '<div class="txt" id="p1ft" style="left:252px;width:460px;text-align:center;top:848px;font-size:38px"></div>'
anim += f'D("#p1a",{T(41):.3f},.4);D("#p1f",{T(41) + .2:.3f},.5);'
label = 'Editor de Vídeo'
t0, t1 = T(45), T(47, 'e')
for n in range(1, len(label) + 1):
    ta = t0 + (t1 - t0) * n / len(label)
    anim += f'tl.set("#p1ft",{{textContent:"{label[:n]}"}},{ta:.3f}-S);'
svg += stroke('p1t', 'M482 940 L482 968 M282 968 L682 968 M282 968 L282 990 M482 968 L482 990 M682 968 L682 990', 6)
anim += f'D("#p1t",{T(48):.3f},.5);'
for n, (lab, cx, wi) in enumerate([('vídeos brutos', 282, 52), ('referências', 482, 54), ('exportação', 682, 56)]):
    svg += stroke(f'p1sf{n}', folder(cx - 65, 990, 130, 78), 6)
    body += f'<div class="txt" id="p1sl{n}" style="left:{cx - 100}px;width:200px;text-align:center;top:1080px;font-size:28px">{lab}</div>'
    anim += f'D("#p1sf{n}",{T(wi):.3f},.35);P("#p1sl{n}",{T(wi) + .1:.3f},.3);'
    sfx.append((T(wi), 'pop'))
for ta in np.linspace(t0, t1, 8):
    sfx.append((float(ta), 'tick'))
scenes.append(scene('p1', s, e, body, svg, anim, banner=('passo 1 · configuração', s + .05)))

# C · passo 2: ferramentas (4 caixas "grátis" que se especializam)
s, e = T(57), T(111) - 0.06
body, svg, anim = '', '', ''
body += f'<div class="ico" id="c3i" style="left:427px;top:690px;width:110px;height:110px">{STAR}</div>'
anim += f'P("#c3i",{T(60):.3f});'
bx = [(120, 520), (490, 520), (120, 880), (490, 880)]
tools = [('HyperFrames', 'motion', T(85), 'M12 38 L30 18 L50 30 M10 40 a4 4 0 1 0 0.1 0 M30 16 a4 4 0 1 0 0.1 0 M52 30 a4 4 0 1 0 0.1 0'),
         ('ffmpeg', 'cortes', T(91), 'M10 10 L46 46 M46 10 L10 46 M14 8 a7 7 0 1 0 0.1 0 M14 44 a7 7 0 1 0 0.1 0'),
         ('Whisper', 'legendas', T(96), 'M8 28 V28 M16 18 V38 M24 8 V48 M32 16 V40 M40 22 V34 M48 26 V30'),
         ('yt-dlp', 'baixar', T(103), 'M28 8 V36 M16 26 L28 38 L40 26 M10 48 H46')]
arrs = [('c3a0', 470, 640, 470, 690, 440, 720), ('c3a1', 600, 640, 600, 690, 540, 725),
        ('c3a2', 470, 880, 470, 830, 440, 800), ('c3a3', 600, 880, 600, 830, 540, 795)]
tg = T(66)
for n, ((x, y), (nm, lab, tt, ic)) in enumerate(zip(bx, tools)):
    svg += (f'<path id="c3b{n}" d="{rr(x, y, 350, 140, 22)}" fill="none" stroke="{INK}" stroke-width="6" stroke-dasharray="14 12" '
            f'stroke-linecap="round" filter="url(#rf)" style="opacity:0"/>')
    svg += (f'<g id="c3k{n}" transform="translate({x + 26} {y + 36}) scale(1.05)" style="opacity:0"><path d="{ic}" fill="none" stroke="{INK}" '
            f'stroke-width="4.5" stroke-linecap="round" stroke-linejoin="round"/></g>')
    body += (f'<div class="hand" id="c3g{n}" style="left:{x}px;width:350px;text-align:center;top:{y + 34}px;font-size:60px">grátis</div>'
             f'<div class="txt" id="c3n{n}" style="left:{x + 100}px;top:{y + 22}px;font-size:36px;opacity:0">{nm}</div>'
             f'<div class="hand" id="c3l{n}" style="left:{x + 100}px;top:{y + 66}px;font-size:56px;opacity:0">{lab}</div>')
    ax = arrs[n]
    svg += arrow(ax[0], ax[1], ax[2], ax[3], ax[4], ax[5], ax[6], INK, 5)
    anim += (f'F("#c3b{n}",{tg + n * .12:.3f});F("#c3g{n}",{tg + .1 + n * .12:.3f});'
             f'tl.to("#c3g{n}",{{opacity:0,duration:.2}},{tt - s:.3f});P("#c3n{n}",{tt + .05:.3f},.35);P("#c3l{n}",{tt + .2:.3f},.35);F("#c3k{n}",{tt:.3f});'
             f'D("#{ax[0]}",{tt + .1:.3f},.4);')
    sfx.append((tt, 'pop'))
scenes.append(scene('c3', s, e, body, svg, anim, banner=('passo 2 · ferramentas', s + .05)))

# E · passo 3: estilo (bom gosto + celulares)
s, e = T(125), T(150) - 0.06
body, svg, anim = '', '', ''
body += '<div class="hand" id="e1a" style="left:590px;top:486px;font-size:78px">bom gosto</div>'
svg += heart('e1h', 805, 560, 1.0)
anim += (f'tl.fromTo("#e1a",{{opacity:0,rotation:-14,scale:.8}},{{opacity:1,rotation:-6,scale:1,duration:.45,ease:"back.out(1.6)"}},{T(134) - s:.3f});'
         f'D("#e1h",{T(135) + .2:.3f},.5);')
pos = [(217, 590), (407, 590), (597, 590), (312, 870), (502, 870)]
for n, (x, y) in enumerate(pos):
    g1, g2 = grads[[0, 2, 4, 6, 8][n]]
    body += (f'<div id="e1v{n}" style="position:absolute;left:{x}px;top:{y}px;width:150px;height:250px;border-radius:22px;border:5px solid {INK};'
             f'background:linear-gradient(160deg,{g1},{g2});box-shadow:0 12px 22px rgba(0,0,0,.25);overflow:hidden">'
             f'<div style="position:absolute;left:14px;top:16px;width:80px;height:12px;border-radius:6px;background:#fff;opacity:.8"></div>'
             f'<div style="position:absolute;left:14px;top:38px;width:54px;height:12px;border-radius:6px;background:#fff;opacity:.5"></div>'
             f'<div style="position:absolute;left:55px;top:100px;width:0;height:0;border-left:42px solid #fff;border-top:26px solid transparent;border-bottom:26px solid transparent;opacity:.85"></div></div>')
    tt = T(141) + n * 0.16
    anim += (f'tl.fromTo("#e1v{n}",{{opacity:0,y:60,rotation:{(-1) ** n * 7},scale:.8}},'
             f'{{opacity:1,y:0,rotation:{(-1) ** n * 2},scale:1,duration:.5,ease:"back.out(1.5)"}},{tt - s:.3f});')
    sfx.append((tt, 'pop'))
for n, (hx, hy) in enumerate([(160, 660), (860, 730), (130, 990), (850, 1010)]):
    svg += heart(f'e1x{n}', hx, hy, .8)
    anim += f'D("#e1x{n}",{T(146) + n * .35:.3f},.4);'
scenes.append(scene('e1', s, e, body, svg, anim, banner=('passo 3 · estilo', s + .05)))

# G · guia de estilo: celulares → Claude → documento
s, e = T(150), T(163, 'e') + 0.1
body = f'<div class="ico" id="g1i" style="left:427px;top:690px;width:110px;height:110px">{STAR}</div>'
svg = ''
anim = f'P("#g1i",{s + .3:.3f});'
for n in range(5):
    x = 130 + n * 130; g1, g2 = grads[[0, 2, 4, 6, 8][n]]
    body += (f'<div id="g1v{n}" style="position:absolute;left:{x}px;top:400px;width:100px;height:170px;border-radius:16px;border:4px solid {INK};'
             f'background:linear-gradient(160deg,{g1},{g2});box-shadow:0 8px 16px rgba(0,0,0,.2)"></div>')
    anim += f'P("#g1v{n}",{s + n * .1:.3f},.35);'
    cx = x + 50
    svg += arrow(f'g1a{n}', cx, 585, cx + (482 - cx) * .15, 650, 482 + (cx - 482) * .35, 685, INK, 4)
    anim += f'D("#g1a{n}",{T(154) + n * .18:.3f},.4);'
svg += arrow('g1d', 482, 810, 482, 840, 482, 870, INK, 5)
anim += f'D("#g1d",{T(160):.3f},.4);'
body += ('<div id="g1c" style="position:absolute;left:130px;top:890px;width:700px;height:200px;border-radius:18px;background:#fbf9f4;'
         'box-shadow:0 14px 30px rgba(0,0,0,.18)"><div class="txt" style="left:34px;top:16px;font-size:34px;font-weight:900">guia de estilo</div>')
for n, (k, v) in enumerate([('legenda', '1–2 palavras por vez'), ('fonte', 'Inter 900'), ('cortes', 'a cada 2–3 s'), ('cor', 'coral + bege')]):
    body += (f'<div class="txt" id="g1k{n}" style="left:34px;top:{66 + n * 31}px;font-size:28px;color:#8a8378;opacity:0">{k}</div>'
             f'<div class="txt" id="g1y{n}" style="left:190px;top:{66 + n * 31}px;font-size:28px;opacity:0">{v}</div>')
    anim += f'F("#g1k{n}",{T(160) + .35 + n * .22:.3f},.25);F("#g1y{n}",{T(160) + .45 + n * .22:.3f},.25);'
    sfx.append((T(160) + .4 + n * .22, 'tick'))
body += '</div>'
anim += f'P("#g1c",{T(160):.3f});'
scenes.append(scene('g1', s, e, body, svg, anim))

# K · CTA: comentário "EDIT" + DM com a skill
s, e = T(197) - 0.1, DUR
body = (f'<div id="k1c" style="position:absolute;left:100px;top:540px;width:740px;height:210px;border-radius:26px;background:#fff;box-shadow:0 16px 34px rgba(0,0,0,.16)">'
        f'<div style="position:absolute;left:30px;top:30px;width:70px;height:70px;border-radius:35px;background:{CORAL}"></div>'
        f'<div class="txt" style="left:118px;top:42px;font-size:34px;color:#555">Você</div>'
        f'<div style="position:absolute;left:30px;top:120px;width:680px;height:72px;border-radius:36px;background:#f1f1f1">'
        f'<div class="txt" id="k1p" style="left:34px;top:18px;font-size:32px;color:#999;font-weight:700">Adicione um comentário…</div>'
        f'<div class="txt" id="k1x" style="left:34px;top:12px;font-size:44px;font-weight:900;letter-spacing:.05em"></div>'
        f'<div style="position:absolute;right:14px;top:10px;width:52px;height:52px;border-radius:26px;background:{INK};color:#fff;font-size:28px;line-height:52px;text-align:center" id="k1s">➤</div></div></div>'
        f'<div id="k1d" style="position:absolute;left:100px;top:790px;width:740px;height:170px;border-radius:26px;background:#fff;box-shadow:0 16px 34px rgba(0,0,0,.16)">'
        f'<div style="position:absolute;left:30px;top:34px;width:84px;height:84px;border-radius:20px;overflow:hidden">{STAR}</div>'
        f'<div class="txt" style="left:136px;top:34px;font-size:34px;font-weight:900">Claude</div>'
        f'<div class="txt" style="left:136px;top:84px;font-size:30px;color:#555">te enviou a skill completa</div></div>')
anim = f'P("#k1c",{s + .1:.3f});'
t0 = T(197) + 0.15
for n in range(4):
    ta = t0 + n * 0.2
    anim += f'tl.set("#k1x",{{textContent:"{"EDIT"[:n + 1]}"}},{ta:.3f}-S);' + (f'tl.set("#k1p",{{opacity:0}},{ta:.3f}-S);' if n == 0 else '')
    sfx.append((ta, 'tick'))
tsend = max(T(203), t0 + 0.9)
anim += f'tl.to("#k1s",{{scale:.85,duration:.1,yoyo:true,repeat:1}},{tsend:.3f}-S);P("#k1d",{tsend + .25:.3f});'
sfx += [(tsend, 'tick'), (tsend + .25, 'ding')]
scenes.append(scene('k1', s, e, body, '', anim))

# --- sons discretos (sintetizados, muito baixos) ---------------------------------------------------------------
SR = 48000


def env(n, a, d):
    t = np.arange(n) / SR
    return np.minimum(t / a, 1) * np.exp(-t / d)


def whoosh():
    n = int(.4 * SR); x = rng.standard_normal(n); y = np.zeros(n)
    for k in range(1, n):
        c = .02 + .16 * math.sin(math.pi * k / n)
        y[k] = y[k - 1] + c * (x[k] - y[k - 1])
    y *= np.sin(math.pi * np.arange(n) / n) ** 2
    return y / np.abs(y).max() * 0.028


def pop():
    n = int(.1 * SR); t = np.arange(n) / SR
    return np.sin(2 * math.pi * np.cumsum(480 - 1200 * t) / SR) * env(n, .003, .028) * 0.020


def tick():
    n = int(.03 * SR); t = np.arange(n) / SR
    return np.sin(2 * math.pi * 1900 * t) * env(n, .001, .007) * 0.012


def ding():
    n = int(.6 * SR); t = np.arange(n) / SR
    return (np.sin(2 * math.pi * 1318 * t) + .3 * np.sin(2 * math.pi * 2636 * t)) * env(n, .004, .16) * 0.018


# --- rosto: cartão escuro + pessoa recortada; tela cheia nas janelas FULL -------------------------------------------
S_BOX, HEAD_TOP_SRC, POP_TOP = 0.52, 330, 1176  # escala da pessoa no cartão; topo do cabelo na fonte; onde o cabelo fica na tela
CX = 540 - 540 * S_BOX
CY = POP_TOP - HEAD_TOP_SRC * S_BOX
BOX_IN = 'inset(1240px 36px 0px 36px round 44px)'
BOX_FULL = 'inset(0px 0px 0px 0px round 0px)'
face_js = f'gsap.set("#cut",{{x:{CX:.1f},y:{CY:.1f},scale:{S_BOX},transformOrigin:"0 0"}});gsap.set("#fbox",{{clipPath:"{BOX_IN}"}});gsap.set("#aroll",{{opacity:0}});'
for a, b in FULL:
    face_js += (f'M.to("#fbox",{{clipPath:"{BOX_FULL}",duration:.4,ease:"power3.inOut"}},{a:.3f});'
                f'M.to("#cut",{{opacity:0,duration:.25}},{a + .1:.3f});M.to("#aroll",{{opacity:1,duration:.25}},{a + .1:.3f});'
                f'M.to("#aroll",{{opacity:0,duration:.25}},{b - .3:.3f});M.to("#cut",{{opacity:1,duration:.25}},{b - .3:.3f});'
                f'M.to("#fbox",{{clipPath:"{BOX_IN}",duration:.4,ease:"power3.inOut"}},{b - .35:.3f});')
    sfx.append((a - 0.02, 'whoosh')); sfx.append((b - 0.37, 'whoosh'))

SND = dict(whoosh=whoosh(), pop=pop(), tick=tick(), ding=ding())
out = np.zeros(int((DUR + 1) * SR))
for t, kind in sfx:
    if t < 0:
        continue
    snd = SND[kind]; i = int(t * SR)
    out[i:i + len(snd)] += snd[:len(out) - i]
with wave.open('video/assets/sfx.wav', 'wb') as f:
    f.setnchannels(1); f.setsampwidth(2); f.setframerate(SR); f.writeframes((np.clip(out, -.9, .9) * 32767).astype(np.int16).tobytes())

# --- index.html ---------------------------------------------------------------------------------------------------
hosts = ''.join(
    f'<div id="{sc["id"]}" data-composition-id="{sc["id"]}" data-composition-src="compositions/{sc["id"]}.html" '
    f'data-start="{sc["start"]:.3f}" data-duration="{sc["dur"]:.3f}" data-track-index="2" data-track-kind="graphics" '
    f'data-width="1080" data-height="1920" style="z-index:10"></div>\n' for sc in scenes)
open('video/index.html', 'w').write(f'''<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=1080, height=1920" />
<script src="https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/gsap.min.js"></script>
<style>
* {{ margin:0; padding:0; box-sizing:border-box; }}
html, body {{ margin:0; width:1080px; height:1920px; overflow:hidden; background:{BG}; }}
#root {{ position:relative; width:1080px; height:1920px; overflow:hidden;
  background:radial-gradient(circle, rgba(0,0,0,.07) 1.5px, transparent 1.8px) 0 0/30px 30px, {BG}; }}
#fbox {{ position:absolute; left:0; top:0; width:1080px; height:1920px; z-index:15; background:linear-gradient(180deg,#1c1c1c,#0b0b0b); }}
#cut {{ position:absolute; left:0; top:0; width:1080px; height:1920px; object-fit:cover; z-index:16;
  -webkit-mask-image:linear-gradient(90deg,transparent 0,#000 17%,#000 83%,transparent 100%); mask-image:linear-gradient(90deg,transparent 0,#000 17%,#000 83%,transparent 100%); }}
#aroll {{ position:absolute; left:0; top:0; width:1080px; height:1920px; object-fit:cover; z-index:17; }}
</style>
</head>
<body>
<div id="root" data-composition-id="main" data-start="0" data-duration="{DUR:.3f}" data-width="1080" data-height="1920">
{hosts}<div id="cap2" data-composition-id="cap2" data-composition-src="compositions/cap2.html" data-start="0" data-duration="{DUR:.3f}" data-track-index="3" data-track-kind="graphics" data-width="1080" data-height="1920" style="z-index:12"></div>
<div id="fbox"></div>
<video id="cut" class="clip" src="assets/matte.webm" muted playsinline data-start="0" data-duration="{DUR:.3f}" data-track-index="0"></video>
<video id="aroll" class="clip" src="assets/aroll.mp4" data-start="0" data-duration="{DUR:.3f}" data-track-index="1" data-has-audio="true" data-volume="1" playsinline></video>
<div id="captions" data-composition-id="captions" data-composition-src="compositions/captions.html" data-start="0" data-duration="{DUR:.3f}" data-track-index="4" data-track-kind="captions" data-width="1080" data-height="1920" style="z-index:20"></div>
<audio id="sfx" class="clip" src="assets/sfx.wav" data-start="0" data-duration="{DUR:.3f}" data-track-index="5" data-volume="1"></audio>
</div>
<script>
window.__timelines = window.__timelines || {{}};
const M = gsap.timeline({{ paused: true }});
window.__timelines["main"] = M;
{face_js}
</script>
</body>
</html>
''')
print(f'ok: {len(groups)} grupos de legenda, {len(PHRASES)} frases, {len(scenes)} cartões, {len(sfx)} sons')
