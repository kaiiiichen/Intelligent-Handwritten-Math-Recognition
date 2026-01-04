# Semantic Engine

**Status:** ✅ **Complete** - Mathematical ranking system ready

## Features

- **Mathematical Priority Ranking:** Context-aware LaTeX suggestions
- **Complete Symbol Database:** 369 symbols with multiple LaTeX alternatives
- **Configurable Weights:** Vision confidence (60%) + Math priority (40%)
- **Integration Ready:** Clean API for UI integration

## Key Components

- `mapping_db/` - Symbol to LaTeX mappings
- `ranking/` - Candidate ranking algorithms
- `rendering/` - LaTeX preview generation
- `integration.py` - Main API interface

## Usage

```python
from semantic_engine.integration import create_suggestion_engine

engine = create_suggestion_engine()
candidates = engine.suggest_latex_candidates(vision_predictions, top_k=5)
```

## Ready for Production

All 369 symbols mapped with mathematical context and priority scoring.
