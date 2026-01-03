# LaTeX Candidate Mapping Database

## Mathematical Priority Principle

The mapping database ranks LaTeX candidates by **"mathematical priority"** - symbols that have more specific mathematical meanings are prioritized over generic alternatives.

### Core Principle

**More mathematically specific symbols > Generic symbols**

### Examples

1. **Logical Implication:**
   - `\implies` (priority: 1.0) - Specific logical implication
   - `\Rightarrow` (priority: 0.6) - General mathematical arrow
   - `\rightarrow` (priority: 0.3) - Generic arrow

2. **Set Membership:**
   - `\in` (priority: 1.0) - Specific set membership symbol
   - `\epsilon` (priority: 0.2) - Greek letter (visually similar but different meaning)

3. **Comparison:**
   - `\leq` (priority: 1.0) - Standard mathematical symbol
   - `<=` (not in database) - ASCII alternative (not recommended)

## Priority Guidelines

### Priority Levels

- **1.0**: Standard mathematical symbol with specific meaning (e.g., `\implies`, `\forall`, `\in`)
- **0.8-0.9**: Mathematical symbol with variant or context-specific use (e.g., `\mapsto`, `\subseteqq`)
- **0.6-0.7**: General mathematical symbol (e.g., `\Rightarrow`, `\subset`)
- **0.3-0.5**: Generic symbol that could have multiple meanings (e.g., `\rightarrow`)
- **0.1-0.2**: Visually similar but semantically different (e.g., `\Sigma` vs `\sum`)

### Classification Rules

1. **Context-Specific > General Purpose**
   - `\implies` (logic) > `\rightarrow` (generic)
   - `\in` (set theory) > `\epsilon` (Greek letter)

2. **Standard Notation > ASCII Alternatives**
   - `\leq` > `<=`
   - `\neq` > `!=`
   - `\times` > `*`

3. **Mathematical Operators > Generic Symbols**
   - `\sum` (summation operator) > `\Sigma` (Greek letter)
   - `\prod` (product operator) > `\Pi` (Greek letter)

4. **Precise Mathematical Meaning > Ambiguous Symbols**
   - `\subseteq` (subset or equal) > `\subset` (proper subset, less precise)

## Database Structure

The database maps:

- **Input**: Symbol class ID (from Vision Engine)
- **Output**: Ranked list of LaTeX candidates with:
  - LaTeX command
  - Mathematical priority score (0.0-1.0)
  - Context description
  - Optional detailed description

## Usage

```python
from semantic_engine.mapping_db.symbol_mapping import SymbolMappingDatabase

# Initialize database
db = SymbolMappingDatabase()

# Get ranked candidates for a symbol
candidates = db.get_ranked_candidates(symbol_class_id=1)

# Candidates are automatically sorted by mathematical priority
for candidate in candidates:
    print(f"{candidate.command} - {candidate.context} (priority: {candidate.math_priority})")
```

## Extending the Database

To add new symbol mappings:

1. Identify the symbol class ID from the Vision Engine
2. List all possible LaTeX candidates
3. Assign mathematical priority scores based on:
   - Specificity of mathematical meaning
   - Standard usage in mathematical literature
   - Context-specific appropriateness
4. Add to `_initialize_mappings()` method in `symbol_mapping.py`

## Future Enhancements

- **Context-aware ranking**: Adjust priorities based on user's current mathematical context (logic, analysis, algebra, etc.)
- **User preference learning**: Learn from user choices to adjust priorities over time
- **Symbol aliases**: Handle multiple visual representations of the same symbol
