#!/bin/bash
set -e

echo "=== Building SleepTimer.app Bundle ==="

# Create build destination directories
BUILD_DIR="dist/SleepTimer.app"
mkdir -p "$BUILD_DIR/Contents/MacOS"
mkdir -p "$BUILD_DIR/Contents/Resources"

# Copy Info.plist, executable scripts, and resources
cp Contents/Info.plist "$BUILD_DIR/Contents/"
cp Contents/MacOS/SleepTimer "$BUILD_DIR/Contents/MacOS/"
cp Contents/MacOS/MenuBarTimer.py "$BUILD_DIR/Contents/MacOS/"
cp Contents/Resources/AppIcon.icns "$BUILD_DIR/Contents/Resources/"

# Grant executable permissions
chmod +x "$BUILD_DIR/Contents/MacOS/SleepTimer"
chmod +x "$BUILD_DIR/Contents/MacOS/MenuBarTimer.py"

# Ad-hoc code sign the application bundle
echo "Ad-hoc code signing bundle..."
codesign --force --deep --sign - "$BUILD_DIR"

echo "=== Build Complete! ==="
echo "Application bundle created at: $BUILD_DIR"
echo "You can now copy it to your Applications folder using:"
echo "  cp -R dist/SleepTimer.app /Applications/"
