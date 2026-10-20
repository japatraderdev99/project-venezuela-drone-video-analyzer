#!/usr/bin/env python3
"""Venezuela · revisão local dos vídeos (só Python 3.8+, sem dependências, só nesta máquina: 127.0.0.1:8765).

Serve a interface (app/), os vídeos da pasta VIDEOS/ (com Range, para pular no tempo) e grava os comentários em comentarios/:
  COMENTARIOS.json   estado atual (a interface lê e grava aqui)
  COMENTARIOS.txt    o mesmo em texto, por versão e tempo
  historico.jsonl    toda operação (criar, editar, resolver, apagar), nunca é reescrito
Na primeira vez (e a cada git pull com comentários novos em app/seed/), os comentários de app/seed/*.json entram uma única vez.

Uso:  python3 servidor.py              abre a revisão no navegador
      python3 servidor.py --checar     só lista os vídeos encontrados e sai
      python3 servidor.py --porta 8770 usa outra porta (padrão 8765)
"""
import json, os, re, socket, subprocess, sys, threading, time, webbrowser
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler

ROOT = os.path.dirname(os.path.abspath(__file__))
APP, CD = (os.path.join(ROOT, n) for n in ('app', 'comentarios'))
# pasta dos vídeos: VIDEOS/ (a antiga videos/ também vale)
VIDS = next((os.path.join(ROOT, n) for n in ('VIDEOS', 'videos') if os.path.isdir(os.path.join(ROOT, n))), os.path.join(ROOT, 'VIDEOS'))
DB, TXT, LOG = (os.path.join(CD, n) for n in ('COMENTARIOS.json', 'COMENTARIOS.txt', 'historico.jsonl'))
PORT = int(sys.argv[sys.argv.index('--porta') + 1]) if '--porta' in sys.argv else 8765
URL = f'http://127.0.0.1:{PORT}/'
SEED = os.path.join(APP, 'seed')
VERSIONS = ('v042', 'v043', 'v044')
EXTS = ('.mp4', '.m4v', '.mov')
MAX_BODY = 2_000_000
lock = threading.Lock()


def find_videos():
    """Para cada versão, o arquivo de vídeo em VIDEOS/ que tem 'v042', 'v043' ou 'v044' no nome (o maior, se houver mais de um)."""
    files = [f for f in os.listdir(VIDS) if f.lower().endswith(EXTS) and not f.startswith('.')] if os.path.isdir(VIDS) else []
    out = {}
    for v in VERSIONS:
        c = [f for f in files if v in f.lower()]
        out[v] = max(c, key=lambda f: os.path.getsize(os.path.join(VIDS, f))) if c else None
    return out


def load():
    try:
        return json.load(open(DB, encoding='utf-8'))
    except FileNotFoundError:
        return []


def tc(t):
    f = round(t * 30); s, f = divmod(f, 30)
    return f"{s // 3600}:{s % 3600 // 60:02d}:{s % 60:02d}.{f:02d}"


def save(items):
    tmp = DB + '.tmp'
    json.dump(items, open(tmp, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    os.replace(tmp, DB)
    out = [f"VENEZUELA — COMENTÁRIOS DE REVISÃO · atualizado {time.strftime('%d/%m/%Y %H:%M')}",
           "Tempo = tempo do vídeo exportado (H:MM:SS.quadro, 30 fps). [ ] aberto · [x] resolvido", ""]
    for ver in sorted({c['ver'] for c in items}):
        cs = sorted((c for c in items if c['ver'] == ver), key=lambda c: c['t'])
        out.append(f"== {ver} · {len(cs)} comentários ({sum(bool(c.get('done')) for c in cs)} resolvidos) ==")
        for c in cs:
            ctx = ' · '.join(x for x in (c.get('place', ''), f"slot {c['slot']}" if c.get('slot') else '') if x)
            out.append(f"[{'x' if c.get('done') else ' '}] {tc(c['t'])}  {ctx}")
            out += ['      ' + ln for ln in c['text'].splitlines()]
            out.append(f"      — {c.get('who') or '?'}, {str(c.get('created', ''))[:16].replace('T', ' ')}  (id {c['id']})")
        out.append('')
    tmp = TXT + '.tmp'
    open(tmp, 'w', encoding='utf-8').write('\n'.join(out))
    os.replace(tmp, TXT)


def valid(it):
    return (isinstance(it, dict) and isinstance(it.get('id'), str) and 0 < len(it['id']) <= 64
            and it.get('ver') in VERSIONS and isinstance(it.get('t'), (int, float))
            and isinstance(it.get('text'), str) and len(it['text']) <= 10_000)


def seed():
    """Comentários de app/seed/ entram uma vez só (os ids já semeados ficam em comentarios/semeados.json),
    então apagar um deles aqui não faz ele voltar no próximo início."""
    if not os.path.isdir(SEED):
        return 0
    done_p = os.path.join(CD, 'semeados.json')
    try:
        done = set(json.load(open(done_p, encoding='utf-8')))
    except (FileNotFoundError, ValueError):
        done = set()
    items = load()
    have = {c['id'] for c in items}
    n = 0
    for f in sorted(os.listdir(SEED)):
        if not f.endswith('.json'):
            continue
        j = json.load(open(os.path.join(SEED, f), encoding='utf-8'))
        for c in (j.get('itens') if isinstance(j, dict) else j) or []:
            if valid(c) and c['id'] not in done:
                done.add(c['id'])
                if c['id'] not in have:
                    items.append(c); n += 1
    if n:
        save(items)
    json.dump(sorted(done), open(done_p, 'w', encoding='utf-8'))
    return n


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *a, **k):
        super().__init__(*a, directory=APP, **k)

    def log_message(self, format, *args):
        pass

    def send_json(self, obj, code=200):
        b = json.dumps(obj, ensure_ascii=False).encode()
        self.send_response(code)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Content-Length', str(len(b)))
        self.send_header('Cache-Control', 'no-store')
        self.end_headers()
        self.wfile.write(b)

    def do_GET(self):
        if self.path.startswith('/api/comentarios'):
            return self.send_json({'items': load()})
        if self.path.startswith('/api/videos'):
            return self.send_json(find_videos())
        m = re.match(r'^/video/(v04\d)$', self.path)
        if m:
            return self.send_video(m.group(1))
        return super().do_GET()

    def do_POST(self):
        if self.path != '/api/comentarios':
            return self.send_error(404)
        n = int(self.headers.get('Content-Length', 0))
        if n > MAX_BODY:
            return self.send_json({'ok': False, 'erro': 'grande demais'}, 413)
        try:
            op = json.loads(self.rfile.read(n) or b'{}')
        except ValueError:
            return self.send_json({'ok': False, 'erro': 'JSON inválido'}, 400)
        it = op.get('item') or {}
        if op.get('op') not in ('add', 'update', 'delete') or not isinstance(it.get('id'), str) or (op['op'] != 'delete' and not valid(it)):
            return self.send_json({'ok': False, 'erro': 'operação inválida'}, 400)
        with lock:
            items = [c for c in load() if c['id'] != it['id']]
            if op['op'] != 'delete':
                items.append(it)
            save(items)
            with open(LOG, 'a', encoding='utf-8') as f:
                f.write(json.dumps(dict(op=op['op'], at=time.strftime('%Y-%m-%dT%H:%M:%S'), item=it), ensure_ascii=False) + '\n')
        self.send_json({'ok': True, 'items': items})

    def send_video(self, ver):
        name = find_videos().get(ver)
        if not name:
            return self.send_error(404, 'video nao encontrado em VIDEOS/')
        path = os.path.join(VIDS, name)
        size = os.path.getsize(path)
        start, end = 0, size - 1
        m = re.match(r'bytes=(\d*)-(\d*)', self.headers.get('Range') or '')
        if m and (m.group(1) or m.group(2)):
            if m.group(1):
                start = int(m.group(1))
                end = min(int(m.group(2)) if m.group(2) else size - 1, size - 1)
            else:
                start = max(0, size - int(m.group(2)))
            if start > end:
                self.send_response(416); self.send_header('Content-Range', f'bytes */{size}'); self.end_headers(); return
            self.send_response(206)
            self.send_header('Content-Range', f'bytes {start}-{end}/{size}')
        else:
            self.send_response(200)
        ctype = 'video/quicktime' if name.lower().endswith('.mov') else 'video/mp4'
        self.send_header('Content-Type', ctype)
        self.send_header('Accept-Ranges', 'bytes')
        self.send_header('Content-Length', str(end - start + 1))
        self.end_headers()
        with open(path, 'rb') as f:
            f.seek(start)
            left = end - start + 1
            while left > 0:
                b = f.read(min(1 << 20, left))
                if not b:
                    break
                try:
                    self.wfile.write(b)
                except (BrokenPipeError, ConnectionResetError):
                    return
                left -= len(b)


def open_browser():
    if sys.platform == 'darwin' and subprocess.run(['open', '-a', 'Google Chrome', URL], capture_output=True).returncode == 0:
        return
    webbrowser.open(URL)


def report():
    vids = find_videos()
    print('Vídeos em VIDEOS/:')
    for v, f in vids.items():
        print(f'  {v}: ' + (f'{f}  ({os.path.getsize(os.path.join(VIDS, f)) / 1e9:.1f} GB)' if f else 'não encontrado'))
    return vids


if __name__ == '__main__':
    if sys.version_info < (3, 8):
        sys.exit('Precisa de Python 3.8 ou mais novo.')
    vids = report()
    if '--checar' in sys.argv:
        sys.exit(0 if any(vids.values()) else 1)
    os.makedirs(CD, exist_ok=True)
    if not os.path.exists(TXT):
        save(load())
    n = seed()
    if n:
        print(f'{n} comentários iniciais carregados de app/seed/.')
    s = socket.socket()
    if s.connect_ex(('127.0.0.1', PORT)) == 0:
        print('A revisão já estava aberta.'); open_browser(); sys.exit(0)
    s.close()
    srv = ThreadingHTTPServer(('127.0.0.1', PORT), Handler)
    print(f'\nRevisão aberta em {URL}\nComentários gravados em {CD}\nDeixe esta janela aberta enquanto revisa (feche ou Ctrl+C para encerrar).')
    if '--sem-navegador' not in sys.argv:
        threading.Timer(0.6, open_browser).start()
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        pass
