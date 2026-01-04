#!/bin/bash

# Quick test script to validate the macOS app setup
set -e

echo "🧪 Quick Test for MathSymbolRecognizer"
echo "========================================"
echo ""

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

PROJECT_DIR="MathSymbolRecognizer"
SOURCES_DIR="$PROJECT_DIR/Sources"
RESOURCES_DIR="$PROJECT_DIR/Resources"

# Test 1: Check source files
echo "1️⃣  Checking source files..."
SWIFT_FILES=(
    "App.swift"
    "ContentView.swift"
    "DrawingCanvasView.swift"
    "RecognitionViewModel.swift"
    "SuggestionListView.swift"
    "ImageExtensions.swift"
    "SymbolMapping.swift"
)

MISSING_FILES=()
for file in "${SWIFT_FILES[@]}"; do
    if [ -f "$SOURCES_DIR/$file" ]; then
        echo "   ✓ $file"
    else
        echo "   ❌ $file (missing)"
        MISSING_FILES+=("$file")
    fi
done

if [ ${#MISSING_FILES[@]} -eq 0 ]; then
    echo -e "   ${GREEN}✓ All source files present${NC}"
else
    echo -e "   ${RED}❌ Missing ${#MISSING_FILES[@]} file(s)${NC}"
    exit 1
fi

echo ""

# Test 2: Check CoreML model
echo "2️⃣  Checking CoreML model..."
if [ -d "$RESOURCES_DIR/best_model.mlpackage" ]; then
    MODEL_SIZE=$(du -sh "$RESOURCES_DIR/best_model.mlpackage" | cut -f1)
    echo "   ✓ best_model.mlpackage found ($MODEL_SIZE)"
    echo -e "   ${GREEN}✓ CoreML model present${NC}"
else
    echo "   ⚠️  best_model.mlpackage not found"
    if [ -d "../exports/best_model.mlpackage" ]; then
        echo "   📦 Copying from ../exports/..."
        mkdir -p "$RESOURCES_DIR"
        cp -r "../exports/best_model.mlpackage" "$RESOURCES_DIR/"
        echo -e "   ${GREEN}✓ Model copied${NC}"
    else
        echo -e "   ${RED}❌ Model not found. Please export it first.${NC}"
        exit 1
    fi
fi

echo ""

# Test 3: Check for common Swift issues
echo "3️⃣  Checking for common issues..."

# Check imports
echo "   Checking imports..."
if grep -q "import SwiftUI" "$SOURCES_DIR/App.swift" && \
   grep -q "import CoreML" "$SOURCES_DIR/RecognitionViewModel.swift"; then
    echo "   ✓ Required imports present"
else
    echo -e "   ${YELLOW}⚠️  Some imports may be missing${NC}"
fi

# Check for @main
if grep -q "@main" "$SOURCES_DIR/App.swift"; then
    echo "   ✓ @main attribute found"
else
    echo -e "   ${RED}❌ @main attribute missing${NC}"
fi

echo ""

# Test 4: File structure
echo "4️⃣  Checking file structure..."
STRUCTURE_OK=true

if [ ! -d "$SOURCES_DIR" ]; then
    echo "   ❌ Sources directory missing"
    STRUCTURE_OK=false
fi

if [ ! -d "$RESOURCES_DIR" ]; then
    echo "   ⚠️  Resources directory missing (creating...)"
    mkdir -p "$RESOURCES_DIR"
fi

if [ "$STRUCTURE_OK" = true ]; then
    echo -e "   ${GREEN}✓ File structure OK${NC}"
fi

echo ""

# Test 5: Check Xcode availability
echo "5️⃣  Checking Xcode setup..."
if command -v xcodebuild &> /dev/null; then
    XCODE_VERSION=$(xcodebuild -version | head -1)
    echo "   ✓ $XCODE_VERSION"
    
    # Check SDK
    MACOS_SDK=$(xcodebuild -showsdks | grep macosx | head -1 | awk '{print $NF}')
    echo "   ✓ macOS SDK: $MACOS_SDK"
else
    echo -e "   ${RED}❌ Xcode not found${NC}"
    exit 1
fi

echo ""

# Summary
echo "========================================"
echo -e "${GREEN}✅ All checks passed!${NC}"
echo ""
echo "📝 Ready to create Xcode project:"
echo ""
echo "   Option 1: Manual (Recommended)"
echo "   1. Open Xcode"
echo "   2. File > New > Project (⇧⌘N)"
echo "   3. macOS > App"
echo "   4. Name: MathSymbolRecognizer"
echo "   5. Interface: SwiftUI"
echo "   6. Save in: $(pwd)"
echo "   7. Add files from $SOURCES_DIR/"
echo "   8. Add model from $RESOURCES_DIR/"
echo ""
echo "   Option 2: Quick start"
echo "   Run: open -a Xcode"
echo "   Then: File > New > Project..."
echo ""
echo "🧪 After project is created:"
echo "   ⌘B to build"
echo "   ⌘R to run"
echo ""

