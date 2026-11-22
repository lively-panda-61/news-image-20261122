"""Tests for the stdlib-only copy entrypoint (main.py).

The grader runs `python3 -P -s main.py` in a pinned image with no network
and a read-only repository. The entrypoint must therefore import nothing
beyond the standard library, copy the committed entry.png to
$MAKEFUN_OUTPUT_DIR/entry.png, and never delete anything.
"""
import ast
import hashlib
import importlib.util
import os
import subprocess
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parent.parent
MAIN = REPO / "main.py"
IMAGE = REPO / "entry.png"


def load_main():
    spec = importlib.util.spec_from_file_location("news22_main", MAIN)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_main_py_exists():
    assert MAIN.is_file(), "main.py must exist at the repo root"


def test_main_py_imports_only_stdlib():
    tree = ast.parse(MAIN.read_text(encoding="utf-8"))
    stdlib = sys.stdlib_module_names
    imported = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imported.update(a.name.split(".")[0] for a in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            imported.add(node.module.split(".")[0])
    third_party = imported - stdlib
    assert not third_party, f"main.py must be stdlib-only, found: {third_party}"
    assert "PIL" not in imported and "pillow" not in imported


def test_entry_png_valid():
    assert IMAGE.is_file(), "entry.png must be committed in the repo"
    from PIL import Image

    with Image.open(IMAGE) as img:
        assert img.format == "PNG"
        assert img.size == (1024, 1024), f"expected 1024x1024, got {img.size}"
    assert IMAGE.stat().st_size <= 1024 * 1024, "entry.png must be at most 1 MiB"


def test_default_out_dir_is_output():
    mod = load_main()
    old = os.environ.pop("MAKEFUN_OUTPUT_DIR", None)
    try:
        assert mod.resolve_out_dir() == "/output"
    finally:
        if old is not None:
            os.environ["MAKEFUN_OUTPUT_DIR"] = old


def test_copy_is_byte_identical_and_honours_env(tmp_path):
    mod = load_main()
    out = tmp_path / "somewhere" / "else"
    rc = mod.main(out_dir=str(out))
    assert rc == 0
    dest = out / "entry.png"
    assert dest.is_file()
    assert dest.read_bytes() == IMAGE.read_bytes()
    digest = hashlib.sha256(dest.read_bytes()).hexdigest()
    assert digest == hashlib.sha256(IMAGE.read_bytes()).hexdigest()


def test_copy_via_env_var(tmp_path, monkeypatch):
    monkeypatch.setenv("MAKEFUN_OUTPUT_DIR", str(tmp_path))
    mod = load_main()
    assert mod.main() == 0
    assert (tmp_path / "entry.png").read_bytes() == IMAGE.read_bytes()


def test_does_not_remove_other_files_in_output_dir(tmp_path):
    keep = tmp_path / "keep-me.txt"
    keep.write_text("do not delete", encoding="utf-8")
    mod = load_main()
    assert mod.main(out_dir=str(tmp_path)) == 0
    assert keep.is_file() and keep.read_text(encoding="utf-8") == "do not delete"
    assert tmp_path.is_dir()


def test_deterministic_two_runs(tmp_path):
    mod = load_main()
    out1, out2 = tmp_path / "a", tmp_path / "b"
    assert mod.main(out_dir=str(out1)) == 0
    assert mod.main(out_dir=str(out2)) == 0
    assert (out1 / "entry.png").read_bytes() == (out2 / "entry.png").read_bytes()


def test_grader_style_subprocess(tmp_path):
    """Run exactly the way the grader runs it, from another directory."""
    out = tmp_path / "out"
    out.mkdir()
    env = dict(os.environ)
    env.update(
        {
            "PYTHONHASHSEED": "0",
            "TZ": "UTC",
            "LANG": "C.UTF-8",
            "MAKEFUN_OUTPUT_DIR": str(out),
        }
    )
    proc = subprocess.run(
        [sys.executable, "-P", "-s", str(MAIN)],
        cwd="/",
        env=env,
        capture_output=True,
        text=True,
        timeout=60,
    )
    assert proc.returncode == 0, f"stderr: {proc.stderr}"
    assert (out / "entry.png").is_file()
    assert (out / "entry.png").read_bytes() == IMAGE.read_bytes()
