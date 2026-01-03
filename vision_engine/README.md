# Vision Engine

The Vision Engine is responsible for classifying drawn mathematical symbols into symbol class hypotheses using deep learning models.

## Overview

The Vision Engine consists of:

- **Data Pipeline**: Loading and preprocessing HASYv2 dataset
- **Model**: Lightweight CNN for symbol classification
- **Training**: Training scripts with top-1/top-5 accuracy metrics
- **Export**: Model export to ONNX format for deployment

## Dataset

### HASYv2 Dataset

HASYv2 is a dataset of 168,233 handwritten mathematical symbol images across 369 classes.

**Download:**

1. Download the HASYv2 dataset from the official repository
2. Extract the dataset to a directory (e.g., `data/hasyv2/`)
3. Ensure the CSV file (e.g., `hasyv2.csv`) is in the dataset root

**Dataset Structure:**

```
data/
└── hasyv2/
    ├── hasyv2.csv          # Dataset metadata
    └── symbols/            # Image files
        ├── symbol_001.png
        ├── symbol_002.png
        └── ...
```

## Hardware Support

The Vision Engine supports multiple hardware backends:

- **MPS (Metal Performance Shaders)**: For Apple Silicon Macs (M1, M2, M3, M4, etc.) - **Recommended for Mac users**
- **CUDA**: For NVIDIA GPUs
- **CPU**: Fallback option

The training script automatically detects and uses the best available device.

## Usage

### 1. Data Loading

```python
from vision_engine.data import get_hasyv2_dataloaders

train_loader, val_loader, test_loader, class_info = get_hasyv2_dataloaders(
    csv_path='data/hasyv2/hasyv2.csv',
    data_root='data/hasyv2',
    batch_size=64,
    target_size=(64, 64),
    augment_train=True
)
```

### 2. Model Creation

```python
from vision_engine.models import create_model

model = create_model(
    num_classes=369,  # Number of symbol classes
    input_size=64,
    dropout=0.3
)
```

### 3. Training

```bash
python -m vision_engine.training.train \
    --csv_path data/hasyv2/hasyv2.csv \
    --data_root data/hasyv2 \
    --num_epochs 50 \
    --batch_size 64 \
    --learning_rate 0.001 \
    --save_dir checkpoints
```

### 4. Model Export

Export trained model to ONNX format:

```bash
python -m vision_engine.export.export_model \
    --checkpoint checkpoints/best_model.pth \
    --output model.onnx \
    --num_classes 369
```

## Model Architecture

The baseline CNN model consists of:

- 4 convolutional layers with batch normalization
- Global average pooling
- 2 fully connected layers with dropout
- Optimized for 64x64 grayscale input images

**Model Size:** ~2-3 MB (suitable for mobile deployment)

## Evaluation Metrics

The training script reports:

- **Top-1 Accuracy**: Percentage of correct predictions (exact match)
- **Top-5 Accuracy**: Percentage of correct predictions in top-5 candidates

These metrics are crucial for the symbol suggestion use case, where users can choose from a ranked list.

## Data Preprocessing

The data pipeline performs:

1. Grayscale conversion
2. Binarization (Otsu thresholding)
3. Bounding box cropping
4. Square padding
5. Resize to target size (64x64)
6. Normalization to [-1, 1]

## Data Augmentation

Training data augmentation includes:

- Random rotation (±10 degrees)
- Random translation (±5%)
- Normalization

## Next Steps

After training:

1. Evaluate on test set
2. Export to ONNX for inference
3. Integrate with Semantic Suggestion Engine for LaTeX candidate ranking
