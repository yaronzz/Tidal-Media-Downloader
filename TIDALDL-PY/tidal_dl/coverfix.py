#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
Utilities for normalising embedded FLAC cover artwork so that players
which rely on baseline JPEG front covers (e.g. Rekordbox) can correctly
recognise the album art.
"""
from __future__ import annotations

import logging
import re
import shutil
import subprocess
import tempfile
from pathlib import Path
from typing import Iterable

__all__ = ["ensure_flac_cover_art"]

_RE_TYPE3 = re.compile(r"^\s*type:\s+3\b", re.M)
_COVER_CANDIDATES = [
    "cover.jpg", "folder.jpg", "front.jpg",
    "Cover.jpg", "Folder.jpg", "Front.jpg",
    "cover.jpeg", "folder.jpeg", "front.jpeg",
    "cover.png", "folder.png", "front.png",
]

_DEPENDENCIES_AVAILABLE: bool | None = None


def _dependencies_ready() -> bool:
    """Return True when both metaflac and ffmpeg are available."""
    global _DEPENDENCIES_AVAILABLE
    if _DEPENDENCIES_AVAILABLE is None:
        _DEPENDENCIES_AVAILABLE = all(
            shutil.which(tool) is not None for tool in ("metaflac", "ffmpeg")
        )
        if not _DEPENDENCIES_AVAILABLE:
            logging.debug(
                "Skipping FLAC cover normalisation because 'metaflac' or 'ffmpeg' is missing."
            )
    return bool(_DEPENDENCIES_AVAILABLE)


def _run(cmd: Iterable[str], *, check: bool = True, capture: bool = True):
    return subprocess.run(
        list(cmd),
        check=check,
        stdout=subprocess.PIPE if capture else None,
        stderr=subprocess.PIPE if capture else None,
        text=True,
    )


def _is_already_good(flac_path: Path, max_px: int) -> bool:
    """Check if the FLAC already contains a baseline front cover image."""
    try:
        out = _run(["metaflac", "--list", "--block-type=PICTURE", str(flac_path)]).stdout
    except subprocess.CalledProcessError:
        return False

    blocks = out.split("METADATA_BLOCK_PICTURE")
    if len(blocks) != 2:
        return False

    block = blocks[1].splitlines()
    if not any("type:" in line and " 3 " in line for line in block):
        return False

    mime = next(
        (
            line.split(":", 1)[1].strip().lower()
            for line in block
            if line.strip().startswith("mime type:")
        ),
        "",
    )
    if mime != "image/jpeg":
        return False

    try:
        width_line = next(
            line for line in block if line.strip().startswith("width:")
        ).split()
        width = int(width_line[1][:-2])
        height = int(width_line[3][:-2])
    except (StopIteration, ValueError, IndexError):
        return False

    return max(width, height) <= max_px


def _has_metaflac_front_cover(flac_path: Path) -> bool:
    try:
        out = _run(["metaflac", "--list", "--block-type=PICTURE", str(flac_path)]).stdout
    except subprocess.CalledProcessError:
        return False
    return bool(_RE_TYPE3.search(out))


def _export_existing_picture(flac_path: Path, dest_file: Path) -> bool:
    try:
        _run(["metaflac", f"--export-picture-to={dest_file}", str(flac_path)])
    except subprocess.CalledProcessError:
        return False
    return dest_file.exists() and dest_file.stat().st_size > 0


def _find_folder_cover(start_dir: Path) -> Path | None:
    for name in _COVER_CANDIDATES:
        candidate = start_dir / name
        if candidate.exists() and candidate.is_file() and candidate.stat().st_size > 0:
            return candidate
    return None


def _reencode_to_baseline_jpeg(src_img: Path, out_jpg: Path, max_px: int) -> bool:
    scale = "scale='min({0},iw)':'min({0},ih)':force_original_aspect_ratio=decrease".format(max_px)
    cmd = [
        "ffmpeg", "-y", "-v", "error", "-i", str(src_img),
        "-vf", scale, "-q:v", "3", "-pix_fmt", "yuvj420p", str(out_jpg),
    ]
    try:
        _run(cmd)
    except subprocess.CalledProcessError:
        return False
    return out_jpg.exists() and out_jpg.stat().st_size > 0


def _import_front_cover(flac_path: Path, jpg_file: Path) -> None:
    _run(["metaflac", "--remove", "--block-type=PICTURE", str(flac_path)], capture=False)
    _run(["metaflac", f"--import-picture-from=3|image/jpeg|||{jpg_file}", str(flac_path)], capture=False)


def ensure_flac_cover_art(flac_path: str | Path, *, max_px: int = 1400) -> bool:
    """Ensure the FLAC file contains a baseline JPEG front cover."""
    path = Path(flac_path)
    if path.suffix.lower() != ".flac" or not path.exists():
        return False

    if not _dependencies_ready():
        return False

    try:
        if _is_already_good(path, max_px):
            return True
        if _has_metaflac_front_cover(path):
            return True

        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            extracted = tmp_path / "extracted_art"
            baseline = tmp_path / "cover.jpg"

            have_art = _export_existing_picture(path, extracted)
            if not have_art:
                folder_cover = _find_folder_cover(path.parent)
                if folder_cover:
                    extracted = folder_cover
                    have_art = True

            if not have_art:
                logging.debug("No cover art found for %s", path)
                return False

            if not _reencode_to_baseline_jpeg(extracted, baseline, max_px):
                logging.debug("Failed to re-encode cover art for %s", path)
                return False

            _import_front_cover(path, baseline)
            return True
    except FileNotFoundError:
        return False
    except Exception:
        logging.debug("Failed to normalise cover art for %s", path, exc_info=True)
        return False

    return False
