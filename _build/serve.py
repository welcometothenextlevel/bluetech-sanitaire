#!/usr/bin/env python3
"""Local preview of docs/ that resolves clean URLs (/contact -> contact.html) like GitHub Pages does."""
import http.server, os, sys
ROOT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "docs")
PREFIX = "/bluetech-sanitaire"
class H(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *a, **k): super().__init__(*a, directory=ROOT, **k)
    def translate_path(self, path):
        p = path.split("?", 1)[0].split("#", 1)[0]
        if p.startswith(PREFIX): p = p[len(PREFIX):] or "/"
        fs = super().translate_path(p)
        if not os.path.exists(fs) and os.path.exists(fs + ".html"): return fs + ".html"
        return fs
    def send_error(self, code, message=None, explain=None):
        if code == 404:
            self.send_response(404); self.send_header("Content-Type", "text/html; charset=utf-8"); self.end_headers()
            self.wfile.write(open(os.path.join(ROOT, "404.html"), "rb").read()); return
        super().send_error(code, message, explain)
    def log_message(self, *a): pass
port = int(sys.argv[1]) if len(sys.argv) > 1 else 4433
http.server.ThreadingHTTPServer(("127.0.0.1", port), H).serve_forever()
