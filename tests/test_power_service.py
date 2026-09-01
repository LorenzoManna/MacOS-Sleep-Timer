from importlib.machinery import SourceFileLoader
import importlib.util
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

PowerService = sleeptimer.PowerService
MacPowerService = sleeptimer.MacPowerService


class DummyPowerService(PowerService):
    def __init__(self):
        self.notifications = []
        self.hibernated = False

    def notify(self, message: str, sound: str = "Purr"):
        self.notifications.append((message, sound))

    def lock_and_hibernate(self):
        self.hibernated = True


class TestPowerService(unittest.TestCase):
    def test_custom_power_service_implementation(self):
        service = DummyPowerService()
        service.notify("Going to sleep", "Basso")
        self.assertEqual(len(service.notifications), 1)
        self.assertEqual(service.notifications[0], ("Going to sleep", "Basso"))

        service.lock_and_hibernate()
        self.assertTrue(service.hibernated)

    @patch("subprocess.Popen")
    def test_mac_power_service_notify(self, mock_popen):
        service = MacPowerService()
        service.notify("Test Message", "Purr")
        mock_popen.assert_called_once()
        args, kwargs = mock_popen.call_args
        self.assertEqual(args[0][0], "osascript")
        self.assertIn('Test Message', args[0][2])
        self.assertIn('Purr', args[0][2])

    @patch("time.sleep")
    @patch("subprocess.run")
    def test_mac_power_service_lock_and_hibernate_success(self, mock_run, mock_sleep):
        service = MacPowerService()
        service.lock_and_hibernate()
        self.assertTrue(mock_run.called)
        # Should call lock, sleep mode 25, and sleepnow
        self.assertGreaterEqual(mock_run.call_count, 3)


if __name__ == "__main__":
    unittest.main()
