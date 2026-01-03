"""
LaTeX Candidate Mapping Database

This package provides the mapping from visual symbol classes to LaTeX candidates,
ranked by mathematical priority.
"""

from .symbol_mapping import (
    SymbolMappingDatabase,
    SymbolMapping,
    LaTeXCandidate,
)

__all__ = [
    "SymbolMappingDatabase",
    "SymbolMapping",
    "LaTeXCandidate",
]

