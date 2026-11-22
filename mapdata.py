"""Dotted world map data, plotted by hand.

Grid: 60 columns (longitude -180..180, 6 degrees each) by 30 rows
(latitude 84..-60, about 4.8 degrees each). Each entry lists the inclusive
column ranges that are land on that row. The renderer draws one dot per
land cell and projects story pins with the same equirectangular mapping.
"""

COLS = 60
ROWS = 30
LAT_TOP = 84.0
LAT_BOTTOM = -60.0

# row -> [(col_start, col_end), ...] inclusive
LAND = {
    0: [(10, 16), (20, 25), (31, 34), (40, 59)],
    1: [(1, 6), (8, 18), (20, 26), (36, 59)],
    2: [(2, 6), (7, 19), (20, 25), (26, 27), (32, 59)],
    3: [(2, 6), (7, 20), (21, 23), (30, 59)],
    4: [(2, 5), (8, 20), (22, 23), (30, 59)],
    5: [(8, 20), (29, 59)],
    6: [(9, 20), (28, 59)],
    7: [(9, 19), (28, 54)],
    8: [(9, 18), (30, 53)],
    9: [(9, 17), (28, 53)],
    10: [(10, 16), (28, 53)],
    11: [(10, 15), (28, 39), (41, 44), (45, 50)],
    12: [(12, 15), (28, 39), (42, 44), (45, 48)],
    13: [(14, 16), (27, 35), (42, 43), (45, 47)],
    14: [(15, 16), (27, 36), (45, 47)],
    15: [(17, 20), (27, 37), (45, 49)],
    16: [(17, 21), (28, 37), (45, 50)],
    17: [(16, 24), (28, 37), (46, 53)],
    18: [(17, 24), (31, 36), (48, 53)],
    19: [(17, 23), (32, 36), (51, 54)],
    20: [(18, 23), (32, 36), (49, 55)],
    21: [(18, 23), (32, 35), (48, 55)],
    22: [(18, 22), (32, 35), (48, 55)],
    23: [(18, 21), (32, 35), (49, 55)],
    24: [(18, 20), (32, 35), (49, 54)],
    25: [(17, 20), (53, 55), (57, 59)],
    26: [(17, 19), (57, 59)],
    27: [(17, 19)],
    28: [(17, 18)],
    29: [(18, 19)],
}

# Small nudges (dx, dy in pixels) for pins that would otherwise collide
# in the crowded Europe / Middle East cluster. Keyed by story id.
PIN_NUDGE = {
    1: (-7, -5),   # Antalya
    2: (7, -3),    # Bahrain
    4: (6, -6),    # Kyiv
    5: (0, -6),    # Gulf of Finland
    10: (-9, 3),   # Brussels
    11: (9, 5),    # Twickenham
    13: (7, 7),    # Gaza
}


def project(lat, lon, width, height):
    """Equirectangular projection onto a box of width x height."""
    x = (lon + 180.0) / 360.0 * width
    y = (LAT_TOP - lat) / (LAT_TOP - LAT_BOTTOM) * height
    return x, y


def land_cells():
    """Yield (col, row) for every land cell."""
    for row, ranges in LAND.items():
        for c0, c1 in ranges:
            for col in range(c0, c1 + 1):
                yield col, row
