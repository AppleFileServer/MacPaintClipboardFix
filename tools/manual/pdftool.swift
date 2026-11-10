// pdftool: renders a PDF's pages as PNGs, for checking the manual's
// layout without extra libraries (macOS's own PDF support).
//
//   pdftool render IN.pdf OUT_DIR DPI      each page as OUT_DIR/page-NN.png
//
// (It also imposed the A5 sample two up on A4 until P24 dropped A5.)
//
// Build: swiftc -O tools/manual/pdftool.swift -o build-manual/pdftool
import AppKit
import PDFKit

let a = CommandLine.arguments
func fail(_ s: String) -> Never { FileHandle.standardError.write((s + "\n").data(using: .utf8)!); exit(2) }
guard a.count >= 4, let doc = CGPDFDocument(URL(fileURLWithPath: a[2]) as CFURL) else {
    fail("usage: pdftool render IN.pdf OUT_DIR DPI")
}
let n = doc.numberOfPages

if a[1] == "render", a.count == 5, let dpi = Double(a[4]) {
    try? FileManager.default.createDirectory(atPath: a[3], withIntermediateDirectories: true)
    for i in 1...n {
        guard let p = doc.page(at: i) else { continue }
        let box = p.getBoxRect(.mediaBox)
        let k = dpi / 72
        let w = Int(box.width * k), h = Int(box.height * k)
        let cs = CGColorSpaceCreateDeviceRGB()
        guard let ctx = CGContext(data: nil, width: w, height: h, bitsPerComponent: 8, bytesPerRow: 0,
                                  space: cs, bitmapInfo: CGImageAlphaInfo.noneSkipLast.rawValue) else { fail("context") }
        ctx.setFillColor(CGColor(red: 1, green: 1, blue: 1, alpha: 1))
        ctx.fill(CGRect(x: 0, y: 0, width: w, height: h))
        ctx.scaleBy(x: k, y: k)
        ctx.drawPDFPage(p)
        let rep = NSBitmapImageRep(cgImage: ctx.makeImage()!)
        let path = String(format: "%@/page-%02d.png", a[3], i)
        try! rep.representation(using: .png, properties: [:])!.write(to: URL(fileURLWithPath: path))
    }
    print("rendered \(n) pages to \(a[3])")
} else {
    fail("unknown command \(a[1])")
}
