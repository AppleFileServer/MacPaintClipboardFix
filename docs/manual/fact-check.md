# MacPaint User's Guide: fact-check plan and register

Stage 1, 21 October 2026. Every instruction in the book must trace to
evidence. In Stage 3 each manuscript paragraph that states a fact gets
an entry, or a reference to one, here.

## Evidence levels

| Level | Meaning | May the book state it as fact? |
|---|---|---|
| **O** | Observed: seen in MacPaint 1.6 (or 1.5 where unchanged) in Mini vMac or on the Mac Plus | Yes |
| **B** | Binary: read from the 1.5/1.6 resources or code (menus, alert text, patched behaviour) | Yes, for text and structure. Behaviour should also be O |
| **S** | Source: the 1.3 source, which matches 1.5 at every place compared, but not everywhere | Only once O confirms it, or for detail too fine to test, marked as such in this register |
| **D** | Documented: the original manual, *Macworld*, Apple technotes | Only with O or S agreeing |
| **CHECK** | Not yet established | No. It stays out of the book, or is marked CHECK in drafts |

## Already established

| Fact | Level | Evidence |
|---|---|---|
| Menu titles, items and Command keys, incl. 1.6's ⌘N/⌘W/⌘Q | B, O | `research/resources-1.5.txt`; patch §10; Jack's test D1–D3 |
| All alert and dialog texts | B | `research/resources-1.5.txt` |
| Help screens (Introduction, Short Cuts) | B | PICT 2400/2401 |
| Page 576 × 720, window 416 × 240, no scroll bars | S, B | source; window resource rect |
| Clipboard works with MacPaint on any volume (1.6) | O (Mini vMac) | PLAN §7, §9; **Mac Plus test pending** |
| ⌘ held at Quit just quits (1.6) | O | test D4 |
| A failed Copy/Cut gives one alert and keeps the picture (1.6) | O | tests D5–D8 |
| MultiFinder switching keeps selections | O | PLAN §11 step 1 |
| Double-click actions (selection rectangle, grabber, brush, pencil, eraser, pattern) | S, B (Short Cuts screen) | ChooseTool; PICT 2401 |
| ⌘ held while painting adds only black dots (brush tested: a grey stroke over black leaves the black solid) | O | C1; `shots/2026-10-25-claude/C1.png` |
| Rotate turns the selection 90° anticlockwise | O | C3; `C3-before.png`, `C3-after.png` |
| The \` key undoes; Backspace clears the selection | O | C6; `C6-undo.png`, `C6-clear.png` |
| MacPaint has no ⌘S for Save: ⌘S is Shadow in the Style menu | B, O | menus; seen 25 Oct |
| Close (⌘W) of an unchanged document asks nothing; Quit with changes asks "Save changes before quitting?" (Yes, No, Cancel) | O | 25 Oct; `M08.png` |

## To establish (CHECK)

Planned for the screenshot sessions: each test is a few seconds while
the relevant shot is being taken.

| # | Question | Source says | Test |
|---|---|---|---|
| C1 | **Done 25 Oct, see above.** ⌘ held while painting (brush, spraypaint, paint can, lines, shapes) paints "transparently": only black dots are added | S | Paint a pattern over a shape with and without ⌘ |
| C2 | Spraypaint adds nothing while the mouse is held still | S | Hold still |
| C3 | **Done 25 Oct, see above.** Rotate direction (90° anticlockwise?) | S (geometry) | Rotate an "L" shape |
| C4 | Shift with Trace Edges gives a shadow | S, MP | Try it |
| C5 | ⌘-< / ⌘-> change the size; ⌘-Shift-< / ⌘-Shift-> change the font, on the Plus keyboard | S, H02 | Try while typing |
| C6 | **Done 25 Oct, see above.** The \` key undoes; Backspace clears | S, H02 | Try |
| C7 | Enter ends a block of text and starts a new one at the insertion point | S | Type, press Enter, type |
| C8 | Text stops at 20 lines / 80 characters, silently | S | Type a long line |
| C9 | Paste into a selection scales the picture to fit | S | Select an area, Paste |
| C10 | A pasted lasso selection comes back transparent, with the lasso chosen | S | Lasso-copy, Paste |
| C11 | Where Paint1 and Paint2 are made under HFS (MacPaint's folder?) | S | Look in the Finder while MacPaint runs (MultiFinder) |
| C12 | MacPaint quits when its disk has under 16K free, including while you work | S | Full PaintVol test |
| C13 | The "rescue" window after a crash | S | Restart Mini vMac while MacPaint runs, then start MacPaint without a document |
| C14 | Print Catalog lists only pictures at the top level of a disk | S | Pictures in a folder, then Print Catalog (with Jack's printer) |
| C15 | Printing from the Finder prints Final; holding ⌘-S gives Draft | MP, S | Needs a printer (printer question: STATUS.md) |
| C16 | Option with a tool other than the pencil does nothing special outside FatBits | S | Try |
| C17 | A second click right after a paint-can fill is ignored | S | Try |
| C18 | Saving over an existing document replaces it in place (risk if the disk fills) | S | Describe the advice only; no test needed |
| C19 | The Font menu lists Jack's fonts | runtime | Shot M05 from Jack's System |
| C20 | Clipboard behaviour on the real Mac Plus (1.6 and 1.5) | — | Jack's hardware test (`docs/TEST-ON-MAC-PLUS.md`) |
