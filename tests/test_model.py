from importlib.machinery import SourceFileLoader
import importlib.util
import time
import unittest
from pathlib import Path

# Dynamically import SleepTimer module from Contents/MacOS/SleepTimer
ROOT = Path(__file__).resolve().parent.parent
SRC_PATH = ROOT / "Contents" / "MacOS" / "SleepTimer"
loader = SourceFileLoader("SleepTimerModule", str(SRC_PATH))
spec = importlib.util.spec_from_file_location("SleepTimerModule", str(SRC_PATH), loader=loader)
sleeptimer = importlib.util.module_from_spec(spec)
loader.exec_module(sleeptimer)

TimerModel = sleeptimer.TimerModel


class TestTimerModel(unittest.TestCase):
    def setUp(self):
        self.model = TimerModel()

    def test_initial_state(self):
        self.assertEqual(self.model.remaining_seconds, 0)
        self.assertEqual(self.model.total_seconds, 0)
        self.assertFalse(self.model.is_running)

    def test_parse_hms_valid_integers(self):
        # 1 hour, 30 minutes, 15 seconds = 3600 + 1800 + 15 = 5415
        total = self.model.parse_hms("1", "30", "15")
        self.assertEqual(total, 5415)

    def test_parse_hms_empty_strings(self):
        self.assertEqual(self.model.parse_hms("", "", ""), 0)
        self.assertEqual(self.model.parse_hms(" ", "15", ""), 900)

    def test_parse_hms_invalid_strings(self):
        self.assertEqual(self.model.parse_hms("abc", "foo", "bar"), 0)
        self.assertEqual(self.model.parse_hms("1", "invalid", "30"), 3630)

    def test_parse_hms_negative_values(self):
        # Negative numbers should be bounded at minimum 0
        self.assertEqual(self.model.parse_hms("-1", "0", "0"), 0)

    def test_format_time(self):
        self.assertEqual(self.model.format_time(0), "00:00:00")
        self.assertEqual(self.model.format_time(59), "00:00:59")
        self.assertEqual(self.model.format_time(60), "00:01:00")
        self.assertEqual(self.model.format_time(3600), "01:00:00")
        self.assertEqual(self.model.format_time(3665), "01:01:05")

    def test_calculate_target_time_str_non_positive(self):
        self.assertEqual(
            self.model.calculate_target_time_str(0),
            "Set duration in hours, mins or secs"
        )
        self.assertEqual(
            self.model.calculate_target_time_str(-10),
            "Set duration in hours, mins or secs"
        )

    def test_calculate_target_time_str_positive(self):
        now = time.time()
        seconds = 3600
        target_str = self.model.calculate_target_time_str(seconds)
        self.assertTrue(target_str.startswith("Sleep scheduled for "))

    def test_get_progress_fraction(self):
        # Total <= 0 returns 0.0
        self.model.total_seconds = 0
        self.model.remaining_seconds = 0
        self.assertEqual(self.model.get_progress_fraction(), 0.0)

        # Fraction calculation
        self.model.total_seconds = 100
        self.model.remaining_seconds = 50
        self.assertAlmostEqual(self.model.get_progress_fraction(), 0.5)

        self.model.remaining_seconds = 100
        self.assertAlmostEqual(self.model.get_progress_fraction(), 1.0)


if __name__ == "__main__":
    unittest.main()
