# Vision Engine

**Status:** ✅ **Complete** - Trained model ready for deployment

## Performance

- **Top-1 Accuracy:** 83.46% (target: 70%)
- **Top-5 Accuracy:** 98.08% (target: 90%)
- **Model Size:** 2.9MB (CoreML), 32KB (ONNX)
- **Classes:** 369 mathematical symbols

## Exported Models

- `../exports/best_model.mlpackage` - CoreML (macOS/iOS)
- `../exports/best_model.onnx` - ONNX (Windows/Linux)

## Architecture

- 4-layer CNN with batch normalization
- Global average pooling
- Optimized for mobile deployment
- Input: 64x64 grayscale images

## Training Complete

All training artifacts in `../checkpoints/`:

- `best_model.pth` - PyTorch checkpoint
- `training_history.json` - Training metrics
- Model ready for production use
