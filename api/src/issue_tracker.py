from __future__ import annotations

import uuid
from datetime import datetime, timezone
from typing import Any, Iterator

from external.issue_tracker.api.src import Comment, Issue, IssueTrackerClient


class MemoryComment(Comment):
    """An in-memory implementation of a Comment."""

    def __init__(self, author: str, content: str):
        self._id = str(uuid.uuid4())
        self._author = author
        self._content = content
        self._created_at = datetime.now(tz=timezone.utc).isoformat()

    @property
    def id(self) -> str:
        return self._id

    @property
    def author(self) -> str:
        return self._author

    @property
    def content(self) -> str:
        return self._content

    @property
    def created_at(self) -> str:
        return self._created_at


class MemoryIssue(Issue):
    """An in-memory implementation of an Issue."""

    def __init__(self, title: str, description: str, creator: str, **kwargs: Any):  # noqa: ANN401
        self._id = str(uuid.uuid4())
        self._title = title
        self._description = description
        self._status = str(kwargs.get("status", "open"))
        self._creator = creator
        self._assignee = kwargs.get("assignee")
        self._created_at = datetime.now(tz=timezone.utc).isoformat()
        self._updated_at = self._created_at
        labels_arg = kwargs.get("labels", [])
        self._labels: list[str] = [str(label) for label in labels_arg] if isinstance(labels_arg, list) else []
        self._priority = kwargs.get("priority")
        self._comments: list[MemoryComment] = []

    @property
    def id(self) -> str:
        return self._id

    @property
    def title(self) -> str:
        return self._title

    @property
    def description(self) -> str:
        return self._description

    @property
    def status(self) -> str:
        return self._status

    @property
    def creator(self) -> str:
        return self._creator

    @property
    def assignee(self) -> str | None:
        return self._assignee

    @property
    def created_at(self) -> str:
        return self._created_at

    @property
    def updated_at(self) -> str:
        return self._updated_at

    @property
    def labels(self) -> list[str]:
        return self._labels

    @property
    def priority(self) -> str | None:
        return self._priority

    def get_comments(self) -> Iterator[Comment]:
        return iter(self._comments)

    def add_comment(self, comment: MemoryComment) -> None:
        self._comments.append(comment)
        self._updated_at = datetime.now(tz=timezone.utc).isoformat()

    def update(self, **kwargs: Any) -> None:  # noqa: ANN401
        """Update issue attributes."""
        if "title" in kwargs:
            self._title = kwargs["title"]
        if "description" in kwargs:
            self._description = kwargs["description"]
        if "status" in kwargs:
            self._status = kwargs["status"]
        if "assignee" in kwargs:
            self._assignee = kwargs["assignee"]
        if "labels" in kwargs:
            labels_arg = kwargs["labels"]
            self._labels = [str(label) for label in labels_arg] if isinstance(labels_arg, list) else self._labels
        if "priority" in kwargs:
            self._priority = kwargs["priority"]

        self._updated_at = datetime.now(tz=timezone.utc).isoformat()

class MemoryIssueTrackerClient(IssueTrackerClient):
    """An in-memory implementation of an Issue Tracker Client."""

    def __init__(self):
        # Specify that this client works with MemoryIssue instances
        self._issues: dict[str, MemoryIssue] = {}
        self._current_user = "default_user"  # In a real system, this would come from auth

    def set_current_user(self, username: str) -> None:
        """Set the current user for operations."""
        self._current_user = username

    def get_issues(self, filters: dict[str, Any] | None = None) -> Iterator[Issue]:
        """Return an iterator of issues, optionally filtered."""
        issues = self._issues.values()

        if filters:
            filtered_issues = []
            for issue in issues:
                match = True
                for key, value in filters.items():
                    if key == "labels" and isinstance(value, list):
                        # Add assertion to help the type checker
                        assert isinstance(value, list)
                        # Check if any of the requested labels are in the issue's labels
                        if not any(label in issue.labels for label in value):
                            match = False
                            break
                    elif (key == "status" and getattr(issue, key) != value) or (key == "assignee" and getattr(issue, key) != value):
                        match = False
                        break
                if match:
                    filtered_issues.append(issue)
            return iter(filtered_issues)

        return iter(issues)

    def get_issue_dict(self) -> dict[str, MemoryIssue]:
        """Return all issues as a dictionary."""
        return self._issues

    def get_issue(self, issue_id: str) -> Issue:
        """Return a specific issue by ID."""
        if issue_id not in self._issues:
            error_message = f"Issue with ID {issue_id} not found"
            raise ValueError(error_message)
        return self._issues[issue_id]

    def create_issue(self, title: str, description: str, **kwargs: Any) -> Issue:  # noqa: ANN401
        """Create a new issue and return it."""
        issue = MemoryIssue(title, description, self._current_user, **kwargs)
        self._issues[issue.id] = issue
        return issue

    def update_issue(self, issue_id: str, **kwargs: Any) -> MemoryIssue:  # noqa: ANN401
        """Update an existing issue and return the updated version."""
        if issue_id not in self._issues:
            error_message = f"Issue with ID {issue_id} not found"
            raise ValueError(error_message)

        issue = self._issues[issue_id]
        issue.update(**kwargs)
        return issue

    def add_comment(self, issue_id: str, content: str) -> Comment:
        """Add a comment to an issue and return the created comment."""
        if issue_id not in self._issues:
            error_message = f"Issue with ID {issue_id} not found"
            raise ValueError(error_message)

        issue = self._issues[issue_id]
        comment = MemoryComment(self._current_user, content)
        issue.add_comment(comment)
        return comment

    def search_issues(self, query: str) -> Iterator[MemoryIssue]:
        """Search for issues matching the query string."""
        # Simple case-insensitive search in title and description
        query = query.lower()

        matching_issues = [
            issue for issue in self._issues.values()
            if query in issue.title.lower() or query in issue.description.lower()
        ]

        return iter(matching_issues)

    def get_current_user(self) -> str:
        return self._current_user
