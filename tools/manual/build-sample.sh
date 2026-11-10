#!/bin/sh
# Builds the Stage 2 sample pages at 7½ x 9 in (P24): the figures, the
# own-use cover and build-manual/MacPaint-sample.pdf. The cover's Woodcut
# document is rebuilt separately (rebuild-woodcut.py) and shot in a
# Mini vMac session (woodcut-screen.png, in the private assets folder).
set -eu
cd "$(dirname "$0")/../.."
PY=${MANUAL_TOOLS:-$HOME/MacPlusProjects/manual-tools}/venv/bin/python
mkdir -p build-manual
"$PY" -I tools/manual/make-figures.py docs/manual/figures/figures.txt docs/manual/figures/png
"$PY" -I tools/manual/make-cover.py
"$PY" -I tools/manual/make-sample.py
tools/manual/build-pdf.sh docs/manual/sample/sample.html build-manual/MacPaint-sample.pdf
swiftc -O tools/manual/pdftool.swift -o build-manual/pdftool
