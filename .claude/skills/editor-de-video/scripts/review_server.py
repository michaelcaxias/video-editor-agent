#!/usr/bin/env python3
"""Servidor local de revisão: player com comentários por timestamp. Só escuta em 127.0.0.1.

uso (da raiz do projeto de vídeo, ex. editor-de-video/):  python3 review_server.py [--port 8765] [--dir .]
Abre http://127.0.0.1:8765 . Os vídeos vêm de exportacao/*.mp4 (e work/*.mp4); os comentários ficam em
revisao/comentarios_<arquivo>.json (o Claude lê esse arquivo e aplica os ajustes).
Suporta Range (seek rápido) e só serve arquivos dentro de --dir.
"""
import argparse, json, mimetypes, os, re, sys, threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, unquote, urlparse

HERE = os.path.dirname(os.path.abspath(__file__))
LOCK = threading.Lock()


def make_handler(base):
    base = os.path.realpath(base)
    rev = os.path.join(base, 'revisao')
    os.makedirs(rev, exist_ok=True)

    def inside(p):
        rp = os.path.realpath(p)
        return rp == base or rp.startswith(base + os.sep)

    def cfile(video):
        name = re.sub(r'[^A-Za-z0-9._-]', '_', os.path.basename(video))
        return os.path.join(rev, f'comentarios_{name}.json')

    class H(BaseHTTPRequestHandler):
        server_version = 'review/1.0'

        def log_message(self, *a):  # silencioso
            pass

        def _json(self, obj, code=200):
            b = json.dumps(obj, ensure_ascii=False, indent=1).encode()
            self.send_response(code); self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.send_header('Content-Length', str(len(b))); self.send_header('Cache-Control', 'no-store'); self.end_headers()
            self.wfile.write(b)

        def _file(self, path, ctype=None, trusted=False):
            if not os.path.isfile(path) or not (trusted or inside(path)):
                self.send_error(404); return
            size = os.path.getsize(path)
            ctype = ctype or mimetypes.guess_type(path)[0] or 'application/octet-stream'
            rng = self.headers.get('Range')
            start, end, code = 0, size - 1, 200
            if rng:
                m = re.match(r'bytes=(\d*)-(\d*)', rng)
                if m:
                    if m.group(1): start = int(m.group(1))
                    if m.group(2): end = int(m.group(2))
                    if not m.group(1) and m.group(2): start, end = max(0, size - int(m.group(2))), size - 1
                    end = min(end, size - 1); code = 206
            self.send_response(code)
            self.send_header('Content-Type', ctype); self.send_header('Accept-Ranges', 'bytes')
            self.send_header('Content-Length', str(end - start + 1)); self.send_header('Cache-Control', 'no-store')
            if code == 206: self.send_header('Content-Range', f'bytes {start}-{end}/{size}')
            self.end_headers()
            try:
                with open(path, 'rb') as f:
                    f.seek(start); left = end - start + 1
                    while left > 0:
                        chunk = f.read(min(65536, left))
                        if not chunk: break
                        self.wfile.write(chunk); left -= len(chunk)
            except (BrokenPipeError, ConnectionResetError):
                pass

        def do_GET(self):
            u = urlparse(self.path); q = parse_qs(u.query)
            if u.path in ('/', '/index.html'):
                return self._file(os.path.join(HERE, '..', 'templates', 'review.html'), 'text/html; charset=utf-8', trusted=True)
            if u.path == '/api/videos':
                out = []
                for d in ('exportacao', 'work'):  # só o nível de cada pasta (sem subpastas de intermediários)
                    dd = os.path.join(base, d)
                    for fn in sorted(os.listdir(dd)) if os.path.isdir(dd) else []:
                        full = os.path.join(dd, fn)
                        if fn.endswith('.mp4') and not fn.startswith('.') and os.path.isfile(full):
                            out.append(dict(path=os.path.relpath(full, base), size=os.path.getsize(full), mtime=os.path.getmtime(full)))
                out.sort(key=lambda x: -x['mtime'])
                return self._json(out)
            if u.path == '/api/comments':
                v = q.get('video', [''])[0]
                p = cfile(v)
                with LOCK:
                    data = json.load(open(p)) if os.path.exists(p) else []
                return self._json(data)
            if u.path.startswith('/media/'):
                return self._file(os.path.join(base, unquote(u.path[len('/media/'):])))
            self.send_error(404)

        def do_POST(self):
            u = urlparse(self.path)
            n = int(self.headers.get('Content-Length', 0))
            try:
                body = json.loads(self.rfile.read(n) or b'{}')
            except Exception:
                return self._json({'error': 'json inválido'}, 400)
            if u.path == '/api/comments':  # grava a lista inteira (a página mantém o estado)
                v = body.get('video', ''); items = body.get('items', [])
                if not isinstance(items, list): return self._json({'error': 'items'}, 400)
                with LOCK:
                    json.dump(items, open(cfile(v), 'w'), ensure_ascii=False, indent=1)
                return self._json({'ok': True, 'n': len(items)})
            self.send_error(404)

    return H


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--port', type=int, default=8765); ap.add_argument('--dir', default='.')
    a = ap.parse_args()
    srv = ThreadingHTTPServer(('127.0.0.1', a.port), make_handler(a.dir))
    print(f'Revisão em http://127.0.0.1:{a.port}  (dir: {os.path.realpath(a.dir)})  Ctrl+C para sair', flush=True)
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    main()
