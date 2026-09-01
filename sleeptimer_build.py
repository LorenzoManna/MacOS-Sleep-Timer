#!/usr/bin/env python3
"""Build automation and execution helpers for SleepTimer."""

import os
import shutil
import stat
import subprocess
import sys
import zipfile
from pathlib import Path

VERSION = "0.1.0"
PROJECT_ROOT = Path(__file__).resolve().parent
DIST_DIR = PROJECT_ROOT / "dist"
APP_DIR = DIST_DIR / "SleepTimer.app"
ZIP_NAME = f"SleepTimer-v{VERSION}-macOS.zip"


def make_executable(path: Path) -> None:
    """Add executable permissions to a file."""
    if path.exists():
        mode = path.stat().st_mode
        path.chmod(mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)


def build() -> None:
    """Build macOS .app bundle and release zip archive."""
    print("=== Building SleepTimer.app Bundle with Poetry Automation ===")

    # Clean previous builds
    if DIST_DIR.exists():
        shutil.rmtree(DIST_DIR)
    old_zip = PROJECT_ROOT / ZIP_NAME
    if old_zip.exists():
        old_zip.unlink()

    # Create directory structure
    macos_dir = APP_DIR / "Contents" / "MacOS"
    resources_dir = APP_DIR / "Contents" / "Resources"
    macos_dir.mkdir(parents=True, exist_ok=True)
    resources_dir.mkdir(parents=True, exist_ok=True)

    # Copy bundle contents
    shutil.copy(PROJECT_ROOT / "Contents" / "Info.plist", APP_DIR / "Contents" / "Info.plist")
    shutil.copy(PROJECT_ROOT / "Contents" / "MacOS" / "SleepTimer", macos_dir / "SleepTimer")
    shutil.copy(PROJECT_ROOT / "Contents" / "MacOS" / "MenuBarTimer.py", macos_dir / "MenuBarTimer.py")
    shutil.copy(PROJECT_ROOT / "Contents" / "Resources" / "AppIcon.icns", resources_dir / "AppIcon.icns")

    # Copy distribution root files
    shutil.copy(PROJECT_ROOT / "requirements.txt", DIST_DIR / "requirements.txt")
    shutil.copy(PROJECT_ROOT / "install.sh", DIST_DIR / "install.sh")

    # Set executable permissions
    make_executable(macos_dir / "SleepTimer")
    make_executable(macos_dir / "MenuBarTimer.py")
    make_executable(DIST_DIR / "install.sh")

    # Create release zip archive
    zip_path = PROJECT_ROOT / ZIP_NAME
    print(f"Creating release archive: {ZIP_NAME}...")
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
        for file in ["install.sh", "requirements.txt"]:
            zipf.write(DIST_DIR / file, arcname=file)

        for root, _, files in os.walk(APP_DIR):
            for file in files:
                full_path = Path(root) / file
                rel_path = full_path.relative_to(DIST_DIR)
                zipf.write(full_path, arcname=str(rel_path))

    print("=== Build Complete! ===")
    print(f"Application bundle: {APP_DIR}")
    print(f"Release archive:    {zip_path}")


def run_app() -> None:
    """Run SleepTimer from source."""
    script = PROJECT_ROOT / "Contents" / "MacOS" / "SleepTimer"
    if not script.exists():
        print(f"Error: {script} not found.", file=sys.stderr)
        sys.exit(1)
    subprocess.run([sys.executable, str(script)], check=True)


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "run":
        run_app()
    else:
        build()
