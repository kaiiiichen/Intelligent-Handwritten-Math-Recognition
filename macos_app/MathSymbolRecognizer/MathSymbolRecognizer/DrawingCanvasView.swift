//
//  DrawingCanvasView.swift
//  MathSymbolRecognizer
//
//  High-performance drawing canvas for stroke capture
//

import SwiftUI
import AppKit

struct DrawingCanvasView: NSViewRepresentable {
    @ObservedObject var viewModel: RecognitionViewModel
    
    func makeNSView(context: Context) -> DrawingCanvas {
        let canvas = DrawingCanvas()
        canvas.delegate = viewModel
        viewModel.canvas = canvas
        return canvas
    }
    
    func updateNSView(_ nsView: DrawingCanvas, context: Context) {
        if viewModel.shouldClearCanvas {
            nsView.clear()
            viewModel.shouldClearCanvas = false
        }
    }
}

class DrawingCanvas: NSView {
    weak var delegate: DrawingCanvasDelegate?
    
    private var currentPath: NSBezierPath?
    private var paths: [NSBezierPath] = []
    private var isDrawing = false
    
    override init(frame frameRect: NSRect) {
        super.init(frame: frameRect)
        setupCanvas()
    }
    
    required init?(coder: NSCoder) {
        super.init(coder: coder)
        setupCanvas()
    }
    
    private func setupCanvas() {
        wantsLayer = true
        layer?.backgroundColor = NSColor.white.cgColor
    }
    
    override func mouseDown(with event: NSEvent) {
        let point = convert(event.locationInWindow, from: nil)
        currentPath = NSBezierPath()
        currentPath?.move(to: point)
        isDrawing = true
    }
    
    override func mouseDragged(with event: NSEvent) {
        guard isDrawing, let path = currentPath else { return }
        let point = convert(event.locationInWindow, from: nil)
        path.line(to: point)
        needsDisplay = true
    }
    
    override func mouseUp(with event: NSEvent) {
        guard isDrawing, let path = currentPath else { return }
        paths.append(path)
        currentPath = nil
        isDrawing = false
        needsDisplay = true
        
        // Notify delegate that drawing changed
        delegate?.drawingDidChange()
    }
    
    override func draw(_ dirtyRect: NSRect) {
        super.draw(dirtyRect)
        
        // Draw subtle grid for better drawing guidance (optional)
        if UserPreferences.shared.autoRecognitionEnabled {
            drawGrid()
        }
        
        // Draw all paths with thicker lines for better recognition
        NSColor.black.setStroke()
        for path in paths {
            path.lineWidth = 10.0  // Increased to make lines thicker for better recognition
            path.lineCapStyle = .round
            path.lineJoinStyle = .round
            path.stroke()
        }
        
        // Draw current path with slight transparency to show it's being drawn
        if let currentPath = currentPath {
            NSColor.black.withAlphaComponent(0.8).setStroke()
            currentPath.lineWidth = 10.0  // Increased to make lines thicker for better recognition
            currentPath.lineCapStyle = .round
            currentPath.lineJoinStyle = .round
            currentPath.stroke()
        }
    }
    
    private func drawGrid() {
        // Draw a subtle grid to help with symbol alignment
        NSColor.gray.withAlphaComponent(0.1).setStroke()
        
        let gridSpacing: CGFloat = 20
        let gridPath = NSBezierPath()
        gridPath.lineWidth = 0.5
        
        // Vertical lines
        var x: CGFloat = 0
        while x <= bounds.width {
            gridPath.move(to: NSPoint(x: x, y: 0))
            gridPath.line(to: NSPoint(x: x, y: bounds.height))
            x += gridSpacing
        }
        
        // Horizontal lines
        var y: CGFloat = 0
        while y <= bounds.height {
            gridPath.move(to: NSPoint(x: 0, y: y))
            gridPath.line(to: NSPoint(x: bounds.width, y: y))
            y += gridSpacing
        }
        
        gridPath.stroke()
    }
    
    func clear() {
        paths.removeAll()
        currentPath = nil
        needsDisplay = true
    }
    
    func getImage() -> NSImage? {
        // Check if we have any paths to draw
        guard !paths.isEmpty || currentPath != nil else {
            print("⚠️ Warning: Canvas is empty (no paths to draw)")
            return nil
        }
        
        // Check if bounds are valid
        guard bounds.width > 0 && bounds.height > 0 else {
            print("⚠️ Warning: Canvas bounds are invalid: \(bounds)")
            return nil
        }
        
        let width = Int(bounds.width)
        let height = Int(bounds.height)
        
        // Create bitmap representation manually to ensure we capture the paths
        guard let rep = NSBitmapImageRep(
            bitmapDataPlanes: nil,
            pixelsWide: width,
            pixelsHigh: height,
            bitsPerSample: 8,
            samplesPerPixel: 4, // RGBA
            hasAlpha: true,
            isPlanar: false,
            colorSpaceName: .calibratedRGB,
            bytesPerRow: width * 4,
            bitsPerPixel: 32
        ) else {
            print("⚠️ Warning: Could not create bitmap representation")
            return nil
        }
        
        // Draw into the bitmap representation
        NSGraphicsContext.saveGraphicsState()
        NSGraphicsContext.current = NSGraphicsContext(bitmapImageRep: rep)
        
        // Fill white background
        NSColor.white.setFill()
        bounds.fill()
        
        // Draw all paths in black with thicker lines
        NSColor.black.setStroke()
        for path in paths {
            path.lineWidth = 10.0  // Increased to make lines thicker for better recognition
            path.lineCapStyle = .round
            path.lineJoinStyle = .round
            path.stroke()
        }
        
        // Draw current path if exists
        if let currentPath = currentPath {
            currentPath.lineWidth = 10.0  // Increased to make lines thicker for better recognition
            currentPath.lineCapStyle = .round
            currentPath.lineJoinStyle = .round
            currentPath.stroke()
        }
        
        NSGraphicsContext.restoreGraphicsState()
        
        // Create image from the representation
        let image = NSImage(size: bounds.size)
        image.addRepresentation(rep)
        
        print("✓ Created image from canvas: \(image.size), paths: \(paths.count)")
        print("  Image format: \(rep.samplesPerPixel) samples/pixel, \(rep.bitsPerPixel) bits/pixel")
        
        // Debug: Calculate image hash to verify different symbols produce different images
        if let tiffData = image.tiffRepresentation {
            let hash = tiffData.hashValue
            print("  📊 Image hash: \(hash) (for debugging - different symbols should have different hashes)")
        }
        
        return image
    }
}

protocol DrawingCanvasDelegate: AnyObject {
    func drawingDidChange()
}

