"""
Ranking algorithms for combining Vision Engine outputs with LaTeX candidate mappings.

This module implements the ranking logic that combines:
- Vision Engine confidence scores
- Mathematical priority from mapping database
- Optional user preferences
"""

from semantic_engine.ranking.ranker import (
    CandidateRanker,
    RankedCandidate,
    create_default_ranker,
    create_vision_heavy_ranker,
    create_math_heavy_ranker
)

__all__ = [
    "CandidateRanker",
    "RankedCandidate",
    "create_default_ranker",
    "create_vision_heavy_ranker",
    "create_math_heavy_ranker"
]
