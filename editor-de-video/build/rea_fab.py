#!/usr/bin/env python3
"""Estilo A — "Fabiano" (split): cartão creme no topo com linha-frase + banner laranja + prova real;
rosto embaixo em cartão arredondado com a cabeça recortada saindo por cima da borda. Gera video_rea_fab/.
uso (da pasta editor-de-video): python3 build/rea_fab.py
"""
import sys
sys.path.insert(0, 'build')
from rea_common import *  # noqa

P = 'video_rea_fab'
A = ASSETS
new_project(P, [(f'{A}/aroll.mp4', 'aroll.mp4'), ('work/rea01/matte/matte.webm', 'matte.webm'), (f'{A}/readme.png', 'readme.png'),
                (f'{A}/badges.png', 'badges.png'), (f'{A}/demo_orig.mp4', 'demo_orig.mp4'), (f'{A}/demo_ai.mp4', 'demo_ai.mp4')]
            + [(f'{A}/film_{k}.jpg', f'film_{k}.jpg') for k in range(12)]
            + [(f'{A}/{n}.jpg', f'{n}.jpg') for n in ('ai_a', 'code_a')])
sfx = []

captions(P, top=1062, size=66)

# --- linha-frase do topo: frase que se constrói (cinza → escura) + palavra-chave em serifa itálica com sublinhado -------
PHRASES = [(0, 2, None), (3, 10, 'engenharia reversa'), (11, 13, None), (14, 23, 'filmado'),
           (24, 30, 'IA ou código'), (31, 36, 'legendas'), (37, 42, 'cortes, áudios, efeitos'), (43, 51, 'do zero'),
           (52, 59, 'apps e jogos'), (60, 63, None), (64, 70, None), (71, 72, None), (73, 84, 'guia completo')]
html, js = [], []
for p, (a, b, kw) in enumerate(PHRASES):
    ws = W[a:b + 1]
    t0 = max(ws[0]['s'] - 0.05, 0.0)
    t1 = (W[PHRASES[p + 1][0]]['s'] - 0.07) if p + 1 < len(PHRASES) else DUR - 0.02
    chars = len(' '.join(w['w'] for w in ws))
    fs = max(28, min(38, int(900 / (chars * .56))))
    spans = ' '.join(f'<span id="p{p}w{n}" class="pw">{w["w"]}</span>' for n, w in enumerate(ws))
    kwh = ''
    if kw:
        kwh = f'<div id="p{p}k" class="kw">{kw}</div><svg class="ku" id="p{p}s" viewBox="0 0 1080 60" style="opacity:0"><path id="p{p}u" d="M540 0 L540 0"/></svg>'
    html.append(f'<div id="ph{p}" class="clip ph" data-start="{t0:.3f}" data-duration="{t1 - t0:.3f}"><div class="ln" style="font-size:{fs}px">{spans}</div>{kwh}</div>')
    js.append(f'tl.fromTo("#ph{p}",{{opacity:0,y:14}},{{opacity:1,y:0,duration:.2,ease:"power2.out"}},{t0:.3f});')
    for n, w in enumerate(ws):
        js.append(f'tl.to("#p{p}w{n}",{{color:"{INK}",duration:.1}},{w["s"]:.3f});')
    if kw:
        first = kw.split()[0].strip(',').lower()
        hit = [w for w in ws if w['w'].strip(',.').lower() == first]
        kt = hit[0]['s'] if hit else ws[-1]['s']
        uw = min(900, max(160, len(kw) * 30))
        js.append(f'tl.fromTo("#p{p}k",{{opacity:0,y:18,scale:.92}},{{opacity:1,y:0,scale:1,duration:.38,ease:"back.out(1.4)"}},{kt:.3f});')
        js.append(f'tl.set("#p{p}s",{{opacity:1}},{kt + .1:.3f});')
        js.append(f'tl.to("#p{p}u",{{attr:{{d:"M{540 - uw // 2} 0 Q540 -7 {540 + uw // 2} 0"}},duration:.32,ease:"power2.out"}},{kt + .1:.3f});')
        sfx.append((kt, 'tick'))
    js.append(f'tl.to("#ph{p}",{{opacity:0,duration:.12}},{t1 - .12:.3f});')
open(f'{P}/compositions/cap2.html', 'w').write(f'''<template>
<style>
#root {{ position:absolute; inset:0; font-family:'Inter',sans-serif; }}
.ph {{ position:absolute; left:0; right:0; top:236px; text-align:center; opacity:0; }}
.ln {{ font-weight:700; white-space:nowrap; letter-spacing:-.01em; }}
.pw {{ color:#a39c90; }}
.kw {{ margin-top:4px; font-family:'EB Garamond',serif; font-style:italic; font-weight:500; font-size:64px; line-height:1.05; color:{INK}; }}
.ku {{ position:absolute; left:0; top:126px; width:1080px; height:60px; overflow:visible; }}
.ku path {{ fill:none; stroke:{ORANGE}; stroke-width:6; stroke-linecap:round; }}
</style>
<div id="root" data-composition-id="cap2" data-width="1080" data-height="1920">
{chr(10).join(html)}
</div>
<script>
const tl = gsap.timeline({{ paused: true }});
{chr(10).join(js)}
window.__timelines["cap2"] = tl;
</script>
</template>
''')

# --- cenas do cartão (topo) --------------------------------------------------------------------------------------------
COMMON = f'''
#root {{ position:absolute; inset:0; font-family:'Inter',sans-serif; color:{INK}; }}
#wrap {{ position:absolute; inset:0; overflow:hidden; }}
.banner {{ position:absolute; left:0; right:0; top:384px; text-align:center; }}
.banner span {{ display:inline-block; background:{ORANGE}; color:#fff; font-family:'EB Garamond',serif; font-style:italic; font-weight:500;
  font-size:58px; padding:4px 34px 10px; border-radius:22px; box-shadow:0 10px 24px rgba(232,84,27,.34); }}
.ui {{ position:absolute; background:#161616; border-radius:28px; box-shadow:0 18px 40px rgba(0,0,0,.28); overflow:hidden; }}
.txt {{ position:absolute; font-weight:700; white-space:nowrap; }}
.tile {{ position:absolute; border-radius:16px; overflow:hidden; box-shadow:0 10px 22px rgba(0,0,0,.25); background:#222; }}
.tile img {{ width:100%; height:100%; object-fit:cover; display:block; }}
.tag {{ position:absolute; left:0; right:0; bottom:0; color:#fff; font-weight:800; text-align:left; padding:6px 10px; white-space:nowrap; }}
.pulse {{ position:absolute; border-radius:50%; background:radial-gradient(circle, rgba(232,84,27,.35), rgba(232,84,27,0) 65%); }}
.chk {{ position:absolute; width:46px; height:46px; border-radius:23px; background:{ORANGE}; color:#fff; font-size:30px; line-height:46px; text-align:center; font-weight:900; }}
'''
scenes = []


def scene(cid, start, end, body, anim, banner=None):
    dur = end - start
    bn = ''
    if banner:
        bn = f'<div class="banner" id="{cid}bn"><span>{banner[0]}</span></div>'
        anim = f'P("#{cid}bn",{banner[1]:.3f});' + anim
        sfx.append((banner[1], 'pop'))
    open(f'{P}/compositions/{cid}.html', 'w').write(f'''<template>
<style>{COMMON}</style>
<div id="root" data-composition-id="{cid}" data-width="1080" data-height="1920">
<div id="wrap">
{bn}
{body}
</div>
</div>
<script>
const tl = gsap.timeline({{ paused: true }});
const S = {start:.3f};
const P = (sel, t, d) => tl.fromTo(sel, {{ opacity: 0, y: 36, scale: .9 }}, {{ opacity: 1, y: 0, scale: 1, duration: d || .42, ease: "back.out(1.5)" }}, Math.max(0, t - S));
const F = (sel, t, d) => tl.fromTo(sel, {{ opacity: 0 }}, {{ opacity: 1, duration: d || .3, ease: "power2.out" }}, Math.max(0, t - S));
tl.fromTo("#wrap", {{ opacity: 0, filter: "blur(14px)", x: 70 }}, {{ opacity: 1, filter: "blur(0px)", x: 0, duration: 0.26, ease: "power2.out" }}, 0);
{anim}
tl.to("#wrap", {{ opacity: 0, filter: "blur(14px)", x: -70, duration: 0.2, ease: "power2.in" }}, {dur - 0.22:.3f});
window.__timelines["{cid}"] = tl;
</script>
</template>
''')
    if start > 0:
        sfx.append((start - 0.04, 'whoosh'))
    scenes.append(dict(id=cid, start=start, dur=dur))


def pulse(pid, cx, cy, r):
    return f'<div class="pulse" id="{pid}" style="left:{cx - r}px;top:{cy - r}px;width:{2 * r}px;height:{2 * r}px"></div>'


def pulse_js(pid, t):
    return (f'tl.fromTo("#{pid}",{{opacity:0,scale:.4}},{{opacity:1,scale:1,duration:.5,ease:"power2.out"}},Math.max(0,{t:.3f}-S));'
            f'tl.to("#{pid}",{{scale:1.08,opacity:.7,duration:.9,yoyo:true,repeat:3,ease:"sine.inOut"}},Math.max(0,{t + .5:.3f}-S));')


# A1 · abertura: o repositório (README real) + contador de estrelas
s, e = 0.0, T(11) - 0.06
body = pulse('a1p', 540, 760, 460)
body += (f'<div class="ui" id="a1c" style="left:70px;top:520px;width:940px;height:330px;border:3px solid {ORANGE}">'
         f'<img src="assets/readme.png" style="position:absolute;left:-14px;top:6px;width:967px"></div>'
         f'<div class="ui" id="a1s" style="left:250px;top:880px;width:580px;height:150px;background:#fff;border:3px solid {INK}">'
         f'<div class="txt" style="left:34px;top:22px;font-size:30px;color:#777">estrelas no GitHub</div>'
         f'<div class="txt" id="a1n" style="left:34px;top:58px;font-size:68px;font-weight:900;font-variant-numeric:tabular-nums">0</div>'
         f'<div class="txt" style="left:420px;top:48px;font-size:78px;color:{ORANGE}">★</div></div>')
anim = pulse_js('a1p', 0.1)
anim += f'tl.fromTo("#a1c",{{opacity:0,y:50,scale:.94}},{{opacity:1,y:0,scale:1,duration:.5,ease:"power3.out"}},0.02);'
anim += f'P("#a1s",{T(2):.3f});'
t0 = T(2) + .15
for k in range(1, 23):
    v = int(round(11000 * (1 - (1 - k / 22) ** 2.2), -1)) if k < 22 else 11000
    anim += f'tl.set("#a1n",{{textContent:"{v:,}".replace(",",".")}},{t0 + k * 0.05:.3f}-S);'
anim += f'tl.set("#a1n",{{textContent:"11 mil"}},{t0 + 1.35:.3f}-S);tl.fromTo("#a1n",{{scale:1.15}},{{scale:1,duration:.3,ease:"back.out(2)"}},{t0 + 1.35:.3f}-S);'
sfx += [(T(2), 'pop'), (t0 + 1.35, 'ding')]
scene('a1', s, e, body, anim, banner=('código aberto no GitHub', T(6)))

# A2 · plano por plano: os 12 planos de uma quebra real, rotulados (filmado / IA)
s, e = T(11), T(24) - 0.06
LBL = [('filmado', 88), ('filmado', 53), ('filmado', 87), ('filmado', 88), ('filmado', 88), ('filmado', 93),
       ('filmado', 88), ('filmado', 86), ('filmado', 85), ('filmado', 53), ('IA', 53), ('filmado', 86)]
body, anim = '', ''
for k in range(12):
    x, y = 105 + (k % 6) * 148, 500 + (k // 6) * 270
    lab, pc = LBL[k]
    col = GREEN if lab == 'filmado' else MAGENTA
    body += (f'<div class="tile" id="a2t{k}" style="left:{x}px;top:{y}px;width:130px;height:231px">'
             f'<img src="assets/film_{k}.jpg"><div class="tag" id="a2g{k}" style="background:{col};font-size:19px;opacity:0">{lab} {pc}%</div></div>'
             f'<div class="txt" id="a2n{k}" style="left:{x}px;top:{y + 236}px;font-size:20px;color:#777">plano {k + 1}</div>')
    tt = T(11) + k * 0.085
    anim += f'P("#a2t{k}",{tt:.3f},.32);F("#a2n{k}",{tt + .1:.3f},.2);'
    anim += f'tl.fromTo("#a2g{k}",{{opacity:0,y:20}},{{opacity:1,y:0,duration:.22}},{T(23) - .05 + k * 0.05:.3f}-S);'
    if k % 3 == 0:
        sfx.append((tt, 'tick'))
anim += f'tl.to("#a2t10",{{scale:1.12,duration:.25,yoyo:true,repeat:1}},{T(23) + .7:.3f}-S);'
sfx.append((T(23), 'pop'))
scene('a2', s, e, body, anim, banner=('12 planos, 12 rótulos', T(11) + .05))

# A3 · filmado × IA × código (três planos reais, cada um no seu rótulo)
s, e = T(24), T(31) - 0.06
body = pulse('a3p', 540, 790, 420)
anim = pulse_js('a3p', s + .05)
for n, (img, lab, pc, col, tt) in enumerate([('film_5', 'filmado', 93, GREEN, s + .02), ('ai_a', 'IA', 72, MAGENTA, T(26)),
                                              ('code_a', 'código', 50, ORANGE, T(30))]):
    x = 84 + n * 314
    body += (f'<div class="tile" id="a3t{n}" style="left:{x}px;top:500px;width:284px;height:504px;border:4px solid {col}">'
             f'<img src="assets/{img}.jpg"><div class="tag" style="background:{col};font-size:30px;text-align:center">{lab} {pc}%</div></div>')
    anim += f'P("#a3t{n}",{tt:.3f},.4);'
    sfx.append((tt, 'pop'))
scene('a3', s, e, body, anim, banner=('quem fez cada plano?', s + .05))

# A4 · como foi feito: as camadas que ele descreve (VIDEO.md)
s, e = T(31), T(43) - 0.06
rows = [('legendas', T(36), 'Aa'), ('cortes', T(38), '✂'), ('áudios', T(40), '♪'), ('efeitos', T(42), '✦')]
body = (f'<div class="ui" id="a4c" style="left:110px;top:500px;width:860px;height:560px">'
        f'<div class="txt" style="left:40px;top:30px;font-size:34px;color:#fff;font-family:monospace">VIDEO.md</div>'
        f'<div style="position:absolute;left:40px;top:86px;width:780px;height:3px;background:#333"></div>')
anim = f'P("#a4c",{s + .02:.3f},.45);'
for n, (lab, tt, ic) in enumerate(rows):
    y = 120 + n * 108
    body += (f'<div id="a4r{n}" style="position:absolute;left:30px;top:{y}px;width:800px;height:92px;border-radius:18px;background:#222;opacity:.35">'
             f'<div class="txt" style="left:24px;top:14px;width:64px;height:64px;border-radius:14px;background:#333;color:{ORANGE};font-size:40px;line-height:64px;text-align:center">{ic}</div>'
             f'<div class="txt" style="left:112px;top:20px;font-size:44px;color:#fff">{lab}</div>'
             f'<div class="chk" id="a4k{n}" style="left:726px;top:23px;opacity:0">✓</div></div>')
    anim += (f'tl.to("#a4r{n}",{{opacity:1,background:"#2b211c",duration:.2}},{tt:.3f}-S);'
             f'tl.fromTo("#a4k{n}",{{opacity:0,scale:.3}},{{opacity:1,scale:1,duration:.3,ease:"back.out(2.2)"}},{tt + .05:.3f}-S);')
    sfx.append((tt + .05, 'pop'))
body += '</div>'
scene('a4', s, e, body, anim, banner=('como cada plano foi feito', s + .05))

# A5 · refaz do zero: original filmado × refeito por IA (vídeos reais no index; aqui as molduras e rótulos)
s, e = T(43), T(52) - 0.06
Z_TILES = [(110, 'original · filmado', '#555', s + .05), (580, 'refeito · IA', MAGENTA, T(49))]
body, anim = pulse('a5p', 775, 780, 330), pulse_js('a5p', T(49))
for n, (x, lab, col, tt) in enumerate(Z_TILES):
    body += (f'<div class="tile" id="a5f{n}" style="left:{x - 6}px;top:500px;width:402px;height:560px;background:{col}"></div>'
             f'<div class="txt" id="a5l{n}" style="left:{x}px;width:390px;text-align:center;top:1004px;font-size:30px;color:#fff">{lab}</div>')
    anim += f'P("#a5f{n}",{tt:.3f},.4);F("#a5l{n}",{tt + .1:.3f});'
body += f'<div class="txt" id="a5a" style="left:508px;top:700px;font-size:80px;color:{ORANGE}">→</div>'
anim += f'P("#a5a",{T(49) - .15:.3f},.3);'
sfx.append((T(49), 'pop'))
scene('a5', s, e, body, anim, banner=('original × refeito', s + .05))
A5_VIDEOS = [('demo_orig', 110, s + .05, e), ('demo_ai', 580, T(49), e)]

# A6 · apps ✓ jogos ✓ … vídeos
s, e = T(52), T(64) - 0.06
ICONS = {
    'apps': '<rect x="14" y="14" width="30" height="30" rx="8"/><rect x="56" y="14" width="30" height="30" rx="8"/><rect x="14" y="56" width="30" height="30" rx="8"/><rect x="56" y="56" width="30" height="30" rx="8"/>',
    'jogos': '<path d="M22 34 h56 a16 16 0 0 1 16 16 v6 a16 16 0 0 1 -28 10 l-6 -6 h-20 l-6 6 a16 16 0 0 1 -28 -10 v-6 a16 16 0 0 1 16 -16z"/><path d="M30 46 v12 M24 52 h12" stroke="#fff" stroke-width="5"/>',
}
body, anim = '', ''
for n, (lab, tt) in enumerate([('apps', T(57)), ('jogos', T(59))]):
    x = 150 + n * 420
    body += (f'<div class="ui" id="a6c{n}" style="left:{x}px;top:520px;width:360px;height:200px;background:#fff;border:3px solid {INK}">'
             f'<svg viewBox="0 0 100 100" style="position:absolute;left:28px;top:44px;width:110px;height:110px" fill="{INK}">{ICONS[lab]}</svg>'
             f'<div class="txt" style="left:160px;top:66px;font-size:56px">{lab}</div>'
             f'<div class="chk" id="a6k{n}" style="left:296px;top:-2px;opacity:0;background:{GREEN}">✓</div></div>')
    anim += (f'P("#a6c{n}",{T(56) if n == 0 else tt - .1:.3f},.4);'
             f'tl.fromTo("#a6k{n}",{{opacity:0,scale:.3}},{{opacity:1,scale:1,duration:.3,ease:"back.out(2.2)"}},{tt + .15:.3f}-S);')
    sfx.append((tt + .15, 'pop'))
body += pulse('a6p', 540, 900, 300)
body += (f'<div class="ui" id="a6v" style="left:260px;top:770px;width:560px;height:260px;border:4px solid {ORANGE}">'
         f'<svg viewBox="0 0 100 100" style="position:absolute;left:36px;top:60px;width:140px;height:140px"><circle cx="50" cy="50" r="46" fill="{ORANGE}"/><path d="M40 30 L72 50 L40 70z" fill="#fff"/></svg>'
         f'<div class="txt" style="left:210px;top:62px;font-family:\'EB Garamond\',serif;font-style:italic;font-weight:500;font-size:110px;color:#fff">vídeos</div></div>')
anim += pulse_js('a6p', T(63)) + f'P("#a6v",{T(61):.3f},.5);'
anim += f'tl.to(["#a6c0","#a6c1"],{{opacity:.45,scale:.94,duration:.3}},{T(61):.3f}-S);'
sfx.append((T(63), 'ding'))
scene('a6', s, e, body, anim, banner=('apps → jogos → vídeos', T(56)))

# A7 · CTA: comentário "EDIT" + resposta no Direct
s, e = T(64) - 0.1, DUR
body = (f'<div class="ui" id="a7c" style="left:110px;top:520px;width:860px;height:220px;background:#fff;border:3px solid {INK}">'
        f'<div style="position:absolute;left:30px;top:30px;width:70px;height:70px;border-radius:35px;background:#ddd"></div>'
        f'<div class="txt" style="left:118px;top:44px;font-size:32px;color:#666">você</div>'
        f'<div style="position:absolute;left:30px;top:120px;width:800px;height:76px;border-radius:38px;background:#f1f1f1">'
        f'<div class="txt" id="a7p" style="left:34px;top:20px;font-size:32px;color:#999">Adicione um comentário…</div>'
        f'<div class="txt" id="a7x" style="left:34px;top:12px;font-size:46px;font-weight:900;letter-spacing:.05em;opacity:0"></div>'
        f'<div id="a7s" style="position:absolute;right:12px;top:10px;width:56px;height:56px;border-radius:28px;background:{ORANGE};color:#fff;font-size:28px;line-height:56px;text-align:center">➤</div></div></div>'
        f'<div class="ui" id="a7d" style="left:110px;top:780px;width:860px;height:200px">'
        f'<div style="position:absolute;left:30px;top:40px;width:110px;height:110px;border-radius:24px;background:{ORANGE};color:#fff;font-size:44px;font-weight:900;line-height:110px;text-align:center">DM</div>'
        f'<div class="txt" style="left:170px;top:44px;font-size:38px;color:#fff">Direct</div>'
        f'<div class="txt" style="left:170px;top:100px;font-size:34px;color:#bbb">link + guia completo ✓</div></div>')
anim = f'P("#a7c",{s + .1:.3f});'
t0 = T(72) + 0.05
for n in range(4):
    anim += f'tl.set("#a7x",{{textContent:"{"EDIT"[:n + 1]}"}},{t0 + n * .12:.3f}-S);'
    sfx.append((t0 + n * .12, 'tick'))
anim += f'tl.set("#a7p",{{opacity:0}},{t0:.3f}-S);tl.set("#a7x",{{opacity:1}},{t0:.3f}-S);tl.to("#a7s",{{scale:.85,duration:.1,yoyo:true,repeat:1}},{t0 + .6:.3f}-S);P("#a7d",{T(78):.3f});'
sfx += [(t0 + .6, 'tick'), (T(78), 'ding')]
scene('a7', s, e, body, anim, banner=('link + guia no Direct', T(73)))

# --- index: cartão do rosto (bruto no cartão + cabeça recortada por cima da borda) -------------------------------------
VW, VH, VX, VY = 1703, 950, -260, 1030   # vídeo 16:9 ampliado; cabelo a ~17% do topo do bruto → y ≈ 1170; cartão em y 1240
CARD_TOP = 1240
vids = ''
for n, (vid, x, t0v, t1v) in enumerate(A5_VIDEOS):
    vids += (f'<video id="{vid}" class="clip pv" src="assets/{vid}.mp4" muted playsinline data-start="{t0v:.3f}" data-duration="{t1v - t0v:.3f}" '
             f'data-track-index="{6 + n}" style="left:{x}px;top:506px;width:390px;height:548px"></video>\n')
vjs = ''.join(f'M.fromTo("#{vid}",{{opacity:0,y:36,scale:.9}},{{opacity:1,y:0,scale:1,duration:.42,ease:"back.out(1.5)"}},{t0v:.3f});'
              f'M.to("#{vid}",{{opacity:0,x:-70,duration:.2}},{t1v - .22:.3f});' for vid, x, t0v, t1v in A5_VIDEOS)
hosts = '\n'.join(host(sc['id'], sc['start'], sc['dur'], 2, 10) for sc in scenes)
open(f'{P}/index.html', 'w').write(f'''<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=1080, height=1920" />
<script src="https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/gsap.min.js"></script>
<style>
* {{ margin:0; padding:0; box-sizing:border-box; }}
html, body {{ margin:0; width:1080px; height:1920px; overflow:hidden; background:{CREAM}; }}
#root {{ position:relative; width:1080px; height:1920px; overflow:hidden;
  background:radial-gradient(circle, rgba(0,0,0,.07) 1.5px, transparent 1.8px) 0 0/30px 30px, #F4EFE6; }}
#fcard {{ position:absolute; left:36px; top:{CARD_TOP}px; width:1008px; height:{1920 - CARD_TOP + 60}px; border-radius:44px; overflow:hidden;
  z-index:15; background:#111; box-shadow:0 -8px 30px rgba(0,0,0,.18); }}
#aroll {{ position:absolute; left:{VX - 36}px; top:{VY - CARD_TOP}px; width:{VW}px; height:{VH}px; }}
#headwrap {{ position:absolute; left:0; top:0; width:1080px; height:{CARD_TOP + 2}px; overflow:hidden; z-index:16; }}
#cut {{ position:absolute; left:{VX}px; top:{VY}px; width:{VW}px; height:{VH}px;
  -webkit-mask-image:linear-gradient(90deg,transparent 31%,#000 38%,#000 58%,transparent 65%); mask-image:linear-gradient(90deg,transparent 31%,#000 38%,#000 58%,transparent 65%); }}
.pv {{ position:absolute; z-index:13; border-radius:12px; object-fit:cover; }}
</style>
</head>
<body>
<div id="root" data-composition-id="main" data-start="0" data-duration="{DUR:.3f}" data-width="1080" data-height="1920">
{hosts}
<div id="cap2" data-composition-id="cap2" data-composition-src="compositions/cap2.html" data-start="0" data-duration="{DUR:.3f}" data-track-index="3" data-track-kind="graphics" data-width="1080" data-height="1920" style="z-index:12"></div>
{vids}<div id="fcard"><video id="aroll" class="clip" src="assets/aroll.mp4" data-start="0" data-duration="{DUR:.3f}" data-track-index="1" data-has-audio="true" data-volume="1" playsinline></video></div>
<div id="headwrap"><video id="cut" class="clip" src="assets/matte.webm" muted playsinline data-start="0" data-duration="{DUR:.3f}" data-track-index="0"></video></div>
<div id="captions" data-composition-id="captions" data-composition-src="compositions/captions.html" data-start="0" data-duration="{DUR:.3f}" data-track-index="4" data-track-kind="captions" data-width="1080" data-height="1920" style="z-index:20"></div>
<audio id="sfx" class="clip" src="assets/sfx.wav" data-start="0" data-duration="{DUR:.3f}" data-track-index="5" data-volume="1"></audio>
</div>
<script>
window.__timelines = window.__timelines || {{}};
const M = gsap.timeline({{ paused: true }});
window.__timelines["main"] = M;
{vjs}
</script>
</body>
</html>
''')
write_sfx(P, sfx)
print(f'ok {P}: {len(scenes)} cenas, {len(PHRASES)} frases, {len(sfx)} sons')
