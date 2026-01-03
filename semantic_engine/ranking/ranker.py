"""
Ranking algorithm for combining Vision Engine outputs with LaTeX candidate mappings.

This module implements the core ranking logic that combines:
- Vision Engine confidence scores (visual similarity)
- Mathematical priority from mapping database (semantic appropriateness)
- Optional user preferences (future enhancement)
"""

from typing import List, Dict, Optional, Tuple
import numpy as np
from dataclasses import dataclass

from semantic_engine.mapping_db.symbol_mapping import (
    SymbolMappingDatabase,
    LaTeXCandidate,
    SymbolMapping
)


@dataclass
class RankedCandidate:
    """A ranked LaTeX candidate with combined scores."""
    latex_command: str
    symbol_class_id: int
    vision_confidence: float  # From Vision Engine (0.0-1.0)
    math_priority: float  # From mapping database (0.0-1.0)
    combined_score: float  # Combined ranking score
    context: str  # Brief context description
    description: Optional[str] = None  # Optional detailed description
    
    def __lt__(self, other):
        """For sorting: higher combined_score comes first."""
        return self.combined_score > other.combined_score


class CandidateRanker:
    """
    Ranks LaTeX candidates by combining Vision Engine confidence with mathematical priority.
    
    Ranking Formula:
        combined_score = α * vision_confidence + β * math_priority
    
    Where:
        - α (vision_weight): Weight for visual confidence (default: 0.6)
        - β (math_weight): Weight for mathematical priority (default: 0.4)
    
    This ensures that:
    1. High visual confidence symbols are prioritized
    2. Mathematically appropriate symbols are preferred over generic alternatives
    3. The balance can be adjusted based on use case
    """
    
    def __init__(
        self,
        mapping_db: Optional[SymbolMappingDatabase] = None,
        vision_weight: float = 0.6,
        math_weight: float = 0.4
    ):
        """
        Initialize the ranker.
        
        Args:
            mapping_db: Symbol mapping database. If None, creates a new one.
            vision_weight: Weight for vision confidence in combined score (default: 0.6)
            math_weight: Weight for math priority in combined score (default: 0.4)
        """
        if mapping_db is None:
            mapping_db = SymbolMappingDatabase()
        self.mapping_db = mapping_db
        
        # Validate weights
        total_weight = vision_weight + math_weight
        if abs(total_weight - 1.0) > 1e-6:
            raise ValueError(
                f"Weights must sum to 1.0, got {total_weight:.6f}. "
                f"vision_weight={vision_weight}, math_weight={math_weight}"
            )
        
        self.vision_weight = vision_weight
        self.math_weight = math_weight
    
    def rank_candidates(
        self,
        vision_predictions: np.ndarray,
        top_k_symbols: int = 5,
        top_k_candidates_per_symbol: int = 3
    ) -> List[RankedCandidate]:
        """
        Rank LaTeX candidates from Vision Engine predictions.
        
        Args:
            vision_predictions: Vision Engine output (logits or probabilities) of shape (num_classes,)
                               or (1, num_classes). Values should be in [0, 1] range (apply softmax if needed).
            top_k_symbols: Number of top symbol classes to consider from Vision Engine
            top_k_candidates_per_symbol: Maximum number of LaTeX candidates per symbol class
        
        Returns:
            List of RankedCandidate objects, sorted by combined_score (descending)
        """
        # Flatten and normalize predictions
        if vision_predictions.ndim > 1:
            vision_predictions = vision_predictions.flatten()
        
        # Apply softmax if values are logits (not already probabilities)
        # Check if values are in reasonable probability range
        if vision_predictions.min() < 0 or vision_predictions.max() > 1.0:
            # Likely logits, apply softmax
            exp_preds = np.exp(vision_predictions - np.max(vision_predictions))
            vision_predictions = exp_preds / exp_preds.sum()
        
        # Get top-k symbol classes from Vision Engine
        top_k_indices = np.argsort(vision_predictions)[-top_k_symbols:][::-1]
        top_k_confidences = vision_predictions[top_k_indices]
        
        # Collect all candidates from top-k symbols
        all_candidates = []
        
        for symbol_id, confidence in zip(top_k_indices, top_k_confidences):
            # Get LaTeX candidates for this symbol
            latex_candidates = self.mapping_db.get_ranked_candidates(symbol_id)
            
            if not latex_candidates:
                # No mapping found, create a default candidate
                # This handles symbols not yet in the mapping database
                all_candidates.append(
                    RankedCandidate(
                        latex_command=f"\\symbol_{symbol_id}",  # Placeholder
                        symbol_class_id=int(symbol_id),
                        vision_confidence=float(confidence),
                        math_priority=0.5,  # Default neutral priority
                        combined_score=float(confidence * self.vision_weight + 0.5 * self.math_weight),
                        context="symbol (no mapping available)",
                        description=f"Symbol class {symbol_id} - mapping not yet available"
                    )
                )
                continue
            
            # Create ranked candidates for each LaTeX option
            for latex_cand in latex_candidates[:top_k_candidates_per_symbol]:
                combined_score = (
                    confidence * self.vision_weight +
                    latex_cand.math_priority * self.math_weight
                )
                
                all_candidates.append(
                    RankedCandidate(
                        latex_command=latex_cand.command,
                        symbol_class_id=int(symbol_id),
                        vision_confidence=float(confidence),
                        math_priority=latex_cand.math_priority,
                        combined_score=combined_score,
                        context=latex_cand.context,
                        description=latex_cand.description
                    )
                )
        
        # Sort by combined score (descending)
        all_candidates.sort()
        
        return all_candidates
    
    def rank_candidates_from_top_k(
        self,
        top_k_symbols: List[Tuple[int, float]],
        top_k_candidates_per_symbol: int = 3
    ) -> List[RankedCandidate]:
        """
        Rank LaTeX candidates from a list of top-k symbol predictions.
        
        This is useful when you already have top-k results from Vision Engine.
        
        Args:
            top_k_symbols: List of (symbol_class_id, confidence) tuples
            top_k_candidates_per_symbol: Maximum number of LaTeX candidates per symbol class
        
        Returns:
            List of RankedCandidate objects, sorted by combined_score (descending)
        """
        all_candidates = []
        
        for symbol_id, confidence in top_k_symbols:
            # Get LaTeX candidates for this symbol
            latex_candidates = self.mapping_db.get_ranked_candidates(symbol_id)
            
            if not latex_candidates:
                # No mapping found, create a default candidate
                all_candidates.append(
                    RankedCandidate(
                        latex_command=f"\\symbol_{symbol_id}",
                        symbol_class_id=symbol_id,
                        vision_confidence=confidence,
                        math_priority=0.5,
                        combined_score=confidence * self.vision_weight + 0.5 * self.math_weight,
                        context="symbol (no mapping available)",
                        description=f"Symbol class {symbol_id} - mapping not yet available"
                    )
                )
                continue
            
            # Create ranked candidates for each LaTeX option
            for latex_cand in latex_candidates[:top_k_candidates_per_symbol]:
                combined_score = (
                    confidence * self.vision_weight +
                    latex_cand.math_priority * self.math_weight
                )
                
                all_candidates.append(
                    RankedCandidate(
                        latex_command=latex_cand.command,
                        symbol_class_id=symbol_id,
                        vision_confidence=confidence,
                        math_priority=latex_cand.math_priority,
                        combined_score=combined_score,
                        context=latex_cand.context,
                        description=latex_cand.description
                    )
                )
        
        # Sort by combined score (descending)
        all_candidates.sort()
        
        return all_candidates


def create_default_ranker() -> CandidateRanker:
    """Create a ranker with default settings."""
    return CandidateRanker()


def create_vision_heavy_ranker() -> CandidateRanker:
    """Create a ranker that heavily weights visual confidence (80% vision, 20% math)."""
    return CandidateRanker(vision_weight=0.8, math_weight=0.2)


def create_math_heavy_ranker() -> CandidateRanker:
    """Create a ranker that heavily weights mathematical priority (40% vision, 60% math)."""
    return CandidateRanker(vision_weight=0.4, math_weight=0.6)

