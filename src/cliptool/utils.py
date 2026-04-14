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