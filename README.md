# Intelligent Handwritten Math Recognition

A cross-platform LaTeX input assistant that recognizes single handwritten mathematical symbols and provides ranked LaTeX command suggestions.

## Core Objective

Build a **cross-platform LaTeX input assistant**: the user intentionally draws **one mathematical symbol**, and the system returns a **ranked suggestion list** of possible LaTeX commands (each with rendered preview), so the user can **choose the intended one** quickly and reliably.

> **Scope boundary:** This project targets **single-symbol recognition for LaTeX input assistance**, _not_ full handwritten formula-to-LaTeX conversion.

## Architecture

- **Vision Engine**: Classifies drawn shapes into symbol hypotheses (PyTorch → ONNX → CoreML)
- **Semantic Suggestion Engine**: Maps symbol classes to ranked LaTeX candidates with mathematical preferences
- **Personalization Layer**: Remembers user choices for future suggestions

## Project Structure

```
.
├── vision_engine/          # Phase 1: Vision Engine (PyTorch)
│   ├── data/               # Data loading and preprocessing
│   ├── models/             # Model definitions
│   ├── training/           # Training scripts
│   └── export/             # Model export (ONNX, CoreML)
├── semantic_engine/        # Phase 2: Semantic Suggestion Engine
│   ├── mapping_db/         # LaTeX candidate mapping database
│   └── ranking/            # Ranking algorithms
├── personalization/        # Phase 3: Personalization Layer
├── macos_client/           # Phase 4: macOS MVP (Swift)
└── docs/                   # Documentation

```

## Development Roadmap

See [ROADMAP.md](ROADMAP.md) for detailed phases and current progress.

## License

[To be determined]
