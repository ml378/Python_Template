import unittest
from typing import Any, Dict, Iterator, List, Optional

from api.src import Comment, Issue, IssueTrackerClient


class MockComment:
    @property
    def id(self) -> str:
        return "comment-1"

    @property
    def author(self) -> str:
        return "user1"

    @property
    def content(self) -> str:
        return "This is a comment"
        
    @property
    def created_at(self) -> str:
        return "2023-01-01"

class MockIssue:
    @property
    def id(self) -> str:
        return "issue-1"
        
    @property
    def title(self) -> str:
        return "Test Issue"
        
    @property
    def description(self) -> str:
        return "Description of test issue"
        
    @property
    def status(self) -> str:
        return "open"
        
    @property
    def creator(self) -> str:
        return "user1"
        
    @property
    def assignee(self) -> Optional[str]:
        return "user2"
        
    @property
    def created_at(self) -> str:
        return "2023-01-01"
        
    @property
    def updated_at(self) -> str:
        return "2023-01-02"
        
    @property
    def labels(self) -> List[str]:
        return ["bug", "frontend"]
        
    @property
    def priority(self) -> Optional[str]:
        return "high"
        
    def get_comments(self) -> Iterator[Comment]:
        yield MockComment()

class MockIssueTrackerClient:
    def get_issues(self, filters: Optional[Dict[str, Any]] = None) -> Iterator[Issue]:
        yield MockIssue()
        
    def get_issue(self, issue_id: str) -> Issue:
        return MockIssue()
        
    def create_issue(self, title: str, description: str, **kwargs) -> Issue:
        return MockIssue()
        
    def update_issue(self, issue_id: str, **kwargs) -> Issue:
        return MockIssue()
        
    def add_comment(self, issue_id: str, content: str) -> Comment:
        return MockComment()
        
    def search_issues(self, query: str) -> Iterator[Issue]:
        yield MockIssue()

class TestProtocolConformance(unittest.TestCase):
    def test_comment_protocol(self):
        """Test that MockComment conforms to Comment protocol"""
        comment = MockComment()
        self.assertIsInstance(comment, Comment)
        
    def test_issue_protocol(self):
        """Test that MockIssue conforms to Issue protocol"""
        issue = MockIssue()
        self.assertIsInstance(issue, Issue)
        
    def test_issue_tracker_client_protocol(self):
        """Test that MockIssueTrackerClient conforms to IssueTrackerClient protocol"""
        client = MockIssueTrackerClient()
        self.assertIsInstance(client, IssueTrackerClient)
        
    def test_incomplete_implementation(self):
        """Test that an incomplete implementation fails the protocol check"""
        class IncompleteComment:
            @property
            def id(self) -> str:
                return "comment-1"
            
            # Missing other required properties
        
        incomplete = IncompleteComment()
        self.assertNotIsInstance(incomplete, Comment)

if __name__ == "__main__":
    unittest.main()