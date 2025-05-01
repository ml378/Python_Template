from typing import Any, Dict, Optional

from src import IssueTrackerClient, get_issue_tracker_client
from src.ai_client import AIConversationClient


class AIIssueIntegration:
    """Integration between AI conversation client and issue tracker."""

    def __init__(
        self,
        ai_client: AIConversationClient,
        issue_client: Optional[IssueTrackerClient] = None,
    ):
        """Initialize the integration with both clients.

        Args:
            ai_client: The AI conversation client
            issue_client: The issue tracker client (uses default if None)

        """
        self.ai_client = ai_client
        self.issue_client = issue_client or get_issue_tracker_client()
        self.commands = {
            "create_issue": self._parse_create_issue,
            "list_issues": self._parse_list_issues,
        }

    def process_message(self, session_id: str, message: str) -> Dict[str, Any]:
        """Process a user message and execute issue tracker commands if detected.

        Args:
            session_id: The conversation session ID
            message: The user's message

        Returns:
            The AI response, potentially including issue tracker operation results

        """
        # First, send message to AI client for processing
        response = self.ai_client.send_message(session_id, message)

        # Check if message contains issue creation commands
        command_result = self._process_commands(message)

        # If command was executed, append result to AI response
        if command_result:
            response["content"] += f"\n\n{command_result}"

        return response

    def _process_commands(self, message: str) -> Optional[str]:
        """Check if message contains issue tracker commands and process them.

        Args:
            message: The user message to check for commands

        Returns:
            Command result message or None if no command was detected

        """
        lower_message = message.lower()

        for command, handler in self.commands.items():
            if command in lower_message:
                return handler(message)

        return None

    def _parse_create_issue(self, message: str) -> str:
        """Parse message for issue creation parameters.

        Format expected: "create issue with title: X, description: Y"
        """
        # Extract title (basic parsing)
        title_parts = message.split("title:", 1)
        if len(title_parts) < 2:
            return "Could not parse issue title. Please specify 'title: your title'"

        title_desc = title_parts[1].split("description:", 1)
        title = title_desc[0].strip().strip(",")

        # Extract description if available
        description = (
            title_desc[1].strip() if len(title_desc) > 1 else "Created via AI assistant"
        )

        # Create the issue
        try:
            issue = self.issue_client.create_issue(
                title=title,
                description=description,
            )
            return f"✅ Issue created successfully with ID: {issue.id}\nTitle: {issue.title}"
        except Exception as e:
            return f"❌ Failed to create issue: {e!s}"

    def _parse_list_issues(self, _message: str) -> str:
        """List recent issues from the tracker."""
        try:
            issues = list(self.issue_client.get_issues())[:5]  # Get up to 5 issues
            if not issues:
                return "No issues found."

            result = "Recent issues:\n"
            for issue in issues:
                result += f"- [{issue.id}] {issue.title} ({issue.status})\n"
            return result
        except Exception as e:
            return f"❌ Failed to list issues: {e!s}"
