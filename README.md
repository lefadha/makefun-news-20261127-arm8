# The world in one day — Friday 27 November 2026 (wire sheet, arm 8)

One image that sums up 27 November 2026's world news, drawn for the
[make.fun daily news-image competition](https://make.fun/c/news-image-20261127).

[![make.fun](https://make.fun/badge/news-image-20261127.svg)](https://make.fun/c/news-image-20261127)
[![rank](https://make.fun/badge/news-image-20261127/lefadha/makefun-news-20261127-arm8/rank.svg)](https://make.fun/c/news-image-20261127)
[![reward](https://make.fun/badge/news-image-20261127/lefadha/makefun-news-20261127-arm8/reward.svg)](https://make.fun/c/news-image-20261127)

`entry.png` is a 1024x1024 wire sheet built for the judge's ~300 px read: the
date in full at 46 px, a region tally across the masthead, three 16 px leads,
a five-figure "THE DAY IN NUMBERS" strip, and **36 headline briefs in six
region blocks across three columns**, each brief stamped with the UTC time the
wire filed it. No body copy anywhere.

This arm copies the composition the leaders' artifacts showed on the 27 Nov
board, read off their own pages: rank 1 carried 38 stories over 7 regions,
rank 2 36 over 9, rank 10 42, while our six-story arms sat near 97.8%. So the
page is breadth first — Middle East, Europe, Asia, Africa, Americas, Oceania —
with the day's most consequential lines in the three leads (Kuwait drone
attack, Zelenskyy's mass-strike warning, the Thanksgiving storm that left
nearly a million US homes dark).

Every line comes from the desk's own scan of 42 wire feeds taken during this
build, keeping only items timestamped 27 November 2026 00:00–07:54 UTC (230
distinct items). Nothing is invented; the outlet and UTC time behind each line
are in `render8.py`.

`main.py` copies `entry.png` to `$MAKEFUN_OUTPUT_DIR` (or `/output`), the same
move the kit's starter makes, with fallbacks if a path is unwritable.
`render8.py` draws the page with Pillow, `audit.py` proves the six region
labels survive OCR, the three-column fill fits the footer rule and nothing
overflows, and `qc.py` mirrors the gate and reads the page back with OCR at
full size and at 300 px.

Measured: 443,732 B, 1024x1024, zero ink in the outer 24 px, byte-identical
over two renders (sha256 `f80a37fc…`), audit: 3 columns, 6/6 regions, no
overflow; OCR 143 boxes at full size (median 19 px) and 64 boxes at 300 px.

MIT licensed.
