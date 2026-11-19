#!/usr/bin/env python3
"""Transcreve takes com tempo por palavra (faster-whisper, local; GPU se houver CUDA, senão CPU).

Para cada vídeo: cria um link dele em --out (se estiver em outra pasta), extrai o áudio 16 kHz mono (<nome>.wav),
transcreve e grava <nome>.words.json = [{"i": 0, "w": "Você", "s": 0.48, "e": 0.71}, ...]. Imprime a transcrição
numerada ("[12]palavra"), usada para montar a EDL do cut_aroll.py, a duração e o primeiro ataque de voz.

uso: transcribe.py <video ou pasta> [...] [--out DIR] [--lang pt] [--model small] [--force]
Rode com o python do venv do projeto: .venv/bin/python -I scripts/transcribe.py ...
"""
import argparse, glob, json, os, subprocess, sys, wave
import numpy as np

VID = ('.mov', '.mp4', '.m4v', '.MOV', '.MP4', '.mkv', '.webm')


def onset(wav):
    """Primeiro ataque de voz pela envoltória RMS em janelas de 20 ms (o corte do gancho entra aqui, nunca na respiração)."""
    w = wave.open(wav); a = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(float)
    n = len(a) // 320; r = np.sqrt((a[:n * 320].reshape(n, 320) ** 2).mean(1))
    thr = max(np.percentile(r, 10) * 3, np.percentile(r, 99) * .06)
    return round(int(np.argmax(r > thr)) * .02, 2), round(len(a) / 16000, 2)


def words(wav, model, lang):
    from faster_whisper import WhisperModel
    w = wave.open(wav); x = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32) / 32768
    for dev, ct in (('cuda', 'float16'), ('cpu', 'int8')):
        try:
            segs, _ = WhisperModel(model, device=dev, compute_type=ct).transcribe(
                x, language=lang, word_timestamps=True, condition_on_previous_text=False)
            return [dict(w=t.word.strip(), s=round(t.start, 3), e=round(t.end, 3))
                    for seg in segs for t in (seg.words or []) if t.word.strip()]
        except Exception as ex:  # sem CUDA/cuBLAS: cai para CPU
            if dev == 'cpu': raise
            print(f'(GPU indisponível: {str(ex)[:60]}; usando CPU)', file=sys.stderr)


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('src', nargs='+'); ap.add_argument('--out')
    ap.add_argument('--lang', default='pt'); ap.add_argument('--model', default='small')
    ap.add_argument('--force', action='store_true'); a = ap.parse_args()
    files = []
    for s in a.src:
        s = os.path.expanduser(s)
        files += sorted(f for f in glob.glob(os.path.join(s, '*')) if f.endswith(VID)) if os.path.isdir(s) else [s]
    if not files: sys.exit('nenhum vídeo encontrado')
    for f in files:
        base = os.path.splitext(os.path.basename(f))[0]; out = os.path.expanduser(a.out) if a.out else os.path.dirname(f)
        os.makedirs(out, exist_ok=True); wav = f'{out}/{base}.wav'; js = f'{out}/{base}.words.json'
        link = os.path.join(out, os.path.basename(f))
        if os.path.realpath(os.path.dirname(f)) != os.path.realpath(out) and not os.path.lexists(link):
            os.symlink(os.path.abspath(f), link)
        if not os.path.exists(wav) or a.force:
            subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', f, '-vn', '-ac', '1', '-ar', '16000', '-c:a', 'pcm_s16le', wav], check=True)
        if not os.path.exists(js) or a.force:
            W = words(wav, a.model, a.lang)
            for i, x in enumerate(W): x['i'] = i
            json.dump(W, open(js, 'w'), ensure_ascii=False, indent=0)
        W = json.load(open(js)); on, dur = onset(wav)
        print(f'\n== {base}  ({dur} s, voz começa em {on} s, {len(W)} palavras) → {js}')
        print(' '.join(f"[{x['i']}]{x['w']}" for x in W))


if __name__ == '__main__':
    main()
