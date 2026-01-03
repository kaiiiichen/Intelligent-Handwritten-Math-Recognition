"""
ONNX export utilities for the Vision Engine.
"""

import torch
import onnx
import onnxruntime as ort
from typing import Optional, Tuple
import os

from ..models import SymbolClassifierCNN


def export_to_onnx(
    model: SymbolClassifierCNN,
    output_path: str,
    input_size: Tuple[int, int] = (64, 64),
    opset_version: int = 11,
    verify: bool = True
) -> str:
    """
    Export PyTorch model to ONNX format.
    
    Args:
        model: Trained SymbolClassifierCNN model
        output_path: Path to save the ONNX model
        input_size: Input image size (height, width)
        opset_version: ONNX opset version (default: 11)
        verify: Whether to verify the exported model (default: True)
    
    Returns:
        Path to the exported ONNX model
    """
    model.eval()
    
    # Create dummy input
    dummy_input = torch.randn(1, 1, input_size[0], input_size[1])
    
    # Export to ONNX
    print(f"Exporting model to ONNX format...")
    print(f"Input shape: {dummy_input.shape}")
    print(f"Output path: {output_path}")
    
    torch.onnx.export(
        model,
        dummy_input,
        output_path,
        export_params=True,
        opset_version=opset_version,
        do_constant_folding=True,
        input_names=['input'],
        output_names=['output'],
        dynamic_axes={
            'input': {0: 'batch_size'},
            'output': {0: 'batch_size'}
        }
    )
    
    print(f"Model exported successfully to {output_path}")
    
    # Verify the exported model
    if verify:
        print("Verifying exported model...")
        onnx_model = onnx.load(output_path)
        onnx.checker.check_model(onnx_model)
        print("Model verification passed!")
        
        # Test inference with ONNX Runtime
        print("Testing ONNX Runtime inference...")
        ort_session = ort.InferenceSession(output_path)
        ort_inputs = {ort_session.get_inputs()[0].name: dummy_input.numpy()}
        ort_outputs = ort_session.run(None, ort_inputs)
        print(f"ONNX Runtime output shape: {ort_outputs[0].shape}")
        print("ONNX Runtime inference test passed!")
    
    return output_path


def export_checkpoint_to_onnx(
    checkpoint_path: str,
    output_path: str,
    num_classes: int = 369,
    input_size: Tuple[int, int] = (64, 64),
    device: str = 'cpu'
) -> str:
    """
    Export a model checkpoint to ONNX format.
    
    Note: ONNX export should typically be done on CPU to ensure compatibility.
    If device is 'mps' or 'cuda', the model will be loaded on that device but
    moved to CPU for export.
    """
    """
    Export a model checkpoint to ONNX format.
    
    Args:
        checkpoint_path: Path to PyTorch checkpoint file
        output_path: Path to save the ONNX model
        num_classes: Number of classes (default: 369)
        input_size: Input image size (default: (64, 64))
        device: Device to load the model on (default: 'cpu')
    
    Returns:
        Path to the exported ONNX model
    """
    from ..models import create_model
    
    # Load checkpoint (use CPU for loading to ensure compatibility)
    load_device = 'cpu'  # Always load on CPU for ONNX export compatibility
    checkpoint = torch.load(checkpoint_path, map_location=load_device)
    
    # Get model config from checkpoint if available
    if 'model_config' in checkpoint:
        config = checkpoint['model_config']
        num_classes = config.get('num_classes', num_classes)
        input_size = (config.get('input_size', input_size[0]), input_size[1])
    
    # Create model and load on CPU (ONNX export requires CPU)
    model = create_model(num_classes=num_classes, input_size=input_size[0])
    model.load_state_dict(checkpoint['model_state_dict'])
    model.eval()
    model = model.to('cpu')  # Ensure model is on CPU for export
    
    # Export (ONNX export must be done on CPU)
    return export_to_onnx(model, output_path, input_size=input_size)

