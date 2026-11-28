# The world in one day — Friday 27 November 2026 (wire sheet, arm 8)

One image that sums up 27 November 2026's world news, drawn for the
[make.fun daily news-image competition](https://make.fun/c/news-image-20261127).

[![make.fun](https://make.fun/badge/news-image-20261127.svg)](https://make.fun/c/news-image-20261127)
[![rank](https://make.fun/badge/news-image-20261127/lefadha/makefun-news-20261127-arm8/rank.svg)](https://make.fun/c/news-image-20261127)
[![reward](https://make.fun/badge/news-image-20261127/lefadha/makefun-news-20261127-arm8/reward.svg)](https://make.fun/c/news-image-20261127)

`entry.png` is a 1024x1024 wire sheet built for the judge's ~300 px read: the
date in full at 46 px, a region tally across the masthead, three 16 px leads,
a five-figure "THE DAY IN NUMBERS" strip, and **42 headline briefs in six
region blocks across three columns**, each brief stamped with the UTC time the
wire filed it. No body copy anywhere.

This arm copies the composition the leaders' artifacts showed on the 27 Nov
board: rank 1 carried 38 stories over 7 regions, rank 2 36 over 9, rank 10 42,
while our six-story arms sat near 97.8%. So the page is breadth first — Middle
East 7, Europe 9, Asia 9, Africa 5, Americas 8, Oceania 4 — with the day's
most consequential lines in the three leads (the Hamas chief's son surviving a
strike as the US disables a ship leaving Iran, Spain voting as Ibiza races to
stop an oil spill, and the Thanksgiving storm that left hundreds of thousands
without power and postponed the Macy's parade).

Every line comes from the desk's own scan of 42 wire feeds taken during this
build, keeping only items timestamped 27 November 2026 00:00-23:58 UTC: 198
distinct rows still carried by the feeds at 09:0xZ. All 42 briefs match a row
at their own UTC stamp (a verifier checks at least 55% of each headline's
content words against that row); nothing is invented and no row the scan no
longer carries is kept. The figure strip is read off the same rows: Gaza's
1.3M threatened by winter weather, the Kenyan cult leader's 123 deaths,
Nigeria's 17 villagers in Plateau state, Niger's 13 soldiers, and the 7,000
tonnes of diesel on the tanker capsized off Ibiza.

`main.py` copies `entry.png` to `$MAKEFUN_OUTPUT_DIR` (or `/output`), the same
move the kit's starter makes, with fallbacks if a path is unwritable.
`render8.py` draws the page with Pillow, `audit.py` proves the six region
labels survive OCR, the three-column fill fits the footer rule and nothing
overflows, and `qc.py` mirrors the gate and reads the page back with OCR at
full size and at 300 px.

Measured in this run: 530,457 B, 1024x1024, zero ink in the outer 24 px on all
four edges, byte-identical over two renders (sha256 `319b7a57…`), audit: 3
columns (548/498/420 of 620 px), 6/6 regions, no overflow, 38 of 42 headlines
legible; OCR 119 boxes at full size (median 20 px, all confident) and 75 boxes
at 300 px (22 confident).

MIT licensed.
