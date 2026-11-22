"""Entrypoint: copy the committed poster to /output/entry.png.

Standard library only — no Pillow, no fonts, no drawing at grade time.
The poster (entry.png) is rendered in the builder's session by render.py
and committed to this repository; the competition rules bless exactly
this shape: "the simplest program copies an image the repository holds".

The output directory is honoured from MAKEFUN_OUTPUT_DIR (default
/output). Nothing is ever deleted: only entry.png is written.
"""
import hashlib
import os
import shutil
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent
SOURCE = REPO / "entry.png"
DEFAULT_OUT_DIR = "/output"


def resolve_out_dir():
    return os.environ.get("MAKEFUN_OUTPUT_DIR", DEFAULT_OUT_DIR)


def main(out_dir=None):
    if not SOURCE.is_file():
        print(f"missing {SOURCE}", file=sys.stderr)
        return 1
    dest_dir = Path(out_dir) if out_dir is not None else Path(resolve_out_dir())
    dest_dir.mkdir(parents=True, exist_ok=True)
    dest = dest_dir / "entry.png"
    shutil.copyfile(SOURCE, dest)
    digest = hashlib.sha256(dest.read_bytes()).hexdigest()
    size = dest.stat().st_size
    print(f"wrote {dest} ({size} bytes, sha256 {digest})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
