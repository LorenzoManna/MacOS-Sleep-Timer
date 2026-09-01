#!/bin/bash
set -e

# SleepTimer macOS Installer
REPO_OWNER="LorenzoManna"
REPO_NAME="MacOS-Sleep-Timer"
APP_NAME="SleepTimer.app"
TARGET_DIR="/Applications"

echo "=========================================="
echo "  😴 Installing SleepTimer for macOS"
echo "=========================================="

# 1. Verify Python 3 installation
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python 3 is required but not installed."
    echo "Please install Python 3 from https://www.python.org/ or via Homebrew ('brew install python')."
    exit 1
fi

echo "✓ Python 3 found: $(python3 --version)"

TEMP_DIR=$(mktemp -d)
cleanup() {
    if [ -n "$TEMP_DIR" ] && [ -d "$TEMP_DIR" ]; then
        rm -rf "$TEMP_DIR"
    fi
}
trap cleanup EXIT

# 2. Check & install Python dependencies
echo "📦 Checking Python dependencies (rumps, pyobjc-framework-Cocoa)..."
if (cd "$TEMP_DIR" && python3 -c "import rumps, Foundation" 2>/dev/null); then
    echo "✓ Python dependencies already installed."
else
    echo "Installing required Python dependencies..."
    PIP_FLAGS="--quiet"
    if (cd "$TEMP_DIR" && python3 -m pip install --help 2>&1 | grep -q -- "--break-system-packages"); then
        PIP_FLAGS="$PIP_FLAGS --break-system-packages"
    fi

    if ! (cd "$TEMP_DIR" && python3 -m pip install $PIP_FLAGS rumps pyobjc-framework-Cocoa); then
        echo "⚠️ Warning: Failed standard pip install, attempting with --user flag..."
        (cd "$TEMP_DIR" && python3 -m pip install --quiet --user rumps pyobjc-framework-Cocoa) || true
    fi
    echo "✓ Python dependencies installed."
fi

SOURCE_APP=""

if [ -n "$SCRIPT_DIR" ] && [ -d "$SCRIPT_DIR/$APP_NAME" ]; then
    # Local release bundle
    SOURCE_APP="$SCRIPT_DIR/$APP_NAME"
elif [ -n "$SCRIPT_DIR" ] && [ -d "$SCRIPT_DIR/Contents" ]; then
    # Local git repository / source checkout
    TEMP_DIR=$(mktemp -d)
    mkdir -p "$TEMP_DIR/$APP_NAME"
    cp -R "$SCRIPT_DIR/Contents" "$TEMP_DIR/$APP_NAME/"
    chmod +x "$TEMP_DIR/$APP_NAME/Contents/MacOS/"*
    SOURCE_APP="$TEMP_DIR/$APP_NAME"
else
    # Remote curl/pipe mode: download from GitHub
    echo "📥 Downloading latest SleepTimer release..."
    TEMP_DIR=$(mktemp -d)
    ZIP_URL="https://github.com/$REPO_OWNER/$REPO_NAME/releases/latest/download/SleepTimer-v0.1.1-macOS.zip"
    FALLBACK_URL="https://github.com/$REPO_OWNER/$REPO_NAME/archive/refs/heads/main.zip"
    
    if curl -fsSL -o "$TEMP_DIR/bundle.zip" "$ZIP_URL" 2>/dev/null; then
        unzip -q -o "$TEMP_DIR/bundle.zip" -d "$TEMP_DIR"
        SOURCE_APP="$TEMP_DIR/$APP_NAME"
    elif curl -fsSL -o "$TEMP_DIR/repo.zip" "$FALLBACK_URL" 2>/dev/null; then
        unzip -q -o "$TEMP_DIR/repo.zip" -d "$TEMP_DIR"
        mkdir -p "$TEMP_DIR/$APP_NAME"
        cp -R "$TEMP_DIR/$REPO_NAME-main/Contents" "$TEMP_DIR/$APP_NAME/"
        chmod +x "$TEMP_DIR/$APP_NAME/Contents/MacOS/"*
        SOURCE_APP="$TEMP_DIR/$APP_NAME"
    else
        echo "Fetching repository via git..."
        git clone --depth 1 "https://github.com/$REPO_OWNER/$REPO_NAME.git" "$TEMP_DIR/repo"
        mkdir -p "$TEMP_DIR/$APP_NAME"
        cp -R "$TEMP_DIR/repo/Contents" "$TEMP_DIR/$APP_NAME/"
        chmod +x "$TEMP_DIR/$APP_NAME/Contents/MacOS/"*
        SOURCE_APP="$TEMP_DIR/$APP_NAME"
    fi
fi

if [ ! -d "$SOURCE_APP" ]; then
    echo "❌ Error: Could not locate $APP_NAME bundle."
    exit 1
fi

# 4. Install into /Applications
echo "🚀 Installing $APP_NAME to $TARGET_DIR..."
if [ -d "$TARGET_DIR/$APP_NAME" ]; then
    echo "Removing previous installation..."
    sudo rm -rf "$TARGET_DIR/$APP_NAME"
fi

sudo cp -R "$SOURCE_APP" "$TARGET_DIR/"
sudo chmod -R 755 "$TARGET_DIR/$APP_NAME"

# 5. Clear Gatekeeper quarantine attributes
echo "🛡️ Clearing macOS quarantine attributes..."
if [ -x "/usr/bin/xattr" ]; then
    sudo /usr/bin/xattr -cr "$TARGET_DIR/$APP_NAME" 2>/dev/null || true
else
    sudo xattr -cr "$TARGET_DIR/$APP_NAME" 2>/dev/null || true
fi

echo ""
echo "=========================================="
echo "  🎉 SleepTimer successfully installed!"
echo "=========================================="
echo "You can now open SleepTimer from your Applications folder, Spotlight, or Launchpad."
