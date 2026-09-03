# AGENTS.md

Welcome to the **MacOS Sleep Timer** repository. This document provides essential architectural context, development workflows, and coding conventions for AI agents and developers working on this codebase.

---

## 📌 Project Overview

**MacOS Sleep Timer** is a lightweight, modern macOS utility for scheduling system sleep, screen lock, and hibernation. It consists of:
1. **Main GUI Window**: Built using Python's standard `tkinter` library with custom dark-themed UI components (circular countdown timer, preset duration buttons, live clock preview, fast keyboard entry with auto-advance and `00` fallback).
2. **Menu Bar Status Item**: A background tray app built with `rumps` and `pyobjc-framework-Cocoa` that displays the remaining countdown in the macOS menu bar.
3. **macOS App Bundle (`SleepTimer.app`)**: Packaged as a standard macOS application directory structure with custom icons, Gatekeeper quarantine handling, and automated installation scripts.
4. **Continuous Integration (CI)**: Automated multi-OS GitHub Actions test suite running on Apple Silicon and Intel macOS across supported Python runtimes.

---

## 🏗️ Architecture & Directory Structure

```text
MacOS-Sleep-Timer/
├── AGENTS.md               # Agent & developer guidance (this file)
├── README.md               # User and developer documentation
├── pyproject.toml          # Poetry configuration & script entrypoints
├── poetry.toml             # In-project .venv isolation setting
├── poetry.lock             # Locked dependency manifest
├── requirements.txt        # Runtime dependencies (pip)
├── requirements-dev.txt    # Development & test dependencies (pip)
├── install.sh              # Unified installer (supports curl | bash & local execution)
├── build_app.sh            # Shell-based app bundling script
├── sleeptimer_build.py     # Python build automation (used by poetry run build-app)
├── .github/
│   └── workflows/
│       └── ci.yml          # GitHub Actions CI matrix (macOS 15, macOS 15 Intel, macOS 14)
├── tests/                  # Unittest test suite (34 tests)
│   ├── test_model.py       # Domain model logic tests
│   ├── test_controller.py  # GUI, auto-advance, zero fallback & lifecycle controller tests
│   ├── test_power_service.py # Power management service & notification tests
│   ├── test_menubar.py     # Menu bar item tests
│   └── test_build.py       # Build automation tests
├── assets/
│   └── screenshot.png      # Application screenshot
└── Contents/               # macOS bundle structure
    ├── Info.plist          # App metadata, bundle identifier, version info
    ├── MacOS/
    │   ├── SleepTimer      # Main Python executable & GUI application (MVC)
    │   └── MenuBarTimer.py # Menu bar tray application
    └── Resources/
        └── AppIcon.icns    # macOS application icon
```

### Core Components

- **`Contents/MacOS/SleepTimer`**:
  - Main application script using Model-View-Controller (MVC) architecture.
  - **`TimerModel`**: Manages time calculations, remaining seconds, and formatting.
  - **`SleepTimerView`**: Custom dark UI with circular canvas progress arc, entry auto-advance on 2 digits, text auto-selection on focus, and automatic `00` fallback when empty.
  - **`SleepTimerAppController`**: Orchestrates timer loops, dynamic sub-minute notification timing, preset buttons, and spawns `MenuBarTimer.py` (or self with `--menubar` in frozen builds) as a subprocess.
  - **`MacPowerService`**: System interface executing `/usr/bin/osascript` for notifications, `CGSession` for screen locking, and `pmset` for hibernation.
- **`Contents/MacOS/MenuBarTimer.py`**:
  - Independent menu bar status bar tool built using `rumps`.
  - Displays remaining countdown and allows opening the main window (`SIGUSR1`) or stopping the timer (`SIGUSR2`).
- **`sleeptimer_build.py`**:
  - Automated build script utilizing PyInstaller that packages a standalone, zero-dependency `dist/SleepTimer.app` and creates the `SleepTimer-v<version>-macOS.zip` consumer release archive (containing `SleepTimer.app` and `README.txt` with user setup and MIT license).
- **`install.sh`**:
  - CLI installer for automated `curl | bash` and local developer execution; automatically detects standalone bundles, copies `SleepTimer.app` to `/Applications`, and clears macOS quarantine flags (`/usr/bin/xattr -cr`).

---

## 🛠️ Development & Build Workflows

### Prerequisites
- macOS 14.0+ (Sonoma or later)
- Python 3.11+ (Standard library `tkinter` must be available)
- [Poetry](https://python-poetry.org/) (recommended) or `pip`

### Common Commands

| Task | Poetry Command | Pip / Direct Command |
| :--- | :--- | :--- |
| **Install Runtime Dependencies** | `poetry install --without dev` | `pip install -r requirements.txt` |
| **Install Dev Dependencies** | `poetry install` | `pip install -r requirements-dev.txt` |
| **Run App from Source** | `poetry run sleeptimer` | `python3 Contents/MacOS/SleepTimer` |
| **Run Unit Tests** | `poetry run python -m unittest discover -s tests` | `python3 -m unittest discover -s tests` |
| **Generate Test Coverage** | `poetry run coverage run --source=Contents/MacOS,sleeptimer_build -m unittest discover -s tests && poetry run coverage report` | `coverage report` |
| **Validate Info.plist** | `plutil -lint Contents/Info.plist` | `plutil -lint Contents/Info.plist` |
| **Build App Bundle & Archive** | `poetry run build-app` | `./build_app.sh` or `python3 sleeptimer_build.py` |

---

## 🤖 Continuous Integration (GitHub Actions)

The CI pipeline in `.github/workflows/ci.yml` automatically triggers on every push and pull request. It executes a test matrix across:
- **macOS Runners**:
  - `macos-15` (macOS Sequoia - Apple Silicon)
  - `macos-15-intel` (macOS Sequoia - Intel x86_64)
  - `macos-14` (macOS Sonoma - Apple Silicon)
- **Python Versions**: `3.11`, `3.12`, `3.13`

Each matrix job validates `Info.plist`, runs the 34 unit tests, checks test coverage, verifies packaging of `SleepTimer.app`, and assesses code signature integrity and Gatekeeper policy.

---

## 📋 Guidelines for Modifying Code

1. **Maintain Zero Heavy Dependencies**:
   - Keep GUI dependencies tied to Python's standard `tkinter`. Avoid introducing bulky GUI frameworks (e.g. Qt, Electron, wxPython).
   - Menu bar features should rely only on `rumps` and `pyobjc-framework-Cocoa`.

2. **macOS Compatibility & Security**:
   - Power management operations should use system utilities (`pmset`, `osascript`, `CGSession`).
   - Preserve Gatekeeper quarantine clearing logic (`xattr -cr`) in installation routines.

3. **Version Synchronization**:
   - When bumping the version, update all of the following:
     - `pyproject.toml` (`version`)
     - `Contents/Info.plist` (`CFBundleVersion` and `CFBundleShortVersionString`)
     - `sleeptimer_build.py` (`VERSION`)
     - `build_app.sh` (`ZIP_NAME`)
     - `install.sh` (`SleepTimer-v<version>-macOS.zip` download link)
     - `README.md` (release archive links)
     - `tests/test_build.py` (version assertions)

4. **Bundle Integrity**:
   - Always ensure executable permissions (`chmod +x`) on scripts inside `Contents/MacOS/` and `install.sh`.
   - Never remove `Contents/Info.plist` or `Contents/Resources/AppIcon.icns`.
