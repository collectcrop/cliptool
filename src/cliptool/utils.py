from __future__ import annotations

from pathlib import Path


def resolve_path(path_str: str) -> Path:
    path = Path(path_str).expanduser().resolve()
    if not path.exists():
        raise FileNotFoundError(f"Path does not exist: {path}")
    return path


def to_uri(path_str: str) -> str:
    return resolve_path(path_str).as_uri()


def to_abs_path(path_str: str) -> str:
    return str(resolve_path(path_str))

def guess_image_target(path_str: str) -> str:
    path = resolve_path(path_str)
    suffix = path.suffix.lower()

    mapping = {
        ".png": "image/png",
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".gif": "image/gif",
        ".bmp": "image/bmp",
        ".webp": "image/webp",
        ".svg": "image/svg+xml",
    }

    if suffix not in mapping:
        raise ValueError(
            f"Unsupported image type: {suffix}. "
            "Supported: png, jpg, jpeg, gif, bmp, webp, svg"
        )
    return mapping[suffix]