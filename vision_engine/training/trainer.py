"""
Training utilities for the Vision Engine.
"""

import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader
from typing import Dict, Optional
import os
from tqdm import tqdm
import json

from ..models import SymbolClassifierCNN
from .metrics import calculate_accuracy_metrics


class Trainer:
    """
    Trainer class for symbol classification model.
    """
    
    def __init__(
        self,
        model: SymbolClassifierCNN,
        train_loader: DataLoader,
        val_loader: DataLoader,
        device: torch.device,
        learning_rate: float = 0.001,
        weight_decay: float = 1e-4,
        save_dir: str = "./checkpoints"
    ):
        self.model = model.to(device)
        self.train_loader = train_loader
        self.val_loader = val_loader
        self.device = device
        self.save_dir = save_dir
        
        # Create save directory
        os.makedirs(save_dir, exist_ok=True)
        
        # Loss function
        self.criterion = nn.CrossEntropyLoss()
        
        # Optimizer
        self.optimizer = optim.Adam(
            self.model.parameters(),
            lr=learning_rate,
            weight_decay=weight_decay
        )
        
        # Learning rate scheduler
        self.scheduler = optim.lr_scheduler.ReduceLROnPlateau(
            self.optimizer,
            mode='min',
            factor=0.5,
            patience=5
        )
        
        # Training history
        self.history = {
            'train_loss': [],
            'train_top1': [],
            'train_top5': [],
            'val_loss': [],
            'val_top1': [],
            'val_top5': []
        }
    
    def train_epoch(self) -> Dict[str, float]:
        """Train for one epoch."""
        self.model.train()
        running_loss = 0.0
        all_predictions = []
        all_targets = []
        
        pbar = tqdm(self.train_loader, desc="Training")
        for images, labels, _ in pbar:
            images = images.to(self.device)
            labels = labels.to(self.device)
            
            # Forward pass
            self.optimizer.zero_grad()
            outputs = self.model(images)
            loss = self.criterion(outputs, labels)
            
            # Backward pass
            loss.backward()
            self.optimizer.step()
            
            # Statistics
            running_loss += loss.item()
            all_predictions.append(outputs.detach().cpu())
            all_targets.append(labels.detach().cpu())
            
            # Update progress bar
            pbar.set_postfix({'loss': loss.item()})
        
        # Calculate metrics
        all_predictions = torch.cat(all_predictions, dim=0)
        all_targets = torch.cat(all_targets, dim=0)
        top1_acc, top5_acc = calculate_accuracy_metrics(all_predictions, all_targets)
        
        avg_loss = running_loss / len(self.train_loader)
        
        return {
            'loss': avg_loss,
            'top1': top1_acc,
            'top5': top5_acc
        }
    
    def validate(self) -> Dict[str, float]:
        """Validate the model."""
        self.model.eval()
        running_loss = 0.0
        all_predictions = []
        all_targets = []
        
        with torch.no_grad():
            pbar = tqdm(self.val_loader, desc="Validation")
            for images, labels, _ in pbar:
                images = images.to(self.device)
                labels = labels.to(self.device)
                
                # Forward pass
                outputs = self.model(images)
                loss = self.criterion(outputs, labels)
                
                # Statistics
                running_loss += loss.item()
                all_predictions.append(outputs.cpu())
                all_targets.append(labels.cpu())
        
        # Calculate metrics
        all_predictions = torch.cat(all_predictions, dim=0)
        all_targets = torch.cat(all_targets, dim=0)
        top1_acc, top5_acc = calculate_accuracy_metrics(all_predictions, all_targets)
        
        avg_loss = running_loss / len(self.val_loader)
        
        return {
            'loss': avg_loss,
            'top1': top1_acc,
            'top5': top5_acc
        }
    
    def train(self, num_epochs: int, save_best: bool = True) -> Dict:
        """
        Train the model for multiple epochs.
        
        Args:
            num_epochs: Number of epochs to train
            save_best: Whether to save the best model based on validation loss
        
        Returns:
            Training history dictionary
        """
        best_val_loss = float('inf')
        
        print(f"Starting training for {num_epochs} epochs...")
        print(f"Device: {self.device}")
        print(f"Model parameters: {sum(p.numel() for p in self.model.parameters()):,}")
        
        for epoch in range(num_epochs):
            print(f"\nEpoch {epoch + 1}/{num_epochs}")
            print("-" * 50)
            
            # Train
            train_metrics = self.train_epoch()
            self.history['train_loss'].append(train_metrics['loss'])
            self.history['train_top1'].append(train_metrics['top1'])
            self.history['train_top5'].append(train_metrics['top5'])
            
            # Validate
            val_metrics = self.validate()
            self.history['val_loss'].append(val_metrics['loss'])
            self.history['val_top1'].append(val_metrics['top1'])
            self.history['val_top5'].append(val_metrics['top5'])
            
            # Learning rate scheduling
            self.scheduler.step(val_metrics['loss'])
            
            # Print metrics
            print(f"Train - Loss: {train_metrics['loss']:.4f}, "
                  f"Top-1: {train_metrics['top1']:.4f}, "
                  f"Top-5: {train_metrics['top5']:.4f}")
            print(f"Val   - Loss: {val_metrics['loss']:.4f}, "
                  f"Top-1: {val_metrics['top1']:.4f}, "
                  f"Top-5: {val_metrics['top5']:.4f}")
            
            # Save best model
            if save_best and val_metrics['loss'] < best_val_loss:
                best_val_loss = val_metrics['loss']
                self.save_checkpoint(
                    os.path.join(self.save_dir, 'best_model.pth'),
                    epoch=epoch,
                    metrics=val_metrics
                )
                print(f"Saved best model (val_loss: {best_val_loss:.4f})")
        
        # Save final model and history
        self.save_checkpoint(
            os.path.join(self.save_dir, 'final_model.pth'),
            epoch=num_epochs - 1,
            metrics=val_metrics
        )
        self.save_history(os.path.join(self.save_dir, 'training_history.json'))
        
        return self.history
    
    def save_checkpoint(
        self,
        filepath: str,
        epoch: int,
        metrics: Dict[str, float]
    ):
        """Save model checkpoint."""
        checkpoint = {
            'epoch': epoch,
            'model_state_dict': self.model.state_dict(),
            'optimizer_state_dict': self.optimizer.state_dict(),
            'scheduler_state_dict': self.scheduler.state_dict(),
            'metrics': metrics,
            'model_config': {
                'num_classes': self.model.num_classes,
                'input_size': self.model.input_size
            }
        }
        torch.save(checkpoint, filepath)
    
    def load_checkpoint(self, filepath: str):
        """Load model checkpoint."""
        checkpoint = torch.load(filepath, map_location=self.device)
        self.model.load_state_dict(checkpoint['model_state_dict'])
        self.optimizer.load_state_dict(checkpoint['optimizer_state_dict'])
        self.scheduler.load_state_dict(checkpoint['scheduler_state_dict'])
        return checkpoint
    
    def save_history(self, filepath: str):
        """Save training history to JSON."""
        with open(filepath, 'w') as f:
            json.dump(self.history, f, indent=2)

