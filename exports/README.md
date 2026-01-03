# Exported Models

This directory contains the exported models ready for cross-platform deployment.

## Model Files

### `best_model.onnx`
- **Format:** ONNX (Open Neural Network Exchange)
- **Platform:** Windows, Linux, Cross-platform
- **Inference:** ONNX Runtime
- **Input:** Grayscale image (1, 1, 64, 64)
- **Output:** Probability distribution over 369 symbol classes (1, 369)
- **Size:** ~3 MB
- **Status:** ✅ Verified and tested

### `best_model.mlpackage`
- **Format:** CoreML (Apple Machine Learning)
- **Platform:** iOS, iPadOS, macOS
- **Inference:** CoreML framework (Apple Neural Engine where available)
- **Input:** Grayscale image (1, 1, 64, 64)
- **Output:** Probability distribution over 369 symbol classes
- **Size:** ~3 MB
- **Minimum Deployment Target:** iOS 13+
- **Status:** ✅ Verified and tested

## Usage

### ONNX (Windows/Linux)

```python
import onnxruntime as ort
import numpy as np

# Load model
session = ort.InferenceSession("best_model.onnx")

# Prepare input (grayscale image, 64x64)
input_image = np.random.randn(1, 1, 64, 64).astype(np.float32)

# Run inference
outputs = session.run(None, {"input": input_image})
predictions = outputs[0]  # Shape: (1, 369)

# Get top-k predictions
top_k = 5
top_indices = np.argsort(predictions[0])[-top_k:][::-1]
top_probs = predictions[0][top_indices]
```

### CoreML (iOS/iPadOS/macOS)

```swift
import CoreML

// Load model
let model = try MLModel(contentsOf: URL(fileURLWithPath: "best_model.mlpackage"))

// Prepare input
let input = try MLMultiArray(shape: [1, 1, 64, 64], dataType: .float32)
// ... fill input with image data ...

// Create input feature provider
let inputProvider = try MLDictionaryFeatureProvider(dictionary: ["input": MLFeatureValue(multiArray: input)])

// Run inference
let prediction = try model.prediction(from: inputProvider)
let output = prediction.featureValue(for: "var_145")?.multiArrayValue

// Get top-k predictions
// ... process output ...
```

## Export Script

To export models yourself:

```bash
python3 -m vision_engine.export.export_all \
    --checkpoint checkpoints/best_model.pth \
    --output_dir exports \
    --num_classes 369 \
    --input_size 64
```

Or export individual formats:

```bash
# ONNX only
python3 -m vision_engine.export.export_all \
    --checkpoint checkpoints/best_model.pth \
    --output_dir exports \
    --num_classes 369 \
    --onnx-only

# CoreML only
python3 -m vision_engine.export.export_all \
    --checkpoint checkpoints/best_model.pth \
    --output_dir exports \
    --num_classes 369 \
    --coreml-only
```

## Model Performance

- **Top-1 Accuracy:** 83.46% (Target: >70% ✅)
- **Top-5 Accuracy:** 98.08% (Target: >90% ✅)
- **Classes:** 369 mathematical symbols (HASYv2 dataset)

## Notes

- Both models are exported from the same trained checkpoint (`checkpoints/best_model.pth`)
- Models expect normalized grayscale input (64x64 pixels)
- Output is raw logits/probabilities - apply softmax if needed
- For production use, consider model quantization for smaller file size

