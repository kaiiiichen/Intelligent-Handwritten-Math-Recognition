"""
Utility functions for the Vision Engine.
"""

import torch
from typing import Tuple


def get_device() -> torch.device:
    """
    Get the best available device for training.
    
    Priority:
    1. MPS (Metal Performance Shaders) for Apple Silicon Macs
    2. CUDA for NVIDIA GPUs
    3. CPU as fallback
    
    Returns:
        torch.device: The best available device
    """
    if torch.backends.mps.is_available():
        return torch.device('mps')
    elif torch.cuda.is_available():
        return torch.device('cuda')
    else:
        return torch.device('cpu')


def get_device_info() -> Tuple[torch.device, str]:
    """
    Get device and device info string.
    
    Returns:
        Tuple of (device, info_string)
    """
    device = get_device()
    
    if device.type == 'mps':
        info = f"MPS (Metal Performance Shaders) - Apple Silicon"
    elif device.type == 'cuda':
        info = f"CUDA - {torch.cuda.get_device_name(0)}"
    else:
        info = "CPU"
    
    return device, info


def set_seed(seed: int = 42):
    """
    Set random seed for reproducibility.
    
    Args:
        seed: Random seed value
    """
    torch.manual_seed(seed)
    
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)
    
    # Note: MPS doesn't have manual_seed_all, but manual_seed should be sufficient
    if torch.backends.mps.is_available():
        torch.mps.manual_seed(seed)


def get_optimal_num_workers(device: torch.device) -> int:
    """
    Get optimal number of workers for DataLoader based on device.
    
    Args:
        device: The device being used
    
    Returns:
        Optimal number of workers
    """
    if device.type == 'mps':
        # MPS may have issues with multiple workers, use 0 or 2
        return 0
    elif device.type == 'cuda':
        # CUDA can handle more workers
        return 4
    else:
        # CPU can use multiple workers
        return 4

