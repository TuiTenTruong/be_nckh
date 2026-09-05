"""Resolve stored media paths to loadable absolute URLs."""
from __future__ import annotations

import hashlib
import os
from pathlib import Path

DEFAULT_IMAGE_URL = (
    "https://images.unsplash.com/photo-1546069901-ba9599a7e63c?w=1200"
)

_STATIC_ROOT = Path(__file__).resolve().parents[2] / "static"
_IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".gif", ".bmp", ".avif"}


def get_public_base_url() -> str:
    try:
        from flask import has_request_context, request

        if has_request_context():
            return request.host_url.rstrip("/")
    except RuntimeError:
        pass

    return os.getenv("API_PUBLIC_URL", "http://127.0.0.1:5000").rstrip("/")


def _is_absolute_image_url(url: str) -> bool:
    if not url:
        return False

    lowered = url.lower()
    if lowered.startswith("http://") or lowered.startswith("https://"):
        if "source.unsplash.com" in lowered:
            return False
        if any(
            host in lowered
            for host in (
                "images.unsplash.com",
                "picsum.photos",
                "dummyimage.com",
            )
        ):
            return True
        path = lowered.split("?", 1)[0]
        return any(path.endswith(ext) for ext in _IMAGE_EXTENSIONS)

    return False


def _placeholder_url(label: str) -> str:
    text = (label or "Mon an").strip() or "Mon an"
    seed = hashlib.sha1(text.encode("utf-8")).hexdigest()[:12]
    return f"https://picsum.photos/seed/{seed}/1200/800"


def resolve_image_url(
    raw_url: str | None,
    *,
    name: str = "",
    public_base: str | None = None,
) -> str:
    """
    Turn DB paths like ``images/foo.jpg`` into a browser-loadable URL.

    Priority:
    1. Already absolute http(s) image URL
    2. Existing file under ``be_nckh/static/`` → ``{base}/static/...``
    3. Name-based placeholder (Option A when assets are missing)
    """
    raw = (raw_url or "").strip()
    base = (public_base or get_public_base_url()).rstrip("/")

    if _is_absolute_image_url(raw):
        return raw

    if raw:
        normalized = raw.replace("\\", "/").lstrip("/")
        if normalized.startswith("static/"):
            normalized = normalized[len("static/") :]

        file_path = _STATIC_ROOT / normalized
        if file_path.is_file():
            return f"{base}/static/{normalized}"

        if normalized.startswith("images/"):
            return _placeholder_url(name or normalized.rsplit("/", 1)[-1])

    if name.strip():
        return _placeholder_url(name)

    return DEFAULT_IMAGE_URL
