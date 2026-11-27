"""Gate mirror + legibility read: the same three limits the sealed scorer checks,
then OCR at the judge's own 'about 300 pixels across' size."""
import os

import numpy as np
from PIL import Image
from rapidocr_onnxruntime import RapidOCR

P = 'entry.png'
ocr = RapidOCR()
im = Image.open(P)
print('format', im.format, 'size', im.size, 'bytes', os.path.getsize(P),
      '<=1MiB', os.path.getsize(P) <= 1048576, '<=1024', max(im.size) <= 1024)
im = im.convert('RGB')
a = np.asarray(im.convert('L'))
rows = np.where((a[:24, :] < 235).any(axis=1))[0]
cols_l = np.where((a[:, :24] < 235).any(axis=0))[0]
cols_r = np.where((a[:, -24:] < 235).any(axis=0))[0]
bot = np.where((a[-24:, :] < 235).any(axis=1))[0]
print('border ink: top', len(rows), 'left', len(cols_l), 'right', len(cols_r), 'bottom', len(bot))
for tag, g in (('full', im), ('300px', im.resize((300, 300), Image.LANCZOS))):
    res, _ = ocr(np.asarray(g))
    hs = [max(p[1] for p in b) - min(p[1] for p in b) for b, t, c in res]
    print(tag, 'boxes', len(res), 'h_med', round(float(np.median(hs)), 1),
          'good', sum(1 for b, t, c in res if c > 0.7))
    if tag == '300px':
        print('   ', ' | '.join(t for b, t, c in res))
