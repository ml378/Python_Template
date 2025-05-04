from __future__ import annotations

import logging

from typing import TYPE_CHECKING, Any, Dict, Callable

from src import IssueTrackerClient, get_issue_tracker_client

if TYPE_CHECKING:
    from src.ai_client import AIConversationClient

# todo: replace generic RunTimeError catches
class AIIssueIntegration:
    """Integration between AI conversation client and issue tracker."""

    def __init__(
        self,
        ai_client: AIConversationClient,
        issue_client: IssueTrackerClient | None = None,
    ):
        """Initialize the integration with both clients.

        Args:
            ai_client: The AI conversation client
            issue_client: The issue tracker client (uses default if None)

        """
        self.ai_client = ai_client
        self.issue_client = issue_client or get_issue_tracker_client()
        self.commands = {
            "create issue": self._parse_create_issue,
            "list issues": self._parse_list_issues,
        }

    def process_message(self, session_id: str, message: str) -> dict[str, Any]:
        """Process a user message and execute issue tracker commands if detected.

        Args:
            session_id: The conversation session ID
            message: The user's message

        Returns:
            The AI response, potentially including issue tracker operation results

        """
        response = self.ai_client.send_message(session_id, message)

        command_result = self._process_commands(message)

        if command_result:
            response["content"] += f"\n\n{command_result}"

        return response

    def _process_commands(self, message: str) -> str | None:
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
        try:
            lower_message = message.lower()
            if "title:" not in lower_message:
                 return "Could not parse issue title. Please specify 'title: your title'"

            title_start_index = lower_message.find("title:") + len("title:")
            title_part = message[title_start_index:] 

            desc_marker = "description:"
            desc_start_index = title_part.lower().find(desc_marker)

            if desc_start_index != -1:
                title = title_part[:desc_start_index].strip().rstrip(',') 
                description = title_part[desc_start_index + len(desc_marker):].strip()
            else:
                title = title_part.strip().rstrip(',')
                description = "Created via AI assistant" 

            if not title: 
                 return "Could not parse issue title. Title appears to be empty."

            issue = self.issue_client.create_issue(
                title=title,
                description=description,
            )
            return f"Issue created successfully with ID: {issue.id}\nTitle: {issue.title}"

        except Exception as e:
            logging.error(f"Error creating issue via AI: {e!s}", exc_info=True)
            return f"Failed to create issue: {e!s}"

    def _parse_list_issues(self, _message: str) -> str:
        """List recent issues from the tracker."""
        result = ""
        try:
            issues = list(self.issue_client.get_issues(filters={}))[:5] 
            if not issues:
                return "No issues found."

            result = "Recent issues:\n"
            for issue in issues:
                result += f"- [{issue.id}] {issue.title} ({issue.status})\n"
        except RuntimeError as e:  
            logging.error(f"Error listing issues: {e!s}", exc_info=True)
            return f"Failed to list issues: {e!s}"
        else:
            return result.strip()
