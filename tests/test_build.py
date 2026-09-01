import os
import stat
import tempfile
import unittest
from pathlib import Path

import sleeptimer_build


class TestBuildAutomation(unittest.TestCase):
    def test_version_defined(self):
        self.assertEqual(sleeptimer_build.VERSION, "0.1.1")

    def test_project_root_exists(self):
        self.assertTrue(sleeptimer_build.PROJECT_ROOT.exists())
        self.assertTrue((sleeptimer_build.PROJECT_ROOT / "Contents").exists())

    def test_make_executable(self):
        with tempfile.NamedTemporaryFile(delete=False) as f:
            temp_path = Path(f.name)

        try:
            # Remove execute permissions
            temp_path.chmod(0o644)
            sleeptimer_build.make_executable(temp_path)
            mode = temp_path.stat().st_mode
            self.assertTrue(bool(mode & stat.S_IXUSR))
        finally:
            if temp_path.exists():
                temp_path.unlink()


if __name__ == "__main__":
    unittest.main()
