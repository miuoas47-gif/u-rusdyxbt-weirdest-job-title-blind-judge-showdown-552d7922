#!/usr/bin/env python3
"""Write the weirdest job title to $MAKEFUN_OUTPUT_DIR/entry.txt.

The bounty gate requires entry.txt to hold UTF-8 text of 1 to 60
characters, not only whitespace. This program writes exactly one job
title -- a single line, no trailing newline -- then reads the file
back to prove what landed on disk is what was intended.
"""

import os
import sys

TITLE = "Chief Doorknob Polisher, Buckingham Palace"
MAX_CHARS = 60


def main() -> int:
    if len(sys.argv) > 1:
        print("usage: main.py (takes no arguments)", file=sys.stderr)
        return 2

    if not 1 <= len(TITLE) <= MAX_CHARS:
        print(f"title is {len(TITLE)} chars, must be 1-60", file=sys.stderr)
        return 1
    if TITLE != TITLE.strip() or "\n" in TITLE or "\r" in TITLE:
        print("title must be a single non-blank line", file=sys.stderr)
        return 1
    if any(ord(ch) < 0x20 for ch in TITLE):
        print("title must not contain control characters", file=sys.stderr)
        return 1

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")

    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(TITLE)

    with open(path, "r", encoding="utf-8", newline="") as f:
        written = f.read()
    if written != TITLE:
        print("read-back mismatch", file=sys.stderr)
        return 1

    print(f"Wrote entry.txt ({len(TITLE)} chars): {TITLE}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
