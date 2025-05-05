from __future__ import annotations

import json
import logging
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterator

from src import Comment, Issue, IssueTrackerClient

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


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

    def to_dict(self) -> dict[str, Any]:
        """Serialize comment to a dictionary."""
        return {
            "id": self._id,
            "author": self._author,
            "content": self._content,
            "created_at": self._created_at,
    }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> MemoryComment:
        """Deserialize comment from a dictionary."""
        # creates a new instance, id will match but object is new; override generated uuid
        comment = cls(author=data["author"], content=data["content"])
        comment._id = data["id"]
        comment._created_at = data["created_at"]
        return comment


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
        self._labels: list[str] = (
            [str(label) for label in labels_arg] if isinstance(labels_arg, list) else []
        )
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
            self._labels = (
                [str(label) for label in labels_arg]
                if isinstance(labels_arg, list)
                else self._labels
            )
        if "priority" in kwargs:
            self._priority = kwargs["priority"]

        self._updated_at = datetime.now(tz=timezone.utc).isoformat()

    def to_dict(self) -> dict[str, Any]:
        """Serialize issue and its comments to a dictionary."""
        return {
            "id": self._id,
            "title": self._title,
            "description": self._description,
            "status": self._status,
            "creator": self._creator,
            "assignee": self._assignee,
            "created_at": self._created_at,
            "updated_at": self._updated_at,
            "labels": self._labels,
            "priority": self._priority,
            "comments": [comment.to_dict() for comment in self._comments],
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> MemoryIssue:
        """Deserialize issue and its comments from a dictionary."""
        issue = cls(
            title=data["title"],
            description=data["description"],
            creator=data["creator"],
            status=data["status"],
            assignee=data["assignee"],
            labels=data["labels"],
            priority=data["priority"],
        )

        issue._id = data["id"]
        issue._created_at = data["created_at"]
        issue._updated_at = data["updated_at"]

        issue._comments = [MemoryComment.from_dict(c_data) for c_data in data["comments"]]
        return issue


class MemoryIssueTrackerClient(IssueTrackerClient):
    """An in-memory implementation of an Issue Tracker Client."""

    def __init__(self):
        # specify that this client works with MemoryIssue instances
        self._issues: dict[str, MemoryIssue] = {}
        self._current_user = (
            "default_user"
        )

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
                        assert isinstance(value, list)
                        if not any(label in issue.labels for label in value):
                            match = False
                            break
                    elif (key == "status" and getattr(issue, key) != value) or (
                        key == "assignee" and getattr(issue, key) != value
                    ):
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
        query = query.lower()

        matching_issues = [
            issue
            for issue in self._issues.values()
            if query in issue.title.lower() or query in issue.description.lower()
        ]

        return iter(matching_issues)

    def close_issue(self, issue_id: str, resolution: str) -> Issue:
        """Close an issue with a given resolution."""
        if issue_id not in self._issues:
            error_message = f"Issue with ID {issue_id} not found"
            raise ValueError(error_message)

        issue = self._issues[issue_id]
        issue.update(status="closed")
        self.add_comment(issue_id, f"Closed with resolution: {resolution}")
        return issue

    def get_current_user(self) -> str:
        return self._current_user


class FileIssueTrackerClient(IssueTrackerClient):
    """An Issue Tracker Client that persists issues to a JSON file."""

    def __init__(self, filepath: str = "data/issues.json"):
        self._filepath = filepath
        self._issues: dict[str, MemoryIssue] = {}
        self._current_user = "default_user"
        self._load_issues()

    def _ensure_data_dir_exists(self) -> None:
        """Create the data directory if it doesn't exist."""
        dir_path = Path(self._filepath).parent
        if not dir_path.exists():
            try:
                # Create the directory, including any necessary parents.
                # exist_ok=True prevents an error if the directory already exists (e.g., due to a race condition).
                dir_path.mkdir(parents=True, exist_ok=True)
                logger.info("Created data directory: %s", dir_path)
            except OSError:
                logger.exception("Failed to create data directory %s", dir_path)
                # log for now, potential raise later

    def _load_issues(self) -> None:
        """Load issues from the JSON file."""
        if not Path(self._filepath).exists():
            logger.warning("Data file not found: %s. Starting fresh.", self._filepath)
            self._issues = {}
            return

        try:
            with Path(self._filepath).open(encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, dict):
                     self._issues = {
                        issue_id: MemoryIssue.from_dict(issue_data)
                        for issue_id, issue_data in data.items()
                     }
                     logger.info(f"Loaded {len(self._issues)} issues from {self._filepath}")  # noqa: G004
                else:
                    logger.error(f"Invalid data format in {self._filepath}. Expected a dictionary. Starting fresh.")    # noqa: G004
                    self._issues = {}
        except json.JSONDecodeError:
            logger.exception(f"Failed to decode JSON from {self._filepath}. File might be corrupted. Starting fresh.")  # noqa: G004
            self._issues = {}
        except Exception:
             logger.exception(f"An unexpected error occurred while loading {self._filepath}. Starting fresh.")  # noqa: G004
             self._issues = {}


    def _save_issues(self) -> None:
        """Save the current state of issues to the JSON file."""
        try:
            data_to_save = {
                issue_id: issue.to_dict()
                for issue_id, issue in self._issues.items()
            }
            with Path(self._filepath).open("w", encoding="utf-8") as f:
                json.dump(data_to_save, f, indent=2)
            logger.debug(f"Saved {len(self._issues)} issues to {self._filepath}")   # noqa: G004
        except Exception:
            logger.exception(f"Failed to save issues to {self._filepath}")  # noqa: G004

    def set_current_user(self, username: str) -> None:
        """Set the current user for operations."""
        self._current_user = username

    def get_current_user(self) -> str:
        return self._current_user

    def get_issues(self, filters: dict[str, Any] | None = None) -> Iterator[Issue]:
        """Return an iterator of issues, optionally filtered."""
        issues = self._issues.values()
        if filters:
            filtered_issues = []
            for issue in issues:
                match = True
                for key, value in filters.items():
                    attr_value = getattr(issue, key, None)
                    if key == "labels" and isinstance(value, list):
                        issue_labels = getattr(issue, "labels", [])
                        if not isinstance(issue_labels, list) or not any(label in issue_labels for label in value):
                            match = False
                            break
                    elif attr_value != value:
                         match = False
                         break
                if match:
                    filtered_issues.append(issue)
            return iter(filtered_issues)
        return iter(issues)


    def get_issue_dict(self) -> dict[str, MemoryIssue]:
        """Return all issues as a dictionary."""
        # optimistically assumes in-memory is up to date
        return self._issues.copy()

    def get_issue(self, issue_id: str) -> Issue:
        """Return a specific issue by ID."""
        if issue_id not in self._issues:
            error_message = f"Issue with ID {issue_id} not found"
            raise ValueError(error_message)
        return self._issues[issue_id]

    def create_issue(self, title: str, description: str, **kwargs: Any) -> Issue:  # noqa: ANN401
        """Create a new issue, save it, and return it."""
        issue = MemoryIssue(title, description, self._current_user, **kwargs)
        self._issues[issue.id] = issue
        self._save_issues()
        return issue

    def update_issue(self, issue_id: str, **kwargs: Any) -> Issue:  # noqa: ANN401
        """Update an existing issue, save it, and return the updated version."""
        issue = self.get_issue(issue_id)
        if not isinstance(issue, MemoryIssue):
            msg = "Issue found is not an updatable MemoryIssue instance"
            raise TypeError(msg)
        issue.update(**kwargs)
        self._save_issues()
        return issue

    def add_comment(self, issue_id: str, content: str) -> Comment:
        """Add a comment to an issue, save it, and return the created comment."""
        issue = self.get_issue(issue_id)
        if not isinstance(issue, MemoryIssue):
             msg = "Issue found is not a MemoryIssue instance that can accept comments"
             raise TypeError(msg)

        comment = MemoryComment(self._current_user, content)
        issue.add_comment(comment)
        self._save_issues()
        return comment

    def search_issues(self, query: str) -> Iterator[Issue]:
        """Search for issues matching the query string."""
        query = query.lower()
        matching_issues = [
            issue
            for issue in self._issues.values()
            if query in issue.title.lower() or query in issue.description.lower()
        ]
        return iter(matching_issues)


    def close_issue(self, issue_id: str, resolution: str) -> Issue:
        """Close an issue with a given resolution and save."""
        issue = self.get_issue(issue_id)
        if not isinstance(issue, MemoryIssue):
            msg = "Issue found is not an updatable MemoryIssue instance"
            raise TypeError(msg)

        issue.update(status="closed")
        self.add_comment(issue_id, f"Closed with resolution: {resolution}")
        return issue
