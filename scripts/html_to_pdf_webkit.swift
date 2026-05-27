import AppKit
import WebKit

final class PDFExporter: NSObject, WKNavigationDelegate {
    let webView: WKWebView
    let inputURL: URL
    let outputURL: URL
    let timeout: TimeInterval
    var didFinish = false

    init(inputURL: URL, outputURL: URL, width: CGFloat, height: CGFloat, timeout: TimeInterval) {
        self.inputURL = inputURL
        self.outputURL = outputURL
        self.timeout = timeout
        let configuration = WKWebViewConfiguration()
        self.webView = WKWebView(frame: CGRect(x: 0, y: 0, width: width, height: height), configuration: configuration)
        super.init()
        self.webView.navigationDelegate = self
    }

    func start() {
        webView.loadFileURL(inputURL, allowingReadAccessTo: inputURL.deletingLastPathComponent())
        DispatchQueue.main.asyncAfter(deadline: .now() + timeout) {
            if !self.didFinish {
                fputs("Timed out loading \(self.inputURL.path)\n", stderr)
                NSApplication.shared.terminate(nil)
            }
        }
    }

    func webView(_ webView: WKWebView, didFinish navigation: WKNavigation!) {
        didFinish = true
        DispatchQueue.main.asyncAfter(deadline: .now() + 0.4) {
            self.renderPDF()
        }
    }

    func webView(_ webView: WKWebView, didFail navigation: WKNavigation!, withError error: Error) {
        fputs("Navigation failed: \(error.localizedDescription)\n", stderr)
        NSApplication.shared.terminate(nil)
    }

    func webView(_ webView: WKWebView, didFailProvisionalNavigation navigation: WKNavigation!, withError error: Error) {
        fputs("Navigation failed: \(error.localizedDescription)\n", stderr)
        NSApplication.shared.terminate(nil)
    }

    func renderPDF() {
        let script = "Math.max(document.body.scrollHeight, document.documentElement.scrollHeight, document.body.offsetHeight, document.documentElement.offsetHeight)"
        webView.evaluateJavaScript(script) { value, error in
            if let error = error {
                fputs("Height read failed: \(error.localizedDescription)\n", stderr)
                NSApplication.shared.terminate(nil)
                return
            }
            let contentHeight = CGFloat((value as? NSNumber)?.doubleValue ?? Double(self.webView.bounds.height))
            var rect = self.webView.bounds
            rect.size.height = max(contentHeight, self.webView.bounds.height)

            if #available(macOS 11.0, *) {
                let config = WKPDFConfiguration()
                config.rect = rect
                self.webView.createPDF(configuration: config) { result in
                    switch result {
                    case .success(let data):
                        do {
                            try FileManager.default.createDirectory(at: self.outputURL.deletingLastPathComponent(), withIntermediateDirectories: true)
                            try data.write(to: self.outputURL)
                            NSApplication.shared.terminate(nil)
                        } catch {
                            fputs("Write failed: \(error.localizedDescription)\n", stderr)
                            NSApplication.shared.terminate(nil)
                        }
                    case .failure(let error):
                        fputs("PDF render failed: \(error.localizedDescription)\n", stderr)
                        NSApplication.shared.terminate(nil)
                    }
                }
            } else {
                fputs("WKWebView PDF export requires macOS 11 or newer.\n", stderr)
                NSApplication.shared.terminate(nil)
            }
        }
    }
}

let args = CommandLine.arguments
guard args.count >= 3 else {
    fputs("Usage: html_to_pdf_webkit.swift input.html output.pdf [width] [height]\n", stderr)
    exit(2)
}

let inputURL = URL(fileURLWithPath: args[1])
let outputURL = URL(fileURLWithPath: args[2])
let width = CGFloat(Double(args.count > 3 ? args[3] : "816") ?? 816)
let height = CGFloat(Double(args.count > 4 ? args[4] : "1056") ?? 1056)

let app = NSApplication.shared
app.setActivationPolicy(.prohibited)
let exporter = PDFExporter(inputURL: inputURL, outputURL: outputURL, width: width, height: height, timeout: 20)
exporter.start()
app.run()
