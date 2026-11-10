import PDFKit
let doc = PDFDocument(url: URL(fileURLWithPath: CommandLine.arguments[1]))!
for a in CommandLine.arguments.dropFirst(2) { let i = Int(a)!; print("=== page \(i)"); print(doc.page(at:i-1)?.string ?? "") }
