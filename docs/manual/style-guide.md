# MacPaint User's Guide: style guide

Stage 1, 21 October 2026; revised 25 October 2026.

> **25 October 2026: back to 7½ × 9 in (Programme P24, superseding
> P23).** Jack reversed D1/D5: this book, like every MacLife manual, is
> made at the family's 7½ × 9 in page, with MacTrack's grid, type sizes
> and stylesheet unchanged. §2–§4 below describe the withdrawn A5
> design and are kept only as a record. What still applies from them:
> double-sided printing on a colour laser on good paper, wire bound.
> Figures: a whole screen (512 pixels) fills the 308 pt text column at
> 0.6 pt per pixel; small figures beside the text may use 0.48. The
> cover keeps MacPaint's own Woodcut on its screen (§6).

This book uses the MacLife house style (design "B"). This guide records
only what is specific to this book. Everything else follows the house
style unchanged:

- **Authority:** the MacMusic style guide, SG1–SG10
  (`~/MacPlusProjects/MacMusicPlayer/docs/manual/style-guide.md`).
- **Refinements:** MacTrack's later additions, §8.1–8.3 and TS6
  (`~/MacPlusProjects/MacWellness/docs/manual/`).
- **In this repository:** in Stage 2 the style guide, CSS and scripts are
  copied in and renamed, so the book can be rebuilt from this repository
  alone.

All A5 numbers below are proposals until the Stage 2 prototype is
printed and approved.

## 1. Decisions this guide rests on

| | Decision | Source |
|---|---|---|
| D1 | A5 portrait, 148 × 210 mm, as the new MacLife standard | Jack, 21 Oct 2026 |
| D2 | The book documents **MacPaint 1.6** | Jack, 21 Oct 2026 |
| D3 | **Own-use edition only**, never shared | Jack, 21 Oct 2026 |
| D4 | The sources live in `MacPaintClipboardFix/docs/manual/`, and the folder keeps its name | decided, reversible |
| D5 | Printed on **A4, cut to A5, wire bound** (Programme decision P23) | Jack, 21 Oct 2026 |
| D6 | The family structure: Learning, Using, Reference, Appendixes | decided |
| D7 | Screens come from Mini vMac (⌘-Shift-3), in sessions Jack drives from a shot list. Open menus are drawn from MacPaint's own resources | Jack, 21 Oct 2026 |

## 2. Page and grid (A5)

The family page is 540 × 648 pt. A5 is 419.5 × 595.3 pt: 0.78 of the
width but 0.92 of the height. A straight scale doesn't work, so the grid
is re-derived from the width, and the extra height gives each page a few
more lines.

| Element | Family (7½ × 9 in) | A5 (proposed) |
|---|---|---|
| Page | 540 × 648 pt | 419.5 × 595.3 pt |
| Margins (top, right, bottom, left) | 40 / 40 / 50 / 52 pt | 31 / 40 / 39 / 40 pt (both sides clear the wire, §3) |
| Text area | 448 × 558 pt | 339.5 × 525 pt |
| Margin column | 118 pt | 90 pt |
| Gutter, with a 0.6 pt grey rule | 22 pt | 17 pt |
| Text column | about 308 pt | about 232.5 pt (82 mm) |
| Wide margin | always on the left (not mirrored) | margin column on the left; left and right margins equal for double-sided wire binding (§3) |

**Task pages.** The family's four-column task grid doesn't fit A5: the
columns would be about 75 pt wide. On A5, a task page puts the topic
heading and its short introduction in the margin column, and stacks the
tasks ("To …") in the text column, with small figures after each step.

**Chapter openers.** As in the family: a full-bleed two-page spread
showing a MacPaint screen in light grey, with the white chapter panel in
the margin column of the right-hand page. The panel has MacTrack's red
0.75 pt box.

## 3. Printing and binding (D5, Programme P23)

Manuals are generated at A5, printed on **A4**, **cut** to A5 and
**wire bound**. The PDF stays at A5 page size. The printing
consequences are worked out in the prototype:

- **Two pages to a sheet.** Two A5 pages fit exactly on one A4 sheet,
  so the build also makes a print copy imposed two-up on A4, with a
  cutting line. Cutting the sheet in half leaves no trimming margin.
- **The printer's unprintable edge** (about 4–5 mm) falls on three
  edges of each A5 page, so nothing can print right to those edges.
  The cover and the chapter openers can't bleed unless each page is
  printed on its own A4 sheet and trimmed on all four sides. That uses
  twice the paper and four cuts per page. **Proposal:** give the bleed
  pages a white border that matches the printer's edge. To be decided
  with the printed prototype.
- **Binding margin: printed double-sided** (Jack, 21 Oct 2026). Wire
  binding goes on the left of right-hand pages and the right of
  left-hand pages, so **both side margins must clear the holes**, about
  12–15 mm. The house style keeps the margin column on the left of every
  page. The margins are therefore **40 pt (14 mm) left and right**
  (top 31, bottom 39), which gives a text area of 339.5 × 525 pt. The
  grid in §2 becomes:
  - margin column 90 pt;
  - gutter 17 pt;
  - text column about 232.5 pt (82 mm).

  The prototype is printed double-sided and punched to check this.
- **Printer and paper:** a **colour laser** printer on good-quality
  paper (Jack, 21 Oct 2026).
  - The red-orange accent (`#e0442b`) prints in colour.
  - Screens and figures stay pure black.
  - Laser output is typically 600 dpi, so the figure scales in §5
    (0.48 and 0.6 pt per screen dot) fall on whole printer dots.
  - The prototype also checks that the light-grey opener art and the
    grey notes reproduce cleanly.

## 4. Type

The type keeps the family's typefaces, colours and hierarchy at sizes
reduced for the narrower column. That gives about 50–55 characters per
line, close to the family's line length.

| Element | Family | A5 (proposed) |
|---|---|---|
| Body | MacMusic Garamond 100, 13/16 | **MacPaint Garamond 100, 11/14** |
| Margin heads | bold Helvetica 14/16, red | 12/14, red |
| Contents head | bold Helvetica 18/20, red | 16/18, red |
| Lesson head (with red numbered square) | 10.5/12.5 | 9.5/11.5, 15 pt square |
| Step | 10.5/13 | 9.5/12 |
| Task head ("To …") | 10.5/12.5 | 9.5/11.5 |
| Task and table text | 11/13.5 | 10/12.5 |
| Reference sub-head | 11/13 | 10/12 |
| Chapter number / name on the opener | 15 / 22/25 Garamond | 13 / 19/22 |
| Appendix, Glossary and Index titles | 26/30 | 22/26 |
| Callouts | Helvetica 8.5–9 | Helvetica 8 |
| Running feet | Garamond 9.5, grey | 8.5, grey |
| Keycaps | Helvetica 8.5 | 7.5 |
| Copyright page | 9.5/12 | 8.5/11 |

Nothing is smaller than 7.5 pt. **The font** is EB Garamond, built and
renamed "MacPaint Garamond 100" with the family's `condense-font.py`
(at width 1.00), as the OFL requires. **The sans serif** is the
system's Helvetica, as in the family.

## 5. Figures

- **Screens** are exact 1-bit Mac Plus pixels, reproduced as the family
  does: enlarged by whole pixels and rendered pixelated, in pure black,
  with the window's own frame as the edge, a torn edge for partial
  screens, and **no captions or figure numbers** in the book (they live
  in `figures.md`).
- **Scale.** To keep pixels sharp on a 300 or 600 dpi printer, figures
  use scales that are a whole number of printer dots per screen pixel:
  - **0.48 pt per pixel** (2 dots at 300 dpi, 4 at 600) for windows and
    parts of windows in the text column. The MacPaint window
    (416 × 240) is then 200 × 115 pt.
  - **0.6 pt per pixel** (5 dots at 600 dpi) for full screens, which
    span the margin and text columns (MacTrack's `figure.across`). The
    full screen (512 × 342) is then 307 × 205 pt.
  - **Check:** the prototype print tests that Chicago 12 menu text
    stays readable at 0.48. If it doesn't, window figures move to 0.6
    and span both columns.
- **Open menus and dialogs that can't be captured** are drawn pixel
  for pixel from MacPaint's own resources (MENU, DLOG/DITL, ALRT) in
  the Chicago bitmap font. `figures.md` labels them "drawn", never
  "shot".
- **MacPaint's own help screens** (Goodies › Introduction, Short Cuts)
  are reproduced from PICT 2400 and 2401 in the program.
- **Example artwork** (brush strokes, patterns, before and after) is
  painted in MacPaint itself during the sessions, so every example is
  genuine MacPaint output. Nothing is copied from Apple's manual.
- **Callouts:** Helvetica 8 pt labels in the margin column, red 0.7 pt
  leaders (`callouts.py`). Red action marks show click and drag, in the
  family's style, which itself comes from MacPaint's own manual.
- **Colour and black.** The book is printed on a colour laser, so the
  red accent prints red. Still, no information depends on the colour
  alone, so a black-only print stays usable.

## 6. Covers and front matter (own-use edition only)

- **Front cover:** the family's own-use cover, made from MacDraw's
  cover (hand, mouse, cable and pale-blue screen,
  `manual-assets-private/macdraw-cover-4489.png`), which has the same
  layout as Apple's 1984 MacPaint manual cover but a far sharper scan.
  Its screen shows MacPaint 1.6 with the **Woodcut** open, as the 1984
  cover did (Jack, 25 Oct 2026). No copy of the Woodcut document was
  found, so `tools/manual/rebuild-woodcut.py` rebuilds it from the 1984
  cover scan (1.5 scan pixels per Mac pixel): close, but not MacPaint's
  own pixels. It and the cover stay in the private assets folder. The
  title is "MacPaint User's Guide" in Garamond, at the top left with the
  rainbow logo.
- **Inside front cover (copyright page)** in two columns, drafted
  wording:
  - "MacPaint User's Guide © 2026 Jack McAteer." Rights paragraph as in
    the family.
  - "MacPaint was written by Bill Atkinson. MacPaint © 1985 Apple
    Computer, Inc." (as MacPaint's own About box says)
  - "MacPaint 1.6 is a personal modification of MacPaint 1.5, made for
    this edition and used under the terms on which Apple released
    MacPaint's source code: for non-commercial use only."
  - The not-affiliated statement, as in the family.
  - The trademark line.
  - Edition line: "MacPaint 1.6 · First edition, [month] 2026 ·
    Own-use edition: not for distribution".
  - Right column: the disclaimer, as in the family.
- **Title page, back cover, "Tell Us What You Think":** as in the
  family's own-use edition. The Legal Statement page is left out,
  because there is no shareable licence for this program.

## 7. Editorial rules specific to this book

- **Voice and spelling:** as the family (SG). Apple's 1984–85 voice,
  British spelling, and the Mac's own words quoted exactly as they
  appear (e.g. "Align Middle", "FontSize", "Goodies", "9 point").
- **Names:** tools, palettes and menus are named as in `terminology.md`.
  Menu commands are named exactly as in the program.
- **The world described:** a Macintosh Plus with System 6.0.7, the
  Finder or MultiFinder, a hard disk and floppies, and an ImageWriter or
  LaserWriter, with the **ImageWriter** shown and used for examples (Jack's printer, 21 Oct 2026). Nothing about emulators, SD
  cards, modern Macs or the patch work.
- **Version:**
  - The book describes MacPaint 1.6 throughout.
  - A short appendix, "About MacPaint 1.6", says how it differs from
    1.5, so a reader with 1.5 knows what doesn't apply.
  - Until the Mac Plus test passes, every passage about Clipboard
    behaviour that depends on 1.6 is marked CHECK in the manuscript.
- **"Important" notes** (two or three in the book). Candidates:
  - only one document can be open at a time;
  - dragging the picture off the page in Show Page can't be undone;
  - Revert can't be undone.
- **No invented features.** Every instruction traces to an entry in
  `fact-check.md`.
