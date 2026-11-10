#!/usr/bin/env python3
"""Makes the MacTrack manual's figures (Phase 4/5; copied from MacMusic's,
W3) from the figure build's screens (TF7), which are kept outside the
repository: exact 1x PNGs of the Mac Plus's screen ("screen 0 0 1").

Each screenshot shows the Mac Plus's 512 x 342 one-bit screen at an exact
whole-number zoom, so the screen is recovered pixel for pixel (each
block's centre sampled), then cropped (figures.md: F, W, L, M, D) and
written as a PNG enlarged by whole pixels, so it stays sharp in print.

Usage (with Pillow; see docs/environment.md):
    make-figures.py <figures.txt> <out folder>

figures.txt has one figure per line (# starts a comment):
    <name> <screenshot file> <crop> [options]
  crop:     full | window | lcd | box | menu | x,y,w,h   (Mac screen pixels)
            window: the Day or History window, frame and shadow (always
                    in the same place: 'WIND' 128 and 129);
            box:    the largest dialog or alert box (a rectangle of black
                    lines below the menu bar);
            menu:   a pulled-down menu, with its title in the menu bar
                    and its shadow
  options:  zoom=N        enlargement (default 4)
            ink=RRGGBB    the colour black pixels print in (default 000000)
            paper=RRGGBB  the colour white pixels print in (default ffffff)
            erase=x,y,w,h paint an area white; repeatable
            desk=x,y,w,h  paint an area in the grey desk's checkerboard,
                          in step with the pixel above it; repeatable
            nopointer     paint out the arrow pointer wherever it shows
                          (it is found exactly, from its own bitmap)
            pointer=x,y   draw the arrow pointer with its tip at Mac pixel
                          (x, y), clicking there (as MW 63, 65)
            torn          end the picture in a torn, zigzag lower edge,
                          for a piece of the screen (MW 16, 65)
The screenshot settings (where the screen starts, the zoom) are on a line
    screen <x0> <y0> <zoom>   (default: 384 198 4, the owner's Mini vMac)."""

import os, sys
from PIL import Image

FULL = (0, 0, 512, 342)
WINDOW = (3, 21, 507, 317)  # the Day and History windows, frame and shadow


# The arrow pointer, 16 x 16 (the Toolbox's arrow cursor): its image and
# its mask, one row a number, the leftmost pixel the highest bit.
ARROW = (0x0000, 0x4000, 0x6000, 0x7000, 0x7800, 0x7C00, 0x7E00, 0x7F00,
         0x7F80, 0x7C00, 0x6C00, 0x4600, 0x0600, 0x0300, 0x0300, 0x0000)
ARROW_MASK = (0xC000, 0xE000, 0xF000, 0xF800, 0xFC00, 0xFE00, 0xFF00, 0xFF80,
              0xFFC0, 0xFFE0, 0xFE00, 0xEF00, 0xCF00, 0x8780, 0x0780, 0x0380)


def add_pointer(screen, x, y):
    """Draws the arrow pointer, its tip at (x, y): white under its mask,
    then black where its image is (as the Mac draws a cursor)."""
    px = screen.load()
    for dy in range(16):
        for dx in range(16):
            if not (0 <= x + dx - 1 < 512 and 0 <= y + dy - 1 < 342):
                continue
            bit = 0x8000 >> dx
            if ARROW_MASK[dy] & bit:
                px[x + dx - 1, y + dy - 1] = 0 if ARROW[dy] & bit else 255


def tear(part):
    """A torn lower edge: a zigzag line 4 pixels deep, everything below
    it white (MW 16, 65)."""
    px = part.load()
    w, h = part.size
    for x in range(w):
        k = x % 12
        edge = h - 2 - (k if k < 6 else 12 - k) * 4 // 6
        px[x, edge] = 0
        for y in range(edge + 1, h):
            px[x, y] = 255


def remove_pointer(screen):
    """Whitens the arrow pointer wherever it shows on the screen: every
    place where the pixels under its mask are exactly its image."""
    px = screen.load()
    cells = [(dx, dy, bool(ARROW[dy] & (0x8000 >> dx)))
             for dy in range(16) for dx in range(16) if ARROW_MASK[dy] & (0x8000 >> dx)]
    found = 0
    for y in range(342 - 15):
        for x in range(512 - 15):
            if all((px[x + dx, y + dy] == 0) == black for dx, dy, black in cells):
                for dx, dy, _ in cells:
                    px[x + dx, y + dy] = 255
                found += 1
    return found


def find_rects(screen, min_width=60, min_height=30):
    """Rectangles of black lines (dialog boxes, alerts, menus), largest
    first: a top and a bottom line with matching ends (give or take a
    shadow's two pixels) and black sides between them."""
    px = screen.load()
    lines = []
    for y in range(19, 342):
        x = 0
        while x < 512:
            if px[x, y] == 0:
                start = x
                while x < 512 and px[x, y] == 0:
                    x += 1
                if x - start >= min_width:
                    lines.append((y, start, x - 1))
            x += 1
    found = []
    for i, (ty, tx0, tx1) in enumerate(lines):
        for by, bx0, bx1 in lines[i + 1:]:
            if by - ty < min_height or abs(bx0 - tx0) > 2 or abs(bx1 - tx1) > 2:
                continue
            x0, x1 = min(tx0, bx0), max(tx1, bx1)
            left = sum(px[x0, y] == 0 or px[x0 + 1, y] == 0 for y in range(ty, by + 1))
            right = sum(px[x1, y] == 0 or px[x1 - 1, y] == 0 for y in range(ty, by + 1))
            if min(left, right) >= 0.9 * (by - ty + 1):
                found.append((x0, ty, x1 - x0 + 1, by - ty + 1))
    found.sort(key=lambda r: -r[2] * r[3])
    return found


def find_menu(screen):
    """(left, right, bottom) of a pulled-down menu. Its top edge is the
    menu bar's own bottom line, so it is found from its title, which is
    highlighted (white on black) in the menu bar: the menu's left frame
    drops from the title's left end to the bottom; the right frame is the
    first column to its right that is black almost all the way down (a
    highlighted item, a bar across, can't be)."""
    px = screen.load()
    title = None
    for x in range(0, 500):
        if all(px[x + i, 17] == 0 for i in range(12)) and px[x - 1, 17] != 0:
            title = x
            break
    if title is None:
        sys.exit("no highlighted menu title found")
    for left in range(title - 3, title + 4):
        y = 20
        while y < 341 and px[left, y] == 0:
            y += 1
        if y - 20 >= 20:
            break
    else:
        sys.exit("no menu frame found below the title")
    bottom = y - 1
    rows = range(22, bottom - 2)
    for right in range(left + 30, 512):              # the right frame: a full column
        if sum(px[right, r] == 0 for r in rows) >= 0.9 * len(rows):
            return left, right, bottom
    sys.exit("no menu right frame found")


def menu_bar_end(screen):
    """The x just past the menu bar's last title (before the icons at its
    right end)."""
    px = screen.load()
    end = 0
    for x in range(0, 440):
        if any(px[x, y] == 0 for y in range(2, 18)):
            end = x
    return end + 1


def clear_around_menu(part, screen, cx):
    """Whitens whatever shows beside and below a menu crop, below the
    menu bar, except the menu itself and its shadow (two pixels to the
    right and below, starting two pixels in); and in the menu bar, the
    end of the title before the highlighted one."""
    left, right, bottom = find_menu(screen)
    px = part.load()
    w, h = part.size
    for y in range(0, 19):
        for x in range(0, max(0, left - 1 - cx)):
            px[x, y] = 255
    for y in range(20, h):
        for x in range(w):
            sx = cx + x
            inside = left <= sx <= right and y <= bottom
            shadow = sx == right + 1 and y >= 22     # System 6: 1 pixel; the bottom
                                                     # one is already inside `bottom`
            if not (inside or shadow):
                px[x, y] = 255


def crop_box(screen, kind):
    if kind == "full":
        return FULL
    if kind == "window":
        return WINDOW
    rects = find_rects(screen)
    if kind == "box":
        # below the menu bar, and not the Day or History window (nearly
        # the screen's width): the dialog in front of it
        rects = [r for r in rects if r[1] > 22 and r[2] < 500]
        if not rects:
            sys.exit("no dialog box found")
        return rects[0]                              # exactly the box's frame
    if kind == "menu":
        x0, x1, bottom = find_menu(screen)
        x1 = max(x1 + 3, menu_bar_end(screen) + 4)      # the whole menu bar's titles
        left = max(0, x0 - 6)
        return (left, 0, min(x1 - left + 1, 512 - left), bottom + 3)
    return tuple(map(int, kind.split(",")))


def mac_screen(path, x0, y0, k):
    """The emulated screen, one value per Mac pixel: 0 black, 255 white."""
    shot = Image.open(path).convert("L")
    screen = Image.new("L", (512, 342), 255)
    px, out = shot.load(), screen.load()
    for j in range(342):
        for i in range(512):
            out[i, j] = 0 if px[x0 + i * k + k // 2, y0 + j * k + k // 2] < 128 else 255
    return screen


def main():
    spec, out = sys.argv[1], sys.argv[2]
    os.makedirs(out, exist_ok=True)
    x0, y0, k = 384, 198, 4
    cache = {}
    for line in open(spec, encoding="utf-8"):
        line = line.split("#", 1)[0].strip()
        if not line:
            continue
        words = line.split()
        if words[0] == "screen":
            x0, y0, k = map(int, words[1:4])
            continue
        name, source, crop = words[0], os.path.expanduser(words[1].replace("%20", " ")), words[2]
        opts = {"zoom": "4", "ink": "000000", "paper": "ffffff"}
        erase, desk = [], []
        for w in words[3:]:
            if w in ("nopointer", "torn"):
                opts[w] = True
                continue
            key, value = w.split("=", 1)
            if key == "erase":
                erase.append(tuple(map(int, value.split(","))))
            elif key == "desk":
                desk.append(tuple(map(int, value.split(","))))
            else:
                opts[key] = value
        if source not in cache:
            cache[source] = mac_screen(source, x0, y0, k)
        screen = cache[source].copy()
        for (ex, ey, ew, eh) in erase:
            screen.paste(255, (ex, ey, ex + ew, ey + eh))
        for (ex, ey, ew, eh) in desk:                # the grey desk's checkerboard,
            px = screen.load()                       # in step with the pixel above
            phase = (ex + ey - 1) % 2 if px[ex, ey - 1] == 0 else (ex + ey) % 2
            for y in range(ey, ey + eh):
                for x in range(ex, ex + ew):
                    px[x, y] = 0 if (x + y) % 2 == phase else 255
        if opts.get("nopointer") and not remove_pointer(screen):
            sys.exit("%s: no pointer found" % name)
        if "pointer" in opts:
            add_pointer(screen, *map(int, opts["pointer"].split(",")))
        cx, cy, cw, ch = crop_box(screen, crop)
        part = screen.crop((cx, cy, cx + cw, cy + ch))
        if crop == "menu":
            clear_around_menu(part, screen, cx)
        if opts.get("torn"):
            tear(part)
        zoom = int(opts["zoom"])
        part = part.resize((cw * zoom, ch * zoom), Image.NEAREST)
        ink = tuple(int(opts["ink"][i:i + 2], 16) for i in (0, 2, 4))
        paper = tuple(int(opts["paper"][i:i + 2], 16) for i in (0, 2, 4))
        rgb = Image.new("RGB", part.size, paper)
        rgb.paste(Image.new("RGB", part.size, ink), mask=part.point(lambda v: 255 - v))
        rgb.save(os.path.join(out, name + ".png"), optimize=True)
        print("%-14s %-7s %dx%d" % (name, crop, cw, ch))


main()
