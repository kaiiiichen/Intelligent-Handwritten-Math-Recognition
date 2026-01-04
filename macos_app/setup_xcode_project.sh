#!/bin/bash

# Script to set up Xcode project for MathSymbolRecognizer
# This script helps create the Xcode project structure

set -e

PROJECT_DIR="MathSymbolRecognizer"
RESOURCES_DIR="$PROJECT_DIR/Resources"

echo "Setting up MathSymbolRecognizer Xcode project..."

# Create Resources directory
mkdir -p "$RESOURCES_DIR"

# Copy CoreML model if it exists
if [ -f "../exports/best_model.mlpackage" ]; then
    echo "Copying CoreML model..."
    cp -r "../exports/best_model.mlpackage" "$RESOURCES_DIR/"
    echo "✓ CoreML model copied"
else
    echo "⚠ Warning: CoreML model not found at ../exports/best_model.mlpackage"
    echo "  Please copy it manually to $RESOURCES_DIR/"
fi

# Copy symbol mapping files
if [ -f "symbol_mapping.json" ]; then
    echo "Copying symbol_mapping.json..."
    cp "symbol_mapping.json" "$RESOURCES_DIR/"
    echo "✓ symbol_mapping.json copied"
fi

if [ -f "../semantic_engine/mapping_db/symbol_mapping_full.json" ]; then
    echo "Copying symbol_mapping_full.json..."
    cp "../semantic_engine/mapping_db/symbol_mapping_full.json" "$RESOURCES_DIR/"
    echo "✓ symbol_mapping_full.json copied"
else
    echo "⚠ Warning: symbol_mapping_full.json not found"
    echo "  Please copy it manually from semantic_engine/mapping_db/ to $RESOURCES_DIR/"
fi

# Create Xcode project using xcodegen if available, or provide instructions
if command -v xcodegen &> /dev/null; then
    echo "Using xcodegen to create project..."
    # xcodegen would be used here if project.yml exists
else
    echo ""
    echo "To create the Xcode project:"
    echo "1. Open Xcode"
    echo "2. File > New > Project"
    echo "3. Choose 'macOS' > 'App'"
    echo "4. Product Name: MathSymbolRecognizer"
    echo "5. Interface: SwiftUI"
    echo "6. Language: Swift"
    echo "7. Save in: $(pwd)"
    echo ""
    echo "Then:"
    echo "- Add all files from Sources/ to the project"
    echo "- Add best_model.mlpackage to Resources/"
    echo "- Set deployment target to macOS 13.0+"
    echo ""
fi

echo ""
echo "Setup complete!"
echo ""
echo "Next steps:"
echo "1. Open MathSymbolRecognizer.xcodeproj in Xcode"
echo "2. Ensure best_model.mlpackage is in Resources/"
echo "3. Build and run (⌘R)"

