# 🚀 Quick Start - Testing MathSymbolRecognizer

## ✅ Pre-flight Check Complete

All files are ready:

- ✅ 7 Swift source files
- ✅ CoreML model (2.9M)
- ✅ Xcode 26.2 installed
- ✅ macOS SDK available

## 🎯 Next Step: Create Xcode Project

### Fast Track (5 minutes)

1. **Xcode should be opening now...**

2. **Create New Project**:
   - In Xcode: **File > New > Project** (⇧⌘N)
   - Choose **macOS** > **App**
   - Click **Next**

3. **Configure**:
   - Product Name: `MathSymbolRecognizer`
   - Interface: **SwiftUI**
   - Language: **Swift**
   - Save in: `macos_app/` folder
   - Click **Create**

4. **Add Files** (Important!):
   - **Delete** default `ContentView.swift` and `MathSymbolRecognizerApp.swift`
   - Right-click project > **Add Files to "MathSymbolRecognizer"...**
   - Navigate to `MathSymbolRecognizer/Sources/`
   - **Select ALL 7 .swift files**
   - ✅ Check "Copy items if needed"
   - ✅ Check "Add to targets"
   - Click **Add**

5. **Add Model**:
   - Right-click project > **Add Files to "MathSymbolRecognizer"...**
   - Navigate to `MathSymbolRecognizer/Resources/`
   - Select `best_model.mlpackage`
   - ✅ Check "Copy items if needed"
   - ✅ Check "Add to targets"
   - Click **Add**

6. **Build & Run**:
   - Press **⌘B** to build
   - Press **⌘R** to run

## 🧪 Test Checklist

Once the app runs:

- [ ] Draw a symbol (try drawing "∑" or "→")
- [ ] Click "Recognize"
- [ ] Check suggestions appear
- [ ] Click a suggestion to copy LaTeX

## 📚 Full Documentation

- **Setup Guide**: `create_xcode_project.md`
- **Testing Guide**: `TESTING.md`
- **Project README**: `README.md`

## 🆘 Troubleshooting

If you encounter issues:

1. **Build Errors**: Check all files are added to target
2. **Model Not Found**: Verify model is in Resources and added to target
3. **Drawing Issues**: Check `DrawingCanvasView` connection

See `TESTING.md` for detailed troubleshooting.

---

**Ready? Let's test! 🎉**
