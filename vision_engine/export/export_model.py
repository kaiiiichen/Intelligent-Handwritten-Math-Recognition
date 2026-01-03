"""
Script to export trained model to ONNX format.

Usage:
    python -m vision_engine.export.export_model \
        --checkpoint checkpoints/best_model.pth \
        --output model.onnx \
        --num_classes 369
"""

import argparse
from .onnx_export import export_checkpoint_to_onnx


def main():
    parser = argparse.ArgumentParser(description='Export model to ONNX')
    
    parser.add_argument('--checkpoint', type=str, required=True,
                        help='Path to PyTorch checkpoint file')
    parser.add_argument('--output', type=str, required=True,
                        help='Path to save ONNX model')
    parser.add_argument('--num_classes', type=int, default=369,
                        help='Number of classes (default: 369)')
    parser.add_argument('--input_size', type=int, default=64,
                        help='Input image size (default: 64)')
    parser.add_argument('--device', type=str, default='cpu',
                        help='Device to load model on (default: cpu)')
    
    args = parser.parse_args()
    
    export_checkpoint_to_onnx(
        checkpoint_path=args.checkpoint,
        output_path=args.output,
        num_classes=args.num_classes,
        input_size=(args.input_size, args.input_size),
        device=args.device
    )
    
    print(f"\nModel exported successfully to {args.output}")


if __name__ == '__main__':
    main()

