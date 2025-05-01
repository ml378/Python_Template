import unittest

import pytest

from src.issue_tracker import MemoryComment, MemoryIssue, MemoryIssueTrackerClient


class TestMemoryIssueTrackerClient(unittest.TestCase):
    """Tests for the MemoryIssueTrackerClient class."""

    def setUp(self):
        """Set up a fresh client for each test."""
        self.client = MemoryIssueTrackerClient()

    def setup_test_issues(self):
        """Set up test issues."""
        self.client.set_current_user("user1")
        self.client.create_issue(
            "Bug 1",
            "Description for bug 1",
            status="open",
            labels=["bug", "ui"],
            priority="high",
        )
        self.client.create_issue(
            "Feature Request",
            "Add new feature",
            status="open",
            labels=["feature"],
            assignee="user2",
        )
        self.client.set_current_user("user2")
        self.client.create_issue(
            "Bug 2",
            "Another bug description",
            status="closed",
            labels=["bug", "backend"],
            assignee="user1",
        )
        self.client.set_current_user("default_user")  # Reset user for subsequent tests

    def test_init(self):
        """Test client initialization."""
        self.assertIsInstance(self.client.get_issue_dict(), dict)
        self.assertEqual(len(self.client.get_issue_dict()), 0)
        self.assertEqual(self.client.get_current_user(), "default_user")

    def test_set_current_user(self):
        """Test setting the current user."""
        self.client.set_current_user("test_user")
        self.assertEqual(self.client.get_current_user(), "test_user")

    def test_create_issue(self):
        """Test creating a new issue."""
        self.client.set_current_user("creator_user")
        issue = self.client.create_issue(
            "New Issue",
            "Issue Description",
            labels=["test"],
            priority="medium",
            assignee="assignee_user",
        )
        self.assertIsInstance(issue, MemoryIssue)
        self.assertEqual(issue.title, "New Issue")
        self.assertEqual(issue.description, "Issue Description")
        self.assertEqual(issue.creator, "creator_user")
        self.assertEqual(issue.status, "open")  # Default status
        self.assertEqual(issue.labels, ["test"])
        self.assertEqual(issue.priority, "medium")
        self.assertEqual(issue.assignee, "assignee_user")
        self.assertIn(issue.id, self.client.get_issue_dict())
        self.assertEqual(self.client.get_issue_dict()[issue.id], issue)

    def test_get_issue(self):
        """Test retrieving a specific issue."""
        self.setup_test_issues()
        issue_id = next(iter(self.client.get_issue_dict().keys()))
        issue = self.client.get_issue(issue_id)
        self.assertEqual(issue.id, issue_id)
        self.assertEqual(issue.title, "Bug 1")

    def test_get_issue_not_found(self):
        """Test retrieving a non-existent issue raises ValueError."""
        with pytest.raises(ValueError, match="Issue with ID non_existent_id not found"):
            self.client.get_issue("non_existent_id")

    def test_get_issues_no_filters(self):
        """Test retrieving all issues without filters."""
        self.setup_test_issues()
        issues = list(self.client.get_issues())
        self.assertEqual(len(issues), 3)
        titles = {issue.title for issue in issues}
        self.assertEqual(titles, {"Bug 1", "Feature Request", "Bug 2"})

    def test_get_issues_with_filters(self):
        """Test retrieving issues with various filters."""
        self.setup_test_issues()
        # Filter by status
        open_issues = list(self.client.get_issues(filters={"status": "open"}))
        self.assertEqual(len(open_issues), 2)
        self.assertEqual({issue.title for issue in open_issues}, {"Bug 1", "Feature Request"})

        # Filter by labels
        bug_issues = list(self.client.get_issues(filters={"labels": ["bug"]}))
        self.assertEqual(len(bug_issues), 2)
        self.assertEqual({issue.title for issue in bug_issues}, {"Bug 1", "Bug 2"})

        # Filter by multiple criteria
        open_bug_issues = list(
            self.client.get_issues(filters={"status": "open", "labels": ["bug"]}),
        )
        self.assertEqual(len(open_bug_issues), 1)
        self.assertEqual(open_bug_issues[0].title, "Bug 1")

    def test_update_issue(self):
        """Test updating an existing issue."""
        self.setup_test_issues()
        issue_id = next(iter(self.client.get_issue_dict().keys()))
        original_issue = self.client.get_issue(issue_id)
        original_updated_at = original_issue.updated_at

        updated_issue = self.client.update_issue(
            issue_id,
            title="Updated Bug 1",
            status="in_progress",
            assignee="user3",
            labels=["bug", "critical"],
            priority="critical",
        )

        self.assertEqual(updated_issue.id, issue_id)
        self.assertEqual(updated_issue.title, "Updated Bug 1")
        self.assertEqual(updated_issue.status, "in_progress")
        self.assertEqual(updated_issue.assignee, "user3")
        self.assertEqual(updated_issue.labels, ["bug", "critical"])
        self.assertEqual(updated_issue.priority, "critical")
        self.assertNotEqual(updated_issue.updated_at, original_updated_at)

        # Verify update is reflected in storage
        stored_issue = self.client.get_issue(issue_id)
        self.assertEqual(stored_issue.title, "Updated Bug 1")
        self.assertEqual(stored_issue.status, "in_progress")

    def test_update_issue_not_found(self):
        """Test updating a non-existent issue raises ValueError."""
        with pytest.raises(ValueError, match="Issue with ID non_existent_id not found"):
            self.client.update_issue("non_existent_id", title="Doesn't Matter")

    def test_add_comment(self):
        """Test adding a comment to an issue."""
        self.setup_test_issues()
        issue_id = next(iter(self.client.get_issue_dict().keys()))
        self.client.set_current_user("commenter_user")
        comment_content = "This is a test comment."

        comment = self.client.add_comment(issue_id, comment_content)

        self.assertIsInstance(comment, MemoryComment)
        self.assertEqual(comment.author, "commenter_user")
        self.assertEqual(comment.content, comment_content)
        self.assertIsNotNone(comment.id)
        self.assertIsNotNone(comment.created_at)

        # Verify comment is added to the issue
        issue = self.client.get_issue(issue_id)
        comments = list(issue.get_comments())
        self.assertEqual(len(comments), 1)
        self.assertEqual(comments[0], comment)
        self.assertEqual(comments[0].content, comment_content)

    def test_add_comment_issue_not_found(self):
        """Test adding a comment to a non-existent issue raises ValueError."""
        with pytest.raises(ValueError, match="Issue with ID non_existent_id not found"):
            self.client.add_comment("non_existent_id", "Some comment")

    def test_search_issues(self):
        """Test searching issues by query string."""
        self.setup_test_issues()

        # Search in title
        results_bug = list(self.client.search_issues("Bug"))
        self.assertEqual(len(results_bug), 2)
        self.assertEqual({issue.title for issue in results_bug}, {"Bug 1", "Bug 2"})

        # Search in description
        results_description = list(self.client.search_issues("another bug"))
        self.assertEqual(len(results_description), 1)
        self.assertEqual(results_description[0].title, "Bug 2")

    def test_close_issue(self):
        """Test closing an issue with resolution."""
        self.setup_test_issues()
        issue_id = next(iter(self.client.get_issue_dict().keys()))

        closed_issue = self.client.close_issue(issue_id, "fixed")

        self.assertEqual(closed_issue.status, "closed")

        # Verify a comment was added with the resolution
        comments = list(closed_issue.get_comments())
        self.assertEqual(len(comments), 1)
        self.assertIn("fixed", comments[0].content)


if __name__ == "__main__":
    unittest.main()
