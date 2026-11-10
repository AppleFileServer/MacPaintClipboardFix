#!/usr/bin/env python3
"""Makes the MacPaint User's Guide's own-use cover (copied from MacTrack's,
which came from MacMusic's; style guide §6): MacDraw's cover, at the
family's 7½ x 9 in (P24), with its title replaced by "MacPaint User’s
Guide" and its screen by MacPaint 1.6 showing the Woodcut, as on Apple's
1984 MacPaint manual (Jack, 25 Oct 2026).

The screen is woodcut-screen.png in the private assets folder: an exact
512 x 342 shot of MacPaint 1.6 with the rebuilt Woodcut document open
(rebuild-woodcut.py, then a Mini vMac session). Until it exists, the
Example 1 screen (figure e01-cover) stands in.

The cover is written as cover-macpaint.jpg in the private assets folder
(~/MacPlusProjects/manual-assets-private, or MANUAL_ASSETS), never in the
repository: it holds Apple's artwork. Without that folder there is no
cover (this book is own-use only, D3).

Usage (with Pillow): make-cover.py"""
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..", "..")
FIGURES = os.path.join(ROOT, "docs", "manual", "figures", "png")
PRIVATE = os.environ.get("MANUAL_ASSETS",
                         os.path.expanduser("~/MacPlusProjects/manual-assets-private"))
TOOLS = os.environ.get("MANUAL_TOOLS", os.path.expanduser("~/MacPlusProjects/manual-tools"))
FONT = os.path.join(TOOLS, "fonts", "built-macpaint", "MacPaintGaramond100-Regular.ttf")

# Where things are on the MacDraw cover scan (4489 x 5360), measured
# (as MacTrack's make-cover.py).
SCREEN = (1503, 704, 4406, 2652)        # the screen: the black bezel's inner edges
TITLE = (1420, 380, 2420, 632)          # "MacDraw", to be painted out
TITLE_LEFT, TITLE_BASE = 1436, 600      # where the new title is set
TITLE_CAP = 168                         # MacDraw's capital height, in pixels
HOLES = 205                             # the wire binding's holes, left of here
PALE_BLUE = (0xc1, 0xdc, 0xe6)          # the scan's screen, sampled


def cover():
    scan = os.path.join(PRIVATE, "macdraw-cover-4489.png")
    if not os.path.exists(scan):
        print("no private assets: no cover (own-use edition only)")
        return
    im = Image.open(scan).convert("RGB")
    draw = ImageDraw.Draw(im)

    # The binding holes down the left edge go, painted in the paper's own
    # colour, sampled just to their right (as MacTrack's).
    strip = im.crop((HOLES, 0, HOLES + 20, im.height)).resize((1, 1), Image.BOX)
    draw.rectangle((0, 0, HOLES, im.height), fill=strip.getpixel((0, 0)))

    # The title: paint out "MacDraw" and set ours at the same capital height.
    draw.rectangle(TITLE, fill=(255, 255, 255))
    size = 100
    font = ImageFont.truetype(FONT, size)
    cap = font.getbbox("M")[3] - font.getbbox("M")[1]
    font = ImageFont.truetype(FONT, round(size * TITLE_CAP / cap))
    draw.text((TITLE_LEFT, TITLE_BASE), "MacPaint User’s Guide", font=font,
              fill=(20, 20, 20), anchor="ls")

    # The screen: MacPaint 1.6 with the Woodcut, in the cover's pale blue.
    shot = os.path.join(PRIVATE, "woodcut-screen.png")
    if os.path.exists(shot):
        mac = Image.open(shot).convert("L")
        screen = Image.new("RGB", mac.size, PALE_BLUE)
        screen.paste((0, 0, 0), mask=mac.point(lambda v: 255 if v < 128 else 0))
    else:
        print("no woodcut-screen.png yet: Example 1 stands in")
        screen = Image.open(os.path.join(FIGURES, "e01-cover.png")).convert("RGB")
    x0, y0, x1, y1 = SCREEN
    im.paste(screen.resize((x1 - x0, y1 - y0), Image.NEAREST), (x0, y0))

    path = os.path.join(PRIVATE, "cover-macpaint.jpg")
    im.resize((2700, round(2700 * im.height / im.width)), Image.LANCZOS).save(path, quality=90)
    print("wrote", path)


cover()
