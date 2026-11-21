"""Serve the built learning site (learning/dist) for local preview.

Usage: uv run python learning/serve.py [--open]

The port comes from the PORT environment variable, so a preview tool can move it when 8765 is taken.
--open opens the site in the default browser once the server listens, so the first request can't miss it.
"""

import argparse
import functools
import http.server
import os
import webbrowser
from pathlib import Path

DIST = Path(__file__).resolve().parent / "dist"


class NoCacheHandler(http.server.SimpleHTTPRequestHandler):
    """Tells the browser to check every file again, so a rebuilt site.css shows on a normal reload."""

    def end_headers(self):
        self.send_header("Cache-Control", "no-cache")
        super().end_headers()


def main(argv=None, open_browser=webbrowser.open):
    parser = argparse.ArgumentParser(description="Serve learning/dist for local preview.")
    parser.add_argument("--open", action="store_true", help="open the site in the default browser")
    args = parser.parse_args(argv)

    port = int(os.environ.get("PORT", "8765"))
    handler = functools.partial(NoCacheHandler, directory=DIST)
    server = http.server.ThreadingHTTPServer(("127.0.0.1", port), handler)
    url = f"http://localhost:{server.server_address[1]}/"
    print(f"Serving {DIST} on {url}")
    if args.open:
        open_browser(url)
    server.serve_forever()


if __name__ == "__main__":
    main()
