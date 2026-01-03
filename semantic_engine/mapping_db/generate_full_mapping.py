"""
Script to generate a complete symbol mapping database from symbols.csv.

This script reads the symbols.csv file and generates mappings for all 369 symbols.
For symbols that already have detailed mappings (manually curated), it preserves them.
For other symbols, it creates basic mappings with the LaTeX command from the CSV.
"""

import csv
import json
from pathlib import Path
from typing import Dict, Set
import sys

# Add parent directory to path to import symbol_mapping
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from semantic_engine.mapping_db.symbol_mapping import (
    SymbolMappingDatabase,
    SymbolMapping,
    LaTeXCandidate
)


def load_symbols_csv(csv_path: str) -> Dict[int, str]:
    """
    Load symbols from CSV file.
    
    Returns:
        Dictionary mapping symbol_id -> latex_command
    """
    symbols = {}
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            symbol_id = int(row['symbol_id'])
            latex = row['latex']
            symbols[symbol_id] = latex
    return symbols


def generate_symbol_name(latex_command: str, symbol_id: int) -> str:
    """
    Generate a human-readable symbol name from LaTeX command.
    
    Args:
        latex_command: LaTeX command (e.g., "\\sum", "A", "\\alpha")
        symbol_id: Symbol ID
    
    Returns:
        Human-readable name
    """
    # Remove backslash if present
    if latex_command.startswith('\\'):
        name = latex_command[1:]
        # Replace common patterns
        name = name.replace('mathcal{', '').replace('}', '')
        name = name.replace('mathbb{', '').replace('}', '')
        name = name.replace('mathfrak{', '').replace('}', '')
        name = name.replace('mathscr{', '').replace('}', '')
        name = name.replace('mathds{', '').replace('}', '')
        return name
    else:
        # Single character or simple symbol
        return latex_command


def create_basic_mapping(symbol_id: int, latex_command: str) -> SymbolMapping:
    """
    Create a basic mapping for a symbol with a single LaTeX candidate.
    
    Args:
        symbol_id: Symbol class ID
        latex_command: LaTeX command
    
    Returns:
        SymbolMapping object
    """
    symbol_name = generate_symbol_name(latex_command, symbol_id)
    
    # Determine context based on LaTeX command
    context = "mathematical symbol"
    if latex_command.startswith('\\'):
        context = f"LaTeX command: {latex_command}"
    elif latex_command.isalpha():
        if latex_command.isupper():
            context = "capital letter"
        else:
            context = "lowercase letter"
    elif latex_command.isdigit():
        context = "digit"
    else:
        context = "symbol"
    
    return SymbolMapping(
        symbol_class_id=symbol_id,
        symbol_name=symbol_name,
        latex_candidates=[
            LaTeXCandidate(
                command=latex_command,
                math_priority=1.0,  # Default: highest priority for the primary command
                context=context,
                description=f"Primary LaTeX representation for {symbol_name}"
            )
        ]
    )


def generate_full_database(
    symbols_csv_path: str,
    existing_db: SymbolMappingDatabase,
    output_path: str
) -> SymbolMappingDatabase:
    """
    Generate a complete mapping database for all symbols.
    
    Args:
        symbols_csv_path: Path to symbols.csv file
        existing_db: Existing database with manually curated mappings
        output_path: Path to save the complete database JSON
    
    Returns:
        Complete SymbolMappingDatabase
    """
    # Load all symbols from CSV
    all_symbols = load_symbols_csv(symbols_csv_path)
    
    # Get IDs that already have detailed mappings
    existing_ids: Set[int] = set(existing_db.mappings.keys())
    
    # Create new database starting with existing mappings
    full_db = SymbolMappingDatabase()
    full_db.mappings = existing_db.mappings.copy()
    
    # Add mappings for symbols not yet in the database
    missing_count = 0
    for symbol_id, latex_command in all_symbols.items():
        if symbol_id not in existing_ids:
            # Create basic mapping
            mapping = create_basic_mapping(symbol_id, latex_command)
            full_db.mappings[symbol_id] = mapping
            missing_count += 1
    
    print(f"Generated mappings for {missing_count} symbols")
    print(f"Total symbols in database: {len(full_db.mappings)}")
    print(f"Manually curated mappings: {len(existing_ids)}")
    print(f"Auto-generated mappings: {missing_count}")
    
    # Save to file
    full_db.save_to_file(output_path)
    print(f"\nComplete database saved to: {output_path}")
    
    return full_db


def main():
    """Main function to generate the complete mapping database."""
    # Paths
    project_root = Path(__file__).parent.parent.parent
    symbols_csv_path = project_root / "data" / "symbols.csv"
    output_path = project_root / "semantic_engine" / "mapping_db" / "symbol_mapping_full.json"
    
    # Check if symbols.csv exists
    if not symbols_csv_path.exists():
        print(f"Error: symbols.csv not found at {symbols_csv_path}")
        return
    
    # Load existing database (with manually curated mappings)
    print("Loading existing database with manually curated mappings...")
    existing_db = SymbolMappingDatabase()
    
    # Generate complete database
    print("\nGenerating complete mapping database...")
    full_db = generate_full_database(
        str(symbols_csv_path),
        existing_db,
        str(output_path)
    )
    
    # Print some statistics
    print("\n=== Database Statistics ===")
    print(f"Total symbols: {len(full_db.mappings)}")
    
    # Count symbols with multiple candidates
    multi_candidate_count = sum(
        1 for m in full_db.mappings.values() if len(m.latex_candidates) > 1
    )
    print(f"Symbols with multiple LaTeX candidates: {multi_candidate_count}")
    print(f"Symbols with single LaTeX candidate: {len(full_db.mappings) - multi_candidate_count}")
    
    # Test a few mappings
    print("\n=== Sample Mappings ===")
    test_ids = [31, 59, 88, 185, 882]  # A, \rightarrow, \sum, \leq, \forall
    for test_id in test_ids:
        if test_id in full_db.mappings:
            mapping = full_db.mappings[test_id]
            print(f"\nSymbol ID {test_id}: {mapping.symbol_name}")
            for i, cand in enumerate(mapping.latex_candidates[:3], 1):
                print(f"  {i}. {cand.command} (priority: {cand.math_priority:.2f}) - {cand.context}")


if __name__ == "__main__":
    main()

