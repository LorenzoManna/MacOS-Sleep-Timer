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

# Create installer script inside dist/
cat << 'EOF' > "$DIST_DIR/install.sh"
#!/bin/bash
set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
APP_NAME="SleepTimer.app"
TARGET_DIR="/Applications"

echo "=== Installing SleepTimer Dependencies & Application ==="

# 1. Verify Python 3 installation
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is required but not installed."
    echo "Please install Python 3 from https://www.python.org/ or via Homebrew ('brew install python')."
    exit 1
fi

# 2. Automatically install Python dependencies via pip
if [ -f "$SCRIPT_DIR/requirements.txt" ]; then
    echo "Installing Python dependencies from requirements.txt..."
    python3 -m pip install --quiet -r "$SCRIPT_DIR/requirements.txt"
else
    echo "Installing required dependencies (rumps)..."
    python3 -m pip install --quiet rumps pyobjc-framework-Cocoa
fi

if [ ! -d "$SCRIPT_DIR/$APP_NAME" ]; then
    echo "Error: $APP_NAME not found in $SCRIPT_DIR"
    exit 1
fi

# 3. Copy SleepTimer.app to /Applications
if [ -d "$TARGET_DIR/$APP_NAME" ]; then
    echo "Removing previous installation in $TARGET_DIR..."
    sudo rm -rf "$TARGET_DIR/$APP_NAME"
fi

echo "Copying $APP_NAME to $TARGET_DIR..."
sudo cp -R "$SCRIPT_DIR/$APP_NAME" "$TARGET_DIR/"

# 4. Clear Gatekeeper quarantine attributes
echo "Clearing macOS quarantine attributes..."
sudo xattr -cr "$TARGET_DIR/$APP_NAME"

echo ""
echo "🎉 SleepTimer successfully installed to $TARGET_DIR!"
echo "You can now open SleepTimer from Applications or Launchpad."
EOF

chmod +x "$DIST_DIR/install.sh"

# Create zip archive containing SleepTimer.app, install.sh, and requirements.txt
ZIP_NAME="SleepTimer-v1.1.0-macOS.zip"
(cd "$DIST_DIR" && zip -r -q "../$ZIP_NAME" SleepTimer.app install.sh requirements.txt)

echo "=== Build Complete! ==="
echo "Application bundle created at: $BUILD_DIR"
echo "Release archive created at: $ZIP_NAME"
