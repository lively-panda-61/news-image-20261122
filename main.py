"""Entrypoint for the news-image-20261122 entry (Python 3.13).

Copies the pre-rendered front page (entry.png, drawn by generate.py
from the verified stories in stories.json) to the grader's output
directory. No network, no writes outside the output directory, and
it never removes the output directory itself -- it only writes the
one file inside it.

Outside the grader's container, MAKEFUN_OUTPUT_DIR stands in for
/output:
    mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
"""

import os
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SOURCE = HERE / "entry.png"
OUTPUT_DIR = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
TARGET = OUTPUT_DIR / "entry.png"


def main():
    if not SOURCE.exists():
        print(f"entry.png missing next to {__file__}", file=sys.stderr)
        return 1
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(SOURCE, TARGET)
    size = TARGET.stat().st_size
    print(f"copied entry.png ({size} bytes) to {TARGET}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
