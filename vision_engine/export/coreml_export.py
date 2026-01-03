"""
CoreML export utilities for the Vision Engine.

Supports exporting PyTorch models to CoreML format for deployment on
iOS, iPadOS, and macOS platforms.
"""

import torch
import coremltools as ct
from typing import Tuple, Optional
import os

from ..models import SymbolClassifierCNN


def export_to_coreml(
    model: SymbolClassifierCNN,
    output_path: str,
    input_size: Tuple[int, int] = (64, 64),
    class_labels: Optional[list] = None,
    verify: bool = True
) -> str:
    """
    Export PyTorch model to CoreML format.
    
    Args:
        model: Trained SymbolClassifierCNN model
        output_path: Path to save the CoreML model (.mlpackage)
        input_size: Input image size (height, width)
        class_labels: Optional list of class labels (for metadata)
        verify: Whether to verify the exported model (default: True)
    
    Returns:
        Path to the exported CoreML model
    """
    model.eval()
    
    # Create dummy input
    dummy_input = torch.randn(1, 1, input_size[0], input_size[1])
    
    # Trace the model
    print(f"Tracing model for CoreML export...")
    print(f"Input shape: {dummy_input.shape}")
    
    # Trace the model (convert to TorchScript)
    traced_model = torch.jit.trace(model, dummy_input)
    
    # Convert to CoreML
    print(f"Converting to CoreML format...")
    print(f"Output path: {output_path}")
    
    # Convert to CoreML
    # Use simpler API for better compatibility
    mlmodel = ct.convert(
        traced_model,
        inputs=[ct.TensorType(name="input", shape=dummy_input.shape)],
        minimum_deployment_target=ct.target.iOS13,  # Support iOS 13+
        compute_units=ct.ComputeUnit.ALL,  # Use CPU, GPU, and Neural Engine
    )
    
    # Add metadata
    mlmodel.author = "Intelligent Handwritten Math Recognition"
    mlmodel.short_description = "Mathematical symbol classifier for LaTeX input assistance"
    mlmodel.version = "1.0"
    
    # Add class labels if provided
    if class_labels:
        mlmodel.output_description["output"] = f"Probability distribution over {len(class_labels)} symbol classes"
    
    # Save the model
    mlmodel.save(output_path)
    print(f"CoreML model exported successfully to {output_path}")
    
    # Verify the exported model
    if verify:
        print("Verifying exported CoreML model...")
        try:
            # Load and verify
            loaded_model = ct.models.MLModel(output_path)
            print("CoreML model verification passed!")
            
            # Print model metadata
            print(f"\nModel Metadata:")
            print(f"  Input: {loaded_model.input_description}")
            print(f"  Output: {loaded_model.output_description}")
            print(f"  Author: {loaded_model.author}")
            print(f"  Version: {loaded_model.version}")
        except Exception as e:
            print(f"Warning: CoreML model verification failed: {e}")
    
    return output_path


def export_checkpoint_to_coreml(
    checkpoint_path: str,
    output_path: str,
    num_classes: int = 369,
    input_size: Tuple[int, int] = (64, 64),
    class_labels: Optional[list] = None,
    device: str = 'cpu'
) -> str:
    """
    Export a model checkpoint to CoreML format.
    
    Args:
        checkpoint_path: Path to PyTorch checkpoint file
        output_path: Path to save the CoreML model (.mlpackage)
        num_classes: Number of classes (default: 369)
        input_size: Input image size (default: (64, 64))
        class_labels: Optional list of class labels (for metadata)
        device: Device to load the model on (default: 'cpu')
    
    Returns:
        Path to the exported CoreML model
    
    Note:
        CoreML export should be done on CPU to ensure compatibility.
        The model will be loaded on the specified device but moved to CPU for export.
    """
    from ..models import create_model
    
    # Load checkpoint (use CPU for loading to ensure compatibility)
    load_device = 'cpu'  # Always load on CPU for CoreML export compatibility
    checkpoint = torch.load(checkpoint_path, map_location=load_device)
    
    # Get model config from checkpoint if available
    if 'model_config' in checkpoint:
        config = checkpoint['model_config']
        num_classes = config.get('num_classes', num_classes)
        input_size = (config.get('input_size', input_size[0]), input_size[1])
    
    # Create model and load on CPU (CoreML export requires CPU)
    model = create_model(num_classes=num_classes, input_size=input_size[0])
    model.load_state_dict(checkpoint['model_state_dict'])
    model.eval()
    model = model.to('cpu')  # Ensure model is on CPU for export
    
    # Export (CoreML export must be done on CPU)
    return export_to_coreml(
        model, 
        output_path, 
        input_size=input_size,
        class_labels=class_labels
    )

