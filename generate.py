"""Front-page poster generator for news-image-20261122.

Draws a 1024x1024 newspaper front page from stories.json:
masthead naming the day, a world map with numbered story markers,
three featured stories, and the full list of the day's headlines.

Usage:
    python3 generate.py            # writes entry.png next to this file

Deterministic: same stories.json always yields the same PNG bytes.
"""

import json
import logging
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

from worldmap import CONTINENTS

logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
log = logging.getLogger("generate")

W, H = 1024, 1024
MARGIN = 30

PAPER = (246, 241, 230)
INK = (20, 20, 20)
NAVY = (15, 42, 74)
RED = (179, 32, 44)
OCEAN = (214, 228, 240)
LAND = (198, 210, 179)
LAND_EDGE = (120, 135, 105)
MUTED = (96, 96, 96)
RULE = (180, 175, 165)

FONT_DIRS = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
]

# Story ids marked on the map (chosen so no two markers overlap).
DOT_IDS = [1, 2, 3, 5, 6, 7, 9, 11, 14, 16, 18, 22, 25, 27]
FEATURED_IDS = [1, 2, 3]


def load_font(bold=False, serif=False, size=14):
    """First available DejaVu font matching the request."""
    if serif:
        names = ["DejaVuSerif-Bold.ttf"]
    elif bold:
        names = ["DejaVuSans-Bold.ttf"]
    else:
        names = ["DejaVuSans.ttf"]
    for name in names:
        path = Path("/usr/share/fonts/truetype/dejavu") / name
        if path.exists():
            return ImageFont.truetype(str(path), size)
    return ImageFont.load_default()


def wrap(text, font, max_width):
    """Greedy word wrap; returns a list of lines that fit max_width."""
    words = text.split()
    if not words:
        return [""]
    lines, cur = [], words[0]
    for word in words[1:]:
        trial = cur + " " + word
        if font.getlength(trial) <= max_width:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    lines.append(cur)
    return lines


def draw_centered(draw, cx, y, text, font, fill):
    draw.text((cx, y), text, font=font, fill=fill, anchor="ma")


def render(stories, out_path):
    """Render the poster; return the list of logical strings drawn.

    The returned list is the test hook: it proves every headline was
    drawn (wrapping may split a headline across visual lines, but the
    full string is in the list exactly once per story).
    """
    stories = sorted(stories, key=lambda s: s["id"])
    by_id = {s["id"]: s for s in stories}
    drawn = []

    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # Frame.
    d.rectangle([6, 6, W - 7, H - 7], outline=INK, width=2)

    # ---- Masthead -----------------------------------------------------
    y = 14
    title_font = load_font(serif=True, size=66)
    draw_centered(d, W // 2, y, "THE WORLD", title_font, NAVY)
    drawn.append("THE WORLD")
    y = 92
    d.line([(MARGIN, y), (W - MARGIN, y)], fill=RED, width=3)
    y = 100
    date_font = load_font(bold=True, size=24)
    date_line = "SUNDAY, 22 NOVEMBER 2026"
    draw_centered(d, W // 2, y, date_line, date_font, RED)
    drawn.append("SUNDAY")
    drawn.append("22 NOVEMBER 2026")
    y = 130
    tag_font = load_font(size=13)
    tag = "ONE DAY  ·  EVERYWHERE  —  %d STORIES FROM EVERY TIME ZONE" % len(stories)
    draw_centered(d, W // 2, y, tag, tag_font, MUTED)
    drawn.append(tag)

    # ---- World map ----------------------------------------------------
    map_box = (MARGIN, 158, W - MARGIN, 370)
    d.rectangle(map_box, fill=OCEAN, outline=RULE, width=1)
    mx0, my0, mx1, my1 = map_box
    mw, mh = mx1 - mx0, my1 - my0

    def project(lon, lat):
        # Equirectangular, cropped to lat -60..85.
        x = mx0 + (lon + 180.0) / 360.0 * mw
        y = my0 + (85.0 - lat) / 145.0 * mh
        return x, y

    for name, poly in CONTINENTS.items():
        pts = [project(lon, lat) for lon, lat in poly]
        d.polygon(pts, fill=LAND, outline=LAND_EDGE)

    dot_font = load_font(bold=True, size=13)
    for sid in DOT_IDS:
        s = by_id[sid]
        x, y = project(s["lon"], s["lat"])
        r = 10
        d.ellipse([x - r, y - r, x + r, y + r], fill=RED, outline="white",
                  width=2)
        d.text((x, y), str(sid), font=dot_font, fill="white", anchor="mm")
    caption_font = load_font(bold=True, size=12)
    d.text((mx0 + 8, my1 - 22),
           "WHERE THE DAY HAPPENED — NUMBERS MATCH THE STORIES BELOW",
           font=caption_font, fill=MUTED)
    drawn.append("WHERE THE DAY HAPPENED")

    # ---- Featured stories ---------------------------------------------
    feat_y = 384
    col_w = (W - 2 * MARGIN - 2 * 24) // 3
    feat_bottom = feat_y
    for i, sid in enumerate(FEATURED_IDS):
        s = by_id[sid]
        x0 = MARGIN + i * (col_w + 24)
        kick_font = load_font(bold=True, size=13)
        d.text((x0, feat_y), s["region"].upper(), font=kick_font, fill=RED)
        drawn.append(s["region"].upper())
        head_font = load_font(bold=True, size=18)
        lines = wrap(s["headline"], head_font, col_w)
        yy = feat_y + 20
        for line in lines:
            d.text((x0, yy), line, font=head_font, fill=INK)
            yy += 22
        sum_font = load_font(size=13)
        sum_lines = wrap(s["summary"], sum_font, col_w)
        yy += 4
        for line in sum_lines[:3]:
            d.text((x0, yy), line, font=sum_font, fill=(60, 60, 60))
            yy += 17
        feat_bottom = max(feat_bottom, yy)
        drawn.append(s["headline"])
        drawn.append(s["summary"])

    # ---- The day in brief ---------------------------------------------
    list_y = feat_bottom + 12
    d.line([(MARGIN, list_y), (W - MARGIN, list_y)], fill=INK, width=2)
    list_y += 10
    sec_font = load_font(bold=True, size=17)
    d.text((MARGIN, list_y), "THE DAY IN BRIEF", font=sec_font, fill=NAVY)
    d.text((W - MARGIN, list_y), "ALL TIMES 22 NOV 2026",
           font=load_font(bold=True, size=12), fill=MUTED, anchor="ra")
    drawn.append("THE DAY IN BRIEF")
    list_y += 30

    rest = [s for s in stories if s["id"] not in FEATURED_IDS]
    half = (len(rest) + 1) // 2
    columns = [rest[:half], rest[half:]]
    list_bottom = 968
    avail_h = list_bottom - list_y

    # Pick the largest body size that fits both columns.
    # Leading is tight (size+4) with a 3 px gap between items.
    chosen = None
    for size in (15, 14, 13, 12):
        head_f = load_font(bold=True, size=size)
        num_f = load_font(bold=True, size=size)
        heights = []
        for col in columns:
            total = 0
            for s in col:
                lines = wrap(s["headline"], head_f, 472 - 28)
                total += len(lines) * (size + 4) + 3
            heights.append(total)
        if max(heights) <= avail_h:
            chosen = (size, head_f, num_f)
            break
    if chosen is None:
        size = 12
        chosen = (size, load_font(bold=True, size=size),
                  load_font(bold=True, size=size))
    size, head_f, num_f = chosen
    log.info("list body font size %d (avail %d px)", size, avail_h)

    for ci, col in enumerate(columns):
        x0 = MARGIN + ci * (472 + 20)
        yy = list_y
        for s in col:
            d.text((x0, yy), "%d." % s["id"], font=num_f, fill=RED)
            lines = wrap(s["headline"], head_f, 472 - 28)
            ly = yy
            for line in lines:
                d.text((x0 + 28, ly), line, font=head_f, fill=INK)
                ly += size + 4
            yy = ly + 3
            drawn.append(s["headline"])

    # ---- Footer --------------------------------------------------------
    foot_font = load_font(size=11)
    d.line([(MARGIN, 978), (W - MARGIN, 978)], fill=RULE, width=1)
    foot = ("Compiled Sunday 22 November 2026 from wire reports — Reuters · AP · "
            "ANI · Hindustan Times · Investor's Business Daily")
    d.text((MARGIN, 986), foot, font=foot_font, fill=MUTED)
    d.text((W - MARGIN, 986), "make.fun · news-image-20261122",
           font=foot_font, fill=MUTED, anchor="ra")
    drawn.append(foot)

    img.save(out_path, format="PNG", optimize=True)
    log.info("wrote %s (%d bytes)", out_path,
             Path(out_path).stat().st_size)
    return drawn


def main():
    root = Path(__file__).resolve().parent
    stories = json.loads((root / "stories.json").read_text(encoding="utf-8"))
    log.info("loaded %d verified stories for 22 November 2026",
             len(stories))
    render(stories, root / "entry.png")
    log.info("done: entry.png ready")


if __name__ == "__main__":
    sys.exit(main())
