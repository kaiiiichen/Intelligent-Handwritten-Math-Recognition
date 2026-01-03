# Mathematical Priority Guide

## Core Principle

**The more "mathematical" a symbol is, the higher its priority**

Here, "mathematical" means: the symbol has a more specific and precise meaning in mathematical contexts.

## Design Philosophy

### Why Mathematical Priority?

In mathematical expressions, the same visual symbol may correspond to multiple LaTeX commands, but they have different mathematical meanings:

- `\implies` vs `\Rightarrow` vs `\rightarrow`
  - `\implies`: Logical implication (most mathematical, most precise)
  - `\Rightarrow`: General mathematical arrow (medium)
  - `\rightarrow`: Generic arrow (least mathematical, could mean mapping, direction, etc.)

The system should prioritize **mathematically most appropriate** symbols, not just "most likely" ones.

### Priority Scoring System

- **1.0**: Standard mathematical symbol with specific mathematical meaning
  - Examples: `\implies`, `\forall`, `\exists`, `\in`, `\sum`, `\int`
  
- **0.8-0.9**: Mathematical symbol variant or context-specific usage
  - Examples: `\mapsto`, `\subseteqq`, `\bigcup`
  
- **0.6-0.7**: General mathematical symbol
  - Examples: `\Rightarrow`, `\subset`, `\leqslant`
  
- **0.3-0.5**: Generic symbol that could have multiple meanings
  - Examples: `\rightarrow`, `\ast`
  
- **0.1-0.2**: Visually similar but semantically different
  - Examples: `\Sigma` (Greek letter) vs `\sum` (summation operator)

## Classification Rules

### 1. Context-Specific > Generic

| Mathematical Specific | Generic Alternative | Priority Difference |
|----------------------|-------------------|---------------------|
| `\implies` | `\rightarrow` | 1.0 vs 0.3 |
| `\in` | `\epsilon` | 1.0 vs 0.2 |
| `\sum` | `\Sigma` | 1.0 vs 0.3 |

### 2. Standard Mathematical Notation > ASCII Alternatives

| Standard Symbol | ASCII Alternative | Description |
|----------------|------------------|-------------|
| `\leq` | `<=` | Standard mathematical symbol |
| `\neq` | `!=` | Standard mathematical symbol |
| `\times` | `*` | Standard mathematical symbol |

### 3. Mathematical Operators > Letter Symbols

| Operator | Letter | Description |
|----------|--------|-------------|
| `\sum` | `\Sigma` | Summation operator vs Greek letter |
| `\prod` | `\Pi` | Product operator vs Greek letter |
| `\int` | (no corresponding letter) | Integral operator |

### 4. Precise Meaning > Ambiguous Symbols

| Precise | Ambiguous | Description |
|---------|-----------|-------------|
| `\subseteq` | `\subset` | "Subset or equal" vs "proper subset" (less precise) |

## Practical Examples

### Example 1: Logical Implication

User draws a double right arrow:

**Recommended order:**

1. `\implies` (priority: 1.0) - Logical implication
2. `\Rightarrow` (priority: 0.6) - General mathematical arrow
3. `\rightarrow` (priority: 0.3) - Generic arrow

**Reasoning:** In mathematical contexts, double arrows typically represent logical implication, and `\implies` is the most standard and precise choice.

### Example 2: Set Membership

User draws an "element of" symbol:

**Recommended order:**

1. `\in` (priority: 1.0) - Set membership
2. `\epsilon` (priority: 0.2) - Greek letter epsilon

**Reasoning:** `\in` is the standard symbol in set theory, while `\epsilon` is just a visually similar Greek letter with completely different mathematical meaning.

### Example 3: Summation

User draws a summation symbol:

**Recommended order:**

1. `\sum` (priority: 1.0) - Summation operator
2. `\Sigma` (priority: 0.3) - Greek letter

**Reasoning:** `\sum` is the mathematical summation operator, while `\Sigma` is just a visually similar Greek letter.

## Integration with Vision Engine

When the Vision Engine outputs symbol classification results, we combine two scores:

```
Final ranking score = Vision confidence × Mathematical priority
```

**Example:**

- Vision Engine identifies as "double right arrow" with confidence 0.95
- Mapping database returns:
  - `\implies`: 0.95 × 1.0 = 0.95
  - `\Rightarrow`: 0.95 × 0.6 = 0.57
  - `\rightarrow`: 0.95 × 0.3 = 0.28

This approach considers both visual recognition accuracy and mathematical correctness.

## Extension Guide

When adding new symbol mappings, consider the following questions:

1. **Does this symbol have a specific meaning in mathematics?**
   - Yes → Priority 1.0
   - No → Continue evaluation

2. **Is this symbol standard mathematical notation?**
   - Yes → Priority 0.8-0.9
   - No → Continue evaluation

3. **Is this symbol generic?**
   - Yes → Priority 0.3-0.5

4. **Is this symbol visually similar but semantically different from others?**
   - Yes → Priority 0.1-0.2

## Future Enhancements

- **Context-aware ranking**: Adjust priorities based on user's current mathematical context (logic, analysis, algebra, etc.)
- **User preference learning**: Learn from user choices to fine-tune priorities while maintaining mathematical correctness
- **Symbol alias handling**: Handle multiple visual representations of the same symbol
