#!/bin/bash
set -e

echo "=== Building SleepTimer.app Bundle ==="

DIST_DIR="dist"
BUILD_DIR="$DIST_DIR/SleepTimer.app"

# Clean previous build artifacts
rm -rf "$DIST_DIR" SleepTimer-*.zip

# Create build destination directories
mkdir -p "$BUILD_DIR/Contents/MacOS"
mkdir -p "$BUILD_DIR/Contents/Resources"

# Copy Info.plist, executable scripts, resources, and requirements
cp Contents/Info.plist "$BUILD_DIR/Contents/"
cp Contents/MacOS/SleepTimer "$BUILD_DIR/Contents/MacOS/"
cp Contents/MacOS/MenuBarTimer.py "$BUILD_DIR/Contents/MacOS/"
cp Contents/Resources/AppIcon.icns "$BUILD_DIR/Contents/Resources/"
cp requirements.txt "$DIST_DIR/requirements.txt"

# Grant executable permissions
chmod +x "$BUILD_DIR/Contents/MacOS/SleepTimer"
chmod +x "$BUILD_DIR/Contents/MacOS/MenuBarTimer.py"

# Copy installer script to dist/
cp install.sh "$DIST_DIR/install.sh"
chmod +x "$DIST_DIR/install.sh"

# Create zip archive containing SleepTimer.app, install.sh, and requirements.txt
ZIP_NAME="SleepTimer-v0.1.1-macOS.zip"
(cd "$DIST_DIR" && zip -r -q "../$ZIP_NAME" SleepTimer.app install.sh requirements.txt)

echo "=== Build Complete! ==="
echo "Application bundle created at: $BUILD_DIR"
echo "Release archive created at: $ZIP_NAME"
