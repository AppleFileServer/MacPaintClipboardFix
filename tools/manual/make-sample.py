#!/usr/bin/env python3
"""Writes docs/manual/sample/sample.html, the Stage 2 prototype of the
MacPaint User's Guide at the family's 7½ x 9 in (P24): the cover, the
copyright page, the title page, the contents, About This Manual,
Chapter 1's opener spread, Lesson 3 (the screen, labelled), Lesson 10
(a large-illustration page) and the Edit menu's reference page.

Every statement traces to fact-check.md. Anything known only from the
1.3 source is marked CHECK (class "check"), which the finished book
won't print.

Usage: make-sample.py, then
    tools/manual/build-pdf.sh docs/manual/sample/sample.html build-manual/MacPaint-sample.pdf"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))   # book.py, callouts.py (python -I)
from book import BOOK, img, opener, page
import callouts

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "..", "docs", "manual", "sample", "sample.html")
EDITION = "MacPaint 1.6 &middot; Sample pages, October 2026 &middot; Own-use edition: not for distribution"
CHECK = '<span class="check">CHECK</span>'

SCALE = 0.6             # points per Mac pixel: a whole screen (512) fills
                        # the text column (308 pt)


def boxes(*items):
    return '<ul class="boxes">%s</ul>' % "".join("<li>%s</li>" % i for i in items)


def margin_head(title, ident):
    return '<div class="margin"><h2 class="margin-head" id="%s">%s</h2></div>' % (ident, title)


def lesson_head(n, title, ident):
    return ('<div class="margin"><div class="lesson-head" id="%s"><span class="number">%d</span>'
            '<span class="title">%s</span></div></div>' % (ident, n, title))


# ---- Front matter ------------------------------------------------------------

COVER = '<div class="cover"><img src="private/cover-macpaint.jpg"></div>\n'

COPYRIGHT = """
<div class="copyright"><div class="copy-columns">
 <div>
  <p class="copy-head">Copyright</p>
  <p>This manual is copyrighted, with all rights reserved.</p>
  <p>MacPaint User&rsquo;s Guide &copy; 2026 Jack McAteer.</p>
  <p>MacPaint was written by Bill Atkinson. MacPaint &copy; 1985 Apple
  Computer, Inc.</p>
  <p>MacPaint 1.6 is a personal modification of MacPaint 1.5, made for
  this edition and used under the terms on which Apple released
  MacPaint&rsquo;s source code: for non-commercial use only.</p>
  <p>This manual is an independent work, and is not affiliated with,
  endorsed by, sponsored by or produced by Apple Inc.</p>
  <p>Apple, Macintosh, MacPaint and ImageWriter are trademarks of Apple
  Inc. Other names and trademarks belong to their respective owners.</p>
  <p>%s</p>
 </div>
 <div>
  <p class="copy-head">Please note</p>
  <p>MacPaint is intended to run on vintage hardware and software. Keep
  backup copies of your pictures on another disk.</p>
  <p class="caps">The author accepts no responsibility for loss or
  corruption of pictures or other data arising from the use of the
  software, except to the extent that such liability cannot lawfully be
  excluded or limited.</p>
 </div>
</div></div>
""" % EDITION

TITLE = ('<div class="title-page"><div class="title-logo">'
         '<img class="logo" src="private/rainbow-logo.png" style="width:36pt; height:%.1fpt"></div>'
         '<p class="title-name">%s</p></div>\n' % (36 * 295 / 314, BOOK))

# The whole book's contents (outline.md). Page numbers are shown only for
# what's in the sample: the rest come with the book.
TOC = [("about", "About This Manual", "part"),
       ("chapter-1", "Chapter 1: Learning MacPaint", "ch"),
       (None, "Introduction: What Is MacPaint?", "sec"),
       (None, "Lessons 1&ndash;2: Putting MacPaint on Your Disk; Starting MacPaint", "sec"),
       ("lesson-3", "Lesson 3: The MacPaint Screen", "sec"),
       (None, "Lessons 4&ndash;9: Painting, Shapes, Erasing, Selecting, Words", "sec"),
       ("lesson-10", "Lesson 10: Looking at the Whole Page", "sec"),
       (None, "Lessons 11&ndash;13: Saving, Printing, Quitting", "sec"),
       (None, "What Now?", "sec"),
       (None, "Chapter 2: Using MacPaint", "ch"),
       (None, "Painting and Drawing &middot; Patterns &middot; Erasing", "sec"),
       (None, "Selecting and Changing &middot; Cut, Copy and Paste", "sec"),
       (None, "Text &middot; Detailed Work &middot; The Whole Page", "sec"),
       (None, "Documents &middot; Printing", "sec"),
       (None, "Chapter 3: MacPaint Reference", "ch"),
       (None, "The Screen &middot; The Tools", "sec"),
       ("edit-menu", "The Menus", "sec"),
       (None, "The Introduction and Short Cuts Screens", "sec"),
       (None, "Appendix A: Messages", "part"),
       (None, "Appendix B: MacPaint and Your Disks", "part"),
       (None, "Appendix C: Keyboard Shortcuts", "part"),
       (None, "Appendix D: Troubleshooting", "part"),
       (None, "Appendix E: About MacPaint 1.6", "part"),
       (None, "Glossary", "part"), (None, "Index", "part")]


def contents():
    rows = "".join('<li class="toc-%s"><span class="t">%s</span>%s</li>'
                   % (cls, t, '<a class="pg%s" href="#%s"></a>' % (" roman" if a == "about" else "", a)
                      if a else "")
                   for a, t, cls in TOC)
    return ('<div class="front"><div class="flow">'
            '<div class="margin"><h2 class="contents-head">Contents</h2></div>'
            '<ul class="toc book-toc">%s</ul>'
            '<p class="draft-note">Sample pages: page numbers are given only for the '
            'pages in this sample.</p></div></div>\n' % rows)


ABOUT = "".join([
    '<div class="front"><div class="flow">',
    margin_head("About This Manual", "about"),
    "<p>MacPaint is for painting pictures on your Macintosh, with tools "
    "much like a painter&rsquo;s own: a paintbrush, a pencil, spraypaint, "
    "an eraser, and a paint can that fills whole areas. This manual shows "
    "you how.</p>",

    '<div class="margin"><h3 class="margin-sub">What you need</h3></div>',
    "<p>To use MacPaint, you need:</p>",
    boxes("a Macintosh Plus with System 6.0.7;",
          "a hard disk, or 800K floppy disks, for MacPaint and your pictures;",
          "an ImageWriter printer, if you&rsquo;d like to print."),

    '<div class="margin"><h3 class="margin-sub">What you should know</h3></div>',
    "<p>This manual assumes you know the basics of your Macintosh: using "
    "the mouse, choosing from menus, and working with windows and disks. "
    "If you don&rsquo;t, start with your <i>Macintosh</i> owner&rsquo;s "
    "guide.</p>",

    '<div class="margin"><h3 class="margin-sub">How to use this manual</h3></div>',
    "<p>There are three ways in:</p>",
    boxes("<b>Learn it:</b> Chapter 1 paints one picture with you, in "
          "thirteen short lessons.",
          "<b>Look it up:</b> Chapter 2 shows how to do each task, Chapter 3 "
          "describes every tool and menu, and the appendixes explain "
          "MacPaint&rsquo;s messages.",
          "<b>Just try it:</b> start MacPaint and paint. Undo takes back the "
          "last thing you did."),

    '<div class="margin"><h3 class="margin-sub">MacPaint 1.6</h3></div>',
    "<p>This manual describes MacPaint 1.6. Nearly all of it applies to "
    "MacPaint 1.5 too: Appendix E lists the differences.</p>",

    '<div class="margin"><h3 class="margin-sub">Conventions</h3></div>',
    '<p class="step">A step tells you what to do.</p>',
    "<p>The plain text after it tells you what happens.</p>",
    '<p class="grey">Grey text adds a remark you can skip.</p>',
    "<p>Keys are named as they&rsquo;re marked: <kbd>Return</kbd>, "
    "<kbd>Backspace</kbd>, and the Command key, <kbd>&#8984;</kbd>.</p>",
    "</div></div>\n",
])

# ---- Chapter 1 ------------------------------------------------------------------

S01_LABELS = [("Menu bar", 4, 70, 9),
              ("The document&rsquo;s name", 22, 262, 38),
              ("Tool palette", 72, 14, 120),
              ("Drawing window", 120, 84, 200),
              ("Line widths", 170, 22, 283),
              ("Current pattern", 186, 90, 318),
              ("Pattern palette", 202, 125, 330)]

LESSON3 = "".join([
    '<div class="chapter page-break"><div class="flow">',
    lesson_head(3, "The MacPaint Screen", "lesson-3"),
    "<p>When MacPaint starts, it opens a new, untitled document, with the "
    "paintbrush chosen. Everything you paint with is on the screen at "
    "once.</p>",
    '<figure class="wide">%s</figure>'
    % callouts.figure("figures/s01-screen.png", 512, 342, SCALE, S01_LABELS),
    "<p>The <b>tool palette</b> on the left holds MacPaint&rsquo;s twenty "
    "tools. To choose a tool, click it: the tool you&rsquo;ve chosen is "
    "highlighted.</p>",
    "<p>Below it, the <b>line widths</b> set how thick lines and the "
    "borders of shapes are drawn. A check mark shows the width in "
    "use.</p>",
    "<p>Along the bottom, the <b>pattern palette</b> holds 38 patterns. "
    "The box at its left shows the <b>current pattern</b>: the one "
    "you&rsquo;re painting with.</p>",
    "<p>The <b>drawing window</b> shows part of your picture: 416 dots "
    "across and 240 down, out of a page of 576 by 720 dots, 8 by 10 inches. "
    "It has no scroll bars. Lesson 10 shows how to see the rest of the "
    "page.</p>",
    '<p class="grey">For a reminder of the tools and the short cuts, '
    "choose Introduction or Short Cuts from the Goodies menu.</p>",
    "</div></div>\n",
])

LESSON10 = "".join([
    '<div class="chapter page-break"><div class="flow">',
    lesson_head(10, "Looking at the Whole Page", "lesson-10"),
    "<p>The window shows only part of the page. To see the whole page at "
    "once:</p>",
    '<p class="step">Choose Show Page from the Goodies menu.</p>',
    "<p>The whole page appears, reduced, with your picture on it. The "
    "dotted rectangle marks the part of the page the window shows.</p>",
    '<figure>%s</figure>' % img("s05-show-page", round(512 * SCALE, 1)),
    '<p class="step">Drag the dotted rectangle to another part of the '
    'page, then click OK.</p>',
    "<p>The window now shows that part of the page.</p>",
    "<p>To move your view a little way, use the grabber:</p>",
    '<p class="step">Click the grabber (the hand) in the tool palette, then '
    'drag in the window.</p>',
    '<figure>%s</figure>' % img("s06-grabber", round(422 * SCALE, 1)),   # its top, torn
    "<p>The picture moves with the pointer, so you can see another part of "
    "the page.</p>",
    "</div></div>\n",
])

# ---- Chapter 3: the Edit menu ----------------------------------------------------


def entry(name, key, text):
    k = ' <span class="key">%s</span>' % key if key else ""
    return ('<div class="entry"><div class="margin"><h4 class="cmd">%s%s</h4></div>'
            '<p>%s</p></div>' % (name, k, text))


EDIT = "".join([
    '<div class="chapter page-break"><div class="foot-name" data-foot="Chapter 3: MacPaint Reference"></div>'
    '<div class="flow">',
    margin_head("The Menus", "menus"),
    '<h3 class="ref-head section" id="edit-menu">The Edit Menu</h3>',
    '<figure class="beside">%s</figure>' % img("m03-edit", round(265 * 0.48, 1)),   # 4 dots a pixel at 600 dpi
    "<p>The Edit menu&rsquo;s commands change the part of the picture "
    "you&rsquo;ve selected. Until you select something, only Undo and "
    "Paste can be chosen.</p>",
    entry("Undo", "&#8984;Z", "Takes back the last change you made to the "
          "picture. The <kbd>`</kbd> key does the same."),
    entry("Cut", "&#8984;X", "Removes the selection and puts it on the "
          "Clipboard."),
    entry("Copy", "&#8984;C", "Puts a copy of the selection on the "
          "Clipboard."),
    entry("Paste", "&#8984;V", "Puts the Clipboard&rsquo;s picture in the "
          "middle of the window, selected, ready to drag into place."),
    entry("Clear", "", "Erases the selection, leaving white. "
          "<kbd>Backspace</kbd> does the same."),
    entry("Invert", "", "Turns the selection&rsquo;s black dots white and "
          "its white dots black." + CHECK),
    entry("Fill", "", "Fills the selection with the current pattern." + CHECK),
    entry("Trace Edges", "&#8984;E", "Outlines the shapes in the selection." + CHECK),
    entry("Flip Horizontal", "", "Flips the selection from left to right."
          + CHECK),
    entry("Flip Vertical", "", "Flips the selection upside down." + CHECK),
    entry("Rotate", "", "Turns the selection a quarter turn "
          "anticlockwise."),
    '<p class="grey">Flip Horizontal, Flip Vertical and Rotate work on a '
    "selection made with the selection rectangle, not the lasso." + CHECK + "</p>",
    "</div></div>\n",
])

OPENER = opener(1, "Learning MacPaint", "c1-opener").replace(
    '<div class="opener opener-left">', '<div class="opener opener-left" id="chapter-1">', 1)

body = COVER + COPYRIGHT + TITLE + contents() + ABOUT + OPENER + LESSON3 + LESSON10 + EDIT
os.makedirs(os.path.dirname(OUT), exist_ok=True)
open(OUT, "w", encoding="utf-8").write(page(BOOK + ": sample pages", body))
print("wrote", os.path.normpath(OUT))
