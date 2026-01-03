"""
Test script for the LaTeX candidate mapping database.

This demonstrates how the mapping database works with mathematical priority ranking.
"""

from symbol_mapping import SymbolMappingDatabase


def test_mathematical_priority():
    """Test that mathematical priority ranking works correctly."""
    db = SymbolMappingDatabase()
    
    print("=" * 70)
    print("Testing Mathematical Priority Ranking")
    print("=" * 70)
    
    # Test cases: symbols where mathematical priority matters
    test_cases = [
        (1, "Double Right Arrow (implies)"),
        (2, "Double Left-Right Arrow (iff)"),
        (4, "Subset or Equal"),
        (5, "Element Of"),
        (12, "For All (quantifier)"),
        (19, "Sum (summation)"),
    ]
    
    for symbol_id, description in test_cases:
        print(f"\n{description}:")
        print("-" * 70)
        candidates = db.get_ranked_candidates(symbol_id)
        
        if not candidates:
            print(f"  No candidates found for symbol ID {symbol_id}")
            continue
        
        for i, cand in enumerate(candidates, 1):
            priority_bar = "█" * int(cand.math_priority * 20)
            print(f"  {i}. {cand.command:20} Priority: {cand.math_priority:.2f} {priority_bar}")
            print(f"     Context: {cand.context}")
            if cand.description:
                print(f"     {cand.description}")


def test_priority_comparison():
    """Compare priorities for similar symbols to verify mathematical priority principle."""
    db = SymbolMappingDatabase()
    
    print("\n" + "=" * 70)
    print("Priority Comparison: Mathematical vs Generic")
    print("=" * 70)
    
    comparisons = [
        {
            "title": "Logical Implication",
            "symbol_id": 1,
            "expected_top": "\\implies",
            "reason": "\\implies has specific logical meaning"
        },
        {
            "title": "Set Membership",
            "symbol_id": 5,
            "expected_top": "\\in",
            "reason": "\\in is the standard set membership symbol"
        },
        {
            "title": "Summation",
            "symbol_id": 19,
            "expected_top": "\\sum",
            "reason": "\\sum is the mathematical operator, not just a letter"
        },
    ]
    
    for comp in comparisons:
        candidates = db.get_ranked_candidates(comp["symbol_id"])
        if candidates:
            top_candidate = candidates[0]
            status = "✓" if top_candidate.command == comp["expected_top"] else "✗"
            print(f"\n{status} {comp['title']}:")
            print(f"  Top candidate: {top_candidate.command} (priority: {top_candidate.math_priority:.2f})")
            print(f"  Expected: {comp['expected_top']}")
            print(f"  Reason: {comp['reason']}")
            
            if len(candidates) > 1:
                print(f"  Alternatives:")
                for cand in candidates[1:3]:  # Show top 2 alternatives
                    print(f"    - {cand.command} (priority: {cand.math_priority:.2f})")


def demonstrate_usage():
    """Demonstrate how to use the database in a real scenario."""
    db = SymbolMappingDatabase()
    
    print("\n" + "=" * 70)
    print("Usage Example: Vision Engine Output → LaTeX Suggestions")
    print("=" * 70)
    
    # Simulate Vision Engine output: (symbol_class_id, confidence_score)
    vision_outputs = [
        (1, 0.95),  # High confidence: double right arrow
        (1, 0.65),  # Medium confidence: double right arrow
        (4, 0.88),  # High confidence: subset or equal
    ]
    
    print("\nSimulating Vision Engine predictions:")
    for symbol_id, confidence in vision_outputs:
        print(f"\n  Symbol ID: {symbol_id}, Confidence: {confidence:.2f}")
        candidates = db.get_ranked_candidates(symbol_id)
        
        if candidates:
            print(f"  Top 3 LaTeX suggestions:")
            for i, cand in enumerate(candidates[:3], 1):
                # Combined score: vision confidence * math priority
                combined_score = confidence * cand.math_priority
                print(f"    {i}. {cand.command:20} "
                      f"(math priority: {cand.math_priority:.2f}, "
                      f"combined: {combined_score:.2f})")
                print(f"       {cand.context}")


if __name__ == "__main__":
    test_mathematical_priority()
    test_priority_comparison()
    demonstrate_usage()
    
    print("\n" + "=" * 70)
    print("All tests completed!")
    print("=" * 70)

