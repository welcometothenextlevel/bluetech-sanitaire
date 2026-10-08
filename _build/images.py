#!/usr/bin/env python3
"""One-off: turns the client's photos in _src/ into webp+jpg in docs/assets/img/work."""
import os
from PIL import Image, ImageOps
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "_src")
OUT = os.path.join(ROOT, "docs", "assets", "img", "work")
MAP = {
    "WhatsApp Image 2026-10-04 at 5.29.53 PM (1).jpeg": "gaine-collecteurs",
    "WhatsApp Image 2026-10-04 at 5.29.53 PM.jpeg": "double-bati-ventilation",
    "WhatsApp Image 2026-10-04 at 5.29.54 PM (1).jpeg": "mur-brique-geberit",
    "WhatsApp Image 2026-10-04 at 5.29.54 PM (2).jpeg": "colonne-chute",
    "WhatsApp Image 2026-10-04 at 5.29.54 PM (3).jpeg": "salle-de-bains-sauge",
    "WhatsApp Image 2026-10-04 at 5.29.54 PM (4).jpeg": "evacuations-controlees",
    "WhatsApp Image 2026-10-04 at 5.29.54 PM.jpeg": "salle-de-bains-gros-oeuvre",
    "WhatsApp Image 2026-10-04 at 6.12.14 PM.jpeg": "wc-douche-collecteur",
    "WhatsApp Image 2026-10-04 at 6.12.15 PM (1).jpeg": "bati-lavabo",
    "WhatsApp Image 2026-10-04 at 6.12.15 PM.jpeg": "wc-bain-ventilation",
}
os.makedirs(OUT, exist_ok=True)
for src, name in MAP.items():
    im = ImageOps.exif_transpose(Image.open(os.path.join(SRC, src))).convert("RGB")
    for w, suf in ((1500, ""), (760, "-s")):
        c = im.copy(); c.thumbnail((w, w * 2), Image.LANCZOS)
        base = os.path.join(OUT, name + suf)
        c.save(base + ".jpg", "JPEG", quality=74, optimize=True, progressive=True)
        c.save(base + ".webp", "WEBP", quality=70, method=6)
        print(name + suf, c.size, os.path.getsize(base + ".webp") // 1024, "KB webp", os.path.getsize(base + ".jpg") // 1024, "KB jpg")
