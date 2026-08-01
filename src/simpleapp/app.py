"""Simple Flask API for testing."""

from __future__ import annotations

import os
import platform
import socket
import time
import uuid
from datetime import datetime, timezone

from flask import Flask, jsonify, request

app = Flask(__name__)

_ITEMS: dict[str, dict] = {}


def _version() -> str:
    return os.environ.get("APP_VERSION", "0.2.0")


@app.get("/")
def welcome():
    """Original simpleapp welcome page."""
    return (
        "<!doctype html>"
        "<html><head><title>simpleapp</title></head>"
        "<body style='font-family: system-ui; margin: 2rem; line-height: 1.5;'>"
        "<h1>Welcome!</h1>"
        "<p>simpleapp on Kind via Argo CD (Poetry).</p>"
        f"<p>Pod: <code>{socket.gethostname()}</code> · v{_version()}</p>"
        "<h2>Try</h2>"
        "<ul>"
        "<li><a href='/api/host'>/api/host</a> · <a href='/api/info'>/api/info</a></li>"
        "<li><a href='/healthz'>/healthz</a> · <a href='/readyz'>/readyz</a></li>"
        "<li><a href='/api/echo?msg=hello'>/api/echo?msg=hello</a></li>"
        "<li><a href='/api/time'>/api/time</a></li>"
        "<li><a href='/api/headers'>/api/headers</a></li>"
        "<li><a href='/api/items'>/api/items</a></li>"
        "<li><a href='/api/status/418'>/api/status/418</a></li>"
        "<li><a href='/api/slow?seconds=1'>/api/slow?seconds=1</a></li>"
        "</ul>"
        "</body></html>"
    )


@app.get("/healthz")
def healthz():
    return jsonify(status="ok")


@app.get("/readyz")
def readyz():
    return jsonify(status="ready", hostname=socket.gethostname())



@app.get("/api/info")
def api_info():
    return jsonify(
        app="simpleapp",
        version=_version(),
        hostname=socket.gethostname(),
        os=platform.system(),
        architecture=platform.machine(),
        python=platform.python_version(),
     )


@app.get("/api/echo")
def api_echo_get():
    msg = request.args.get("msg", "")
    return jsonify(echo=msg, method="GET", length=len(msg))


@app.post("/api/echo")
def api_echo_post():
    payload = request.get_json(silent=True)
    if payload is None:
        payload = {"raw": request.get_data(as_text=True)}
    return jsonify(echo=payload, method="POST"), 201


@app.get("/api/headers")
def api_headers():
    return jsonify(headers={k: v for k, v in request.headers.items()})


@app.get("/api/time")
def api_time():
    now = datetime.now(timezone.utc)
    return jsonify(
        utc=now.isoformat(),
        unix=now.timestamp(),
        hostname=socket.gethostname(),
    )


@app.get("/api/env")
def api_env():
    keys = ("APP_VERSION", "PORT", "HOSTNAME", "KUBERNETES_SERVICE_HOST")
    return jsonify(env={k: os.environ.get(k) for k in keys})


@app.get("/api/status/<int:code>")
def api_status(code: int):
    if code < 100 or code > 599:
        return jsonify(error="status code must be 100-599"), 400
    return jsonify(requested_status=code, ok=code < 400), code


@app.get("/api/slow")
def api_slow():
    seconds = request.args.get("seconds", default=1.0, type=float)
    seconds = max(0.0, min(seconds, 10.0))
    time.sleep(seconds)
    return jsonify(slept_seconds=seconds)

def main() -> None:
    port = int(os.environ.get("PORT", "8080"))
    app.run(host="0.0.0.0", port=port)


if __name__ == "__main__":
    main()
