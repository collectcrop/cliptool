from __future__ import annotations

# PYTHON_ARGCOMPLETE_OK

import argparse
import sys
from pathlib import Path

import argcomplete
from argcomplete.completers import FilesCompleter

from .payload import (
    make_binary_file_payload,
    make_gnome_copied_files_payload,
    make_path_payload,
    make_text_payload,
    make_uri_list_payload,
)
from .utils import guess_image_target, to_abs_path, to_uri
from .x11 import XClipError, copy_to_clipboard, read_targets


IMAGE_EXTENSIONS = [
    "png",
    "jpg",
    "jpeg",
    "gif",
    "bmp",
    "webp",
    "svg",
]


def image_path_completer(prefix: str, parsed_args, **kwargs):
    base = Path(".")
    results = []

    for p in base.glob(f"{prefix}*") if prefix else base.iterdir():
        if p.is_file() and p.suffix.lower().lstrip(".") in IMAGE_EXTENSIONS:
            results.append(str(p))
    return results


def add_file_argument(parser: argparse.ArgumentParser, image_only: bool = False) -> None:
    action = parser.add_argument("file", help="Path to the file")
    if image_only:
        action.completer = image_path_completer
    else:
        action.completer = FilesCompleter()


def handle_copy_file(path_str: str) -> None:
    copy_to_clipboard(make_uri_list_payload(path_str), target="text/uri-list")
    print(f"Copied file URI list for: {to_abs_path(path_str)}")


def handle_copy_text(path_str: str) -> None:
    copy_to_clipboard(make_text_payload(path_str), target="text/plain")
    print(f"Copied file content as text/plain: {to_abs_path(path_str)}")


def handle_copy_path(path_str: str) -> None:
    copy_to_clipboard(make_path_payload(path_str), target="text/plain")
    print(f"Copied absolute path: {to_abs_path(path_str)}")


def handle_copy_gnome_file(path_str: str) -> None:
    copy_to_clipboard(
        make_gnome_copied_files_payload(path_str),
        target="x-special/gnome-copied-files",
    )
    print(f"Copied GNOME file payload for: {to_abs_path(path_str)}")


def handle_copy_image(path_str: str) -> None:
    target = guess_image_target(path_str)
    copy_to_clipboard(make_binary_file_payload(path_str), target=target)
    print(f"Copied image as {target}: {to_abs_path(path_str)}")


def handle_print_uri(path_str: str) -> None:
    print(to_uri(path_str))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="cliptool",
        description="Small X11 clipboard helper"
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    p_copy_file = subparsers.add_parser(
        "copy-file",
        aliases=["cf"],
        help="Copy as text/uri-list",
    )
    add_file_argument(p_copy_file)

    p_copy_text = subparsers.add_parser(
        "copy-text",
        aliases=["ct"],
        help="Copy file content as text/plain",
    )
    add_file_argument(p_copy_text)

    p_copy_path = subparsers.add_parser(
        "copy-path",
        aliases=["cp"],
        help="Copy absolute file path as text/plain",
    )
    add_file_argument(p_copy_path)

    p_copy_gnome_file = subparsers.add_parser(
        "copy-gnome-file",
        aliases=["cgf"],
        help="Copy as x-special/gnome-copied-files",
    )
    add_file_argument(p_copy_gnome_file)

    p_copy_image = subparsers.add_parser(
        "copy-image",
        aliases=["ci"],
        help="Copy image bytes with detected image/* target",
    )
    add_file_argument(p_copy_image, image_only=True)

    p_uri = subparsers.add_parser(
        "uri",
        aliases=["u"],
        help="Print file:// URI",
    )
    add_file_argument(p_uri)

    subparsers.add_parser(
        "targets",
        aliases=["tg"],
        help="Show clipboard TARGETS",
    )

    argcomplete.autocomplete(parser)
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    try:
        if args.command in ("copy-file", "cf"):
            handle_copy_file(args.file)
        elif args.command in ("copy-text", "ct"):
            handle_copy_text(args.file)
        elif args.command in ("copy-path", "cp"):
            handle_copy_path(args.file)
        elif args.command in ("copy-gnome-file", "cgf"):
            handle_copy_gnome_file(args.file)
        elif args.command in ("copy-image", "ci"):
            handle_copy_image(args.file)
        elif args.command in ("uri", "u"):
            handle_print_uri(args.file)
        elif args.command in ("targets", "tg"):
            print(read_targets(), end="")
        else:
            parser.error(f"Unknown command: {args.command}")

    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except XClipError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(2)
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        sys.exit(3)


if __name__ == "__main__":
    main()