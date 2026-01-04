//
//  RecognitionViewModel.swift
//  MathSymbolRecognizer
//
//  View model for symbol recognition
//

import SwiftUI
import CoreML
import AppKit
import Accelerate
import Combine

class RecognitionViewModel: ObservableObject, DrawingCanvasDelegate {
    @Published var suggestions: [Suggestion] = []
    @Published var isProcessing = false
    @Published var shouldClearCanvas = false
    
    private var mlModel: MLModel?
    private let imageSize: Int = 64
    private let autoRecognitionTimer = AutoRecognitionTimer()
    
    init() {
        print("🚀 Initializing RecognitionViewModel...")
        loadModel()
        if mlModel == nil {
            print("⚠️ Warning: Model not loaded. Recognition will not work.")
        }
    }
    
    func drawingDidChange() {
        // Auto-recognition: trigger recognition after user stops drawing
        if UserPreferences.shared.autoRecognitionEnabled {
            autoRecognitionTimer.schedule(delay: UserPreferences.shared.autoRecognitionDelay) { [weak self] in
                DispatchQueue.main.async {
                    self?.recognizeSymbol()
                }
            }
        }
    }
    
    func clearDrawing() {
        shouldClearCanvas = true
        suggestions.removeAll()
        autoRecognitionTimer.cancel() // Cancel any pending auto-recognition
    }
    
    func selectSuggestion(_ suggestion: Suggestion) {
        // Record user's choice
        UserPreferences.shared.recordChoice(symbolId: suggestion.symbolId, latexCommand: suggestion.latexCommand)
        
        // Copy to clipboard
        let pasteboard = NSPasteboard.general
        pasteboard.clearContents()
        pasteboard.setString(suggestion.latexCommand, forType: .string)
        
        // Provide haptic feedback (if available)
        NSHapticFeedbackManager.defaultPerformer.perform(.alignment, performanceTime: .now)
    }
    
    func selectSuggestionByIndex(_ index: Int) {
        guard index < suggestions.count else { return }
        selectSuggestion(suggestions[index])
    }
    
    func recognizeSymbol() {
        print("🔍 Starting recognition...")
        
        guard let canvas = canvas else {
            print("❌ Error: Canvas is nil")
            return
        }
        
        guard let image = canvas.getImage() else {
            print("❌ Error: Could not get image from canvas")
            return
        }
        
        print("✓ Got image from canvas: \(image.size)")
        
        // Check if image has content (not empty)
        if image.size.width == 0 || image.size.height == 0 {
            print("⚠️ Warning: Image is empty")
            return
        }
        
        isProcessing = true
        
        Task { @MainActor in
            defer { self.isProcessing = false }
            
            print("📸 Preprocessing image...")
            // Preprocess image
            guard let preprocessedImage = preprocessImage(image) else {
                print("❌ Error: Image preprocessing failed")
                return
            }
            
            print("✓ Image preprocessed successfully")
            print("🤖 Running inference...")
            
            // Run inference
            guard let predictions = runInference(preprocessedImage) else {
                print("❌ Error: Inference failed")
                return
            }
            
            print("✓ Inference completed. Got \(predictions.count) predictions")
            
            // Get top-k symbol predictions
            let topK = getTopK(predictions, k: 5)
            print("📊 Top-5 symbol predictions (model indices):")
            for (rank, (modelIndex, confidence)) in topK.enumerated() {
                let symbolId = SymbolMapping.shared.getSymbolId(fromIndex: modelIndex) ?? modelIndex
                let latex = SymbolMapping.shared.getLatexCommand(fromIndex: modelIndex)
                print("  \(rank + 1). Model Index \(modelIndex) -> Symbol ID \(symbolId) -> \(latex): \(confidence * 100)%")
            }
            
            // Apply mathematical priority ranking
            // Formula: combined_score = vision_weight * vision_confidence + math_weight * math_priority
            let visionWeight: Float = 0.6
            let mathWeight: Float = 0.4
            
            var allCandidates: [(latex: String, symbolId: Int, visionConf: Float, mathPriority: Float, combinedScore: Float)] = []
            
            // Collect candidates from top-k symbols
            for (modelIndex, visionConf) in topK {
                let symbolId = SymbolMapping.shared.getSymbolId(fromIndex: modelIndex) ?? modelIndex
                let candidates = SymbolMapping.shared.getRankedCandidates(fromIndex: modelIndex)
                
                if candidates.isEmpty {
                    // Fallback: use simple mapping
                    let latex = SymbolMapping.shared.getLatexCommand(fromIndex: modelIndex)
                    let combinedScore = visionConf * visionWeight + 0.5 * mathWeight  // Default math priority = 0.5
                    allCandidates.append((latex: latex, symbolId: symbolId, visionConf: visionConf, mathPriority: 0.5, combinedScore: combinedScore))
                } else {
                    // Add all candidates for this symbol
                    for candidate in candidates.prefix(3) {  // Limit to top 3 candidates per symbol
                        let combinedScore = visionConf * visionWeight + candidate.mathPriority * mathWeight
                        allCandidates.append((latex: candidate.command, symbolId: symbolId, visionConf: visionConf, mathPriority: candidate.mathPriority, combinedScore: combinedScore))
                    }
                }
            }
            
            // Sort by combined score (descending)
            allCandidates.sort { $0.combinedScore > $1.combinedScore }
            
            // Take top 5
            let topCandidates = Array(allCandidates.prefix(5))
            
            print("📊 Top-5 ranked candidates (with math priority):")
            for (rank, cand) in topCandidates.enumerated() {
                print("  \(rank + 1). \(cand.latex) (vision: \(cand.visionConf * 100)%, math: \(cand.mathPriority), combined: \(cand.combinedScore))")
            }
            
            // Convert to suggestions with "last chosen" markers
            self.suggestions = topCandidates.map { cand in
                let isLastChosen = UserPreferences.shared.getLastChoice(symbolId: cand.symbolId) == cand.latex
                return Suggestion(
                    symbolId: cand.symbolId,
                    latexCommand: cand.latex,
                    confidence: cand.combinedScore,  // Use combined score as confidence
                    preview: nil, // LaTeX preview will be generated by LaTeXPreview view
                    isLastChosen: isLastChosen,
                    context: nil, // TODO: Add context from semantic engine
                    description: nil // TODO: Add description from semantic engine
                )
            }
            
            print("✅ Recognition complete. Found \(self.suggestions.count) suggestions")
        }
    }
    
    // Canvas reference will be set by DrawingCanvasView
    weak var canvas: DrawingCanvas?
    
    private func loadModel() {
        print("📦 Loading CoreML model...")
        
        // Try multiple possible locations and formats
        var modelURL: URL?
        
        // First try: .mlmodelc (compiled model - most common in bundles)
        if let url = Bundle.main.url(forResource: "best_model", withExtension: "mlmodelc") {
            modelURL = url
            print("  ✓ Found compiled model (.mlmodelc) at: \(url.path)")
        }
        // Second try: .mlpackage (source package)
        else if let url = Bundle.main.url(forResource: "best_model", withExtension: "mlpackage") {
            modelURL = url
            print("  ✓ Found model package (.mlpackage) at: \(url.path)")
        }
        // Third try: .mlmodel (single file model)
        else if let url = Bundle.main.url(forResource: "best_model", withExtension: "mlmodel") {
            modelURL = url
            print("  ✓ Found model (.mlmodel) at: \(url.path)")
        }
        // Fourth try: without extension
        else if let url = Bundle.main.url(forResource: "best_model", withExtension: nil) {
            modelURL = url
            print("  ✓ Found model (no extension) at: \(url.path)")
        }
        // Last resort: check all resources
        else {
            print("  ⚠️ Model not found in main bundle")
            print("  📂 Checking bundle resources...")
            if let resourcePath = Bundle.main.resourcePath {
                print("  Resource path: \(resourcePath)")
                let fileManager = FileManager.default
                if let files = try? fileManager.contentsOfDirectory(atPath: resourcePath) {
                    print("  Files in bundle:")
                    for file in files.filter({ $0.contains("model") || $0.contains("mlpackage") || $0.contains("mlmodelc") }) {
                        print("    - \(file)")
                    }
                }
            }
        }
        
        guard let url = modelURL else {
            print("  ❌ Error: Could not find CoreML model in bundle")
            print("  💡 Make sure 'best_model.mlpackage' or 'best_model.mlmodelc' is added to the target's 'Copy Bundle Resources'")
            return
        }
        
        do {
            print("  📥 Loading model from: \(url.path)")
            mlModel = try MLModel(contentsOf: url)
            print("  ✅ CoreML model loaded successfully!")
            
            // Print model info
            if let model = mlModel {
                print("  📊 Model info:")
                print("    Inputs: \(model.modelDescription.inputDescriptionsByName.keys.joined(separator: ", "))")
                print("    Outputs: \(model.modelDescription.outputDescriptionsByName.keys.joined(separator: ", "))")
            }
        } catch {
            print("  ❌ Error loading CoreML model: \(error)")
            print("  Error details: \(error.localizedDescription)")
        }
    }
    
    private func preprocessImage(_ image: NSImage) -> MLMultiArray? {
        print("  Resizing image to \(imageSize)x\(imageSize)...")
        print("  Original image size: \(image.size)")
        
        // Crop to content bounding box and resize to 64x64
        // This ensures the symbol fills the image instead of being tiny
        let resized: NSImage
        if let cropped = image.croppedAndResized(to: NSSize(width: imageSize, height: imageSize), padding: 4.0) {
            resized = cropped
            print("  ✓ Image cropped and resized to: \(resized.size)")
        } else {
            // Fallback to simple resize if cropping fails
            guard let simpleResized = image.resized(to: NSSize(width: imageSize, height: imageSize)) else {
                print("  ❌ Failed to resize image")
                return nil
            }
            resized = simpleResized
            print("  ✓ Image resized to: \(resized.size) (simple resize, no crop)")
        }
        
        // Convert to grayscale
        print("  Converting to grayscale...")
        guard let grayscale = resized.toGrayscale() else {
            print("  ❌ Failed to convert to grayscale")
            return nil
        }
        print("  ✓ Converted to grayscale. Size: \(grayscale.size)")
        
        // Convert to MLMultiArray
        print("  Converting to pixel buffer...")
        guard let pixelBuffer = grayscale.toPixelBuffer() else {
            print("  ❌ Failed to convert to pixel buffer")
            return nil
        }
        let pixelBufferWidth = CVPixelBufferGetWidth(pixelBuffer)
        let pixelBufferHeight = CVPixelBufferGetHeight(pixelBuffer)
        print("  ✓ Converted to pixel buffer. Size: \(pixelBufferWidth)x\(pixelBufferHeight)")
        
        // Create MLMultiArray: (1, 1, 64, 64)
        let shape = [1, 1, imageSize, imageSize].map { NSNumber(value: $0) }
        guard let array = try? MLMultiArray(shape: shape, dataType: .float32) else {
            return nil
        }
        
        // Copy pixel data
        CVPixelBufferLockBaseAddress(pixelBuffer, .readOnly)
        defer { CVPixelBufferUnlockBaseAddress(pixelBuffer, .readOnly) }
        
        guard let baseAddress = CVPixelBufferGetBaseAddress(pixelBuffer) else {
            return nil
        }
        
        let bytesPerRow = CVPixelBufferGetBytesPerRow(pixelBuffer)
        let width = CVPixelBufferGetWidth(pixelBuffer)
        let height = CVPixelBufferGetHeight(pixelBuffer)
        
        // Ensure dimensions match expected size
        guard width == imageSize && height == imageSize else {
            print("  ❌ Error: Image size mismatch. Expected \(imageSize)x\(imageSize), got \(width)x\(height)")
            return nil
        }
        print("  ✓ Pixel buffer dimensions: \(width)x\(height)")
        
        // For MLMultiArray shape [1, 1, 64, 64], use multi-dimensional indexing
        // Index format: [batch, channel, height, width] = [0, 0, y, x]
        print("  Copying pixel data to MLMultiArray...")
        var pixelCount = 0
        // Debug: check pixel value range
        var minVal: UInt8 = 255
        var maxVal: UInt8 = 0
        var nonZeroCount = 0
        
        for y in 0..<imageSize {
            for x in 0..<imageSize {
                let pixelOffset = y * bytesPerRow + x
                guard pixelOffset < bytesPerRow * height else {
                    continue // Safety check
                }
                var pixelValue = baseAddress.assumingMemoryBound(to: UInt8.self)[pixelOffset]
                
                // Track statistics (before normalization)
                minVal = min(minVal, pixelValue)
                maxVal = max(maxVal, pixelValue)
                if pixelValue > 10 {  // Consider non-zero if > threshold
                    nonZeroCount += 1
                }
                
                // CRITICAL: Model was trained with Normalize(mean=[0.5], std=[0.5])
                // This transforms [0, 1] -> [-1, 1] using: (x - 0.5) / 0.5 = 2x - 1
                // Step 1: Normalize to [0, 1] range
                // After inversion in toGrayscale():
                // - pixelValue = 0 means black background (training format)
                // - pixelValue = 255 means white symbol (training format)
                let normalized01 = Float(pixelValue) / 255.0
                // Step 2: Apply same normalization as training: (x - 0.5) / 0.5 = 2x - 1
                let normalizedValue = 2.0 * normalized01 - 1.0
                
                // Use multi-dimensional index: [batch=0, channel=0, y, x]
                // MLMultiArray requires [NSNumber] for indexing
                let multiIndex = [0, 0, y, x].map { NSNumber(value: $0) }
                array[multiIndex] = NSNumber(value: normalizedValue)
                pixelCount += 1
            }
        }
        
        // Debug: Check normalized value range and calculate input hash
        var normalizedMin: Float = 1.0
        var normalizedMax: Float = -1.0
        var inputHash: Int = 0
        
        // Sample some pixels for debugging
        for y in 0..<min(5, imageSize) {
            for x in 0..<min(5, imageSize) {
                let multiIndex = [0, 0, y, x].map { NSNumber(value: $0) }
                let val = Float(truncating: array[multiIndex])
                normalizedMin = min(normalizedMin, val)
                normalizedMax = max(normalizedMax, val)
            }
        }
        
        // CRITICAL DEBUG: Print actual pixel values at key positions
        // Since image is binary (only black/white), values should be -1.0 (black) or 1.0 (white)
        let debugPositions: [(Int, Int)] = [
            (16, 16), (16, 32), (16, 48),  // Top row
            (32, 16), (32, 32), (32, 48),  // Middle row (center is 32,32)
            (48, 16), (48, 32), (48, 48)   // Bottom row
        ]
        
        var pixelValuesString = "  📊 Actual model input values (center 3x3 grid):\n"
        for (y, x) in debugPositions {
            let multiIndex = [0, 0, y, x].map { NSNumber(value: $0) }
            let val = Float(truncating: array[multiIndex])
            pixelValuesString += String(format: "    [%2d,%2d] = %.3f  ", y, x, val)
            if (x == 48) { pixelValuesString += "\n" }
            // Simple hash: multiply by position and sum
            inputHash = inputHash &+ Int(val * 1000) &* (y * 64 + x)
        }
        print(pixelValuesString)
        
        // Count how many pixels are -1.0 (black) vs 1.0 (white)
        var blackCount = 0
        var whiteCount = 0
        var otherCount = 0
        for y in 0..<imageSize {
            for x in 0..<imageSize {
                let multiIndex = [0, 0, y, x].map { NSNumber(value: $0) }
                let val = Float(truncating: array[multiIndex])
                if abs(val - (-1.0)) < 0.01 {
                    blackCount += 1
                } else if abs(val - 1.0) < 0.01 {
                    whiteCount += 1
                } else {
                    otherCount += 1
                }
            }
        }
        
        print("  📊 Pixel statistics: min=\(minVal), max=\(maxVal), non-zero pixels=\(nonZeroCount)/\(pixelCount)")
        print("  📊 Normalized value range (sample): min=\(normalizedMin), max=\(normalizedMax) (expected: [-1.0, 1.0])")
        print("  📊 Binary pixel distribution: black(-1.0)=\(blackCount), white(1.0)=\(whiteCount), other=\(otherCount)")
        print("  📊 Input hash: \(inputHash) (different symbols should produce different hashes)")
        print("  ✓ Copied \(pixelCount) pixels to MLMultiArray")
        
        return array
    }
    
    private func runInference(_ input: MLMultiArray) -> [Float]? {
        guard let model = mlModel else {
            print("  ❌ Error: MLModel is nil")
            return nil
        }
        
        do {
            // Create input feature provider
            let inputName = model.modelDescription.inputDescriptionsByName.keys.first ?? "input"
            print("  Using input name: '\(inputName)'")
            let inputProvider = try MLDictionaryFeatureProvider(dictionary: [inputName: MLFeatureValue(multiArray: input)])
            
            // Run prediction
            print("  Running model prediction...")
            let prediction = try model.prediction(from: inputProvider)
            
            // Get output
            let outputName = model.modelDescription.outputDescriptionsByName.keys.first ?? "output"
            print("  Using output name: '\(outputName)'")
            guard let output = prediction.featureValue(for: outputName)?.multiArrayValue else {
                print("  ❌ Error: Could not get output from prediction")
                return nil
            }
            
            print("  ✓ Got output with \(output.count) elements")
            
            // Convert to array
            var predictions: [Float] = []
            for i in 0..<output.count {
                predictions.append(Float(truncating: output[i]))
            }
            
            // Apply softmax
            let softmaxed = softmax(predictions)
            print("  ✓ Applied softmax. Max value: \(softmaxed.max() ?? 0)")
            return softmaxed
        } catch {
            print("  ❌ Error running inference: \(error)")
            return nil
        }
    }
    
    private func softmax(_ values: [Float]) -> [Float] {
        let maxValue = values.max() ?? 0
        let expValues = values.map { exp($0 - maxValue) }
        let sum = expValues.reduce(0, +)
        return expValues.map { $0 / sum }
    }
    
    private func getTopK(_ predictions: [Float], k: Int) -> [(Int, Float)] {
        let indexed = predictions.enumerated().map { ($0.offset, $0.element) }
        let sorted = indexed.sorted { $0.1 > $1.1 }
        return Array(sorted.prefix(k))
    }
    
}

struct Suggestion: Identifiable {
    let id = UUID()
    let symbolId: Int
    let latexCommand: String
    let confidence: Float
    let preview: NSImage?
    let isLastChosen: Bool
    let context: String?
    let description: String?
    
    init(symbolId: Int, latexCommand: String, confidence: Float, preview: NSImage? = nil, isLastChosen: Bool = false, context: String? = nil, description: String? = nil) {
        self.symbolId = symbolId
        self.latexCommand = latexCommand
        self.confidence = confidence
        self.preview = preview
        self.isLastChosen = isLastChosen
        self.context = context
        self.description = description
    }
}

