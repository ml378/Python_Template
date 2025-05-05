from __future__ import annotations

import argparse
import asyncio
import logging
import sys
from typing import TYPE_CHECKING, Any

from src import IssueTrackerClient, get_issue_tracker_client

if TYPE_CHECKING:
    from src.ai_client import AIConversationClient

# TODO: replace generic RunTimeError catches
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
            "create issue aasjhfga": self._parse_create_issue,
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


        # Parse AI's response for commands instead of user message
        if "content" in response:
            print("AI response received: %s", response["content"])
            command_result = self._process_commands(response["content"])
            if command_result:
                # Replace AI's response with just the command result
                response["content"] = command_result

        return response

    def _process_commands(self, ai_response: str) -> str | None:
        """Check if AI response contains issue tracker commands and process them.

        Args:
            ai_response: The AI response to check for commands

        Returns:
            Command result message or None if no command was detected

        """
        lower_response = ai_response.lower()

        for command, handler in self.commands.items():
            if command in lower_response:
                return handler(ai_response)

        return None

    def _parse_create_issue(self, response: str) -> str:
        """Parse AI response for issue creation parameters.

        Format expected: 'create issue, title, description, creator, assignee, priority'
        """
        try:
            # Split the response by commas and strip whitespace
            parts = [part.strip() for part in response.split(',')]
            
            # Verify the first part starts with "create issue"
            if not parts[0].lower().startswith("create issue aasjhfga"):
                return "Invalid issue creation format. Expected format: 'create issue, title, description, ...'"
            
            # Extract title (required field)
            if len(parts) < 2 or not parts[1]:
                return "Could not parse issue title. Please provide a title after 'create issue'"
            
            title = parts[1]
            
            # Extract description (optional field)
            description = parts[2] if len(parts) > 2 and parts[2] else "Created via AI assistant"
            
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
    
    def _parse_list_issues(self, _response: str) -> str:
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


async def interactive_issue_chat(integration: AIIssueIntegration, user_id: str) -> None:
    """Start an interactive chat loop with issue integration capabilities.

    Args:
        integration: The AI issue integration instance
        user_id: Unique identifier for the user

    """
    session_id = integration.ai_client.start_new_session(user_id)

    # Send initial context-setting message
    system_message = f"""
        In this session, You are in charge of interfacing with a issue tracker tool. 
        Never include words such as "Assistant: " or "AI: " at the beginning of your responses.
        If you are uncertain about the user's intention, ask for clarification.
        The user's name is: {user_id}. Please use this name as the creator when creating issues, and feel free to use it in your responses.
        If the user ask you to create a issue, respond the with following information the use provided in a CSV-like format in a single line, without any quotation for formating: 
        The first item should be "create issue aasjhfga" and the rest should be the information for the following fields:
        title, description, creator, assignee, priority
        and do not include any other text in the response.
        Priority should be a number between 1 and 5, where 1 is the highest priority and 5 is the lowest.
        Please parse the above data from the user's request. If the user did not provide one of those data, it is fine to leave the field empty.
        If the user asks to list the issues or what issues are available, respond with "list issues" and nothing else.
    """

    # Send system message but don't show response to user
    integration.ai_client.send_message(session_id, f"SYSTEM: {system_message.strip()}")

    print(f"Issue-enabled chat session started (ID: {session_id}). Type 'exit' or 'quit' to end.")
    print("You can ask the AI to:")
    print("  - create a issue with infomration such as title, description, creator, assignee, and priority on a scale of 1-5")
    print("  - list issues")
    print("Feel free to use natural language to interact with the AI! Your commands will be processed automatically.")

    loop = asyncio.get_event_loop()

    while True:
        try:
            user_input = await loop.run_in_executor(None, input, "You: ")
            user_input = user_input.strip()

            if user_input.lower() in {"exit", "quit"}:
                integration.ai_client.end_session(session_id)
                print("Session ended.")
                break

            if not user_input:
                continue

            # Process message through the integration
            ai_response = integration.process_message(session_id, user_input)

            # Print AI response if available
            if ai_response and "content" in ai_response:
                print(f"AI: {ai_response['content']}")

        except EOFError:  # Handle Ctrl+D
            integration.ai_client.end_session(session_id)
            print("\nSession ended.")
            break
        except KeyboardInterrupt:  # Handle Ctrl+C
            integration.ai_client.end_session(session_id)
            print("\nSession interrupted and ended.")
            break
        except Exception as e:
            print(f"An error occurred: {e}")


async def run_cli() -> None:
    """Parse command-line arguments and start the issue integration CLI."""
    parser = argparse.ArgumentParser(description="AI Issue Integration CLI")
    parser.add_argument("--user-id", default="default_user", help="User ID for the session")

    args = parser.parse_args()
    
    # If using default user_id, ask for user's name
    if args.user_id == "default_user":
        try:
            user_name = input("Please enter your name: ").strip()
            if user_name:
                args.user_id = user_name
            else:
                print("Using default user ID as no name was provided.")
        except (EOFError, KeyboardInterrupt):
            print("\nExiting application.")
            return

    # Import here to avoid circular imports
    from src.ai_client import AIConversationClient
    from src.gemini_api_client import GeminiAPIClient

    # Create the API client without a system prompt
    api_client = GeminiAPIClient()
    ai_client = AIConversationClient(api_client)

    # Create the integration
    integration = AIIssueIntegration(ai_client)

    # Start interactive chat (system prompt will be sent as first message)
    await interactive_issue_chat(integration, args.user_id)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(run_cli())
    except Exception as e:
        print(f"Fatal error: {e}")
        sys.exit(1)
