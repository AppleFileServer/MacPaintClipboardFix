# MacPaint Clipboard Fix

A small standalone project to make MacPaint's Cut, Copy and Paste
(and so the Scrapbook) work when MacPaint lives on a different volume
from the System Folder. It is separate from the classic Mac suite
programme in `../Programme` and is not listed in its catalogue.

- **Started:** 19 October 2026
- **Status:** MacPaint 1.6 (clipboard fix plus I1, I2, I4) built and passed in Mini vMac on 21 October 2026; awaiting Jack's test on the real Mac Plus (`docs/TEST-ON-MAC-PLUS.md`)
- **Plan:** [`docs/PLAN.md`](docs/PLAN.md)

## What's here

| Path | Contents |
|---|---|
| `source/chm-original/` | The MacPaint 1.3 source exactly as released by the Computer History Museum in 2010 (`102658076_macpaint_acc.zip`, unpacked into `extracted/`) |
| `source/gryphel-1.3-gry2/` | Paul C. Pratt's 2014 MPW rebuild of 1.3 (Gryphel Project): disk image, plus its contents unpacked into `disk-contents/` (modified source in `src/`, built app, build script) |
| `originals/MacPaint-1.5.rsrc` | Read-only reference copy of the resource fork of the MacPaint 1.5 actually used on the Mac Plus, taken from `BlueSCSI-backups/HD20_512 Applications 40 MB 2026-10-14.hda` (`Graphics:MacPaint`). MacPaint keeps all its code in the resource fork; the data fork is empty. |
| `tools/` | Python inspection scripts (run with `../transfer-tools/venv/bin/python -I`); `make-probe-disks.py` and `run-probe.sh` for probe runs |
| `probe/` | Clipboard probe (Retro68 C): repeats MacPaint's and the Scrapbook's clipboard calls in Mini vMac and logs the results. Build: `cmake -S probe -B probe/build -DCMAKE_TOOLCHAIN_FILE=$HOME/Retro68-build/build-target/cmake/retro68.toolchain.cmake && cmake --build probe/build`; run: `tools/run-probe.sh` (about 2 seconds of emulator time, uses private copies of Mini vMac and the System disk) |
| `runs/` | Kept probe runs: disks and `ProbeLog.txt` |
| `build/` | The patched copy, `MacPaint 1.6` (`.rsrc`, MacBinary `.bin`, 800 KB `.dsk`), with `SHA256SUMS`. Remake with `tools/patch-macpaint.py originals/MacPaint-1.5.rsrc build` |
| `SHA256SUMS` | Checksums of the downloads and the reference copy |

## Rules

- **Never modify an original.** Patch only copies, and keep the
  unpatched MacPaint on the Mac until the patched one has proved itself
  (in line with programme decision P12).
- **Licence:** the MacPaint source is "Copyright © 1984 Apple Inc. and
  is made available only for non-commercial use". Keep this project
  personal and non-commercial, and don't redistribute patched builds.

## Sources

- Computer History Museum, "MacPaint and QuickDraw Source Code":
  https://computerhistory.org/blog/macpaint-and-quickdraw-source-code/
  (zip: https://d1yx3ys82bpsa0.cloudfront.net/102658076_macpaint_acc.zip)
- Gryphel Project, MacPaint: https://www.gryphel.com/c/sw/general/macpaint/
