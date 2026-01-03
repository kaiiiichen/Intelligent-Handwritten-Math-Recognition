"""
Example usage of the Semantic Suggestion Engine.

This script demonstrates how to use the complete suggestion system:
1. Simulate Vision Engine predictions
2. Get ranked LaTeX candidate suggestions
3. Display results
"""

import numpy as np
from semantic_engine import create_suggestion_engine


def simulate_vision_predictions(symbol_id: int, confidence: float = 0.9) -> np.ndarray:
    """
    Simulate Vision Engine predictions for a given symbol.
    
    Args:
        symbol_id: Symbol class ID (0-indexed, but our database uses actual IDs)
        confidence: Confidence score for the predicted symbol
    
    Returns:
        Array of shape (369,) with predictions
    """
    predictions = np.zeros(369)
    # Note: symbol_id in our database might not match array index
    # This is a simplified simulation
    if 0 <= symbol_id < 369:
        predictions[symbol_id] = confidence
        # Add some noise for other symbols
        predictions += np.random.rand(369) * 0.1
        # Normalize
        predictions = predictions / predictions.sum()
    return predictions


def example_basic_usage():
    """Basic example of using the suggestion engine."""
    print("=" * 70)
    print("Example 1: Basic Usage")
    print("=" * 70)
    
    # Create suggestion engine
    engine = create_suggestion_engine()
    
    # Simulate Vision Engine output for symbol ID 59 (\rightarrow)
    # In reality, this would come from the actual Vision Engine model
    vision_output = simulate_vision_predictions(59, confidence=0.85)
    
    # Get ranked suggestions
    candidates = engine.suggest_latex_candidates(vision_output, top_k=5)
    
    print(f"\nVision Engine predicted symbol with confidence 0.85")
    print(f"Top {len(candidates)} LaTeX candidate suggestions:\n")
    
    for i, cand in enumerate(candidates, 1):
        print(f"{i}. {cand.latex_command:20} "
              f"(vision: {cand.vision_confidence:.3f}, "
              f"math: {cand.math_priority:.3f}, "
              f"combined: {cand.combined_score:.3f})")
        print(f"   Context: {cand.context}")
        if cand.description:
            print(f"   {cand.description}")
        print()


def example_multiple_symbols():
    """Example showing suggestions for multiple symbols."""
    print("\n" + "=" * 70)
    print("Example 2: Multiple Symbols")
    print("=" * 70)
    
    engine = create_suggestion_engine()
    
    # Test different symbols
    test_symbols = [
        (59, 0.9, "\\rightarrow"),  # Right arrow
        (88, 0.85, "\\sum"),  # Sum
        (185, 0.8, "\\leq"),  # Less than or equal
        (882, 0.95, "\\forall"),  # For all
    ]
    
    for symbol_id, confidence, expected_latex in test_symbols:
        print(f"\n--- Symbol ID {symbol_id} (expected: {expected_latex}) ---")
        vision_output = simulate_vision_predictions(symbol_id, confidence)
        candidates = engine.suggest_latex_candidates(vision_output, top_k=3)
        
        for i, cand in enumerate(candidates, 1):
            print(f"  {i}. {cand.latex_command:20} "
                  f"(score: {cand.combined_score:.3f}) - {cand.context}")


def example_from_top_k():
    """Example using top-k symbols directly."""
    print("\n" + "=" * 70)
    print("Example 3: Using Top-K Symbols")
    print("=" * 70)
    
    engine = create_suggestion_engine()
    
    # Simulate top-k results from Vision Engine
    # Format: [(symbol_id, confidence), ...]
    top_k_symbols = [
        (59, 0.85),   # \rightarrow
        (753, 0.12),   # \Rightarrow (alternative)
        (761, 0.08),   # \leftarrow (less likely)
    ]
    
    print("\nTop-k symbols from Vision Engine:")
    for symbol_id, conf in top_k_symbols:
        print(f"  Symbol ID {symbol_id}: {conf:.3f}")
    
    # Get ranked suggestions
    candidates = engine.suggest_from_top_k_symbols(top_k_symbols, top_k=5)
    
    print(f"\nTop {len(candidates)} ranked LaTeX candidates:\n")
    for i, cand in enumerate(candidates, 1):
        print(f"{i}. {cand.latex_command:20} "
              f"(vision: {cand.vision_confidence:.3f}, "
              f"math: {cand.math_priority:.3f}, "
              f"combined: {cand.combined_score:.3f})")
        print(f"   Context: {cand.context}")


def example_custom_weights():
    """Example with custom ranking weights."""
    print("\n" + "=" * 70)
    print("Example 4: Custom Ranking Weights")
    print("=" * 70)
    
    # Create engine with math-heavy weighting (prioritize mathematical correctness)
    math_heavy_engine = create_suggestion_engine(
        vision_weight=0.4,
        math_weight=0.6
    )
    
    # Create engine with vision-heavy weighting (prioritize visual similarity)
    vision_heavy_engine = create_suggestion_engine(
        vision_weight=0.8,
        math_weight=0.2
    )
    
    vision_output = simulate_vision_predictions(59, confidence=0.85)
    
    print("\n--- Math-Heavy Ranking (40% vision, 60% math) ---")
    candidates_math = math_heavy_engine.suggest_latex_candidates(vision_output, top_k=3)
    for i, cand in enumerate(candidates_math, 1):
        print(f"  {i}. {cand.latex_command:20} (score: {cand.combined_score:.3f})")
    
    print("\n--- Vision-Heavy Ranking (80% vision, 20% math) ---")
    candidates_vision = vision_heavy_engine.suggest_latex_candidates(vision_output, top_k=3)
    for i, cand in enumerate(candidates_vision, 1):
        print(f"  {i}. {cand.latex_command:20} (score: {cand.combined_score:.3f})")


def main():
    """Run all examples."""
    print("\n" + "=" * 70)
    print("Semantic Suggestion Engine - Example Usage")
    print("=" * 70)
    
    example_basic_usage()
    example_multiple_symbols()
    example_from_top_k()
    example_custom_weights()
    
    print("\n" + "=" * 70)
    print("Examples completed!")
    print("=" * 70)


if __name__ == "__main__":
    main()

