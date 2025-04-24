import unittest
import sys, os
from typing import Iterator, List, Optional

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from api.src import Comment, Issue, IssueTrackerClient
from api.src.issue_tracker import MemoryComment, MemoryIssue, MemoryIssueTrackerClient


class TypeCheckingTests(unittest.TestCase):
    """
    These tests verify that our implementations satisfy the protocol type requirements.
    """
    
    def test_comment_types(self) -> None:
        comment: Comment = MemoryComment(author="user", content="content")
        self.assertIsInstance(comment, Comment)
        
    def test_issue_types(self) -> None:
        issue: Issue = MemoryIssue(title="title", description="desc", creator="user")
        self.assertIsInstance(issue, Issue)
        
    def test_client_types(self) -> None:
        client: IssueTrackerClient = MemoryIssueTrackerClient()
        self.assertIsInstance(client, IssueTrackerClient)

if __name__ == "__main__":
    unittest.main()