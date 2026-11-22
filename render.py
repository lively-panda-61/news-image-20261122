"""Build-time poster renderer for the News Image 22 Nov v4 entry.

Renders entry.png (1024x1024) from news.py with Pillow. This script runs
ONLY at build time; the submitted entrypoint (main.py) is stdlib-only
and just copies the committed entry.png.

Deterministic: no randomness, no time, no network. Running it twice
produces byte-identical output.
"""

import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

from news import DATE_LINE, MAP_PINS, REGIONS, STORIES, TITLE, SUBTITLE

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "entry.png"

W, H = 1024, 1024

FONT_DIR = Path("/usr/share/fonts/truetype/dejavu")
F_BOLD = str(FONT_DIR / "DejaVuSans-Bold.ttf")
F_REG = str(FONT_DIR / "DejaVuSans.ttf")
F_SERIF_BOLD = str(FONT_DIR / "DejaVuSerif-Bold.ttf")

NAVY = (14, 30, 58)
NAVY2 = (20, 44, 84)
GOLD = (201, 162, 39)
GOLD_LIGHT = (232, 196, 90)
PAPER = (250, 248, 242)
INK = (24, 28, 36)
GRAY = (92, 98, 110)
WHITE = (255, 255, 255)
RED = (179, 38, 30)
MAP_BG = (232, 240, 247)
MAP_DOT = (126, 166, 201)

REGION_COLORS = {
    "Middle East": (179, 38, 30),
    "Europe": (29, 78, 216),
    "Asia-Pacific": (14, 122, 91),
    "Americas": (194, 65, 12),
    "Africa": (124, 58, 237),
    "Economy": (71, 85, 105),
    "Science & Sport": (190, 24, 93),
}


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns a list of lines that fit max_w."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def fit_text(draw, text, fnt_path, size, max_w, min_size=11):
    """Shrink font until text fits on one line; then truncate with ellipsis."""
    s = size
    while s > min_size:
        f = font(fnt_path, s)
        if draw.textlength(text, font=f) <= max_w:
            return f, text
        s -= 1
    f = font(fnt_path, s)
    while text and draw.textlength(text + "…", font=f) > max_w:
        text = text[:-1]
    return f, text + "…"


# ---------------------------------------------------------------- panels
def panel_missiles(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(22, 35, 63))
    d.rectangle([x, y + h - 26, x + w, y + h], fill=(13, 60, 74))
    # skyline
    for bx, bw, bh in [(6, 18, 34), (30, 14, 48), (50, 22, 30), (78, 16, 42), (100, 20, 36)]:
        d.rectangle([x + bx, y + h - 26 - bh, x + bx + bw, y + h - 26], fill=(10, 20, 38))
    # missile arcs
    for (x0, y0, x1, y1) in [(8, 92, 62, 34), (30, 98, 88, 40), (58, 100, 118, 52)]:
        d.arc([x + x0 - 26, y + y0 - 52, x + x1 + 26, y + y1 + 52], 200, 340, fill=(255, 176, 66), width=4)
    # explosion starburst
    cx, cy = x + w - 26, y + 30
    for ang in range(0, 360, 30):
        r = 20
        ex = cx + int(r * math.cos(math.radians(ang)))
        ey = cy + int(r * math.sin(math.radians(ang)))
        d.line([cx, cy, ex, ey], fill=(255, 196, 66), width=3)
    d.ellipse([cx - 9, cy - 9, cx + 9, cy + 9], fill=(255, 214, 90))
    d.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill=(255, 255, 255))


def panel_summit(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(15, 61, 51))
    # table
    d.ellipse([x + 8, y + h - 52, x + w - 8, y + h - 8], fill=(8, 42, 36))
    d.ellipse([x + 20, y + h - 44, x + w - 20, y + h - 16], fill=(24, 84, 68))
    # flags around the table
    for i, col in enumerate([(179, 38, 30), (29, 78, 216), (201, 162, 39), (14, 122, 91), (124, 58, 237)]):
        fx = x + 16 + i * 22
        d.rectangle([fx, y + 44, fx + 14, y + 62], fill=col)
        d.line([fx + 7, y + 62, fx + 7, y + h - 46], fill=(220, 220, 220), width=2)
    # thermometer
    tx = x + w - 30
    d.rounded_rectangle([tx, y + 14, tx + 16, y + h - 30], radius=8, fill=(255, 255, 255))
    d.rounded_rectangle([tx + 3, y + 34, tx + 13, y + h - 33], radius=5, fill=(179, 38, 30))
    d.ellipse([tx - 3, y + h - 40, tx + 19, y + h - 18], fill=(179, 38, 30))


def panel_arrest(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(31, 41, 55))
    # searchlight beams
    d.polygon([(x + 10, y + 6), (x + 60, y + 6), (x + w - 10, y + h - 30), (x + 30, y + h - 30)], fill=(250, 220, 110))
    d.polygon([(x + w - 10, y + 6), (x + w - 60, y + 6), (x + 20, y + h - 30), (x + w - 40, y + h - 30)], fill=(120, 160, 250))
    # handcuffs
    cy = y + h // 2 + 12
    d.ellipse([x + 28, cy - 18, x + 64, cy + 18], outline=(255, 255, 255), width=6)
    d.ellipse([x + w - 64, cy - 18, x + w - 28, cy + 18], outline=(255, 255, 255), width=6)
    d.line([x + 64, cy, x + w - 64, cy], fill=(255, 255, 255), width=5)
    d.ellipse([x + w // 2 - 6, cy - 6, x + w // 2 + 6, cy + 6], fill=(255, 255, 255))
    # siren dots
    d.ellipse([x + 12, y + 12, x + 24, y + 24], fill=(239, 68, 68))
    d.ellipse([x + w - 24, y + 12, x + w - 12, y + 24], fill=(59, 130, 246))


def panel_summit3(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(18, 58, 92))
    # three flag panels
    fw = (w - 24) // 3
    # US: stripes + canton
    fx = x + 8
    for i in range(6):
        d.rectangle([fx, y + 12 + i * 7, fx + fw, y + 12 + i * 7 + 7], fill=(179, 38, 30) if i % 2 == 0 else (255, 255, 255))
    d.rectangle([fx, y + 12, fx + fw // 2, y + 33], fill=(29, 78, 216))
    # China: red + stars
    fx = x + 8 + fw + 4
    d.rectangle([fx, y + 12, fx + fw, y + 54], fill=(222, 41, 16))
    for sx, sy in [(8, 8), (20, 12), (26, 20), (20, 26), (10, 22)]:
        d.ellipse([fx + sx - 2, y + 12 + sy - 2, fx + sx + 2, y + 12 + sy + 2], fill=(255, 222, 0))
    # Russia: white/blue/red bands
    fx = x + 8 + 2 * (fw + 4)
    d.rectangle([fx, y + 12, fx + fw, y + 26], fill=(255, 255, 255))
    d.rectangle([fx, y + 26, fx + fw, y + 40], fill=(0, 57, 166))
    d.rectangle([fx, y + 40, fx + fw, y + 54], fill=(179, 38, 30))
    # three silhouettes
    for i in range(3):
        sx = x + 24 + i * 44
        d.ellipse([sx, y + h - 52, sx + 28, y + h - 24], fill=(10, 25, 45))
        d.pieslice([sx - 8, y + h - 26, sx + 36, y + h + 22], 180, 360, fill=(10, 25, 45))


def panel_markets(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(26, 26, 26))
    # candlesticks
    bars = [(16, 30, 52), (36, 22, 62), (56, 40, 74), (76, 52, 88), (96, 66, 100)]
    for bx, top, bot in bars:
        d.rectangle([x + bx, y + top, x + bx + 12, y + bot], fill=(220, 60, 60))
        d.line([x + bx + 6, y + top - 8, x + bx + 6, y + bot + 8], fill=(220, 60, 60), width=2)
    # falling arrow
    d.line([x + 8, y + 22, x + w - 30, y + h - 34], fill=(255, 214, 90), width=5)
    d.polygon([(x + w - 34, y + h - 48), (x + w - 8, y + h - 42), (x + w - 30, y + h - 16)], fill=(255, 214, 90))
    f = font(F_BOLD, 22)
    d.text((x + 10, y + h - 30), "-3.7%", font=f, fill=(255, 255, 255))


def panel_ship(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(44, 62, 80))
    # sea
    d.rectangle([x, y + h - 34, x + w, y + h], fill=(23, 52, 74))
    for wy in (h - 26, h - 16):
        for wx in range(0, w, 24):
            d.arc([x + wx, y + wy - 6, x + wx + 22, y + wy + 6], 180, 360, fill=(180, 210, 235), width=2)
    # ship hull + containers
    d.polygon([(x + 14, y + h - 34), (x + w - 14, y + h - 34), (x + w - 30, y + h - 14), (x + 30, y + h - 14)], fill=(12, 24, 38))
    for i, col in enumerate([(179, 38, 30), (29, 78, 216), (201, 162, 39)]):
        d.rectangle([x + 26 + i * 26, y + h - 62, x + 26 + i * 26 + 22, y + h - 36], fill=col)
    # fire plume
    cx = x + w - 34
    d.polygon([(cx - 12, y + h - 60), (cx, y + 18), (cx + 12, y + h - 60)], fill=(255, 140, 40))
    d.polygon([(cx - 6, y + h - 60), (cx, y + 34), (cx + 6, y + h - 60)], fill=(255, 214, 90))
    d.ellipse([cx - 16, y + 12, cx + 4, y + 32], fill=(120, 120, 120))
    d.ellipse([cx - 4, y + 4, cx + 16, y + 24], fill=(150, 150, 150))


PANELS = {
    "missiles": panel_missiles,
    "summit": panel_summit,
    "arrest": panel_arrest,
    "summit3": panel_summit3,
    "markets": panel_markets,
    "ship": panel_ship,
}

# Extra panels used as small region icons / spare illustrations.
def panel_fire(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(60, 20, 16))
    d.polygon([(x + w // 2, y + 10), (x + w - 16, y + h - 20), (x + 16, y + h - 20)], fill=(255, 140, 40))
    d.polygon([(x + w // 2, y + 34), (x + w - 26, y + h - 20), (x + 26, y + h - 20)], fill=(255, 214, 90))


def panel_quake(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(58, 48, 30))
    d.rectangle([x, y + h - 30, x + w, y + h], fill=(40, 32, 20))
    pts = [(x + 10, y + 12), (x + 40, y + 40), (x + 30, y + 60), (x + 60, y + 78), (x + 48, y + 100), (x + 80, y + h - 30)]
    d.line(pts, fill=(255, 255, 255), width=4, joint="curve")
    d.polygon([(x + 84, y + 20), (x + 104, y + 20), (x + 104, y + 52), (x + 84, y + 52)], fill=(140, 120, 90))
    d.polygon([(x + 88, y + 52), (x + 100, y + 52), (x + 100, y + 64), (x + 88, y + 64)], fill=(140, 120, 90))


def panel_flood(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(23, 68, 110))
    for wy in (30, 55, 80, 104):
        for wx in range(0, w, 28):
            d.arc([x + wx, y + wy - 8, x + wx + 26, y + wy + 8], 180, 360, fill=(180, 220, 245), width=3)
    d.polygon([(x + 20, y + 18), (x + 44, y + 18), (x + 38, y + 30), (x + 26, y + 30)], fill=(255, 255, 255))


def panel_sport(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(22, 90, 60))
    d.ellipse([x + w // 2 - 34, y + h // 2 - 34, x + w // 2 + 34, y + h // 2 + 34], fill=(255, 255, 255))
    d.polygon([(x + w // 2, y + h // 2 - 34), (x + w // 2 + 28, y + h // 2 - 10), (x + w // 2 + 16, y + h // 2 + 26),
               (x + w // 2 - 16, y + h // 2 + 26), (x + w // 2 - 28, y + h // 2 - 10)], fill=(22, 90, 60))
    d.ellipse([x + w // 2 - 8, y + h // 2 - 8, x + w // 2 + 8, y + h // 2 + 8], fill=(255, 255, 255))


def panel_tech(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(30, 30, 60))
    cx, cy = x + w // 2, y + h // 2
    for ang in (0, 60, 120):
        d.arc([cx - 44, cy - 18, cx + 44, cy + 18], 0, 360, fill=(120, 180, 255), width=3)
    d.ellipse([cx - 8, cy - 8, cx + 8, cy + 8], fill=(255, 214, 90))
    d.ellipse([cx + 36, cy - 22, cx + 44, cy - 14], fill=(255, 255, 255))
    d.ellipse([cx - 40, cy + 12, cx - 32, cy + 20], fill=(255, 255, 255))


PANELS.update({
    "fire": panel_fire,
    "quake": panel_quake,
    "flood": panel_flood,
    "sport": panel_sport,
    "tech": panel_tech,
})


# ---------------------------------------------------------------- map
CONTINENTS = [
    # North America (lon, lat)
    [(-168, 66), (-140, 70), (-125, 72), (-110, 68), (-95, 69), (-85, 66), (-80, 73), (-65, 60), (-55, 52), (-60, 46), (-70, 42), (-75, 35), (-80, 26), (-85, 30), (-90, 21), (-97, 16), (-105, 20), (-115, 28), (-125, 40), (-125, 48), (-140, 60), (-155, 58), (-168, 66)],
    # South America
    [(-80, 10), (-75, 5), (-60, 5), (-50, 0), (-35, -8), (-40, -20), (-50, -30), (-60, -38), (-70, -52), (-73, -40), (-70, -20), (-80, -5), (-80, 10)],
    # Europe
    [(-10, 36), (-5, 44), (0, 50), (5, 58), (10, 58), (18, 56), (23, 60), (28, 58), (30, 45), (23, 40), (15, 38), (8, 44), (0, 44), (-10, 36)],
    # Africa
    [(-17, 15), (-10, 30), (0, 35), (10, 37), (20, 32), (30, 31), (35, 28), (43, 12), (51, 10), (48, 0), (40, -10), (35, -20), (30, -30), (20, -35), (15, -25), (12, -10), (9, 4), (-8, 5), (-17, 15)],
    # Asia
    [(30, 70), (50, 70), (70, 72), (90, 75), (110, 76), (130, 72), (150, 70), (170, 66), (178, 65), (170, 60), (160, 55), (155, 50), (140, 45), (130, 40), (127, 35), (120, 30), (110, 20), (105, 10), (100, 8), (95, 15), (90, 22), (80, 15), (75, 8), (70, 20), (60, 25), (50, 30), (45, 30), (40, 35), (35, 42), (30, 45), (30, 60), (30, 70)],
    # Australia
    [(113, -22), (114, -30), (120, -34), (130, -32), (140, -38), (150, -37), (153, -27), (146, -19), (142, -11), (135, -12), (130, -13), (122, -14), (114, -20), (113, -22)],
]


def point_in_poly(lon, lat, poly):
    inside = False
    n = len(poly)
    j = n - 1
    for i in range(n):
        xi, yi = poly[i]
        xj, yj = poly[j]
        if (yi > lat) != (yj > lat):
            xin = (xj - xi) * (lat - yi) / (yj - yi) + xi
            if lon < xin:
                inside = not inside
        j = i
    return inside


def draw_map(d, x0, y0, x1, y1):
    d.rectangle([x0, y0, x1, y1], fill=MAP_BG)
    lon0, lon1 = -180.0, 180.0
    lat0, lat1 = 75.0, -60.0
    step = 6
    px = x0 + 4
    while px < x1 - 4:
        py = y0 + 4
        while py < y1 - 4:
            lon = lon0 + (px - x0) / (x1 - x0) * (lon1 - lon0)
            lat = lat0 + (py - y0) / (y1 - y0) * (lat1 - lat0)
            if any(point_in_poly(lon, lat, c) for c in CONTINENTS):
                d.ellipse([px - 2, py - 2, px + 2, py + 2], fill=MAP_DOT)
            py += step
        px += step
    # pins
    f_pin = font(F_BOLD, 13)
    for num, lon, lat in MAP_PINS:
        px = x0 + (lon - lon0) / (lon1 - lon0) * (x1 - x0)
        py = y0 + (lat0 - lat) / (lat0 - lat1) * (y1 - y0)
        d.ellipse([px - 10, py - 10, px + 10, py + 10], fill=RED, outline=WHITE, width=2)
        tw = d.textlength(str(num), font=f_pin)
        d.text((px - tw / 2, py - 7), str(num), font=f_pin, fill=WHITE)


# ---------------------------------------------------------------- region icons (22x22, drawn in header bands)
def region_icon(d, region, x, y):
    col = REGION_COLORS[region]
    if region == "Middle East":  # flame
        d.polygon([(x + 11, y + 1), (x + 20, y + 14), (x + 11, y + 21), (x + 2, y + 14)], fill=(255, 140, 40))
        d.polygon([(x + 11, y + 9), (x + 17, y + 17), (x + 11, y + 21), (x + 5, y + 17)], fill=(255, 214, 90))
    elif region == "Europe":  # thermometer
        d.rounded_rectangle([x + 8, y + 1, x + 14, y + 16], radius=4, fill=WHITE)
        d.rectangle([x + 10, y + 8, x + 12, y + 15], fill=RED)
        d.ellipse([x + 6, y + 14, x + 16, y + 22], fill=RED)
    elif region == "Asia-Pacific":  # mountain + sun
        d.polygon([(x + 1, y + 21), (x + 11, y + 5), (x + 21, y + 21)], fill=WHITE)
        d.ellipse([x + 15, y + 1, x + 21, y + 7], fill=GOLD_LIGHT)
    elif region == "Americas":  # quake crack
        d.line([(x + 3, y + 2), (x + 10, y + 9), (x + 7, y + 13), (x + 14, y + 18), (x + 11, y + 21)], fill=WHITE, width=3, joint="curve")
    elif region == "Africa":  # wave
        for wy in (6, 13, 20):
            d.arc([x + 1, y + wy - 4, x + 21, y + wy + 4], 180, 360, fill=WHITE, width=2)
    elif region == "Economy":  # bars
        for i, bh in enumerate((6, 11, 16)):
            d.rectangle([x + 3 + i * 7, y + 21 - bh, x + 8 + i * 7, y + 21], fill=WHITE)
    else:  # Science & Sport: atom
        d.ellipse([x + 9, y + 9, x + 13, y + 13], fill=GOLD_LIGHT)
        d.ellipse([x + 2, y + 6, x + 20, y + 16], outline=WHITE, width=2)
        d.ellipse([x + 2, y + 6, x + 20, y + 16], outline=WHITE, width=2)


# ---------------------------------------------------------------- build
def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- masthead (0..92): navy gradient + gold rule + hatch texture
    for yy in range(92):
        t = yy / 92
        r = int(NAVY[0] + (NAVY2[0] - NAVY[0]) * t)
        g = int(NAVY[1] + (NAVY2[1] - NAVY[1]) * t)
        b = int(NAVY[2] + (NAVY2[2] - NAVY[2]) * t)
        d.line([(0, yy), (W, yy)], fill=(r, g, b))
    for hx in range(-92, W, 26):
        d.line([(hx, 92), (hx + 92, 0)], fill=(24, 48, 88), width=2)
    d.rectangle([0, 90, W, 92], fill=GOLD)

    f_title = font(F_SERIF_BOLD, 56)
    f_sub = font(F_BOLD, 22)
    f_date1 = font(F_BOLD, 26)
    f_date2 = font(F_REG, 20)
    d.text((16, 8), TITLE, font=f_title, fill=WHITE)
    d.text((16, 62), SUBTITLE, font=f_sub, fill=GOLD_LIGHT)
    d.text((700, 10), "SUNDAY", font=f_date1, fill=WHITE)
    d.text((700, 44), "22 NOVEMBER 2026", font=f_date2, fill=GOLD_LIGHT)

    # ---- stat strip (92..124)
    d.rectangle([0, 92, W, 124], fill=GOLD)
    f_stat = font(F_BOLD, 15)
    n_top = sum(1 for s in STORIES if s["top"])
    stat_left = f"{len(STORIES)} STORIES  •  {len(REGIONS)} REGIONS  •  {n_top} TOP STORIES  •  13 PICTURES"
    d.text((16, 101), stat_left, font=f_stat, fill=NAVY)
    f_check = font(F_BOLD, 13)
    check = "CHECKED: ALL EVENTS 22 NOV 2026"
    tw = d.textlength(check, font=f_check)
    d.text((W - 16 - tw, 103), check, font=f_check, fill=NAVY)

    # ---- top stories grid (124..518): 2 cols x 3 rows, cells 500x126
    top = [s for s in STORIES if s["top"]]
    f_kick = font(F_BOLD, 12)
    f_head = font(F_BOLD, 19)
    f_deck = font(F_REG, 13)
    for i, s in enumerate(top):
        cx = 8 + (i % 2) * 508
        cy = 124 + (i // 2) * 132
        cw, ch = 500, 126
        d.rectangle([cx, cy, cx + cw, cy + ch], fill=WHITE, outline=(210, 208, 198), width=1)
        # panel
        PANELS[s["panel"]](d, cx + 1, cy + 1, 138, ch - 2)
        # number badge
        bx, by = cx + 8, cy + 8
        d.ellipse([bx, by, bx + 26, by + 26], fill=RED, outline=WHITE, width=2)
        f_num = font(F_BOLD, 15)
        num = str(i + 1)
        d.text((bx + 13 - d.textlength(num, font=f_num) / 2, by + 4), num, font=f_num, fill=WHITE)
        # text
        tx = cx + 150
        tw_text = cw - 150 - 10
        col = REGION_COLORS[s["region"]]
        d.text((tx, cy + 8), f"{i + 1} · {s['region'].upper()}", font=f_kick, fill=col)
        lines = wrap(d, s["title"], f_head, tw_text)[:2]
        ly = cy + 28
        for ln in lines:
            d.text((tx, ly), ln, font=f_head, fill=INK)
            ly += 24
        dlines = wrap(d, s["deck"], f_deck, tw_text)[:3]
        for ln in dlines:
            d.text((tx, ly), ln, font=f_deck, fill=GRAY)
            ly += 17

    # ---- world map strip (526..622)
    d.rectangle([8, 526, 1016, 622], outline=(210, 208, 198), width=1)
    draw_map(d, 9, 527, 1015, 621)

    # ---- briefs band (630..1016): 3 columns, 10 briefs each
    briefs = [s for s in STORIES if not s["top"]]
    cols = [briefs[i * 10:(i + 1) * 10] for i in range(3)]
    f_rhead = font(F_BOLD, 13)
    f_btitle = font(F_BOLD, 14)
    f_bdeck = font(F_REG, 12)
    for ci, col_stories in enumerate(cols):
        x = 8 + ci * 338
        y = 630
        cur_region = None
        for s in col_stories:
            if s["region"] != cur_region:
                cur_region = s["region"]
                col = REGION_COLORS[cur_region]
                d.rectangle([x, y, x + 330, y + 22], fill=col)
                region_icon(d, cur_region, x + 4, y + 1)
                d.text((x + 30, y + 4), cur_region.upper(), font=f_rhead, fill=WHITE)
                y += 22
            # brief: title (fit) + deck (fit, one line)
            tf, title = fit_text(d, s["title"], F_BOLD, 14, 330 - 8)
            d.text((x + 4, y + 1), title, font=tf, fill=INK)
            df, deck = fit_text(d, s["deck"], F_REG, 12, 330 - 8)
            d.text((x + 4, y + 15), deck, font=df, fill=GRAY)
            y += 30
        # column rule
        d.line([(x + 330, 630), (x + 330, 1016)], fill=(220, 218, 208), width=1)

    img.save(OUT, format="PNG")
    print(f"wrote {OUT} ({OUT.stat().st_size} bytes)")


if __name__ == "__main__":
    build()
