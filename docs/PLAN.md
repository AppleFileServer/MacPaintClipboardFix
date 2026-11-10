# Plan: MacPaint clipboard on a separate volume

Drafted 19 October 2026. Planning only: nothing has been patched or
built yet.

## 0. Goal (agreed with Jack, 19 October 2026)

MacPaint can be on **any volume**, and the active System Folder can be
on **any volume**. In MacPaint, Cut, Copy and Paste, both to and from
the clipboard and the **Scrapbook** desk accessory, must always work
correctly.

Approach agreed: patch a **copy** of MacPaint 1.5 (Option A below) and
keep the unpatched original alongside it.

## 1. The problem in one paragraph

MacPaint doesn't go through the Scrap Manager to move pictures. It
asks the Scrap Manager for the clipboard file's **name**
("Clipboard File"), then opens that file itself with File Manager
`_Open` on **drive 0, the default volume**. When an application is
launched, the default volume is the application's own folder. If
MacPaint shares a volume with the System Folder, HFS's search path
quietly falls back to that volume's blessed System Folder, finds the
real Clipboard File, and everything works. On a volume of its own
there's no Clipboard File, or only a stale one, so picture Copy and
Paste fail. The Scrap Manager itself always uses the startup volume's
System Folder. Text pasting goes through `GetScrap` normally, so it
should still work.

## 2. Evidence

### In the published 1.3 source (`source/chm-original/.../MacPaint.p`)

| Where | What it does |
|---|---|
| `CutOrCopy`, line 1592 | `OpenFile(0,0,scrapPtr^.scrapName^,Nil,scrapFile)`: drive 0, and the result is **not checked** |
| `CutOrCopy`, line 1658 | `FlushVol(0)`: flushes the wrong volume too |
| `Paste`, line 1791 | `OpenFile(0,0,scrapPtr^.scrapName^,Nil,scrapFile)`: drive 0, failure shows "trouble reading the scrap" |
| `PaintAsm.a`, `OpenFile` (about line 2592) | Puts `drive` straight into `ioVRefNum` (`IODrvNum`) and calls `_Open`, with no directory ID |

Because the open result isn't checked in `CutOrCopy`, a failed open
leaves `scrapFile` holding whatever was in the parameter block. The
writes and the `CloseFile` that follow then act on an unknown file
reference number. This is probably harmless, since the first write
usually fails and raises an alert, but it isn't guaranteed. Until
this is fixed, **avoid Copy/Cut in MacPaint when it's on its own
volume**.

### In the MacPaint 1.5 actually in use (`originals/MacPaint-1.5.rsrc`)

The About box reads "MacPaint version 1.5 … Copyright 1985". The
compiled code matches the 1.3 source byte for byte at both sites:

| Resource | Offset | Bytes | Meaning |
|---|---|---|---|
| `CODE` 4 (SegScrap, Copy/Cut) | `0xA8` | `4267 4267 4267 2F2C 000C 42A7 486D FF74 4EAD 01BA` | push result, **drive 0**, version 0, name ptr, Nil buffer, `@scrapFile`; JSR `OpenFile` |
| `CODE` 5 (SegPaste) | `0x19C` | `4267 4267 4267 2F2B 000C 42A7 486D FF74 4EAD 01BA` | the same call in Paste |

(Offsets are into the `CODE` resource data, header included, as the
scripts in `tools/` report them.) So 1.5 still has the bug, and the
1.3 source is a faithful guide to the code being patched.

### Prior art

Paul C. Pratt's 2014 rebuild (`source/gryphel-1.3-gry2/`) fixed this
same bug ("an incompatibility with HFS in clipboard operations"). He
added a `GetSysVol` routine that reads the System file's volume from
`SysMap` → FCB → VCB, and passed it to both `OpenFile` calls instead
of 0. That confirms the diagnosis. His fix is 1.3 only and leaves
`FlushVol(0)` unchanged.

## 3. Options

| | Option | Gains | Costs |
|---|---|---|---|
| **A (recommended)** | **Binary-patch a copy of MacPaint 1.5**: two 6-byte edits so both `OpenFile` calls use the startup volume | Keeps 1.5 and everything else unchanged; tiny, reversible and easy to verify | Fixes only the volume. Anything wider needs spare space in a CODE segment |
| B | Use Gryphel's prebuilt 1.3-gry2 as is | Ready today | It's 1.3: loses the 1.4/1.5 changes, and its About box differs |
| C | Rebuild from source with a fuller fix | Can also check errors, flush the right volume and handle in-memory scrap | Needs MPW Pascal and Asm. The suite toolchain is Retro68 (C only), so this means setting up MPW under emulation. Also produces 1.3, not 1.5 |

The source is still essential for A: it's the map that shows exactly
which bytes to change and why.

## 4. The patch (Option A)

At each site, replace the first two of the three pushes:

```
was:  4267        CLR.W   -(SP)         ; result
      4267        CLR.W   -(SP)         ; drive = 0  (default volume)
      4267        CLR.W   -(SP)         ; version = 0
now:  2F38 020E   MOVE.L  $020E,-(SP)   ; result = junk, drive = BootDrive ($0210)
      4267        CLR.W   -(SP)         ; version = 0
```

`MOVE.L $020E` pushes the low word of `Time` (`$020E`) into the
result slot, which `OpenFile` overwrites anyway, and pushes
`BootDrive` (`$0210`) as the drive. It's the same length and leaves
the stack layout unchanged. `BootDrive` holds the working directory
of the startup System Folder, which is where the Scrap Manager keeps
Clipboard File. Because the System sets it at startup to wherever the
active System Folder is, the patch doesn't depend on either volume.
MacPaint can be anywhere, and so can the System Folder. A stale
Clipboard File on MacPaint's own volume is ignored as well.

**To confirm first (step 1 below):** that the System 6.0.7 Scrap
Manager on the Plus really does open Clipboard File via `BootDrive`.
If it doesn't, use Gryphel's approach instead (the System file's
volume from `SysMap`). That needs about 30 bytes of new code: add it
to the end of `CODE` 1 and call it through a new jump-table entry
(more work, still small).

### Second fix for the Scrapbook (on hold: the probe found it unnecessary under the Finder, see §7)

The Scrapbook's Copy (and MultiFinder, when switching applications)
may leave the clipboard **in memory** rather than in Clipboard File.
MacPaint's Paste asks `GetScrap` where the picture is, then reads that
position **from the file**, so it would paste an old picture or
rubbish. Copy is already safe here, because it calls `UnloadScrap`
first.

The fix is for Paste to call `UnloadScrap` (trap `A9FA`) just before
it opens the file. That writes the in-memory clipboard to disk with
the same layout, so the position `GetScrap` gave stays correct. There
are no spare bytes inline for this, so the plan is:

- add a small helper routine (about 20 bytes) to the end of
  `CODE` 5;
- give it a new jump-table entry in `CODE` 0;
- replace the Paste site's `4267 4267 4267` with a 4-byte
  `JSR nn(A5)` to the helper, plus one `CLR.W -(SP)`.

The helper calls `UnloadScrap`, then pushes the result and
`BootDrive` words under its own return address. This change is
slightly larger, so it gets its own before-and-after test. Step 2
checks first whether the Scrapbook really leaves the clipboard in
memory under System 6.0.7. If it doesn't, this fix is skipped.

Optional, if space allows: make `FlushVol(0)` at the end of Copy/Cut
flush the startup volume. Without it, a crash right after a Copy
could leave the startup volume's catalogue stale. It isn't needed
for the clipboard to work.

## 5. Steps

1. **Confirm the Scrap Manager's volume.** Disassemble the scrap code
   in the Plus ROM and System 6.0.7, or run a short Mini vMac test
   (a couple of minutes at most, at a time Jack chooses). Decide
   between `BootDrive` and the `SysMap` volume.
2. **Reproduce the bug in Mini vMac.** Use two disks: a System 6.0.7
   boot disk, and a separate volume holding only a copy of MacPaint
   1.5. Copy should give "MacPaint is having trouble writing the
   scrap", which matches what Jack sees. Note what Paste does, whether
   text Paste works, and whether the Scrapbook leaves the clipboard
   in memory (this decides whether the second fix is needed).
3. **Quick check against prior art.** Put Gryphel's 1.3-gry2 on the
   separate volume. If Copy and Paste work, the diagnosis is proven.
4. **Write the patcher.** Write a small host-side Python script that
   takes a *copy* of MacPaint 1.5, checks the expected bytes at both
   sites (refusing to run if they differ), writes the two edits,
   changes the version shown to 1.6, and outputs a new
   file plus a checksum. Make no edits by hand in ResEdit, so the
   change can be repeated and undone.
5. **Test in Mini vMac** (short runs, one feature at a time; see the
   test list below).
6. **Try it on the Mac Plus**: copy it to the Applications volume
   beside the original, as "MacPaint 1.6". Use it for a while
   before retiring the original. Keep the original in `originals/`
   regardless.

### Test list

- Copy and Cut in MacPaint, then Paste back into MacPaint (rectangle
  selection and lasso)
- MacPaint → MacWrite / Scrapbook, and Scrapbook → MacPaint (picture)
- Text from MacWrite → MacPaint (should already work; must not
  break)
- Quit MacPaint, then paste its picture into another application
  (the clipboard survives the quit)
- Every combination of where MacPaint and the active System Folder
  live:
  - MacPaint and the System Folder on the same volume (in the System
    Folder, and in another folder)
  - MacPaint on another volume
  - the System Folder on a different volume from usual (start up from
    another disk)
  - a stale Clipboard File left on MacPaint's volume
- Under the Finder alone and under MultiFinder
- Startup volume nearly full, or locked: the alerts appear and
  nothing crashes
- Scrapbook → MacPaint pastes the *current* Scrapbook item, not an
  older one, including right after a text copy elsewhere (this tests
  the second fix)
- Scrapbook: paste a MacPaint picture in, scroll away and back, then
  copy it out again

## 6. Answers from Jack (19 October 2026)

1. "Sketchpad" means the **Scrapbook** desk accessory.
2. Symptom: MacPaint **can't write to the clipboard** (the Copy/Cut
   failure in section 2).
3. Option A is approved: patch a copy of 1.5 and keep the original.
4. The Plus starts up from a System 6 volume, but the fix must not
   depend on that. MacPaint and the active System Folder can each be
   on any volume (section 0).

No open questions remain.

## 7. Results: probe run, 19 October 2026 (steps 1 and 2)

The probe (`probe/probe.c`) ran in a private copy of Mini vMac
(`tools/run-probe.sh`; Mini vMac ran for about 2 seconds) with two
disks:

- **SysDisk:** System 6.0.7, with a blessed System Folder.
- **PaintVol:** stands in for MacPaint's own volume.

It repeated MacPaint 1.5's file calls exactly, with the default
directory set as the Finder would set it for MacPaint. The full log
is `runs/20261019-083619/ProbeLog.txt`, and every check passed.

| Question | Answer |
|---|---|
| Where does the Scrap Manager keep Clipboard File? | In the **startup System Folder** (`BootDrive`), wherever the application's default directory is. Nothing goes onto MacPaint's volume. |
| Does `BootDrive` point at the active System Folder? | Yes (BootDrive −32733 = SysDisk:System Folder). |
| MacPaint as shipped, on its own volume | `_Open` fails with −43 (file not found) and leaves the reference number as **0**. Every write then fails, so you get "MacPaint is having trouble writing the scrap". **This is exactly Jack's symptom.** |
| MacPaint as shipped, same volume as the System (any folder) | It works: HFS's search path finds the System Folder's Clipboard File. |
| A stale Clipboard File on MacPaint's volume | The shipped MacPaint **silently opens the wrong file** there, so other programs never see its pictures. |
| `BootDrive` fix, MacPaint on its own volume | It opens SysDisk:System Folder:Clipboard File, even with a stale file present. |
| Gryphel's `SysMap` fix | It also works here (through the HFS search path). `BootDrive` is the more direct choice and fits in place, so **`BootDrive` is chosen**. |
| A picture written by the patched Copy | Read back correctly through the Scrap Manager, so other programs and the Scrapbook will see it. |
| Do the Scrapbook's calls leave the clipboard in memory? | **No**, not while MacPaint is running: MacPaint unloads the clipboard at startup, and once it's on disk, `ZeroScrap`/`PutScrap` write straight to the file (scrapState stays 0). The `BootDrive` fix alone pastes the current Scrapbook item. |

Two corrections to the earlier sections:

- **"Error −49" is normal.** The Scrap Manager keeps Clipboard File
  open, so MacPaint's `_Open` returns −49 ("already open for
  writing") along with the existing reference number. MacPaint's
  Paste code already accepts −49 for this reason.
- **The "unknown reference number" risk doesn't arise.** A failed
  open leaves 0, which can't touch another file. Copy/Cut in the
  shipped MacPaint is safe, just useless off the System volume.

### What this means for the plan

- The **first fix (`BootDrive`, two 6-byte edits) is enough** under
  the Finder.
- The **second fix (`UnloadScrap` before Paste) is on hold.** It's
  needed only if a real test shows something reloading the clipboard
  into memory while MacPaint runs. MultiFinder is the one candidate
  left untested (the probe boots without it).
- Step 3 (trying Gryphel's build) is no longer needed: the probe
  showed both candidate fixes working directly.

## Naming

The patched MacPaint is **MacPaint 1.6** (Jack, 19 October 2026).
It was called "MacPaint 1.5 CF" before that.

## 8. Patcher (step 4), 19 October 2026

`tools/patch-macpaint.py` (run with `../transfer-tools/venv/bin/python -I`)
writes `build/MacPaint 1.6.{rsrc,bin,dsk}` and `build/SHA256SUMS`.

It runs only on the exact MacPaint 1.5 in `originals/` (checked by
checksum), checks every byte before changing it, and confirms the
clipboard `OpenFile` call occurs only at the two known sites. It
changes 10 bytes in place:

- the two `BootDrive` edits;
- the version, 1.5 → 1.6, in the About box (`DITL` 2006) and in the
  signature resource the Finder's Get Info shows (`MPNT` 0).

`--reverse` undoes the patch, giving a file byte-identical to the
original (checked). A disassembly of both patched sites shows
`move.l $020E,-(sp)` then `clr.w -(sp)` before `jsr OpenFile`, as
intended.

## 9. Testing on the Mac Plus (steps 5 and 6)

Jack is testing both the original and the patched copy on the real Mac
Plus (his choice, 19 October 2026), using `docs/TEST-ON-MAC-PLUS.md`.
Record the results here when they come back.

**Mini vMac by hand, 19 October 2026** (`tools/run-interactive.sh`).
The System 6.0.7 copy started under MultiFinder, with both MacPaints
on a separate volume, PaintVol. Jack found that **both the patched and
the unpatched MacPaint copy and paste correctly**. That doesn't match
the probe (§7), where the shipped `OpenFile(0)` call failed with −43
from another volume. The difference is unexplained so far. Possible
reasons:

- MultiFinder, or the Finder launching MacPaint, sets the default
  directory differently from the probe;
- MultiFinder patches the scrap or file calls;
- something in Jack's real Mac Plus setup, which is where he sees
  the error.

Jack will test on the real hardware.

**Explanation found for the "selected pixels disappear after Copy"
symptom** (code reading, 19 October 2026; `docs/manual/STAGE0-REPORT.md` §4):

- The Edit menu doesn't drop the selection before Copy shows "trouble
  writing the scrap".
- When the alert closes, the activate handler runs `MainToAlt`, which
  blanks the still-selected area (the same step Cut uses). The pixels
  vanish at the next redraw.
- The failed Copy has also emptied the clipboard (`ZeroScrap` runs
  first).
- An immediate Undo should restore the pixels.
- The patch prevents this only by preventing the failure. Check it on
  the Mac Plus with the unpatched copy.

**For that test:** when Jack asks, put **both** `MacPaint` (original)
and `MacPaint 1.6` on the BlueSCSI **ID 6** image
(`HD60_512 …hda`). First confirm with Jack which ID 6 image, and back
it up before writing.

## 10. Candidate improvements for 1.6 (proposed 21 October 2026, not yet approved)

These came from the manual research (`docs/manual/STAGE0-REPORT.md` §4).
Each would be a further edit in `tools/patch-macpaint.py`, with checks,
tests and the ability to undo it, like the clipboard fix. Kinds of edit:

- **In place:** change a few bytes where they are.
- **Resource:** edit or add a resource; the resource fork is rebuilt.
- **Code cave:** add a small routine to a CODE segment and call it.

| # | Improvement | Why | Kind | Risk |
|---|---|---|---|---|
| I1 | **Stop ⌘-Quit from restarting the Mac.** Holding ⌘ while quitting ejects the disk and jumps into ROM. | A hidden trap that can lose work in other open programs under MultiFinder | In place: make the key test always fail | Low |
| I2 | **Never lose the selection when Copy fails.** Today, closing the "trouble writing the scrap" alert blanks the selected area. | The 1.6 fix makes the failure rare, but a full or locked startup disk can still cause it | Code cave: drop or redraw the selection safely after the alert | Medium |
| I3 | **Don't empty the Clipboard until the new picture is written.** Copy now calls `ZeroScrap` first, so a failed Copy leaves the Clipboard empty. | A failed Copy keeps the old contents | Code cave (reorder the calls) | Medium |
| I4 | **Add ⌘ keys to the File menu** where letters are free: ⌘N New, ⌘W Close, ⌘Q Quit. ⌘O and ⌘S stay Outline and Shadow; changing them would break the Style keys everyone knows. | Faster everyday use | Resource (MENU 2) | Low |
| I5 | **Add a SIZE resource** so MultiFinder gives MacPaint a sensible memory partition. | Today MultiFinder uses its default partition. Needs measuring first | Resource | Low (once measured) |
| I6 | **Safe Save:** write to a temporary file, then swap. Today Save overwrites the old file in place, so a disk filling mid-save could damage the only copy. | Protects existing pictures | Larger code change | High: needs more code space and careful testing |
| I7 | **Print Catalog on HFS:** it counts only the files at the root of the volume. | Catalog is incomplete for pictures in folders | Larger code change | High |
| I8 | **Beep instead of silently ignoring** text past 20 lines or 80 characters, or a pasted text that's too big. | Feedback where there's none now | Code cave | Medium |

Not proposed: new features such as more than one document, selections
bigger than the window, or flipping a lasso selection. Those amount to
a rewrite, not a patch.

### Approved and built for 1.6: I1, I2, I4 (Jack, 21 October 2026)

All three are in `tools/patch-macpaint.py` alongside the clipboard fix.
Every edit checks the bytes it replaces. The resource fork is rebuilt
in its original order, the fork grows from 59,824 to 59,890 bytes, and
`--reverse` gives back the original 1.5 exactly (checked on every
build). Each patched site was disassembled after building.

- **I1:** `CODE 1 +0x52FE`, `BEQ.S` → `BRA.S`. QuitProgram still reads
  the ⌘ key but never calls EjectReset, which is now dead code.
- **I4:** MENU 2 key bytes: New ⌘N, Close ⌘W, Quit ⌘Q. MenuKey does
  the rest: the commands already dim correctly, and ⌘N works only when
  no window is open, just like choosing New.
- **I2:** three routines appended to CODE 4, sharing a flag byte at
  `$0A78` (ApplScratch, unused by MacPaint):
  - **CopyStart** (`+0x334`, called from `+0x98`) clears the flag.
  - **ScrapAlertOnce** (`+0x31C`, called from WScrapError `+0x12`)
    sets the flag and shows "trouble writing the scrap" only once. A
    failure partway through the picture used to repeat the alert for
    every failed piece.
  - **CopyFailGuard** (`+0x302`, called at label 9 `+0x2C0`) runs if
    the flag is set. It empties the half-written Clipboard, then calls
    KillStuff (put the selection down in place) and AcceptEdits.
  - **Result:** when Copy or Cut fails, the picture is unchanged, the
    selection is put down, the Clipboard is empty, there is one alert,
    and Cut deletes nothing.
  - **Rejected alternative:** stop the activate handler's `MainToAlt`
    while a selection is live. For a lasso selection the working image
    holds the marching-ants mask at that moment, so this would have
    left ants in the picture where the alert had been.
  - **Still open:** the activate handler can blank a *live* selection
    in any other case where MacPaint is brought to the front without
    first putting the selection down. Under MultiFinder that could
    include switching to another program and back with something
    selected. Watch for it in testing; it would need its own fix.

**How to test I2:** `tools/run-interactive.sh --full-startup-disk`
leaves about 2 KB free on the startup disk copy, so copying a large
picture runs out of room partway. See `docs/TEST-ON-MAC-PLUS.md`
section D.

## 11. Plan: selected pixels vanishing under MultiFinder (drafted 21 October 2026, not started)

### What we know

- **The mechanism (from the source).** The activate handler runs
  `MainToAlt` every time MacPaint's window comes to the front. That
  rebuilds the working image from the last accepted picture and, if a
  selection is still live, blanks the area it was taken from. MacPaint
  is safe only because it puts the selection down first (`KillStuff`,
  `AcceptEdits`, `BorrowAlt`) before everything it knows will cover its
  window: desk accessories, About, Open/Save, alerts. The failed Copy
  was the one exception, and I2 closes it.
- **What MultiFinder does to a program that isn't MultiFinder-aware**,
  like MacPaint, which has no SIZE resource:
  - It feeds the program a mouse-down in the menu bar, so the program
    thinks the user chose a desk accessory from the Apple menu and
    calls `OpenDeskAcc`. It does this so the program converts its
    scrap.
  - It also feeds it activate and deactivate events, because the
    program doesn't deactivate its own window.
  - The switching itself happens at the next `GetNextEvent`.

  (*Dr. Dobb's Journal*, Dec 1988, "Writing Programs for MultiFinder";
  Apple Technote TB 14.)
- **So MacPaint's own desk-accessory path should run when you switch
  away,** putting the selection down safely, and the pixels may *not*
  vanish. My earlier warning (§10, "still open") was a guess from the
  code. **First we find out whether it happens at all, and by which
  route.**

### Step 1: find out whether it happens, and how (Mini vMac, Jack driving)

Test both the original 1.5 and 1.6, under MultiFinder, with MacPaint on
its own volume and on the startup volume.

**Selections:**
- a fresh rectangle selection;
- a fresh lasso selection;
- a selection that has been moved, and one that has been Option-copied;
- a pasted picture;
- pasted text (still editable);
- text being typed (insertion point showing).

**Switching away by:**
- clicking another program's window;
- clicking the desktop (Finder);
- choosing another program or a desk accessory from the Apple menu;
- clicking a desk accessory window that is already open.

**Coming back by:**
- clicking MacPaint's window;
- clicking MacPaint's palette;
- choosing MacPaint from the Apple menu (the list of open programs).

**Record for each:** whether the selection is still selected, whether
its pixels are still there after clicking elsewhere in MacPaint, whether
Undo brings them back, and any alert. Keep each case short.

If every case passes, the MultiFinder issue doesn't exist. Record that
and stop.

### Step 2 (only if a case fails): see which events MacPaint gets

- Make a **diagnostic build** (never released) that keeps a small log of
  every event MacPaint processes in memory. For each event it records
  the event code, whether the window becomes active, whether a selection
  is live, and the `scrnFlag` and `edgeFlag` flags.
- The log is written to a file when MacPaint quits, so it can be read
  off the disk image.
- This shows whether MultiFinder's fake desk-accessory step ran before
  the failing switch, or whether MacPaint only got a deactivate and an
  activate.

### Step 3: the fix, chosen from what Step 2 shows

- **Option A (recommended if MacPaint only gets deactivate/activate):**
  - **Where:** handle the **deactivate** that MacPaint didn't cause
    itself. "Didn't cause" means a deactivate arriving while `scrnFlag`
    is FALSE, i.e. not just after `BorrowAlt`.
  - **What:** do exactly what MacPaint does before opening a desk
    accessory: `KillEdges` (lasso marching ants), `KillStuff`,
    `AcceptEdits`, `BorrowAlt`.
  - **Why it's safe:** switching only happens at the next
    `GetNextEvent`, so the screen is still intact while this runs. The
    later activate then restores everything correctly, exactly as after
    a desk accessory.
  - **Size:** about 30 bytes, in the dead EjectReset space at
    `CODE 1 +0x54F4` (freed by I1) or appended to CODE 1, plus a hook
    in the activate handler.
  - **Result:** the selection is put down when you switch away, with
    the same rule and look as opening a desk accessory today.
- **Option B: make MacPaint MultiFinder-aware.**
  - **What:** a SIZE resource with `acceptSuspendResumeEvents` and
    `doesActivateOnFGSwitch`, and handling of suspend and resume
    events (event 15): on suspend do the Option A steps, on resume
    redraw.
  - **Gains:** faster switching, with no fake menu-bar click. It also
    delivers I5 (a proper memory partition).
  - **Costs:** more new code: a new event type and the window's
    highlighting done by MacPaint itself, so more risk.
  - **Recommendation:** a later enhancement, not the fix.
- **Option C: change the activate handler** so it doesn't blank a live
  selection. This was rejected for I2: with a lasso selection the
  working image holds the marching-ants mask, and the screen may
  already be covered by then.

### Step 4: build, check, test

- Add the fix to `tools/patch-macpaint.py`, with the same byte checks,
  disassembly of each site and undo check.
- Retest Step 1's matrix, plus everything that already goes through the
  activate handler:
  - opening and closing desk accessories;
  - About MacPaint;
  - Open and Save dialogs;
  - the disk-full and other alerts;
  - Introduction and Short Cuts;
  - I2 with a full startup disk;
  - running without MultiFinder.

### Step 5: record

- Results go in §9/§11 and in the test sheet.
- The behaviour goes in the manual (Stage 0 report, D2). Under
  MultiFinder, switching away puts the selection down, just as a desk
  accessory does.

### Step 1 result (Jack, Mini vMac under MultiFinder, 21 October 2026)

**Every case passed** in both the original 1.5 and 1.6: no selected
pixels vanished when switching away and back. This matches the
documented behaviour, where MultiFinder fakes a desk-accessory open, so
MacPaint puts the selection down itself. **The MultiFinder issue
doesn't occur, so §11 stops here** and nothing more is to be built. The
"still open" note in §10 is resolved.

The same session passed the 1.6 tests **D1 (⌘W), D2 (⌘N), D3 (⌘Q) and
D4 (⌘ held while quitting: normal quit)**. Session:
`runs/20261021-104052-interactive`.

### I2 result (Jack, Mini vMac, full startup disk, 21 October 2026)

Tests **D5–D8 passed** (`tools/run-interactive.sh --full-startup-disk`,
session `runs/20261021-104330-interactive-full`, about 2 KB free):

- **Copy or Cut of a large rectangle or lasso selection:** one "trouble
  writing the scrap" alert, and the picture is kept. Cut deletes
  nothing.
- **Paste afterwards:** no stale or partial picture.

**Status of 1.6:** every 1.6 change (clipboard fix, I1, I2, I4) has now
passed in Mini vMac. What remains is Jack's test on the real Mac Plus
(§9), where the original clipboard error was seen.

### Hardware test image (21 October 2026)

At Jack's request, both programs were put on the ID 6 Projects disk:
`hardware/HD60_512 Projects.hda`. It's a copy of
`sd-backups/2026-10-20/`, which is left unchanged, with a new `MacPaint`
folder holding `MacPaint` (original) and `MacPaint 1.6`. All the other
files are verified unchanged. See `hardware/README.md`.

The patcher now gives its outputs a fixed date (21 Oct 2026 12:00), so
rebuilds are identical and the Finder doesn't show 1903.
