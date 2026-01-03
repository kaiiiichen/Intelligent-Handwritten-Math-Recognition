"""
Evaluation metrics for symbol classification.
"""

import torch
from typing import Tuple


def calculate_top_k_accuracy(
    predictions: torch.Tensor,
    targets: torch.Tensor,
    k: int = 5
) -> float:
    """
    Calculate top-k accuracy.
    
    Args:
        predictions: Model predictions (logits) of shape (batch_size, num_classes)
        targets: Ground truth labels of shape (batch_size,)
        k: Number of top predictions to consider
    
    Returns:
        Top-k accuracy as a float between 0 and 1
    """
    with torch.no_grad():
        _, top_k_indices = torch.topk(predictions, k, dim=1)
        correct = top_k_indices.eq(targets.view(-1, 1).expand_as(top_k_indices))
        top_k_acc = correct.any(dim=1).float().mean().item()
    
    return top_k_acc


def calculate_accuracy_metrics(
    predictions: torch.Tensor,
    targets: torch.Tensor
) -> Tuple[float, float]:
    """
    Calculate top-1 and top-5 accuracy.
    
    Args:
        predictions: Model predictions (logits) of shape (batch_size, num_classes)
        targets: Ground truth labels of shape (batch_size,)
    
    Returns:
        Tuple of (top_1_accuracy, top_5_accuracy)
    """
    top_1_acc = calculate_top_k_accuracy(predictions, targets, k=1)
    top_5_acc = calculate_top_k_accuracy(predictions, targets, k=5)
    
    return top_1_acc, top_5_acc

