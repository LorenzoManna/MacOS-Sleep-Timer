#!/bin/bash
# SleepTimer Double-Clickable macOS Installer
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" 2>/dev/null && pwd)"
cd "$DIR"
exec bash "$DIR/install.sh"
