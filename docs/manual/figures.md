# MacPaint User's Guide: illustration register and shot list

Stage 1, 21 October 2026. Every figure the book needs, with a stable
code. The book prints no figure numbers; the codes live only here.
Scales and treatment follow `style-guide.md` §5.

## Kinds of figure

| Code | Kind | How it is made |
|---|---|---|
| S | Screen | Shot in Mini vMac with ⌘-Shift-3. System 6 saves the whole screen as a MacPaint document ("Screen 0", "Screen 1", …) on the startup disk. Stage 2 adds a tool that reads these off the disk image as exact 1-bit pixels |
| M | Menu or dialog that can't be shot (open menus) | Drawn pixel for pixel from MacPaint's resources (MENU 1–7, DLOG/DITL, ALRT) in the Chicago font; labelled "drawn" |
| H | MacPaint's own help screens | PICT 2400 and 2401 from the program (`research/help-*.png`) |
| E | Example artwork | Painted in MacPaint during the sessions, then shot or saved as a document |
| D | Diagram | Drawn for the book: line art, 1-bit |
| F | Finder screen | Shot in Mini vMac with ⌘-Shift-3 |

**Status values:** planned, shot, drawn, done (processed and checked).

## Register

| Code | What | Kind | Used in | Status |
|---|---|---|---|---|
| S01 | The whole screen just after starting: untitled window, paintbrush chosen | S | Lesson 2; Lesson 3 (labelled); Ref. The Screen | shot (13.28.22; again 25 Oct) |
| S02 | The window with a paintbrush stroke in a pattern | S (W) | Lesson 4 | planned |
| S03 | Shapes drawn, the filled-oval tool chosen | S (W) | Lesson 5 | planned |
| S04 | A selection with its dotted outline, being dragged | S (W) | Lesson 7 | planned |
| S05 | Show Page view, with the dotted rectangle | S (F) | Lesson 10; Ch 2 The Whole Page | shot (25 Oct with Example 1; also 13.31.32; 13.31.49 and 13.31.55 while dragging the frame) |
| S06 | The grabber moving the picture | S (W) | Lesson 10 | shot (25 Oct) |
| S07 | The Save dialog, "Save document as:" | S (D) | Lesson 11 | shot (25 Oct, empty and "Example 1"; also 13.31.12; 13.31.15 with "Replace existing" alert) |
| S08 | The Brush Shape dialog | S (D) | Ch 2 Painting | planned |
| S09 | The Brush Mirrors dialog | S (D) | Ch 2 Painting | planned |
| S10 | The Edit Pattern dialog | S (D) | Ch 2 Patterns | planned |
| S11 | FatBits, with the actual-size view | S (W) | Ch 2 Detailed Work | planned |
| S12 | Text being typed (insertion point) | S (W) | Lesson 9; Ch 2 Text | planned |
| S13 | The Scrapbook with a MacPaint picture | S (W) | Ch 2 Cut, Copy and Paste | planned |
| S14 | The Open dialog | S (D) | Ch 2 Documents | planned |
| S15 | The "rescue" window title | S (part) | Ch 2 Documents; App. B | planned (needs a deliberate crash; may be drawn instead) |
| S16 | Print Catalog output | S or a scan of a printout | Ch 2 Printing | planned (printer question: STATUS.md) |
| S17–S20 | Chapter opener screens (MacPaint with a picture) for Ch 1, 2, 3 and Appendixes | S (F) | Openers, light grey | planned |
| M01 | Apple menu (About MacPaint…) | M | Ref. Menus | shot (25 Oct), but it lists the Mini vMac System's desk accessories (Tetris, Wi-Fi…): trim or draw for the book |
| M02 | File menu, with ⌘N, ⌘W, ⌘Q (1.6) | M | Lesson 12; Ref. | shot (13.32.44–13.32.55, one per item highlighted) |
| M03 | Edit menu | M | Lesson 8; Ref.; **prototype** | shot (13.32.38, 13.32.39; Paste enabled, the rest dimmed) |
| M04 | Goodies menu | M | Ref. | shot (13.32.10–13.32.22, one per item highlighted) |
| M05 | Font menu (Jack's installed fonts) | M | Lesson 9; Ref. | shot (13.32.28) from the Mini vMac System disk, not Jack's Mac Plus |
| M06 | FontSize menu, with outlined sizes | M | Lesson 9; Ref. | shot (13.32.30) |
| M07 | Style menu | M | Lesson 9; Ref. | shot (13.32.34) |
| M08 | "Save changes before quitting?" | M or S | Lesson 13; App. A | shot (25 Oct) |
| M09 | All 15 alerts, small | M | App. A | planned |
| H01 | Introduction screen (PICT 2400) | H | Ref.; Lesson 3 | have source |
| H02 | Short Cuts screen (PICT 2401) | H | Ref.; App. C | have source |
| E01 | A finished example picture | E | Ch 1 Introduction | shot (25 Oct): house, tree, sun, dotted sky, "Home Sweet Home"; saved as "Example 1" (page in `shots/2026-10-25-claude/`). Jack's first version: 13.30.59 |
| E02 | Paintbrush strokes in several brush shapes and patterns | E | Lesson 4 | planned |
| E03 | Hollow and filled shapes, with and without borders | E | Lesson 5; Ch 2 | planned |
| E04 | Before and after erasing | E | Lesson 6 | planned |
| E05 | Lasso and rectangle selections compared | E | Lesson 7; Ch 2 Selecting | planned |
| E06 | Flip Horizontal, before and after | E | Lesson 8 | planned |
| E07 | Words in a picture: fonts and styles | E | Lesson 9 | planned |
| E08 | Invert, Fill, Trace Edges and Rotate examples | E | Ch 2 Selecting | planned |
| E09 | Multiple copies (Option-⌘) and stretching (⌘) | E | Ch 2 Selecting | planned |
| E10 | Paint leaking through a gap | E | Ch 2 Painting | planned |
| D01 | The window as a frame on the 8 × 10 page | D | Ch 1 Introduction | planned |
| D02 | The Mac Plus keyboard with MacPaint's special keys | D | App. C | planned (based on H02's layout, redrawn) |
| C01 | Cover screen: MacPaint 1.6 with the **Woodcut** open, as on Apple's 1984 manual (D8). The Woodcut is **rebuilt** from the 1984 cover scan (`tools/manual/rebuild-woodcut.py`), not MacPaint's own pixels; the screen around it is an exact shot. Private: `manual-assets-private/woodcut-screen.png` | S (rebuilt picture) | Cover | shot (25 Oct) |
| F01 | The MacPaint icon in a folder on the hard disk | F | About This Manual; Lesson 1 | shot (25 Oct, Graphics folder on PaintVol) |

## Session 1: shots for the Stage 2 prototype

The prototype is the cover, title page, contents, Chapter 1 opener,
Lesson 3 (the screen), a large-illustration page (Lesson 10) and the
Edit-menu reference page. It needs only these:

| # | Shot | How |
|---|---|---|
| 1 | **S01** | Start MacPaint 1.6. Before touching anything, press ⌘-Shift-3 |
| 2 | **E01 / S17** | Paint a simple picture that fills the window (see note), then ⌘-Shift-3. Save it as "Example 1" too |
| 3 | **S05** | Choose Goodies › Show Page. ⌘-Shift-3 |
| 4 | **S06** | Choose the grabber and drag the picture a little. ⌘-Shift-3 after letting go |

M03 (Edit menu) and H01 come from the resources and need no shot.

**Session 1 result (21 Oct, Jack driving):** 30 macOS screenshots of
Mini vMac, converted to exact 512 × 342 Mac screens by
`tools/grab-host-screens.py` (see `shots/README.md`). macOS screenshots
can show open menus, so menus are now shot rather than drawn. Still to
take: S06 (grabber), and E01 with a sky and some words.

**Session 2 result (25 Oct, Claude driving):** all four session-1 shots
plus F01, S07, M01, M08 and checks C1, C3, C6, in
`shots/2026-10-25-claude/`.

**Note on example art:** the picture should be original and simple,
for example a house with a tree, a patterned sky and a few words. It
appears in several places, so it's worth taking a few minutes over.
Jack chose a house with a tree (21 Oct).

**Session rules** (the shared Mini vMac):
- short;
- a copy of the System disk, with MacPaint 1.6 on its own volume, as
  `tools/run-interactive.sh` does;
- ⌘-Shift-3 can't capture while a menu is open or the mouse button is
  held down.
