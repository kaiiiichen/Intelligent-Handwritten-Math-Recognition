# Intelligent Handwritten Math Recognition - Development Roadmap

**Last Updated:** 2025-01-04
**Status:** Phase 1 & 2 Complete - Models Exported, Semantic Engine Ready

---

## Core Objective

Build a **cross-platform LaTeX input assistant**: the user intentionally draws **one mathematical symbol**, and the system returns a **ranked suggestion list** of possible LaTeX commands (each with rendered preview), so the user can **choose the intended one** quickly and reliably.

> **Scope boundary (important):** This project targets **single-symbol recognition for LaTeX input assistance**, _not_ full handwritten formula-to-LaTeX conversion.

---

## 1. Problem Statement & Philosophy

### 1.1 What's broken in existing tools

Many handwriting/OCR tools for math fail in two recurring ways:

1. **Visual fragility:** Subtle glyph differences in handwriting cause high error rates.
2. **Math-unaware outputs:** They treat symbols as images rather than mathematical entities (e.g., `\Sigma` vs. `\sum`, or `\Rightarrow` vs. `\implies`).

This roadmap is designed around a pragmatic truth:

> **For single symbols, ambiguity is normal.** A great tool shouldn't pretend ambiguity doesn't exist — it should present _good candidates_, ordered by mathematical sense, and let the user decide.

### 1.2 The Technical Rationale: Vision vs. Trajectory

Why prefer **offline-style vision recognition** (shape-based) over **trajectory/pen-order** approaches?

* **The stroke-order dilemma:** Unlike Chinese characters, mathematical symbols have _no canonical stroke order_, and personal style variance is huge.
  * Sigma (`\Sigma`) can be 1 stroke or multiple strokes.
  * Integral (`\int`) can be top-down or bottom-up.
* **Design decision:** Even if we collect input on-device (finger/stylus), we intentionally treat the drawing as a **final geometric shape**.
  * We can rasterize strokes into an image and run a CNN/ViT-style classifier.
  * Time order becomes (at most) a weak auxiliary signal — never a hard assumption.

Result: **Stroke-order invariance** and a cleaner engineering path for a robust MVP.

### 1.3 Our Philosophy: A Decoupled, Tool-First Architecture

Instead of forcing one model to learn _everything_, we split the system into:

* **Vision Engine (Shape → Symbol hypotheses):** Classify the drawn shape into a shortlist of likely symbol classes.
* **Semantic Suggestion Engine (Symbol hypotheses → LaTeX candidates):** Map each symbol class to **multiple LaTeX candidates**, then **rank them** with mathematically informed heuristics (and light personalization).

Crucially, the system is a **suggestion tool**, not an oracle:

* We aim for _high-quality top-k_ recommendations.
* The final selection remains user-controlled.

---

## 2. User Experience Spec (the product contract)

### 2.1 Output format: ranked candidate list

For each user input, show a list like:

1. `\implies` ⇒ (Rendered preview) **Recommended**
2. `\Rightarrow` ⇒ (Rendered preview)
3. `\rightarrow` → (Rendered preview)

Each item includes:

* LaTeX command
* Rendered preview (offline if possible)
* Optional short hint (e.g., "logical implication", "mapping", "derivation arrow")

### 2.2 Mathematical preference order (not just "most likely")

Ranking is **not purely visual**. Some commands are more mathematically appropriate defaults:

* Double arrow is visually similar across contexts, but `\implies` is often the best default in logic-heavy use.
* `\rightarrow` is common for functions/mappings; it shouldn't silently replace implication.

So the system ranks by a blend of:

* **Visual confidence** (Vision Engine)
* **Math preference** (Semantic Suggestion Engine, by mode or heuristics)
* **Light personalization** (see next section)

### 2.3 Interaction memory: "Last time you chose …"

Add a lightweight user history feature:

* When the user selects a candidate for a given symbol (or symbol cluster), store that choice.
* Next time the user draws a similar symbol, the suggestion list stays **mathematically ranked**, but the previously chosen candidate gets a subtle marker, e.g.:
  * "★ last chosen"
  * or a small badge "last time"

This preserves mathematical correctness **and** respects the user's personal habits.

---

## 3. Technical Stack

### Machine Learning (The "Brain")

* **Framework:** PyTorch (training), ONNX (cross-platform inference), CoreML (Apple platforms)
* **Architecture:** CNN baseline (4-layer CNN with batch normalization, optimized for symbol classification)
  * Current: 4 conv layers → Global Average Pooling → 2 FC layers
  * Model size: ~2-3 MB (suitable for mobile deployment)
  * Future upgrade path: lightweight ViT / attention-augmented CNN if needed
* **Datasets:** HASYv2 (primary, 369 symbol classes), CROHME (symbol extraction), MNIST/EMNIST (prototyping)
* **Device Support:**
  * Training: MPS (Metal Performance Shaders) for Apple Silicon acceleration
  * Inference: CoreML (iOS/iPadOS/macOS), ONNX Runtime (Windows/Linux)

### macOS Client (The MVP)

* **Language:** Swift
* **UI:** SwiftUI
* **Inference:** CoreML (Apple Neural Engine where available)

### Cross-Platform Deployment Strategy

* **Apple Platforms (iOS/iPadOS/macOS):**
  * **Format:** CoreML (.mlpackage)
  * **Inference:** CoreML framework (Apple Neural Engine where available)
  * **Benefits:** Native performance, on-device inference, privacy-preserving
  
* **Windows/Linux:**
  * **Format:** ONNX (.onnx)
  * **Inference:** ONNX Runtime (CPU/GPU acceleration)
  * **Benefits:** Cross-platform compatibility, efficient inference
  
* **Future Frameworks:**
  * Electron or Flutter (evaluate for cross-platform UI)
  * Web deployment: ONNX.js or TensorFlow.js (evaluate)

---

## 4. Development Roadmap

### Phase 1: Vision Engine (Python/PyTorch) ✅ **COMPLETE**

_Goal: Robust top-k symbol hypotheses over 300+ symbols (optimize for top-1 and top-5)._

**Status:** Model training and cross-platform export completed successfully. Ready for integration.

**Completed:**

* ✅ Data pipeline setup (HASYv2 dataset loading and preprocessing)
* ✅ Model baseline implementation (CNN architecture)
* ✅ Training infrastructure (trainer, metrics, checkpointing)
* ✅ Device support (MPS for Apple Silicon)
* ✅ Data augmentation pipeline
* ✅ **Model training completed (50 epochs)**
* ✅ **Model evaluation and validation completed**
* ✅ ONNX export code implementation

**Current Performance (Final Epoch 50):**

* **Top-1 Accuracy: 83.46%** (Target: >70% ✅ **Exceeded by 13.46%**)
* **Top-5 Accuracy: 98.08%** (Target: >90% ✅ **Exceeded by 8.08%**)
* Validation Loss: 0.523 (converged and stable)
* Training Loss: 0.654 (well converged)

**Model Checkpoints:**

* `checkpoints/best_model.pth` - Best validation performance model
* `checkpoints/final_model.pth` - Final epoch model
* `checkpoints/training_history.json` - Complete training metrics

**Completed (Export & Integration):**

* ✅ Model export to ONNX format (Windows/Linux/Cross-platform)
* ✅ Model export to CoreML format (iOS/iPadOS/macOS)
* ✅ Unified export script for all platforms (`export_all.py`)
* ✅ Model format validation and testing
* ✅ Cross-platform deployment infrastructure

**Exported Models:**

* `exports/best_model.onnx` - ONNX format for Windows/Linux/Cross-platform
  * Verified with ONNX Runtime
  * Input: (1, 1, 64, 64) grayscale image
  * Output: (1, 369) probability distribution over symbol classes
  
* `exports/best_model.mlpackage` - CoreML format for iOS/iPadOS/macOS
  * Verified with CoreML framework
  * Supports Apple Neural Engine acceleration
  * Minimum deployment target: iOS 13+

**Remaining (Optional):**

* ⏳ Performance optimization and fine-tuning (optional, current performance exceeds targets)
* ⏳ Model quantization for smaller file size (if needed)
* ⏳ Additional format exports (TensorFlow Lite, etc.) if required

---

### Phase 2: Semantic Suggestion Engine (Logic + Ranking) ✅ **COMPLETE**

_Goal: Map symbol hypotheses to ranked LaTeX candidates with mathematical preferences._

**Status:** Core functionality complete. Ready for integration with UI.

**Completed:**

* ✅ Mapping database structure (`SymbolMappingDatabase`)
* ✅ LaTeX candidate data model (`LaTeXCandidate`, `SymbolMapping`)
* ✅ Mathematical priority scoring system
* ✅ Initial symbol mappings (20+ common mathematical symbols with detailed alternatives)
* ✅ Mathematical priority guidelines documentation
* ✅ **Ranking algorithm implementation (`CandidateRanker`)**
  * Combines Vision Engine confidence scores with mathematical priority
  * Configurable weights (default: 60% vision, 40% math)
  * Supports vision-heavy and math-heavy ranking modes
* ✅ **Complete symbol mapping database (all 369+ symbols)**
  * Auto-generated mappings for all symbols from HASYv2 dataset
  * Preserves manually curated mappings for common symbols
  * JSON-based storage for easy extension
* ✅ **LaTeX candidate rendering system (`LaTeXRenderer`)**
  * Matplotlib backend for development
  * PIL backend fallback
  * Supports image and SVG output (SVG placeholder for future)
* ✅ **Integration interface (`SemanticSuggestionEngine`)**
  * Unified API connecting Vision Engine and Semantic Engine
  * Takes Vision Engine predictions and returns ranked LaTeX candidates
  * Supports both raw predictions and top-k symbol lists
  * Example usage scripts provided

**Remaining (Optional Enhancements):**

* ⏳ Mode-based ranking (Logic Mode, Analysis Mode, etc.) - Future enhancement
* ⏳ Advanced preview rendering (MathJax/KaTeX integration for production)
* ⏳ User preference learning (Phase 3)

---

### Phase 3: Personalization Layer (Interaction Memory) ⏳ **NOT STARTED**

_Goal: Improve UX without corrupting math ranking._

**Status:** Not yet started

**Planned:**

* ⏳ User choice storage system
* ⏳ Per-symbol last-choice tracking
* ⏳ UI markers for "last chosen" candidates
* ⏳ History management (clear, export, import)
* ⏳ Optional style clustering for similar symbols

---

### Phase 4: macOS MVP (Swift) ✅ **IN PROGRESS**

_Goal: A native, fast Mac app that feels like a real tool, not a demo._

**Status:** Core implementation complete. Ready for Xcode project setup and testing.

**Completed:**

* ✅ **Project structure created**
  * SwiftUI app structure
  * Source files organized
  * Resources directory setup
* ✅ **High-performance drawing canvas (`DrawingCanvas`)**
  * NSView-based canvas for stroke capture
  * Real-time stroke rendering
  * Mouse/trackpad input support
  * Image export functionality
* ✅ **Client-side preprocessing (`ImageExtensions`)**
  * Image resize to 64x64 pixels
  * Grayscale conversion
  * Pixel normalization (0.0-1.0)
  * MLMultiArray conversion for CoreML
* ✅ **CoreML integration (`RecognitionViewModel`)**
  * Model loading from bundle
  * Inference pipeline implementation
  * Softmax normalization
  * Top-k prediction extraction
* ✅ **UI/UX implementation**
  * Main view with split layout (`ContentView`)
  * Drawing canvas view (`DrawingCanvasView`)
  * Suggestion list view (`SuggestionListView`)
  * Copy-to-clipboard functionality
  * Basic symbol-to-LaTeX mapping (`SymbolMapping`)

**Remaining:**

* ⏳ Xcode project setup (manual step - see `macos_app/create_xcode_project.md`)
* ⏳ Testing and debugging
* ⏳ LaTeX preview rendering
* ⏳ "Last chosen" marker
* ⏳ Settings and preferences UI
* ⏳ Integration with Semantic Suggestion Engine (Python bridge or Swift port)

---

### Phase 5: Cross-Platform Expansion ⏳ **NOT STARTED**

_Goal: Bring it to Windows and Linux._

**Status:** Not yet started

**Planned:**

* ⏳ Framework evaluation (Electron vs. Flutter)
* ⏳ ONNX Runtime integration for non-Apple devices
* ⏳ UI porting while preserving minimal aesthetics
* ⏳ Platform-specific optimizations

---

## 5. Future Outlook

### 5.1 Offline LaTeX rendering improvements

* Better local rendering quality
* Faster previews
* Optional caching of frequent symbols

### 5.2 From single symbol → full handwritten formula to LaTeX (HMER)

After the single-symbol tool is stable, a natural next step is expanding toward **full handwritten mathematical expression recognition (HMER)**: converting complete handwritten formulas into LaTeX.

A realistic, extensible path is **structure-aware and modular**:

* Segmentation / symbol grouping
* Symbol classification (reusing this project's Vision Engine)
* Spatial relation prediction (superscripts, fractions, radicals, etc.)
* Structure tree/graph construction
* LaTeX generation

Recent work on **structural** HMER suggests that modular, structure-aware pipelines can provide stronger interpretability and extensibility than purely end-to-end generation.

### 5.3 Personalization beyond memory (optional)

* Carefully explore per-user adaptation only after we have strong baselines
* Default stance: **don't overfit to one user** unless the UX clearly benefits

---

## Progress Summary

| Phase | Status | Progress |
| :--- | :--- | :--- |
| Phase | Status | Progress |
| :--- | :--- | :--- |
| Phase 1: Vision Engine | ✅ **COMPLETE** | **100%** (Training complete, models exported) |
| Phase 2: Semantic Suggestion Engine | ✅ **COMPLETE** | **100%** (Ranking, mapping, rendering complete) |
| Phase 3: Personalization Layer | ⏳ Not Started | 0% |
| Phase 4: macOS MVP | ✅ **IN PROGRESS** | **~80%** (Core implementation complete, needs Xcode setup) |
| Phase 5: Cross-Platform | ⏳ Not Started | 0% |

**Overall Project Progress:** ~55%

**Recent Achievements:**

* ✅ Phase 1 model training completed with excellent performance (Top-1: 83.46%, Top-5: 98.08%)
* ✅ Model performance significantly exceeds targets
* ✅ **Cross-platform model export completed:**
  * ONNX model exported and verified (Windows/Linux/Cross-platform)
  * CoreML model exported and verified (iOS/iPadOS/macOS)
  * Unified export infrastructure ready for deployment
* ✅ **Phase 2 Semantic Suggestion Engine completed:**
  * Ranking algorithm combining vision confidence and mathematical priority
  * Complete mapping database for all 369+ symbols
  * LaTeX rendering system for candidate previews
  * Integration interface ready for UI integration
* ✅ **Phase 4 macOS MVP core implementation:**
  * Drawing canvas with stroke capture
  * Image preprocessing pipeline
  * CoreML inference integration
  * SwiftUI interface with suggestion list
  * Copy-to-clipboard functionality

---

## References

* HASYv2 Dataset: [https://www.kaggle.com/datasets/guru001/hasyv2](https://www.kaggle.com/datasets/guru001/hasyv2)
