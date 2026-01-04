# Creating the Xcode Project

Since we can't automatically create a full Xcode project from the command line, follow these steps:

## Step 1: Create New Xcode Project

1. Open Xcode
2. File > New > Project (⇧⌘N)
3. Select **macOS** tab
4. Choose **App**
5. Click **Next**

## Step 2: Configure Project

- **Product Name**: `MathSymbolRecognizer`
- **Team**: (Your development team)
- **Organization Identifier**: (e.g., `com.yourname`)
- **Interface**: **SwiftUI**
- **Language**: **Swift**
- **Storage**: **None** (we'll add files manually)
- **Include Tests**: Optional

Click **Next** and save in: `/Users/kaichen/Documents/Github/Intelligent-Handwritten-Math-Recognition/macos_app/`

## Step 3: Add Source Files

1. Delete the default `ContentView.swift` and `MathSymbolRecognizerApp.swift` (if they exist)
2. Right-click on the project in Navigator
3. Select **Add Files to "MathSymbolRecognizer"...**
4. Navigate to `MathSymbolRecognizer/Sources/`
5. Select all `.swift` files:
   - `App.swift`
   - `ContentView.swift`
   - `DrawingCanvasView.swift`
   - `RecognitionViewModel.swift`
   - `SuggestionListView.swift`
   - `ImageExtensions.swift`
   - `SymbolMapping.swift`
6. Ensure **"Copy items if needed"** is checked
7. Click **Add**

## Step 4: Add CoreML Model

1. Right-click on the project in Navigator
2. Select **Add Files to "MathSymbolRecognizer"...**
3. Navigate to `MathSymbolRecognizer/Resources/`
4. Select `best_model.mlpackage`
5. Ensure **"Copy items if needed"** is checked
6. Ensure **"Add to targets: MathSymbolRecognizer"** is checked
7. Click **Add**

## Step 5: Configure Build Settings

1. Select the project in Navigator
2. Select the **MathSymbolRecognizer** target
3. Go to **General** tab:
   - **Minimum Deployments**: macOS 13.0
   - **Supported Platforms**: macOS
4. Go to **Signing & Capabilities**:
   - Enable **App Sandbox** (if needed)
   - Add **User Selected File** capability (for future file import)

## Step 6: Build and Run

1. Select a scheme: **MathSymbolRecognizer > My Mac**
2. Build (⌘B) to check for errors
3. Run (⌘R) to launch the app

## Troubleshooting

### CoreML Model Not Found
- Ensure `best_model.mlpackage` is in the project's Resources folder
- Check that it's added to the target in Build Phases > Copy Bundle Resources

### Import Errors
- Ensure all Swift files are added to the target
- Clean build folder (⇧⌘K) and rebuild

### Drawing Not Working
- Check that `DrawingCanvasView` is properly connected to `RecognitionViewModel`
- Verify canvas delegate is set correctly

## Next Steps

After the project is set up:
- Test drawing on the canvas
- Verify CoreML inference works
- Test suggestion list display
- Test copy-to-clipboard functionality

