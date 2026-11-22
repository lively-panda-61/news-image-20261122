"""Entrypoint: render the Sunday 22 November 2026 front page to /output/entry.png.

The poster is drawn deterministically from stories.py, so two runs write
identical bytes. The output directory honours MAKEFUN_OUTPUT_DIR when the
harness sets it, and defaults to /output.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import draw


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    img = draw.render_poster()
    path = os.path.join(out_dir, "entry.png")
    img.save(path, format="PNG", optimize=True)
    print(f"wrote {path} ({os.path.getsize(path)} bytes, {img.size[0]}x{img.size[1]})")
    return path


if __name__ == "__main__":
    main()
