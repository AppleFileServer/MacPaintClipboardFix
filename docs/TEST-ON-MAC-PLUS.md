# Testing on the Mac Plus

Run each test with **both** applications and note the result in the
two columns:

- **MacPaint**: the original, unchanged (`Graphics:MacPaint`)
- **MacPaint 1.6**: the patched copy

Expected results are for **1.6**. The original should fail wherever
MacPaint isn't on the startup volume.

## Install

1. Copy `MacPaint 1.6` onto the Mac. Use whichever suits you:
   - `build/MacPaint 1.6.dsk`, an 800 KB floppy image;
   - `build/MacPaint 1.6.bin`, MacBinary.
2. Put it in `Graphics` on the Applications volume, next to the
   original. Don't replace or rename the original.
3. Check: **About MacPaint…** in 1.6 says "MacPaint version 1.6".

Both copies have the same creator (`MPNT`), so double-clicking a
MacPaint document may open either one. Start the application you
want first, then use **Open…** from inside it.

Close the Scrapbook and quit other applications between tests.

## A. MacPaint on the Applications volume (System on its usual volume)

| # | Test | Expected (1.6) | MacPaint | 1.6 |
|---|---|---|---|---|
| A1 | Select a rectangle, **Copy**. | No alert | | |
| A2 | **Cut** a lasso selection. | No alert | | |
| A3 | **Paste** in MacPaint after A1. | The copied picture | | |
| A4 | Copy, open the **Scrapbook**, **Paste** into it. | The picture appears in the Scrapbook | | |
| A5 | In the Scrapbook, scroll to another picture, **Copy**, close the Scrapbook, **Paste** in MacPaint. | *That* Scrapbook picture, not the earlier one | | |
| A6 | Repeat A5 with a different Scrapbook picture. | The new picture each time | | |
| A7 | Copy text in MacWrite (or the Note Pad), **Paste** in MacPaint. | The text, as a picture | | |
| A8 | Copy in MacPaint, **Quit**, open MacWrite, **Paste**. | The picture appears in MacWrite | | |
| A9 | Copy a picture in MacDraw or SuperPaint, **Paste** in MacPaint. | The picture | | |

## B. Under MultiFinder

Start up with MultiFinder, and keep MacPaint and the Scrapbook or
another application open together.

| # | Test | Expected (1.6) | MacPaint | 1.6 |
|---|---|---|---|---|
| B1 | A1, A3 and A5 again | As above | | |
| B2 | Copy in another open application, click into MacPaint, **Paste**. | What you just copied, not something older | | |
| B3 | Copy in MacPaint, click into MacWrite, **Paste**. | The picture | | |

## C. Other places

| # | Test | Expected (1.6) | MacPaint | 1.6 |
|---|---|---|---|---|
| C1 | MacPaint copied onto the System volume (any folder): A1, A3, A5 | Works (the original should work here too) | | |
| C2 | MacPaint on a third volume or a floppy: A1, A3, A5 | Works | | |
| C3 | If you can start up from a different System volume: A1, A3, A5 | Works | | |

## If something goes wrong

Write down the test number, the exact alert text, and what was pasted
instead. If a Scrapbook paste in **B** gives an *older* picture, that's
the case the second fix (PLAN §4) is for.

Undo isn't needed: the original is untouched. Drag `MacPaint 1.6`
to the Trash.

## D. The other 1.6 improvements (21 October 2026)

| # | Test | Expected in 1.6 | Original 1.5 does | 1.6 |
|---|---|---|---|---|
| D1 | With a document open, press ⌘W. | Closes it (asks to save if changed) | Nothing | Passed in Mini vMac, 21 Oct |
| D2 | With no document open, press ⌘N. | New untitled document | Nothing | Passed in Mini vMac, 21 Oct |
| D3 | Press ⌘Q. | Quits (asks to save if changed) | Nothing | Passed in Mini vMac, 21 Oct |
| D4 | Choose Quit while holding ⌘. | Quits normally to the Finder | **Ejects the disk and restarts the Mac.** Only try this in Mini vMac, or on the Plus with nothing else open. | Passed in Mini vMac, 21 Oct |
| D5 | Startup disk **full** (in Mini vMac: `tools/run-interactive.sh --full-startup-disk`). Select a large area of a busy picture (rectangle), **Copy**. | **One** "trouble writing the scrap" alert. The picture is unchanged; the selection is gone but its pixels stay put. | Possibly several alerts; the selected pixels vanish when you click elsewhere | Passed in Mini vMac, 21 Oct (full startup disk) |
| D6 | Same as D5 with a **lasso** selection. | As D5 | As D5 | Passed in Mini vMac, 21 Oct (full startup disk) |
| D7 | Same as D5 with **Cut**. | One alert; nothing is cut | The selection is cut and nothing reaches the Clipboard | Passed in Mini vMac, 21 Oct (full startup disk) |
| D8 | After D5, choose Paste. | Nothing is pasted (the Clipboard is empty), or the alert "trouble reading the scrap" | Unpredictable | Passed in Mini vMac, 21 Oct (full startup disk) |
| D9 | Under MultiFinder: select something, click into another program's window, then click back into MacPaint. | The selection and its pixels are unchanged | Unknown: possibly the pixels vanish (see PLAN §10) | Passed in Mini vMac, 21 Oct (both versions) |
