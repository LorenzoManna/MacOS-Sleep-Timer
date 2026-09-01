# AGENTS.md

Welcome to the **MacOS Sleep Timer** repository. This document provides essential architectural context, development workflows, and coding conventions for AI agents and developers working on this codebase.

---

## 📌 Project Overview

**MacOS Sleep Timer** is a lightweight, modern macOS utility for scheduling system sleep, screen lock, and hibernation. It consists of:
1. **Main GUI Window**: Built using Python's standard `tkinter` library with custom dark-themed UI components (circular countdown timer, preset duration buttons, live clock preview).
2. **Menu Bar Status Item**: A background tray app built with `rumps` and `pyobjc-framework-Cocoa` that displays the remaining countdown in the macOS menu bar.
3. **macOS App Bundle (`SleepTimer.app`)**: Packaged as a standard macOS application directory structure with custom icons, Gatekeeper quarantine handling, and installation scripts.

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
├── tests/                  # Unittest test suite
│   ├── test_model.py       # Domain model logic tests
│   ├── test_controller.py  # GUI & lifecycle controller tests
│   ├── test_power_service.py # Power management service tests
│   ├── test_menubar.py     # Menu bar item tests
│   └── test_build.py       # Build automation tests
├── assets/
│   └── screenshot.png      # Application screenshot
└── Contents/               # macOS bundle structure
    ├── Info.plist          # App metadata, bundle identifier, version info
    ├── MacOS/
    │   ├── SleepTimer      # Main Python executable & GUI application
    │   └── MenuBarTimer.py # Menu bar tray application
    └── Resources/
        └── AppIcon.icns    # macOS application icon
```

### Core Components

- **`Contents/MacOS/SleepTimer`**:
  - Main application script using Model-View-Controller (MVC) architecture.
  - Implements `PowerService` interface and `MacPowerService` with `pmset`, `CGSession`, and `osascript` commands.
  - Handles process lifecycle and launches `MenuBarTimer.py` as a subprocess when a timer starts.
- **`Contents/MacOS/MenuBarTimer.py`**:
  - Independent menu bar status bar tool built using `rumps`.
  - Displays remaining countdown and allows opening the main window or stopping the timer.
- **`sleeptimer_build.py`**:
  - Automated build script that packages `dist/SleepTimer.app` and creates the `SleepTimer-v<version>-macOS.zip` distribution archive.
- **`install.sh`**:
  - Installs runtime dependencies, copies `SleepTimer.app` to `/Applications`, and clears macOS quarantine flags (`xattr -cr`).

---

## 🛠️ Development & Build Workflows

### Prerequisites
- macOS 11.0+ (Big Sur or later)
- Python 3.10+ (Standard library `tkinter` must be available)
- [Poetry](https://python-poetry.org/) (recommended) or `pip`

### Common Commands

| Task | Poetry Command | Pip / Direct Command |
| :--- | :--- | :--- |
| **Install Runtime Dependencies** | `poetry install --without dev` | `pip install -r requirements.txt` |
| **Install Dev Dependencies** | `poetry install` | `pip install -r requirements-dev.txt` |
| **Run App from Source** | `poetry run sleeptimer` | `python3 Contents/MacOS/SleepTimer` |
| **Run Unit Tests** | `poetry run python -m unittest discover -s tests` | `python3 -m unittest discover -s tests` |
| **Build App Bundle & Archive** | `poetry run build-app` | `./build_app.sh` or `python3 sleeptimer_build.py` |

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
     - `README.md` (release archive links)

4. **Bundle Integrity**:
   - Always ensure executable permissions (`chmod +x`) on scripts inside `Contents/MacOS/` and `install.sh`.
   - Never remove `Contents/Info.plist` or `Contents/Resources/AppIcon.icns`.
