"""Tests for the JSON storage implementation of the issue tracker.
"""
import os
import tempfile
import unittest

from src.json_storage import JsonIssueTrackerClient


class TestJsonIssueTrackerClient(unittest.TestCase):
    """Test cases for the JSON file storage implementation."""

    def setUp(self):
        """Create a temporary file for testing."""
        self.temp_file = tempfile.NamedTemporaryFile(delete=False)
        self.temp_file.close()
        self.client = JsonIssueTrackerClient(self.temp_file.name)

    def tearDown(self):
        """Remove the temporary file after tests."""
        if os.path.exists(self.temp_file.name):
            os.unlink(self.temp_file.name)

    def test_create_issue(self):
        """Test creating a new issue."""
        issue = self.client.create_issue("Test Issue", "This is a test issue")

        self.assertIsNotNone(issue["id"])
        self.assertEqual(issue["title"], "Test Issue")
        self.assertEqual(issue["description"], "This is a test issue")
        self.assertEqual(issue["status"], "open")

        # Verify it was saved to the file
        saved_client = JsonIssueTrackerClient(self.temp_file.name)
        saved_issue = saved_client.get_issue(issue["id"])
        self.assertEqual(saved_issue["title"], "Test Issue")

    def test_get_issue(self):
        """Test retrieving an issue by ID."""
        issue = self.client.create_issue("Test Issue", "Description")
        retrieved_issue = self.client.get_issue(issue["id"])

        self.assertEqual(retrieved_issue["title"], "Test Issue")
        self.assertEqual(retrieved_issue["id"], issue["id"])

        # Test getting non-existent issue
        self.assertIsNone(self.client.get_issue("non-existent-id"))

    def test_update_issue(self):
        """Test updating an existing issue."""
        issue = self.client.create_issue("Original Title", "Original Description")

        # Update the issue
        updated = self.client.update_issue(
            issue["id"],
            title="Updated Title",
            status="closed"
        )

        self.assertEqual(updated["title"], "Updated Title")
        self.assertEqual(updated["description"], "Original Description")
        self.assertEqual(updated["status"], "closed")

        # Verify it was saved
        saved_client = JsonIssueTrackerClient(self.temp_file.name)
        saved_issue = saved_client.get_issue(issue["id"])
        self.assertEqual(saved_issue["title"], "Updated Title")

        # Test updating non-existent issue
        self.assertIsNone(self.client.update_issue("non-existent-id", title="New"))

    def test_delete_issue(self):
        """Test deleting an issue."""
        issue = self.client.create_issue("Test Issue", "Description")

        # Verify it exists
        self.assertIsNotNone(self.client.get_issue(issue["id"]))

        # Delete it
        result = self.client.delete_issue(issue["id"])
        self.assertTrue(result)

        # Verify it's gone
        self.assertIsNone(self.client.get_issue(issue["id"]))

        # Test deleting non-existent issue
        self.assertFalse(self.client.delete_issue("non-existent-id"))

    def test_list_issues(self):
        """Test listing all issues with optional filtering."""
        # Create some test issues
        self.client.create_issue("Issue 1", "Description 1", status="open")
        self.client.create_issue("Issue 2", "Description 2", status="closed")
        self.client.create_issue("Issue 3", "Description 3", status="open")

        # Test listing all issues
        all_issues = self.client.list_issues()
        self.assertEqual(len(all_issues), 3)

        # Test filtering by status
        open_issues = self.client.list_issues(status="open")
        self.assertEqual(len(open_issues), 2)

        closed_issues = self.client.list_issues(status="closed")
        self.assertEqual(len(closed_issues), 1)
        self.assertEqual(closed_issues[0]["title"], "Issue 2")


if __name__ == "__main__":
    unittest.main()
