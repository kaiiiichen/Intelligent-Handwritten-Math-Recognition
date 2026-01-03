"""
Semantic Suggestion Engine

This package provides the semantic suggestion engine that maps visual symbol classes
to ranked LaTeX candidates with mathematical preferences.
"""

__version__ = "0.2.0"

from semantic_engine.integration import (
    SemanticSuggestionEngine,
    create_suggestion_engine
)
from semantic_engine.mapping_db.symbol_mapping import (
    SymbolMappingDatabase,
    LaTeXCandidate,
    SymbolMapping
)
from semantic_engine.ranking.ranker import (
    CandidateRanker,
    RankedCandidate,
    create_default_ranker
)
from semantic_engine.rendering.latex_renderer import (
    LaTeXRenderer,
    create_renderer
)

__all__ = [
    "SemanticSuggestionEngine",
    "create_suggestion_engine",
    "SymbolMappingDatabase",
    "LaTeXCandidate",
    "SymbolMapping",
    "CandidateRanker",
    "RankedCandidate",
    "create_default_ranker",
    "LaTeXRenderer",
    "create_renderer"
]
