//
//  ImageExtensions.swift
//  MathSymbolRecognizer
//
//  Image processing utilities
//

import AppKit
import CoreVideo
import Foundation

extension NSImage {
    /// Crop to content bounding box with padding, then resize
    func croppedAndResized(to size: NSSize, padding: CGFloat = 4.0) -> NSImage? {
        // First, find the bounding box of non-white content
        guard let sourceRep = self.representations.first as? NSBitmapImageRep,
              let sourceData = sourceRep.bitmapData else {
            return nil
        }
        
        let sourceWidth = sourceRep.pixelsWide
        let sourceHeight = sourceRep.pixelsHigh
        let bytesPerRow = sourceRep.bytesPerRow
        let bytesPerPixel = sourceRep.bitsPerPixel / 8
        
        // Find bounding box of non-white pixels (assuming white background = 255)
        var minX = sourceWidth
        var maxX = 0
        var minY = sourceHeight
        var maxY = 0
        
        for y in 0..<sourceHeight {
            for x in 0..<sourceWidth {
                let offset = y * bytesPerRow + x * bytesPerPixel
                // Check if pixel is not white (RGB all > 240 means white)
                let r = sourceData[offset]
                let g = sourceData[offset + 1]
                let b = sourceData[offset + 2]
                
                // If pixel is not white (has content)
                if r < 240 || g < 240 || b < 240 {
                    minX = min(minX, x)
                    maxX = max(maxX, x)
                    minY = min(minY, y)
                    maxY = max(maxY, y)
                }
            }
        }
        
        // If no content found, return nil
        guard maxX >= minX && maxY >= minY else {
            return nil
        }
        
        // Add padding
        let paddingInt = Int(padding)
        minX = max(0, minX - paddingInt)
        minY = max(0, minY - paddingInt)
        maxX = min(sourceWidth - 1, maxX + paddingInt)
        maxY = min(sourceHeight - 1, maxY + paddingInt)
        
        let cropWidth = maxX - minX + 1
        let cropHeight = maxY - minY + 1
        
        // Crop the image
        guard let croppedCGImage = sourceRep.cgImage?.cropping(to: CGRect(
            x: minX,
            y: minY,
            width: cropWidth,
            height: cropHeight
        )) else {
            return nil
        }
        
        // Now resize the cropped image
        let croppedImage = NSImage(cgImage: croppedCGImage, size: NSSize(width: cropWidth, height: cropHeight))
        return croppedImage.resized(to: size)
    }
    
    func resized(to size: NSSize) -> NSImage? {
        // Create a bitmap representation with exact pixel dimensions
        let width = Int(size.width)
        let height = Int(size.height)
        
        guard width > 0 && height > 0 else {
            return nil
        }
        
        // Get source bitmap
        guard let sourceRep = self.representations.first as? NSBitmapImageRep else {
            return nil
        }
        
        let sourceWidth = sourceRep.pixelsWide
        let sourceHeight = sourceRep.pixelsHigh
        
        guard sourceWidth > 0 && sourceHeight > 0 else {
            return nil
        }
        
        // Create destination bitmap
        guard let destRep = NSBitmapImageRep(
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
            return nil
        }
        
        // Use Core Graphics for nearest-neighbor scaling (no anti-aliasing)
        guard let sourceCGImage = sourceRep.cgImage else {
            return nil
        }
        
        NSGraphicsContext.saveGraphicsState()
        guard let context = NSGraphicsContext(bitmapImageRep: destRep) else {
            NSGraphicsContext.restoreGraphicsState()
            return nil
        }
        NSGraphicsContext.current = context
        
        // Set interpolation quality to nearest neighbor (no anti-aliasing)
        context.cgContext.interpolationQuality = .none
        
        // Draw with nearest neighbor scaling
        context.cgContext.draw(sourceCGImage, in: CGRect(x: 0, y: 0, width: width, height: height))
        
        NSGraphicsContext.restoreGraphicsState()
        
        // Create new image with the bitmap representation
        let newImage = NSImage(size: size)
        newImage.addRepresentation(destRep)
        return newImage
    }
    
    func toGrayscale() -> NSImage? {
        // Get bitmap representation from the image
        guard let tiffData = self.tiffRepresentation,
              let sourceBitmap = NSBitmapImageRep(data: tiffData) else {
            print("  ❌ Failed to get bitmap representation from image")
            return nil
        }
        
        let targetWidth = sourceBitmap.pixelsWide
        let targetHeight = sourceBitmap.pixelsHigh
        
        guard targetWidth > 0 && targetHeight > 0 else {
            print("  ❌ Invalid bitmap dimensions: \(targetWidth)x\(targetHeight)")
            return nil
        }
        
        // Create a grayscale bitmap representation
        guard let grayRep = NSBitmapImageRep(
            bitmapDataPlanes: nil,
            pixelsWide: targetWidth,
            pixelsHigh: targetHeight,
            bitsPerSample: 8,
            samplesPerPixel: 1,
            hasAlpha: false,
            isPlanar: false,
            colorSpaceName: .calibratedWhite,
            bytesPerRow: targetWidth,
            bitsPerPixel: 8
        ) else {
            print("  ❌ Failed to create grayscale bitmap representation")
            return nil
        }
        
        // Convert RGB to grayscale manually
        guard let sourceData = sourceBitmap.bitmapData,
              let grayData = grayRep.bitmapData else {
            print("  ❌ Failed to get bitmap data pointers")
            return nil
        }
        
        let sourceBytesPerRow = sourceBitmap.bytesPerRow
        let sourceSamplesPerPixel = sourceBitmap.samplesPerPixel  // Usually 4 for RGBA, 3 for RGB
        let sourceBytesPerPixel = sourceBitmap.bitsPerPixel / 8
        
        print("  📊 Source bitmap: \(targetWidth)x\(targetHeight), \(sourceSamplesPerPixel) samples/pixel, \(sourceBytesPerPixel) bytes/pixel")
        
        // Sample a few pixels to verify format
        var samplePixels: [(r: UInt8, g: UInt8, b: UInt8, gray: UInt8, inverted: UInt8)] = []
        var pixelStats = (min: UInt8(255), max: UInt8(0), backgroundCount: 0, symbolCount: 0)
        
        for y in 0..<targetHeight {
            for x in 0..<targetWidth {
                let sourceOffset = y * sourceBytesPerRow + x * sourceBytesPerPixel
                let grayOffset = y * targetWidth + x
                
                // Safety check
                guard sourceOffset + sourceBytesPerPixel <= sourceBytesPerRow * targetHeight,
                      grayOffset < targetWidth * targetHeight else {
                    continue
                }
                
                // Get RGB values
                // For RGBA: [R, G, B, A] at offset
                // For RGB: [R, G, B] at offset
                let r = sourceData[sourceOffset]
                let g = sourceData[sourceOffset + 1]
                let b = sourceData[sourceOffset + 2]
                
                // Convert to grayscale using standard luminance weights
                // Y = 0.299*R + 0.587*G + 0.114*B
                let gray = UInt8((Int(r) * 299 + Int(g) * 587 + Int(b) * 114) / 1000)
                
                // CRITICAL: Model was trained with THRESH_BINARY_INV
                // Training data: BLACK background (0) with WHITE symbols (255)
                // Our canvas: WHITE background (255) with BLACK symbols (0)
                // Solution: INVERT the image to match training format
                let invertedGray = 255 - gray
                grayData[grayOffset] = invertedGray
                
                // Track statistics
                pixelStats.min = min(pixelStats.min, invertedGray)
                pixelStats.max = max(pixelStats.max, invertedGray)
                if invertedGray < 128 {
                    pixelStats.backgroundCount += 1
                } else {
                    pixelStats.symbolCount += 1
                }
                
                // Sample first few pixels for debugging
                if samplePixels.count < 5 && (x < 3 && y < 3) {
                    samplePixels.append((r: r, g: g, b: b, gray: gray, inverted: invertedGray))
                }
            }
        }
        
        if !samplePixels.isEmpty {
            print("  📊 Sample pixels:")
            for (i, pixel) in samplePixels.enumerated() {
                print("    [\(i)] RGB(\(pixel.r), \(pixel.g), \(pixel.b)) -> Gray: \(pixel.gray) -> Inverted: \(pixel.inverted)")
            }
        }
        
        print("  📊 Grayscale stats: min=\(pixelStats.min), max=\(pixelStats.max)")
        print("  📊 Pixel distribution: background (dark) pixels=\(pixelStats.backgroundCount), symbol (bright) pixels=\(pixelStats.symbolCount)")
        print("  ✓ Grayscale conversion complete (inverted for model compatibility)")
        
        let grayImage = NSImage(size: NSSize(width: targetWidth, height: targetHeight))
        grayImage.addRepresentation(grayRep)
        
        // Apply morphological dilation to thicken lines
        // This is critical because mouse-drawn lines are very thin
        // Using radius=2 for slightly thicker lines
        return grayImage.dilated(radius: 2)
    }
    
    /// Apply morphological dilation to thicken white pixels (symbols)
    /// This helps with thin mouse-drawn lines that become too thin after scaling
    func dilated(radius: Int = 1) -> NSImage? {
        guard radius > 0 else { return self }
        
        guard let tiffData = self.tiffRepresentation,
              let sourceBitmap = NSBitmapImageRep(data: tiffData) else {
            return nil
        }
        
        let width = sourceBitmap.pixelsWide
        let height = sourceBitmap.pixelsHigh
        
        guard let sourceData = sourceBitmap.bitmapData else {
            return nil
        }
        
        // Create output bitmap
        guard let outputRep = NSBitmapImageRep(
            bitmapDataPlanes: nil,
            pixelsWide: width,
            pixelsHigh: height,
            bitsPerSample: 8,
            samplesPerPixel: 1,
            hasAlpha: false,
            isPlanar: false,
            colorSpaceName: .calibratedWhite,
            bytesPerRow: width,
            bitsPerPixel: 8
        ), let outputData = outputRep.bitmapData else {
            return nil
        }
        
        // Copy source to output first
        for y in 0..<height {
            for x in 0..<width {
                let offset = y * width + x
                outputData[offset] = sourceData[offset]
            }
        }
        
        // Apply dilation: for each white pixel (symbol), set neighbors to white
        // Use two-pass: first identify white pixels, then dilate
        for y in 0..<height {
            for x in 0..<width {
                let offset = y * width + x
                let pixelValue = sourceData[offset]
                
                // If this is a white pixel (symbol), dilate it
                if pixelValue > 128 {  // White pixel (symbol after inversion)
                    // Set neighbors within radius to white
                    for dy in -radius...radius {
                        for dx in -radius...radius {
                            // Skip center pixel (already white)
                            if dx == 0 && dy == 0 { continue }
                            
                            let nx = x + dx
                            let ny = y + dy
                            
                            // Check bounds
                            if nx >= 0 && nx < width && ny >= 0 && ny < height {
                                let neighborOffset = ny * width + nx
                                // Set neighbor to white (dilate)
                                outputData[neighborOffset] = 255
                            }
                        }
                    }
                }
            }
        }
        
        let dilatedImage = NSImage(size: NSSize(width: width, height: height))
        dilatedImage.addRepresentation(outputRep)
        return dilatedImage
    }
    
    func toPixelBuffer() -> CVPixelBuffer? {
        // Use the image's actual size, not the representation size
        let width = Int(self.size.width)
        let height = Int(self.size.height)
        
        guard width > 0 && height > 0 else {
            return nil
        }
        
        // Get bitmap representation
        guard let tiffData = self.tiffRepresentation,
              let bitmapImage = NSBitmapImageRep(data: tiffData) else {
            return nil
        }
        
        // Ensure the bitmap matches the expected size
        let bitmapWidth = bitmapImage.pixelsWide
        let bitmapHeight = bitmapImage.pixelsHigh
        
        // If sizes don't match, we need to create a new representation
        let finalBitmap: NSBitmapImageRep
        if bitmapWidth != width || bitmapHeight != height {
            // Create a new bitmap with correct size
            finalBitmap = NSBitmapImageRep(
                bitmapDataPlanes: nil,
                pixelsWide: width,
                pixelsHigh: height,
                bitsPerSample: 8,
                samplesPerPixel: 1,
                hasAlpha: false,
                isPlanar: false,
                colorSpaceName: .calibratedWhite,
                bytesPerRow: width,
                bitsPerPixel: 8
            )!
            
            // Draw the image into the correctly sized bitmap
            NSGraphicsContext.saveGraphicsState()
            NSGraphicsContext.current = NSGraphicsContext(bitmapImageRep: finalBitmap)
            self.draw(in: NSRect(x: 0, y: 0, width: width, height: height),
                      from: NSRect(origin: .zero, size: self.size),
                      operation: .copy,
                      fraction: 1.0)
            NSGraphicsContext.restoreGraphicsState()
        } else {
            finalBitmap = bitmapImage
        }
        
        var pixelBuffer: CVPixelBuffer?
        let status = CVPixelBufferCreate(
            kCFAllocatorDefault,
            width,
            height,
            kCVPixelFormatType_OneComponent8,
            nil,
            &pixelBuffer
        )
        
        guard status == kCVReturnSuccess, let buffer = pixelBuffer else {
            return nil
        }
        
        CVPixelBufferLockBaseAddress(buffer, [])
        defer { CVPixelBufferUnlockBaseAddress(buffer, []) }
        
        guard let baseAddress = CVPixelBufferGetBaseAddress(buffer) else {
            return nil
        }
        
        let bytesPerRow = CVPixelBufferGetBytesPerRow(buffer)
        guard let bitmapData = finalBitmap.bitmapData else {
            return nil
        }
        
        for y in 0..<height {
            let srcRow = bitmapData.advanced(by: y * finalBitmap.bytesPerRow)
            let dstRow = baseAddress.assumingMemoryBound(to: UInt8.self).advanced(by: y * bytesPerRow)
            memcpy(dstRow, srcRow, width)
        }
        
        return buffer
    }
}

