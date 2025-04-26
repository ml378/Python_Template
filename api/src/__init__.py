from __future__ import annotations
from typing import Any, Dict, Iterator, List, Optional, Protocol, runtime_checkable

@runtime_checkable
class Comment(Protocol):
    """A comment on an issue."""

    @property
    def id(self) -> str:
        """Return the id of the comment."""
        raise NotImplementedError

    @property
    def author(self) -> str:
        """Return the author of the comment."""
        raise NotImplementedError

    @property
    def content(self) -> str:
        """Return the content of the comment."""
        raise NotImplementedError

    @property
    def created_at(self) -> str:
        """Return the creation date of the comment."""
        raise NotImplementedError

@runtime_checkable
class Issue(Protocol):
    """An Issue in the issue tracker."""

    @property
    def id(self) -> str:
        """Return the id of the issue."""
        raise NotImplementedError

    @property
    def title(self) -> str:
        """Return the title of the issue."""
        raise NotImplementedError

    @property
    def description(self) -> str:
        """Return the description of the issue."""
        raise NotImplementedError

    @property
    def status(self) -> str:
        """Return the status of the issue (open, closed, etc.)."""
        raise NotImplementedError

    @property
    def creator(self) -> str:
        """Return the creator of the issue."""
        raise NotImplementedError

    @property
    def assignee(self) -> str | None:
        """Return the assignee of the issue, if any."""
        raise NotImplementedError

    @property
    def created_at(self) -> str:
        """Return the creation date of the issue."""
        raise NotImplementedError

    @property
    def updated_at(self) -> str:
        """Return the last update date of the issue."""
        raise NotImplementedError

    @property
    def labels(self) -> list[str]:
        """Return the labels associated with the issue."""
        raise NotImplementedError

    @property
    def priority(self) -> str | None:
        """Return the priority of the issue, if set."""
        raise NotImplementedError

    def get_comments(self) -> Iterator[Comment]:
        """Return an iterator of comments for this issue."""
        raise NotImplementedError

@runtime_checkable
class IssueTrackerClient(Protocol):
    """An Issue Tracker Client used to manage issues."""

    def get_issues(self, filters: dict[str, Any] | None) -> Iterator[Issue]:
        """Return an iterator of issues, optionally filtered."""
        raise NotImplementedError

    def get_issue(self, issue_id: str) -> Issue:
        """Return a specific issue by ID."""
        raise NotImplementedError

    def create_issue(self, title: str, description: str, **kwargs: any) -> Issue:
        """Create a new issue and return it."""
        raise NotImplementedError

    def update_issue(self, issue_id: str, **kwargs: any) -> Issue:
        """Update an existing issue and return the updated version."""
        raise NotImplementedError

    def add_comment(self, issue_id: str, content: str) -> Comment:
        """Add a comment to an issue and return the created comment."""
        raise NotImplementedError

    def search_issues(self, query: str) -> Iterator[Issue]:
        """Search for issues matching the query string."""
        raise NotImplementedError

def get_issue_tracker_client() -> IssueTrackerClient:
    """Return an instance of an Issue Tracker Client."""
    from api.src.issue_tracker import MemoryIssueTrackerClient
    return MemoryIssueTrackerClient()
