import unittest

from src import Comment, Issue
from src.mock_implementation import MockIssue, MockIssueTrackerClient


class TestProtocolBehavior(unittest.TestCase):
    def test_issue_get_comments(self):
        """Test that getting comments from an issue returns Comment objects."""
        issue = MockIssue()
        comments = list(issue.get_comments())
        self.assertTrue(len(comments) > 0)
        self.assertIsInstance(comments[0], Comment)

    def test_client_create_issue(self):
        """Test issue creation returns an Issue object."""
        client = MockIssueTrackerClient()
        issue = client.create_issue("New Issue", "Description")
        self.assertIsInstance(issue, Issue)

    def test_client_add_comment(self):
        """Test adding a comment returns a Comment object."""
        client = MockIssueTrackerClient()
        comment = client.add_comment("issue-1", "New comment")
        self.assertIsInstance(comment, Comment)


if __name__ == "__main__":
    unittest.main()
