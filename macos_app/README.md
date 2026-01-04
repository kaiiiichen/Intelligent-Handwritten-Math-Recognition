# MathSymbolRecognizer - macOS MVP

Native macOS application for intelligent handwritten mathematical symbol recognition.

## Features

- **High-performance drawing canvas**: Smooth stroke capture with Apple Pencil or mouse
- **CoreML inference**: On-device symbol recognition using Apple Neural Engine
- **Ranked suggestions**: LaTeX candidates sorted by confidence and mathematical priority
- **Copy to clipboard**: One-click LaTeX command copying
- **Native SwiftUI**: Fast, responsive macOS interface

## Requirements

- macOS 13.0+ (Ventura or later)
- Xcode 15.0+
- CoreML model: `best_model.mlpackage` (from `../exports/`)

## Setup

1. **Copy CoreML model**:

   ```bash
   cp ../exports/best_model.mlpackage MathSymbolRecognizer/Resources/
   ```

2. **Open in Xcode**:

   ```bash
   open MathSymbolRecognizer.xcodeproj
   ```

3. **Build and run** (⌘R)

## Project Structure

```
MathSymbolRecognizer/
├── Sources/
│   ├── App.swift                    # App entry point
│   ├── ContentView.swift           # Main view
│   ├── DrawingCanvasView.swift      # Drawing canvas (NSView)
│   ├── RecognitionViewModel.swift   # Recognition logic
│   ├── SuggestionListView.swift    # Suggestion list UI
│   └── ImageExtensions.swift        # Image processing utilities
└── Resources/
    └── best_model.mlpackage         # CoreML model
```

## Architecture

### Drawing Canvas

- `DrawingCanvas`: NSView-based canvas for stroke capture
- Captures mouse/trackpad input
- Renders strokes in real-time
- Exports drawing as NSImage

### Image Preprocessing

- Resize to 64x64 pixels
- Convert to grayscale
- Normalize pixel values (0.0-1.0)
- Convert to MLMultiArray format

### CoreML Integration

- Loads `best_model.mlpackage`
- Runs inference on preprocessed image
- Returns probability distribution over 369 symbol classes
- Applies softmax for normalized probabilities

### Suggestion Ranking

- Gets top-k symbol predictions
- Maps to LaTeX commands (TODO: integrate with semantic engine)
- Displays ranked list with confidence scores

## TODO

- [ ] Integrate with Semantic Suggestion Engine (Python bridge or Swift port)
- [ ] Add LaTeX preview rendering
- [ ] Implement "last chosen" marker
- [ ] Add settings and preferences
- [ ] Support for Apple Pencil (iPad compatibility)
- [ ] Auto-recognition on drawing completion
- [ ] History and favorites

## Integration with Python Backend

For full semantic ranking, the app can:

1. Export image to Python script
2. Run Python inference + semantic ranking
3. Import results back to SwiftUI

Or port the semantic engine to Swift for native performance.
