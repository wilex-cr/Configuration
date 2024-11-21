import unittest
import io
from contextlib import redirect_stdout
import tarfile
import os
import tempfile
import shutil

from src.emulator import Emulator


class TestEmulator(unittest.TestCase):

    def setUp(self):
        self.temp_archive = tempfile.NamedTemporaryFile(delete=False)
        self.temp_archive_path = self.temp_archive.name
        self.temp_archive.close()

        shutil.copyfile("example_data/for_testing.tar", self.temp_archive_path)

        self.emulator = Emulator("testcomputer", self.temp_archive_path)

    def tearDown(self):
        if self.emulator.filesystem:
            self.emulator.filesystem.close()
        os.remove(self.temp_archive_path)

    def assert_output(self, expected_output, method, *args, **kwargs):
        """Asserts that calling method with the given arguments produces the expected output to stdout."""
        f = io.StringIO()
        with redirect_stdout(f):
            method(*args, **kwargs)

        output = f.getvalue().strip()
        if isinstance(expected_output, list):
            expected_output = "\n".join(expected_output)
        self.assertEqual(output, expected_output)

    # ls tests
    def test_ls_root(self):
        expected_output = [
            ".gitattributes",
            ".gitignore",
            "README.md",
            "java_prac_3/",
            "java_prac_4/",
        ]
        self.assert_output(
            expected_output, self.emulator.execute_command, "ls /")

    def test_ls_relative(self):
        expected_output = ["vehicles/"]
        self.assert_output(
            expected_output, self.emulator.execute_command, "ls java_prac_3")

    # cd tests
    def test_cd_relative(self):
        expected_output = "/java_prac_3"
        self.emulator.execute_command("cd java_prac_3")
        self.assert_output(
            expected_output, self.emulator.execute_command, "pwd")

    def test_cd_invalid_path(self):
        expected_output = "cd: can't cd to someshittyfile: No such file or directory"
        self.assert_output(
            expected_output, self.emulator.execute_command, "cd someshittyfile")

    # pwd tests
    def test_pwd_initial_directory(self):
        self.assert_output("/", self.emulator.execute_command, "pwd")

    def test_pwd_after_cd(self):
        self.emulator.execute_command("cd java_prac_3")
        self.assert_output(
            "/java_prac_3", self.emulator.execute_command, "pwd")

    # history tests
    def test_history_initial(self):
        self.emulator.history.append("history")
        self.assert_output(
            "1 history", self.emulator.execute_command, "history")

    def test_history_cd(self):
        self.emulator.history.append("cd java_prac_3")
        self.emulator.history.append("history")
        self.assert_output(["1 cd java_prac_3", "2 history"],
                           self.emulator.execute_command, "history")

    # mkdir tests
    def test_mkdir_creates_directory(self):
        self.emulator.execute_command("mkdir testdir")
        f = io.StringIO()
        with redirect_stdout(f):
            self.emulator.execute_command("ls")
        output = f.getvalue().strip()
        self.assertIn("testdir/", output)

    def test_mkdir_existing_directory(self):
        self.emulator.execute_command("mkdir testdir")
        expected_output = "mkdir: cannot create directory 'testdir': File exists"
        self.assert_output(
            expected_output, self.emulator.execute_command, "mkdir testdir")


if __name__ == '__main__':
    unittest.main()
