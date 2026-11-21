import importlib.util
import socket
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
_spec = importlib.util.spec_from_file_location("learning_serve", ROOT / "scripts" / "serve.py")
serve = importlib.util.module_from_spec(_spec)
sys.modules["learning_serve"] = serve
_spec.loader.exec_module(serve)


class StopServing(Exception):
    pass


def run_main(monkeypatch, argv):
    """Run serve.main on a free port; stop where it would start serving and return the opened URLs."""
    monkeypatch.setenv("PORT", "0")
    opened = []

    def opener(url):
        port = int(url.rsplit(":", 1)[1].rstrip("/"))
        with socket.create_connection(("127.0.0.1", port), timeout=2):
            pass  # the server must already listen when the browser opens
        opened.append(url)

    def stop(self):
        self.server_close()
        raise StopServing

    monkeypatch.setattr(serve.http.server.ThreadingHTTPServer, "serve_forever", stop)
    with pytest.raises(StopServing):
        serve.main(argv, open_browser=opener)
    return opened


def test_open_flag_opens_the_site_once_the_server_listens(monkeypatch):
    opened = run_main(monkeypatch, ["--open"])
    assert len(opened) == 1
    assert opened[0].startswith("http://localhost:")


def test_without_open_flag_no_browser_opens(monkeypatch):
    assert run_main(monkeypatch, []) == []


def test_files_are_served_with_no_cache_so_a_rebuild_shows_on_reload(tmp_path):
    import functools
    import threading
    import urllib.request

    (tmp_path / "site.css").write_text("body{}", encoding="utf-8")
    handler = functools.partial(serve.NoCacheHandler, directory=tmp_path)
    server = serve.http.server.ThreadingHTTPServer(("127.0.0.1", 0), handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        url = f"http://127.0.0.1:{server.server_address[1]}/site.css"
        with urllib.request.urlopen(url, timeout=2) as response:
            assert response.headers["Cache-Control"] == "no-cache"
            assert response.read() == b"body{}"
    finally:
        server.shutdown()
        server.server_close()
