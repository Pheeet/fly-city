# Fly City

An isometric Three.js city with the Fly Floor trading tower and the Fly Casino.

- **Live:** https://pheeet.github.io/fly-city/
- `index.html` is the source page. `python3 build_pages.py` writes the GitHub Pages copy to `docs/`.
- `python3 build_floor.py` writes the copy that Fly Floor serves at `:8767/city` (three.js vendored, because Fly Floor's CSP only allows same-origin scripts).
- Live fly data comes from Fly Floor's `/api/state` through Tailscale Funnel (`https://diamondserver.tail23260b.ts.net/api/state`). These are demo/paper bots.
- In Fly Casino, two mushroom-body fly brains learn heads-up blackjack by playing each other. "เตะแล้วเล่น" (kick and play) lets you take one fly's seat.
