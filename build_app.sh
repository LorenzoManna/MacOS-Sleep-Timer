#!/bin/bash
set -e

echo "=== Building SleepTimer Standalone Application Bundle ==="

if command -v poetry &>/dev/null; then
    poetry run build-app
else
    python3 sleeptimer_build.py
fi
