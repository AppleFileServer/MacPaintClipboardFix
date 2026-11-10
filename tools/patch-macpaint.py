"""Make MacPaint 1.6 from a copy of MacPaint 1.5 (docs/PLAN.md sections 4, 7, 8 and 10).

Usage (run with ../transfer-tools/venv/bin/python -I):
    patch-macpaint.py ORIGINAL_RSRC OUT_DIR            make MacPaint 1.6
    patch-macpaint.py --reverse PATCHED_RSRC OUT_DIR   undo it (proves reversibility)

ORIGINAL_RSRC is MacPaint 1.5's resource fork (originals/MacPaint-1.5.rsrc;
its data fork is empty). The input is only read. The patcher refuses to
run unless the input's checksum and every byte it changes are exactly
as expected.

The changes, in addition to the version number:
  clipboard  Cut, Copy and Paste open the startup System Folder's
             Clipboard File (BootDrive) instead of the default volume.
  I1         Holding Command while choosing Quit no longer ejects the
             disk and restarts the Mac.
  I2         When Copy or Cut can't write the Clipboard: one alert (not
             one per failed piece), the Clipboard is left empty, and the
             selection is put down in place with the picture kept,
             instead of the selected pixels being blanked when the
             alert closes. Cut then deletes nothing.
  I4         File menu: Command-N New, Command-W Close, Command-Q Quit.

OUT_DIR gets:
    MacPaint 1.6.rsrc   the patched resource fork
    MacPaint 1.6.bin    MacBinary II, for transfer tools
    MacPaint 1.6.dsk    800 KB HFS floppy image holding the application
    SHA256SUMS
"""
import sys, os, struct, hashlib, binascii

ORIGINAL_SHA256 = '766faf80fcc7edf832d6da2f4c42e3bd8af221bcba0fd856e97f9b2e36e7b565'
NAME = 'MacPaint 1.6'
TYPE, CREATOR = b'APPL', b'MPNT'
FINDER_FLAGS = 0x2000          # hasBundle, as the original (0x2100) minus "inited"
# Fixed creation/modification date for the output files (21 October 2026,
# 12:00, seconds since 1 January 1904), so rebuilds give identical files.
MAC_DATE = 3875428800

OPEN_CALL_TAIL = bytes.fromhex('42A7 486D FF74 4EAD 01BA')   # NIL buffer, @scrapFile, JSR OpenFile

# In-place edits: (resource type, id, offset into the resource data or None
# to search for a unique match, original bytes, new bytes, why).
# Offsets count from the start of the resource data (CODE's 4-byte header included).
PATCHES = [
    (b'CODE', 4, 0xA8,
     bytes.fromhex('4267 4267 4267 2F2C 000C') + OPEN_CALL_TAIL,
     bytes.fromhex('2F38 020E 4267 2F2C 000C') + OPEN_CALL_TAIL,
     'clipboard, CutOrCopy: OpenFile drive 0 -> BootDrive (MOVE.L $020E,-(SP))'),
    (b'CODE', 5, 0x19C,
     bytes.fromhex('4267 4267 4267 2F2B 000C') + OPEN_CALL_TAIL,
     bytes.fromhex('2F38 020E 4267 2F2B 000C') + OPEN_CALL_TAIL,
     'clipboard, Paste: OpenFile drive 0 -> BootDrive (MOVE.L $020E,-(SP))'),
    (b'CODE', 1, 0x52F2,
     bytes.fromhex('4267 3F3C 0030 4EBA AD0A 101F 6704 4EBA 01F2'),
     bytes.fromhex('4267 3F3C 0030 4EBA AD0A 101F 6004 4EBA 01F2'),
     'I1, QuitProgram: IF KeyIsDown(Command) THEN EjectReset -> never (BEQ.S -> BRA.S)'),
    (b'CODE', 4, 0x98,
     bytes.fromhex('102D FB96 6704 4EAD 002A'),
     bytes.fromhex('4EBA 029A 4E71 4E71 4E71'),
     'I2, CutOrCopy start: JSR CopyStart (+0x334) replaces IF acceptFlag THEN AcceptEdits'),
    (b'CODE', 4, 0x12,
     bytes.fromhex('4267 3F3C 083C 4EAD 0192 3D5F 0008'),
     bytes.fromhex('4EBA 0308 4E71 4E71 4E71 4E71 4E71'),
     'I2, WScrapError: JSR ScrapAlertOnce (+0x31C) replaces MyAlert(2108)'),
    (b'CODE', 4, 0x2C0,
     bytes.fromhex('4267 3F2D FF74 4EAD 0072'),
     bytes.fromhex('4EBA 0040 4E71 4EAD 0072'),
     'I2, CutOrCopy label 9: JSR CopyFailGuard (+0x302); NOP'),
    (b'MENU', 2, None, b'\x03New\x00\x00', b'\x03New\x00N', 'I4, File menu: Command-N New'),
    (b'MENU', 2, None, b'\x05Close\x00\x00', b'\x05Close\x00W', 'I4, File menu: Command-W Close'),
    (b'MENU', 2, None, b'\x04Quit\x00\x00', b'\x04Quit\x00Q', 'I4, File menu: Command-Q Quit'),
    (b'DITL', 2006, None, b'MacPaint version 1.5', b'MacPaint version 1.6',
     'About box: version 1.6'),
    (b'MPNT', 0, None, b'MacPaint Version 1.5', b'MacPaint Version 1.6',
     'signature resource (Finder Get Info): version 1.6'),
]

# Code appended to CODE 4 for I2. A flag byte in ApplScratch ($0A78, the
# 12 bytes the system reserves for applications; MacPaint doesn't use them)
# records that the Clipboard couldn't be written during this Copy or Cut.
#   CopyFailGuard (+0x302) runs at CutOrCopy's label 9. If the flag is set it
#     empties the half-written Clipboard (scrapSize := 0, A4 = InfoScrap),
#     then does what MacPaint does before every other alert -- KillStuff (put
#     the selection down) and AcceptEdits -- so the activate event after the
#     alert can't blank the selected pixels. Then it makes the two pushes its
#     JSR displaced.
#   ScrapAlertOnce (+0x31C) replaces WScrapError's MyAlert call: it sets the
#     flag and shows "trouble writing the scrap" only the first time.
#   CopyStart (+0x334) replaces "IF acceptFlag THEN AcceptEdits" at the start
#     of CutOrCopy, clearing the flag first.
I2_CODE = bytes.fromhex(
    # CopyFailGuard
    '4A38 0A78'   # TST.B   $0A78.W        ; did the Clipboard write fail?
    '670A'        # BEQ.S   push
    '4294'        # CLR.L   (A4)           ; scrapSize := 0, Clipboard empty
    '4EAD 0152'   # JSR     338(A5)        ; KillStuff   (CODE 1 +0x6EA)
    '4EAD 002A'   # JSR     42(A5)         ; AcceptEdits (CODE 1 +0x5E6)
    '205F'        # push: MOVEA.L (SP)+,A0 ; our return address
    '4267'        # CLR.W   -(SP)          ; displaced: CloseFile result
    '3F2D FF74'   # MOVE.W  -140(A5),-(SP) ; displaced: scrapFile
    '4ED0'        # JMP     (A0)
    # ScrapAlertOnce
    '4A38 0A78'   # TST.B   $0A78.W
    '6610'        # BNE.S   done           ; already told the user
    '50F8 0A78'   # ST      $0A78.W
    '4267'        # CLR.W   -(SP)
    '3F3C 083C'   # MOVE.W  #2108,-(SP)    ; "...trouble writing the scrap."
    '4EAD 0192'   # JSR     402(A5)        ; MyAlert
    '544F'        # ADDQ.W  #2,SP          ; discard its result
    '4E75'        # done: RTS
    # CopyStart
    '51F8 0A78'   # SF      $0A78.W        ; no failure yet
    '4A2D FB96'   # TST.B   -1130(A5)      ; acceptFlag
    '6704'        # BEQ.S   +4
    '4EED 002A'   # JMP     42(A5)         ; AcceptEdits, returns to CutOrCopy
    '4E75')       # RTS
APPENDS = [
    (b'CODE', 4, 0x302, I2_CODE, 'I2, CopyFailGuard +0x302, ScrapAlertOnce +0x31C, CopyStart +0x334'),
]


# ---- resource fork reading and writing (keeps every other byte as it was) ----

def parse_fork(fork):
    """Return (header area, list of refs, map bytes). A ref is
    [data offset, type, id, attrs, ref-entry position in map, data bytes]."""
    data_off, map_off, data_len, map_len = struct.unpack_from('>IIII', fork, 0)
    rmap = bytearray(fork[map_off:map_off + map_len])
    type_list = struct.unpack_from('>H', rmap, 24)[0]
    ntypes = struct.unpack_from('>H', rmap, type_list)[0] + 1
    refs = []
    for t in range(ntypes):
        rtype, count, ref_off = struct.unpack_from('>4sHH', rmap, type_list + 2 + 8 * t)
        for r in range(count + 1):
            pos = type_list + ref_off + 12 * r
            rid, _name, attr_off = struct.unpack_from('>hHI', rmap, pos)
            off = attr_off & 0xFFFFFF
            length = struct.unpack_from('>I', fork, data_off + off)[0]
            body = fork[data_off + off + 4:data_off + off + 4 + length]
            refs.append([off, rtype, rid, attr_off >> 24, pos, bytearray(body)])
    refs.sort(key=lambda r: r[0])
    return bytes(fork[:data_off]), refs, rmap


def build_fork(head, refs, rmap):
    """Write the data blocks back in their original order and fix the offsets."""
    data = bytearray()
    for ref in refs:
        struct.pack_into('>I', rmap, ref[4] + 4, (ref[3] << 24) | len(data))
        data += struct.pack('>I', len(ref[5])) + ref[5]
    data_off = len(head)
    map_off = data_off + len(data)
    hdr = struct.pack('>IIII', data_off, map_off, len(data), len(rmap))
    rmap[0:16] = hdr                       # the map keeps a copy of the header
    return hdr + head[16:] + bytes(data) + bytes(rmap)


def find(refs, rtype, rid):
    return next(r for r in refs if r[1] == rtype and r[2] == rid)


def apply(fork, reverse):
    head, refs, rmap = parse_fork(fork)
    for rtype, rid, off, old, new, why in PATCHES:
        if reverse:
            old, new = new, old
        body = find(refs, rtype, rid)[5]
        if off is None:
            if bytes(body).count(old) != 1:
                sys.exit(f'refusing: {rtype.decode()} {rid} has {bytes(body).count(old)} copies of {old!r}, expected 1')
            off = bytes(body).index(old)
        if bytes(body[off:off + len(old)]) != old:
            sys.exit(f'refusing: {rtype.decode()} {rid} at {off:#x} is {bytes(body[off:off+len(old)]).hex()}, '
                     f'expected {old.hex()} ({why})')
        body[off:off + len(new)] = new
        print(f'  {rtype.decode()} {rid} +{off:#x}: {old.hex(" ", 2)} -> {new.hex(" ", 2)}  [{why}]')
    for rtype, rid, length, code, why in APPENDS:
        body = find(refs, rtype, rid)[5]
        if reverse:
            if len(body) != length + len(code) or bytes(body[length:]) != code:
                sys.exit(f'refusing: {rtype.decode()} {rid} does not end with the appended code ({why})')
            del body[length:]
            print(f'  {rtype.decode()} {rid}: removed {len(code)} appended bytes  [{why}]')
        else:
            if len(body) != length:
                sys.exit(f'refusing: {rtype.decode()} {rid} is {len(body)} bytes, expected {length} ({why})')
            body += code
            print(f'  {rtype.decode()} {rid} +{length:#x}: appended {code.hex(" ", 2)}  [{why}]')
    return build_fork(head, refs, rmap)


def check_no_other_sites(fork):
    """The clipboard OpenFile call must appear exactly at the two known sites."""
    _head, refs, _rmap = parse_fork(fork)
    sites = []
    for _off, rtype, rid, _a, _p, body in refs:
        if rtype != b'CODE':
            continue
        i = body.find(OPEN_CALL_TAIL)
        while i >= 0:
            if body[i - 4:i - 2] in (b'\x2f\x2c', b'\x2f\x2b') and body[i - 2:i] == b'\x00\x0c':
                sites.append((rid, i - 10))
            i = body.find(OPEN_CALL_TAIL, i + 1)
    want = [(4, 0xA8), (5, 0x19C)]
    if sorted(sites) != want:
        sys.exit(f'refusing: clipboard OpenFile calls found at {sites}, expected {want}')


def macbinary(name, rsrc, data=b''):
    n = name.encode('mac_roman')
    h = bytearray(128)
    h[1] = len(n); h[2:2 + len(n)] = n
    h[65:69], h[69:73] = TYPE, CREATOR
    h[73] = FINDER_FLAGS >> 8
    struct.pack_into('>IIII', h, 83, len(data), len(rsrc), MAC_DATE, MAC_DATE)
    h[101] = FINDER_FLAGS & 0xFF
    h[122] = h[123] = 129                      # MacBinary II
    struct.pack_into('>H', h, 124, binascii.crc_hqx(bytes(h[:124]), 0))
    pad = lambda b: b + bytes(-len(b) % 128)
    return bytes(h) + pad(data) + pad(rsrc)


def floppy(name, rsrc):
    import machfs
    v = machfs.Volume(); v.name = NAME
    f = machfs.File()
    f.type, f.creator, f.flags = TYPE, CREATOR, FINDER_FLAGS
    f.rsrc = rsrc
    f.crdate = f.mddate = MAC_DATE
    v[name] = f
    return v.write(size=800 * 1024, bootable=False)


def main():
    args = sys.argv[1:]
    reverse = args[:1] == ['--reverse']
    if reverse:
        args = args[1:]
    if len(args) != 2:
        sys.exit(__doc__)
    src, out = args
    fork = open(src, 'rb').read()
    digest = hashlib.sha256(fork).hexdigest()

    if reverse:
        print(f'undoing the patch in {src}')
        result = apply(fork, reverse=True)
        if hashlib.sha256(result).hexdigest() != ORIGINAL_SHA256:
            sys.exit('reversed file does not match the original MacPaint 1.5')
        os.makedirs(out, exist_ok=True)
        open(os.path.join(out, 'MacPaint 1.5 (unpatched).rsrc'), 'wb').write(result)
        print('ok: identical to the original MacPaint 1.5')
        return

    if digest != ORIGINAL_SHA256:
        sys.exit(f'refusing: {src} is not the MacPaint 1.5 this patch was made for (sha256 {digest})')
    if build_fork(*parse_fork(fork)) != fork:
        sys.exit('internal check failed: rebuilding the unchanged fork does not reproduce it')
    check_no_other_sites(fork)
    print(f'patching {src}')
    result = apply(fork, reverse=False)

    # Round trip: undoing must give back the original exactly.
    if hashlib.sha256(apply(result, reverse=True)).hexdigest() != ORIGINAL_SHA256:
        sys.exit('internal check failed: the patch does not undo cleanly')
    print(f'  {len(fork)} -> {len(result)} bytes; undo checked: gives back the original exactly')

    os.makedirs(out, exist_ok=True)
    files = {
        NAME + '.rsrc': result,
        NAME + '.bin': macbinary(NAME, result),
        NAME + '.dsk': floppy(NAME, result),
    }
    for fn, b in files.items():
        open(os.path.join(out, fn), 'wb').write(b)
    with open(os.path.join(out, 'SHA256SUMS'), 'w') as s:
        for fn, b in files.items():
            s.write(f'{hashlib.sha256(b).hexdigest()}  {fn}\n')
    print(f'written to {out}: ' + ', '.join(files))


if __name__ == '__main__':
    main()
