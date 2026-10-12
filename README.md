# Fly City

An isometric Three.js city with the Fly Floor trading tower and the Fly Casino.

- **Live:** https://pheeet.github.io/fly-city/
- `index.html` is the source page. `python3 build_pages.py` writes the GitHub Pages copy to `docs/`.
- `python3 build_floor.py` writes the copy that Fly Floor serves at `:8767/city` (three.js vendored, because Fly Floor's CSP only allows same-origin scripts).
- Live fly data comes from Fly Floor's `/api/state` through a Cloudflare quick tunnel whose URL is kept in a gist (`tools/fly_tunnel.py`). These are demo/paper bots.
- Fly Floor tower: F2 FlyIndex (5 seeds), F3 FlyBTC, F4 FlyGold (H4 gold, long-only; data in `/api/state` `extras.flygold`). `#f2`/`#f3`/`#f4` in the URL opens a floor.
- In Fly Casino, two mushroom-body fly brains learn heads-up blackjack by playing each other. "เตะแล้วเล่น" (kick and play) lets you take one fly's seat.
