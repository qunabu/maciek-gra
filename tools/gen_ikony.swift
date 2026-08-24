import Foundation
import CoreGraphics
import ImageIO
import UniformTypeIdentifiers

// usage: gen_ikony <katalog>
let kat = CommandLine.arguments.count > 1 ? CommandLine.arguments[1] : FileManager.default.currentDirectoryPath

func wczytaj(_ p: String) -> CGImage? {
    guard let src = CGImageSourceCreateWithURL(URL(fileURLWithPath: p) as CFURL, nil) else { return nil }
    return CGImageSourceCreateImageAtIndex(src, 0, nil)
}

let maciek = wczytaj(kat + "/maciek_ship.png")

func zapisz(_ img: CGImage, _ p: String) {
    guard let dest = CGImageDestinationCreateWithURL(URL(fileURLWithPath: p) as CFURL,
                                                     UTType.png.identifier as CFString, 1, nil) else { return }
    CGImageDestinationAddImage(dest, img, nil)
    CGImageDestinationFinalize(dest)
    print("zapisano \(p)")
}

func ikona(_ rozmiar: Int, tresc: CGFloat, maskowalna: Bool) -> CGImage {
    let s = CGFloat(rozmiar)
    let cs = CGColorSpace(name: CGColorSpace.sRGB)!
    let ctx = CGContext(data: nil, width: rozmiar, height: rozmiar, bitsPerComponent: 8,
                        bytesPerRow: 0, space: cs,
                        bitmapInfo: CGImageAlphaInfo.premultipliedLast.rawValue)!

    // tło: granatowy kosmos
    ctx.setFillColor(CGColor(srgbRed: 0.02, green: 0.024, blue: 0.06, alpha: 1))
    ctx.fill(CGRect(x: 0, y: 0, width: s, height: s))

    // mgławica
    let grad = CGGradient(colorsSpace: cs, colors: [
        CGColor(srgbRed: 0.42, green: 0.09, blue: 0.48, alpha: 0.85),
        CGColor(srgbRed: 0.12, green: 0.04, blue: 0.24, alpha: 0.45),
        CGColor(srgbRed: 0.02, green: 0.02, blue: 0.06, alpha: 0.0)
    ] as CFArray, locations: [0, 0.5, 1])!
    ctx.drawRadialGradient(grad, startCenter: CGPoint(x: s * 0.35, y: s * 0.7), startRadius: 0,
                           endCenter: CGPoint(x: s * 0.35, y: s * 0.7), endRadius: s * 0.85,
                           options: [])
    let grad2 = CGGradient(colorsSpace: cs, colors: [
        CGColor(srgbRed: 0.85, green: 0.32, blue: 0.12, alpha: 0.45),
        CGColor(srgbRed: 0.2, green: 0.05, blue: 0.02, alpha: 0.0)
    ] as CFArray, locations: [0, 1])!
    ctx.drawRadialGradient(grad2, startCenter: CGPoint(x: s * 0.8, y: s * 0.18), startRadius: 0,
                           endCenter: CGPoint(x: s * 0.8, y: s * 0.18), endRadius: s * 0.6,
                           options: [])

    // gwiazdy (deterministycznie)
    var seed: UInt64 = 20260824
    func rnd() -> CGFloat { seed = seed &* 6364136223846793005 &+ 1442695040888963407
                            return CGFloat((seed >> 33) % 10000) / 10000.0 }
    for _ in 0..<(rozmiar / 6) {
        let r = rnd() * s * 0.006 + s * 0.004
        ctx.setFillColor(CGColor(srgbRed: 1, green: 0.95, blue: 0.86, alpha: rnd() * 0.7 + 0.2))
        ctx.fillEllipse(in: CGRect(x: rnd() * s, y: rnd() * s, width: r, height: r))
    }

    // różowa aureola pod Maćkiem
    let aura = CGGradient(colorsSpace: cs, colors: [
        CGColor(srgbRed: 1, green: 0.24, blue: 0.65, alpha: 0.5),
        CGColor(srgbRed: 1, green: 0.24, blue: 0.65, alpha: 0.0)
    ] as CFArray, locations: [0, 1])!
    ctx.drawRadialGradient(aura, startCenter: CGPoint(x: s / 2, y: s * 0.46), startRadius: s * 0.05,
                           endCenter: CGPoint(x: s / 2, y: s * 0.46), endRadius: s * 0.46,
                           options: [])

    // Maciek
    if let m = maciek {
        let h = s * 0.74 * tresc
        let w = h * CGFloat(m.width) / CGFloat(m.height)
        ctx.draw(m, in: CGRect(x: s / 2 - w / 2, y: s * 0.5 - h * 0.42, width: w, height: h))
    }

    if !maskowalna {
        // różowa obwódka
        ctx.setStrokeColor(CGColor(srgbRed: 1, green: 0.24, blue: 0.65, alpha: 0.9))
        ctx.setLineWidth(s * 0.035)
        let m = s * 0.028
        let path = CGPath(roundedRect: CGRect(x: m, y: m, width: s - 2 * m, height: s - 2 * m),
                          cornerWidth: s * 0.14, cornerHeight: s * 0.14, transform: nil)
        ctx.addPath(path); ctx.strokePath()
    }
    return ctx.makeImage()!
}

zapisz(ikona(512, tresc: 1.0, maskowalna: false), kat + "/ikona-512.png")
zapisz(ikona(192, tresc: 1.0, maskowalna: false), kat + "/ikona-192.png")
zapisz(ikona(512, tresc: 0.68, maskowalna: true), kat + "/ikona-maskowalna-512.png")
zapisz(ikona(180, tresc: 1.0, maskowalna: false), kat + "/apple-touch-icon.png")
zapisz(ikona(64, tresc: 1.0, maskowalna: false), kat + "/favicon-64.png")
