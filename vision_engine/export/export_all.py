"""
Unified model export script for cross-platform deployment.

Exports trained PyTorch models to:
- ONNX format (Windows/Linux/Cross-platform)
- CoreML format (iOS/iPadOS/macOS)

Usage:
    python -m vision_engine.export.export_all \
        --checkpoint checkpoints/best_model.pth \
        --output_dir exports \
        --num_classes 369
"""

import argparse
import os
from pathlib import Path
from typing import Optional

from .onnx_export import export_checkpoint_to_onnx
from .coreml_export import export_checkpoint_to_coreml


def export_all_formats(
    checkpoint_path: str,
    output_dir: str = "exports",
    num_classes: int = 369,
    input_size: int = 64,
    export_onnx: bool = True,
    export_coreml: bool = True,
    class_labels: Optional[list] = None
) -> dict:
    """
    Export model to all supported formats for cross-platform deployment.
    
    Args:
        checkpoint_path: Path to PyTorch checkpoint file
        output_dir: Directory to save exported models
        num_classes: Number of classes (default: 369)
        input_size: Input image size (default: 64)
        export_onnx: Whether to export ONNX format (default: True)
        export_coreml: Whether to export CoreML format (default: True)
        class_labels: Optional list of class labels (for metadata)
    
    Returns:
        Dictionary with paths to exported models:
        {
            'onnx': 'path/to/model.onnx' or None,
            'coreml': 'path/to/model.mlpackage' or None
        }
    """
    # Create output directory
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    # Get checkpoint name for output file naming
    checkpoint_name = Path(checkpoint_path).stem
    
    results = {
        'onnx': None,
        'coreml': None
    }
    
    print("=" * 60)
    print("Cross-Platform Model Export")
    print("=" * 60)
    print(f"Checkpoint: {checkpoint_path}")
    print(f"Output directory: {output_dir}")
    print(f"Number of classes: {num_classes}")
    print(f"Input size: {input_size}x{input_size}")
    print()
    
    # Export to ONNX (Windows/Linux/Cross-platform)
    if export_onnx:
        try:
            print("📦 Exporting to ONNX format (Windows/Linux/Cross-platform)...")
            onnx_path = output_path / f"{checkpoint_name}.onnx"
            export_checkpoint_to_onnx(
                checkpoint_path=checkpoint_path,
                output_path=str(onnx_path),
                num_classes=num_classes,
                input_size=(input_size, input_size),
                device='cpu'
            )
            results['onnx'] = str(onnx_path)
            print(f"✅ ONNX export successful: {onnx_path}\n")
        except Exception as e:
            print(f"❌ ONNX export failed: {e}\n")
    
    # Export to CoreML (iOS/iPadOS/macOS)
    if export_coreml:
        try:
            print("🍎 Exporting to CoreML format (iOS/iPadOS/macOS)...")
            coreml_path = output_path / f"{checkpoint_name}.mlpackage"
            export_checkpoint_to_coreml(
                checkpoint_path=checkpoint_path,
                output_path=str(coreml_path),
                num_classes=num_classes,
                input_size=(input_size, input_size),
                class_labels=class_labels,
                device='cpu'
            )
            results['coreml'] = str(coreml_path)
            print(f"✅ CoreML export successful: {coreml_path}\n")
        except Exception as e:
            print(f"❌ CoreML export failed: {e}\n")
    
    # Summary
    print("=" * 60)
    print("Export Summary")
    print("=" * 60)
    if results['onnx']:
        print(f"✅ ONNX: {results['onnx']}")
        print(f"   → Use with ONNX Runtime on Windows/Linux")
    if results['coreml']:
        print(f"✅ CoreML: {results['coreml']}")
        print(f"   → Use with CoreML framework on iOS/iPadOS/macOS")
    print("=" * 60)
    
    return results


def main():
    parser = argparse.ArgumentParser(
        description='Export model to all supported formats for cross-platform deployment'
    )
    
    parser.add_argument(
        '--checkpoint', 
        type=str, 
        required=True,
        help='Path to PyTorch checkpoint file'
    )
    parser.add_argument(
        '--output_dir', 
        type=str, 
        default='exports',
        help='Directory to save exported models (default: exports)'
    )
    parser.add_argument(
        '--num_classes', 
        type=int, 
        default=369,
        help='Number of classes (default: 369)'
    )
    parser.add_argument(
        '--input_size', 
        type=int, 
        default=64,
        help='Input image size (default: 64)'
    )
    parser.add_argument(
        '--onnx-only', 
        action='store_true',
        help='Export only ONNX format'
    )
    parser.add_argument(
        '--coreml-only', 
        action='store_true',
        help='Export only CoreML format'
    )
    
    args = parser.parse_args()
    
    # Determine which formats to export
    export_onnx = not args.coreml_only
    export_coreml = not args.onnx_only
    
    # Export all formats
    export_all_formats(
        checkpoint_path=args.checkpoint,
        output_dir=args.output_dir,
        num_classes=args.num_classes,
        input_size=args.input_size,
        export_onnx=export_onnx,
        export_coreml=export_coreml
    )


if __name__ == '__main__':
    main()

