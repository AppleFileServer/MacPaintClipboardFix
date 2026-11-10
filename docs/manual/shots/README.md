# Screenshots

`2026-10-21-host/`: session 1, Jack driving, 21 October 2026. Thirty
macOS screenshots (⌘-Shift-3 on the host, saved to Jack's Desktop,
which still holds the originals) converted to exact 512 × 342 Mac
screens by `tools/grab-host-screens.py`. The log is
`grab-2026-10-21.log`.

**How exact:** Mini vMac draws each Mac pixel as a 4 × 4 block of pure
black or white, and the tool rejects a shot unless every block is
uniform. Two exceptions:
- the outer edge, read from each block's inner pixels;
- the bottom corners, rounded off by macOS (and, bottom right, shaded
  by the floating screenshot thumbnail). There, 54–84 pixels per shot
  are filled from the grey desk checkerboard around them.

The Mac's own ⌘-Shift-3 didn't work: macOS takes the keys first.

| Time | Shows | Use |
|---|---|---|
| 13.28.22 | Just started: untitled, paintbrush chosen | **S01** |
| 13.30.59 | House and tree, untitled | **E01** (first version) |
| 13.31.12 | Save dialog, "Save document as: Test" | **S07** |
| 13.31.15 | Replace existing "Test"? | App. A / S07 |
| 13.31.20 | House and tree, titled Test | E01 / openers |
| 13.31.32 | Show Page, picture at the top | **S05** |
| 13.31.49, 13.31.55 | Show Page, dragging the window frame | S05, Ch 2 The Whole Page |
| 13.31.59 | Back from Show Page: the frame moved off the picture | Ch 2 The Whole Page |
| 13.32.10–13.32.22 | Goodies menu, each item highlighted | **M04** |
| 13.32.28 | Font menu (the Mini vMac System disk's fonts) | **M05** |
| 13.32.30 | FontSize menu, outlined sizes | **M06** |
| 13.32.34 | Style menu | **M07** |
| 13.32.38, 13.32.39 | Edit menu: only Undo and Paste enabled | **M03** |
| 13.32.44–13.32.55 | File menu, each item highlighted; New and Open dimmed while a document is open; ⌘N/⌘W/⌘Q | **M02** |

Not yet shot: S06 (the grabber), M01 (Apple menu), and E01 with a sky
and words.

`2026-10-25-claude/`: session 2, Claude driving Mini vMac with
`tools/vmacctl` (clicks and keys) and `tools/vmacshot.sh` (captures the
Mini vMac window, even when covered, and converts it the same way).

| File | Shows | Use |
|---|---|---|
| F01 | The Graphics folder: MacPaint and MacPaint 1.6 icons | **F01** |
| S01 | Just started: untitled, paintbrush chosen | **S01** |
| E01 | House, tree, sun, dotted sky, "Home Sweet Home" | **E01**, openers |
| Graphics_Example 1.page | The saved document's whole 576 × 720 page | E01, D01 |
| S07-empty, S07 | Save dialog, empty and "Example 1" | **S07** |
| S05 | Show Page with Example 1 | **S05** |
| S06 | The grabber after moving the view | **S06** |
| M01 | Apple menu (the emulator System's desk accessories) | M01, to trim or draw |
| M08 | "Save changes before quitting?" | **M08** |
| C1, C3-*, C6-* | Fact checks C1, C3, C6 | `fact-check.md` |
