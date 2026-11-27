"""Layout audit for arm 8.

Three proofs on the rendered page: the column solver (shared with the renderer)
still fits six regions into three columns with nothing crossing the footer rule,
the OCR read at full size still finds every region label and the date, and at
least 30 of the 36 headlines come back as readable text.
"""
import re

import numpy as np
from PIL import Image, ImageDraw
from rapidocr_onnxruntime import RapidOCR

import render8

im = Image.open("entry.png").convert("RGB")
res, _ = RapidOCR()(np.asarray(im))
texts = [t for _, t, _ in res]


def norm(s):
    return re.sub(r"[^a-z0-9 ]", "", s.lower())


blob = norm(" ".join(texts))
labels = [name for name, _ in render8.REGIONS]
for lab in labels + ["THE DAY IN NUMBERS"]:
    print("%-16s %s" % (lab, "found" if norm(lab) in blob else "** MISSING **"))
print("date 27 november 2026   %s" % ("found" if "27 november 2026" in blob else "** MISSING **"))

d = ImageDraw.Draw(Image.new("RGB", (1024, 1024)))
cols = render8.layout(d)
print("columns", len(cols), "heights", [h for _, h in cols], "limit", render8.BOTTOM - render8.TOP)
placed = [b[0] for col, _ in cols for b in col]
print("regions placed", len(placed), "of", len(labels), "lost", [r for r in labels if r not in placed])
print("overflow", "yes" if any(h > render8.BOTTOM - render8.TOP for _, h in cols) else "no")

words = set(blob.split())
hit = 0
miss = []
for _, items in render8.REGIONS:
    for _, head in items:
        toks = [w for w in norm(head).split() if len(w) > 2]
        if sum(1 for w in toks if w in words) >= 0.6 * len(toks):
            hit += 1
        else:
            miss.append(head[:44])
print("headlines readable %d of %d" % (hit, sum(len(i) for _, i in render8.REGIONS)))
for m in miss[:6]:
    print("  miss:", m)
print("boxes", len(texts))
