from importlib.machinery import SourceFileLoader
import importlib.util
import tkinter as tk
import unittest
from pathlib import Path
from unittest.mock import patch, MagicMock

# Dynamically import SleepTimer module from Contents/MacOS/SleepTimer
ROOT = Path(__file__).resolve().parent.parent
SRC_PATH = ROOT / "Contents" / "MacOS" / "SleepTimer"
loader = SourceFileLoader("SleepTimerModule", str(SRC_PATH))
spec = importlib.util.spec_from_file_location("SleepTimerModule", str(SRC_PATH), loader=loader)
sleeptimer = importlib.util.module_from_spec(spec)
loader.exec_module(sleeptimer)

SleepTimerAppController = sleeptimer.SleepTimerAppController
PowerService = sleeptimer.PowerService


class MockPowerService(PowerService):
    def __init__(self):
        self.notifications = []
        self.hibernated = False

    def notify(self, message: str, sound: str = "Purr"):
        self.notifications.append((message, sound))

    def lock_and_hibernate(self):
        self.hibernated = True


class TestSleepTimerAppController(unittest.TestCase):
    def setUp(self):
        try:
            self.root = tk.Tk()
            self.root.withdraw()  # Hide GUI window during tests
        except Exception as e:
            self.skipTest(f"Tkinter display not available: {e}")

        self.power_service = MockPowerService()
        self.controller = SleepTimerAppController(self.root, power_service=self.power_service)

    def tearDown(self):
        if hasattr(self, "controller") and self.controller._bar_process:
            try:
                self.controller._bar_process.terminate()
            except Exception:
                pass
        if hasattr(self, "root"):
            try:
                self.root.destroy()
            except Exception:
                pass

    def test_preset_clicks(self):
        self.controller.on_preset_click("15m")
        self.assertEqual(self.controller.view.mins_var.get(), "15")
        self.assertEqual(self.controller.view.hours_var.get(), "0")

        self.controller.on_preset_click("1h")
        self.assertEqual(self.controller.view.hours_var.get(), "1")
        self.assertEqual(self.controller.view.mins_var.get(), "0")

        self.controller.on_preset_click("2h")
        self.assertEqual(self.controller.view.hours_var.get(), "2")
        self.assertEqual(self.controller.view.mins_var.get(), "0")

    def test_start_with_zero_seconds_fails_validation(self):
        self.controller.view.hours_var.set("0")
        self.controller.view.mins_var.set("0")
        self.controller.view.secs_var.set("0")

        self.controller.start()
        self.assertFalse(self.controller.model.is_running)
        self.assertEqual(self.controller.view.status_var.get(), "Set duration in hours, mins or secs")

    @patch("subprocess.Popen")
    def test_start_and_stop_lifecycle(self, mock_popen):
        mock_process = MagicMock()
        mock_popen.return_value = mock_process

        self.controller.view.mins_var.set("15")
        self.controller.start()

        self.assertTrue(self.controller.model.is_running)
        self.assertEqual(self.controller.model.total_seconds, 900)
        self.assertEqual(self.controller.view.start_btn.text, "Stop Timer")

        self.controller.stop()
        self.assertFalse(self.controller.model.is_running)
        self.assertEqual(self.controller.view.start_btn.text, "Start Timer")
        mock_process.terminate.assert_called_once()

    def test_toggle(self):
        with patch.object(self.controller, "start") as mock_start, \
             patch.object(self.controller, "stop") as mock_stop:
            self.controller.model.is_running = False
            self.controller.toggle()
            mock_start.assert_called_once()

            self.controller.model.is_running = True
            self.controller.toggle()
            mock_stop.assert_called_once()

    def test_fire_invokes_power_service(self):
        with patch("time.sleep"):
            self.controller._fire()
            self.assertTrue(self.power_service.hibernated)
            self.assertEqual(len(self.power_service.notifications), 1)


if __name__ == "__main__":
    unittest.main()
