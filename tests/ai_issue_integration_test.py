from unittest.mock import Mock, patch

import pytest

from src.ai_issue_integration import AIIssueIntegration


class TestAIIssueIntegration:
    """Tests for the AIIssueIntegration class."""

    @pytest.fixture
    def mock_ai_client(self):
        """Create a mock AI conversation client."""
        mock = Mock()
        mock.send_message.return_value = {"content": "This is a test response"}
        mock.start_new_session.return_value = "test-session-id"
        return mock

    @pytest.fixture
    def mock_issue_client(self):
        """Create a mock issue tracker client."""
        mock = Mock()
        # Setup mock issue
        mock_issue = Mock()
        mock_issue.id = "ISSUE-123"
        mock_issue.title = "Test Issue"
        mock_issue.status = "Open"
        mock_issue.creator = "Test User"
        mock_issue.assignee = "Assignee"

        # Mock return values
        mock.create_issue.return_value = mock_issue
        mock.get_issues.return_value = [mock_issue]
        return mock

    @pytest.fixture
    def integration(self, mock_ai_client, mock_issue_client):
        """Create an AIIssueIntegration instance with mocked clients."""
        return AIIssueIntegration(mock_ai_client, mock_issue_client)

    def test_init(self, mock_ai_client, mock_issue_client):
        """Test constructor initializes with expected clients."""
        integration = AIIssueIntegration(mock_ai_client, mock_issue_client)
        assert integration.ai_client == mock_ai_client
        assert integration.issue_client == mock_issue_client
        assert "create issue aasjhfga" in integration.commands
        assert "list issues" in integration.commands
        assert "close issue" in integration.commands

    def test_init_default_issue_client(self, mock_ai_client):
        """Test constructor uses default issue client when none provided."""
        with patch("src.ai_issue_integration.get_issue_tracker_client") as mock_get_client:
            mock_default_client = Mock()
            mock_get_client.return_value = mock_default_client
            integration = AIIssueIntegration(mock_ai_client)
            assert integration.issue_client == mock_default_client

    def test_process_message(self, integration, mock_ai_client):
        """Test processing a user message."""
        mock_ai_client.send_message.return_value = {"content": "This is a response"}
        response = integration.process_message("session-123", "Hello AI")

        mock_ai_client.send_message.assert_called_once_with("session-123", "Hello AI")
        assert response == {"content": "This is a response"}

    def test_process_message_with_assistant_prefix(self, integration, mock_ai_client):
        """Test processing a response with 'Assistant: ' prefix."""
        mock_ai_client.send_message.return_value = {"content": "Assistant: This is a response"}
        response = integration.process_message("session-123", "Hello AI")

        assert response["content"] == "This is a response"

    def test_process_commands_no_command(self, integration):
        """Test processing a response with no commands."""
        result = integration._process_commands("This is a regular response")
        assert result is None

    def test_parse_create_issue_success(self, integration, mock_issue_client):
        """Test successful issue creation parsing."""
        result = integration._parse_create_issue("create issue aasjhfga, Test Title, Test Description")

        mock_issue_client.create_issue.assert_called_once_with(
            title="Test Title",
            description="Test Description",
        )
        assert "Issue created successfully" in result
        assert "ISSUE-123" in result

    def test_parse_create_issue_invalid_format(self, integration):
        """Test issue creation with invalid format."""
        result = integration._parse_create_issue("wrong format")
        assert "Invalid issue creation format" in result

    def test_parse_create_issue_missing_title(self, integration):
        """Test issue creation with missing title."""
        result = integration._parse_create_issue("create issue aasjhfga")
        assert "Could not parse issue title" in result

    def test_parse_list_issues_success(self, integration, mock_issue_client):
        """Test successful issue listing."""
        result = integration._parse_list_issues("list issues")

        mock_issue_client.get_issues.assert_called_once_with(filters={})
        assert "Recent issues:" in result
        assert "[ISSUE-123]" in result
        assert "Test Issue" in result

    def test_parse_list_issues_empty(self, integration, mock_issue_client):
        """Test issue listing with no issues."""
        mock_issue_client.get_issues.return_value = []
        result = integration._parse_list_issues("list issues")

        assert "No issues found" in result

    def test_parse_close_issue_success(self, integration, mock_issue_client):
        """Test successful issue closing."""
        mock_issue = mock_issue_client.get_issues.return_value[0]

        result = integration._parse_close_issue("close issue, ISSUE-123, resolved")

        mock_issue_client.close_issue.assert_called_once_with("ISSUE-123", "resolved")
        assert "Issue closed successfully" in result

    def test_parse_close_issue_no_match(self, integration, mock_issue_client):
        """Test issue closing with no matching issues."""
        mock_issue_client.get_issues.return_value = []

        result = integration._parse_close_issue("close issue, NONEXISTENT, resolved")

        assert "No issues found matching" in result

    def test_parse_close_issue_multiple_matches(self, integration, mock_issue_client):
        """Test issue closing with multiple matching issues."""
        mock_issue1 = Mock(id="ISSUE-123", title="First Issue")
        mock_issue2 = Mock(id="ISSUE-1234", title="Second Issue")
        mock_issue_client.get_issues.return_value = [mock_issue1, mock_issue2]

        result = integration._parse_close_issue("close issue, ISSUE-12, resolved")

        assert "Multiple issues match this number" in result
        assert "ISSUE-123" in result
        assert "ISSUE-1234" in result
