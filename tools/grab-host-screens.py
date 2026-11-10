"""Recover exact 512 x 342 Mac Plus screens from macOS screenshots of
Mini vMac (⌘-Shift-3 on the host), for when the Mac's own ⌘-Shift-3
can't be used: open menus, or macOS catching the keys first.

Mini vMac magnified 2x on a Retina display draws each Mac pixel as a
4 x 4 block of exactly (0,0,0) or (255,255,255). This finds the block
grid, reads one value per block and checks that every block is
uniform, so the result is either exact or rejected.

The one exception is the bottom corners, which macOS rounds off with
the window (and, bottom right, may shade with the floating thumbnail). If the lost pixels there lie in the grey desk's
checkerboard, they are filled from it; the
number filled is reported. Anything else lost is a rejection.

Usage (run with ../manual-tools/venv/bin/python -I, which has PIL):
    grab-host-screens.py OUT_DIR SCREENSHOT.png ...
"""
import os, sys
from PIL import Image

W, H, S = 512, 342, 4            # Mac screen; host pixels per Mac pixel
BLACK, WHITE, OTHER = 0, 1, 2


def classes(img):
    """Rows of codes: BLACK, WHITE, or OTHER for any other colour."""
    w, h = img.size
    code = {(0, 0, 0, 255): BLACK, (255, 255, 255, 255): WHITE}   # opaque only: a
    data = [code.get(p, OTHER) for p in img.convert('RGBA').get_flattened_data()]  # window
                                                   # capture's clipped corners are transparent
    return [data[y * w:(y + 1) * w] for y in range(h)]


def uniform(rows, x, y):
    a = rows[y][x]
    return a != OTHER and all(rows[y + j][x + i] == a for j in range(S) for i in range(S))


def score(rows, ox, oy):
    """Uniform blocks, not counting the outer ring of Mac pixels (the
    window edge may shade it) or the bottom corners (macOS rounds them)."""
    return sum(uniform(rows, ox + mx * S, oy + my * S)
               for my in range(1, H - 1) for mx in range(1, W - 1)
               if not corner(mx, my))


CORNER = 12                      # width of each bottom-corner area that may be filled
TALL = {False: 12, True: 24}     # its height, left and right: on the right, the
                                 # shadow of macOS's floating thumbnail reaches higher


def corner(x, y):
    right = x >= W - CORNER
    return (x < CORNER or right) and y >= H - TALL[right]


def longest_run(cells):
    best = (0, 0); run = 0
    for i, c in enumerate(cells):
        run = run + 1 if c != OTHER else 0
        if run > best[0]:
            best = (run, i - run + 1)
    return best


def find_grid(rows):
    """Top left of the Mac screen, from the widest and tallest runs of
    black and white, then the block grid nearby that fits exactly."""
    h, w = len(rows), len(rows[0])
    across = max(longest_run(rows[y]) for y in range(0, h, 16))
    if across[0] < W * S - 8:
        return None
    x0 = across[1]
    down = max(longest_run([rows[y][x] for y in range(h)])
               for x in range(x0 + 64, x0 + W * S - 64, 64))
    if down[0] < H * S - 8:
        return None
    y0 = down[1]
    best = max((score(rows, ox, oy), ox, oy)
               for oy in range(max(0, y0 - 4), min(h - H * S, y0 + 4) + 1)
               for ox in range(max(0, x0 - 4), min(w - W * S, x0 + 4) + 1))
    need = (W - 2) * (H - 2) - sum(corner(x, y) for y in range(1, H - 1) for x in range(1, W - 1))
    return best[1:] if best[0] == need else None


def read_screen(rows, ox, oy):
    """Mac pixels (BLACK/WHITE), with the bottom corners filled from the
    8-pixel pattern beside or above them. Returns (pixels, filled) or None."""
    mac = [[OTHER] * W for _ in range(H)]
    for y in range(H):
        for x in range(W):
            if 0 < x < W - 1 and 0 < y < H - 1:
                ok = uniform(rows, ox + x * S, oy + y * S)
            else:                                  # outer ring: inner pixels only
                bx, by = ox + x * S, oy + y * S
                ok = rows[by + 1][bx + 1] != OTHER and all(
                    rows[by + j][bx + i] == rows[by + 1][bx + 1] for j in (1, 2) for i in (1, 2))
            if ok:
                mac[y][x] = rows[oy + y * S + 2][ox + x * S + 2]
    filled = 0                                     # fill each lost corner pixel
    for _ in range(2 * max(TALL.values())):        # where the grey checkerboard
        for y in range(H - max(TALL.values()), H): # around it is certain: two
            for x in [*range(CORNER), *range(W - CORNER, W)]:   # pixels 2 away agree
                if mac[y][x] != OTHER or not corner(x, y):      # and none 1 away
                    continue                                    # matches them
                far = [mac[j][i] for i, j in ((x - 2, y), (x + 2, y), (x, y - 2), (x, y + 2))
                       if 0 <= i < W and 0 <= j < H and mac[j][i] != OTHER]
                near = [mac[j][i] for i, j in ((x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1))
                        if 0 <= i < W and 0 <= j < H and mac[j][i] != OTHER]
                if len(far) >= 2 and len(set(far)) == 1 and near and far[0] not in near:
                    mac[y][x] = far[0]
                    filled += 1
    if any(OTHER in r for r in mac):
        return None
    return mac, filled


def main():
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    out = sys.argv[1]
    os.makedirs(out, exist_ok=True)
    for path in sys.argv[2:]:
        name = os.path.splitext(os.path.basename(path))[0]
        rows = classes(Image.open(path))
        g = find_grid(rows)
        if g is None:
            print(f'REJECTED {name}: no exact 512 x 342 screen found')
            continue
        ox, oy = g
        r = read_screen(rows, ox, oy)
        if r is None:
            print(f'REJECTED {name}: pixels lost outside the repeating corner pattern')
            continue
        pix, filled = r
        mac = Image.new('1', (W, H))
        mac.putdata([255 * v for row in pix for v in row])
        mac.save(os.path.join(out, name + '.png'))
        print(f'ok {name}: screen at {ox},{oy}; {filled} corner pixels filled')


if __name__ == '__main__':
    main()
