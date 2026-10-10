#!/usr/bin/env python3
"""Public live-data bridge for Fly City on GitHub Pages.

- A tiny proxy on 127.0.0.1:8769 that serves only GET /api/state (copied from Fly Floor :8767),
  with CORS for https://pheeet.github.io. Every other path is 404.
- A Cloudflare quick tunnel to that proxy. The tunnel URL changes on every start, so the
  current URL is written to a public gist that the page reads (GIST_ID, file fly-city-api.json).
"""
import json, os, re, subprocess, sys, threading, time, urllib.request
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

UPSTREAM = 'http://127.0.0.1:8767/api/state'
PORT = 8769
ORIGIN = 'https://pheeet.github.io'
GIST_ID = os.environ.get('FLY_GIST_ID', '')
GH = os.path.expanduser('~/.local/bin/gh')
CLOUDFLARED = os.path.expanduser('~/.local/bin/cloudflared')


class Proxy(BaseHTTPRequestHandler):
    def _send(self, code, body, ctype='application/json'):
        self.send_response(code)
        self.send_header('Content-Type', ctype)
        self.send_header('Content-Length', str(len(body)))
        self.send_header('Cache-Control', 'no-store')
        self.send_header('Access-Control-Allow-Origin', ORIGIN)
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path.split('?')[0] != '/api/state':
            return self._send(404, b'{"error":"not found"}')
        try:
            with urllib.request.urlopen(UPSTREAM, timeout=12) as r:
                self._send(200, r.read())
        except Exception:
            self._send(503, b'{"error":"Fly Floor unavailable"}')

    def log_message(self, *_):
        pass


def publish(url):
    if not GIST_ID:
        print('no FLY_GIST_ID; tunnel url', url, flush=True)
        return
    body = json.dumps({'files': {'fly-city-api.json': {'content': json.dumps({'url': url, 'updated': int(time.time())})}}})
    subprocess.run([GH, 'api', '-X', 'PATCH', f'gists/{GIST_ID}', '--input', '-'], input=body.encode(), check=False,
                   stdout=subprocess.DEVNULL)
    print('published', url, flush=True)


def main():
    server = ThreadingHTTPServer(('127.0.0.1', PORT), Proxy)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    proc = subprocess.Popen([CLOUDFLARED, 'tunnel', '--no-autoupdate', '--url', f'http://127.0.0.1:{PORT}'],
                            stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    for line in proc.stdout:
        m = re.search(r'https://[a-z0-9-]+\.trycloudflare\.com', line)
        if m:
            publish(m.group(0))
    sys.exit(proc.wait() or 1)


if __name__ == '__main__':
    main()
