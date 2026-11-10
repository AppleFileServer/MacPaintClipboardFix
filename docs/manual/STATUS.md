# MacPaint User's Guide: status

## Current stage

**Stage 2 sample pages** rebuilt at **7½ × 9 in** (Programme P24,
25 Oct 2026, superseding P23's A5), waiting for Jack's print check. The
cover shows MacPaint 1.6 with the rebuilt Woodcut (shot 25 Oct). Stage 1 is
still waiting for Jack's review.

## Completed work

- **19 Oct 2026, Stage 0:**
  - research report (`STAGE0-REPORT.md`) and evidence (`research/`);
  - the other projects were only read; nothing was committed.
- **21 Oct 2026, Stage 1:**
  - `style-guide.md`: the A5 adaptation of the house style;
  - `outline.md`: detailed contents, about 120 pages;
  - `figures.md`: illustration register and session 1 shot list;
  - `terminology.md`;
  - `fact-check.md`: evidence levels, established facts and 20 CHECK
    items.

- **21 and 25 Oct 2026, screenshot sessions 1 and 2:** see below.
- **25 Oct 2026, Stage 2 sample pages** (`tools/manual/build-sample.sh`):
  - (first built at A5 with an A4 two-up copy; rebuilt at 7½ × 9 in
    the same day, P24) `build-manual/MacPaint-sample.pdf`, 10 pages: cover, copyright,
    title, contents, About This Manual, Chapter 1 opener spread,
    Lesson 3 (labelled screen), Lesson 10 (Show Page and grabber), the
    Edit menu's reference page;
  - toolset copied from MacTrack's (read only) into `tools/manual/`
    and renamed; "MacPaint Garamond 100" built into
    `manual-tools/fonts/built-macpaint/`; `manual.css` re-derived for
    the family page; the own-use cover (`manual-assets-private/cover-macpaint.jpg`)
    made from MacDraw's;
  - new: `pdftool.swift` (renders pages), `rebuild-woodcut.py`, and in
    `make-figures.py` a `desk=` option and 1-pixel menu shadows.

## Decisions made

| | Decision | By |
|---|---|---|
| D1 | ~~A5 portrait~~ **7½ × 9 in**, the family size (Programme P24, superseding P23) | Jack, 21 Oct; changed 25 Oct |
| D2 | Document **MacPaint 1.6** | Jack, 21 Oct |
| D3 | **Own-use edition only** | Jack, 21 Oct |
| D4 | Sources in `MacPaintClipboardFix/docs/manual/`; the folder isn't renamed | decided, reversible |
| D6 | The family structure: Learning (13 lessons), Using (task pages), Reference, Appendixes A–E | decided |
| D5 | ~~Printed on A4, cut to A5~~ (P23, superseded). Still: double-sided, colour laser, good paper, wire bound | Jack, 21 and 25 Oct |
| D8 | The cover keeps MacPaint's **Woodcut** (as Apple's 1984 manual), rebuilt from the cover scan onto the sharp MacDraw cover | Jack, 25 Oct |
| D7 | Screens from Mini vMac, as exact pixels from macOS screenshots of its window (the Mac's own ⌘-Shift-3 never reaches it). Since 25 Oct Claude can drive the sessions itself (`tools/vmacctl`, `tools/vmacshot.sh`). Open menus are shot, not drawn | Jack, 21 and 25 Oct |

**Programme P24** (`../../../Programme/DECISIONS.md`, 25 Oct) supersedes
P23: every MacLife manual stays 7½ × 9 in. MacMoney's specification §13
still says A5 and needs updating in its own session.

## Outstanding questions

1. **Withdrawn** (P24): how bleed pages are cut from A4.
2. **Settled:** the example picture is a house with a tree (Jack,
   21 Oct): Example 1, painted 25 Oct.
3. **Settled:** the Mac Plus prints to an **ImageWriter** (Jack, 21 Oct). The printing pages and the Catalog figure describe it.
4. **C20:** the Mac Plus test of 1.6's Clipboard behaviour. Until it
   passes, the Clipboard text is marked CHECK.

## Verification results

The manual hasn't been built yet. MacPaint 1.6 itself passed every
Mini vMac test (`../PLAN.md` §9–§11).

## Screenshot session 1 (21 October 2026)

- Mini vMac was opened (`runs/20261021-110954-interactive`) for Jack to
  take the four shots.
- Jack had to leave and allowed Claude to drive Mini vMac for the
  session. Claude's tool for sending key and mouse events to Mini vMac
  was **blocked by Claude Code's safety check**. Claude didn't work
  around it, so the shots are **not taken yet**.
- **Ready:** `tools/extract-screens.py` reads the ⌘-Shift-3 "Screen N"
  files (or any MacPaint document) from a disk image as exact 1-bit
  PNGs. It was tested on a MacPaint document from the Applications disk
  backup.

## Checking the printed sample

`build-manual/MacPaint-sample.pdf` (10 pages, 7½ × 9 in). Print it
double-sided on the colour laser and look at:

1. **Menu text** at 0.6 pt per pixel (Lesson 3, Lesson 10) and at 0.48
   (the Edit menu, beside the text): is Chicago readable?
2. **The cover and the opener**, which run to the page edges: how they
   come out on the printer and paper used.
3. **The grey opener art** and the grey notes print cleanly.
4. **The cover's Woodcut** (once shot): good enough as a rebuild?

Also for Jack:
- The copyright page says "MacPaint © 1985 Apple Computer, Inc." as
  MacPaint 1.6's About box does, not the draft's "1983–1985".
- CHECK tags (red) mark the Edit menu's source-only facts. They'll be
  tested in a session and never print in the book.

## Next steps

1. Jack prints and checks the sample (above), and reviews the Stage 1
   documents.
2. Then Stage 3: the manuscript, starting with Chapter 1, with screenshot
   sessions (Claude driving) for its figures and the remaining CHECK
   items.
