#!/bin/bash
set -e

# SleepTimer macOS Installer
REPO_OWNER="LorenzoManna"
REPO_NAME="MacOS-Sleep-Timer"
APP_NAME="SleepTimer.app"
TARGET_DIR="${TARGET_DIR:-/Applications}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" 2>/dev/null && pwd)"

echo "=========================================="
echo "  😴 Installing SleepTimer for macOS"
echo "=========================================="

TEMP_DIR=$(mktemp -d)
cleanup() {
    if [ -n "$TEMP_DIR" ] && [ -d "$TEMP_DIR" ]; then
        rm -rf "$TEMP_DIR"
    fi
}
trap cleanup EXIT

# 1. Locate or download SleepTimer.app
SOURCE_APP=""

if [ -n "$SCRIPT_DIR" ] && [ -d "$SCRIPT_DIR/$APP_NAME" ]; then
    # Local release bundle
    SOURCE_APP="$SCRIPT_DIR/$APP_NAME"
elif [ -n "$SCRIPT_DIR" ] && [ -d "$SCRIPT_DIR/dist/$APP_NAME" ]; then
    # Local dist build directory
    SOURCE_APP="$SCRIPT_DIR/dist/$APP_NAME"
elif [ -n "$SCRIPT_DIR" ] && [ -d "$SCRIPT_DIR/Contents" ]; then
    # Local git repository / source checkout
    mkdir -p "$TEMP_DIR/$APP_NAME"
    cp -R "$SCRIPT_DIR/Contents" "$TEMP_DIR/$APP_NAME/"
    chmod +x "$TEMP_DIR/$APP_NAME/Contents/MacOS/"*
    SOURCE_APP="$TEMP_DIR/$APP_NAME"
else
    # Remote curl/pipe mode: download from GitHub
    echo "📥 Downloading latest SleepTimer release..."
    ZIP_URL="https://github.com/$REPO_OWNER/$REPO_NAME/releases/latest/download/SleepTimer-v0.2.0-macOS.zip"
    FALLBACK_URL="https://github.com/$REPO_OWNER/$REPO_NAME/archive/refs/heads/main.zip"
    
    if curl -fsSL -o "$TEMP_DIR/bundle.zip" "$ZIP_URL" 2>/dev/null; then
        if command -v ditto &>/dev/null; then
            ditto -x -k "$TEMP_DIR/bundle.zip" "$TEMP_DIR"
        else
            unzip -q -o "$TEMP_DIR/bundle.zip" -d "$TEMP_DIR"
        fi
        SOURCE_APP="$TEMP_DIR/$APP_NAME"
    elif curl -fsSL -o "$TEMP_DIR/repo.zip" "$FALLBACK_URL" 2>/dev/null; then
        if command -v ditto &>/dev/null; then
            ditto -x -k "$TEMP_DIR/repo.zip" "$TEMP_DIR"
        else
            unzip -q -o "$TEMP_DIR/repo.zip" -d "$TEMP_DIR"
        fi
        mkdir -p "$TEMP_DIR/$APP_NAME"
        if command -v ditto &>/dev/null; then
            ditto "$TEMP_DIR/$REPO_NAME-main/Contents" "$TEMP_DIR/$APP_NAME/Contents"
        else
            cp -R "$TEMP_DIR/$REPO_NAME-main/Contents" "$TEMP_DIR/$APP_NAME/"
        fi
        chmod +x "$TEMP_DIR/$APP_NAME/Contents/MacOS/"*
        SOURCE_APP="$TEMP_DIR/$APP_NAME"
    else
        echo "Fetching repository via git..."
        git clone --depth 1 "https://github.com/$REPO_OWNER/$REPO_NAME.git" "$TEMP_DIR/repo"
        mkdir -p "$TEMP_DIR/$APP_NAME"
        if command -v ditto &>/dev/null; then
            ditto "$TEMP_DIR/repo/Contents" "$TEMP_DIR/$APP_NAME/Contents"
        else
            cp -R "$TEMP_DIR/repo/Contents" "$TEMP_DIR/$APP_NAME/"
        fi
        chmod +x "$TEMP_DIR/$APP_NAME/Contents/MacOS/"*
        SOURCE_APP="$TEMP_DIR/$APP_NAME"
    fi
fi

if [ ! -d "$SOURCE_APP" ]; then
    echo "❌ Error: Could not locate $APP_NAME bundle."
    exit 1
fi

# 2. Check if the bundle is a standalone zero-dependency app
if [ -d "$SOURCE_APP/Contents/Frameworks" ] || (file "$SOURCE_APP/Contents/MacOS/SleepTimer" 2>/dev/null | grep -q "Mach-O"); then
    echo "✓ Standalone application detected (no external Python runtime required)."
else
    echo "📦 Source script bundle detected: checking host Python environment..."
    if ! command -v python3 &> /dev/null; then
        echo "❌ Error: Python 3.11+ is required for source installs but not installed."
        echo "Please install Python 3.11+ from https://www.python.org/ or via Homebrew ('brew install python')."
        exit 1
    fi

    if ! python3 -c "import sys; sys.exit(0 if sys.version_info >= (3, 11) else 1)" 2>/dev/null; then
        echo "❌ Error: Python 3.11 or later is required (found $(python3 --version))."
        echo "Please upgrade Python via Homebrew ('brew install python') or from https://www.python.org/."
        exit 1
    fi

    echo "✓ Python found: $(python3 --version)"

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
fi

# 3. Determine permissions & target directory
TARGET_DIR="${TARGET_DIR:-/Applications}"
USE_SUDO=false

if [ ! -w "$TARGET_DIR" ]; then
    USE_SUDO=true
fi

run_cmd() {
    if [ "$USE_SUDO" = true ]; then
        sudo "$@"
    else
        "$@"
    fi
}

# 4. Install into TARGET_DIR
echo "🚀 Installing $APP_NAME to $TARGET_DIR..."
if [ -d "$TARGET_DIR/$APP_NAME" ]; then
    echo "Removing previous installation..."
    run_cmd rm -rf "$TARGET_DIR/$APP_NAME"
fi

if command -v ditto &>/dev/null; then
    run_cmd ditto "$SOURCE_APP" "$TARGET_DIR/$APP_NAME"
else
    run_cmd cp -a "$SOURCE_APP" "$TARGET_DIR/"
fi
run_cmd chmod -R 755 "$TARGET_DIR/$APP_NAME"

# 5. Clear Gatekeeper quarantine attributes
echo "🛡️ Clearing macOS quarantine attributes..."
if [ -x "/usr/bin/xattr" ]; then
    run_cmd /usr/bin/xattr -cr "$TARGET_DIR/$APP_NAME" 2>/dev/null || true
else
    run_cmd xattr -cr "$TARGET_DIR/$APP_NAME" 2>/dev/null || true
fi

echo ""
echo "=========================================="
echo "  🎉 SleepTimer successfully installed!"
echo "=========================================="
echo "You can now open SleepTimer from your Applications folder, Spotlight, or Launchpad."

if [ -t 0 ]; then
    echo ""
    read -n 1 -s -r -p "Press any key to close this window..."
    echo ""
fi
