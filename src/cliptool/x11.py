from __future__ import annotations

import shutil
import subprocess


class XClipError(RuntimeError):
    pass


def ensure_xclip() -> None:
    if shutil.which("xclip") is None:
        raise XClipError("xclip not found in PATH. Please install xclip first.")


def copy_to_clipboard(data: bytes, target: str | None = None) -> None:
    ensure_xclip()
    cmd = ["xclip", "-selection", "clipboard", "-in"]
    if target:
        cmd += ["-t", target]

    try:
        subprocess.run(cmd, input=data, check=True)
    except subprocess.CalledProcessError as e:
        raise XClipError(f"xclip failed: {e}") from e


def read_targets() -> str:
    ensure_xclip()
    cmd = ["xclip", "-selection", "clipboard", "-out", "-t", "TARGETS"]
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        raise XClipError(f"failed to read TARGETS: {e}") from e