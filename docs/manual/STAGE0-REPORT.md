# MacPaint User's Guide: Stage 0 research report

19 October 2026. Stage 0 only: research and proposals, no manual
production. Evidence is in `research/` beside this file.

Tags: **[seen]** observed directly in files or the binary; **[source]**
from the MacPaint 1.3 source, probably true of 1.5 but not proven;
**[inferred]**; **[unverified]** needs the running application.

## 0. Working directory and boundaries

- **Location (decided, reversible):** `~/MacPlusProjects/MacPaintClipboardFix/`,
  which already holds MacPaint's source, binaries and patch. The suite
  convention is that a manual lives in its application's repository
  (`docs/manual/` and `tools/manual/`, as in MacMusic and MacTrack), so
  the manual goes in `docs/manual/` and, later, `tools/manual/`.
- **Separation:** the patch work (`originals/`, `build/`, `probe/`,
  `tools/patch-*`, `docs/PLAN.md`) is not touched by the manual.
- **No git:** this folder isn't a git repository, so there's no
  branch or uncommitted work to protect. Nothing has been committed
  anywhere.
- **Other projects:** MacMusic, MacTrack, MacMoney, Programme,
  `manual-tools` and `manual-assets-private` were only read.

## 1. Reference manuals and assets found

| What | Where | Status |
|---|---|---|
| MacMusic User's Guide, 2nd ed. (1.1), 92 pp, own-use and plain | `releases/MacMusic-1.1/` | **Approved** (manual-1.1-part-d.md, 13 Oct). The most authoritative model |
| MacMusic Utilities, 1st ed., 110 pp, own-use only | `releases/MacMusic-1.1/` | Committed |
| MacTrack User's Guide, 112 pp, plus Quick Start and Keyboard Card | `releases/MacTrack-B-0.9.0-candidate-feba0f6/` (plain), `…-own-use/` | **Candidate**, not final. Its CSS adds later refinements (boxed opener title, `figure.across`, figure rules §8.1–8.3) |
| MacMoney manual | — | **Does not exist.** The only mention is `MacMoney/docs/SPECIFICATION.md` §13: "Formal MacLife manuals should use A5…" |
| Style guides | `MacMusicPlayer/docs/manual/style-guide.md` (SG1–SG10), `docs/plans/manual-1987.md`; `MacWellness/docs/manual/`, `docs/plans/manual-1987.md` (TM, TS, TF) | Authoritative for the house style |
| Build scripts | `MacMusicPlayer/tools/manual/`, `MacWellness/tools/manual/` (per-project copies) | — |
| Shared tools | `manual-tools/`: headless Chrome 155, Paged.js 0.4.3, EB Garamond plus renamed builds, venv | Archived in `environment-1.0/manual-tools.tar.gz` |
| Private Apple artwork for own-use editions | `manual-assets-private/` (MacDraw cover, rainbow logo, per-product covers) | Never shared |
| MacDraw manual (the suite's visual reference) | `~/MacPlus/Manuals/MacDraw Manual.pdf` (123 pp) | Reference scan |
| Original MacPaint manual | `~/MacPlus/Manuals/MacPaint Manual 1984.pdf`, `~/Macintosh/Macintosh Manuals/MacPaint 1983.pdf` | The **same scan** (pixel-identical renders). Part no. 030-0848-D, ©1983, a 1985 printing |
| MacPaint 1.5 (your copy) and 1.3 source | `originals/`, `source/` | Your 1.5 is identical, resource for resource, to archive.org's 1.5 |
| MacPaint's built-in help screens | `research/help-introduction-PICT2400.png`, `research/help-shortcuts-PICT2401.png` | Real 1-bit 416×240 pictures from the 1.5 binary |

## 2. Verified publishing conventions

These are measured from the PDFs and the CSS in `docs/manual/manual.css`
and `tools/manual/make-book.py` of both projects.

**Page size: not A5. Every MacLife manual and card is 7½ × 9 in
portrait (540 × 648 pt, 190.5 × 228.6 mm).** A5 is 148 × 210 mm, and
nothing has ever been built at A5. The A5 sentence in MacMoney's
specification is the only source. See decision D1.

**Page and grid**
- **Margins:** top 40 pt, right 40, bottom 50, left 52. They are not
  mirrored: the wide margin is always on the left.
- **Text area:** 448 × 558 pt.
- **Columns:** a 118 pt margin column, then a 22 pt gutter with a
  0.6 pt grey rule, then a text column of about 308 pt. Task pages use
  4 columns with rules.
- **Allowances:** none for binding or bleed. SG3 records a wire-O look
  with a spine flap, but the flap is never built.

**Type**
- **Body:** EB Garamond renamed per product (the OFL requirement:
  "MacMusic Garamond 100", "MacTrack Garamond 100"), 13/16 pt, ragged
  right.
- **Headings and labels:** Helvetica.
- **Colours:** red-orange accent `#e0442b`, grey notes `#8c8c8c`.
- **Hierarchy:**
  - margin heads: bold Helvetica 14/16, red;
  - lesson heads: 10.5 pt with a red numbered square;
  - steps: 10.5 pt with a black square;
  - task heads ("To …"): 10.5 pt;
  - reference sub-heads: 11 pt with a red square;
  - tables: Helvetica heads with Garamond rows;
  - keycaps: rounded Helvetica 8.5 pt.

**Chapters and running feet**
- **Openers:** a full-bleed two-page spread showing the program's own
  1-bit screen in light grey. A white panel in the margin column
  carries "Chapter n" (15 pt) and the chapter name (22/25 pt); MacTrack
  adds a red box around the panel.
- **After the opener:** the chapter's own contents page, then an
  Introduction.
- **Running feet, no heads:** 9.5 pt grey Garamond. Left pages read
  "number, chapter name"; right pages read "section name, number".
- **Numbering:** front matter in lower-case roman. Arabic numbers start
  at 2 on Chapter 1's left opener page.
- **Contents:** one book-wide page, with chapters in bold Helvetica and
  sections in Garamond. Numbers sit flush right with no leaders, and
  come from a two-pass build.

**Figures**
- Exact 1-bit Mac Plus screens, reproduced pixel for pixel. The PNGs
  are enlarged by whole pixels and rendered pixelated, in pure black.
- No added border: the window's own frame is the edge. Partial screens
  get a torn edge.
- **No captions or figure numbers in the books.** The numbers live
  only in `figures.md`.
- **Labels:** Helvetica 8.5–9 pt callouts in the margin, with red
  0.7 pt leaders. Red action marks (taken from MacPaint's own manual)
  show clicks and drags.
- **Scale:** about 0.6 pt per screen pixel, within the text column.

**Notes**
- Grey Garamond for remarks you can skip.
- "Important": the word in bold Helvetica in the margin, the note
  between 0.8 pt black rules, used 2–3 times per book.
- Text to type: Helvetica, between dotted rules.

**Covers and front matter**
- **Plain edition:** the program's 32×32 icon, the title in Garamond
  34/38, and the screen tinted pale blue in a 10 pt frame.
- **Own-use edition:** MacDraw's cover art (hand, mouse and cable) with
  the screen pasted in.
- **Title page:** the name in Garamond 30/34, with the icon or logo.
- **Copyright page:** two columns, 9.5/12.
  - Left column: "© 2026 Jack McAteer", "independent project, … not
    affiliated with … Apple Inc.", a trademark line, credits, and the
    edition line (e.g. "MacMusic 1.1 · Second edition, October 2026").
  - Right column: the disclaimer.
- **Back matter:** Legal Statement (MacMusic), a "Tell Us What You
  Think" page, and a back cover with the publisher's name in heavy
  Helvetica.

**Editions**
- **Plain:** no Apple artwork. This is the shareable edition.
- **Own-use:** adds the Apple artwork from `manual-assets-private`.
  `make-book.py` builds own-use when those assets are present.

**Editorial**
- Apple's 1984–85 voice: "you", short steps, the result after each step,
  and "Choose X from the Y menu".
- British spelling, except the Mac's own words, which are quoted
  literally.
- Describe only the Plus world (System 6.0.7, floppy and SCSI disks,
  ImageWriter). Nothing about modern Macs or BlueSCSI.
- Every fact is checked against the code; anything unchecked is marked
  CHECK.
- The owner approves the style guide, outline, sample spread and each
  chapter.

**Printing:** no paper, printer or binding assumption is documented
for the manuals.

## 3. The original MacPaint manual's instructional structure

The original is a 32-page "book of hints" that sends readers to the
Macintosh owner's guide for basic mouse skills. Its layout is Apple's
earlier "A" design: all Helvetica, with a narrow title column, 2 to 4
ruled text columns, a picture beside every instruction, red click and
drag marks, and a growing isometric kitchen on each chapter divider.

| Printed pages | Contents |
|---|---|
| 2 | How to Use This Book |
| 3–8 | **Ch 1 Learning MacPaint**: one guided session: open, screen map, brush squiggle, select, Flip Horizontal, Undo, erase, type in New York 12 Outline, Save, Print |
| 9–26 | **Ch 2 Using MacPaint**: task pages in any order: Lines and Patterns; Text; Paintbrush; Editing Patterns; Using the Entire Page; Shifting the Whole Picture; Filling In Areas; Selecting and Changing an Area; Cutting and Pasting; Four Ways to Erase; Detailed Drawing; Constraining; File Menu |
| 27–32 | **Ch 3 Reference**: Tools Summary, Shortcuts, Other Special Keys |

It has no glossary, index, troubleshooting section or message list.
It never mentions the Scrapbook, disk space, the work files or any
alert. It leaves several commands unexplained: Save As, Revert, Quit,
Invert, Fill, Trace Edges, Flip Vertical, Rotate, and Goodies ›
Introduction and Short Cuts.

**Terminology** (use the manual's terms, but the program's menu
labels win):
- palettes: tool palette, border palette (line and border widths),
  patterns, current pattern;
- the drawing window, insertion point;
- tools: lasso, selection rectangle, grabber, text tool, paint can,
  spraypaint, paintbrush, pencil, line tool, eraser;
- shapes: hollow and filled shapes (rectangle, rounded-corner
  rectangle, oval, freehand shape, polygon);
- FatBits, the Clipboard.

The built-in Introduction screen uses shorter labels: selection,
scroll, area fill, spray paint, brush.

## 4. MacPaint 1.5: technical findings and differences from the original manual

**Identity.** The About box reads "MacPaint version 1.5 / written by
Bill Atkinson / Copyright 1985, Apple Computer Inc." **[seen]**

**What 1.5 adds over the original manual**
- **Version 1.0 lacked** Edit › **Fill**, the **10-point** size and the
  **Print Draft / Print Final** split. **[seen: resource dumps of 1.0
  and 1.5]**
- **Version 1.3 (May 1984) added** ⌘ transparent painting, Print Final,
  Fill, 10 point and the Geneva 12 default. (*Macworld* Jul/Aug 1984)
- **Version 1.4 (Sept 1984)** kept the whole picture in memory on a
  512K Mac. (*Macworld* Nov 1984) **[inferred** for 1.5 on a Plus; the
  1.3 source streams the picture through the Paint1/Paint2 work files**]**
- **Version 1.5 (April 1985)** can print on the LaserWriter.
  (*Macworld* Oct 1985) Its menus and alerts are identical to 1.3.
  - Code differences found so far: Copy adds LaserWriter picture
    comments and writes the bitmap in 60-row bands. **[seen]** Other
    differences haven't been searched for.
- **MacPaint 1.5 is not HFS-aware.** It predates HFS.

**Menus** **[seen, MENU 1–7]**
- **Apple:** About MacPaint…, then the desk accessories.
- **File:** New, Open…, Close, Save, Save As…, Revert, Print Draft,
  Print Final, Print Catalog, Quit. **None has a ⌘ key.**
- **Edit:** Undo ⌘Z, Cut ⌘X, Copy ⌘C, Paste ⌘V, Clear, Invert, Fill,
  Trace Edges ⌘E, Flip Horizontal, Flip Vertical, Rotate.
- **Goodies:** Grid, FatBits, Show Page, Edit Pattern, Brush Shape,
  Brush Mirrors, Introduction, Short Cuts.
- **Font:** the installed fonts.
- **FontSize:** 9, 10, 12, 14, 18, 24, 36, 48, 72 point. Sizes the font
  really has are outlined.
- **Style:** Plain ⌘P, Bold ⌘B, Italic ⌘I, Underline ⌘U, Outline ⌘O,
  Shadow ⌘S, Align Left ⌘L, Align Middle ⌘M, Align Right ⌘R.

**Rules a beginner will hit** **[source]**
- Only one document can be open at a time: New and Open are dimmed
  until you Close.
- The page is 576 × 720 pixels (8 × 10 in). The window is fixed at
  416 × 240, with no scroll bars.
- A selection can be no bigger than the window.
- Trace Edges, the Flips and Rotate need a rectangle selection, not a
  lasso.
- A block of text holds at most 20 lines of 80 characters. Extra
  characters are silently ignored.
- The Font, FontSize and Style menus are dimmed while a picture is
  selected.
- **There is no Page Setup and no print dialog.**

**Tools, modifiers and double-clicks** **[source, and cross-checked
against the built-in Short Cuts screen, seen]**
- **Double-clicks:**
  - selection rectangle: selects the window;
  - grabber (hand): Show Page;
  - brush: Brush Shape;
  - pencil: FatBits;
  - eraser: erases the window;
  - a pattern: Edit Pattern.
- **Modifiers:**
  - Option-drag copies;
  - Option-⌘-drag makes multiple copies, with the line width setting
    the spacing;
  - ⌘-drag stretches, and Shift keeps the proportions;
  - Option with lines and borders paints them in the current pattern;
  - Option in FatBits scrolls;
  - ⌘-click with the pencil enters or leaves FatBits;
  - ⌘-< / ⌘-> change the font size; ⌘-Shift-< / ⌘-Shift-> change the
    font;
  - **the ` key undoes; Backspace clears; Enter fixes text.**
- **[unverified]** ⌘ "transparent" (OR-mode) painting with the brush,
  spray paint, lines and shapes.
- **[unverified]** the exact behaviour of ⌘-Shift-< and ⌘-Shift-> on
  the Plus keyboard.

**Files and disks** **[source]**
- Open lists only MacPaint (PNTG) documents.
- The palette patterns are saved in each document.
- MacPaint works through **Paint1** and **Paint2** temporary files on
  the disk it was started from. **[unverified]** whether under HFS that
  is the application's folder.
- After a crash, those files reopen as a window titled "rescue".
- MacPaint quits if that disk has under 16 KB free, and it checks this
  continually while you work.
- Save checks there's enough room first. Saving over a file replaces
  it in place.
- Printing from the Finder gives Final quality.

**Messages:** 15 alerts with their exact texts, and when each appears
(`research/resources-1.5.txt` gives the texts; the timing comes from
the source).

**Hazard to warn about** **[source + seen in the binary]:** holding ⌘
while choosing Quit ejects the disk and **restarts the Mac**.

**The Clipboard problem: what is established**
- With MacPaint on a different volume from the active System Folder,
  Copy and Cut show "MacPaint is having trouble writing the scrap".
  - Confirmed at the level of MacPaint's file calls in Mini vMac
    (`docs/PLAN.md` §7).
  - Your hand test in Mini vMac didn't reproduce it, under MultiFinder,
    so the conditions aren't fully understood. **[unverified on your
    Mac Plus]**
- **"The selected pixels disappear after Copy" now has a likely
  explanation.**
  - The Edit menu doesn't drop the selection before showing the alert.
  - When the alert closes, MacPaint's activate handler restores its
    working image and blanks the still-selected area, the same step
    Cut uses.
  - The pixels vanish at the next redraw. An immediate Undo should
    bring them back.
  - The failed Copy has also emptied the Clipboard.
  - **[source + binary-confirmed code path; unverified in use]**
- **The message names the "scrap", not the Scrapbook.** The Scrapbook
  itself isn't involved: it worked in the probe once the Clipboard was
  on disk.
- MacPaint 1.6 (the patch) fixes the volume problem in tests, so the
  alert, and with it the pixel loss, should no longer occur. It is
  **not yet verified on the Mac Plus**, so the manual must not yet say
  it is fixed.

## 5. Proposed manual structure

This follows the MacLife family (Learning, then Using, then Reference,
then Appendixes) with your outline's topics placed in it. Your
eight-chapter outline would break the house pattern, so I've mapped it
instead. **Page count:** an estimate of 70–90 pp at 7½ × 9 in
[inferred].

- **Front matter:** Cover; copyright and edition page; Title page;
  Contents; *About This Manual* (what you need, what you should know,
  how to use this manual, conventions).
- **Chapter 1, Learning MacPaint:** numbered lessons forming one
  session that grows:
  1. Starting MacPaint and the screen (window, tools, line widths,
     patterns).
  2. A first drawing: brush, shapes, Undo.
  3. Selecting and changing: Flip, Copy and Paste within the picture.
  4. Words in pictures: the Text tool, Font, FontSize, Style.
  5. Saving, closing and printing.

  It ends with "What Now?".
- **Chapter 2, Using MacPaint:** task pages ("To …"):
  - drawing and painting (each tool, line widths, patterns,
    constraining with Shift);
  - erasing (four ways);
  - filling areas and leaks;
  - selecting, moving, copying, stretching and multiple copies;
  - Invert, Fill, Trace Edges, the Flips, Rotate;
  - Cut, Copy, Paste and Clear, the **Clipboard vs the Scrapbook**,
    pasting text;
  - FatBits and detailed work;
  - Show Page and moving the whole picture;
  - Grid;
  - editing patterns, brush shapes, Brush Mirrors;
  - text techniques;
  - working with documents (New, Open, Save, Save As, Revert, Close,
    Quit) and disks;
  - printing (Draft, Final, Catalog, from the Finder);
  - a few short projects. (Your Chapter 8: a geometric picture, a
    shaded object, a poster, a composed picture. These could instead
    become a final "Projects" part of Chapter 1; see D6.)
- **Chapter 3, Reference:**
  - the screen;
  - each tool, with its double-click and modifier keys;
  - each menu and command;
  - the built-in Introduction and Short Cuts screens.
- **Appendixes:**
  - A, Messages: all 15 alerts, what each means and what to do.
  - B, MacPaint and Your Disks: work files, rescue, disk space, which
    disk to keep MacPaint on.
  - C, Keyboard Shortcuts.
  - D, Troubleshooting:
    - saving and disk-full problems;
    - Clipboard failures, written to the final build;
    - paint leaking;
    - a selection that won't Rotate;
    - the ⌘-Quit restart;
    - normal behaviour versus failures.
- **Back matter:** Glossary, Index, and the comment page (as in the
  family).

## 6. Illustration approach

- **Screens:** exact 1-bit screens, as in MacMusic. The most reliable
  route is in Mini vMac: **⌘-Shift-3 saves the whole screen as a
  MacPaint document ("Screen 0", "Screen 1", …)** on the startup disk.
  I can read those straight off the disk image as exact pixels, with
  no screenshot permissions needed on this Mac.
  - The session is driven by you from a shot list, as you did for
    MacMusic, and the emulator time is agreed in advance.
  - Open menus can't be captured this way; they would be drawn
    exactly from the MENU resources in the Chicago font, and labelled
    as drawings (as the brief requires).
- **The built-in help screens** (Introduction, Short Cuts) already
  exist as real pictures from the binary.
- **Example artwork** (strokes, patterns, before and after) would be
  drawn in MacPaint itself during the same sessions, so it is genuine
  MacPaint output.

## 7. Recommended source and build workflow

- **Copy the MacTrack manual toolset** (the newest refinements) into
  `tools/manual/`, renamed for MacPaint. That means `book.py`,
  `make-book.py`, chapter generators, `make-figures.py`,
  `callouts.py`, `make-cover.py`, `build-pdf.sh` and `print-pdf.py`.
- **Copy its CSS and style guide** into `docs/manual/`, with an
  addendum for MacPaint's differences.
- **Font:** build "MacPaint Garamond 100" with `condense-font.py`.
- **Shared tools:** keep using `manual-tools/` (Chrome, Paged.js,
  fonts) unchanged.
- **Output:** to `build-manual/`, kept separate from sources.
- **Release:** checksums in `SHA256SUMS`, plus a README with the build
  steps.

This is the same pipeline as the approved manuals, so no new tools
are needed. **If A5 is chosen** (D1), only the page, grid and type
sizes change; the pipeline stays the same.

## 8. Proposed file structure

```
MacPaintClipboardFix/
  docs/manual/
    STAGE0-REPORT.md        this report
    STATUS.md               stage, decisions, questions, results, next steps
    research/               evidence (resource dump, disassembly, help screens, scripts)
    style-guide.md          (Stage 1) house style plus MacPaint addendum
    outline.md              (Stage 1) detailed contents
    figures.md              (Stage 1) illustration register / shot list
    fact-check.md           (Stage 3) every claim → evidence
    manual.css, chapters…   (Stage 2+)
    figures/                (Stage 4) screen sources and PNGs
  tools/manual/             (Stage 2) build scripts
  build-manual/             generated PDFs only
```

## 9. Decisions that need your approval

- **D1. Page size.** Your brief says A5, but every existing manual is
  7½ × 9 in, and A5 appears only in MacMoney's specification.
  - **7½ × 9 in** matches the family exactly, with no redesign.
  - **A5** means re-deriving the grid. The text block shrinks from
    158 to about 120 mm, so type and figure scale must drop. It would
    also set the size for MacMoney and later manuals.
  - **Recommendation:** 7½ × 9, unless A5 is meant to become the
    suite standard. If it is, say so, and I'll propose an A5 grid in
    the Stage 2 prototype for your approval.
- **D2. Version documented.**
  - **Recommendation:** the manual documents **MacPaint 1.6**, the
    build you'll ship, provided your Mac Plus test passes. Until
    then, the Clipboard and troubleshooting text stay marked
    unverified.
  - If you'd rather document **1.5**, the manual must disclose the
    volume problem as a known limitation: keep MacPaint on the
    startup disk.
- **D3. Edition and identity.** MacPaint is Apple's program, and the
  1.3 source licence is non-commercial, with patched builds not to be
  redistributed. The family's plain edition says "© Jack McAteer …
  independent project".
  - **Recommendation:** **own-use only**, like MacMusic Utilities.
  - Wording: the manual text "© 2026 Jack McAteer", with "MacPaint ©
    Apple" credited and nothing claiming the program as your own.
  - Cover: the MacDraw-derived own-use cover.
- **D4. Where the manual lives.** `MacPaintClipboardFix/docs/manual/`
  is used for now. Would you like the folder renamed (e.g. "MacPaint")
  now that it holds both the patch and the manual? I won't rename it
  without your OK.
- **D5. Printing.** Which printer, paper and binding will you use
  (e.g. A4 sheets trimmed, wire-O)? Nothing is recorded, and this
  affects margins and whether a binding allowance is needed.
- **D6. Structure.** Do you agree to use the family's three chapters
  plus appendixes, with your eight topics mapped into them (as in §5),
  instead of eight chapters?
- **D7. Screenshots.** Do you agree to the ⌘-Shift-3 route, with you
  driving Mini vMac from a shot list in agreed sessions?

## 10. Open questions (technical and historical)

1. The Clipboard failure didn't reproduce in your Mini vMac session
   under MultiFinder. What on your Mac Plus differs?
   - This can be pinned down after your hardware test, if you want.
   - The probe shows that both copies of MacPaint fail when launched
     with a different default volume.
2. Your hardware test of the failed-Copy pixel loss: does Undo restore
   the pixels?
3. On a Plus, does 1.5 keep the whole picture in memory (the 1.4
   change), or stream it through Paint1 and Paint2? Where are those
   files under HFS?
4. ⌘ transparent painting, spray behaviour, the Rotate direction and
   ⌘-Shift font changes: all to check during the screenshot sessions.
5. Your actual font list in System 6.0.7, for the Font menu figure.
6. Your printer (ImageWriter or LaserWriter), for the printing section.
7. Any 1.4/1.5 changes beyond those found: no changelog exists. This
   only matters if a behaviour differs from the 1.3 source.

## 11. First prototype proposed (Stage 2, after your decisions)

Six pages at the chosen size:
- the own-use cover;
- the title page;
- the contents page;
- the Chapter 1 opener spread;
- Lesson 1, "The MacPaint screen", with a real annotated screen;
- a Reference page for the Edit menu;
- a "To make multiple copies" task page.

All with real text and real 1-bit screens from a short screenshot
session.
