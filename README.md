# Bluetech Sanitaire — site

Site of Bluetech Sanitaire Sàrl (Prilly VD), served by GitHub Pages from `docs/`.

- Edit content in `_build/build.py`, then run `python3 _build/build.py` — it regenerates every page in `docs/`.
- CSS/JS are hand-written in `docs/assets/` (GSAP, ScrollTrigger, Lenis and three.js are vendored). Bump `V` in `build.py` after editing them.
- Local preview with clean URLs: `python3 _build/serve.py 4433`.

## To confirm with the owner (placeholders)
In `_build/build.py`:
- `PHONE_DISPLAY`, `PHONE_TEL`, `WA_NUMBER` — phone and WhatsApp are placeholders (+41 XX…).
- `EMAIL` — empty; once set, the forms offer "send by e-mail" too.
- `REVIEWS` / `REVIEWS_ARE_EXAMPLES` — the Google review cards are examples; replace with real reviews and set the flag to `False`.
- `GOOGLE_REVIEWS_URL` — "Laisser un avis" button appears once set.
- `NOINDEX` — `True` keeps the site out of Google while placeholders remain.
- `TOWNS` — area served is inferred from the Prilly address.

Facts used (Registre du commerce VD, 2026-10-08): Bluetech Sanitaire Sàrl, Route de Renens 2, 1008 Prilly, IDE CHE-227.168.225, associé-gérant Ahmet Hoti, inscrite en juillet 2026. All photos are the company's own.
