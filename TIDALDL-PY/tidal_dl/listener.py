#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""HTTP listener mode that mirrors the extension bridge script."""

from __future__ import annotations

import copy
import logging
import os
import threading
import time
from dataclasses import dataclass
from typing import Optional

from flask import Flask, abort, jsonify, request

from download import downloadCover, downloadTrack
from enums import AudioQuality, Type
from events import loginByConfig
from printf import Printf
from settings import SETTINGS
from tidal import TIDAL_API

LOG = logging.getLogger(__name__)

RESET = "\x1b[0m"
BLUE = "\x1b[94m"
GREEN = "\x1b[92m"
ORANGE = "\x1b[38;5;208m"
USE_COLOR = True

_log_lock = threading.Lock()


@dataclass
class DownloadOutcome:
    success: bool
    codec: str
    title: str
    error: str = ""


def _colorize(text: Optional[str], color: str) -> str:
    if not USE_COLOR or not text:
        return (text or "").strip()
    return f"{color}{text.strip()}{RESET}"


def _get_listener_secret() -> str:
    return (SETTINGS.listenerSecret or "").strip()


def _get_log_path() -> str:
    download_dir = SETTINGS.downloadPath or "./download"
    return os.path.join(download_dir, "listener.log")


def _append_log_line(line: str) -> None:
    path = _get_log_path()
    directory = os.path.dirname(path)
    if directory:
        os.makedirs(directory, exist_ok=True)
    with _log_lock:
        with open(path, "a", encoding="utf-8") as handle:
            handle.write(line)


def _log_attempt_header(url: str, attempt: str) -> None:
    _append_log_line(f"\n[{time.strftime('%F %T')}] START ({attempt}) url={url}\n")


def _log_attempt_footer(result: DownloadOutcome) -> None:
    code = 0 if result.success else 1
    if result.error:
        _append_log_line(result.error.strip() + "\n")
    _append_log_line(f"[{time.strftime('%F %T')}] EXIT code={code}\n")


def _log_summary(codec: str, title: str, success: bool, url: str) -> None:
    code = 0 if success else 1
    codec_s = _colorize(codec or "UNKNOWN", ORANGE)
    title_s = _colorize(title or "(no title)", GREEN)
    url_s = _colorize(url or "", BLUE)
    line = f"{codec_s}  {title_s}  code={code}  url={url_s}".strip()
    LOG.info(line)


def _restore_login_state(original_key) -> None:
    """Replace the API login state with the provided snapshot."""

    if original_key is None:
        return
    TIDAL_API.key = original_key


def _download_track(url: str, bearer_token: Optional[str]) -> DownloadOutcome:
    original_key = None
    if bearer_token:
        try:
            original_key = copy.deepcopy(TIDAL_API.key)
        except Exception:  # pragma: no cover - best-effort snapshot
            original_key = None
        try:
            TIDAL_API.loginByAccessToken(bearer_token)
        except Exception as exc:
            _restore_login_state(original_key)
            return DownloadOutcome(False, "", "", f"Authorization with provided bearer token failed: {exc}")
    else:
        if not loginByConfig():
            return DownloadOutcome(False, "", "", "Authentication required. Run a login flow first.")

    try:
        etype, obj = TIDAL_API.getByString(url)
    except Exception as exc:  # pragma: no cover - defensive
        _restore_login_state(original_key)
        return DownloadOutcome(False, "", "", str(exc))

    if etype != Type.Track:
        _restore_login_state(original_key)
        return DownloadOutcome(False, "", "", "Only track URLs are supported.")

    album = None
    try:
        if obj.album and obj.album.id:
            album = TIDAL_API.getAlbum(obj.album.id)
    except Exception:
        album = None

    if album and SETTINGS.saveCovers:
        downloadCover(album)

    ok, message, stream = downloadTrack(obj, album)
    codec = ""
    if stream is not None:
        if stream.codec:
            codec = str(stream.codec).upper()
        elif stream.soundQuality:
            codec = str(stream.soundQuality).upper()
    if not codec and obj.audioQuality:
        codec = str(obj.audioQuality)

    if ok:
        _restore_login_state(original_key)
        return DownloadOutcome(True, codec, obj.title)
    _restore_login_state(original_key)
    return DownloadOutcome(False, codec, obj.title, message)


def _perform_attempt(url: str, first_try: bool, bearer_token: Optional[str]) -> DownloadOutcome:
    attempt_label = "primary" if first_try else "fallback"
    _log_attempt_header(url, attempt_label)

    original_quality = SETTINGS.audioQuality
    try:
        if not first_try and SETTINGS.audioQuality != AudioQuality.HiFi:
            SETTINGS.audioQuality = AudioQuality.HiFi
        result = _download_track(url, bearer_token)
    finally:
        SETTINGS.audioQuality = original_quality

    _log_attempt_footer(result)
    _log_summary(result.codec, result.title, result.success, url)
    return result


def _run_attempts(url: str, bearer_token: Optional[str]) -> DownloadOutcome:
    result = _perform_attempt(url, True, bearer_token)
    if result.success:
        return result
    return _perform_attempt(url, False, bearer_token)


def _auth_and_get_request() -> tuple[str, Optional[str]]:
    if request.headers.get("X-Auth") != _get_listener_secret():
        abort(403)
    data = request.get_json(force=True) or {}
    url = (data.get("url") or "").strip()
    if not url:
        abort(400, "URL is required")
    allowed_prefixes = (
        "https://tidal.com/track",
        "https://www.tidal.com/track",
        "https://tidal.com/browse/track",
        "https://www.tidal.com/browse/track",
    )
    if not url.startswith(allowed_prefixes):
        abort(400, "URL must start with https://tidal.com/track")
    bearer = (data.get("bearerAuthorization") or "").strip()
    if not bearer:
        bearer = (data.get("bearer_token") or "").strip()
    if not bearer:
        auth_header = request.headers.get("Authorization", "")
        if auth_header.lower().startswith("bearer "):
            bearer = auth_header[7:].strip()
    if bearer:
        bearer = bearer.strip()
    return url, bearer or None


def _create_app() -> Flask:
    app = Flask(__name__)

    @app.after_request
    def add_cors(resp):  # type: ignore[override]
        resp.headers["Access-Control-Allow-Origin"] = "*"
        resp.headers["Access-Control-Allow-Headers"] = "Content-Type, X-Auth, Authorization"
        resp.headers["Access-Control-Allow-Methods"] = "POST, OPTIONS"
        return resp

    @app.route("/run", methods=["OPTIONS"])
    def options():  # type: ignore[override]
        return ("", 204)

    def _async_runner(url: str, bearer_token: Optional[str]) -> None:
        try:
            _run_attempts(url, bearer_token)
        except Exception:  # pragma: no cover - defensive
            LOG.exception("Listener download failed for %s", url)

    @app.post("/run")
    def run_async():  # type: ignore[override]
        url, bearer = _auth_and_get_request()
        os.makedirs(SETTINGS.downloadPath, exist_ok=True)
        threading.Thread(target=_async_runner, args=(url, bearer), daemon=True).start()
        return jsonify(status="started")

    @app.post("/run_sync")
    def run_sync():  # type: ignore[override]
        url, bearer = _auth_and_get_request()
        os.makedirs(SETTINGS.downloadPath, exist_ok=True)

        primary = _perform_attempt(url, True, bearer)
        if primary.success:
            return jsonify(status="finished", final_code=0, codec=primary.codec, title=primary.title)

        fallback = _perform_attempt(url, False, bearer)
        code = 0 if fallback.success else 1
        return jsonify(status="finished", final_code=code, codec=fallback.codec, title=fallback.title)

    return app


def start_listener() -> None:
    if not SETTINGS.listenerEnabled:
        Printf.err("Listener mode is disabled. Enable it in settings first.")
        return

    secret = _get_listener_secret()
    if not secret:
        Printf.err("Listener secret is empty. Set a value in settings before starting listener mode.")
        return

    port = SETTINGS.listenerPort or 8123
    try:
        port = int(port)
    except (TypeError, ValueError):
        port = 8123

    Printf.info(f"Starting listener mode on 127.0.0.1:{port}")
    Printf.info("Send POST requests to /run or /run_sync with header X-Auth set to your secret.")

    app = _create_app()
    app.run(host="127.0.0.1", port=port)


__all__ = ["start_listener"]

