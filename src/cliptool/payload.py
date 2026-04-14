from __future__ import annotations

from .utils import to_abs_path, to_uri


def make_text_payload(path_str: str) -> bytes:
    with open(to_abs_path(path_str), "rb") as f:
        return f.read()


def make_path_payload(path_str: str) -> bytes:
    return to_abs_path(path_str).encode("utf-8")


def make_uri_list_payload(path_str: str) -> bytes:
    # text/uri-list conventionally uses CRLF
    return (to_uri(path_str) + "\r\n").encode("utf-8")


def make_gnome_copied_files_payload(path_str: str, action: str = "copy") -> bytes:
    # Common GNOME/Nautilus-style payload
    # Example:
    # copy
    # file:///abs/path
    return f"{action}\n{to_uri(path_str)}\n".encode("utf-8")