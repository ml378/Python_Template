import unittest
import sys, os
from typing import Any, Dict, Iterator, List, Optional

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from api.src import Comment, Issue, IssueTrackerClient
from api.src.issue_tracker import MemoryComment, MemoryIssue, MemoryIssueTrackerClient


class TestProtocolBehavior(unittest.TestCase):
    def test_issue_get_comments(self):
        """Test that getting comments from an issue returns Comment objects"""
        issue = MemoryIssue(title="Test Issue", description="Description", creator="user1")
        # Add a comment to the issue
        comment = MemoryComment(author="user1", content="Test comment")
        issue.add_comment(comment)
        
        # Check if we can retrieve the comment
        comments = list(issue.get_comments())
        self.assertEqual(len(comments), 1)
        self.assertIsInstance(comments[0], Comment)
        self.assertEqual(comments[0].content, "Test comment")
        
    def test_client_create_issue(self):
        """Test issue creation returns an Issue object"""
        client = MemoryIssueTrackerClient()
        client.set_current_user("test_user")
        issue = client.create_issue(
            title="New Issue", 
            description="Description",
            labels=["bug", "frontend"],
            priority="high"
        )
        self.assertIsInstance(issue, Issue)
        self.assertEqual(issue.title, "New Issue")
        self.assertEqual(issue.description, "Description")
        self.assertEqual(issue.creator, "test_user")
        self.assertEqual(issue.labels, ["bug", "frontend"])
        self.assertEqual(issue.priority, "high")
        
    def test_client_add_comment(self):
        """Test adding a comment returns a Comment object"""
        client = MemoryIssueTrackerClient()
        client.set_current_user("test_user")
        
        # First create an issue
        issue = client.create_issue("Test Issue", "Description")
        
        # Now add a comment to it
        comment = client.add_comment(issue.id, "New comment")
        
        self.assertIsInstance(comment, Comment)
        self.assertEqual(comment.content, "New comment")
        self.assertEqual(comment.author, "test_user")
        
        # Verify the comment is attached to the issue
        retrieved_issue = client.get_issue(issue.id)
        comments = list(retrieved_issue.get_comments())
        self.assertEqual(len(comments), 1)
        self.assertEqual(comments[0].content, "New comment")

    def test_update_issue(self):
        """Test updating an issue"""
        client = MemoryIssueTrackerClient()
        client.set_current_user("test_user")
        
        # Create an issue
        issue = client.create_issue("Original Title", "Original Description")
        
        # Update the issue
        updated_issue = client.update_issue(
            issue.id, 
            title="Updated Title",
            description="Updated Description",
            status="closed",
            assignee="another_user",
            labels=["feature"],
            priority="low"
        )
        
        # Verify the updates
        self.assertEqual(updated_issue.title, "Updated Title")
        self.assertEqual(updated_issue.description, "Updated Description")
        self.assertEqual(updated_issue.status, "closed")
        self.assertEqual(updated_issue.assignee, "another_user")
        self.assertEqual(updated_issue.labels, ["feature"])
        self.assertEqual(updated_issue.priority, "low")

    def test_search_issues(self):
        """Test searching for issues"""
        client = MemoryIssueTrackerClient()
        
        # Create some issues
        client.create_issue("Bug in login", "Users can't log in properly")
        client.create_issue("Feature request", "Add dark mode")
        client.create_issue("Another bug", "Form validation fails")
        
        # Search for "bug" issues
        bug_issues = list(client.search_issues("bug"))
        
        self.assertEqual(len(bug_issues), 2)
        titles = [issue.title for issue in bug_issues]
        self.assertIn("Bug in login", titles)
        self.assertIn("Another bug", titles)

if __name__ == "__main__":
    unittest.main()