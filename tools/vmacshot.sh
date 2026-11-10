#!/bin/sh
# Capture the running Mini vMac's window (even if other windows cover it)
# and convert it to an exact 512 x 342 Mac screen PNG.
# Usage: tools/vmacshot.sh OUT_DIR NAME
set -u
cd "$(dirname "$0")/.." || exit 2
OUT=$1; NAME=$2
P=$(pgrep -x minivmac) || { echo "Mini vMac isn't running"; exit 2; }
WID=$(tools/vmacctl/vmacctl "$P" window | awk 'NR==1{print $1}')
TMP=${TMPDIR:-/tmp}/vmacshot.$$
mkdir -p "$TMP" "$OUT"
screencapture -x -o -l "$WID" "$TMP/$NAME.png" &&
    ../manual-tools/venv/bin/python -I tools/grab-host-screens.py "$OUT" "$TMP/$NAME.png"
rm -r "$TMP"
