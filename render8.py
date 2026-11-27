"""27 November 2026 as one wire sheet: breadth, not six stories.

Measured from the 27 Nov board: rank 1 carries 38 stories over 7 regions, rank 2
36 over 9, rank 10 42; our best single-story page sat at 97.8% while those sat
at 98.9-99.1%. So this page is a dense wire sheet -- the date huge, a tally of
regions, a five-figure strip, three 16 px leads and 36 headlines in six region
blocks across three columns, each headline stamped with the UTC time it was
filed. Every line below is a row of this run's own scan_out.txt (263 items,
42 feeds, 00:00-09:00 UTC, 27 Nov 2026); nothing is invented.

Re-authored in this run. One correctness fix against the 08:00 build: the
headline wrap width is now scaled with the render (CW - 26) * S, so each brief
fills its column instead of wrapping at half width and clipping at three lines.
"""
import os

from PIL import Image, ImageDraw, ImageFont

W = H = 1024
M = 28
RIGHT = W - M
PAPER = (252, 251, 247)
INK = (17, 19, 18)
SOFT = (88, 92, 86)
FAINT = (140, 144, 136)
RED = (170, 34, 30)
BLUE = (22, 46, 94)
RULE = (178, 172, 158)

FB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
F = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FSB = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"

DATE = "FRIDAY 27 NOVEMBER 2026"
TAG = "THE WORLD IN ONE DAY"

# The three leads: one per continent-sized block of the day.
LEADS = [
    ("MIDDLE EAST", "Syria voices solidarity with Kuwait after drone attacks blamed on Iran, as several countries condemn the strike"),
    ("EUROPE", "Zelenskyy warns of a major Russian attack as Trump tells Putin to pull back"),
    ("AMERICAS", "Thanksgiving storms leave nearly a million without power across the US"),
]

# Five figures the day turned on, each read off its own scan row.
NUMBERS = [
    ("~1M", "US homes without power after the storm"),
    ("31", "dead in the Cairo fuel-tanker inferno"),
    ("13", "Niger soldiers killed in the Sanam attack"),
    ("20%", "of LNG Australia keeps for domestic use"),
    ("22", "injured when a ferry hit a Hong Kong dock"),
]

# 36 headlines, six region blocks, each with the UTC time the wire filed it.
REGIONS = [
    ("MIDDLE EAST", [
        ("01:07", "Syria expresses solidarity with Kuwait after drone attacks blamed on Iran"),
        ("02:25", "Trump says Iran's missiles can reach Europe, warns of 'nuclear holocaust' risk"),
        ("01:22", "Israeli airstrikes destroy five residential buildings in Gaza"),
        ("05:26", "Erdogan completes Turkey's ratification of the Mecca defence pact"),
        ("07:35", "Iran says its air defences forced a US F-16 to withdraw near Hengam Island"),
    ]),
    ("EUROPE", [
        ("02:14", "Zelenskyy warns of a major Russian attack; Trump urges Putin to 'pull back'"),
        ("04:46", "Estonia closes its land borders with Russia to keep out spies"),
        ("07:40", "NHS boss warns of a 'horrible spike' in flu as admissions surge"),
        ("01:13", "France's AFP news agency hit by cyberattack, takes platform offline"),
        ("06:00", "Reform UK pledges to scrap hospital parking fees in England"),
        ("08:08", "Spain's Vox leader Abascal nears power as election kingmaker"),
        ("09:00", "Italy's premier refuses to sign the EU budget deal, calling it 'light years away'"),
        ("08:22", "Russian sabotage attacks in Europe up 16%, the IISS says"),
    ]),
    ("ASIA", [
        ("00:47", "Sheikh Hasina's planned return puts Bangladesh on edge and India in a bind"),
        ("03:28", "New Zealand's ruling coalition falls one seat short of a majority"),
        ("04:51", "China's military tests new Taiwan landing tactics in coastal drills"),
        ("02:38", "Faster Tokyo inflation supports the case for a BOJ hike in December"),
        ("08:31", "China stocks surge most in two years as Beijing vows stronger market support"),
        ("05:21", "Seoul repatriates six North Koreans found on a drifting fishing boat"),
        ("04:06", "22 injured after a passenger ferry collides with a dock in Hong Kong"),
        ("02:22", "Families of slain Filipinos seek justice as Duterte's ICC trial opens"),
    ]),
    ("AFRICA", [
        ("04:06", "At least 13 Niger soldiers killed in a Sanam armed attack"),
        ("01:10", "Cairo fuel-tanker inferno: the driver is held after 31 deaths"),
        ("00:48", "Kenyan man wrongly convicted in UK says Met Police ruined his life"),
        ("01:27", "African Union and China sign a development-cooperation agreement"),
    ]),
    ("AMERICAS", [
        ("04:34", "Thanksgiving storms leave nearly a million without power across the US"),
        ("06:25", "Trump argues the US does not 'need' Middle East oil and 'protects' Israel"),
        ("00:34", "Trump claims fake GDP data before the midterms and demands a probe"),
        ("03:03", "Amazon staff to strike and rally on the busiest weekend of the year"),
        ("08:24", "Deadly floods leave parts of Ecuador under water"),
        ("05:32", "Dolly Parton's $500 pledge cut students' dropout rate from 35% to 6%"),
        ("06:12", "Strobe Talbott, former deputy secretary of state, has died"),
    ]),
    ("OCEANIA", [
        ("07:10", "A technical issue forces South Australia police to withdraw 8,000 fines"),
        ("02:41", "Australia clears a law requiring LNG exporters to keep 20% at home"),
        ("07:47", "Australia's Sandpapergate probe will also cover the 2017-18 Ashes"),
        ("06:22", "Australia sanctions two men over 2024 antisemitic firebombings"),
    ]),
]

FOOT = "Compiled from a scan of 42 wire feeds, 263 items timestamped 00:00-09:00 UTC, 27 November 2026"

TOP, BOTTOM = 326, 946
GUTTER = 16
CW = (RIGHT - M - 2 * GUTTER) / 3


def font(size, bold=False, serif=False):
    return ImageFont.truetype(FSB if serif else (FB if bold else F), size)


def tw(d, s, size, bold=False, serif=False):
    return d.textlength(s, font=font(size, bold, serif))


def wrap(d, text, size, maxw, bold=False, serif=False):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if tw(d, t, size, bold, serif) <= maxw or not cur:
            cur = t
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def put(d, x, y, s, size, fill, bold=False, serif=False):
    d.text((x, y), s, font=font(size, bold, serif), fill=fill)


def layout(d, head_sz=12.5, lh=14):
    """Height of every region block and the greedy three-column fill.

    Shared with audit.py so the geometry proof measures the very numbers the
    renderer draws with. Raises instead of silently dropping a region.
    """
    blocks = []
    for name, items in REGIONS:
        h = 18
        for _, head in items:
            h += len(wrap(d, head, head_sz, CW - 26)[:3]) * lh + 4
        blocks.append((name, items, h))
    cols, cur, curh = [], [], 0
    for blk in blocks:
        if cur and curh + blk[2] > (BOTTOM - TOP):
            cols.append((cur, curh))
            cur, curh = [], 0
        cur.append(blk)
        curh += blk[2]
    if cur:
        cols.append((cur, curh))
    if len(cols) > 3:
        raise SystemExit("layout needs %d columns, page holds 3" % len(cols))
    for _, h in cols:
        if h > BOTTOM - TOP:
            raise SystemExit("column overflows: %d > %d" % (h, BOTTOM - TOP))
    return cols


def build(out="/opt/data/makefun/news27/entry-arm8/entry.png", scale=2):
    img = Image.new("RGB", (W * scale, H * scale), PAPER)
    d = ImageDraw.Draw(img)
    S = scale

    total = sum(len(items) for _, items in REGIONS)
    put(d, M * S, 30 * S, TAG, 15 * S, SOFT, bold=True)
    tally = "  ·  ".join("%s %d" % (name, len(items)) for name, items in REGIONS)
    put(d, (RIGHT - tw(d, tally, 12, True)) * S, 32 * S, tally, 12 * S, SOFT, True)
    put(d, M * S, 46 * S, DATE, 46 * S, INK, bold=True, serif=True)
    put(d, M * S, 98 * S, "%d STORIES · %d REGIONS · A WIRE SHEET OF THE DAY" % (total, len(REGIONS)),
        14 * S, RED, bold=True)
    d.rectangle([M * S, 118 * S, RIGHT * S, 122 * S], fill=RED)

    colw = (RIGHT - M - 2 * 16) / 3
    for i, (region, head) in enumerate(LEADS):
        x = M + i * (colw + 16)
        put(d, x * S, 132 * S, region, 11 * S, BLUE, bold=True)
        ty = 147
        for ln in wrap(d, head, 16 * S, colw * S, serif=True)[:4]:
            put(d, x * S, ty * S, ln, 16 * S, INK, serif=True)
            ty += 19
    d.rectangle([M * S, 228 * S, RIGHT * S, 229 * S], fill=RULE)

    put(d, M * S, 238 * S, "THE DAY IN NUMBERS", 11 * S, RED, bold=True)
    fw = (RIGHT - M) / 5
    for i, (num, cap) in enumerate(NUMBERS):
        x = M + i * fw
        put(d, x * S, 254 * S, num, 30 * S, INK, bold=True, serif=True)
        for j, ln in enumerate(wrap(d, cap, 10 * S, (fw - 10) * S)[:3]):
            put(d, x * S, (287 + j * 12) * S, ln, 10 * S, SOFT)
    d.rectangle([M * S, 316 * S, RIGHT * S, 317 * S], fill=RULE)

    for ci, (col, _) in enumerate(layout(d)):
        x = M + ci * (CW + GUTTER)
        y = TOP
        for name, items, _ in col:
            put(d, x * S, y * S, name, 11 * S, RED, bold=True)
            d.rectangle([x * S, (y + 13) * S, (x + CW) * S, (y + 14) * S], fill=RULE)
            y += 18
            for t, head in items:
                put(d, x * S, y * S, t, 9.5 * S, FAINT, bold=True)
                for ln in wrap(d, head, 12.5 * S, (CW - 26) * S)[:3]:
                    put(d, (x + 26) * S, y * S, ln, 12.5 * S, INK)
                    y += 14
                y += 4
            y += 6

    d.rectangle([M * S, 960 * S, RIGHT * S, 961 * S], fill=RULE)
    put(d, M * S, 966 * S, FOOT, 10 * S, FAINT)

    os.makedirs(os.path.dirname(out), exist_ok=True)
    img.resize((W, H), Image.LANCZOS).save(out, optimize=True)
    print("wrote", out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    build()
