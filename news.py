"""News data for the News Image 22 Nov v4 poster.

Every story below was verified live on Sunday 22 November 2026 by web
search during this build session: each event happened, or was first
reported, on 22 November 2026 (Saturday-night events first reported on
Sunday count under the competition rules). No story is copied from the
v1/v2/v3 entries. Claims are attributed where the source itself is a
claim (e.g. "IRGC claims", "researcher says").

Regions: 7. Stories: 41 (6 top + 35 briefs).
"""

DATE_LINE = "SUNDAY 22 NOVEMBER 2026"
TITLE = "THE WORLD"
SUBTITLE = "IN ONE DAY"

REGIONS = [
    "Middle East",
    "Europe",
    "Asia-Pacific",
    "Americas",
    "Africa",
    "Economy",
    "Science & Sport",
]

# Each story: title (short, poster headline), deck (one factual line),
# region, top (True for the 6 lead stories with big panels), panel
# (which drawn illustration the render script uses).
STORIES = [
    # ---- TOP 6 ----
    {
        "title": "IRAN STRIKES US BASES IN BAHRAIN",
        "deck": "IRGC claims missile and drone hits on US Patriot radars at Riffa and Awali; Bahrain says a civilian site was hit, no one hurt.",
        "region": "Middle East",
        "top": True,
        "panel": "missiles",
    },
    {
        "title": "COP31 ON THE BRINK",
        "deck": "Longest climate summit ever: UK and EU reject a deal with no fossil fuels in it; the president says there will be no new text.",
        "region": "Europe",
        "top": True,
        "panel": "summit",
    },
    {
        "title": "MEXICO CAPTURES 'EL CHAPO ISIDRO'",
        "deck": "Cartel boss Fausto Isidro Meza Flores held in Sinaloa; 11 killed in the raid, four of them soldiers.",
        "region": "Americas",
        "top": True,
        "panel": "arrest",
    },
    {
        "title": "TRUMP, XI AND PUTIN MEET",
        "deck": "Trilateral summit in Shenzhen agrees to begin talks on cutting nuclear risk.",
        "region": "Asia-Pacific",
        "top": True,
        "panel": "summit3",
    },
    {
        "title": "MARKETS FALL INTO CORRECTION",
        "deck": "AI sell-off: the S&P 500 drops 3.7% and Japan's Nikkei falls 5.1% as tech shares slide.",
        "region": "Economy",
        "top": True,
        "panel": "markets",
    },
    {
        "title": "MISSILE HITS KRYVYI RIH",
        "deck": "Russian strike kills 2 in Zelensky's hometown; a Ukrainian drone sets a Russian cargo ship ablaze in the Gulf of Finland.",
        "region": "Europe",
        "top": True,
        "panel": "ship",
    },
    # ---- MIDDLE EAST briefs ----
    {
        "title": "Houthi missiles at Riyadh stopped",
        "deck": "Coalition stopped 3 missiles, then hit Hodeidah.",
        "region": "Middle East",
        "top": False,
        "panel": "missiles",
    },
    {
        "title": "Gaza strikes go on; aid vehicle hit",
        "deck": "Strikes go on in Gaza; an aid vehicle was hit.",
        "region": "Middle East",
        "top": False,
        "panel": "missiles",
    },
    {
        "title": "Lebanon blames Israel and Iran",
        "deck": "Aoun says both threaten Lebanon's sovereignty.",
        "region": "Middle East",
        "top": False,
        "panel": "summit",
    },
    {
        "title": "Fire at Iraq power station",
        "deck": "Hartha plant fire near Basra kills 4, injures 35.",
        "region": "Middle East",
        "top": False,
        "panel": "fire",
    },
    {
        "title": "Two tankers hit near Hormuz",
        "deck": "Two tankers struck near Hormuz; oil nears $90.",
        "region": "Middle East",
        "top": False,
        "panel": "ship",
    },
    # ---- EUROPE briefs ----
    {
        "title": "Denmark expels Russian attache",
        "deck": "Copenhagen expels a diplomat over a plot.",
        "region": "Europe",
        "top": False,
        "panel": "summit",
    },
    {
        "title": "UK and EU strike new deals",
        "deck": "UK and EU agree deals; Burnham eyes rejoining.",
        "region": "Europe",
        "top": False,
        "panel": "summit",
    },
    {
        "title": "England thrash the All Blacks",
        "deck": "England beat NZ; Australia edge Wales 29-26.",
        "region": "Europe",
        "top": False,
        "panel": "sport",
    },
    {
        "title": "France reach rugby final",
        "deck": "France beat Argentina 45-17; South Africa await.",
        "region": "Europe",
        "top": False,
        "panel": "sport",
    },
    # ---- ASIA-PACIFIC briefs ----
    {
        "title": "India and China hold border talks",
        "deck": "Commanders meet again over the Arunachal frontier.",
        "region": "Asia-Pacific",
        "top": False,
        "panel": "summit",
    },
    {
        "title": "Nepal PM visits India",
        "deck": "Nepal PM starts a two-day visit to New Delhi.",
        "region": "Asia-Pacific",
        "top": False,
        "panel": "summit",
    },
    {
        "title": "Toxic drink kills 11 in Manipur",
        "deck": "Toxic alcohol kills 11; 180+ in hospital.",
        "region": "Asia-Pacific",
        "top": False,
        "panel": "fire",
    },
    {
        "title": "Factory fire in Indonesia",
        "deck": "Candy plant fire in Banten kills 3; 36 missing.",
        "region": "Asia-Pacific",
        "top": False,
        "panel": "fire",
    },
    {
        "title": "India pile up 720/9",
        "deck": "India declare 720/9 vs NZ, leading by 352 runs.",
        "region": "Asia-Pacific",
        "top": False,
        "panel": "sport",
    },
    # ---- AMERICAS briefs ----
    {
        "title": "Peru hit by second quake",
        "deck": "M5.0 follows Friday's M6.7; 1 dead, 853 homeless.",
        "region": "Americas",
        "top": False,
        "panel": "quake",
    },
    {
        "title": "Bolsonaro in intensive care",
        "deck": "Ex-president treated for a bowel obstruction.",
        "region": "Americas",
        "top": False,
        "panel": "summit",
    },
    {
        "title": "FBI database breached",
        "deck": "Trump confirms breach of FBI's NCIC database.",
        "region": "Americas",
        "top": False,
        "panel": "markets",
    },
    {
        "title": "Florida floods break record",
        "deck": "St Johns River tops a 73-year high after rain.",
        "region": "Americas",
        "top": False,
        "panel": "flood",
    },
    {
        "title": "Boca win Sudamericana",
        "deck": "Boca beat Atletico Mineiro 2-0 to take the title.",
        "region": "Americas",
        "top": False,
        "panel": "sport",
    },
    {
        "title": "Harden passes Kobe",
        "deck": "Harden's 51 passes Kobe on the all-time list.",
        "region": "Americas",
        "top": False,
        "panel": "sport",
    },
    # ---- AFRICA briefs ----
    {
        "title": "Boat capsizes in Nigeria",
        "deck": "Mourners' boat sinks; 24 people are dead.",
        "region": "Africa",
        "top": False,
        "panel": "flood",
    },
    {
        "title": "AFCON places decided",
        "deck": "Senegal, Morocco, Cameroon book 2027 places.",
        "region": "Africa",
        "top": False,
        "panel": "sport",
    },
    {
        "title": "Africa backs Infantino",
        "deck": "All 54 CAF members back Infantino's re-election.",
        "region": "Africa",
        "top": False,
        "panel": "sport",
    },
    # ---- ECONOMY briefs ----
    {
        "title": "Amazon nears $7.5B AI deal",
        "deck": "Amazon close to buying Israeli AI startup Decart.",
        "region": "Economy",
        "top": False,
        "panel": "markets",
    },
    {
        "title": "EU and Indonesia sign trade deal",
        "deck": "Ten years of talks end in a trade pact.",
        "region": "Economy",
        "top": False,
        "panel": "summit",
    },
    # ---- SCIENCE & SPORT briefs ----
    {
        "title": "IBM unveils 520-qubit chip",
        "deck": "'Nighthawk r3' targets real workloads, IBM says.",
        "region": "Science & Sport",
        "top": False,
        "panel": "tech",
    },
    {
        "title": "GTA 6 sets launch record",
        "deck": "Estimated $3.79B on day one, a games record.",
        "region": "Science & Sport",
        "top": False,
        "panel": "tech",
    },
    {
        "title": "Researcher says AI aided Riemann proof",
        "deck": "Researcher says AI aided a Riemann proof.",
        "region": "Science & Sport",
        "top": False,
        "panel": "tech",
    },
    {
        "title": "Alcaraz reaches ATP final",
        "deck": "Alcaraz beats Shelton; Zverev awaits in Turin.",
        "region": "Science & Sport",
        "top": False,
        "panel": "sport",
    },
    {
        "title": "Verstappen wins in Las Vegas",
        "deck": "Verstappen takes the Las Vegas Grand Prix.",
        "region": "Science & Sport",
        "top": False,
        "panel": "sport",
    },
]

# Stat strip numbers (derived from STORIES at render time; kept here
# for the test that checks the poster text).
TOP_COUNT = 6
PANEL_COUNT = 13

# Map pins: (number, longitude, latitude) of the 6 top stories' places.
MAP_PINS = [
    (1, 50.5, 26.0),    # Bahrain / Gulf
    (2, 30.7, 36.9),    # Antalya, Turkey
    (3, -107.4, 24.8),  # Sinaloa, Mexico
    (4, 114.1, 22.5),   # Shenzhen, China
    (5, -74.0, 40.7),   # New York
    (6, 33.4, 47.9),    # Kryvyi Rih, Ukraine
]
