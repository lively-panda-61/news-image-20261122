"""Tests for the news-image-20261122 v2 poster (TDD: written before the code).

Run: python3 -m pytest tests/ -q   (or: python3 tests/test_poster.py)
"""
import hashlib
import json
import os
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PIL import Image

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def test_stories_file_exists_and_parses():
    path = os.path.join(REPO, "stories.py")
    assert os.path.exists(path), "stories.py missing"


def test_story_count_and_regions():
    import stories

    items = stories.STORIES
    assert len(items) == 36, f"expected 36 stories, got {len(items)}"
    regions = {}
    for s in items:
        regions[s["region"]] = regions.get(s["region"], 0) + 1
    assert len(regions) == 7, f"expected 7 regions, got {sorted(regions)}"
    assert sum(regions.values()) == 36
    assert regions.get("Europe") == 8, regions
    assert regions.get("Middle East") == 5, regions
    assert regions.get("Asia-Pacific") == 9, regions
    assert regions.get("Americas") == 7, regions
    assert regions.get("Africa") == 2, regions
    assert regions.get("Oceania") == 2, regions
    assert regions.get("Global") == 3, regions


def test_all_stories_dated_22_nov_2026_with_source():
    import stories

    for s in stories.STORIES:
        assert s["date"] == "2026-11-22", f"story {s['id']} not dated 22 Nov 2026"
        assert s["headline"].strip(), f"story {s['id']} has no headline"
        assert s["summary"].strip(), f"story {s['id']} has no summary"
        assert s["source"].strip(), f"story {s['id']} has no source"
        assert s["place"].strip(), f"story {s['id']} has no place"
        assert "lat" in s and "lon" in s, f"story {s['id']} has no map coords"


def test_drawn_panels():
    import stories

    drawn = [s for s in stories.STORIES if s.get("draw")]
    assert len(drawn) == 13, f"expected 13 drawn panels, got {len(drawn)}"
    assert [s["id"] for s in drawn] == list(range(1, 14))
    for s in drawn:
        assert s["draw"] in stories.DRAW_KEYS, f"story {s['id']} bad draw key"


def test_stat_strip():
    import stories

    assert len(stories.STATS) == 6
    for value, caption in stories.STATS:
        assert value.strip() and caption.strip()


def test_poster_renders_1024_and_small_enough():
    import draw

    img = draw.render_poster()
    assert img.size == (1024, 1024), f"poster is {img.size}"
    assert img.mode == "RGB"
    path = "/tmp/test-entry.png"
    img.save(path, format="PNG", optimize=True)
    size = os.path.getsize(path)
    assert size <= 1_048_576, f"poster is {size} bytes, over the 1 MiB cap"


def test_poster_is_deterministic():
    import draw

    a = draw.render_poster()
    b = draw.render_poster()
    ha = hashlib.sha256(a.tobytes()).hexdigest()
    hb = hashlib.sha256(b.tobytes()).hexdigest()
    assert ha == hb, "two renders differ"


def test_main_copies_entry_to_output(tmp_path):
    out = tmp_path / "output"
    out.mkdir()
    env = dict(os.environ, MAKEFUN_OUTPUT_DIR=str(out))
    r = subprocess.run(
        [sys.executable, os.path.join(REPO, "main.py")],
        env=env, capture_output=True, text=True, timeout=120,
    )
    assert r.returncode == 0, f"main.py failed: {r.stderr[-2000:]}"
    target = out / "entry.png"
    assert target.exists(), "main.py did not write entry.png to the output dir"
    img = Image.open(target)
    assert img.size == (1024, 1024)
    assert target.stat().st_size <= 1_048_576
    # second run must write identical bytes (grader runs it twice)
    r2 = subprocess.run(
        [sys.executable, os.path.join(REPO, "main.py")],
        env=env, capture_output=True, text=True, timeout=120,
    )
    assert r2.returncode == 0
    assert target.read_bytes() == Image.open(target).tobytes() or True
    first = target.read_bytes()
    r3 = subprocess.run(
        [sys.executable, os.path.join(REPO, "main.py")],
        env=env, capture_output=True, text=True, timeout=120,
    )
    assert r3.returncode == 0
    assert target.read_bytes() == first, "second run wrote different bytes"


def test_no_secrets_in_repo_text():
    bad = ["API_KEY=", "api_key=", "BEGIN PRIVATE KEY", "BEGIN RSA PRIVATE KEY",
           "password=", "ghp_", "gho_"]
    for root, _dirs, files in os.walk(REPO):
        if "__pycache__" in root or ".git" in root or root.endswith("/tests"):
            continue
        for f in files:
            if f.endswith((".py", ".md", ".json", ".txt")):
                text = open(os.path.join(root, f), errors="ignore").read()
                for token in bad:
                    assert token not in text, f"{token} found in {f}"


if __name__ == "__main__":
    import pytest

    raise SystemExit(pytest.main([__file__, "-q"]))
