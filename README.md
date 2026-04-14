# cliptool

`cliptool` is a small command-line helper for Linux X11 clipboard workflows.
It wraps `xclip` and lets you copy file-related payloads with the correct target type.

## Features

- Copy `text/uri-list` payloads (common for file manager paste behavior)
- Copy file content as `text/plain`
- Copy absolute path as `text/plain`
- Copy GNOME/Nautilus-style `x-special/gnome-copied-files` payload
- Print `file://` URI without touching the clipboard
- Inspect clipboard `TARGETS`

## Requirements

- Linux with X11 session
- `xclip` available in `PATH`
- Python 3.9+

Install `xclip` first (example for Debian/Ubuntu):

```bash
sudo apt-get update
sudo apt-get install -y xclip
```

## Install

From the project root:

```bash
python -m pip install -e .
```

Confirm the CLI is available:

```bash
cliptool --help
```

## Commands

| Command | Alias | Behavior | Clipboard target |
| --- | --- | --- | --- |
| `copy-file <path>` | `cf` | Copy URI list for path | `text/uri-list` |
| `copy-text <path>` | `ct` | Copy file bytes as text | `text/plain` |
| `copy-path <path>` | `cp` | Copy resolved absolute path | `text/plain` |
| `copy-gnome-file <path>` | `cgf` | Copy GNOME copied-files payload | `x-special/gnome-copied-files` |
| `uri <path>` | `u` | Print resolved `file://` URI | (no clipboard write) |
| `targets` | `tg` | Print current clipboard `TARGETS` | (read-only) |

Notes:

- `<path>` must exist.
- For `copy-text`, `<path>` should be a readable regular file.

## Practical Usage Examples

Create a test file:

```bash
mkdir -p /tmp/cliptool-demo
printf 'hello cliptool\n' > /tmp/cliptool-demo/demo.txt
```

### 1) Print a URI (no clipboard write)

```bash
cliptool uri /tmp/cliptool-demo/demo.txt
```

Typical output:

```text
file:///tmp/cliptool-demo/demo.txt
```

### 2) Copy URI list for file-manager style paste

```bash
cliptool copy-file /tmp/cliptool-demo/demo.txt
```

Typical output:

```text
Copied file URI list for: /tmp/cliptool-demo/demo.txt
```

Check clipboard content:

```bash
xclip -selection clipboard -out -t text/uri-list
```

Expected content:

```text
file:///tmp/cliptool-demo/demo.txt
```

### 3) Copy file content as plain text

```bash
cliptool copy-text /tmp/cliptool-demo/demo.txt
```

Check clipboard content:

```bash
xclip -selection clipboard -out -t text/plain
```

Expected content:

```text
hello cliptool
```

### 4) Copy absolute path as plain text

```bash
cliptool copy-path /tmp/cliptool-demo/demo.txt
```

Check clipboard content:

```bash
xclip -selection clipboard -out -t text/plain
```

Expected content:

```text
/tmp/cliptool-demo/demo.txt
```

### 5) Copy GNOME/Nautilus copied-files payload

```bash
cliptool copy-gnome-file /tmp/cliptool-demo/demo.txt
```

Check clipboard content:

```bash
xclip -selection clipboard -out -t x-special/gnome-copied-files
```

Expected content:

```text
copy
file:///tmp/cliptool-demo/demo.txt
```

### 6) Inspect available clipboard targets

```bash
cliptool targets
```

Example output may include:

```text
TARGETS
UTF8_STRING
text/plain
text/uri-list
x-special/gnome-copied-files
```

## Exit Codes

- `0`: success
- `1`: invalid/missing path (for example, path does not exist)
- `2`: `xclip` related failure
- `3`: unexpected runtime error

## Troubleshooting

### `xclip not found in PATH`

Install `xclip` and make sure it is available:

```bash
which xclip
```

### `xclip failed` or `Can't open display`

- Run inside an X11 desktop session.
- Ensure `DISPLAY` is set.
- If you are on Wayland-only workflows, behavior may vary unless X11 compatibility is enabled.

### `Path does not exist: ...`

Use an existing path. You can verify with:

```bash
ls -la <path>
```

## Development

Run directly from source during development:

```bash
python -m cliptool.cli --help
```
