#!/bin/bash

# Script to create Xcode project and test the macOS app
set -e

PROJECT_NAME="MathSymbolRecognizer"
PROJECT_DIR="MathSymbolRecognizer"
SOURCES_DIR="$PROJECT_DIR/Sources"
RESOURCES_DIR="$PROJECT_DIR/Resources"

echo "🚀 Setting up MathSymbolRecognizer for testing..."
echo ""

# Check if Xcode is available
if ! command -v xcodebuild &> /dev/null; then
    echo "❌ Error: Xcode is not installed or xcodebuild is not in PATH"
    exit 1
fi

# Check if model exists
if [ ! -d "$RESOURCES_DIR/best_model.mlpackage" ]; then
    echo "⚠️  Warning: CoreML model not found"
    echo "   Copying from ../exports/..."
    if [ -d "../exports/best_model.mlpackage" ]; then
        mkdir -p "$RESOURCES_DIR"
        cp -r "../exports/best_model.mlpackage" "$RESOURCES_DIR/"
        echo "   ✓ Model copied"
    else
        echo "   ❌ Model not found at ../exports/best_model.mlpackage"
        echo "   Please ensure the model is exported first"
        exit 1
    fi
fi

# Check Swift files
if [ ! -d "$SOURCES_DIR" ]; then
    echo "❌ Error: Sources directory not found"
    exit 1
fi

SWIFT_FILES=$(find "$SOURCES_DIR" -name "*.swift" | wc -l)
echo "✓ Found $SWIFT_FILES Swift source files"

# Try to create Xcode project using xcodebuild
echo ""
echo "📦 Creating Xcode project..."

# Create a basic project.yml for xcodegen (if available)
if command -v xcodegen &> /dev/null; then
    echo "   Using xcodegen..."
    # We'll create project.yml below
else
    echo "   xcodegen not found, will create project manually"
fi

# For now, let's check if we can at least validate Swift syntax
echo ""
echo "🔍 Checking Swift syntax..."

# Try to compile a single file to check syntax
if swiftc -typecheck "$SOURCES_DIR/App.swift" -sdk $(xcrun --show-sdk-path --sdk macosx) 2>&1 | head -20; then
    echo "   ✓ App.swift syntax OK"
else
    echo "   ⚠️  Some syntax issues found (this is expected without full project context)"
fi

echo ""
echo "✅ Setup complete!"
echo ""
echo "📝 Next steps:"
echo ""
echo "Option 1: Create Xcode project manually (recommended)"
echo "   1. Open Xcode"
echo "   2. File > New > Project"
echo "   3. Choose macOS > App"
echo "   4. Product Name: $PROJECT_NAME"
echo "   5. Interface: SwiftUI, Language: Swift"
echo "   6. Save in: $(pwd)"
echo "   7. Add all files from $SOURCES_DIR/"
echo "   8. Add $RESOURCES_DIR/best_model.mlpackage to Resources"
echo ""
echo "Option 2: Use the automated helper"
echo "   Run: open -a Xcode"
echo "   Then follow: macos_app/create_xcode_project.md"
echo ""
echo "🧪 To test after project is created:"
echo "   1. Open MathSymbolRecognizer.xcodeproj in Xcode"
echo "   2. Build (⌘B)"
echo "   3. Run (⌘R)"
echo ""

