# MathSymbolRecognizer - macOS App

**Status:** ✅ **Ready to Use** - Full-featured LaTeX input assistant

## 🚀 Quick Start

1. **Open:** `MathSymbolRecognizer.xcodeproj` in Xcode
2. **Build:** Press ⌘B
3. **Run:** Press ⌘R
4. **Draw:** Sketch a mathematical symbol
5. **Select:** Click or press 1-5 to choose suggestion
6. **Use:** LaTeX command is copied to clipboard!

## ✨ Features

### 🎨 Live LaTeX Previews

- See exactly what each LaTeX command produces
- 100+ mathematical symbols with Unicode rendering
- Professional mathematical font support

### 🤖 Auto-Recognition

- Recognizes symbols automatically after drawing (1s delay)
- Configurable in settings (0.5-3.0 seconds)
- Manual recognition still available (Enter key)

### ⭐ Smart Personalization

- Remembers your LaTeX command choices
- Shows "⭐ last chosen" markers
- Mathematical priority ranking preserved

### ⌨️ Keyboard Shortcuts

- **1-5:** Select suggestions instantly
- **Enter:** Manual recognition
- **Delete:** Clear canvas
- **Gear icon:** Open settings

## 🎯 Perfect For

- **Students:** Quick LaTeX symbols for homework and notes
- **Researchers:** Efficient mathematical writing
- **Educators:** Creating mathematical content
- **Anyone:** Who needs LaTeX symbols fast!

## 🔧 Technical Details

- **Model:** 83.46% accuracy on 369 symbol classes
- **Performance:** ~100ms recognition on Apple Silicon
- **Privacy:** All processing happens on-device
- **Size:** 2.9MB CoreML model included in app

## 📱 System Requirements

- **macOS:** 11.0+ (Big Sur or later)
- **Xcode:** 14.0+ for building
- **Hardware:** Any Mac (optimized for Apple Silicon)

## 🎮 How to Use

### Basic Workflow

1. **Draw** a mathematical symbol on the white canvas
2. **Wait** for auto-recognition (or click "Recognize")
3. **See** suggestions with live LaTeX previews
4. **Select** by clicking or pressing number keys 1-5
5. **Paste** the LaTeX command anywhere you need it!

### Pro Tips

- **Settings:** Click gear icon to customize auto-recognition
- **Keyboard:** Use 1-5 keys for lightning-fast selection
- **Memory:** System remembers your preferences with star markers
- **Clear:** Press Delete to start over

## 🛠️ Development

### Project Structure

```
MathSymbolRecognizer/
├── App.swift                    # App entry point
├── ContentView.swift           # Main interface
├── DrawingCanvasView.swift     # Drawing canvas
├── RecognitionViewModel.swift  # Recognition logic
├── SuggestionListView.swift    # Suggestion display
├── LaTeXRenderer.swift         # Preview rendering
├── UserPreferences.swift       # Settings & memory
├── SettingsView.swift          # Settings interface
└── Resources/
    └── best_model.mlpackage    # CoreML model
```

### Key Components

- **DrawingCanvas:** High-performance NSView for stroke capture
- **LaTeXRenderer:** Unicode conversion for 100+ symbols
- **UserPreferences:** Auto-recognition settings and choice memory
- **RecognitionViewModel:** CoreML integration and ranking logic

## 🎉 Success Stories

This app transforms the LaTeX symbol input experience:

- **Before:** Look up LaTeX commands, type carefully, hope for no typos
- **After:** Draw symbol, press number key, paste - done in 2 seconds!

Perfect for anyone who writes mathematical content and wants to focus on ideas, not LaTeX syntax.
