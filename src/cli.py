#!/usr/bin/env python3
"""
CLI front-end for the issue tracker.
"""
import argparse
import sys
from typing import Any, Dict, List, Optional

from src.mock_implementation import MockIssueTrackerClient


class IssueTrackerCLI:
    """Command-line interface for the issue tracker."""

    def __init__(self):
        self.client = MockIssueTrackerClient()
        self.parser = self._create_parser()

    def _create_parser(self) -> argparse.ArgumentParser:
        """Create the command-line argument parser."""
        parser = argparse.ArgumentParser(description="Issue Tracker CLI")
        subparsers = parser.add_subparsers(dest="command", help="Command to run")

        # List issues command
        list_parser = subparsers.add_parser("list", help="List all issues")
        list_parser.add_argument("--status", help="Filter by status")
        list_parser.add_argument("--assignee", help="Filter by assignee")

        # Get issue command
        get_parser = subparsers.add_parser("get", help="Get an issue by ID")
        get_parser.add_argument("issue_id", help="ID of the issue to get")
        get_parser.add_argument("--comments", action="store_true", help="Show comments")

        # Create issue command
        create_parser = subparsers.add_parser("create", help="Create a new issue")
        create_parser.add_argument("title", help="Issue title")
        create_parser.add_argument("description", help="Issue description")
        create_parser.add_argument("--status", default="open", help="Issue status")
        create_parser.add_argument("--assignee", help="Issue assignee")
        create_parser.add_argument("--priority", help="Issue priority")

        # Update issue command
        update_parser = subparsers.add_parser("update", help="Update an existing issue")
        update_parser.add_argument("issue_id", help="ID of the issue to update")
        update_parser.add_argument("--title", help="New issue title")
        update_parser.add_argument("--description", help="New issue description")
        update_parser.add_argument("--status", help="New issue status")
        update_parser.add_argument("--assignee", help="New issue assignee")
        update_parser.add_argument("--priority", help="New issue priority")

        # Add comment command
        comment_parser = subparsers.add_parser("comment", help="Add a comment to an issue")
        comment_parser.add_argument("issue_id", help="ID of the issue to comment on")
        comment_parser.add_argument("content", help="Comment content")

        # Search command
        search_parser = subparsers.add_parser("search", help="Search for issues")
        search_parser.add_argument("query", help="Search query")

        return parser

    def run(self, args: Optional[List[str]] = None) -> None:
        """Run the CLI with the given arguments."""
        parsed_args = self.parser.parse_args(args)
        if not parsed_args.command:
            self.parser.print_help()
            return

        command_method = getattr(self, f"cmd_{parsed_args.command}", None)
        if command_method:
            command_method(parsed_args)
        else:
            print(f"Unknown command: {parsed_args.command}")

    def cmd_list(self, args: argparse.Namespace) -> None:
        """List issues command handler."""
        filters: Dict[str, Any] = {}
        if args.status:
            filters["status"] = args.status
        if args.assignee:
            filters["assignee"] = args.assignee

        print("Issues:")
        for issue in self.client.get_issues(filters=filters if filters else None):
            print(f"  {issue.id}: {issue.title} [{issue.status}] - Assigned to: {issue.assignee or 'None'}")

    def cmd_get(self, args: argparse.Namespace) -> None:
        """Get issue command handler."""
        issue = self.client.get_issue(args.issue_id)
        print(f"ID: {issue.id}")
        print(f"Title: {issue.title}")
        print(f"Description: {issue.description}")
        print(f"Status: {issue.status}")
        print(f"Creator: {issue.creator}")
        print(f"Assignee: {issue.assignee or 'None'}")
        print(f"Created: {issue.created_at}")
        print(f"Updated: {issue.updated_at}")
        print(f"Priority: {issue.priority or 'None'}")
        print(f"Labels: {', '.join(issue.labels)}")
        
        if args.comments:
            print("\nComments:")
            for comment in issue.get_comments():
                print(f"  [{comment.author} on {comment.created_at}]")
                print(f"  {comment.content}")
                print()

    def cmd_create(self, args: argparse.Namespace) -> None:
        """Create issue command handler."""
        kwargs = {}
        if args.status:
            kwargs["status"] = args.status
        if args.assignee:
            kwargs["assignee"] = args.assignee
        if args.priority:
            kwargs["priority"] = args.priority

        issue = self.client.create_issue(args.title, args.description, **kwargs)
        print(f"Created issue {issue.id}: {issue.title}")

    def cmd_update(self, args: argparse.Namespace) -> None:
        """Update issue command handler."""
        kwargs = {}
        if args.title:
            kwargs["title"] = args.title
        if args.description:
            kwargs["description"] = args.description
        if args.status:
            kwargs["status"] = args.status
        if args.assignee:
            kwargs["assignee"] = args.assignee
        if args.priority:
            kwargs["priority"] = args.priority

        if not kwargs:
            print("No updates specified")
            return

        issue = self.client.update_issue(args.issue_id, **kwargs)
        print(f"Updated issue {issue.id}: {issue.title}")

    def cmd_comment(self, args: argparse.Namespace) -> None:
        """Add comment command handler."""
        comment = self.client.add_comment(args.issue_id, args.content)
        print(f"Added comment to issue {args.issue_id}: {comment.content[:30]}...")

    def cmd_search(self, args: argparse.Namespace) -> None:
        """Search issues command handler."""
        print(f"Search results for '{args.query}':")
        for issue in self.client.search_issues(args.query):
            print(f"  {issue.id}: {issue.title} [{issue.status}]")


def main() -> None:
    """Main entry point for the CLI."""
    cli = IssueTrackerCLI()
    cli.run(sys.argv[1:])


if __name__ == "__main__":
    main()
