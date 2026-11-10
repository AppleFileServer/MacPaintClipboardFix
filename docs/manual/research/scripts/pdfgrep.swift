import PDFKit
import Foundation
let doc = PDFDocument(url: URL(fileURLWithPath: CommandLine.arguments[1]))!
let re = try! NSRegularExpression(pattern: CommandLine.arguments[2], options: [.caseInsensitive])
for i in 0..<doc.pageCount {
  guard let s = doc.page(at:i)?.string else { continue }
  let ns = s as NSString
  for m in re.matches(in: s, range: NSRange(location:0, length: ns.length)) {
    let a = max(0, m.range.location-250); let l = min(ns.length-a, m.range.length+500)
    print("--- p\(i+1): " + ns.substring(with: NSRange(location:a, length:l)).replacingOccurrences(of: "\n", with: " "))
  }
}
