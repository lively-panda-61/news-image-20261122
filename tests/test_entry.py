"""Tests for the News Image 22 Nov v4 entry (news-image-20261122).

Run: python3 -m pytest tests/ -q   (or: python3 -m unittest discover -s tests -v)
Covers: stdlib-only entrypoint, copy behaviour + determinism, poster
validity, story data (36 verified stories, 7 regions), LICENSE SPDX,
README badges.
"""

import ast
import hashlib
import importlib.util
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ALLOWED_IMPORTS = {"hashlib", "os", "shutil", "sys", "pathlib"}

EXPECTED_REGIONS = {
    "Middle East",
    "Europe",
    "Asia-Pacific",
    "Americas",
    "Africa",
    "Economy",
    "Science & Sport",
}


def load_news():
    spec = importlib.util.spec_from_file_location("news", ROOT / "news.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


class TestEntrypoint(unittest.TestCase):
    def test_main_py_is_stdlib_only(self):
        tree = ast.parse((ROOT / "main.py").read_text())
        imported = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imported.update(a.name.split(".")[0] for a in node.names)
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    imported.add(node.module.split(".")[0])
        self.assertTrue(
            imported <= ALLOWED_IMPORTS,
            f"main.py imports non-stdlib modules: {imported - ALLOWED_IMPORTS}",
        )
        self.assertTrue(imported, "main.py imports nothing at all")

    def test_main_copies_entry_png_byte_identical(self):
        with tempfile.TemporaryDirectory() as tmp:
            outdir = Path(tmp) / "out"
            outdir.mkdir()
            env = {
                "PATH": os.environ["PATH"],
                "MAKEFUN_OUTPUT_DIR": str(outdir),
                "PYTHONHASHSEED": "0",
                "TZ": "UTC",
                "LANG": "C.UTF-8",
            }
            proc = subprocess.run(
                [sys.executable, "-P", "-s", str(ROOT / "main.py")],
                env=env,
                cwd="/",
                capture_output=True,
                text=True,
            )
            self.assertEqual(proc.returncode, 0, proc.stderr)
            produced = outdir / "entry.png"
            self.assertTrue(produced.exists(), "main.py wrote no entry.png")
            src = (ROOT / "entry.png").read_bytes()
            self.assertEqual(produced.read_bytes(), src, "output differs from entry.png")
            self.assertEqual(
                hashlib.sha256(produced.read_bytes()).hexdigest(),
                hashlib.sha256(src).hexdigest(),
            )

    def test_main_is_deterministic(self):
        digests = []
        for _ in range(2):
            with tempfile.TemporaryDirectory() as tmp:
                outdir = Path(tmp) / "out"
                outdir.mkdir()
                env = {
                    "PATH": os.environ["PATH"],
                    "MAKEFUN_OUTPUT_DIR": str(outdir),
                    "PYTHONHASHSEED": "0",
                    "TZ": "UTC",
                    "LANG": "C.UTF-8",
                }
                proc = subprocess.run(
                    [sys.executable, "-P", "-s", str(ROOT / "main.py")],
                    env=env,
                    cwd="/",
                    capture_output=True,
                    text=True,
                )
                self.assertEqual(proc.returncode, 0, proc.stderr)
                digests.append(
                    hashlib.sha256((outdir / "entry.png").read_bytes()).hexdigest()
                )
        self.assertEqual(digests[0], digests[1], "two runs differ")

    def test_main_defaults_to_output_dir(self):
        src = (ROOT / "main.py").read_text()
        self.assertIn("/output", src, "main.py must default MAKEFUN_OUTPUT_DIR to /output")


class TestPoster(unittest.TestCase):
    def test_entry_png_is_valid_1024(self):
        from PIL import Image

        path = ROOT / "entry.png"
        self.assertTrue(path.exists(), "entry.png missing — run render.py first")
        size = path.stat().st_size
        self.assertLessEqual(size, 1_048_576, f"entry.png {size} bytes > 1 MiB")
        self.assertGreaterEqual(size, 100_000, f"entry.png only {size} bytes — too sparse")
        with Image.open(path) as im:
            self.assertEqual(im.format, "PNG")
            self.assertEqual(im.size, (1024, 1024))
            self.assertEqual(im.mode, "RGB")

    def test_render_is_deterministic(self):
        before = hashlib.sha256((ROOT / "entry.png").read_bytes()).hexdigest()
        env = dict(os.environ, PYTHONHASHSEED="0", TZ="UTC", LANG="C.UTF-8")
        proc = subprocess.run(
            [sys.executable, str(ROOT / "render.py")],
            env=env,
            cwd=str(ROOT),
            capture_output=True,
            text=True,
        )
        self.assertEqual(proc.returncode, 0, proc.stderr)
        after = hashlib.sha256((ROOT / "entry.png").read_bytes()).hexdigest()
        self.assertEqual(before, after, "render.py is not deterministic")


class TestNewsData(unittest.TestCase):
    def test_story_count_and_regions(self):
        news = load_news()
        self.assertGreaterEqual(len(news.STORIES), 36, "need 36+ stories")
        self.assertEqual(set(news.REGIONS), EXPECTED_REGIONS)
        self.assertEqual(len(news.REGIONS), 7)

    def test_every_story_wellformed(self):
        news = load_news()
        for i, s in enumerate(news.STORIES):
            self.assertIn("title", s, f"story {i} has no title")
            self.assertIn("deck", s, f"story {i} has no deck")
            self.assertIn("region", s, f"story {i} has no region")
            self.assertIn(s["region"], EXPECTED_REGIONS, f"story {i} bad region")
            self.assertTrue(s["title"].strip(), f"story {i} empty title")
            self.assertTrue(s["deck"].strip(), f"story {i} empty deck")
            self.assertLessEqual(len(s["title"]), 64, f"story {i} title too long")
            self.assertGreaterEqual(len(s["deck"]), 20, f"story {i} deck too short")

    def test_each_region_has_at_least_two_stories(self):
        news = load_news()
        counts = {r: 0 for r in EXPECTED_REGIONS}
        for s in news.STORIES:
            counts[s["region"]] += 1
        for region, n in counts.items():
            self.assertGreaterEqual(n, 2, f"region {region} has only {n} stories")

    def test_top_stories_are_six(self):
        news = load_news()
        top = [s for s in news.STORIES if s.get("top")]
        self.assertEqual(len(top), 6, "need exactly 6 top stories")
        self.assertEqual(len({s["region"] for s in top}), 5, "top stories span 5+ regions")

    def test_date_line_names_the_day(self):
        news = load_news()
        self.assertIn("22 NOVEMBER 2026", news.DATE_LINE)
        self.assertIn("SUNDAY", news.DATE_LINE)


class TestRepoGates(unittest.TestCase):
    def test_license_spdx_first_line(self):
        lines = (ROOT / "LICENSE").read_text().splitlines()
        self.assertTrue(lines, "LICENSE is empty")
        self.assertIn("SPDX-License-Identifier: MIT", lines[0])

    def test_readme_has_three_badges(self):
        readme = (ROOT / "README.md").read_text()
        self.assertIn(
            "https://make.fun/badge/news-image-20261122.svg", readme
        )
        self.assertIn(
            "https://make.fun/badge/news-image-20261122/lively-panda-61/news-image-20261122/rank.svg",
            readme,
        )
        self.assertIn(
            "https://make.fun/badge/news-image-20261122/lively-panda-61/news-image-20261122/reward.svg",
            readme,
        )

    def test_no_secrets_in_tracked_files(self):
        for path in ROOT.rglob("*"):
            if (
                path.is_file()
                and ".git/" not in str(path)
                and "tests/" not in str(path)
                and path.name != "entry.png"
            ):
                text = path.read_bytes()
                for bad in (b"sk-", b"api_key=", b"API_KEY=", b"BEGIN PRIVATE KEY"):
                    self.assertNotIn(bad, text, f"{path} looks like it holds a secret")


if __name__ == "__main__":
    unittest.main()
