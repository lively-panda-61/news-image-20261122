"""Entry point for the News Image 22 Nov v4 entry (news-image-20261122).

The poster is pre-rendered at build time and committed as entry.png.
This program only copies it to the output directory, using the standard
library alone, so it runs identically on any Python.
"""

import hashlib
import os
import shutil
import sys
from pathlib import Path

SOURCE = Path(__file__).resolve().with_name("entry.png")


def main():
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    target = out_dir / "entry.png"
    shutil.copyfile(SOURCE, target)
    digest = hashlib.sha256(target.read_bytes()).hexdigest()
    print(f"copied entry.png -> {target} (sha256 {digest})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
