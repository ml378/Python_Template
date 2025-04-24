import unittest
import sys, os
from typing import Any, Dict, Iterator, List, Optional

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from api.src import Comment, Issue, IssueTrackerClient
from api.src.issue_tracker import MemoryComment, MemoryIssue, MemoryIssueTrackerClient


class TestProtocolConformance(unittest.TestCase):
    def test_comment_protocol(self):
        """Test that MemoryComment conforms to Comment protocol"""
        comment = MemoryComment(author="user1", content="This is a comment")
        self.assertIsInstance(comment, Comment)
        
    def test_issue_protocol(self):
        """Test that MemoryIssue conforms to Issue protocol"""
        issue = MemoryIssue(title="Test Issue", description="Description of test issue", creator="user1")
        self.assertIsInstance(issue, Issue)
        
    def test_issue_tracker_client_protocol(self):
        """Test that MemoryIssueTrackerClient conforms to IssueTrackerClient protocol"""
        client = MemoryIssueTrackerClient()
        self.assertIsInstance(client, IssueTrackerClient)

if __name__ == "__main__":
    unittest.main()