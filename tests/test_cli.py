"""Tests for the CLI interface of the issue tracker.
"""
import os
import sys
import tempfile
import unittest
from io import StringIO

from src.cli import main


class TestCli(unittest.TestCase):
    """Test cases for the CLI interface."""

    def setUp(self):
        """Set up temporary file for JSON storage."""
        self.temp_file = tempfile.NamedTemporaryFile(delete=False)
        self.temp_file.close()
        self.storage_path = self.temp_file.name

        # Capture stdout
        self.captured_output = StringIO()
        self.original_stdout = sys.stdout
        sys.stdout = self.captured_output

        # Save original argv
        self.original_argv = sys.argv

    def tearDown(self):
        """Restore stdout and clean up temporary files."""
        sys.stdout = self.original_stdout
        sys.argv = self.original_argv

        if os.path.exists(self.storage_path):
            os.unlink(self.storage_path)

    def _get_output(self):
        """Helper to get captured stdout."""
        return self.captured_output.getvalue().strip()

    def test_create_issue_command(self):
        """Test the 'create' command in CLI."""
        # Directly modify sys.argv
        sys.argv = [
            "issue-tracker",
            "--storage", "json",
            "--storage-path", self.storage_path,
            "create",
            "Test Issue",
            "Test Description"
        ]

        main()
        output = self._get_output()
        self.assertIn("Issue created with ID:", output)
        self.assertIn("Title: Test Issue", output)

    def test_list_issues_command(self):
        """Test the 'list' command in CLI."""
        # First create an issue
        sys.argv = [
            "issue-tracker",
            "--storage", "json",
            "--storage-path", self.storage_path,
            "create",
            "Test Issue",
            "Test Description"
        ]

        main()
        self.captured_output.truncate(0)
        self.captured_output.seek(0)

        # Then list issues
        sys.argv = [
            "issue-tracker",
            "--storage", "json",
            "--storage-path", self.storage_path,
            "list"
        ]

        main()
        output = self._get_output()
        self.assertIn("Title: Test Issue", output)

    def test_get_issue_command(self):
        """Test the 'get' command in CLI."""
        # First create an issue and get its ID
        sys.argv = [
            "issue-tracker",
            "--storage", "json",
            "--storage-path", self.storage_path,
            "create",
            "Test Issue",
            "Test Description"
        ]

        main()
        output = self._get_output()
        issue_id = output.split("Issue created with ID:")[1].split("\n")[0].strip()

        self.captured_output.truncate(0)
        self.captured_output.seek(0)

        # Then get the issue details
        sys.argv = [
            "issue-tracker",
            "--storage", "json",
            "--storage-path", self.storage_path,
            "get",
            issue_id
        ]

        main()
        output = self._get_output()
        self.assertIn(f"ID: {issue_id}", output)
        self.assertIn("Title: Test Issue", output)
        self.assertIn("Description: Test Description", output)


if __name__ == "__main__":
    unittest.main()
