#!/bin/sh
# Open a Mini vMac session for testing MacPaint by hand, with MacPaint on
# a different volume from the System Folder:
#   disk 1: a copy of ~/minivmac/System607-hfs.img (Finder, Scrapbook,
#           MultiFinder; it starts up under MultiFinder)
#   disk 2: "PaintVol", with Graphics:MacPaint (original 1.5) and
#           Graphics:MacPaint 1.6 (patched)
# Everything is a copy in runs/<time>-interactive; the shared ~/minivmac
# folder is only read. The session stays open until you quit it
# (Special > Shut Down, then quit Mini vMac).
#
# Usage: tools/run-interactive.sh [--full-startup-disk] [--doc FILE.pntg]...
#   --full-startup-disk  fill the startup disk copy until about 2 KB is
#                        free (a file called "Filler" at its top level), so
#                        that copying a large picture can't be written to
#                        the Clipboard: the case improvement I2 is for.
#   --doc FILE.pntg      also put this MacPaint document (data fork only)
#                        in PaintVol:Graphics, named as the file without
#                        ".pntg"; repeatable.

set -u
FULL=0
DOCS=""
while [ $# -gt 0 ]; do
    case $1 in
        --full-startup-disk) FULL=1 ;;
        --doc) DOCS="$DOCS
$(cd "$(dirname "$2")" && pwd)/$(basename "$2")"; shift ;;
        *) echo "unknown option $1"; exit 2 ;;
    esac
    shift
done
cd "$(dirname "$0")/.." || exit 2
MINIVMAC=${MINIVMAC:-$HOME/minivmac}
PY=../transfer-tools/venv/bin/python

if pgrep -x minivmac > /dev/null; then
    echo "Mini vMac is already running: not starting another."; exit 2
fi
[ -f "build/MacPaint 1.6.rsrc" ] || { echo "run tools/patch-macpaint.py first"; exit 2; }

RUN=runs/$(date +%Y%m%d-%H%M%S)-interactive
[ $FULL = 1 ] && RUN=$RUN-full
DAT=$RUN/minivmac.app/Contents/mnvm_dat
mkdir -p "$RUN"
cp -R "$MINIVMAC/minivmac.app" "$RUN/"
mkdir -p "$DAT"
ln -s "$MINIVMAC/vMac.ROM" "$DAT/vMac.ROM"
cp "$MINIVMAC/System607-hfs.img" "$DAT/disk1.dsk"

if [ $FULL = 1 ]; then
    H=${RETRO68:-$HOME/Retro68-build}/toolchain/bin
    export HOME="$PWD/$RUN"          # hfsutils keeps its state file in $HOME
    free=$("$H/hmount" "$DAT/disk1.dsk" | sed -n 's/^Volume has \([0-9]*\) bytes free$/\1/p')
    size=$(( (free - 2048) / 512 * 512 ))
    dd if=/dev/zero of="$RUN/Filler" bs=512 count=$((size / 512)) 2>/dev/null
    "$H/hcopy" -r "$RUN/Filler" ":Filler" || exit 2
    "$H/humount" > /dev/null
    "$H/hmount" "$DAT/disk1.dsk" | grep "bytes free"
    "$H/humount" > /dev/null
    rm "$RUN/Filler"
fi

$PY -I - "$DAT/disk2.dsk" "$DOCS" <<'EOF' || exit 2
import os, sys, machfs
v = machfs.Volume(); v.name = 'PaintVol'
g = machfs.Folder(); v['Graphics'] = g
for name, path in (('MacPaint', 'originals/MacPaint-1.5.rsrc'),
                   ('MacPaint 1.6', 'build/MacPaint 1.6.rsrc')):
    f = machfs.File()
    f.type, f.creator, f.flags = b'APPL', b'MPNT', 0x2000
    f.rsrc = open(path, 'rb').read()
    g[name] = f
for path in filter(None, sys.argv[2].split('\n')):
    f = machfs.File()
    f.type, f.creator = b'PNTG', b'MPNT'
    f.data = open(path, 'rb').read()
    g[os.path.basename(path)[:-len('.pntg')]] = f
open(sys.argv[1], 'wb').write(v.write(size=1440 * 1024, bootable=False))
EOF

nohup "$RUN/minivmac.app/Contents/MacOS/minivmac" > "$RUN/minivmac.log" 2>&1 &
echo "Mini vMac started from $RUN"
