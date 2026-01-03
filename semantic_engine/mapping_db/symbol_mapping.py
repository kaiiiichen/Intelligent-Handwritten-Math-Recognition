"""
LaTeX Candidate Mapping Database

This module defines the mapping from visual symbol classes to LaTeX candidates,
ranked by "mathematical priority" - symbols that have more specific mathematical
meanings are prioritized over generic alternatives.

Mathematical Priority Principle:
- Symbols with specific mathematical meanings (e.g., \\implies for logical implication)
  are ranked higher than generic alternatives (e.g., \\rightarrow for general arrow)
- This ensures the system suggests the most mathematically appropriate LaTeX command
"""

from typing import List, Dict, Optional
from dataclasses import dataclass, field
import json


@dataclass
class LaTeXCandidate:
    """A single LaTeX command candidate for a symbol."""
    command: str  # LaTeX command, e.g., "\\implies"
    math_priority: float  # Mathematical priority score (0.0-1.0, higher = more mathematical)
    context: str  # Brief context description, e.g., "logical implication"
    description: Optional[str] = None  # Optional detailed description


@dataclass
class SymbolMapping:
    """Mapping from a visual symbol class to LaTeX candidates."""
    symbol_class_id: int  # ID from Vision Engine
    symbol_name: str  # Human-readable name, e.g., "double right arrow"
    latex_candidates: List[LaTeXCandidate] = field(default_factory=list)
    
    def get_ranked_candidates(self) -> List[LaTeXCandidate]:
        """Return candidates sorted by mathematical priority (descending)."""
        return sorted(self.latex_candidates, key=lambda x: x.math_priority, reverse=True)


class SymbolMappingDatabase:
    """
    Database of symbol-to-LaTeX mappings, ranked by mathematical priority.
    
    Mathematical Priority Guidelines:
    1. Symbols with specific mathematical meanings > generic symbols
       Example: \\implies (logical implication) > \\Rightarrow (general arrow) > \\rightarrow (generic arrow)
    2. Standard mathematical notation > ASCII alternatives
       Example: \\leq > <=, \\neq > !=, \\times > *
    3. Context-specific symbols > general-purpose symbols
       Example: \\in (set membership) > general epsilon, \\forall (quantifier) > general A
    """
    
    def __init__(self):
        self.mappings: Dict[int, SymbolMapping] = {}
        self._initialize_mappings()
    
    def _initialize_mappings(self):
        """Initialize the mapping database with common mathematical symbols."""
        
        # ===== Logical Implication / Arrow Symbols =====
        # Double right arrow (implies)
        self.mappings[1] = SymbolMapping(
            symbol_class_id=1,
            symbol_name="double right arrow",
            latex_candidates=[
                LaTeXCandidate(
                    command="\\implies",
                    math_priority=1.0,  # Highest: specific logical meaning
                    context="logical implication",
                    description="Standard symbol for logical implication in mathematical logic"
                ),
                LaTeXCandidate(
                    command="\\Rightarrow",
                    math_priority=0.6,  # Medium: general mathematical arrow
                    context="general implication",
                    description="General double-line right arrow, less specific than \\implies"
                ),
                LaTeXCandidate(
                    command="\\rightarrow",
                    math_priority=0.3,  # Lower: generic arrow
                    context="generic arrow or mapping",
                    description="Generic right arrow, can mean function mapping or general direction"
                ),
            ]
        )
        
        # Double left-right arrow (iff)
        self.mappings[2] = SymbolMapping(
            symbol_class_id=2,
            symbol_name="double left-right arrow",
            latex_candidates=[
                LaTeXCandidate(
                    command="\\iff",
                    math_priority=1.0,
                    context="if and only if",
                    description="Standard symbol for logical equivalence (if and only if)"
                ),
                LaTeXCandidate(
                    command="\\Leftrightarrow",
                    math_priority=0.6,
                    context="general equivalence",
                    description="General double-line bidirectional arrow"
                ),
                LaTeXCandidate(
                    command="\\leftrightarrow",
                    math_priority=0.3,
                    context="generic bidirectional arrow",
                    description="Generic bidirectional arrow"
                ),
            ]
        )
        
        # Single right arrow
        self.mappings[3] = SymbolMapping(
            symbol_class_id=3,
            symbol_name="right arrow",
            latex_candidates=[
                LaTeXCandidate(
                    command="\\rightarrow",
                    math_priority=0.8,
                    context="function mapping or limit",
                    description="Commonly used for function mappings f: A → B or limits"
                ),
                LaTeXCandidate(
                    command="\\to",
                    math_priority=0.7,
                    context="function mapping (shorthand)",
                    description="Shorthand for \\rightarrow, commonly used in function notation"
                ),
                LaTeXCandidate(
                    command="\\mapsto",
                    math_priority=0.9,
                    context="element mapping",
                    description="Maps to (element-wise), e.g., x ↦ f(x)"
                ),
            ]
        )
        
        # ===== Set Theory Symbols =====
        # Subset or equal
        self.mappings[4] = SymbolMapping(
            symbol_class_id=4,
            symbol_name="subset or equal",
            latex_candidates=[
                LaTeXCandidate(
                    command="\\subseteq",
                    math_priority=1.0,
                    context="subset or equal",
                    description="Standard symbol for subset or equal in set theory"
                ),
                LaTeXCandidate(
                    command="\\subset",
                    math_priority=0.7,
                    context="proper subset",
                    description="Proper subset (not equal)"
                ),
                LaTeXCandidate(
                    command="\\subseteqq",
                    math_priority=0.9,
                    context="subset or equal (variant)",
                    description="Variant of \\subseteq, less common"
                ),
            ]
        )
        
        # Element of
        self.mappings[5] = SymbolMapping(
            symbol_class_id=5,
            symbol_name="element of",
            latex_candidates=[
                LaTeXCandidate(
                    command="\\in",
                    math_priority=1.0,
                    context="set membership",
                    description="Standard symbol for set membership (element of)"
                ),
                LaTeXCandidate(
                    command="\\epsilon",
                    math_priority=0.2,
                    context="Greek letter epsilon",
                    description="Greek letter epsilon, visually similar but different meaning"
                ),
            ]
        )
        
        # Union
        self.mappings[6] = SymbolMapping(
            symbol_class_id=6,
            symbol_name="union",
            latex_candidates=[
                LaTeXCandidate(
                    command="\\cup",
                    math_priority=1.0,
                    context="set union",
                    description="Standard symbol for set union"
                ),
                LaTeXCandidate(
                    command="\\bigcup",
                    math_priority=0.9,
                    context="big union",
                    description="Large union operator for indexed unions"
                ),
            ]
        )
        
        # Intersection
        self.mappings[7] = SymbolMapping(
            symbol_class_id=7,
            symbol_name="intersection",
            latex_candidates=[
                LaTeXCandidate(
                    command="\\cap",
                    math_priority=1.0,
                    context="set intersection",
                    description="Standard symbol for set intersection"
                ),
                LaTeXCandidate(
                    command="\\bigcap",
                    math_priority=0.9,
                    context="big intersection",
                    description="Large intersection operator for indexed intersections"
                ),
            ]
        )
        
        # ===== Comparison Symbols =====
        # Less than or equal
        self.mappings[8] = SymbolMapping(
            symbol_class_id=8,
            symbol_name="less than or equal",
            latex_candidates=[
                LaTeXCandidate(
                    command="\\leq",
                    math_priority=1.0,
                    context="less than or equal",
                    description="Standard mathematical symbol for less than or equal"
                ),
                LaTeXCandidate(
                    command="\\leqslant",
                    math_priority=0.8,
                    context="less than or equal (variant)",
                    description="Variant of \\leq, less common"
                ),
            ]
        )
        
        # Greater than or equal
        self.mappings[9] = SymbolMapping(
            symbol_class_id=9,
            symbol_name="greater than or equal",
            latex_candidates=[
                LaTeXCandidate(
                    command="\\geq",
                    math_priority=1.0,
                    context="greater than or equal",
                    description="Standard mathematical symbol for greater than or equal"
                ),
                LaTeXCandidate(
                    command="\\geqslant",
                    math_priority=0.8,
                    context="greater than or equal (variant)",
                    description="Variant of \\geq, less common"
                ),
            ]
        )
        
        # Not equal
        self.mappings[10] = SymbolMapping(
            symbol_class_id=10,
            symbol_name="not equal",
            latex_candidates=[
                LaTeXCandidate(
                    command="\\neq",
                    math_priority=1.0,
                    context="not equal",
                    description="Standard mathematical symbol for not equal"
                ),
                LaTeXCandidate(
                    command="\\ne",
                    math_priority=0.9,
                    context="not equal (shorthand)",
                    description="Shorthand for \\neq"
                ),
            ]
        )
        
        # Approximately equal
        self.mappings[11] = SymbolMapping(
            symbol_class_id=11,
            symbol_name="approximately equal",
            latex_candidates=[
                LaTeXCandidate(
                    command="\\approx",
                    math_priority=1.0,
                    context="approximately equal",
                    description="Standard symbol for approximately equal"
                ),
                LaTeXCandidate(
                    command="\\simeq",
                    math_priority=0.8,
                    context="asymptotically equal",
                    description="Asymptotically equal, used in asymptotic analysis"
                ),
                LaTeXCandidate(
                    command="\\cong",
                    math_priority=0.7,
                    context="congruent",
                    description="Congruent, used in geometry"
                ),
            ]
        )
        
        # ===== Logical Quantifiers =====
        # For all
        self.mappings[12] = SymbolMapping(
            symbol_class_id=12,
            symbol_name="for all",
            latex_candidates=[
                LaTeXCandidate(
                    command="\\forall",
                    math_priority=1.0,
                    context="universal quantifier",
                    description="Universal quantifier (for all) in mathematical logic"
                ),
            ]
        )
        
        # Exists
        self.mappings[13] = SymbolMapping(
            symbol_class_id=13,
            symbol_name="exists",
            latex_candidates=[
                LaTeXCandidate(
                    command="\\exists",
                    math_priority=1.0,
                    context="existential quantifier",
                    description="Existential quantifier (there exists) in mathematical logic"
                ),
            ]
        )
        
        # ===== Operators =====
        # Multiplication
        self.mappings[14] = SymbolMapping(
            symbol_class_id=14,
            symbol_name="multiplication",
            latex_candidates=[
                LaTeXCandidate(
                    command="\\times",
                    math_priority=1.0,
                    context="multiplication or cross product",
                    description="Standard symbol for multiplication or cross product"
                ),
                LaTeXCandidate(
                    command="\\cdot",
                    math_priority=0.9,
                    context="dot product or scalar multiplication",
                    description="Dot product or scalar multiplication"
                ),
                LaTeXCandidate(
                    command="\\ast",
                    math_priority=0.5,
                    context="asterisk multiplication",
                    description="Asterisk multiplication, less common"
                ),
            ]
        )
        
        # Division
        self.mappings[15] = SymbolMapping(
            symbol_class_id=15,
            symbol_name="division",
            latex_candidates=[
                LaTeXCandidate(
                    command="\\div",
                    math_priority=1.0,
                    context="division",
                    description="Standard symbol for division"
                ),
            ]
        )
        
        # Plus minus
        self.mappings[16] = SymbolMapping(
            symbol_class_id=16,
            symbol_name="plus minus",
            latex_candidates=[
                LaTeXCandidate(
                    command="\\pm",
                    math_priority=1.0,
                    context="plus or minus",
                    description="Standard symbol for plus or minus"
                ),
                LaTeXCandidate(
                    command="\\mp",
                    math_priority=0.9,
                    context="minus or plus",
                    description="Minus or plus (opposite of \\pm)"
                ),
            ]
        )
        
        # ===== Equivalence =====
        # Equivalent
        self.mappings[17] = SymbolMapping(
            symbol_class_id=17,
            symbol_name="equivalent",
            latex_candidates=[
                LaTeXCandidate(
                    command="\\equiv",
                    math_priority=1.0,
                    context="equivalent or congruent",
                    description="Standard symbol for equivalence or congruence"
                ),
                LaTeXCandidate(
                    command="\\sim",
                    math_priority=0.7,
                    context="similar or asymptotically equivalent",
                    description="Similar or asymptotically equivalent"
                ),
            ]
        )
        
        # ===== Integral =====
        # Integral
        self.mappings[18] = SymbolMapping(
            symbol_class_id=18,
            symbol_name="integral",
            latex_candidates=[
                LaTeXCandidate(
                    command="\\int",
                    math_priority=1.0,
                    context="integral",
                    description="Standard symbol for integral"
                ),
                LaTeXCandidate(
                    command="\\oint",
                    math_priority=0.9,
                    context="contour integral",
                    description="Contour integral (closed path integral)"
                ),
                LaTeXCandidate(
                    command="\\iint",
                    math_priority=0.8,
                    context="double integral",
                    description="Double integral"
                ),
            ]
        )
        
        # ===== Summation =====
        # Sum
        self.mappings[19] = SymbolMapping(
            symbol_class_id=19,
            symbol_name="sum",
            latex_candidates=[
                LaTeXCandidate(
                    command="\\sum",
                    math_priority=1.0,
                    context="summation",
                    description="Standard symbol for summation"
                ),
                LaTeXCandidate(
                    command="\\Sigma",
                    math_priority=0.3,
                    context="Greek letter capital sigma",
                    description="Greek letter capital sigma, visually similar but different from \\sum"
                ),
            ]
        )
        
        # ===== Product =====
        # Product
        self.mappings[20] = SymbolMapping(
            symbol_class_id=20,
            symbol_name="product",
            latex_candidates=[
                LaTeXCandidate(
                    command="\\prod",
                    math_priority=1.0,
                    context="product",
                    description="Standard symbol for product"
                ),
                LaTeXCandidate(
                    command="\\Pi",
                    math_priority=0.3,
                    context="Greek letter capital pi",
                    description="Greek letter capital pi, visually similar but different from \\prod"
                ),
            ]
        )
    
    def get_mapping(self, symbol_class_id: int) -> Optional[SymbolMapping]:
        """Get the mapping for a given symbol class ID."""
        return self.mappings.get(symbol_class_id)
    
    def get_ranked_candidates(self, symbol_class_id: int) -> List[LaTeXCandidate]:
        """Get ranked LaTeX candidates for a symbol class, sorted by mathematical priority."""
        mapping = self.get_mapping(symbol_class_id)
        if mapping is None:
            return []
        return mapping.get_ranked_candidates()
    
    def to_json(self) -> str:
        """Export the database to JSON format."""
        data = {}
        for class_id, mapping in self.mappings.items():
            data[class_id] = {
                "symbol_class_id": mapping.symbol_class_id,
                "symbol_name": mapping.symbol_name,
                "latex_candidates": [
                    {
                        "command": cand.command,
                        "math_priority": cand.math_priority,
                        "context": cand.context,
                        "description": cand.description
                    }
                    for cand in mapping.latex_candidates
                ]
            }
        return json.dumps(data, indent=2, ensure_ascii=False)
    
    def save_to_file(self, filepath: str):
        """Save the database to a JSON file."""
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(self.to_json())
    
    @classmethod
    def from_json(cls, json_str: str) -> 'SymbolMappingDatabase':
        """Load the database from JSON format."""
        data = json.loads(json_str)
        db = cls()
        db.mappings = {}
        for class_id_str, mapping_data in data.items():
            class_id = int(class_id_str)
            candidates = [
                LaTeXCandidate(
                    command=cand["command"],
                    math_priority=cand["math_priority"],
                    context=cand["context"],
                    description=cand.get("description")
                )
                for cand in mapping_data["latex_candidates"]
            ]
            db.mappings[class_id] = SymbolMapping(
                symbol_class_id=class_id,
                symbol_name=mapping_data["symbol_name"],
                latex_candidates=candidates
            )
        return db
    
    @classmethod
    def from_json_file(cls, filepath: str) -> 'SymbolMappingDatabase':
        """Load the database from a JSON file."""
        with open(filepath, 'r', encoding='utf-8') as f:
            json_str = f.read()
        return cls.from_json(json_str)
    
    def load_full_mapping(self, filepath: str):
        """
        Load full mapping database from JSON file and merge with existing mappings.
        This preserves manually curated mappings while adding auto-generated ones.
        """
        full_db = self.from_json_file(filepath)
        # Merge: existing mappings take precedence
        for class_id, mapping in full_db.mappings.items():
            if class_id not in self.mappings:
                # Only add if not already present (preserve manual mappings)
                self.mappings[class_id] = mapping


# Example usage and testing
if __name__ == "__main__":
    # Create database
    db = SymbolMappingDatabase()
    
    # Test: Get ranked candidates for double right arrow
    print("=== Double Right Arrow (implies) ===")
    candidates = db.get_ranked_candidates(1)
    for i, cand in enumerate(candidates, 1):
        print(f"{i}. {cand.command:15} (priority: {cand.math_priority:.1f}) - {cand.context}")
        if cand.description:
            print(f"   {cand.description}")
    
    print("\n=== Subset or Equal ===")
    candidates = db.get_ranked_candidates(4)
    for i, cand in enumerate(candidates, 1):
        print(f"{i}. {cand.command:15} (priority: {cand.math_priority:.1f}) - {cand.context}")
    
    print("\n=== Save to JSON ===")
    db.save_to_file("symbol_mapping.json")
    print("Database saved to symbol_mapping.json")

