"""
Integration module connecting Vision Engine and Semantic Suggestion Engine.

This module provides a unified interface for:
1. Taking image input (or Vision Engine predictions)
2. Getting ranked LaTeX candidate suggestions
3. Rendering previews for candidates
"""

from typing import List, Optional, Tuple
import numpy as np
from pathlib import Path

from semantic_engine.mapping_db.symbol_mapping import SymbolMappingDatabase
from semantic_engine.ranking.ranker import CandidateRanker, RankedCandidate
from semantic_engine.rendering.latex_renderer import LaTeXRenderer, create_renderer


class SemanticSuggestionEngine:
    """
    Main integration class that combines Vision Engine outputs with semantic ranking.
    
    This is the primary interface for the complete suggestion system:
    - Takes Vision Engine predictions (or raw image)
    - Maps to LaTeX candidates using the mapping database
    - Ranks candidates by combining visual confidence and mathematical priority
    - Optionally renders previews
    """
    
    def __init__(
        self,
        mapping_db: Optional[SymbolMappingDatabase] = None,
        ranker: Optional[CandidateRanker] = None,
        renderer: Optional[LaTeXRenderer] = None,
        load_full_mapping: bool = True
    ):
        """
        Initialize the Semantic Suggestion Engine.
        
        Args:
            mapping_db: Symbol mapping database. If None, creates a new one.
            ranker: Candidate ranker. If None, creates a default one.
            renderer: LaTeX renderer. If None, creates a default one.
            load_full_mapping: If True, loads the full mapping database from JSON file.
        """
        # Initialize mapping database
        if mapping_db is None:
            mapping_db = SymbolMappingDatabase()
            if load_full_mapping:
                # Try to load full mapping database
                full_mapping_path = Path(__file__).parent / "mapping_db" / "symbol_mapping_full.json"
                if full_mapping_path.exists():
                    try:
                        mapping_db.load_full_mapping(str(full_mapping_path))
                    except Exception as e:
                        print(f"Warning: Could not load full mapping database: {e}")
                        print("Using default mappings only.")
        
        self.mapping_db = mapping_db
        
        # Initialize ranker
        if ranker is None:
            ranker = CandidateRanker(mapping_db=self.mapping_db)
        self.ranker = ranker
        
        # Initialize renderer (optional, for preview generation)
        self.renderer = renderer
    
    def suggest_latex_candidates(
        self,
        vision_predictions: np.ndarray,
        top_k: int = 10,
        include_previews: bool = False
    ) -> List[RankedCandidate]:
        """
        Get ranked LaTeX candidate suggestions from Vision Engine predictions.
        
        Args:
            vision_predictions: Vision Engine output (logits or probabilities) of shape (num_classes,)
                               or (1, num_classes)
            top_k: Maximum number of candidates to return
            include_previews: If True, generates preview images (requires renderer)
        
        Returns:
            List of RankedCandidate objects, sorted by combined score (descending)
        """
        # Rank candidates
        candidates = self.ranker.rank_candidates(
            vision_predictions,
            top_k_symbols=5,  # Consider top 5 symbol classes
            top_k_candidates_per_symbol=3  # Up to 3 LaTeX candidates per symbol
        )
        
        # Limit to top_k
        candidates = candidates[:top_k]
        
        # Generate previews if requested
        if include_previews and self.renderer:
            # Note: Preview generation would be done here
            # For now, we just return the candidates
            # In a full implementation, you might attach preview data to candidates
            pass
        
        return candidates
    
    def suggest_from_top_k_symbols(
        self,
        top_k_symbols: List[Tuple[int, float]],
        top_k: int = 10
    ) -> List[RankedCandidate]:
        """
        Get ranked LaTeX candidates from a list of top-k symbol predictions.
        
        This is useful when you already have top-k results from Vision Engine.
        
        Args:
            top_k_symbols: List of (symbol_class_id, confidence) tuples
            top_k: Maximum number of candidates to return
        
        Returns:
            List of RankedCandidate objects, sorted by combined score (descending)
        """
        candidates = self.ranker.rank_candidates_from_top_k(
            top_k_symbols,
            top_k_candidates_per_symbol=3
        )
        
        return candidates[:top_k]
    
    def get_candidate_info(self, candidate: RankedCandidate) -> dict:
        """
        Get detailed information about a candidate.
        
        Args:
            candidate: RankedCandidate object
        
        Returns:
            Dictionary with candidate information
        """
        return {
            "latex_command": candidate.latex_command,
            "symbol_class_id": candidate.symbol_class_id,
            "vision_confidence": candidate.vision_confidence,
            "math_priority": candidate.math_priority,
            "combined_score": candidate.combined_score,
            "context": candidate.context,
            "description": candidate.description
        }
    
    def format_suggestion_list(
        self,
        candidates: List[RankedCandidate],
        max_items: int = 5
    ) -> List[str]:
        """
        Format candidates as a human-readable list.
        
        Args:
            candidates: List of RankedCandidate objects
            max_items: Maximum number of items to include
        
        Returns:
            List of formatted strings
        """
        formatted = []
        for i, cand in enumerate(candidates[:max_items], 1):
            formatted.append(
                f"{i}. {cand.latex_command:20} "
                f"(confidence: {cand.vision_confidence:.2f}, "
                f"priority: {cand.math_priority:.2f}, "
                f"score: {cand.combined_score:.3f}) - {cand.context}"
            )
        return formatted


def create_suggestion_engine(
    vision_weight: float = 0.6,
    math_weight: float = 0.4,
    load_full_mapping: bool = True
) -> SemanticSuggestionEngine:
    """
    Create a Semantic Suggestion Engine with default settings.
    
    Args:
        vision_weight: Weight for vision confidence in ranking (default: 0.6)
        math_weight: Weight for math priority in ranking (default: 0.4)
        load_full_mapping: If True, loads the full mapping database
    
    Returns:
        SemanticSuggestionEngine instance
    """
    mapping_db = SymbolMappingDatabase()
    if load_full_mapping:
        full_mapping_path = Path(__file__).parent / "mapping_db" / "symbol_mapping_full.json"
        if full_mapping_path.exists():
            try:
                mapping_db.load_full_mapping(str(full_mapping_path))
            except Exception as e:
                print(f"Warning: Could not load full mapping database: {e}")
    
    ranker = CandidateRanker(
        mapping_db=mapping_db,
        vision_weight=vision_weight,
        math_weight=math_weight
    )
    
    return SemanticSuggestionEngine(
        mapping_db=mapping_db,
        ranker=ranker,
        renderer=None  # Renderer is optional
    )

