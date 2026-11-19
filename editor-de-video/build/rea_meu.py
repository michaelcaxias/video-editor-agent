#!/usr/bin/env python3
"""Estilo B — "raio-X do próprio vídeo" (do meu jeito, dentro do guia de estilo: creme + coral, Inter 900 + Caveat,
legenda branca com contorno, rosto ↔ prova a cada 2–4 s, CTA com comentário digitado + resposta).
Topo: rosto num monitor 16:9 (o bruto é horizontal; quase sem ampliar) com selo do plano (filmado / código).
Base: a linha do tempo real deste vídeo (cortes, legendas, onda do áudio, efeitos) sendo lida pelo cursor.
uso (da pasta editor-de-video): python3 build/rea_meu.py
"""
import json, sys
sys.path.insert(0, 'build')
from rea_common import *  # noqa

P = 'video_rea_meu'
A = ASSETS
new_project(P, [(f'{A}/aroll.mp4', 'aroll.mp4'), (f'{A}/readme.png', 'readme.png'), (f'{A}/badges.png', 'badges.png'),
                (f'{A}/paper_orig.mp4', 'paper_orig.mp4'), (f'{A}/paper_remake.mp4', 'paper_remake.mp4'),
                ('build/hf-template/fonts/caveat-700.woff2', 'fonts/caveat-700.woff2')]
            + [(f'{A}/{n}.jpg', f'{n}.jpg') for n in ('film_5', 'ai_a', 'code_a')])
sfx = []
MX, MY, MW, MH = 40, 300, 1000, 563          # monitor (16:9)
TX, TY, TW = 270, 1092, 740                    # área das trilhas da linha do tempo
PX = TW / DUR
FONT = "@font-face { font-family:'Caveat'; font-weight:700; src:url('assets/fonts/caveat-700.woff2') format('woff2'); }"

groups = captions(P, top=896, size=64)

# --- planos: prova (código) nas janelas abaixo; rosto (filmado) no resto, com os jump cuts reais do A-roll ---------
PROOF = [('b1', 0.0, T(3) - 0.06), ('b2', T(24), T(31) - 0.06), ('b3', T(43), T(52) - 0.06), ('b4', T(52), T(64) - 0.06)]
jumps = [s['t0'] for s in json.load(open(f'{SRC}/segments.json'))][1:]
bounds = sorted(set([0.0, DUR] + [x for _, a, b in PROOF for x in (a, b + 0.06)] +
                    [j for j in jumps if not any(a - .3 <= j <= b + .3 for _, a, b in PROOF)]))
shots = []
for a, b in zip(bounds, bounds[1:]):
    if b - a < 0.2:
        continue
    kind = 'código' if any(pa - .01 <= a < pb for _, pa, pb in PROOF) else 'filmado'
    shots.append((a, b, kind))

COMMON = f'''{FONT}
#root {{ position:absolute; inset:0; font-family:'Inter',sans-serif; color:{INK}; }}
.txt {{ position:absolute; font-weight:700; white-space:nowrap; }}
.hand {{ position:absolute; font-family:'Caveat',cursive; font-weight:700; color:{CORAL}; white-space:nowrap; }}
.card {{ position:absolute; border-radius:22px; box-shadow:0 12px 26px rgba(0,0,0,.18); overflow:hidden; }}
.tile {{ position:absolute; border-radius:16px; overflow:hidden; box-shadow:0 10px 22px rgba(0,0,0,.25); }}
.tile img {{ width:100%; height:100%; object-fit:cover; display:block; }}
.tag {{ position:absolute; left:0; right:0; bottom:0; color:#fff; font-weight:800; font-size:26px; text-align:center; padding:6px 0; }}
'''


def comp(cid, start, end, body, anim, extra_css='', clip_mon=False):
    dur = end - start
    if clip_mon:  # prova dentro do monitor, entra e sai com wipe
        body = (f'<div id="wrap" style="position:absolute;left:{MX}px;top:{MY}px;width:{MW}px;height:{MH}px;border-radius:30px;overflow:hidden">'
                f'{body}</div>')
        anim = (f'tl.fromTo("#wrap",{{clipPath:"inset(0% 0% 0% 100%)"}},{{clipPath:"inset(0% 0% 0% 0%)",duration:.3,ease:"power3.out"}},0);' + anim +
                f'tl.to("#wrap",{{clipPath:"inset(0% 100% 0% 0%)",duration:.24,ease:"power3.in"}},{dur - .26:.3f});')
        if start > 0:
            sfx.append((start - .03, 'whoosh'))
    open(f'{P}/compositions/{cid}.html', 'w').write(f'''<template>
<style>{COMMON}{extra_css}</style>
<div id="root" data-composition-id="{cid}" data-width="1080" data-height="1920">
{body}
</div>
<script>
const tl = gsap.timeline({{ paused: true }});
const S = {start:.3f};
const P = (sel, t, d) => tl.fromTo(sel, {{ opacity: 0, y: 30, scale: .9 }}, {{ opacity: 1, y: 0, scale: 1, duration: d || .4, ease: "back.out(1.5)" }}, Math.max(0, t - S));
const F = (sel, t, d) => tl.fromTo(sel, {{ opacity: 0 }}, {{ opacity: 1, duration: d || .3, ease: "power2.out" }}, Math.max(0, t - S));
const D = (sel, t, d) => tl.fromTo(sel, {{ strokeDashoffset: 1.05 }}, {{ strokeDashoffset: 0, duration: d || .5, ease: "power1.inOut" }}, Math.max(0, t - S));
{anim}
window.__timelines["{cid}"] = tl;
</script>
</template>
''')
    return dict(id=cid, start=start, dur=dur)


hosts = []

# b1 · README real do repositório (prova no quadro 0)
_, s, e = PROOF[0]
body = (f'<div style="position:absolute;inset:0;background:#10131a"></div>'
        f'<img id="b1r" src="assets/readme.png" style="position:absolute;left:16px;top:70px;width:967px">'
        f'<img id="b1b" src="assets/badges.png" style="position:absolute;left:220px;top:400px;width:560px">'
        f'<div class="hand" id="b1h" style="left:640px;top:440px;font-size:64px;transform:rotate(-6deg)">11 mil ★</div>')
anim = 'tl.fromTo("#b1r",{scale:1.08},{scale:1,duration:1.6,ease:"power2.out"},0);P("#b1b",.35);P("#b1h",.8);'
sfx.append((0.8, 'pop'))
hosts.append(comp('b1', s, e, body, anim, clip_mon=True))

# b2 · filmado × IA × código (planos reais de uma quebra do rea-video)
_, s, e = PROOF[1]
body = f'<div style="position:absolute;inset:0;background:#F4EFE6"></div>'
anim = ''
for n, (img, lab, pc, col, tt) in enumerate([('film_5', 'filmado', 93, GREEN, s + .05), ('ai_a', 'IA', 72, MAGENTA, T(26)),
                                              ('code_a', 'código', 50, CORAL, T(30))]):
    x = 115 + n * 270
    body += (f'<div class="tile" id="b2t{n}" style="left:{x}px;top:36px;width:250px;height:444px;border:4px solid {col}">'
             f'<img src="assets/{img}.jpg"><div class="tag" style="background:{col}">{lab} {pc}%</div></div>')
    anim += f'P("#b2t{n}",{tt:.3f});'
    sfx.append((tt, 'pop'))
body += '<div class="hand" style="left:0;right:0;text-align:center;top:486px;font-size:54px" id="b2h">o rea-video rotula cada plano</div>'
anim += 'F("#b2h",' + f'{s + .4:.3f});'
hosts.append(comp('b2', s, e, body, anim, clip_mon=True))

# b3 · original × refeito do zero (vídeos reais no index; aqui fundo e rótulos)
_, s, e = PROOF[2]
B3_VIDEOS = [('paper_orig', MX + 20, MY + 170, s + .05, e), ('paper_remake', MX + 510, MY + 170, T(49), e)]
body = (f'<div style="position:absolute;inset:0;background:#1a1a1a"></div>'
        f'<div class="txt" id="b3l0" style="left:20px;top:112px;font-size:36px;color:#ddd">original</div>'
        f'<div class="txt" id="b3l1" style="left:510px;top:112px;font-size:36px;color:{CORAL}">refeito do zero</div>'
        f'<div class="hand" id="b3h" style="left:470px;top:420px;font-size:62px;transform:rotate(-4deg)">mesmo plano, outro estilo</div>')
anim = f'F("#b3l0",{s + .1:.3f});F("#b3l1",{T(49):.3f});P("#b3h",{T(49) + .5:.3f});'
sfx.append((T(49), 'pop'))
hosts.append(comp('b3', s, e, body, anim, clip_mon=True))

# b4 · apps ✓ jogos ✓ → vídeos (lousa)
_, s, e = PROOF[3]
body = (f'<div style="position:absolute;inset:0;background:#F4EFE6"></div>'
        f'<div class="txt" id="b4t" style="left:80px;top:112px;font-size:34px;color:#857e73">já aprenderam a clonar:</div>'
        f'<div class="hand" id="b4a" style="left:80px;top:150px;font-size:110px;color:{INK}">apps <span style="color:{GREEN}">✓</span></div>'
        f'<div class="hand" id="b4j" style="left:80px;top:290px;font-size:110px;color:{INK}">jogos <span style="color:{GREEN}">✓</span></div>'
        f'<div class="txt" id="b4v" style="left:520px;top:210px;font-size:118px;font-weight:900;color:{CORAL}">vídeos</div>'
        f'<svg style="position:absolute;left:0;top:0;width:{MW}px;height:{MH}px;overflow:visible" viewBox="0 0 {MW} {MH}">'
        f'<path id="b4c" d="M520 200 C 640 150 900 160 940 250 C 980 350 760 390 600 378 C 470 365 470 260 560 220" pathLength="1" fill="none" '
        f'stroke="{CORAL}" stroke-width="8" stroke-linecap="round" style="stroke-dasharray:1 2;stroke-dashoffset:1.05"/>'
        f'<path id="b4s" d="M80 460 L940 460" pathLength="1" stroke="{INK}" stroke-width="5" stroke-linecap="round" style="stroke-dasharray:1 2;stroke-dashoffset:1.05"/></svg>'
        f'<div class="hand" id="b4n" style="left:600px;top:400px;font-size:58px;transform:rotate(-5deg)">a vez deles</div>')
anim = (f'F("#b4t",{s + .15:.3f});'
        f'tl.fromTo("#b4a",{{opacity:0,x:-30}},{{opacity:1,x:0,duration:.3}},{T(57) - .15:.3f}-S);'
        f'tl.fromTo("#b4j",{{opacity:0,x:-30}},{{opacity:1,x:0,duration:.3}},{T(59) - .1:.3f}-S);'
        f'tl.to(["#b4a","#b4j"],{{opacity:.35,duration:.3}},{T(60):.3f}-S);'
        f'P("#b4v",{T(62):.3f},.45);D("#b4c",{T(63):.3f},.55);F("#b4n",{T(63) + .3:.3f});')
sfx += [(T(57), 'tick'), (T(59), 'tick'), (T(63), 'ding')]
hosts.append(comp('b4', s, e, body, anim, clip_mon=True))

# CTA · comentário "EDIT" + resposta no Direct (cobre a linha do tempo)
s, e = T(64) - 0.1, DUR
body = (f'<div id="kbg" style="position:absolute;left:40px;top:1010px;width:1000px;height:640px;border-radius:30px;background:#F4EFE6"></div>'
        f'<div class="card" id="k1c" style="left:80px;top:1060px;width:920px;height:230px;background:#fff;border:4px solid {INK}">'
        f'<div style="position:absolute;left:30px;top:30px;width:72px;height:72px;border-radius:36px;background:#ddd"></div>'
        f'<div class="txt" style="left:120px;top:46px;font-size:32px;color:#666">você</div>'
        f'<div style="position:absolute;left:30px;top:124px;width:856px;height:78px;border-radius:39px;background:#f1f1f1">'
        f'<div class="txt" id="k1p" style="left:34px;top:22px;font-size:32px;color:#999">Adicione um comentário…</div>'
        f'<div class="txt" id="k1x" style="left:34px;top:12px;font-size:48px;font-weight:900;letter-spacing:.05em;opacity:0"></div>'
        f'<div id="k1s" style="position:absolute;right:12px;top:11px;width:56px;height:56px;border-radius:28px;background:{CORAL};color:#fff;font-size:28px;line-height:56px;text-align:center">➤</div></div></div>'
        f'<div class="card" id="k1d" style="left:80px;top:1330px;width:920px;height:200px;background:{INK}">'
        f'<div style="position:absolute;left:30px;top:44px;width:112px;height:112px;border-radius:26px;background:{CORAL};color:#fff;font-size:44px;font-weight:900;line-height:112px;text-align:center">DM</div>'
        f'<div class="txt" style="left:172px;top:46px;font-size:38px;color:#fff">Direct</div>'
        f'<div class="txt" style="left:172px;top:102px;font-size:34px;color:#bbb">link + guia completo ✓</div></div>'
        f'<div class="hand" id="k1h" style="left:640px;top:1540px;font-size:64px;transform:rotate(-4deg)">comenta EDIT ↑</div>')
anim = ('tl.fromTo("#kbg",{opacity:0},{opacity:1,duration:.25},0);P("#k1c",.05);' + f'F("#k1h",{T(71):.3f});')
t0 = T(72) + 0.05
for n in range(4):
    anim += f'tl.set("#k1x",{{textContent:"{"EDIT"[:n + 1]}"}},{t0 + n * .12:.3f}-S);'
    sfx.append((t0 + n * .12, 'tick'))
anim += f'tl.set("#k1p",{{opacity:0}},{t0:.3f}-S);tl.set("#k1x",{{opacity:1}},{t0:.3f}-S);tl.to("#k1s",{{scale:.85,duration:.1,yoyo:true,repeat:1}},{t0 + .6:.3f}-S);P("#k1d",{T(78):.3f});'
sfx += [(s, 'whoosh'), (t0 + .6, 'tick'), (T(78), 'ding')]
cta = comp('k1', s, e, body, anim)

# --- HUD do monitor: cantos, selo do plano (nº + filmado/código), feixe de varredura, timecode --------------------------
corner = lambda x, y, dx, dy: f'<path d="M{x} {y + dy * 46} L{x} {y} L{x + dx * 46} {y}" />'
body = (f'<svg style="position:absolute;left:0;top:0;width:1080px;height:1920px;overflow:visible"><g fill="none" stroke="{CORAL}" stroke-width="6" stroke-linecap="round">'
        + corner(MX + 22, MY + 22, 1, 1) + corner(MX + MW - 22, MY + 22, -1, 1) + corner(MX + 22, MY + MH - 22, 1, -1) + corner(MX + MW - 22, MY + MH - 22, -1, -1)
        + '</g></svg>'
        f'<div style="position:absolute;left:{MX}px;top:{MY}px;width:{MW}px;height:{MH}px;border-radius:30px;overflow:hidden">'
        f'<div id="beam" style="position:absolute;left:0;top:0;width:{MW}px;height:90px;opacity:0;'
        f'background:linear-gradient(180deg,rgba(217,87,59,0),rgba(217,87,59,.45) 85%,{CORAL} 100%)"></div></div>'
        f'<div id="chip" style="position:absolute;left:{MX + 40}px;top:{MY + 36}px;height:52px;border-radius:26px;background:rgba(22,20,18,.82);'
        f'color:#fff;font-weight:800;font-size:28px;line-height:52px;padding:0 22px;white-space:nowrap">'
        f'<span id="cn">PLANO 01</span><span id="ck" style="margin-left:14px;padding:4px 12px;border-radius:14px;background:{CORAL}">código</span></div>'
        f'<div class="hand" style="left:56px;top:176px;font-size:68px">raio-x deste vídeo</div>'
        f'<div class="txt" id="tc" style="right:60px;top:196px;font-size:40px;font-variant-numeric:tabular-nums;color:{INK}">00:00.0</div>')
anim = ''
for n, (a, b, kind) in enumerate(shots):
    col = GREEN if kind == 'filmado' else CORAL
    anim += (f'tl.set("#cn",{{textContent:"PLANO {n + 1:02d}"}},{a:.3f});tl.set("#ck",{{textContent:"{kind}",background:"{col}"}},{a:.3f});'
             f'tl.fromTo("#chip",{{scale:.9}},{{scale:1,duration:.2,ease:"back.out(2)"}},{a:.3f});')
for k in range(int(DUR * 10) + 1):
    anim += f'tl.set("#tc",{{textContent:"00:{k // 10:02d}.{k % 10}"}},{k / 10:.2f});'
ts = T(6)  # "engenharia reversa": feixe varre o rosto
anim += (f'tl.set("#beam",{{opacity:1,y:-90}},{ts:.3f});tl.to("#beam",{{y:{MH - 90},duration:.9,ease:"power1.inOut"}},{ts:.3f});'
         f'tl.set("#beam",{{opacity:0}},{ts + .9:.3f});')
anim += f'tl.to("#ck",{{scale:1.25,duration:.18,yoyo:true,repeat:3}},{T(23):.3f});'  # "filmado"
sfx += [(ts, 'whoosh'), (T(23), 'pop')]
open(f'{P}/compositions/hud.html', 'w').write(f'''<template>
<style>{COMMON}#chip span {{ display:inline-block; line-height:1.2; }}</style>
<div id="root" data-composition-id="hud" data-width="1080" data-height="1920">
{body}
</div>
<script>
const tl = gsap.timeline({{ paused: true }});
{anim}
window.__timelines["hud"] = tl;
</script>
</template>
''')

# --- linha do tempo real (VIDEO.md): trilhas reveladas pelo cursor; cada camada acende quando é dita -----------------
ROWS = [('cortes', T(38)), ('legendas', T(36)), ('áudio', T(40)), ('efeitos', T(42))]
RY = {name: TY + n * 130 for n, (name, _) in enumerate(ROWS)}
tracks = ''
for a, b, kind in shots:  # cortes
    col = INK if kind == 'filmado' else CORAL
    tracks += f'<div style="position:absolute;left:{a * PX + 1:.1f}px;top:{RY["cortes"] - TY + 14}px;width:{(b - a) * PX - 3:.1f}px;height:72px;border-radius:8px;background:{col}"></div>'
for grp in groups:  # legendas
    a, b = grp[0]['s'], grp[-1]['e']
    tracks += f'<div style="position:absolute;left:{a * PX:.1f}px;top:{RY["legendas"] - TY + 30}px;width:{max(4, (b - a) * PX - 2):.1f}px;height:40px;border-radius:6px;background:#9c958a"></div>'
wf = waveform(150)
for k, v in enumerate(wf):  # áudio
    h = max(4, v * 84)
    tracks += f'<div style="position:absolute;left:{k * TW / 150:.1f}px;top:{RY["áudio"] - TY + 50 - h / 2:.1f}px;width:{TW / 150 - 1.5:.1f}px;height:{h:.1f}px;border-radius:2px;background:{CORAL}"></div>'
for t, kind in sfx:  # efeitos (os sons deste vídeo)
    if kind in ('pop', 'ding', 'whoosh') and 0 <= t < DUR:
        tracks += f'<div style="position:absolute;left:{t * PX - 9:.1f}px;top:{RY["efeitos"] - TY + 41}px;width:18px;height:18px;transform:rotate(45deg);background:{INK}"></div>'
labels = ''.join(f'<div class="txt lab" id="lb{n}" style="left:70px;top:{RY[name] + 28}px;font-size:36px;color:#857e73">{name}</div>'
                 f'<div id="lr{n}" style="position:absolute;left:56px;top:{RY[name]}px;width:968px;height:110px;border-radius:18px;background:rgba(217,87,59,.14);opacity:0"></div>'
                 for n, (name, _) in enumerate(ROWS))
body = (f'<div id="tw" style="position:absolute;inset:0"><div id="panel" style="position:absolute;left:40px;top:1010px;width:1000px;height:640px;border-radius:30px;background:#fff;border:4px solid {INK};box-shadow:0 14px 30px rgba(0,0,0,.12)"></div>'
        f'<div class="txt" style="left:76px;top:1034px;font-size:34px;font-weight:900">VIDEO.md</div>'
        f'{labels}<div id="rev" style="position:absolute;left:{TX}px;top:{TY}px;width:0px;height:520px;overflow:hidden"><div style="position:absolute;left:0;top:0;width:{TW}px;height:520px">{tracks}</div></div>'
        f'<div id="ph" style="position:absolute;left:{TX}px;top:{TY - 6}px;width:4px;height:524px;border-radius:2px;background:{CORAL}"></div>'
        f'<div class="hand" id="tln" style="left:520px;top:1036px;font-size:46px;opacity:0;transform:rotate(-3deg)">cada corte = um plano ↓</div></div>')
anim = f'tl.to("#rev",{{width:{TW},duration:{DUR:.3f},ease:"none"}},0);tl.to("#ph",{{x:{TW},duration:{DUR:.3f},ease:"none"}},0);'
anim += f'tl.to("#tw",{{opacity:0,duration:.2}},{T(64) + .2:.3f});'
anim += 'tl.fromTo("#panel",{opacity:0,y:40},{opacity:1,y:0,duration:.4,ease:"power3.out"},0);'
anim += f'tl.to("#tln",{{opacity:1,duration:.25}},{T(11):.3f});tl.to("#tln",{{opacity:0,duration:.25}},{T(24) - .3:.3f});'
anim += f'tl.to("#lr0",{{opacity:1,duration:.2,yoyo:true,repeat:3}},{T(11):.3f});tl.to("#lb0",{{color:"{INK}",duration:.2}},{T(11):.3f});'
for n, (name, tt) in enumerate(ROWS):
    anim += (f'tl.to("#lb{n}",{{color:"{CORAL}",scale:1.12,transformOrigin:"0 50%",duration:.18}},{tt:.3f});'
             f'tl.to("#lb{n}",{{color:"{INK}",scale:1,duration:.3}},{tt + .5:.3f});'
             f'tl.fromTo("#lr{n}",{{opacity:0}},{{opacity:1,duration:.15,yoyo:true,repeat:1}},{tt:.3f});')
    sfx.append((tt, 'pop'))
open(f'{P}/compositions/tline.html', 'w').write(f'''<template>
<style>{COMMON}</style>
<div id="root" data-composition-id="tline" data-width="1080" data-height="1920">
{body}
</div>
<script>
const tl = gsap.timeline({{ paused: true }});
{anim}
window.__timelines["tline"] = tl;
</script>
</template>
''')

# --- index -------------------------------------------------------------------------------------------------------
vids, vjs = '', ''
for n, (vid, x, y, t0v, t1v) in enumerate(B3_VIDEOS):
    vids += (f'<video id="{vid}" class="clip pv" src="assets/{vid}.mp4" muted playsinline data-start="{t0v:.3f}" data-duration="{t1v - t0v:.3f}" '
             f'data-track-index="{7 + n}" style="left:{x}px;top:{y}px;width:470px;height:222px"></video>\n')
    vjs += (f'M.fromTo("#{vid}",{{opacity:0,y:30,scale:.9}},{{opacity:1,y:0,scale:1,duration:.4,ease:"back.out(1.5)"}},{t0v:.3f});'
            f'M.to("#{vid}",{{opacity:0,duration:.2}},{t1v - .24:.3f});')
VS = MH / 928
hs = '\n'.join(host(h['id'], h['start'], h['dur'], 2, 16) for h in hosts)
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
  background:radial-gradient(circle, rgba(0,0,0,.07) 1.5px, transparent 1.8px) 0 0/30px 30px, {CREAM}; }}
#mon {{ position:absolute; left:{MX}px; top:{MY}px; width:{MW}px; height:{MH}px; border-radius:30px; overflow:hidden; z-index:15;
  background:#111; box-shadow:0 18px 40px rgba(0,0,0,.25); }}
#monb {{ position:absolute; left:{MX - 5}px; top:{MY - 5}px; width:{MW + 10}px; height:{MH + 10}px; border-radius:34px; border:5px solid {INK}; z-index:18; pointer-events:none; }}
#aroll {{ position:absolute; left:{(MW - 1664 * VS) / 2:.1f}px; top:0; width:{1664 * VS:.1f}px; height:{MH}px; }}
.pv {{ position:absolute; z-index:17; border-radius:12px; object-fit:cover; }}
</style>
</head>
<body>
<div id="root" data-composition-id="main" data-start="0" data-duration="{DUR:.3f}" data-width="1080" data-height="1920">
<div id="tline" data-composition-id="tline" data-composition-src="compositions/tline.html" data-start="0" data-duration="{DUR:.3f}" data-track-index="3" data-track-kind="graphics" data-width="1080" data-height="1920" style="z-index:12"></div>
<div id="mon"><video id="aroll" class="clip" src="assets/aroll.mp4" data-start="0" data-duration="{DUR:.3f}" data-track-index="1" data-has-audio="true" data-volume="1" playsinline></video></div>
{hs}
{vids}<div id="hud" data-composition-id="hud" data-composition-src="compositions/hud.html" data-start="0" data-duration="{DUR:.3f}" data-track-index="4" data-track-kind="graphics" data-width="1080" data-height="1920" style="z-index:19"></div>
<div id="monb"></div>
{host(cta['id'], cta['start'], cta['dur'], 6, 21)}
<div id="captions" data-composition-id="captions" data-composition-src="compositions/captions.html" data-start="0" data-duration="{DUR:.3f}" data-track-index="5" data-track-kind="captions" data-width="1080" data-height="1920" style="z-index:22"></div>
<audio id="sfx" class="clip" src="assets/sfx.wav" data-start="0" data-duration="{DUR:.3f}" data-track-index="9" data-volume="1"></audio>
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
print(f'ok {P}: {len(shots)} planos, {len(groups)} grupos de legenda, {len(sfx)} sons')
