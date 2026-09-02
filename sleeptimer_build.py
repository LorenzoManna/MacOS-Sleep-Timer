#!/usr/bin/env python3
"""Build automation and execution helpers for SleepTimer."""

import os
import shutil
import stat
import subprocess
import sys
import zipfile
from pathlib import Path

VERSION = "0.1.1"
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
    """Build standalone zero-dependency macOS .app bundle and release zip archive."""
    print("=== Building Standalone SleepTimer.app Bundle with PyInstaller ===")

    # Clean previous builds
    if DIST_DIR.exists():
        shutil.rmtree(DIST_DIR)
    build_dir = PROJECT_ROOT / "build"
    if build_dir.exists():
        shutil.rmtree(build_dir)
    old_zip = PROJECT_ROOT / ZIP_NAME
    if old_zip.exists():
        old_zip.unlink()

    icon_path = PROJECT_ROOT / "Contents" / "Resources" / "AppIcon.icns"
    entry_script = PROJECT_ROOT / "Contents" / "MacOS" / "SleepTimer"

    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--noconfirm",
        "--windowed",
        "--name", "SleepTimer",
        "--icon", str(icon_path),
        "--osx-bundle-identifier", "com.local.sleeptimer",
        "--paths", str(PROJECT_ROOT / "Contents" / "MacOS"),
        "--hidden-import", "rumps",
        "--hidden-import", "Foundation",
        "--hidden-import", "MenuBarTimer",
        "--distpath", str(DIST_DIR),
        "--workpath", str(build_dir),
        "--specpath", str(build_dir),
        str(entry_script),
    ]

    subprocess.run(cmd, check=True)

    # Overwrite default Info.plist with our comprehensive Info.plist
    source_plist = PROJECT_ROOT / "Contents" / "Info.plist"
    target_plist = APP_DIR / "Contents" / "Info.plist"
    if source_plist.exists():
        shutil.copy(source_plist, target_plist)

    # Ensure executable permissions on main binary
    make_executable(APP_DIR / "Contents" / "MacOS" / "SleepTimer")

    # Ad-hoc sign the bundle
    if shutil.which("codesign"):
        subprocess.run(["codesign", "--force", "--deep", "--sign", "-", str(APP_DIR)],
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    # Copy distribution root files
    shutil.copy(PROJECT_ROOT / "requirements.txt", DIST_DIR / "requirements.txt")
    shutil.copy(PROJECT_ROOT / "install.sh", DIST_DIR / "install.sh")
    make_executable(DIST_DIR / "install.sh")

    # Clean up temporary build/ directory
    if build_dir.exists():
        shutil.rmtree(build_dir)

    # Create release zip archive with symlink and bundle preservation
    zip_path = PROJECT_ROOT / ZIP_NAME
    create_release_archive(DIST_DIR, zip_path)

    print("=== Build Complete! ===")
    print(f"Standalone Application bundle: {APP_DIR}")
    print(f"Release archive:               {zip_path}")


def create_release_archive(dist_dir: Path, zip_path: Path) -> None:
    """Create release zip archive preserving symlinks, permissions, and code signatures."""
    if zip_path.exists():
        zip_path.unlink()

    print(f"Creating release archive: {zip_path.name}...")

    # Prefer macOS native ditto tool which guarantees 100% fidelity for .app bundles
    if shutil.which("ditto"):
        subprocess.run(
            ["ditto", "-c", "-k", "--sequesterRsrc", str(dist_dir), str(zip_path)],
            check=True,
        )
        return

    # Fallback to zip utility with -y (preserve symlinks)
    if shutil.which("zip"):
        subprocess.run(
            ["zip", "-y", "-r", "-q", str(zip_path.resolve()), "."],
            cwd=str(dist_dir),
            check=True,
        )
        return

    # Fallback to Python zipfile with symlink preservation
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(dist_dir):
            for file in files:
                full_path = Path(root) / file
                rel_path = full_path.relative_to(dist_dir)
                if full_path.is_symlink():
                    link_target = os.readlink(full_path)
                    zinfo = zipfile.ZipInfo(str(rel_path))
                    zinfo.create_system = 3  # Unix
                    zinfo.external_attr = 0o120755 << 16
                    zipf.writestr(zinfo, link_target)
                else:
                    zipf.write(full_path, arcname=str(rel_path))


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
