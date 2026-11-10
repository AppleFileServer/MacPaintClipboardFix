import PDFKit
let doc = PDFDocument(url: URL(fileURLWithPath: CommandLine.arguments[1]))!
let needle = CommandLine.arguments[2].lowercased()
var hits = 0
for i in 0..<doc.pageCount { if let s = doc.page(at:i)?.string, s.lowercased().contains(needle) { hits += 1; print("page", i+1) } }
print("pages", doc.pageCount, "hits", hits, "hasText", (doc.page(at: 5)?.string?.count ?? 0))
