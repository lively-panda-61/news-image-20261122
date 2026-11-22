"""Tests for the build-time poster renderer (render.py + news.py).

The renderer only runs in the builder's session; the graded entrypoint
just copies the rendered entry.png. These tests pin the poster's facts,
structure and determinism.
"""
import hashlib
import importlib.util
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parent.parent
IMAGE = REPO / "entry.png"


def load(name):
    path = REPO / f"{name}.py"
    spec = importlib.util.spec_from_file_location(f"news22_{name}", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_story_count_and_ids():
    news = load("news")
    assert len(news.STORIES) == 36
    ids = [s["id"] for s in news.STORIES]
    assert sorted(ids) == list(range(1, 37)), "story ids must be 1..36"


def test_every_story_has_required_fields_and_date():
    news = load("news")
    for s in news.STORIES:
        for key in ("id", "region", "place", "headline", "summary", "source",
                    "lat", "lon", "date"):
            assert key in s, f"story {s.get('id')} missing {key}"
        assert s["date"] == "2026-11-22", "every story must be 22 Nov 2026"
        assert s["headline"].strip() and s["summary"].strip()
        assert -90 <= s["lat"] <= 90 and -180 <= s["lon"] <= 180


def test_region_counts_sum_to_36():
    news = load("news")
    counts = {}
    for s in news.STORIES:
        counts[s["region"]] = counts.get(s["region"], 0) + 1
    assert sum(counts.values()) == 36
    assert set(counts) == {"Europe", "Middle East", "Asia-Pacific",
                           "Americas", "Africa", "Oceania", "Global"}


def test_thirteen_drawn_panels_have_routines():
    news = load("news")
    render = load("render")
    drawn = [s for s in news.STORIES if s.get("scene")]
    assert len(drawn) == 13, f"expected 13 drawn panels, got {len(drawn)}"
    for s in drawn:
        assert s["scene"] in render.SCENES, f"no scene routine for {s['scene']}"
        assert callable(render.SCENES[s["scene"]])


def test_stats_timeline_regions_present():
    news = load("news")
    assert len(news.STATS) == 6
    assert len(news.TIMELINE) == 6
    assert len(news.REGIONS) == 7
    assert sum(n for _, n, _ in news.REGIONS) == 36
    assert "22 November 2026" in news.DATE_CHECK
    assert "22 November 2026" in news.FOOTER


def test_render_is_deterministic_and_correct_size(tmp_path):
    render = load("render")
    out1 = tmp_path / "one.png"
    out2 = tmp_path / "two.png"
    render.render_poster(out1)
    render.render_poster(out2)
    b1, b2 = out1.read_bytes(), out2.read_bytes()
    assert b1 == b2, "two renders must be byte-identical"
    from PIL import Image

    with Image.open(out1) as img:
        assert img.format == "PNG"
        assert img.size == (1024, 1024)
    assert out1.stat().st_size <= 1024 * 1024


def test_rendered_image_matches_committed_entry(tmp_path):
    render = load("render")
    out = tmp_path / "fresh.png"
    render.render_poster(out)
    assert out.read_bytes() == IMAGE.read_bytes(), (
        "committed entry.png must be exactly what render.py produces")
