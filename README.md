# SleepTimer 😴

A sleek, modern macOS application and menu bar tray tool for scheduling system sleep and hibernation.

---

## 👤 For Users

### Overview
SleepTimer allows you to easily set a sleep countdown for your Mac. Once the countdown finishes, your session is securely locked and your Mac enters hibernation mode.

### Key Features
- ⭕ **Circular Countdown Progress Ring**: Beautiful animated countdown arc showing remaining time at a glance.
- ⏱️ **3-Box Duration Input**: Dedicated, large input fields for **Hours** (`h`), **Minutes** (`m`), and **Seconds** (`s`).
- 🕒 **Live Target Time Calculation**: Instantly displays the exact scheduled hibernation time (`Sleep scheduled for HH:MM:SS`) as you type.
- ⚡ **Quick Preset Pills**: One-click duration presets (`15m`, `30m`, `45m`, `1h`, `2h`).
- 🔔 **Menu Bar Integration**: Minimizes cleanly to your macOS menu bar (`00:29:59 😴`). Clicking the menu bar item instantly brings the main timer window back into focus.
- 🔒 **Secure Hibernation**: Automatically locks your user session (`CGSession`) and initiates safe sleep (`pmset`).

### How to Install & Use
1. Download the latest `SleepTimer-v1.0.0-macOS.zip` from [GitHub Releases](https://github.com/LorenzoManna/MacOS-Sleep-Timer/releases).
2. Extract the archive and launch **`SleepTimer.app`**.
3. Choose a preset or enter your desired duration in hours, minutes, and seconds.
4. Verify the scheduled sleep time and click **Start Timer**.

---

## 💻 For Developers

### Prerequisites
- macOS 11.0 (Big Sur) or later
- Python 3.10+

### Setup & Dependencies
1. Clone the repository:
   ```bash
   git clone https://github.com/LorenzoManna/MacOS-Sleep-Timer.git
   cd MacOS-Sleep-Timer
   ```

2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```
   > **Note**: `tkinter` is built directly into Python's standard library and does not require `pip` installation.

### Running from Source
Execute the main application script:

```bash
python3 Contents/MacOS/SleepTimer
```

### Project Structure
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

## 📄 License

Distributed under the [MIT License](LICENSE.txt). Copyright (c) 2026 Lorenzo Manna.
