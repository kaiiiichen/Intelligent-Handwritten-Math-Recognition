# Testing Guide for MathSymbolRecognizer

## Quick Start Testing

### 1. Run Pre-flight Checks

```bash
cd macos_app
./quick_test.sh
```

This will verify:
- ✅ All source files are present
- ✅ CoreML model is available
- ✅ File structure is correct
- ✅ Xcode is installed

### 2. Create Xcode Project

Since we can't fully automate Xcode project creation, follow these steps:

#### Method A: Using Xcode GUI (Recommended)

1. **Open Xcode**
   ```bash
   open -a Xcode
   ```

2. **Create New Project**
   - File > New > Project (⇧⌘N)
   - Select **macOS** tab
   - Choose **App**
   - Click **Next**

3. **Configure Project**
   - Product Name: `MathSymbolRecognizer`
   - Team: (Your team)
   - Organization Identifier: (e.g., `com.yourname`)
   - Interface: **SwiftUI**
   - Language: **Swift**
   - Click **Next**

4. **Save Location**
   - Navigate to: `macos_app/`
   - **Important**: Uncheck "Create Git repository" (we already have one)
   - Click **Create**

5. **Add Source Files**
   - Delete default `ContentView.swift` and `MathSymbolRecognizerApp.swift`
   - Right-click project > **Add Files to "MathSymbolRecognizer"...**
   - Navigate to `MathSymbolRecognizer/Sources/`
   - Select all `.swift` files
   - ✅ Check "Copy items if needed"
   - ✅ Check "Add to targets: MathSymbolRecognizer"
   - Click **Add**

6. **Add CoreML Model**
   - Right-click project > **Add Files to "MathSymbolRecognizer"...**
   - Navigate to `MathSymbolRecognizer/Resources/`
   - Select `best_model.mlpackage`
   - ✅ Check "Copy items if needed"
   - ✅ Check "Add to targets: MathSymbolRecognizer"
   - Click **Add**

7. **Configure Build Settings**
   - Select project > Target "MathSymbolRecognizer"
   - **General** tab:
     - Minimum Deployments: **macOS 13.0**
   - **Signing & Capabilities**:
     - Enable your development team

### 3. Build and Test

1. **Build** (⌘B)
   - Check for any compilation errors
   - Fix any import or syntax issues

2. **Run** (⌘R)
   - App should launch
   - Test drawing on canvas
   - Click "Recognize" button
   - Verify suggestions appear

## Testing Checklist

### Basic Functionality

- [ ] App launches without crashes
- [ ] Drawing canvas responds to mouse/trackpad
- [ ] Strokes render in real-time
- [ ] "Clear" button works
- [ ] "Recognize" button triggers inference
- [ ] Suggestions list displays results
- [ ] Copy-to-clipboard works

### CoreML Integration

- [ ] Model loads successfully (check console)
- [ ] Inference runs without errors
- [ ] Top-k predictions are extracted
- [ ] Confidence scores are reasonable (0.0-1.0)

### UI/UX

- [ ] Window resizes properly
- [ ] Split view layout works
- [ ] Suggestions are clickable
- [ ] Loading state shows during processing
- [ ] Error handling (if model fails to load)

### Edge Cases

- [ ] Empty canvas (no drawing)
- [ ] Very small drawing
- [ ] Very large drawing
- [ ] Multiple rapid recognitions
- [ ] Clear during recognition

## Common Issues and Fixes

### Issue: "Cannot find 'ContentView' in scope"

**Fix**: Ensure all Swift files are added to the target:
1. Select file in Navigator
2. Check "Target Membership" in File Inspector
3. Ensure "MathSymbolRecognizer" is checked

### Issue: "CoreML model not found"

**Fix**: 
1. Check model is in Resources folder
2. Check "Copy Bundle Resources" in Build Phases
3. Verify model path in code matches bundle structure

### Issue: Drawing not working

**Fix**:
1. Check `DrawingCanvasView` is properly connected
2. Verify `canvas` property is set in `RecognitionViewModel`
3. Check delegate methods are implemented

### Issue: Inference fails

**Fix**:
1. Check model input/output shapes match
2. Verify image preprocessing produces correct format
3. Check console for CoreML errors
4. Ensure model is compiled for current architecture

## Performance Testing

- **Drawing**: Should be smooth, no lag
- **Recognition**: Should complete in < 1 second
- **UI Updates**: Should be responsive, no freezing

## Debugging Tips

1. **Enable Console Logging**
   - Add `print()` statements in key methods
   - Check Xcode console for output

2. **Breakpoints**
   - Set breakpoints in `recognizeSymbol()`
   - Step through preprocessing
   - Inspect MLMultiArray values

3. **Model Verification**
   ```swift
   // In RecognitionViewModel.init()
   if let model = mlModel {
       print("Model loaded: \(model.modelDescription)")
       print("Input: \(model.modelDescription.inputDescriptionsByName)")
       print("Output: \(model.modelDescription.outputDescriptionsByName)")
   }
   ```

4. **Image Inspection**
   - Save preprocessed image to file for debugging
   - Verify dimensions and pixel values

## Next Steps After Testing

Once basic functionality works:
1. Test with various mathematical symbols
2. Verify LaTeX commands are correct
3. Test copy-to-clipboard functionality
4. Consider adding LaTeX preview rendering
5. Integrate with Semantic Suggestion Engine

