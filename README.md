# SleepTimer 😴

**Fall asleep to movies and music without worrying about your Mac staying on all night.**

SleepTimer is a sleek, native macOS countdown utility. When the timer ends, it puts your Mac into display sleep mode (`displaysleep`)—instantly stopping videos, Netflix, YouTube, Spotify, and podcasts to save battery.

<p align="center">
  <img src="assets/screenshot.png" alt="SleepTimer Screenshot" width="500">
</p>

## ✨ Features

- 🍿 **Bedtime Media Stop**: Display sleep instantly pauses video & audio playback.
- ⏱️ **Fast Entry & Presets**: Type exact time or pick presets (`15m`, `30m`, `45m`, `1h`, `2h`).
- 🕒 **Live Target Clock**: Shows the exact time when your Mac will sleep.
- ⭕ **Circular Countdown**: Clean native dark-mode progress ring.
- 🔔 **Menu Bar Status**: Follow the remaining time right from the menu bar.

## 🚀 Installation

### Option 1: Terminal (Fastest)

```bash
curl -fsSL https://raw.githubusercontent.com/LorenzoManna/MacOS-Sleep-Timer/main/install.sh | bash
```

### Option 2: Manual Download

1. Download **[`SleepTimer-v0.2.0-macOS.zip`](https://github.com/LorenzoManna/MacOS-Sleep-Timer/releases/latest)**.
2. Drag **`SleepTimer.app`** into `/Applications`.
3. *(First launch on macOS Sequoia)*: If blocked, go to **System Settings ➔ Privacy & Security** and click **Open Anyway** (or run `xattr -cr /Applications/SleepTimer.app`).

---

## 💻 Development

```bash
# Setup
git clone https://github.com/LorenzoManna/MacOS-Sleep-Timer.git && cd MacOS-Sleep-Timer
poetry install

# Run & Test
poetry run sleeptimer
poetry run python -m unittest discover -s tests

# Build standalone .app bundle
poetry run build-app
```

## 📄 License

MIT © 2026 Lorenzo Manna
