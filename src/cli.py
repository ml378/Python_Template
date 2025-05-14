#!/usr/bin/env python3
"""Command-line interface for the issue tracker application.
Provides commands to interact with the issue tracking system.
"""
import argparse
import sys

from src.json_storage import JsonIssueTrackerClient
from src.mock_implementation import MockIssueTrackerClient


def main():
    """Entry point for the issue tracker CLI application.
    
    Parses command line arguments and executes the appropriate actions.
    
    Returns:
        int: Exit code (0 for success, non-zero for errors)

    """
    parser = argparse.ArgumentParser(description="Issue Tracker CLI")
    parser.add_argument("--storage", choices=["mock", "json"], default="json",
                        help="Storage backend to use (default: json)")
    parser.add_argument("--storage-path", help="Path to JSON storage file (only for json storage)")

    # Add subparsers for different commands
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")

    # Create issue command
    create_parser = subparsers.add_parser("create", help="Create a new issue")
    create_parser.add_argument("title", help="Issue title")
    create_parser.add_argument("description", help="Issue description")
    create_parser.add_argument("--status", default="open", help="Issue status")

    # List issues command
    list_parser = subparsers.add_parser("list", help="List all issues")
    list_parser.add_argument("--status", help="Filter issues by status")

    # Get issue command
    get_parser = subparsers.add_parser("get", help="Get issue details")
    get_parser.add_argument("id", help="Issue ID")

    # Update issue command
    update_parser = subparsers.add_parser("update", help="Update an issue")
    update_parser.add_argument("id", help="Issue ID")
    update_parser.add_argument("--title", help="New issue title")
    update_parser.add_argument("--description", help="New issue description")
    update_parser.add_argument("--status", help="New issue status")

    # Delete issue command
    delete_parser = subparsers.add_parser("delete", help="Delete an issue")
    delete_parser.add_argument("id", help="Issue ID")

    args = parser.parse_args()

    # Initialize the appropriate client
    if args.storage == "mock":
        client = MockIssueTrackerClient()
    else:  # json storage
        client = JsonIssueTrackerClient(args.storage_path)

    # Execute the command
    if args.command == "create":
        issue = client.create_issue(args.title, args.description, status=args.status)
        print(f"Issue created with ID: {issue['id']}")
        print(f"Title: {issue['title']}")
        print(f"Status: {issue['status']}")

    elif args.command == "list":
        issues = client.list_issues(args.status)
        if not issues:
            print("No issues found.")
        else:
            for issue in issues:
                print(f"ID: {issue['id']}")
                print(f"Title: {issue['title']}")
                print(f"Status: {issue['status']}")
                print("-" * 30)

    elif args.command == "get":
        issue = client.get_issue(args.id)
        if not issue:
            print(f"Issue with ID {args.id} not found.")
            return 1
        print(f"ID: {issue['id']}")
        print(f"Title: {issue['title']}")
        print(f"Description: {issue['description']}")
        print(f"Status: {issue['status']}")
        print(f"Created: {issue['created_at']}")
        print(f"Updated: {issue['updated_at']}")

    elif args.command == "update":
        update_data = {}
        if args.title:
            update_data["title"] = args.title
        if args.description:
            update_data["description"] = args.description
        if args.status:
            update_data["status"] = args.status

        if not update_data:
            print("No update data provided.")
            return 1

        issue = client.update_issue(args.id, **update_data)
        if not issue:
            print(f"Issue with ID {args.id} not found.")
            return 1
        print(f"Issue {args.id} updated successfully.")

    elif args.command == "delete":
        success = client.delete_issue(args.id)
        if not success:
            print(f"Issue with ID {args.id} not found.")
            return 1
        print(f"Issue {args.id} deleted successfully.")

    else:
        parser.print_help()

    return 0


if __name__ == "__main__":
    sys.exit(main())
