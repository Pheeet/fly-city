#!/usr/bin/env python3
"""Build the Fly Floor-served copy of the city: ~/hedgefly/visuals/floor/city/.

Fly Floor sends `script-src 'self'`, so the city's inline script becomes city.js and
three.js comes from a local vendor/ folder instead of the CDN. Run after editing index.html.
"""
import pathlib, re, urllib.request

SRC = pathlib.Path(__file__).with_name('index.html')
OUT = pathlib.Path.home() / 'hedgefly/visuals/floor/city'
CDN = 'https://cdn.jsdelivr.net/npm/three@0.147.0/'

html = SRC.read_text()
(OUT / 'vendor').mkdir(parents=True, exist_ok=True)

def vendor(m):
    url = m.group(1)
    name = url.rsplit('/', 1)[1]
    dest = OUT / 'vendor' / name
    if not dest.exists():
        dest.write_bytes(urllib.request.urlopen(url, timeout=30).read())
    return f'<script src="/city/vendor/{name}"></script>'

html = re.sub(r'<script src="(' + re.escape(CDN) + r'[^"]+)"></script>', vendor, html)
m = re.search(r'<script>\n(\(function\(\)\{.*?)</script>', html, re.S)
(OUT / 'city.js').write_text(m.group(1))
html = html[:m.start()] + '<script src="/city/city.js"></script>' + html[m.end():]
html = re.sub(r'<link rel="(preconnect|stylesheet)" href="https://fonts\.[^"]+"[^>]*>\n', '', html)
fonts = ('<style>@font-face{font-family:"Inter Local";src:url(/fonts/InterVariable.woff2) format("woff2");font-weight:100 900}'
         '@font-face{font-family:"Plex Mono Local";src:url(/fonts/IBMPlexMono-Regular.ttf)}'
         '@font-face{font-family:"Plex Thai Local";src:url(/fonts/IBMPlexSansThai-Regular.ttf);font-weight:400}'
         '@font-face{font-family:"Plex Thai Local";src:url(/fonts/IBMPlexSansThai-SemiBold.ttf);font-weight:500 700}'
         ':root{--font-ui:"Inter Local","Plex Thai Local",system-ui,sans-serif;--font-data:"Plex Mono Local","Plex Thai Local",ui-monospace,monospace}</style>')
html = html.replace('</style>', '</style>\n' + fonts, 1)
page = ('<!doctype html><html lang="th"><head><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">'
        '<link rel="icon" href="/favicon.svg"></head><body>\n' + html + '\n</body></html>\n')
(OUT / 'index.html').write_text(page)
print('built', OUT, sorted(p.name for p in (OUT / 'vendor').iterdir()))
