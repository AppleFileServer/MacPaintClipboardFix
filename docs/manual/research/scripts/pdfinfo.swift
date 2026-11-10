import PDFKit
import AppKit
// usage: pdfinfo.swift <pdf> [outdir pages(comma) scale]
let args = CommandLine.arguments
let url = URL(fileURLWithPath: args[1])
guard let doc = PDFDocument(url: url) else { print("cannot open"); exit(1) }
print("pages:", doc.pageCount)
var sizes: [String: [Int]] = [:]
for i in 0..<doc.pageCount {
  let p = doc.page(at: i)!
  let b = p.bounds(for: .mediaBox)
  let k = String(format: "%.2f x %.2f pt (%.1f x %.1f mm)", b.width, b.height, b.width/72*25.4, b.height/72*25.4)
  sizes[k, default: []].append(i+1)
}
for (k, v) in sizes { print(k, "pages:", v.count, v.prefix(5)) }
if args.count > 3 {
  let out = args[2]; let scale = args.count > 4 ? Double(args[4])! : 1.5
  for s in args[3].split(separator: ",") {
    let n = Int(s)!; guard n <= doc.pageCount else { continue }
    let p = doc.page(at: n-1)!
    let b = p.bounds(for: .mediaBox)
    let w = Int(b.width*scale), h = Int(b.height*scale)
    let rep = NSBitmapImageRep(bitmapDataPlanes: nil, pixelsWide: w, pixelsHigh: h, bitsPerSample: 8, samplesPerPixel: 4, hasAlpha: true, isPlanar: false, colorSpaceName: .deviceRGB, bytesPerRow: 0, bitsPerPixel: 0)!
    NSGraphicsContext.saveGraphicsState()
    let ctx = NSGraphicsContext(bitmapImageRep: rep)!
    NSGraphicsContext.current = ctx
    let cg = ctx.cgContext
    cg.setFillColor(NSColor.white.cgColor); cg.fill(CGRect(x:0,y:0,width:w,height:h))
    cg.scaleBy(x: scale, y: scale)
    p.draw(with: .mediaBox, to: cg)
    NSGraphicsContext.restoreGraphicsState()
    let data = rep.representation(using: .png, properties: [:])!
    try! data.write(to: URL(fileURLWithPath: "\(out)/p\(String(format: "%03d", n)).png"))
  }
}
