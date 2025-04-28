import pytest

from ai_conversation_client.src.client import AIConversationClient
from api.src.issue_tracker import MemoryIssueTrackerClient
from src.ai_issue_integration import AIIssueIntegration
from tests.dummy_api_client import DummyAPIClient


@pytest.fixture
def integration():
    ai_api_client = DummyAPIClient()
    ai_client = AIConversationClient(ai_api_client)
    issue_client = MemoryIssueTrackerClient()
    return AIIssueIntegration(ai_client, issue_client)


def test_create_issue_command(integration):
    # Start a session
    session_id = integration.ai_client.start_new_session("test_user")

    # Test issue creation command
    message = "create issue with title: Test Issue, description: This is a test issue"
    response = integration.process_message(session_id, message)

    # Verify response contains confirmation
    assert "Issue created successfully" in response["content"]

    # Verify issue was actually created
    issues = list(integration.issue_client.get_issues())
    assert len(issues) == 1
    assert issues[0].title == "Test Issue"
    assert issues[0].description == "This is a test issue"


def test_list_issues_command(integration):
    # Start a session
    session_id = integration.ai_client.start_new_session("test_user")

    # Create a couple of issues first
    integration.issue_client.create_issue("Issue 1", "Description 1")
    integration.issue_client.create_issue("Issue 2", "Description 2")

    # Test list issues command
    message = "list issues"
    response = integration.process_message(session_id, message)

    # Verify response contains both issues
    assert "Issue 1" in response["content"]
    assert "Issue 2" in response["content"]
