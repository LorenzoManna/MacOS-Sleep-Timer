# SleepTimer 😴

A sleek, modern macOS desktop application and menu bar tray tool for scheduling system sleep and hibernation. 

Built in Python using native Tkinter graphics and AppKit menu bar integration (`rumps`).

---

# 👤 For Users

## Features

- ⭕ **Circular Countdown Progress Ring**: Custom canvas rendering an animated 360-degree progress arc and bold countdown timer.
- ⏱️ **3-Box HMS Duration Input**: Dedicated input fields for Hours (`h`), Minutes (`m`), and Seconds (`s`) with live, real-time target sleep calculation (`Sleep scheduled for HH:MM:SS`).
- ⚡ **Quick Preset Duration Pills**: One-click duration setting (`15m`, `30m`, `45m`, `1h`, `2h`) with active pill highlights.
- 🔔 **macOS Menu Bar Tray Integration**: Seamless status display in your menu bar (`00:29:59 😴`) with quick restoration and cancel actions.
- 🔒 **Native Hibernation Execution**: Automatically locks the macOS user session (`CGSession`) and puts system hardware into safe sleep (`pmset`).

## How to Install & Use

1. **Download**: Go to [GitHub Releases](https://github.com/LorenzoManna/MacOS-Sleep-Timer/releases/latest) and download `SleepTimer-v1.0.0-macOS.zip`.
2. **Install**: Unzip and move `SleepTimer.app` into your `/Applications` folder.
3. **Run**: Double-click `SleepTimer.app` to launch the application.

---

# 💻 For Developers

## Prerequisites & Setup

- macOS 11.0 Big Sur or later
- Python 3.10+ (includes standard `tkinter` library)

### Installing Dependencies

Install the required Python packages using `requirements.txt`:

```bash
pip install -r requirements.txt
```

> **Note**: `tkinter` is built directly into Python's standard library and does not require `pip` installation.

## Running from Source

Launch the application directly from the executable script:

```bash
/Applications/SleepTimer.app/Contents/MacOS/SleepTimer
```

## Project Structure

```text
SleepTimer.app/
├── .gitignore
├── LICENSE.txt
├── README.md
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
