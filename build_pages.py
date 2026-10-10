#!/usr/bin/env python3
"""Build the GitHub Pages copy of Fly City into docs/ (full HTML document, three.js from the CDN)."""
import pathlib
SRC = pathlib.Path(__file__).with_name('index.html')
OUT = SRC.with_name('docs')
OUT.mkdir(exist_ok=True)
page = ('<!doctype html><html lang="th"><head><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">'
        '<style>:root{padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}'
        'body{margin:0;font:14px system-ui,sans-serif}img{max-width:100%}[hidden]{display:none!important}</style>'
        '</head><body>\n' + SRC.read_text() + '\n</body></html>\n')
(OUT / 'index.html').write_text(page)
(OUT / '.nojekyll').write_text('')
print('built', OUT / 'index.html')
