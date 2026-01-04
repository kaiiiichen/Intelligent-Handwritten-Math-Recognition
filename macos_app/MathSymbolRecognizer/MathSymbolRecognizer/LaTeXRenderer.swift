//
//  LaTeXRenderer.swift
//  MathSymbolRecognizer
//
//  LaTeX preview rendering using Core Text and mathematical symbols
//

import SwiftUI
import AppKit
import CoreText

class LaTeXRenderer {
    static let shared = LaTeXRenderer()
    
    private init() {}
    
    /// Render LaTeX command to preview image
    func renderLatex(_ command: String, size: CGSize = CGSize(width: 40, height: 40)) -> NSImage? {
        // For now, we'll use a simple text-based rendering approach
        // In a full implementation, you might integrate with MathJax or KaTeX
        
        let displayText = convertLatexToDisplayText(command)
        return renderText(displayText, size: size)
    }
    
    /// Convert LaTeX command to displayable Unicode text where possible
    private func convertLatexToDisplayText(_ latex: String) -> String {
        // Common LaTeX to Unicode mappings
        let mappings: [String: String] = [
            // Arrows
            "\\rightarrow": "→",
            "\\leftarrow": "←",
            "\\leftrightarrow": "↔",
            "\\Rightarrow": "⇒",
            "\\Leftarrow": "⇐",
            "\\Leftrightarrow": "⇔",
            "\\implies": "⇒",
            "\\iff": "⇔",
            "\\to": "→",
            "\\mapsto": "↦",
            
            // Set theory
            "\\in": "∈",
            "\\notin": "∉",
            "\\subset": "⊂",
            "\\subseteq": "⊆",
            "\\supset": "⊃",
            "\\supseteq": "⊇",
            "\\cup": "∪",
            "\\cap": "∩",
            "\\emptyset": "∅",
            "\\varnothing": "∅",
            
            // Logic
            "\\forall": "∀",
            "\\exists": "∃",
            "\\nexists": "∄",
            "\\land": "∧",
            "\\lor": "∨",
            "\\neg": "¬",
            "\\lnot": "¬",
            
            // Relations
            "\\leq": "≤",
            "\\geq": "≥",
            "\\neq": "≠",
            "\\ne": "≠",
            "\\equiv": "≡",
            "\\approx": "≈",
            "\\sim": "∼",
            "\\simeq": "≃",
            "\\cong": "≅",
            "\\propto": "∝",
            
            // Operations
            "\\times": "×",
            "\\div": "÷",
            "\\pm": "±",
            "\\mp": "∓",
            "\\cdot": "⋅",
            "\\ast": "∗",
            "\\star": "⋆",
            "\\circ": "∘",
            "\\bullet": "•",
            
            // Calculus
            "\\int": "∫",
            "\\iint": "∬",
            "\\iiint": "∭",
            "\\oint": "∮",
            "\\sum": "∑",
            "\\prod": "∏",
            "\\coprod": "∐",
            "\\partial": "∂",
            "\\nabla": "∇",
            "\\infty": "∞",
            
            // Greek letters (lowercase)
            "\\alpha": "α",
            "\\beta": "β",
            "\\gamma": "γ",
            "\\delta": "δ",
            "\\epsilon": "ε",
            "\\varepsilon": "ε",
            "\\zeta": "ζ",
            "\\eta": "η",
            "\\theta": "θ",
            "\\vartheta": "ϑ",
            "\\iota": "ι",
            "\\kappa": "κ",
            "\\lambda": "λ",
            "\\mu": "μ",
            "\\nu": "ν",
            "\\xi": "ξ",
            "\\pi": "π",
            "\\varpi": "ϖ",
            "\\rho": "ρ",
            "\\varrho": "ϱ",
            "\\sigma": "σ",
            "\\varsigma": "ς",
            "\\tau": "τ",
            "\\upsilon": "υ",
            "\\phi": "φ",
            "\\varphi": "ϕ",
            "\\chi": "χ",
            "\\psi": "ψ",
            "\\omega": "ω",
            
            // Greek letters (uppercase)
            "\\Alpha": "Α",
            "\\Beta": "Β",
            "\\Gamma": "Γ",
            "\\Delta": "Δ",
            "\\Epsilon": "Ε",
            "\\Zeta": "Ζ",
            "\\Eta": "Η",
            "\\Theta": "Θ",
            "\\Iota": "Ι",
            "\\Kappa": "Κ",
            "\\Lambda": "Λ",
            "\\Mu": "Μ",
            "\\Nu": "Ν",
            "\\Xi": "Ξ",
            "\\Pi": "Π",
            "\\Rho": "Ρ",
            "\\Sigma": "Σ",
            "\\Tau": "Τ",
            "\\Upsilon": "Υ",
            "\\Phi": "Φ",
            "\\Chi": "Χ",
            "\\Psi": "Ψ",
            "\\Omega": "Ω",
            
            // Other symbols
            "\\aleph": "ℵ",
            "\\hbar": "ℏ",
            "\\ell": "ℓ",
            "\\wp": "℘",
            "\\Re": "ℜ",
            "\\Im": "ℑ",
            "\\angle": "∠",
            "\\triangle": "△",
            "\\square": "□",
            "\\diamond": "◊",
            "\\clubsuit": "♣",
            "\\diamondsuit": "♦",
            "\\heartsuit": "♥",
            "\\spadesuit": "♠"
        ]
        
        // Try exact match first
        if let unicode = mappings[latex] {
            return unicode
        }
        
        // Handle common patterns
        var result = latex
        
        // Remove backslash for simple commands
        if result.hasPrefix("\\") && result.count > 1 {
            let withoutBackslash = String(result.dropFirst())
            if let unicode = mappings[latex] {
                return unicode
            }
            // For unknown commands, show without backslash
            result = withoutBackslash
        }
        
        return result
    }
    
    /// Render text to image with mathematical font
    private func renderText(_ text: String, size: CGSize) -> NSImage? {
        let image = NSImage(size: size)
        
        image.lockFocus()
        defer { image.unlockFocus() }
        
        // Clear background
        NSColor.clear.setFill()
        NSRect(origin: .zero, size: size).fill()
        
        // Set up text attributes with mathematical font
        let fontSize: CGFloat = min(size.width, size.height) * 0.7
        let font = NSFont(name: "STIXTwoMath-Regular", size: fontSize) ?? 
                   NSFont(name: "STIX", size: fontSize) ??
                   NSFont.systemFont(ofSize: fontSize)
        
        let attributes: [NSAttributedString.Key: Any] = [
            .font: font,
            .foregroundColor: NSColor.labelColor
        ]
        
        let attributedString = NSAttributedString(string: text, attributes: attributes)
        
        // Calculate centered position
        let textSize = attributedString.size()
        let x = (size.width - textSize.width) / 2
        let y = (size.height - textSize.height) / 2
        let rect = NSRect(x: x, y: y, width: textSize.width, height: textSize.height)
        
        attributedString.draw(in: rect)
        
        return image
    }
    
    /// Generate preview for multiple LaTeX candidates
    func renderCandidates(_ candidates: [String], size: CGSize = CGSize(width: 40, height: 40)) -> [String: NSImage] {
        var previews: [String: NSImage] = [:]
        
        for candidate in candidates {
            if let preview = renderLatex(candidate, size: size) {
                previews[candidate] = preview
            }
        }
        
        return previews
    }
}

// MARK: - SwiftUI Integration

struct LaTeXPreview: View {
    let command: String
    let size: CGSize
    @State private var previewImage: NSImage?
    
    init(_ command: String, size: CGSize = CGSize(width: 40, height: 40)) {
        self.command = command
        self.size = size
    }
    
    var body: some View {
        Group {
            if let image = previewImage {
                Image(nsImage: image)
                    .resizable()
                    .aspectRatio(contentMode: .fit)
            } else {
                Rectangle()
                    .fill(Color.gray.opacity(0.2))
                    .overlay(
                        Text("?")
                            .font(.caption)
                            .foregroundColor(.secondary)
                    )
            }
        }
        .frame(width: size.width, height: size.height)
        .onAppear {
            generatePreview()
        }
        .onChange(of: command) { _ in
            generatePreview()
        }
    }
    
    private func generatePreview() {
        DispatchQueue.global(qos: .userInitiated).async {
            let preview = LaTeXRenderer.shared.renderLatex(command, size: size)
            DispatchQueue.main.async {
                self.previewImage = preview
            }
        }
    }
}