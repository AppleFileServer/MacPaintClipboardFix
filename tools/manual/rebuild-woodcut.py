#!/usr/bin/env python3
"""Rebuilds MacPaint's "Woodcut" (Susan Kare's picture after Goyō's
"Woman Combing Her Hair", on the cover of Apple's 1984 MacPaint manual)
as a MacPaint document, for the own-use cover (P24; Jack, 25 Oct 2026).

No copy of the original document was found, so the picture is rebuilt
from the only source at hand: the cover scan in Jack's PDF of the manual
(1090 x 1341 when rendered, about 1.5 scan pixels per Mac pixel). Each
of the window's 416 x 240 Mac pixels is read at its centre (the scan
enlarged 4 times, bicubic) and made black below a threshold. The result
is close, not MacPaint's own pixels: figures.md says so.

The window's frame was measured on the scan against MacPaint 1.6's own
screen (frame at Mac x 79 and 496, title bar's lower line at y 47):
    scan x = 408.9 + (mac x - 79) * 1.508
    scan y = 251.7 + (mac y - 47) * 1.498
The top row would catch the title bar's line (the scan is slightly
tilted), so it repeats the row below it.

The picture is placed where a new MacPaint window starts on the page
(80, 120), so opening the document shows it as the cover did. The
512-byte header (the patterns) is Example 1's.

Output, in the private assets folder (Apple's artwork: never in the
repository): Woodcut.pntg, and woodcut-416x240.png for checking.

Usage (the manual-tools venv, with Pillow; sips renders the PDF):
    rebuild-woodcut.py [MANUAL_PDF]"""
import os, subprocess, sys, tempfile
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..", "..")
PDF = sys.argv[1] if len(sys.argv) > 1 else os.path.expanduser("~/MacPlus/Manuals/MacPaint Manual 1984.pdf")
PRIVATE = os.environ.get("MANUAL_ASSETS",
                         os.path.expanduser("~/MacPlusProjects/manual-assets-private"))
HEADER = os.path.join(ROOT, "docs", "manual", "shots", "2026-10-25-claude", "Example 1.pntg")

THRESHOLD = 95                  # paper is about 190, ink about 10
X0, XK, Y0, YK = 408.9, 1.508, 251.7, 1.498
PAGE_AT = (80, 120)             # where a new window starts on the page


def packbits(b):
    out, i = bytearray(), 0
    while i < len(b):
        j = i
        while j + 1 < len(b) and b[j + 1] == b[i] and j - i < 127:
            j += 1
        if j > i:                                   # a run
            out += bytes([257 - (j - i + 1), b[i]])
            i = j + 1
        else:                                       # literal bytes
            j = i
            while j < len(b) and j - i < 128 and not (j + 1 < len(b) and b[j + 1] == b[j]):
                j += 1
            j = max(j, i + 1)
            out += bytes([j - i - 1]) + b[i:j]
            i = j
    return bytes(out)


def main():
    with tempfile.TemporaryDirectory() as tmp:
        png = os.path.join(tmp, "cover.png")
        subprocess.run(["sips", "-s", "format", "png", "-Z", "1341", PDF, "--out", png],
                       check=True, stdout=subprocess.DEVNULL)
        scan = Image.open(png).convert("L")
    if scan.size != (1090, 1341):
        sys.exit("unexpected scan size %s: the measurements won't fit" % (scan.size,))
    big = scan.resize((scan.width * 4, scan.height * 4), Image.BICUBIC)
    px = big.load()
    pic = Image.new("1", (416, 240), 1)
    out = pic.load()
    for my in range(48, 288):
        for mx in range(80, 496):
            sx, sy = X0 + (mx - 79) * XK, Y0 + (my - 47) * YK
            out[mx - 80, my - 48] = 0 if px[int(sx * 4), int(sy * 4)] < THRESHOLD else 1
    for x in range(416):
        out[x, 0] = out[x, 1]

    page = [bytearray(72) for _ in range(720)]
    for y in range(240):
        for x in range(416):
            if out[x, y] == 0:
                X, Y = PAGE_AT[0] + x, PAGE_AT[1] + y
                page[Y][X >> 3] |= 0x80 >> (X & 7)
    header = open(HEADER, "rb").read()[:512]
    os.makedirs(PRIVATE, exist_ok=True)
    open(os.path.join(PRIVATE, "Woodcut.pntg"), "wb").write(
        header + b"".join(packbits(bytes(r)) for r in page))
    pic.save(os.path.join(PRIVATE, "woodcut-416x240.png"))
    print("wrote Woodcut.pntg and woodcut-416x240.png to", PRIVATE)


main()
