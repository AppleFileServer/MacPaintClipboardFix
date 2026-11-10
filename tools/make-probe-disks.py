"""Make the two Mini vMac disks for a clipboard probe run.

Usage: python -I make-probe-disks.py SYSTEM_IMAGE AUTOQUIT_IMAGE APP_DSK OUT_DIR [PAINT_APP_RSRC]

disk1.dsk "SysDisk": a blessed "System Folder" holding the System from
SYSTEM_IMAGE, AutoQuit (as the Finder) and the program from APP_DSK as
the startup application, plus an empty "Other Folder" at the root.
disk2.dsk "PaintVol": a "Graphics" folder, standing in for the volume
MacPaint lives on (with MacPaint itself in it if PAINT_APP_RSRC is given).

The inputs are only read; both disks are new files in OUT_DIR.
"""
import sys, os, machfs

def load(path):
    v = machfs.Volume()
    v.read(open(path, 'rb').read())
    return v

sysimg, aqimg, appdsk, out = sys.argv[1:5]
paint = sys.argv[5] if len(sys.argv) > 5 else None

src = load(sysimg)['System Folder']
aq = load(aqimg)['AutoQuit']
app_vol = load(appdsk)
app = next(f for f in app_vol.values() if isinstance(f, machfs.File) and f.type == b'APPL')

d1 = machfs.Volume(); d1.name = 'SysDisk'
sf = machfs.Folder(); d1['System Folder'] = sf
sf['System'] = src['System']
sf['AutoQuit'] = aq
sf['Probe'] = app
d1['Other Folder'] = machfs.Folder()
open(os.path.join(out, 'disk1.dsk'), 'wb').write(
    d1.write(size=4 * 1024 * 1024, startapp=('System Folder', 'Probe')))

d2 = machfs.Volume(); d2.name = 'PaintVol'
g = machfs.Folder(); d2['Graphics'] = g
if paint:
    mp = machfs.File(); mp.type, mp.creator = b'APPL', b'MPNT'
    mp.rsrc = open(paint, 'rb').read()
    g['MacPaint'] = mp
open(os.path.join(out, 'disk2.dsk'), 'wb').write(d2.write(size=800 * 1024))
print('disks written to', out)
