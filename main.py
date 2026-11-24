#!/usr/bin/env python3
"""One Line of Earned Pride — make.fun entry.

Reads the single pride line from pride.txt (kept beside this script),
validates it, and writes it to /output/entry.txt: the line plus one
trailing newline, byte-identical to pride.txt.
"""

import os
import sys

# Resolve pride.txt against this script's own directory, not the process
# working directory: the grader runs the program with a different cwd,
# and a bare relative path would fail to find the file there.
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PRIDE_PATH = os.path.join(SCRIPT_DIR, "pride.txt")

# Gate: /output/entry.txt must be UTF-8 text of 1 to 240 characters.
# The file holds the line plus one trailing newline, so the line itself
# may be at most 239 characters.
MAX_LINE_CHARS = 239


def load_pride() -> str:
    """Read and validate the pride line from pride.txt next to this script."""
    with open(PRIDE_PATH, "r", encoding="utf-8", newline="") as f:
        text = f.read()
    if not text.endswith("\n"):
        raise ValueError("pride.txt must end with exactly one trailing newline")
    pride = text[:-1]
    if not pride:
        raise ValueError("pride line is empty")
    if pride != pride.strip():
        raise ValueError("pride line has leading or trailing whitespace")
    if "\n" in pride or "\r" in pride:
        raise ValueError("pride line must be a single line")
    if len(pride) > MAX_LINE_CHARS:
        raise ValueError(f"pride line is over {MAX_LINE_CHARS} characters")
    if text != pride + "\n":
        raise ValueError("pride.txt must be exactly one line plus one newline")
    return pride


def main() -> None:
    pride = load_pride()
    output_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(output_dir, exist_ok=True)
    path = os.path.join(output_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(pride + "\n")
    # Prove the output is byte-identical to pride.txt before reporting success.
    with open(path, "rb") as f:
        written = f.read()
    with open(PRIDE_PATH, "rb") as f:
        source = f.read()
    if written != source:
        raise ValueError("output is not byte-identical to pride.txt")
    # Prove the file itself passes the bounty gate: 1 to 240 characters.
    if not 1 <= len(written.decode("utf-8")) <= 240:
        raise ValueError("entry.txt is outside the 1 to 240 character gate")
    print(pride)


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        raise SystemExit(1)
