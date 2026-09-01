import os
import signal
import sys
import time
import unittest
from pathlib import Path
from unittest.mock import patch, MagicMock

# Add Contents/MacOS to sys.path to allow importing MenuBarTimer
ROOT = Path(__file__).resolve().parent.parent
MACOS_DIR = ROOT / "Contents" / "MacOS"
if str(MACOS_DIR) not in sys.path:
    sys.path.insert(0, str(MACOS_DIR))

import MenuBarTimer


class TestMenuBarTimer(unittest.TestCase):
    @patch("MenuBarTimer.NSRunLoop")
    @patch("MenuBarTimer.rumps.Timer")
    def test_timerbar_initialization(self, mock_timer, mock_runloop):
        timer_inst = MagicMock()
        mock_timer.return_value = timer_inst

        app = MenuBarTimer.TimerBar(remaining=1800, parent_pid=12345)
        self.assertEqual(app.parent_pid, 12345)
        self.assertGreater(app.end_time, time.time())
        mock_timer.assert_called_once_with(app.tick, 1)
        timer_inst.start.assert_called_once()

    @patch("MenuBarTimer.NSRunLoop")
    @patch("MenuBarTimer.rumps.Timer")
    def test_timerbar_tick_updates_title(self, mock_timer, mock_runloop):
        mock_timer.return_value = MagicMock()
        app = MenuBarTimer.TimerBar(remaining=3665, parent_pid=None)
        app.tick(None)
        self.assertTrue("01:01:0" in app.title)
        self.assertTrue(app.title.endswith("😴"))

    @patch("MenuBarTimer.NSRunLoop")
    @patch("MenuBarTimer.rumps.quit_application")
    @patch("MenuBarTimer.rumps.Timer")
    def test_timerbar_tick_quits_when_elapsed(self, mock_timer, mock_quit, mock_runloop):
        mock_timer.return_value = MagicMock()
        app = MenuBarTimer.TimerBar(remaining=0, parent_pid=None)
        app.end_time = time.time() - 10
        app.tick(None)
        self.assertTrue(mock_quit.called)

    @patch("MenuBarTimer.NSRunLoop")
    @patch("MenuBarTimer.os.kill")
    @patch("MenuBarTimer.rumps.Timer")
    def test_timerbar_show_app_sends_sigusr1(self, mock_timer, mock_kill, mock_runloop):
        mock_timer.return_value = MagicMock()
        app = MenuBarTimer.TimerBar(remaining=100, parent_pid=9999)
        app.show_app(None)
        mock_kill.assert_called_once_with(9999, signal.SIGUSR1)

    @patch("MenuBarTimer.NSRunLoop")
    @patch("MenuBarTimer.rumps.quit_application")
    @patch("MenuBarTimer.os.kill")
    @patch("MenuBarTimer.rumps.Timer")
    def test_timerbar_stop_timer_sends_sigusr2_and_quits(self, mock_timer, mock_kill, mock_quit, mock_runloop):
        mock_timer.return_value = MagicMock()
        app = MenuBarTimer.TimerBar(remaining=100, parent_pid=9999)
        app.stop_timer(None)
        mock_kill.assert_called_once_with(9999, signal.SIGUSR2)
        mock_quit.assert_called_once()


if __name__ == "__main__":
    unittest.main()
