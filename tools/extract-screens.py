"""Extract MacPaint documents (such as the "Screen 0", "Screen 1" files that
⌘-Shift-3 saves) from a Mini vMac disk image as exact 1-bit PNGs.

Usage (run with ../transfer-tools/venv/bin/python -I):
    extract-screens.py DISK_IMAGE OUT_DIR [NAME_PREFIX]

DISK_IMAGE is read only. It may be a bare HFS volume or a partitioned
(BlueSCSI .hda) image. Every PNTG file whose name starts with NAME_PREFIX
(default "Screen") is decoded. For "Screen N" files, both the full 576×720
page and the 512×342 screen area (top left) are written. Other documents
give the page only.
"""
import os, struct, sys, zlib
import machfs


def volume(path):
    data = open(path, 'rb').read()
    if data[512:514] == b'PM':                     # Apple partition map
        for i in range(1, 64):
            b = data[i * 512:(i + 1) * 512]
            if b[:2] != b'PM':
                break
            start, size = struct.unpack('>II', b[8:16])
            if b[48:80].split(b'\0')[0] == b'Apple_HFS':
                data = data[start * 512:(start + size) * 512]
                break
    v = machfs.Volume()
    v.read(data)
    return v


def unpackbits(src, pos, need):
    out = bytearray()
    while len(out) < need:
        n = src[pos]; pos += 1
        if n < 128:
            out += src[pos:pos + n + 1]; pos += n + 1
        elif n > 128:
            out += bytes([src[pos]]) * (257 - n); pos += 1
    return bytes(out[:need]), pos


def decode_pntg(data):
    """MacPaint document -> list of 720 rows of 72 bytes (bit set = black)."""
    pos, rows = 512, []                            # 512-byte header, then 720 packed rows
    for _ in range(720):
        row, pos = unpackbits(data, pos, 72)
        rows.append(row)
    return rows


def write_png(path, rows, width):
    """Write 1-bit rows (bit set = black) as a greyscale-1 PNG (0 = black)."""
    nbytes = (width + 7) // 8
    raw = b''.join(b'\0' + bytes(x ^ 0xFF for x in r[:nbytes]) for r in rows)
    def chunk(t, d):
        return struct.pack('>I', len(d)) + t + d + struct.pack('>I', zlib.crc32(t + d) & 0xFFFFFFFF)
    png = (b'\x89PNG\r\n\x1a\n' + chunk(b'IHDR', struct.pack('>IIBBBBB', width, len(rows), 1, 0, 0, 0, 0))
           + chunk(b'IDAT', zlib.compress(raw, 9)) + chunk(b'IEND', b''))
    open(path, 'wb').write(png)


def walk(folder, path=''):
    for name, item in folder.items():
        if isinstance(item, machfs.Folder):
            yield from walk(item, path + name + ':')
        else:
            yield path + name, item


def main():
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    image, out = sys.argv[1], sys.argv[2]
    prefix = sys.argv[3] if len(sys.argv) > 3 else 'Screen'
    os.makedirs(out, exist_ok=True)
    found = 0
    for path, f in walk(volume(image)):
        name = path.split(':')[-1]
        if f.type != b'PNTG' or not name.startswith(prefix):
            continue
        page = decode_pntg(bytes(f.data))
        safe = path.replace(':', '_').replace('/', '-')
        write_png(os.path.join(out, safe + '.page.png'), page, 576)
        if name.startswith('Screen'):
            write_png(os.path.join(out, safe + '.png'), page[:342], 512)
        print(path)
        found += 1
    print(f'{found} document(s) written to {out}')


if __name__ == '__main__':
    main()
