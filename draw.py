"""Render the Sunday 22 November 2026 front page as a 1024x1024 PNG.

All artwork is drawn here with PIL primitives (flat vector-style panels);
no photographs, no copied images. The render is fully deterministic:
same input stories always produce the same bytes.
"""
import os

from PIL import Image, ImageDraw, ImageFont

import mapdata
import stories

W, H = 1024, 1024
PAPER = (247, 242, 231)
INK = (26, 26, 26)
RED = (163, 22, 33)
RED_DARK = (139, 26, 26)
GRAY = (85, 85, 85)
LIGHT_GRAY = (120, 120, 120)
RULE = (60, 60, 60)

SERIF_B = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf"
SERIF_I = "/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf"
DSERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

_font_cache = {}


def font(path, size):
    key = (path, size)
    if key not in _font_cache:
        try:
            _font_cache[key] = ImageFont.truetype(path, size)
        except OSError:
            _font_cache[key] = ImageFont.load_default()
    return _font_cache[key]


def wrap(d, text, fnt, max_w):
    """Greedy word wrap; returns a list of lines that fit max_w."""
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = f"{cur} {word}".strip()
        if d.textlength(trial, font=fnt) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_wrapped(d, x, y, text, fnt, max_w, fill=INK, leading=None):
    """Draw wrapped text; returns the y just below the last line."""
    if leading is None:
        leading = int(fnt.size * 1.25)
    for line in wrap(d, text, fnt, max_w):
        d.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def fit_lines(d, text, fnt, max_w, max_lines):
    """Wrap text and clip to max_lines, adding an ellipsis if clipped."""
    lines = wrap(d, text, fnt, max_w)
    if len(lines) > max_lines:
        lines = lines[:max_lines]
        while lines and d.textlength(lines[-1] + "…", font=fnt) > max_w:
            lines[-1] = lines[-1][:-1]
        lines[-1] += "…"
    return lines


# ---------------------------------------------------------------- panels
# Each drawing routine paints flat vector art into the box (x, y, w, h).

def p_cop31(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(207, 227, 232))
    d.rectangle([x, y + h - 26, x + w, y + h], fill=(122, 84, 52))
    # globe
    cx, cy, r = x + w * 0.30, y + h * 0.42, h * 0.30
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(74, 144, 194), outline=INK, width=2)
    d.ellipse([cx - r * 0.55, cy - r * 0.6, cx - r * 0.05, cy - r * 0.1], fill=(90, 164, 105))
    d.ellipse([cx + r * 0.1, cy + r * 0.15, cx + r * 0.6, cy + r * 0.6], fill=(90, 164, 105))
    # delegates at the table
    for i in range(5):
        dx = x + w * (0.52 + i * 0.10)
        d.ellipse([dx, y + h - 52, dx + 16, y + h - 36], fill=(200, 60, 60) if i % 2 else (40, 90, 140))
        d.rectangle([dx + 2, y + h - 36, dx + 14, y + h - 26], fill=(240, 240, 235))
    # clock
    ccx, ccy, cr = x + w * 0.86, y + h * 0.28, 20
    d.ellipse([ccx - cr, ccy - cr, ccx + cr, ccy + cr], fill=(255, 255, 255), outline=INK, width=2)
    d.line([ccx, ccy, ccx, ccy - cr + 5], fill=INK, width=2)
    d.line([ccx, ccy, ccx + cr - 8, ccy + 4], fill=INK, width=2)


def p_bahrain(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(28, 39, 51))
    # buildings
    for bx, bw, bh in [(0.05, 0.16, 0.45), (0.24, 0.12, 0.60), (0.40, 0.18, 0.38), (0.62, 0.14, 0.55)]:
        d.rectangle([x + w * bx, y + h - bh * h - 12, x + w * (bx + bw), y + h - 12], fill=(46, 58, 70))
    # flames
    fx = x + w * 0.55
    for i, (fw, fh, col) in enumerate([(46, 58, (230, 120, 30)), (30, 40, (245, 180, 40)), (16, 24, (255, 230, 120))]):
        d.polygon([(fx - fw // 2 + i * 4, y + h - 12), (fx + i * 3, y + h - 12 - fh), (fx + fw // 2 + i * 4, y + h - 12)], fill=col)
    # smoke
    for sx, sy, sr in [(0.30, 0.25, 12), (0.36, 0.18, 15), (0.72, 0.22, 13)]:
        d.ellipse([x + w * sx - sr, y + h * sy - sr, x + w * sx + sr, y + h * sy + sr], fill=(120, 120, 120))
    # ground fire glow
    d.rectangle([x, y + h - 12, x + w, y + h], fill=(60, 40, 30))


def p_quake(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(223, 232, 238))
    # mountains
    d.polygon([(x, y + h), (x + w * 0.28, y + h * 0.30), (x + w * 0.52, y + h)], fill=(122, 96, 74))
    d.polygon([(x + w * 0.38, y + h), (x + w * 0.66, y + h * 0.18), (x + w, y + h)], fill=(96, 76, 60))
    # snow caps
    d.polygon([(x + w * 0.22, y + h * 0.42), (x + w * 0.28, y + h * 0.30), (x + w * 0.34, y + h * 0.42)], fill=(255, 255, 255))
    d.polygon([(x + w * 0.60, y + h * 0.32), (x + w * 0.66, y + h * 0.18), (x + w * 0.72, y + h * 0.32)], fill=(255, 255, 255))
    # seismograph strip
    sy = y + h * 0.68
    d.rectangle([x + 8, sy, x + w - 8, sy + 26], fill=(255, 255, 255), outline=INK, width=1)
    pts = []
    import math
    for i in range(41):
        px = x + 10 + i * (w - 20) / 40
        py = sy + 13 + math.sin(i * 1.7) * (3 if i % 7 else 10)
        pts.append((px, py))
    d.line(pts, fill=(163, 22, 33), width=2)
    # magnitude badge
    d.rectangle([x + w - 66, y + 8, x + w - 8, y + 30], fill=(26, 26, 26))
    d.text((x + w - 60, y + 11), "M 6.8", font=font(SANS_B, 13), fill=(255, 255, 255))


def p_barrage(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(20, 28, 38))
    # skyline
    for bx, bw, bh in [(0.02, 0.14, 0.42), (0.18, 0.12, 0.58), (0.32, 0.16, 0.36), (0.50, 0.12, 0.52), (0.64, 0.14, 0.40), (0.80, 0.16, 0.48)]:
        d.rectangle([x + w * bx, y + h - bh * h - 10, x + w * (bx + bw), y + h - 10], fill=(38, 48, 60))
        for wy in range(3):
            d.rectangle([x + w * bx + 4, y + h - bh * h + 6 + wy * 12, x + w * bx + 8, y + h - bh * h + 10 + wy * 12], fill=(245, 200, 80))
    # drones with trails
    for dx, dy in [(0.20, 0.18), (0.45, 0.12), (0.68, 0.22), (0.85, 0.14)]:
        d.line([x + w * dx, y + h * dy + 26, x + w * dx, y + h * dy], fill=(200, 200, 200), width=1)
        d.ellipse([x + w * dx - 3, y + h * dy - 3, x + w * dx + 3, y + h * dy + 3], fill=(255, 220, 120))
    # fire glow
    d.polygon([(x + w * 0.30, y + h - 10), (x + w * 0.38, y + h - 34), (x + w * 0.46, y + h - 10)], fill=(230, 120, 30))
    d.polygon([(x + w * 0.70, y + h - 10), (x + w * 0.76, y + h - 26), (x + w * 0.82, y + h - 10)], fill=(245, 180, 40))


def p_ship(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h * 0.62], fill=(168, 196, 208))
    d.rectangle([x, y + h * 0.62, x + w, y + h], fill=(110, 150, 168))
    # waves
    for wy in [0.70, 0.82, 0.93]:
        for wx in range(0, 10):
            d.arc([x + wx * w / 10, y + h * wy, x + (wx + 1) * w / 10, y + h * wy + 12], 180, 360, fill=(255, 255, 255), width=2)
    # freighter
    d.polygon([(x + w * 0.08, y + h * 0.60), (x + w * 0.92, y + h * 0.60), (x + w * 0.86, y + h * 0.78), (x + w * 0.14, y + h * 0.78)], fill=(40, 40, 44))
    d.rectangle([x + w * 0.08, y + h * 0.56, x + w * 0.92, y + h * 0.60], fill=(140, 30, 30))
    for i, col in enumerate([(200, 80, 40), (60, 120, 180), (220, 170, 50), (90, 160, 90)]):
        d.rectangle([x + w * (0.14 + i * 0.19), y + h * 0.40, x + w * (0.30 + i * 0.19), y + h * 0.56], fill=col, outline=INK, width=1)
    # flames on deck
    fx = x + w * 0.55
    d.polygon([(fx - 22, y + h * 0.42), (fx, y + h * 0.18), (fx + 22, y + h * 0.42)], fill=(230, 120, 30))
    d.polygon([(fx - 12, y + h * 0.42), (fx, y + h * 0.26), (fx + 12, y + h * 0.42)], fill=(255, 210, 90))
    d.ellipse([x + w * 0.68 - 12, y + h * 0.10 - 12, x + w * 0.68 + 12, y + h * 0.10 + 12], fill=(120, 120, 120))


def p_cuffs(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(214, 200, 170))
    d.ellipse([x + w * 0.14, y + h * 0.30, x + w * 0.42, y + h * 0.78], outline=(60, 60, 60), width=6)
    d.ellipse([x + w * 0.58, y + h * 0.30, x + w * 0.86, y + h * 0.78], outline=(60, 60, 60), width=6)
    d.ellipse([x + w * 0.22, y + h * 0.40, x + w * 0.34, y + h * 0.68], outline=(60, 60, 60), width=3)
    d.ellipse([x + w * 0.66, y + h * 0.40, x + w * 0.78, y + h * 0.68], outline=(60, 60, 60), width=3)
    # chain links
    for i in range(4):
        lx = x + w * (0.44 + i * 0.04)
        d.ellipse([lx, y + h * 0.50, lx + 10, y + h * 0.62], outline=(60, 60, 60), width=3)
    # map pin
    px, py = x + w * 0.82, y + h * 0.22
    d.ellipse([px - 8, py - 8, px + 8, py + 8], fill=RED)
    d.polygon([(px - 6, py + 4), (px + 6, py + 4), (px, py + 16)], fill=RED)


def p_power(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(38, 52, 84))
    # pylon
    px = x + w * 0.30
    d.polygon([(px - 26, y + h), (px, y + h * 0.18), (px + 26, y + h)], outline=(220, 220, 220), width=3)
    d.line([px - 26, y + h - 8, px + 26, y + h - 8], fill=(220, 220, 220), width=2)
    d.line([px - 34, y + h * 0.30, px + 34, y + h * 0.30], fill=(220, 220, 220), width=2)
    d.line([px - 20, y + h * 0.55, px + 20, y + h * 0.55], fill=(220, 220, 220), width=2)
    # lightning bolt
    bx = x + w * 0.68
    d.polygon([(bx + 8, y + h * 0.15), (bx - 12, y + h * 0.55), (bx + 2, y + h * 0.55), (bx - 8, y + h * 0.88), (bx + 14, y + h * 0.48), (bx, y + h * 0.48)], fill=(255, 210, 60))
    # clock badge
    d.ellipse([x + w - 44, y + 8, x + w - 12, y + 40], fill=(255, 255, 255), outline=INK, width=2)
    d.text((x + w - 38, y + 16), "2h", font=font(SANS_B, 12), fill=INK)


def p_ballot(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(232, 226, 210))
    # ballot box
    d.rectangle([x + w * 0.18, y + h * 0.42, x + w * 0.62, y + h * 0.90], fill=(163, 22, 33), outline=INK, width=2)
    d.rectangle([x + w * 0.30, y + h * 0.36, x + w * 0.50, y + h * 0.42], fill=(255, 255, 255), outline=INK, width=1)
    # ballot paper with check
    d.polygon([(x + w * 0.52, y + h * 0.10), (x + w * 0.78, y + h * 0.06), (x + w * 0.80, y + h * 0.42), (x + w * 0.56, y + h * 0.44)], fill=(255, 255, 255), outline=INK, width=1)
    d.line([x + w * 0.60, y + h * 0.28, x + w * 0.66, y + h * 0.36, x + w * 0.76, y + h * 0.16], fill=(30, 140, 60), width=4)
    d.text((x + w * 0.24, y + h * 0.56), "VOTE", font=font(SANS_B, 16), fill=(255, 255, 255))


def p_plane(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(190, 220, 235))
    d.ellipse([x + w * 0.74, y + h * 0.10, x + w * 0.90, y + h * 0.32], fill=(255, 240, 180))
    # plane silhouette: slim fuselage, swept wings, tail
    d.polygon([(x + w * 0.10, y + h * 0.52), (x + w * 0.62, y + h * 0.44),
               (x + w * 0.90, y + h * 0.50), (x + w * 0.62, y + h * 0.56),
               (x + w * 0.44, y + h * 0.62), (x + w * 0.30, y + h * 0.56)],
              fill=(40, 60, 90))
    d.polygon([(x + w * 0.34, y + h * 0.48), (x + w * 0.42, y + h * 0.28),
               (x + w * 0.50, y + h * 0.48)], fill=(40, 60, 90))
    d.polygon([(x + w * 0.14, y + h * 0.50), (x + w * 0.10, y + h * 0.34),
               (x + w * 0.18, y + h * 0.48)], fill=(40, 60, 90))
    # clouds
    for cx, cy in [(0.10, 0.18), (0.55, 0.14), (0.62, 0.78)]:
        d.ellipse([x + w * cx, y + h * cy, x + w * cx + 30, y + h * cy + 10], fill=(255, 255, 255))


def p_trade(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(232, 236, 228))
    # EU flag
    d.rectangle([x + w * 0.08, y + h * 0.18, x + w * 0.38, y + h * 0.52], fill=(0, 51, 153))
    for i in range(8):
        import math
        a = i * math.pi / 4
        sx = x + w * 0.23 + 22 * math.cos(a)
        sy = y + h * 0.35 + 12 * math.sin(a)
        d.ellipse([sx - 2, sy - 2, sx + 2, sy + 2], fill=(255, 204, 0))
    # Indonesia flag
    d.rectangle([x + w * 0.58, y + h * 0.18, x + w * 0.88, y + h * 0.52], fill=(255, 255, 255), outline=INK, width=1)
    d.rectangle([x + w * 0.58, y + h * 0.18, x + w * 0.88, y + h * 0.35], fill=(200, 30, 30))
    # rising arrow chart
    d.line([x + w * 0.12, y + h * 0.82, x + w * 0.38, y + h * 0.70, x + w * 0.60, y + h * 0.74, x + w * 0.88, y + h * 0.58], fill=(30, 140, 60), width=3)
    d.polygon([(x + w * 0.88, y + h * 0.58), (x + w * 0.80, y + h * 0.56), (x + w * 0.86, y + h * 0.66)], fill=(30, 140, 60))


def p_rugby(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(46, 125, 60))
    for i in range(4):
        d.line([x, y + h * (0.25 + i * 0.22), x + w, y + h * (0.25 + i * 0.22)], fill=(255, 255, 255), width=2)
    # posts
    px = x + w * 0.72
    d.line([px, y + h * 0.15, px, y + h * 0.75], fill=(255, 255, 255), width=3)
    d.line([px - 22, y + h * 0.15, px - 22, y + h * 0.42], fill=(255, 255, 255), width=3)
    d.line([px + 22, y + h * 0.15, px + 22, y + h * 0.42], fill=(255, 255, 255), width=3)
    d.line([px - 22, y + h * 0.42, px + 22, y + h * 0.42], fill=(255, 255, 255), width=3)
    # ball
    d.ellipse([x + w * 0.14, y + h * 0.55, x + w * 0.38, y + h * 0.82], fill=(139, 90, 43), outline=(255, 255, 255), width=2)
    d.line([x + w * 0.18, y + h * 0.68, x + w * 0.34, y + h * 0.68], fill=(255, 255, 255), width=2)


def p_f1(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h * 0.55], fill=(52, 44, 66))
    d.rectangle([x, y + h * 0.55, x + w, y + h], fill=(70, 70, 74))
    # floodlights
    for lx in [0.15, 0.5, 0.85]:
        d.line([x + w * lx, y + 6, x + w * lx, y + h * 0.30], fill=(200, 200, 200), width=2)
        d.ellipse([x + w * lx - 10, y + 2, x + w * lx + 10, y + 14], fill=(255, 240, 180))
    # checkered flag
    for r in range(2):
        for c in range(4):
            if (r + c) % 2 == 0:
                d.rectangle([x + w * 0.82 + c * 7, y + h * 0.62 + r * 7, x + w * 0.82 + c * 7 + 7, y + h * 0.62 + r * 7 + 7], fill=(26, 26, 26))
            else:
                d.rectangle([x + w * 0.82 + c * 7, y + h * 0.62 + r * 7, x + w * 0.82 + c * 7 + 7, y + h * 0.62 + r * 7 + 7], fill=(255, 255, 255))
    # race car
    cx, cy = x + w * 0.18, y + h * 0.72
    d.polygon([(cx, cy - 16), (cx + 26, cy - 16), (cx + 44, cy - 4), (cx + 108, cy - 4), (cx + 118, cy + 6), (cx, cy + 6)], fill=(200, 30, 40))
    d.polygon([(cx + 34, cy - 16), (cx + 44, cy - 30), (cx + 66, cy - 30), (cx + 74, cy - 16)], fill=(160, 20, 30))
    d.ellipse([cx + 14, cy - 2, cx + 34, cy + 14], fill=(20, 20, 20))
    d.ellipse([cx + 88, cy - 2, cx + 108, cy + 14], fill=(20, 20, 20))
    d.rectangle([cx + 108, cy - 22, cx + 116, cy - 4], fill=(200, 30, 40))


def p_aid(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(226, 222, 208))
    d.rectangle([x, y + h * 0.70, x + w, y + h], fill=(120, 120, 120))
    # van
    d.rectangle([x + w * 0.12, y + h * 0.34, x + w * 0.62, y + h * 0.70], fill=(255, 255, 255), outline=INK, width=2)
    d.polygon([(x + w * 0.62, y + h * 0.44), (x + w * 0.82, y + h * 0.52), (x + w * 0.82, y + h * 0.70), (x + w * 0.62, y + h * 0.70)], fill=(230, 230, 230), outline=INK, width=2)
    # red cross
    cx, cy = x + w * 0.37, y + h * 0.50
    d.rectangle([cx - 5, cy - 14, cx + 5, cy + 14], fill=RED)
    d.rectangle([cx - 14, cy - 5, cx + 14, cy + 5], fill=RED)
    # wheels
    for wx in [0.24, 0.72]:
        d.ellipse([x + w * wx - 9, y + h * 0.66 - 9, x + w * wx + 9, y + h * 0.66 + 9], fill=(30, 30, 30))
    # aid boxes
    for i, col in enumerate([(200, 160, 90), (160, 120, 70)]):
        d.rectangle([x + w * (0.84 - i * 0.02), y + h * (0.30 - i * 0.16), x + w * (0.96 - i * 0.02), y + h * (0.44 - i * 0.16)], fill=col, outline=INK, width=1)


PANELS = {
    "cop31": p_cop31, "bahrain": p_bahrain, "quake": p_quake, "barrage": p_barrage,
    "ship": p_ship, "cuffs": p_cuffs, "power": p_power, "ballot": p_ballot,
    "plane": p_plane, "trade": p_trade, "rugby": p_rugby, "f1": p_f1, "aid": p_aid,
}

TAGS = {
    "cop31": "COP31: DEAL CLOSE", "bahrain": "BAHRAIN: STRUCK", "quake": "PERU: QUAKE 6.8",
    "barrage": "400+ DRONES", "ship": "SHIP ABLAZE", "cuffs": "11 DEAD",
    "power": "POWER CUTS", "ballot": "5,700 VOTERS", "plane": "FIRST TRIP",
    "trade": "TRADE DEAL", "rugby": "37–12", "f1": "POLE", "aid": "AID VAN HIT",
}


def draw_tag(d, x, y, text, size=9):
    fnt = font(SANS_B, size)
    tw = d.textlength(text, font=fnt)
    d.rectangle([x, y, x + tw + 12, y + size + 8], fill=RED)
    d.text((x + 6, y + 4), text, font=fnt, fill=(255, 255, 255))


def draw_map(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(220, 232, 234), outline=INK, width=1)
    cw, ch = w / mapdata.COLS, h / mapdata.ROWS
    for col, row in mapdata.land_cells():
        cx, cy = x + (col + 0.5) * cw, y + (row + 0.5) * ch
        d.ellipse([cx - 2, cy - 2, cx + 2, cy + 2], fill=(176, 154, 94))
    # numbered pins for the 13 drawn stories
    for s in stories.STORIES:
        if not s.get("draw"):
            continue
        px, py = mapdata.project(s["lat"], s["lon"], w, h)
        px += x
        py += y
        dx, dy = mapdata.PIN_NUDGE.get(s["id"], (0, 0))
        px, py = px + dx, py + dy
        d.ellipse([px - 8, py - 8, px + 8, py + 8], fill=RED, outline=(255, 255, 255), width=1)
        num = str(s["id"])
        fnt = font(SANS_B, 9)
        tw = d.textlength(num, font=fnt)
        d.text((px - tw / 2, py - 6), num, font=fnt, fill=(255, 255, 255))


def render_poster():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    mx = 14  # side margin
    cw = W - 2 * mx  # 996 content width

    # top red band
    d.rectangle([0, 0, W, 4], fill=RED)
    # kicker
    d.text((mx, 10), "THE WORLD IN ONE DAY", font=font(SANS_B, 13), fill=RED)
    right = "36 STORIES · 7 REGIONS · EVERY ONE DATED SUNDAY 22 NOVEMBER 2026"
    f_k = font(SANS_B, 11)
    d.text((W - mx - d.textlength(right, font=f_k), 11), right, font=f_k, fill=INK)
    # masthead
    f_mast = font(SERIF_B, 54)
    mast = "Sunday 22 November 2026"
    d.text(((W - d.textlength(mast, font=f_mast)) / 2, 28), mast, font=f_mast, fill=INK)
    # sub-headline
    f_sub = font(SERIF_I, 15)
    sub = "COP31 nears a deal in Antalya  ·  Iran strikes US bases in Bahrain  ·  Peru quake 6.8"
    d.text(((W - d.textlength(sub, font=f_sub)) / 2, 88), sub, font=f_sub, fill=RED_DARK)
    # double rule
    d.line([mx, 106, W - mx, 106], fill=RULE, width=2)
    d.line([mx, 109, W - mx, 109], fill=RULE, width=1)

    # ---- stat strip ----
    y0 = 114
    cell = cw / 6
    f_num = font(SANS_B, 24)
    f_cap = font(SANS, 9)
    for i, (value, caption) in enumerate(stories.STATS):
        cx = mx + i * cell
        if i:
            d.line([cx, y0 + 2, cx, y0 + 34], fill=(200, 190, 170), width=1)
        d.text((cx + 8, y0), value, font=f_num, fill=RED)
        for j, line in enumerate(wrap(d, caption, f_cap, cell - 16)):
            d.text((cx + 8, y0 + 26 + j * 11), line, font=f_cap, fill=GRAY)
    d.line([mx, 152, W - mx, 152], fill=(200, 190, 170), width=1)

    # ---- timeline strip ----
    y0 = 156
    d.text((mx, y0), "THE DAY BY HOURS", font=font(SANS_B, 9), fill=RED)
    tx = mx + 128
    f_tl = font(SANS, 9)
    step = (cw - 128) / len(stories.TIMELINE)
    for i, (hh, what) in enumerate(stories.TIMELINE):
        label = f"{hh} — {what}"
        d.text((tx + i * step, y0), label, font=f_tl, fill=INK)

    # ---- region chips ----
    y0 = 174
    x = mx
    f_chip = font(SANS_B, 10)
    for name, count, color in stories.REGIONS:
        label = f"{name.upper()} {count}"
        tw = d.textlength(label, font=f_chip)
        d.rectangle([x, y0, x + tw + 16, y0 + 18], fill=color)
        d.text((x + 8, y0 + 3), label, font=f_chip, fill=(255, 255, 255))
        x += tw + 24

    # ---- hero row ----
    heroes = [s for s in stories.STORIES if s["id"] <= 3]
    hy, hw, hgap = 198, 324, 12
    img_h = 140
    for i, s in enumerate(heroes):
        x = mx + i * (hw + hgap)
        PANELS[s["draw"]](d, x, hy, hw, img_h)
        draw_tag(d, x + 6, hy + 6, TAGS[s["draw"]])
        ty = hy + img_h + 6
        d.text((x, ty), f"{s['id']}  {s['place']} · {s['topic']}", font=font(SANS_B, 10), fill=RED)
        ty += 14
        for line in fit_lines(d, s["headline"], font(DSERIF_B, 17), hw, 2):
            d.text((x, ty), line, font=font(DSERIF_B, 17), fill=INK)
            ty += 21
        ty += 2
        for line in fit_lines(d, s["summary"], font(SANS, 10), hw, 2):
            d.text((x, ty), line, font=font(SANS, 10), fill=(40, 40, 40))
            ty += 13
        ty += 2
        d.text((x, ty), f"({s['source']})", font=font(SANS, 8), fill=GRAY)

    # ---- small panels: 2 rows x 5 ----
    smalls = [s for s in stories.STORIES if 4 <= s["id"] <= 13]
    sw, sh, sgap = 192, 118, 8
    sy0 = 446
    for idx, s in enumerate(smalls):
        row, col = divmod(idx, 5)
        x = mx + col * (sw + sgap)
        y = sy0 + row * (sh + 8)
        PANELS[s["draw"]](d, x, y, sw, 52)
        draw_tag(d, x + 4, y + 4, TAGS[s["draw"]], size=8)
        ty = y + 52
        d.rectangle([x, ty, x + sw, ty + 13], fill=RED)
        d.text((x + 4, ty + 2), f"{s['id']} · {s['place']}", font=font(SANS_B, 8), fill=(255, 255, 255))
        ty += 16
        for line in fit_lines(d, s["headline"], font(SANS_B, 10), sw, 2):
            d.text((x, ty), line, font=font(SANS_B, 10), fill=INK)
            ty += 12
        for line in fit_lines(d, s["summary"], font(SANS, 9), sw, 2):
            d.text((x, ty), line, font=font(SANS, 9), fill=(40, 40, 40))
            ty += 11

    # ---- map + briefs ----
    y0 = 700
    d.text((mx, y0), "WHERE IT HAPPENED", font=font(SANS_B, 10), fill=INK)
    d.text((mx, y0 + 12), "pins match story numbers", font=font(SANS, 8), fill=GRAY)
    bx = mx + 312
    d.text((bx, y0), "ALSO ON SUNDAY 22 NOVEMBER — 23 MORE STORIES", font=font(SANS_B, 10), fill=INK)
    d.line([mx, y0 + 24, W - mx, y0 + 24], fill=RULE, width=1)
    my = y0 + 30
    mh = 210
    draw_map(d, mx, my, 296, mh)
    # briefs in 3 columns
    briefs = [s for s in stories.STORIES if s["id"] >= 14]
    cols = [briefs[0:8], briefs[8:16], briefs[16:23]]
    col_w = (W - mx - bx - 8) / 3
    f_b = font(SANS, 9)
    f_bn = font(SANS_B, 9)
    for ci, col in enumerate(cols):
        cx = bx + ci * (col_w + 4)
        by = my
        for s in col:
            num = f"{s['id']}"
            d.text((cx, by), num, font=f_bn, fill=RED)
            nx = cx + 18
            head = f"{s['place']} — {s['headline']} ({s['source']})"
            lines = fit_lines(d, head, f_b, col_w - 18, 3)
            for line in lines:
                d.text((nx, by), line, font=f_b, fill=INK)
                by += 12
            by += 3

    # ---- date check ----
    y0 = 946
    d.rectangle([mx, y0, W - mx, y0 + 46], outline=RED, width=2)
    d.text((mx + 8, y0 + 4), "DATE CHECK", font=font(SANS_B, 9), fill=RED)
    ty = draw_wrapped(d, mx + 8, y0 + 16, stories.DATE_CHECK.split("— ", 1)[1],
                      font(SANS, 9), W - 2 * mx - 16, leading=12)

    # ---- footer ----
    d.text((mx, 998), stories.FOOTER, font=font(SANS, 8), fill=GRAY)
    return img


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    img = render_poster()
    path = os.path.join(out_dir, "entry.png")
    img.save(path, format="PNG", optimize=True)
    print(f"wrote {path} ({os.path.getsize(path)} bytes, {img.size[0]}x{img.size[1]})")


if __name__ == "__main__":
    main()
