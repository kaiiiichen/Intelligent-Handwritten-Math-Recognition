# Semantic Suggestion Engine

The Semantic Suggestion Engine maps visual symbol classes (from the Vision Engine) to ranked LaTeX candidates with mathematical preferences.

## Overview

This engine provides:

1. **Symbol-to-LaTeX Mapping**: Maps each of the 369+ symbol classes to one or more LaTeX command candidates
2. **Mathematical Priority Ranking**: Ranks LaTeX candidates by mathematical appropriateness (not just visual similarity)
3. **Combined Ranking**: Combines Vision Engine confidence scores with mathematical priority
4. **LaTeX Rendering**: Generates preview images for LaTeX candidates (optional)

## Architecture

```
Vision Engine Predictions → CandidateRanker → Ranked LaTeX Candidates
                              ↓
                    SymbolMappingDatabase
                              ↓
                    LaTeXRenderer (optional)
```

## Quick Start

```python
from semantic_engine import create_suggestion_engine
import numpy as np

# Create suggestion engine
engine = create_suggestion_engine()

# Simulate Vision Engine output (shape: 369,)
vision_predictions = np.random.rand(369)
vision_predictions = vision_predictions / vision_predictions.sum()  # Normalize

# Get ranked LaTeX candidates
candidates = engine.suggest_latex_candidates(vision_predictions, top_k=5)

# Display results
for i, cand in enumerate(candidates, 1):
    print(f"{i}. {cand.latex_command} "
          f"(score: {cand.combined_score:.3f}) - {cand.context}")
```

## Components

### 1. Symbol Mapping Database

Maps symbol class IDs to LaTeX candidates with mathematical priority scores.

**Location:** `semantic_engine/mapping_db/`

**Key Classes:**
- `SymbolMappingDatabase`: Main database class
- `SymbolMapping`: Mapping for a single symbol class
- `LaTeXCandidate`: A single LaTeX command candidate

**Usage:**
```python
from semantic_engine.mapping_db.symbol_mapping import SymbolMappingDatabase

db = SymbolMappingDatabase()
candidates = db.get_ranked_candidates(symbol_class_id=59)  # \rightarrow
```

### 2. Ranking Algorithm

Combines Vision Engine confidence with mathematical priority.

**Location:** `semantic_engine/ranking/`

**Key Classes:**
- `CandidateRanker`: Main ranking class
- `RankedCandidate`: Ranked result with combined scores

**Usage:**
```python
from semantic_engine.ranking import CandidateRanker
import numpy as np

ranker = CandidateRanker(vision_weight=0.6, math_weight=0.4)
vision_predictions = np.random.rand(369)
candidates = ranker.rank_candidates(vision_predictions, top_k_symbols=5)
```

### 3. LaTeX Rendering

Generates preview images for LaTeX candidates.

**Location:** `semantic_engine/rendering/`

**Key Classes:**
- `LaTeXRenderer`: Main renderer class

**Usage:**
```python
from semantic_engine.rendering import LaTeXRenderer

renderer = LaTeXRenderer(backend="matplotlib")
image_bytes = renderer.render_to_image("\\sum", dpi=100)
```

### 4. Integration Interface

Unified API for the complete suggestion system.

**Location:** `semantic_engine/integration.py`

**Key Classes:**
- `SemanticSuggestionEngine`: Main integration class

**Usage:**
```python
from semantic_engine import create_suggestion_engine

engine = create_suggestion_engine()
candidates = engine.suggest_latex_candidates(vision_predictions, top_k=10)
```

## Mathematical Priority Principle

The system ranks LaTeX candidates by **mathematical priority**, not just visual similarity:

- **Higher priority (1.0)**: Symbols with specific mathematical meanings
  - Example: `\implies` (logical implication) > `\rightarrow` (generic arrow)
- **Medium priority (0.6-0.9)**: General mathematical symbols
- **Lower priority (0.3-0.5)**: Generic symbols with multiple meanings
- **Lowest priority (0.1-0.2)**: Visually similar but semantically different

## Ranking Formula

The combined score is calculated as:

```
combined_score = α * vision_confidence + β * math_priority
```

Where:
- `α` (vision_weight): Weight for visual confidence (default: 0.6)
- `β` (math_weight): Weight for mathematical priority (default: 0.4)

This ensures that:
1. High visual confidence symbols are prioritized
2. Mathematically appropriate symbols are preferred over generic alternatives
3. The balance can be adjusted based on use case

## Custom Ranking Weights

You can create rankers with different weightings:

```python
# Math-heavy (prioritize mathematical correctness)
math_heavy = create_suggestion_engine(vision_weight=0.4, math_weight=0.6)

# Vision-heavy (prioritize visual similarity)
vision_heavy = create_suggestion_engine(vision_weight=0.8, math_weight=0.2)
```

## Symbol Mapping Database

The database contains mappings for all 369+ symbols from the HASYv2 dataset:

- **Manually curated mappings**: 20+ common symbols with multiple LaTeX alternatives
- **Auto-generated mappings**: All remaining symbols with their primary LaTeX command

The database is stored in JSON format and can be extended easily.

## Examples

See `semantic_engine/example_usage.py` for complete examples:

```bash
python3 -m semantic_engine.example_usage
```

## Future Enhancements

- **Mode-based ranking**: Adjust priorities based on mathematical context (logic, analysis, algebra, etc.)
- **User preference learning**: Learn from user choices to adjust priorities (Phase 3)
- **Advanced rendering**: MathJax/KaTeX integration for production-quality previews
- **Symbol aliases**: Handle multiple visual representations of the same symbol

## Files Structure

```
semantic_engine/
├── __init__.py                 # Package exports
├── integration.py              # Main integration interface
├── example_usage.py            # Usage examples
├── mapping_db/
│   ├── symbol_mapping.py       # Mapping database implementation
│   ├── symbol_mapping_full.json # Complete database (auto-generated)
│   ├── generate_full_mapping.py # Script to generate full database
│   └── README.md               # Mapping database documentation
├── ranking/
│   ├── ranker.py               # Ranking algorithm
│   └── __init__.py
└── rendering/
    ├── latex_renderer.py       # LaTeX rendering utilities
    └── __init__.py
```

## Integration with Vision Engine

The Semantic Suggestion Engine is designed to work seamlessly with the Vision Engine:

1. **Vision Engine** outputs probability distribution over 369 symbol classes
2. **Semantic Engine** takes these predictions and:
   - Maps each symbol class to LaTeX candidates
   - Ranks candidates by combined score
   - Returns top-k suggestions

See `semantic_engine/example_usage.py` for integration examples.

