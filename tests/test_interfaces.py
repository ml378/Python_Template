import unittest

from src import Comment, Issue, IssueTrackerClient
from src.mock_implementation import MockComment, MockIssue, MockIssueTrackerClient


class TestProtocolConformance(unittest.TestCase):
    def test_comment_protocol(self):
        """Test that MockComment conforms to Comment protocol."""
        comment = MockComment()
        self.assertIsInstance(comment, Comment)

    def test_issue_protocol(self):
        """Test that MockIssue conforms to Issue protocol."""
        issue = MockIssue()
        self.assertIsInstance(issue, Issue)

    def test_issue_tracker_client_protocol(self):
        """Test that MockIssueTrackerClient conforms to IssueTrackerClient protocol."""
        client = MockIssueTrackerClient()
        self.assertIsInstance(client, IssueTrackerClient)

    def test_incomplete_implementation(self):
        """Test that an incomplete implementation fails the protocol check."""

        class IncompleteComment:
            @property
            def id(self) -> str:
                return "comment-1"

        incomplete = IncompleteComment()
        self.assertNotIsInstance(incomplete, Comment)


if __name__ == "__main__":
    unittest.main()
