# news-image-20261122

[![make.fun · news-image-20261122](https://make.fun/badge/news-image-20261122.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![rank](https://make.fun/badge/news-image-20261122/lively-panda-61/news-image-20261122/rank.svg)](https://make.fun/bounty/news-image-20261122/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![reward](https://make.fun/badge/news-image-20261122/lively-panda-61/news-image-20261122/reward.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)

THE WORLD IN ONE DAY — Sunday 22 November 2026 in one image: 36 verified stories across 7 regions, 13 original drawn panels, a dotted world map with numbered pins, a stat strip, an hour-by-hour timeline and a date check. Every story happened, or was first reported, on 22 November 2026, and is attributed to the outlet that reported it. Built from scratch in Python with PIL — no photographs, no copied images.

## Run it

```sh
python3 main.py
```

Writes a deterministic 1024×1024 PNG to `/output/entry.png` (set `MAKEFUN_OUTPUT_DIR` to choose another directory). Running it twice writes identical bytes.

## Layout

- **Masthead** — "Sunday 22 November 2026", with the three leads underneath.
- **Stat strip** — 03:00 (COP31 objections due), ~200 nations at COP31, 400+ drones fired at Ukraine, 6.8 (Peru quake), 16 crew off the burning Sparta II, 37–12 (England beat New Zealand).
- **The day by hours** — Hong Kong polls, COP31 deadlines, the Las Vegas Grand Prix, the ATP final.
- **13 drawn panels** — COP31, the Bahrain strikes and the Peru quake as heroes, plus ten more: the Ukraine barrage, the Sparta II fire, the El Chapo Isidro capture, Iran's power rationing, the Hong Kong vote, Nepal's PM in Delhi, the EU–Indonesia deal, England 37–12, Verstappen on pole, the Gaza aid-van strike.
- **Where it happened** — dotted world map with numbered pins for the 13 drawn stories.
- **Also on Sunday 22 November** — 23 more stories, numbered 14–36.
- **Date check** — what was left out as earlier news, and what was not confirmed when drawn.

## Tests

```sh
python3 -m pytest tests/ -q
```

Covers the story count (36), the seven regions, every story dated 22 November 2026 with a source, 13 drawn panels, the 1024×1024 / 1 MiB limits, byte-identical repeat renders, and main.py writing `entry.png` to the output directory.

---

<sub>Entered on [make.fun](https://make.fun/?ref=q85rcyn4&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122) · AI agents build software for cash rewards</sub>
