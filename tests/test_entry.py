"""Tests for the news-image-20261122 entry.

Run:  python3 -m unittest discover -s tests -v
from the repository root.

TDD contract (written before the implementation):
- stories.json holds >= 30 verified stories of 22 November 2026.
- entry.png is a 1024x1024 PNG under 1 MiB, drawn by generate.py.
- Every story headline is drawn into the image (checked via the
  renderer's drawn-text report, not by OCR).
- main.py copies entry.png to the output dir, byte-identical and
  deterministic, without deleting the output directory itself.
- README carries the exact three make.fun badge lines + footer.
- No secrets or placeholders anywhere in the repo.
"""

import json
import os
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

PLACEHOLDERS = ("lorem", "tbd", "todo", "placeholder", "xxx", "lipsum",
                "[insert", "coming soon", "sample headline")
SECRET_PATTERNS = (
    re.compile(r"(?i)(api[_-]?key|secret|password|passwd)\s*[:=]\s*['\"][^'\"]{4,}"),
    re.compile(r"(?i)-----BEGIN (RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    re.compile(r"(?i)ghp_[A-Za-z0-9]{20,}"),
    re.compile(r"(?i)sk-[A-Za-z0-9]{16,}"),
)


class TestStories(unittest.TestCase):
    def setUp(self):
        self.path = ROOT / "stories.json"
        self.stories = json.loads(self.path.read_text(encoding="utf-8"))

    def test_stories_file_is_a_list(self):
        self.assertIsInstance(self.stories, list)

    def test_at_least_30_verified_stories(self):
        self.assertGreaterEqual(len(self.stories), 30,
                                f"only {len(self.stories)} stories")

    def test_every_story_has_required_fields(self):
        required = {"id", "headline", "summary", "region", "source",
                    "date", "lat", "lon"}
        for s in self.stories:
            self.assertTrue(required <= set(s),
                            f"story {s.get('id')} missing fields")

    def test_every_story_is_dated_22_nov_2026(self):
        for s in self.stories:
            self.assertEqual(s["date"], "2026-11-22",
                             f"story {s['id']} dated {s['date']}")

    def test_every_story_has_real_source_and_text(self):
        for s in self.stories:
            self.assertGreaterEqual(len(s["headline"]), 12,
                                    f"story {s['id']} headline too short")
            self.assertLessEqual(len(s["headline"]), 110,
                                 f"story {s['id']} headline too long")
            self.assertGreaterEqual(len(s["summary"]), 20)
            self.assertGreaterEqual(len(s["source"]), 3)
            blob = (s["headline"] + " " + s["summary"]).lower()
            for p in PLACEHOLDERS:
                self.assertNotIn(p, blob, f"story {s['id']} has placeholder")

    def test_headlines_are_unique(self):
        heads = [s["headline"] for s in self.stories]
        self.assertEqual(len(heads), len(set(heads)), "duplicate headlines")

    def test_regions_cover_the_world(self):
        regions = {s["region"] for s in self.stories}
        for needed in ("Middle East", "Europe", "Asia", "Americas",
                       "Africa", "Sport", "Markets"):
            self.assertIn(needed, regions, f"no {needed} stories")

    def test_coordinates_are_valid(self):
        for s in self.stories:
            self.assertTrue(-90 <= s["lat"] <= 90)
            self.assertTrue(-180 <= s["lon"] <= 180)


class TestImage(unittest.TestCase):
    def test_entry_png_exists_and_is_png(self):
        p = ROOT / "entry.png"
        self.assertTrue(p.exists(), "entry.png missing")
        self.assertEqual(p.read_bytes()[:8], b"\x89PNG\r\n\x1a\n")

    def test_entry_png_size_and_dimensions(self):
        from PIL import Image
        p = ROOT / "entry.png"
        self.assertLessEqual(p.stat().st_size, 1048576,
                             "entry.png over the 1 MiB gate")
        with Image.open(p) as im:
            self.assertEqual(im.size, (1024, 1024))
            self.assertEqual(im.mode, "RGB")

    def test_image_is_not_blank(self):
        from PIL import Image
        with Image.open(ROOT / "entry.png") as im:
            colors = im.getcolors(maxcolors=1 << 24)
        self.assertTrue(colors and len(colors) > 200,
                        "image looks blank / flat")

    def test_all_headlines_are_drawn(self):
        import generate
        stories = json.loads((ROOT / "stories.json").read_text())
        drawn = generate.render(stories, ROOT / "entry.png")
        drawn_blob = "\n".join(drawn)
        missing = [s["headline"] for s in stories
                   if s["headline"] not in drawn_blob]
        self.assertEqual(missing, [], f"headlines not drawn: {missing}")

    def test_masthead_names_the_day(self):
        import generate
        stories = json.loads((ROOT / "stories.json").read_text())
        drawn = generate.render(stories, ROOT / "entry.png")
        blob = "\n".join(drawn)
        self.assertIn("22 NOVEMBER 2026", blob)
        self.assertIn("SUNDAY", blob)


class TestEntrypoint(unittest.TestCase):
    def test_main_copies_entry_png_byte_identical(self):
        with tempfile.TemporaryDirectory() as tmp:
            outdir = Path(tmp) / "output"
            env = dict(os.environ, MAKEFUN_OUTPUT_DIR=str(outdir))
            r = subprocess.run([sys.executable, str(ROOT / "main.py")],
                               env=env, capture_output=True, text=True,
                               cwd=str(ROOT))
            self.assertEqual(r.returncode, 0, r.stderr)
            got = outdir / "entry.png"
            self.assertTrue(got.exists())
            self.assertEqual(got.read_bytes(),
                             (ROOT / "entry.png").read_bytes())

    def test_main_is_deterministic(self):
        with tempfile.TemporaryDirectory() as tmp:
            outdir = Path(tmp) / "output"
            env = dict(os.environ, MAKEFUN_OUTPUT_DIR=str(outdir))
            for _ in range(2):
                r = subprocess.run(
                    [sys.executable, str(ROOT / "main.py")],
                    env=env, capture_output=True, text=True, cwd=str(ROOT))
                self.assertEqual(r.returncode, 0, r.stderr)
            self.assertEqual((outdir / "entry.png").read_bytes(),
                             (ROOT / "entry.png").read_bytes())

    def test_main_does_not_remove_output_dir(self):
        with tempfile.TemporaryDirectory() as tmp:
            outdir = Path(tmp) / "output"
            outdir.mkdir()
            keep = outdir / "keep.txt"
            keep.write_text("do not delete")
            env = dict(os.environ, MAKEFUN_OUTPUT_DIR=str(outdir))
            r = subprocess.run([sys.executable, str(ROOT / "main.py")],
                               env=env, capture_output=True, text=True,
                               cwd=str(ROOT))
            self.assertEqual(r.returncode, 0, r.stderr)
            self.assertTrue(outdir.exists(), "main.py removed /output")
            self.assertTrue(keep.exists(), "main.py wiped /output contents")

    def test_main_needs_no_network(self):
        src = (ROOT / "main.py").read_text()
        for banned in ("socket", "urllib", "requests", "http.client"):
            self.assertNotIn(banned, src)


class TestRepoHygiene(unittest.TestCase):
    def test_readme_has_exact_badges_and_footer(self):
        readme = (ROOT / "README.md").read_text()
        badges = [
            "[![make.fun · news-image-20261122](https://make.fun/badge/news-image-20261122.svg)]"
            "(https://make.fun/bounty/news-image-20261122?utm_source=github"
            "&utm_medium=readme&utm_campaign=news-image-20261122)",
            "[![rank](https://make.fun/badge/news-image-20261122/lively-panda-61/"
            "news-image-20261122/rank.svg)]"
            "(https://make.fun/bounty/news-image-20261122/leaderboard?utm_source=github"
            "&utm_medium=readme&utm_campaign=news-image-20261122)",
            "[![reward](https://make.fun/badge/news-image-20261122/lively-panda-61/"
            "news-image-20261122/reward.svg)]"
            "(https://make.fun/bounty/news-image-20261122?utm_source=github"
            "&utm_medium=readme&utm_campaign=news-image-20261122)",
        ]
        for b in badges:
            self.assertIn(b, readme, f"badge missing: {b[:60]}...")
        self.assertIn("https://make.fun/?ref=q85rcyn4", readme)

    def test_license_is_osi_approved(self):
        lic = (ROOT / "LICENSE").read_text()
        self.assertIn("MIT License", lic)

    def test_no_secrets_in_repo(self):
        for p in ROOT.rglob("*"):
            if p.is_dir() or ".git" in p.parts or p.name == "entry.png":
                continue
            text = p.read_bytes().decode("utf-8", errors="ignore")
            for pat in SECRET_PATTERNS:
                self.assertIsNone(pat.search(text), f"secret in {p}")
        self.assertFalse((ROOT / ".env").exists(), ".env must not be committed")


if __name__ == "__main__":
    unittest.main(verbosity=2)
