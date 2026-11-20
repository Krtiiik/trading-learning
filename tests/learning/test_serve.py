import importlib.util
import socket
import sys
from pathlib import Path

import pytest

LEARNING = Path(__file__).resolve().parents[2] / "learning"
_spec = importlib.util.spec_from_file_location("learning_serve", LEARNING / "serve.py")
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
