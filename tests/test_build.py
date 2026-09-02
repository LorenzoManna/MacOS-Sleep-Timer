import os
import stat
import tempfile
import unittest
from pathlib import Path

import sleeptimer_build


class TestBuildAutomation(unittest.TestCase):
    def test_version_defined(self):
        self.assertEqual(sleeptimer_build.VERSION, "0.2.0")

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
        finally:
            if temp_path.exists():
                temp_path.unlink()

    def test_create_release_archive(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            src_dir = Path(tmpdir) / "dist"
            src_dir.mkdir()
            sample_file = src_dir / "sample.txt"
            sample_file.write_text("Hello World")
            sample_link = src_dir / "link.txt"
            try:
                sample_link.symlink_to("sample.txt")
            except OSError:
                pass  # On systems where symlinks aren't permitted

            out_zip = Path(tmpdir) / "output.zip"
            sleeptimer_build.create_release_archive(src_dir, out_zip)
            self.assertTrue(out_zip.exists())
            self.assertGreater(out_zip.stat().st_size, 0)

    def test_generate_release_readme(self):
        readme = sleeptimer_build.generate_release_readme("0.2.0")
        self.assertIn("SleepTimer for macOS (v0.2.0)", readme)
        self.assertIn("HOW TO INSTALL", readme)
        self.assertIn("Applications", readme)
        self.assertIn("FIRST LAUNCH NOTE", readme)
        self.assertIn("Open Anyway", readme)
        self.assertIn("LICENSE", readme)


if __name__ == "__main__":
    unittest.main()
