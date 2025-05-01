import unittest

from src.ai_client import AIConversationClient
from src.ai_issue_integration import AIIssueIntegration
from src.issue_tracker import MemoryIssueTrackerClient
from tests.dummy_api_client import DummyAPIClient


class TestAIIssueIntegration(unittest.TestCase):
    """Test suite for AIIssueIntegration class using nose2."""

    def setUp(self) -> None:
        """Set up the integration components before each test."""
        ai_api_client = DummyAPIClient()
        self.ai_client = AIConversationClient(ai_api_client)
        self.issue_client = MemoryIssueTrackerClient()
        self.integration = AIIssueIntegration(self.ai_client, self.issue_client)
        self.session_id = self.integration.ai_client.start_new_session("test_user")

    def test_create_issue_command(self) -> None:
        """Test creating an issue through the integration."""
        message = "create issue with title: Test Issue, description: This is a test issue"
        response = self.integration.process_message(self.session_id, message)

        # Verify response contains confirmation
        self.assertIn("Issue created successfully", response["content"])

        # Verify issue was actually created
        issues = list(self.integration.issue_client.get_issues(filters={}))  # Fixed: added the required filters parameter
        self.assertEqual(len(issues), 1)
        self.assertEqual(issues[0].title, "Test Issue")
        self.assertEqual(issues[0].description, "This is a test issue")

    def test_list_issues_command(self) -> None:
        """Test listing issues through the integration."""
        # Create a couple of issues first
        self.issue_client.create_issue("Issue 1", "Description 1")
        self.issue_client.create_issue("Issue 2", "Description 2")

        # Test list issues command
        message = "list issues"
        response = self.integration.process_message(self.session_id, message)

        # Verify response contains both issues
        self.assertIn("Issue 1", response["content"])
        self.assertIn("Issue 2", response["content"])

    def test_regular_message_processing(self) -> None:
        """Test processing regular messages that don't contain commands."""
        message = "Hello, how are you today?"
        response = self.integration.process_message(self.session_id, message)

        # Verify the message was processed by the AI client
        self.assertIn("content", response)
        # No command should be executed for regular messages
        self.assertNotIn("Issue created successfully", response["content"])
        self.assertNotIn("Recent issues", response["content"])


if __name__ == "__main__":
    unittest.main()
