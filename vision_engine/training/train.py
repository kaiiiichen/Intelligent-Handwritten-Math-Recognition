"""
Main training script for the Vision Engine.

Usage:
    python -m vision_engine.training.train \
        --csv_path data/hasyv2.csv \
        --data_root data/hasyv2 \
        --num_epochs 50 \
        --batch_size 64 \
        --learning_rate 0.001
"""

import argparse
import torch
import torch.nn as nn
from torch.utils.data import DataLoader

from ..data import get_hasyv2_dataloaders
from ..models import create_model
from ..utils import get_device, get_device_info, set_seed, get_optimal_num_workers
from .trainer import Trainer


def main():
    parser = argparse.ArgumentParser(description='Train symbol classification model')
    
    # Data arguments
    parser.add_argument('--csv_path', type=str, required=True,
                        help='Path to HASYv2 CSV file')
    parser.add_argument('--data_root', type=str, required=True,
                        help='Root directory containing HASYv2 images')
    parser.add_argument('--train_split', type=float, default=0.8,
                        help='Fraction of data for training (default: 0.8)')
    parser.add_argument('--val_split', type=float, default=0.1,
                        help='Fraction of data for validation (default: 0.1)')
    
    # Model arguments
    parser.add_argument('--input_size', type=int, default=64,
                        help='Input image size (default: 64)')
    parser.add_argument('--dropout', type=float, default=0.3,
                        help='Dropout rate (default: 0.3)')
    
    # Training arguments
    parser.add_argument('--num_epochs', type=int, default=50,
                        help='Number of training epochs (default: 50)')
    parser.add_argument('--batch_size', type=int, default=64,
                        help='Batch size (default: 64)')
    parser.add_argument('--learning_rate', type=float, default=0.001,
                        help='Learning rate (default: 0.001)')
    parser.add_argument('--weight_decay', type=float, default=1e-4,
                        help='Weight decay (default: 1e-4)')
    parser.add_argument('--num_workers', type=int, default=4,
                        help='Number of data loading workers (default: 4)')
    
    # Other arguments
    parser.add_argument('--save_dir', type=str, default='./checkpoints',
                        help='Directory to save checkpoints (default: ./checkpoints)')
    parser.add_argument('--seed', type=int, default=42,
                        help='Random seed (default: 42)')
    parser.add_argument('--augment', action='store_true', default=True,
                        help='Use data augmentation for training')
    
    args = parser.parse_args()
    
    # Set random seed
    set_seed(args.seed)
    
    # Get device (prioritize MPS for Mac, then CUDA, then CPU)
    device, device_info = get_device_info()
    print(f"Using device: {device} ({device_info})")
    
    # Adjust num_workers based on device
    if args.num_workers == 4:  # Only override if using default
        args.num_workers = get_optimal_num_workers(device)
        print(f"Using {args.num_workers} data loading workers")
    
    # Create dataloaders
    print("Loading dataset...")
    train_loader, val_loader, test_loader, class_info = get_hasyv2_dataloaders(
        csv_path=args.csv_path,
        data_root=args.data_root,
        train_split=args.train_split,
        val_split=args.val_split,
        batch_size=args.batch_size,
        num_workers=args.num_workers,
        target_size=(args.input_size, args.input_size),
        augment_train=args.augment
    )
    
    # Create model
    print("Creating model...")
    model = create_model(
        num_classes=class_info['num_classes'],
        input_size=args.input_size,
        dropout=args.dropout
    )
    print(f"Model created with {class_info['num_classes']} classes")
    
    # Create trainer
    trainer = Trainer(
        model=model,
        train_loader=train_loader,
        val_loader=val_loader,
        device=device,
        learning_rate=args.learning_rate,
        weight_decay=args.weight_decay,
        save_dir=args.save_dir
    )
    
    # Train
    history = trainer.train(num_epochs=args.num_epochs, save_best=True)
    
    print("\nTraining completed!")
    print(f"Best validation Top-1 accuracy: {max(history['val_top1']):.4f}")
    print(f"Best validation Top-5 accuracy: {max(history['val_top5']):.4f}")


if __name__ == '__main__':
    main()

