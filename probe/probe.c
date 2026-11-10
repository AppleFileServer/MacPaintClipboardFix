/*
 * Clipboard probe for the MacPaint clipboard fix (docs/PLAN.md, steps 1-2).
 *
 * Runs in Mini vMac with two volumes: "SysDisk" (System 6.0.7, blessed
 * "System Folder", this program inside it) and "PaintVol" (stands in for
 * the volume MacPaint lives on, with a "Graphics" folder). It repeats
 * MacPaint 1.5's own clipboard file calls and the Scrapbook DA's scrap
 * calls with the default directory set as the Finder would set it for
 * MacPaint, and writes what happens to PaintVol:ProbeLog.
 *
 * MacPaint's OpenFile (PaintAsm.a) is a plain _Open with ioVRefNum = drive,
 * ioVersNum = 0, ioPermssn = 0 and ioMisc = NIL; mpOpen below is the same.
 */
#include <Multiverse.h>
#include <string.h>

static char logBuf[16000];
static long logLen;
static short paintVol, sysVol;          /* real vRefNums */
static long sysFolderID, graphicsID, otherID;
static int failures;
static short logVol;
static long logDir = 2;

/* ---- logging ---- */

static void Put(const char *s)
{
    while (*s && logLen < (long)sizeof logBuf - 1)
        logBuf[logLen++] = *s++;
}

static void PutNum(long n)
{
    char t[16]; int i = 0; int neg = n < 0;
    unsigned long u = neg ? -n : n;
    do { t[i++] = '0' + u % 10; u /= 10; } while (u);
    if (neg) Put("-");
    while (i) { char c[2] = { t[--i], 0 }; Put(c); }
}

static void PutP(ConstStringPtr p)
{
    char t[64]; int n = p[0] > 63 ? 63 : p[0];
    memcpy(t, p + 1, n); t[n] = 0; Put(t);
}

static void LogLine(const char *s) { Put(s); Put("\r"); }

static void Check(const char *what, int ok)
{
    Put(ok ? "  PASS " : "  FAIL "); LogLine(what);
    if (!ok) failures++;
}

static void FlushLog(void)
{
    HParamBlockRec pb;
    memset(&pb, 0, sizeof pb);
    pb.fileParam.ioNamePtr = (StringPtr)"\pProbeLog";
    pb.fileParam.ioVRefNum = logVol;
    pb.fileParam.ioDirID = logDir;
    PBHCreateSync(&pb);
    memset(&pb, 0, sizeof pb);
    pb.ioParam.ioNamePtr = (StringPtr)"\pProbeLog";
    pb.ioParam.ioVRefNum = logVol;
    pb.fileParam.ioDirID = logDir;
    pb.ioParam.ioPermssn = fsRdWrPerm;
    if (PBHOpenSync(&pb) != noErr) return;
    {
        short ref = pb.ioParam.ioRefNum;
        ParamBlockRec w;
        memset(&w, 0, sizeof w);
        w.ioParam.ioRefNum = ref;
        w.ioParam.ioBuffer = logBuf;
        w.ioParam.ioReqCount = logLen;
        w.ioParam.ioPosMode = fsFromStart;
        PBWriteSync(&w);
        memset(&w, 0, sizeof w);
        w.ioParam.ioRefNum = ref;
        w.ioParam.ioMisc = (Ptr)logLen;
        PBSetEOFSync(&w);
        memset(&w, 0, sizeof w);
        w.ioParam.ioRefNum = ref;
        PBCloseSync(&w);
        memset(&w, 0, sizeof w);
        w.ioParam.ioVRefNum = logVol;
        PBFlushVolSync(&w);
    }
}

/* ---- file system helpers ---- */

static short FindVol(ConstStringPtr name)
{
    short i;
    for (i = 1; i < 20; i++) {
        HParamBlockRec pb; Str63 n;
        memset(&pb, 0, sizeof pb);
        pb.volumeParam.ioNamePtr = n;
        pb.volumeParam.ioVolIndex = i;
        if (PBHGetVInfoSync(&pb) != noErr) break;
        if (n[0] == name[0] && !memcmp(n + 1, name + 1, n[0]))
            return pb.volumeParam.ioVRefNum;
    }
    return 0;
}

static long DirID(short vol, long parent, ConstStringPtr name)
{
    CInfoPBRec pb;
    memset(&pb, 0, sizeof pb);
    pb.dirInfo.ioNamePtr = (StringPtr)name;
    pb.dirInfo.ioVRefNum = vol;
    pb.dirInfo.ioDrDirID = parent;
    if (PBGetCatInfoSync(&pb) != noErr) return 0;
    return pb.dirInfo.ioDrDirID;
}

static short OpenWD(short vol, long dir)
{
    WDPBRec pb;
    memset(&pb, 0, sizeof pb);
    pb.ioVRefNum = vol;
    pb.ioWDDirID = dir;
    pb.ioWDProcID = 'MPcf';
    if (PBOpenWDSync(&pb) != noErr) return 0;
    return pb.ioVRefNum;
}

static void SetDefault(short ref)
{
    ParamBlockRec pb;
    memset(&pb, 0, sizeof pb);
    pb.volumeParam.ioVRefNum = ref;
    PBSetVolSync(&pb);
}

/* Data-fork length of a file, or -1 if it isn't there. */
static long FileLen(short vol, long dir, ConstStringPtr name)
{
    HParamBlockRec pb;
    memset(&pb, 0, sizeof pb);
    pb.fileParam.ioNamePtr = (StringPtr)name;
    pb.fileParam.ioVRefNum = vol;
    pb.fileParam.ioDirID = dir;
    if (PBHGetFInfoSync(&pb) != noErr) return -1;
    return pb.fileParam.ioFlLgLen;
}

static void Delete(short vol, long dir, ConstStringPtr name)
{
    HParamBlockRec pb;
    memset(&pb, 0, sizeof pb);
    pb.fileParam.ioNamePtr = (StringPtr)name;
    pb.fileParam.ioVRefNum = vol;
    pb.fileParam.ioDirID = dir;
    PBHDeleteSync(&pb);
}

static void MakeStale(short vol, long dir)
{
    HParamBlockRec pb;
    memset(&pb, 0, sizeof pb);
    pb.fileParam.ioNamePtr = (StringPtr)"\pClipboard File";
    pb.fileParam.ioVRefNum = vol;
    pb.fileParam.ioDirID = dir;
    PBHCreateSync(&pb);
}

/* MacPaint's OpenFile(drive, 0, scrapName, NIL, refNum), with a sentinel
   in ioRefNum so we can see what a failed open leaves behind. */
static OSErr mpOpen(short drive, StringPtr name, short *ref)
{
    ParamBlockRec pb;
    OSErr err;
    memset(&pb, 0, sizeof pb);
    pb.ioParam.ioNamePtr = name;
    pb.ioParam.ioVRefNum = drive;
    pb.ioParam.ioRefNum = 0x7777;
    err = PBOpenSync(&pb);
    *ref = pb.ioParam.ioRefNum;
    return err;
}

static int OkOpen(OSErr e) { return e == noErr || e == opWrErr; }

static void CloseRef(short ref)
{
    ParamBlockRec pb;
    memset(&pb, 0, sizeof pb);
    pb.ioParam.ioRefNum = ref;
    PBCloseSync(&pb);
}

static OSErr RW(short ref, long pos, long n, void *buf, int write)
{
    ParamBlockRec pb;
    memset(&pb, 0, sizeof pb);
    pb.ioParam.ioRefNum = ref;
    pb.ioParam.ioBuffer = buf;
    pb.ioParam.ioReqCount = n;
    pb.ioParam.ioPosMode = fsFromStart;
    pb.ioParam.ioPosOffset = pos;
    return write ? PBWriteSync(&pb) : PBReadSync(&pb);
}

/* Which file did a refNum open?  Returns its volume and parent folder. */
static void Where(short ref, short *vol, long *dir)
{
    FCBPBRec pb; Str63 n;
    memset(&pb, 0, sizeof pb);
    pb.ioNamePtr = n;
    pb.ioRefNum = ref;
    pb.ioFCBIndx = 0;
    *vol = 0; *dir = 0;
    if (PBGetFCBInfoSync(&pb) == noErr) { *vol = pb.ioFCBVRefNum; *dir = pb.ioFCBParID; }
}

static void PutPlace(short vol, long dir)
{
    if (vol == sysVol && dir == sysFolderID) Put("SysDisk:System Folder");
    else if (vol == sysVol && dir == 2) Put("SysDisk root");
    else if (vol == paintVol && dir == 2) Put("PaintVol root");
    else if (vol == paintVol && dir == graphicsID) Put("PaintVol:Graphics");
    else { Put("vol "); PutNum(vol); Put(" dir "); PutNum(dir); }
}

/* Volume of the open System file (Gryphel's GetSysVol, via the FCB). */
static short SysMapVol(void)
{
    short v; long d;
    Where(*(short *)0x0A58, &v, &d);
    return v;
}

static void ReportOpen(const char *label, short drive, short *refOut)
{
    short ref, v; long d;
    OSErr err = mpOpen(drive, InfoScrap()->scrapName, &ref);
    Put("  "); Put(label); Put(": _Open drive "); PutNum(drive);
    Put(" -> err "); PutNum(err);
    if (err == noErr || err == opWrErr) {   /* -49: already open, refNum is the open path; MacPaint accepts it */
        Where(ref, &v, &d);
        Put(", opened "); PutPlace(v, d);
    } else {
        Put(", ioRefNum left as "); PutNum(ref);
    }
    LogLine("");
    if (refOut) *refOut = err == noErr ? ref : 0;
    else if (err == noErr) CloseRef(ref);
}

static void ScanClipboards(void)
{
    static const struct { int sys; int which; } places[] = {{1,0},{1,1},{0,0},{0,1}};
    int i;
    for (i = 0; i < 4; i++) {
        short v = places[i].sys ? sysVol : paintVol;
        long d = places[i].sys ? (places[i].which ? 2 : sysFolderID)
                               : (places[i].which ? graphicsID : 2);
        long n = FileLen(v, d, "\pClipboard File");
        Put("    Clipboard File in "); PutPlace(v, d); Put(": ");
        if (n < 0) LogLine("none"); else { PutNum(n); LogLine(" bytes"); }
    }
}

static long StateNow(void) { return InfoScrap()->scrapState; }

int main(void)
{
    short bootDrive = *(short *)0x0210;
    short wdGraphics, wdOther, ref;
    static char data1[] = "SCRAPBOOK-ITEM-NEW!!";   /* 20 bytes, even */
    static char data2[] = "MACPAINT-COPY-OK-ABCD";  /* 21 + pad */
    char buf[64];
    long off, size;

    logVol = bootDrive; logDir = 0;
    LogLine("MacPaint clipboard probe 1: started");
    FlushLog();
    {   /* inserted disks are only mounted when someone asks */
        short drv;
        for (drv = 1; drv <= 8; drv++) {
            ParamBlockRec m;
            memset(&m, 0, sizeof m);
            m.volumeParam.ioVRefNum = drv;
            PBMountVol(&m);
        }
    }
    paintVol = FindVol("\pPaintVol");
    sysVol = FindVol("\pSysDisk");
    if (!paintVol) { LogLine("PaintVol not mounted"); FlushLog(); return 1; }
    logVol = paintVol; logDir = 2;
    FlushLog();
    sysFolderID = DirID(sysVol, 2, "\pSystem Folder");
    graphicsID = DirID(paintVol, 2, "\pGraphics");
    otherID = DirID(sysVol, 2, "\pOther Folder");
    wdGraphics = OpenWD(paintVol, graphicsID);
    wdOther = OpenWD(sysVol, otherID);

    LogLine("MacPaint clipboard probe 1");
    LogLine("== A. Environment");
    Put("  SysDisk vRefNum "); PutNum(sysVol); Put(", System Folder dirID "); PutNum(sysFolderID); LogLine("");
    Put("  PaintVol vRefNum "); PutNum(paintVol); Put(", Graphics dirID "); PutNum(graphicsID); LogLine("");
    {
        WDPBRec pb;
        memset(&pb, 0, sizeof pb);
        pb.ioVRefNum = bootDrive;
        PBGetWDInfoSync(&pb);
        Put("  BootDrive "); PutNum(bootDrive); Put(" = "); PutPlace(pb.ioWDVRefNum, pb.ioWDDirID); LogLine("");
        Check("BootDrive is the startup System Folder",
              pb.ioWDVRefNum == sysVol && pb.ioWDDirID == sysFolderID);
    }
    Put("  System file (SysMap) volume "); PutNum(SysMapVol()); LogLine("");
    Put("  scrapName '"); PutP(InfoScrap()->scrapName); Put("', scrapState "); PutNum(StateNow()); LogLine("");
    FlushLog();

    LogLine("== B. Where does the Scrap Manager keep Clipboard File?");
    Delete(sysVol, sysFolderID, "\pClipboard File");
    SetDefault(wdGraphics);               /* as if MacPaint were launched */
    ZeroScrap();
    PutScrap(8, 'TEXT', (Ptr)"probe-B!");
    Put("  UnloadScrap with default = PaintVol:Graphics -> "); PutNum(UnloadScrap()); LogLine("");
    ScanClipboards();
    Check("Scrap Manager wrote SysDisk:System Folder:Clipboard File",
          FileLen(sysVol, sysFolderID, "\pClipboard File") > 0);
    Check("and nothing on PaintVol",
          FileLen(paintVol, 2, "\pClipboard File") < 0 && FileLen(paintVol, graphicsID, "\pClipboard File") < 0);
    FlushLog();

    LogLine("== C. Do the Scrapbook's calls leave the scrap in memory?");
    UnloadScrap();                        /* MacPaint starts with UnloadScrap */
    Put("  after UnloadScrap: scrapState "); PutNum(StateNow()); LogLine("");
    ZeroScrap();                          /* Scrapbook DRVR 17: ZeroScrap, PutScrap */
    PutScrap(20, 'PICT', (Ptr)data1);
    Put("  after ZeroScrap+PutScrap: scrapState "); PutNum(StateNow());
    Put(", file length "); PutNum(FileLen(sysVol, sysFolderID, "\pClipboard File")); LogLine("");
    LogLine("  (scrapState > 0 means in memory; the file still holds the old scrap)");
    FlushLog();

    LogLine("== D. MacPaint 1.5 as shipped: OpenFile(0, ...)");
    UnloadScrap();
    SetDefault(wdGraphics);
    ReportOpen("default = PaintVol:Graphics (own volume)", 0, 0);
    SetDefault(paintVol);
    ReportOpen("default = PaintVol root", 0, 0);
    SetDefault(wdOther);
    ReportOpen("default = SysDisk:Other Folder (same volume)", 0, 0);
    SetDefault(bootDrive);
    ReportOpen("default = System Folder", 0, 0);
    FlushLog();

    LogLine("== E. Candidate fixes, MacPaint on its own volume");
    SetDefault(wdGraphics);
    ReportOpen("BootDrive", bootDrive, 0);
    ReportOpen("SysMap volume (Gryphel)", SysMapVol(), 0);
    FlushLog();

    LogLine("== F. Stale Clipboard File on MacPaint's volume");
    MakeStale(paintVol, graphicsID);
    MakeStale(paintVol, 2);
    SetDefault(wdGraphics);
    ReportOpen("as shipped, OpenFile(0)", 0, 0);
    ReportOpen("BootDrive", bootDrive, 0);
    ReportOpen("SysMap volume (Gryphel)", SysMapVol(), 0);
    Delete(paintVol, graphicsID, "\pClipboard File");
    Delete(paintVol, 2, "\pClipboard File");
    FlushLog();

    LogLine("== G. Patched Copy (BootDrive), then read back via the Scrap Manager");
    SetDefault(wdGraphics);
    ZeroScrap();
    UnloadScrap();
    {
        PScrapStuff ss = InfoScrap();
        long typ = 'PICT', len = 22, pos = 0;
        if (OkOpen(mpOpen(bootDrive, ss->scrapName, &ref))) {
            RW(ref, pos, 4, &typ, 1); pos += 4;
            RW(ref, pos, 4, &len, 1); pos += 4;
            RW(ref, pos, 22, data2, 1); pos += 22;
            {
                ParamBlockRec pb;
                memset(&pb, 0, sizeof pb);
                pb.ioParam.ioRefNum = ref;
                pb.ioParam.ioMisc = (Ptr)pos;
                PBSetEOFSync(&pb);
            }
            ss->scrapSize = pos;
            CloseRef(ref);
        }
    }
    {
        Handle h = NewHandle(0);
        LoadScrap();
        size = GetScrap(h, 'PICT', &off);
        Put("  GetScrap PICT -> size "); PutNum(size); LogLine("");
        Check("another application would see MacPaint's picture",
              size == 22 && !memcmp(*h, data2, 22));
        DisposeHandle(h);
    }
    FlushLog();

    LogLine("== H. Paste after a Scrapbook copy (scrap in memory)");
    UnloadScrap();
    ZeroScrap();
    PutScrap(20, 'PICT', (Ptr)data1);
    Put("  scrapState "); PutNum(StateNow()); LogLine("");
    SetDefault(wdGraphics);
    size = GetScrap(NULL, 'PICT', &off);
    memset(buf, 0, sizeof buf);
    if (OkOpen(mpOpen(bootDrive, InfoScrap()->scrapName, &ref))) {
        RW(ref, off, 20, buf, 0); CloseRef(ref);
    }
    Put("  BootDrive fix only, read at offset "); PutNum(off); Put(": '");
    buf[20] = 0; Put(buf); LogLine("'");
    Put("  RESULT first fix alone pastes the Scrapbook item: ");
    LogLine(!memcmp(buf, data1, 20) ? "yes" : "NO (old scrap read)");
    /* second fix: UnloadScrap before reading the file */
    UnloadScrap();
    size = GetScrap(NULL, 'PICT', &off);
    memset(buf, 0, sizeof buf);
    if (OkOpen(mpOpen(bootDrive, InfoScrap()->scrapName, &ref))) {
        RW(ref, off, 20, buf, 0); CloseRef(ref);
    }
    Put("  with UnloadScrap first, read at offset "); PutNum(off); Put(": '");
    buf[20] = 0; Put(buf); LogLine("'");
    Check("both fixes paste the Scrapbook item", !memcmp(buf, data1, 20));

    Put("FAILURES: "); PutNum(failures); LogLine("");
    LogLine("DONE");
    FlushLog();
    return 0;
}
