"""27 November 2026 as a wire sheet: the whole UTC day, six regions, three columns.

Re-authored in this run (28 Nov 09:0xZ) from the run's own scan of 42 feeds
(198 distinct items still carried for 27 Nov, 00:00-23:58 UTC). The page keeps
the composition the 27 Nov board rewarded: the full date as the largest
element, a region tally across the masthead, three 16 px leads, a five-figure
"THE DAY IN NUMBERS" strip, and 42 headlines in six region blocks over three
columns, every headline stamped with the UTC minute the wire filed it.

Every line below is a row of this run's scan_out.txt: nothing is invented and
no row that the scan no longer carries is kept. Feed windows roll forward, so
this revision is deliberately drawn from the 198 rows alive at 09:0xZ rather
than the 339-row morning copy.
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

LEADS = [
    ("MIDDLE EAST",
     "Son of Hamas chief survives an Israeli strike as the US disables a ship leaving Iran"),
    ("EUROPE",
     "Spain votes on Sunday as Sanchez defies the polls and Ibiza races to stop an oil spill"),
    ("AMERICAS",
     "Thanksgiving storms cut power to hundreds of thousands and postpone the Macy's parade"),
]

NUMBERS = [
    ("1.3M", "Palestinians threatened by Gaza's winter weather"),
    ("123", "deaths in the Kenyan cult leader's latest conviction"),
    ("17", "villagers killed in Nigeria's Plateau state"),
    ("13", "soldiers killed in southwest Niger"),
    ("7,000", "tonnes of diesel on the tanker capsized off Ibiza"),
]

REGIONS = [
    ("MIDDLE EAST", [
        ("06:46", "Israel's Eisenkot agrees to a coalition deal with the left-wing Democrats"),
        ("09:00", "The corruption case against Benjamin Netanyahu suffers a serious blow"),
        ("14:26", "Son of Hamas chief survives an Israeli air strike, an official says"),
        ("15:39", "Eisenkot accuses Netanyahu's party of stalling Israeli coalition talks"),
        ("18:01", "US disables a ship trying to leave Iran as Tehran vows to confront the blockade"),
        ("21:30", "Report: Israel used Palestinians as human shields in Gaza, commanders encouraged it"),
        ("23:47", "Drone that killed two Italians in Kuwait was Iranian-made, Italy's foreign minister says"),
    ]),
    ("EUROPE", [
        ("03:03", "Amazon staff to strike and rally on the busiest shopping weekend of the year"),
        ("06:09", "Spain's young people on housing ahead of Sunday's election"),
        ("11:49", "Gerard Depardieu ordered to stand trial for rape and sexual assault"),
        ("13:43", "France's far-right Le Pen backs her protege over anti-Semitism allegations"),
        ("16:17", "Austrian court turns ex-tycoon Benko's suspended sentence into six months' prison"),
        ("17:35", "Spain races to stop an oil spill after a ship capsizes off Ibiza"),
        ("17:41", "Zelenskyy criticises Trump for cozying up to Putin as EU delays Ukraine funding"),
        ("21:09", "Ukraine submits a Black Sea ceasefire offer and awaits Russia's response"),
        ("22:00", "S&P revises France's outlook from stable to negative"),
    ]),
    ("ASIA", [
        ("01:21", "North Korean troops cross the inter-Korean border about 40 times in two months"),
        ("06:31", "Seoul shares rally over 4% on hopes of policy support"),
        ("07:01", "Sony launches its new Walkman series, with a price tag of up to 655,000 yen"),
        ("07:26", "The number of students not attending school in Japan reaches a record"),
        ("08:13", "Millions of wives in South Asia are unprotected from marital rape, a study finds"),
        ("08:25", "Suzuki to domestically produce rare metal-free EV batteries"),
        ("10:08", "Kakao founder's acquittal is finalised as prosecutors decide not to appeal"),
        ("15:21", "North Korean launderers turn to little-known crypto services, researchers say"),
        ("23:39", "Japan to revise its AI law to introduce penalties for misuse"),
    ]),
    ("AFRICA", [
        ("11:02", "South Africa is no longer an El Dorado for foreigners, migrants say"),
        ("11:51", "Suspected militants kill 13 soldiers in southwest Niger, the ministry says"),
        ("12:16", "Armed men kill 17 villagers in Nigeria's Plateau state, police say"),
        ("14:32", "Kenyan starvation cult leader is guilty of manslaughter for 123 deaths"),
        ("17:46", "Johannesburg picks Mashaba as mayor in an ANC-backed deal"),
    ]),
    ("AMERICAS", [
        ("05:15", "A major Thanksgiving storm brings flooding and flight delays across the US"),
        ("09:00", "A Niagara family business says $500K a week in Trump tariffs forces it to the US"),
        ("09:57", "Thanksgiving storm on the US East Coast knocks out power and disrupts flights"),
        ("11:07", "Canada's top court upholds Quebec's law banning religious symbols"),
        ("11:42", "Hackers breach the US Air Force's flagship Cloud One computing platform"),
        ("15:21", "Mexico files a complaint with the US over a DEA tip line on drug traffickers"),
        ("19:22", "Hundreds of thousands are out of power in the US after the Thanksgiving storm"),
        ("21:22", "OpenAI countersues Apple for stealing trade secrets"),
    ]),
    ("OCEANIA", [
        ("21:19", "Polls close and counting begins in Australia's Victoria state elections"),
        ("22:21", "Ireland seal fifth place with a 38-14 win over Australia"),
        ("23:35", "The Top End is rocked by several strong earthquakes, prompting a risk review"),
        ("23:58", "A major WA dairy is accused of polluting a river with animal carcasses"),
    ]),
]

FOOT = ("Compiled from a scan of 42 wire feeds, 198 items timestamped "
        "00:00-23:58 UTC, 27 November 2026")

TOP, BOTTOM = 326, 946
GUTTER = 16
CW = (RIGHT - M - 2 * GUTTER) / 3
HEAD_SZ, HEAD_LH = 12.5, 14
BLOCK_GAP = 6


def font(size, bold=False, serif=False):
    return ImageFont.truetype(FSB if serif else (FB if bold else F), size)


def tw(d, s, size, bold=False, serif=False):
    return d.textlength(s, font=font(size, bold, serif))


def wrap(d, text, size, maxw, bold=False, serif=False):
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if not cur or tw(d, trial, size, bold, serif) <= maxw:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def put(d, x, y, s, size, fill, bold=False, serif=False):
    d.text((x, y), s, font=font(size, bold, serif), fill=fill)


def time_gutter(d):
    """Width of the widest UTC stamp plus breathing room."""
    return int(max(tw(d, t, 9.5, True) for _, items in REGIONS for t, _ in items)) + 5


def layout(d):
    """Height of each region block and the three-column split with the flattest top.

    Shared with audit.py so the audit measures exactly the numbers the renderer
    draws with. Blocks keep their order; the split minimises the tallest column.
    Raises instead of silently dropping a block or clipping a headline.
    """
    gutter = time_gutter(d)
    blocks = []
    for name, items in REGIONS:
        h = 18
        for _, head in items:
            lines = wrap(d, head, HEAD_SZ, CW - gutter)
            if len(lines) > 3:
                raise SystemExit("headline needs %d lines, page prints 3: %s"
                                 % (len(lines), head[:60]))
            h += len(lines) * HEAD_LH + 4
        blocks.append((name, items, h))

    limit = BOTTOM - TOP
    n = len(blocks)
    best = None
    for i in range(1, n - 1):
        for j in range(i + 1, n):
            groups = (blocks[:i], blocks[i:j], blocks[j:])
            hs = [sum(b[2] for b in g) for g in groups]
            cost = max(hs)
            if best is None or cost < best[0]:
                best = (cost, groups, hs)
    if best is None:
        raise SystemExit("not enough region blocks for three columns")
    cost, groups, hs = best
    if cost > limit:
        raise SystemExit("three columns cannot hold the day: tallest %d > %d"
                         % (cost, limit))
    return [(list(g), h) for g, h in zip(groups, hs)]


def build(out="/opt/data/makefun/news27/entry-arm8/entry.png", scale=2):
    img = Image.new("RGB", (W * scale, H * scale), PAPER)
    d = ImageDraw.Draw(img)
    S = scale

    total = sum(len(items) for _, items in REGIONS)
    put(d, M * S, 30 * S, TAG, 15 * S, SOFT, bold=True)
    tally = "  ·  ".join("%s %d" % (name, len(items)) for name, items in REGIONS)
    put(d, (RIGHT - tw(d, tally, 12, True)) * S, 32 * S, tally, 12 * S, SOFT, True)
    put(d, M * S, 46 * S, DATE, 46 * S, INK, bold=True, serif=True)
    put(d, M * S, 98 * S,
        "%d STORIES · %d REGIONS · A WIRE SHEET OF THE DAY" % (total, len(REGIONS)),
        14 * S, RED, bold=True)
    d.rectangle([M * S, 118 * S, RIGHT * S, 122 * S], fill=RED)

    for i, (region, head) in enumerate(LEADS):
        x = M + i * (CW + GUTTER)
        put(d, x * S, 132 * S, region, 11 * S, BLUE, bold=True)
        ty = 147
        for ln in wrap(d, head, 16 * S, CW * S, serif=True)[:4]:
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

    gutter = time_gutter(d)
    for ci, (col, _) in enumerate(layout(d)):
        x = M + ci * (CW + GUTTER)
        y = TOP
        for name, items, _ in col:
            put(d, x * S, y * S, name, 11 * S, RED, bold=True)
            d.rectangle([x * S, (y + 13) * S, (x + CW) * S, (y + 14) * S], fill=RULE)
            y += 18
            for stamp, head in items:
                put(d, x * S, y * S, stamp, 9.5 * S, FAINT, bold=True)
                for ln in wrap(d, head, HEAD_SZ * S, (CW - gutter) * S)[:3]:
                    put(d, (x + gutter) * S, y * S, ln, HEAD_SZ * S, INK)
                    y += HEAD_LH
                y += 4
            y += BLOCK_GAP

    d.rectangle([M * S, 960 * S, RIGHT * S, 961 * S], fill=RULE)
    put(d, M * S, 966 * S, FOOT, 10 * S, FAINT)

    parent = os.path.dirname(os.path.abspath(out))
    os.makedirs(parent, exist_ok=True)
    img.resize((W, H), Image.LANCZOS).save(out, optimize=True)
    print("wrote", out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    import sys

    build(sys.argv[1] if len(sys.argv) > 1 else
          "/opt/data/makefun/news27/entry-arm8/entry.png")
