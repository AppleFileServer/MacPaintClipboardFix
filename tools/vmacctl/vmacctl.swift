// vmacctl: send keyboard and mouse events to one Mini vMac process only
// (keys go to its process only; mouse events go system-wide, with Mini vMac
// brought to the front first; see below).
//
// Usage: vmacctl PID OX OY SCALE command...
//   PID     Mini vMac's process id
//   OX OY   host screen position (points) of emulated pixel (0,0)
//   SCALE   host points per emulated pixel (2 when Mini vMac is magnified)
// Commands (coordinates are emulated Mac Plus pixels, 0..511 x 0..341):
//   key CODE [cmd|shift|opt|ctrl ...]   press a key (macOS virtual key code)
//   mods down|up NAME ...               hold or release modifier keys
//   move X Y | click X Y | dclick X Y | down X Y | up X Y
//   drag X1 Y1 X2 Y2 [STEPS]
//   sleep MS
//   activate                            bring Mini vMac to the front (it
//                                       ignores clicks while in the background)
import AppKit
import CoreGraphics

let a = CommandLine.arguments
// vmacctl PID window: print "ID X Y W H" (points) for each on-screen window
// of that process, for screencapture -l ID and for finding the Mac screen.
if a.count == 3, a[2] == "window", let pid = Int(a[1]) {
    let list = CGWindowListCopyWindowInfo([.optionOnScreenOnly], kCGNullWindowID) as? [[String: Any]] ?? []
    for w in list where (w[kCGWindowOwnerPID as String] as? Int) == pid {
        let b = w[kCGWindowBounds as String] as? [String: Double] ?? [:]
        print(w[kCGWindowNumber as String] ?? 0, Int(b["X"] ?? 0), Int(b["Y"] ?? 0), Int(b["Width"] ?? 0), Int(b["Height"] ?? 0))
    }
    exit(0)
}
guard a.count >= 6, let pid = pid_t(a[1]), let ox = Double(a[2]), let oy = Double(a[3]), let sc = Double(a[4]) else {
    FileHandle.standardError.write("usage: vmacctl PID OX OY SCALE command...\n".data(using: .utf8)!)
    exit(2)
}
let src = CGEventSource(stateID: .privateState)
// Mini vMac ignores clicks posted to its process alone (it wants the
// event's window, and AppKit misreads positions given with one), so mouse
// events go system-wide like a real mouse. Mini vMac is brought to the front
// first so nothing else is under the pointer, and the pointer is put back
// where it was at the end.
let home = CGEvent(source: nil)?.location
func pt(_ x: String, _ y: String) -> CGPoint {
    CGPoint(x: ox + Double(x)! * sc + sc / 2, y: oy + Double(y)! * sc + sc / 2)
}
func ms(_ n: Int) { usleep(useconds_t(n * 1000)) }
func post(_ e: CGEvent?) { e?.postToPid(pid) }

var held: CGEventFlags = []
func mouse(_ t: CGEventType, _ p: CGPoint, clicks: Int64 = 1) {
    let e = CGEvent(mouseEventSource: src, mouseType: t, mouseCursorPosition: p, mouseButton: .left)
    e?.setIntegerValueField(.mouseEventClickState, value: clicks)
    e?.flags = held
    e?.post(tap: .cghidEventTap)
}
let modKeys: [String: (CGKeyCode, CGEventFlags)] = [
    "cmd": (55, .maskCommand), "shift": (56, .maskShift), "opt": (58, .maskAlternate), "ctrl": (59, .maskControl)]
func setMods(_ names: [String], down: Bool) {
    for n in names {
        guard let (code, flag) = modKeys[n] else { continue }
        if down { held.insert(flag) } else { held.remove(flag) }
        let e = CGEvent(keyboardEventSource: src, virtualKey: code, keyDown: down)
        e?.flags = held
        post(e)
        ms(40)
    }
}
func modsFrom(_ i: inout Int) -> [String] {
    var m: [String] = []
    while i < a.count, modKeys[a[i]] != nil { m.append(a[i]); i += 1 }
    return m
}

NSRunningApplication(processIdentifier: pid)?.activate()
ms(300)
var i = 5
while i < a.count {
    let c = a[i]; i += 1
    switch c {
    case "key":
        let code = CGKeyCode(a[i])!; i += 1
        let mods = modsFrom(&i)
        setMods(mods, down: true)
        let d = CGEvent(keyboardEventSource: src, virtualKey: code, keyDown: true); d?.flags = held; post(d); ms(60)
        let u = CGEvent(keyboardEventSource: src, virtualKey: code, keyDown: false); u?.flags = held; post(u); ms(40)
        setMods(mods.reversed(), down: false)
    case "mods":
        let dn = a[i] == "down"; i += 1
        setMods(modsFrom(&i), down: dn)
    case "move":
        mouse(.mouseMoved, pt(a[i], a[i + 1])); i += 2; ms(30)
    case "down":
        let p = pt(a[i], a[i + 1]); i += 2
        mouse(.mouseMoved, p); ms(30); mouse(.leftMouseDown, p); ms(60)
    case "up":
        let p = pt(a[i], a[i + 1]); i += 2
        mouse(.leftMouseUp, p); ms(60)
    case "click":
        let p = pt(a[i], a[i + 1]); i += 2
        mouse(.mouseMoved, p); ms(40); mouse(.leftMouseDown, p); ms(80); mouse(.leftMouseUp, p); ms(80)
    case "dclick":
        let p = pt(a[i], a[i + 1]); i += 2
        mouse(.mouseMoved, p); ms(40)
        mouse(.leftMouseDown, p, clicks: 1); ms(50); mouse(.leftMouseUp, p, clicks: 1); ms(90)
        mouse(.leftMouseDown, p, clicks: 2); ms(50); mouse(.leftMouseUp, p, clicks: 2); ms(80)
    case "drag":
        let p1 = pt(a[i], a[i + 1]), p2 = pt(a[i + 2], a[i + 3]); i += 4
        var steps = 20
        if i < a.count, let s = Int(a[i]) { steps = s; i += 1 }
        mouse(.mouseMoved, p1); ms(40); mouse(.leftMouseDown, p1); ms(80)
        for s in 1...steps {
            let t = Double(s) / Double(steps)
            mouse(.leftMouseDragged, CGPoint(x: p1.x + (p2.x - p1.x) * t, y: p1.y + (p2.y - p1.y) * t)); ms(25)
        }
        ms(60); mouse(.leftMouseUp, p2); ms(80)
    case "activate":
        NSRunningApplication(processIdentifier: pid)?.activate()
        ms(300)
    case "sleep":
        ms(Int(a[i])!); i += 1
    default:
        FileHandle.standardError.write("unknown command \(c)\n".data(using: .utf8)!)
        exit(2)
    }
}
if let h = home { CGWarpMouseCursorPosition(h) }
