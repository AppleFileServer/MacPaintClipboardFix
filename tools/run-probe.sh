#!/bin/sh
# Run the clipboard probe in a private copy of Mini vMac (two disks, see
# make-probe-disks.py) and print PaintVol:ProbeLog. About 30 seconds.
# Uses copies only: the shared ~/minivmac folder and its disks are read,
# never written.
#
# Usage: tools/run-probe.sh
#   MINIVMAC  the shared Mini vMac folder (default ~/minivmac)

set -u
cd "$(dirname "$0")/.." || exit 2
MINIVMAC=${MINIVMAC:-$HOME/minivmac}
PY=../transfer-tools/venv/bin/python
TIMEOUT=${PROBE_TIMEOUT:-90}

if pgrep -x minivmac > /dev/null; then
    echo "Mini vMac is already running: not starting another."; exit 2
fi
[ -f probe/build/Probe.dsk ] || { echo "build the probe first (probe/build)"; exit 2; }

RUN=runs/$(date +%Y%m%d-%H%M%S)
DAT=$RUN/minivmac.app/Contents/mnvm_dat
mkdir -p "$RUN"
cp -R "$MINIVMAC/minivmac.app" "$RUN/"
mkdir -p "$DAT"
ln -s "$MINIVMAC/vMac.ROM" "$DAT/vMac.ROM"
$PY -I tools/make-probe-disks.py "$MINIVMAC/System607-hfs.img" \
    "$MINIVMAC/autoquit-1.1.1.dsk" probe/build/Probe.dsk "$DAT" || exit 2

"$DAT/../MacOS/minivmac" &
pid=$!
t=0
while kill -0 $pid 2>/dev/null; do
    sleep 1; t=$((t + 1))
    if [ $t -ge $TIMEOUT ]; then
        echo "timed out after ${TIMEOUT}s: stopping this run's Mini vMac"
        kill $pid; break
    fi
done
echo "Mini vMac ran for ${t}s"

$PY -I -c '
import sys, machfs
for path, where in ((sys.argv[1], ()), (sys.argv[2], ("System Folder",))):
    v = machfs.Volume(); v.read(open(path, "rb").read())
    d = v
    for w in where: d = d[w]
    f = d.get("ProbeLog")
    if f:
        print(f.data.decode("mac_roman").replace("\r", "\n")); break
else:
    print("no ProbeLog written")
' "$DAT/disk2.dsk" "$DAT/disk1.dsk" | tee "$RUN/ProbeLog.txt"
