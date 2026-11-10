#!/bin/sh
# Builds a PDF from one of the manual's HTML files (copied from MacTrack's,
# which came from MacMusic's): copies it, docs/manual/manual.css, the
# figures and the fonts into build-manual/, then prints it with headless
# Chrome (tools/manual/print-pdf.py), Paged.js laying out the pages.
# The tools live outside the repository:
#   MANUAL_TOOLS   default ~/MacPlusProjects/manual-tools
#
# The own-use edition's private assets (D3: this book has no other
# edition) are copied into build-manual/private/, never into the
# repository:
#   MANUAL_ASSETS  default ~/MacPlusProjects/manual-assets-private
#
# Usage: tools/manual/build-pdf.sh <html file> <out.pdf> [<anchors.json>]
#   MANUAL_BUILD   the folder it builds in (default build-manual)

set -eu
cd "$(dirname "$0")/../.."
TOOLS=${MANUAL_TOOLS:-$HOME/MacPlusProjects/manual-tools}
ASSETS=${MANUAL_ASSETS:-$HOME/MacPlusProjects/manual-assets-private}
CHROME=$TOOLS/chrome-headless-shell-mac-arm64/chrome-headless-shell
SRC=$1
OUT=$2
B=${MANUAL_BUILD:-build-manual}
# Clear only what's copied in, so other PDFs are kept.
rm -rf "$B/fonts" "$B/figures" "$B/private" "$B/page.html"; mkdir -p "$B/fonts" "$B/figures"
if [ -d "$ASSETS" ]; then
    mkdir -p "$B/private"
    cp "$ASSETS"/cover-macpaint.jpg "$ASSETS"/rainbow-logo.png "$B/private/" 2>/dev/null || true
fi
cp "$SRC" "$B/page.html"
cp docs/manual/manual.css "$TOOLS/paged.polyfill.js" "$B/"
cp docs/manual/figures/png/*.png "$B/figures/"
cp "$TOOLS"/fonts/built-macpaint/*.ttf "$B/fonts/"
"$TOOLS/venv/bin/python" tools/manual/print-pdf.py "$CHROME" "$B/page.html" "$OUT" ${3:+"$3"}
