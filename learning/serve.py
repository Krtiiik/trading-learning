"""Serve the built learning site (learning/dist) for local preview.

The port comes from the PORT environment variable, so a preview tool can move it when 8765 is taken.
"""

import functools
import http.server
import os
from pathlib import Path

DIST = Path(__file__).resolve().parent / "dist"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", "8765"))
    handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=DIST)
    print(f"Serving {DIST} on http://localhost:{port}")
    http.server.ThreadingHTTPServer(("127.0.0.1", port), handler).serve_forever()
