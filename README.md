# Intelligent Handwritten Math Recognition

A **cross-platform LaTeX input assistant** that recognizes handwritten mathematical symbols and provides ranked LaTeX command suggestions with live previews.

## 🎯 Core Objective

Draw **one mathematical symbol** → Get **ranked LaTeX suggestions** with previews → **Quick selection** → **Copy to clipboard**

> **Scope:** Single-symbol recognition for LaTeX input assistance (not full formula conversion)

## ✨ Key Features

- **🎨 Live LaTeX Previews**: See exactly what each command produces
- **🤖 Auto-Recognition**: Recognizes symbols automatically after drawing
- **⭐ Smart Personalization**: Remembers your choices with "last chosen" markers
- **⌨️ Keyboard Shortcuts**: Press 1-5 to select suggestions instantly
- **🔒 Privacy-First**: All processing happens on-device

## 🏗️ Architecture

```
Vision Engine (PyTorch/CoreML) → Semantic Engine → UI with LaTeX Previews
     ↓                              ↓                    ↓
Symbol Classification        Mathematical Ranking    User Selection
```

- **Vision Engine**: CNN model (83.46% top-1, 98.08% top-5 accuracy)
- **Semantic Engine**: Mathematical priority ranking + user preferences
- **Cross-Platform**: ONNX (Windows/Linux) + CoreML (macOS/iOS)

## 🚀 Current Status

**✅ Ready to Use**: macOS app with full functionality

- Vision model trained and exported
- Semantic ranking implemented
- LaTeX preview rendering
- Auto-recognition with user preferences
- Professional UI with keyboard shortcuts

## 📁 Project Structure

```
├── vision_engine/          # ML model (PyTorch → ONNX/CoreML)
├── semantic_engine/        # LaTeX ranking and mapping
├── macos_app/             # Native macOS application
├── exports/               # Trained models (2.9MB CoreML, 32KB ONNX)
├── data/                  # HASYv2 dataset (369 symbol classes)
└── checkpoints/           # Training results and history
```

## 🎮 Quick Start

### macOS App (Ready Now)

1. Open `macos_app/MathSymbolRecognizer.xcodeproj`
2. Build and run (⌘R)
3. Draw a symbol → See suggestions with previews
4. Click or press 1-5 to select → Copied to clipboard!

### Features to Try

- **Auto-recognition**: Draw and wait 1 second
- **Settings**: Click gear icon to customize
- **Keyboard shortcuts**: 1-5 for quick selection
- **Choice memory**: System remembers your preferences

## 📊 Performance

- **Model Accuracy**: 83.46% top-1, 98.08% top-5
- **Symbol Classes**: 369 mathematical symbols
- **Recognition Speed**: ~100ms on Apple Silicon
- **Model Size**: 2.9MB (CoreML), 32KB (ONNX)

## 🛣️ Development Roadmap

**Phase 1-2: ✅ Complete** - Vision + Semantic engines
**Phase 3: ✅ Complete** - macOS app with full features
**Phase 4: 🔄 Next** - Cross-platform expansion (Windows/Linux)
**Phase 5: 📋 Planned** - Multi-symbol recognition

See [ROADMAP.md](ROADMAP.md) for detailed progress.

## 🤝 Contributing

This project is ready for contributions! Areas of interest:

- Cross-platform UI (Electron/Flutter)
- Additional LaTeX symbol mappings
- Performance optimizations
- Multi-symbol recognition research

## 📄 License

MIT License (see LICENSE file)
