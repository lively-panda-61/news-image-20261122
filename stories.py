"""Story data for the Sunday 22 November 2026 front page (v2).

Every story happened, or was first reported, on Sunday 22 November 2026
in at least one time zone, and is attributed to the outlet that reported
it. Lead stories were checked against Reuters, Al Jazeera, CNN and USGS
reporting of the day; the rest match the day's wire record.
"""

DATE = "2026-11-22"

# Drawn-panel keys. Each maps to a drawing routine in draw.py.
DRAW_KEYS = {
    "cop31", "bahrain", "quake", "barrage", "ship", "cuffs", "power",
    "ballot", "plane", "trade", "rugby", "f1", "aid",
}

STORIES = [
    # ---- Drawn heroes (1-3) ----
    {"id": 1, "region": "Global", "place": "ANTALYA, TÜRKIYE", "topic": "CLIMATE",
     "headline": "COP31 nears a deal as a new text is tabled after overtime talks",
     "summary": "New package after a fight over fossil fuels; delegations have until 03:00 GMT to object before a final plenary.",
     "source": "Reuters, BBC", "lat": 36.9, "lon": 30.7, "draw": "cop31"},
    {"id": 2, "region": "Middle East", "place": "MANAMA, BAHRAIN", "topic": "IRAN WAR",
     "headline": "Iran strikes US bases in Bahrain",
     "summary": "Two waves of drones and missiles hit four US bases; a civilian site burns, no injuries. Tehran says it hit two Patriot radars.",
     "source": "Al Jazeera, Reuters", "lat": 26.0, "lon": 50.55, "draw": "bahrain"},
    {"id": 3, "region": "Americas", "place": "JUNÍN, PERU", "topic": "EARTHQUAKE",
     "headline": "Magnitude 6.8 quake shakes Peru's Andes",
     "summary": "The tremor sent Lima residents into the streets; first reports brought no word of deaths or major damage.",
     "source": "Reuters, USGS", "lat": -11.0, "lon": -76.0, "draw": "quake"},
    # ---- Drawn small panels (4-13) ----
    {"id": 4, "region": "Europe", "place": "KYIV, UKRAINE", "topic": "WAR",
     "headline": "Russia fires 400 drones and 110 missiles",
     "summary": "One of the war's largest overnight attacks; eight killed, Kyiv bridges hit.",
     "source": "Al Jazeera", "lat": 50.45, "lon": 30.52, "draw": "barrage"},
    {"id": 5, "region": "Europe", "place": "GULF OF FINLAND", "topic": "WAR AT SEA",
     "headline": "Russian cargo ship ablaze after drone strike",
     "summary": "Sparta II burns in Finnish waters; 16 crew off, Ukraine 'likely' behind it.",
     "source": "Reuters, Finnish Defence Forces", "lat": 59.9, "lon": 24.5, "draw": "ship"},
    {"id": 6, "region": "Americas", "place": "SINALOA, MEXICO", "topic": "CARTELS",
     "headline": "Mexico captures cartel boss 'El Chapo Isidro'",
     "summary": "Fausto Isidro Meza Flores seized in a raid; 11 killed in violence after.",
     "source": "Reuters, AP", "lat": 24.8, "lon": -107.4, "draw": "cuffs"},
    {"id": 7, "region": "Middle East", "place": "TEHRAN, IRAN", "topic": "ENERGY",
     "headline": "Iran begins rationing electricity from Sunday",
     "summary": "Cuts of up to two hours a day as gas output lags.",
     "source": "RFE/RL", "lat": 35.7, "lon": 51.4, "draw": "power"},
    {"id": 8, "region": "Asia-Pacific", "place": "HONG KONG", "topic": "VOTE",
     "headline": "Hong Kong goes to the polls",
     "summary": "About 5,700 voters pick the 1,500-seat body that chooses the city's leader.",
     "source": "AFP", "lat": 22.3, "lon": 114.2, "draw": "ballot"},
    {"id": 9, "region": "Asia-Pacific", "place": "NEW DELHI", "topic": "DIPLOMACY",
     "headline": "Nepal's new PM heads to India first",
     "summary": "Balendra Shah's first trip abroad: flood aid and energy top talks with Modi.",
     "source": "MEA, Radio Nepal", "lat": 28.6, "lon": 77.2, "draw": "plane"},
    {"id": 10, "region": "Global", "place": "BRUSSELS · JAKARTA", "topic": "TRADE",
     "headline": "EU–Indonesia sign trade deal",
     "summary": "The pact scraps 98.5% of tariffs after a decade of talks.",
     "source": "DW", "lat": 50.85, "lon": 4.35, "draw": "trade"},
    {"id": 11, "region": "Global", "place": "TWICKENHAM", "topic": "RUGBY",
     "headline": "England thrash the All Blacks 37–12",
     "summary": "A record margin of victory for England at Twickenham.",
     "source": "BBC", "lat": 51.45, "lon": -0.34, "draw": "rugby"},
    {"id": 12, "region": "Americas", "place": "LAS VEGAS", "topic": "FORMULA 1",
     "headline": "Verstappen on pole as Vegas races under the lights",
     "summary": "Antonelli drops five places; lights out 04:00 UTC.",
     "source": "F1", "lat": 36.17, "lon": -115.14, "draw": "f1"},
    {"id": 13, "region": "Middle East", "place": "GAZA", "topic": "AID",
     "headline": "Drone strike hits Gaza food-aid van, kills three",
     "summary": "IDF says it targeted Islamic Jihad members.",
     "source": "Al Jazeera, Gaza ministry", "lat": 31.5, "lon": 34.47, "draw": "aid"},
    # ---- Briefs (14-36) ----
    {"id": 14, "region": "Europe", "place": "ESTONIA",
     "headline": "Estonia to close its Russia border crossings",
     "summary": "Land crossings shut in December; Moscow cries 'Iron Curtain'.",
     "source": "Al Jazeera", "lat": 59.4, "lon": 24.7},
    {"id": 15, "region": "Europe", "place": "DENMARK",
     "headline": "Denmark expels Russian attaché over rapper kill plot",
     "summary": "Copenhagen says it foiled a Russian-backed plan to kill a Ukrainian rapper.",
     "source": "Guardian", "lat": 55.7, "lon": 12.6},
    {"id": 16, "region": "Europe", "place": "BELGIUM",
     "headline": "Belgium national strike to halt flights on Monday",
     "summary": "No regular air traffic 07:00–21:00, Skeyes says.",
     "source": "AFP", "lat": 50.85, "lon": 4.35},
    {"id": 17, "region": "Americas", "place": "WASHINGTON",
     "headline": "Trump seeks permanent Iran accord",
     "summary": "A deal to bar Tehran from nuclear arms.",
     "source": "Fox News", "lat": 38.9, "lon": -77.0},
    {"id": 18, "region": "Americas", "place": "WASHINGTON",
     "headline": "Trump plays down reported hack of FBI crime database",
     "summary": "The FBI has not confirmed the NCIC breach.",
     "source": "Reuters", "lat": 38.9, "lon": -77.0},
    {"id": 19, "region": "Americas", "place": "NEW YORK",
     "headline": "Nvidia faces US accounting probe",
     "summary": "The SEC inquiry is at an early stage.",
     "source": "Straits Times", "lat": 40.7, "lon": -74.0},
    {"id": 20, "region": "Americas", "place": "BRASÍLIA",
     "headline": "Bolsonaro in intensive care",
     "summary": "Ex-president stable after blockage.",
     "source": "Al Jazeera, Reuters", "lat": -15.8, "lon": -47.9},
    {"id": 21, "region": "Oceania", "place": "CANBERRA",
     "headline": "Marles rejects US report on AUKUS subs",
     "summary": "He says the budget office is wrong.",
     "source": "ABC, Reuters", "lat": -35.3, "lon": 149.1},
    {"id": 22, "region": "Asia-Pacific", "place": "RANCHI",
     "headline": "Cyclone Akvan cancels 14 flights at Ranchi",
     "summary": "The storm's remnants move inland over eastern India.",
     "source": "ANI", "lat": 23.3, "lon": 85.3},
    {"id": 23, "region": "Oceania", "place": "WELLINGTON",
     "headline": "India face New Zealand in windy Wellington Test",
     "summary": "Pant's 128 puts India on top on day four.",
     "source": "PTI", "lat": -41.3, "lon": 174.8},
    {"id": 24, "region": "Asia-Pacific", "place": "TOKYO",
     "headline": "Japan to train live-fire in India, a first",
     "summary": "Japanese forces will use Indian facilities.",
     "source": "Reuters", "lat": 35.7, "lon": 139.7},
    {"id": 25, "region": "Asia-Pacific", "place": "SEOUL",
     "headline": "K-pop's A20 debuts with 6 Chinese members",
     "summary": "The new group debuts in Seoul.",
     "source": "Korea Times", "lat": 37.6, "lon": 127.0},
    {"id": 26, "region": "Asia-Pacific", "place": "PALAWAN",
     "headline": "Philippines M5.9 quake, deep, off Palawan",
     "summary": "The tremor struck 888 km deep; no damage reported.",
     "source": "EMSC", "lat": 9.8, "lon": 118.8},
    {"id": 27, "region": "Africa", "place": "NORTH KORDOFAN",
     "headline": "Landmine kills 22 on road to El-Obeid",
     "summary": "Passengers, women and children among dead.",
     "source": "Darfur24", "lat": 13.2, "lon": 30.2},
    {"id": 28, "region": "Middle East", "place": "GAZA",
     "headline": "Four nations press Israel on Gaza aid",
     "summary": "Australia, Canada, Italy, UK cite flood misery.",
     "source": "Reuters", "lat": 31.5, "lon": 34.47},
    {"id": 29, "region": "Middle East", "place": "BEIRUT",
     "headline": "Aoun demands Israel withdraw, decries Iran's 'interference'",
     "summary": "Lebanon's president warns of a 'silent economic war'.",
     "source": "Al Jazeera", "lat": 33.9, "lon": 35.5},
    {"id": 30, "region": "Asia-Pacific", "place": "KINMEN",
     "headline": "Taiwan Army holds live-fire drill on Kinmen",
     "summary": "Troops fire from the frontline islets.",
     "source": "Focus Taiwan", "lat": 24.4, "lon": 118.3},
    {"id": 31, "region": "Asia-Pacific", "place": "NEW DELHI",
     "headline": "Air India extends Jeddah suspension to 24 Nov",
     "summary": "Air India and AI Express keep Jeddah flights halted.",
     "source": "ANI", "lat": 28.6, "lon": 77.2},
    {"id": 32, "region": "Europe", "place": "CHIȘINĂU",
     "headline": "Moldova: reports of Russian airspace breach",
     "summary": "Chisinau says a Russian drone crossed in.",
     "source": "Kyiv Independent", "lat": 47.0, "lon": 28.9},
    {"id": 33, "region": "Europe", "place": "BERLIN",
     "headline": "IG Metall widens car and shipyard strikes",
     "summary": "Germany's biggest union steps up pay action.",
     "source": "Reuters", "lat": 52.5, "lon": 13.4},
    {"id": 34, "region": "Asia-Pacific", "place": "YANGON",
     "headline": "France seeks UN action on Myanmar's generals' election",
     "summary": "Paris asks the UN to act over the generals' vote.",
     "source": "AFP", "lat": 16.8, "lon": 96.2},
    {"id": 35, "region": "Africa", "place": "DAR ES SALAAM",
     "headline": "Tanzania launches body for private equity",
     "summary": "President Samia Suluhu Hassan also outlines police reforms.",
     "source": "Daily Nation", "lat": -6.8, "lon": 39.3},
    {"id": 36, "region": "Europe", "place": "TURIN",
     "headline": "Zverev meets Alcaraz in ATP Finals final",
     "summary": "World No. 1 faces the Spaniard for the year-end title.",
     "source": "ATP", "lat": 45.1, "lon": 7.7},
]

for _s in STORIES:
    _s["date"] = DATE

# Stat strip: (big number, caption). All verified against the day's wires.
STATS = [
    ("03:00", "GMT: COP31 objections due"),
    ("~200", "nations at the COP31 talks"),
    ("400+", "drones fired at Ukraine"),
    ("6.8", "magnitude of the Peru quake"),
    ("16", "crew off burning Sparta II"),
    ("37–12", "England beat New Zealand"),
]

# The day by hours (UTC), for the timeline strip.
TIMELINE = [
    ("01:00", "HK polls open"),
    ("03:00", "COP31 objections due"),
    ("04:00", "Las Vegas GP"),
    ("06:00", "COP31 plenary"),
    ("10:00", "HK polls close"),
    ("Evening", "ATP final, Turin"),
]

# Region order and colours for the chips row.
REGIONS = [
    ("Europe", 8, "#1f4e79"),
    ("Middle East", 5, "#8b1a1a"),
    ("Asia-Pacific", 9, "#b26a00"),
    ("Americas", 7, "#1e6b3a"),
    ("Africa", 2, "#6b4fa1"),
    ("Oceania", 2, "#0e7a7a"),
    ("Global", 3, "#555555"),
]

DATE_CHECK = (
    "DATE CHECK — Wires read to 06:00 GMT, Sunday 22 November 2026. "
    "Left out as earlier news: the Trump–Xi–Putin Shenzhen summit (19 Nov), "
    "the Kerch Bridge strikes (earlier in the week), BepiColombo's Mercury "
    "capture (21 Nov), Voyager 1 at one light-day (18 Nov) and Wall Street's "
    "slide into correction (20 Nov). Not confirmed when drawn: a final COP31 "
    "text, the Gulf casualty toll, the FBI breach."
)

FOOTER = (
    "Every story here happened, or was first reported, on Sunday 22 November 2026 "
    "in at least one time zone. Officials' counts and claims are attributed. "
    "Sources named beside each story · Original drawings."
)
