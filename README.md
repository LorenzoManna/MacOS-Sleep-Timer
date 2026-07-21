# SleepTimer 😴

A sleek, modern macOS desktop application and menu bar tray tool for scheduling system sleep and hibernation. 

Built in Python using native Tkinter graphics and AppKit menu bar integration (`rumps`).

---

## Features

- ⭕ **Circular Countdown Progress Ring**: Custom canvas rendering an animated 360-degree progress arc and bold countdown timer.
- ⏱️ **3-Box HMS Duration Input**: Dedicated input fields for Hours (`h`), Minutes (`m`), and Seconds (`s`) with live, real-time target sleep calculation (`Sleep scheduled for HH:MM:SS`).
- ⚡ **Quick Preset Duration Pills**: One-click duration setting (`15m`, `30m`, `45m`, `1h`, `2h`) with active pill highlights.
- 🔔 **macOS Menu Bar Tray Integration**: Seamless tray status display (`00:29:59 😴`) with inter-process POSIX signal handling (`SIGUSR1` / `SIGUSR2`) to bring the main window to front or cancel the timer.
- 🔒 **Native Hibernation Execution**: Automatically locks the macOS user session (`CGSession`) and puts system hardware into safe sleep (`pmset`).

---

## Installation & Build Instructions

### Requirements
- macOS 11.0 Big Sur or later
- Python 3.10+ (includes standard `tkinter` library)

### 1. Install Dependencies
Install Python dependencies using `requirements.txt`:

```bash
pip install -r requirements.txt
```

> **Note**: `tkinter` is built directly into Python's standard library and does not require `pip` installation.

### 2. Build the Application Bundle
Run the build script to assemble the `SleepTimer.app` bundle in the `dist` directory:

```bash
./build_app.sh
```

### 3. Install to macOS Applications
Move the newly built `dist/SleepTimer.app` bundle to your macOS `/Applications` directory:

```bash
cp -R dist/SleepTimer.app /Applications/
```

---

## Running the App

After moving `SleepTimer.app` to your `/Applications` directory, launch it via Spotlight, Finder, or Terminal:

```bash
open /Applications/SleepTimer.app
```

---

## Project Structure

```text
SleepTimer/
├── .gitignore
├── LICENSE.txt
├── README.md
├── build_app.sh
├── requirements.txt
└── Contents/
    ├── Info.plist
    ├── MacOS/
    │   ├── MenuBarTimer.py
    │   └── SleepTimer
    └── Resources/
        └── AppIcon.icns
```

---

## License

Distributed under the [MIT License](LICENSE.txt). Copyright (c) 2026 Lorenzo Manna.
