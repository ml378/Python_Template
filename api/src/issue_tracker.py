import uuid
from datetime import datetime
from typing import Any, Dict, Iterator, List, Optional

from api.src import Comment, Issue, IssueTrackerClient


class MemoryComment(Comment):
    """An in-memory implementation of a Comment."""
    
    def __init__(self, author: str, content: str):
        self._id = str(uuid.uuid4())
        self._author = author
        self._content = content
        self._created_at = datetime.now().isoformat()
    
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
    
    def __init__(self, title: str, description: str, creator: str, **kwargs):
        self._id = str(uuid.uuid4())
        self._title = title
        self._description = description
        self._status = kwargs.get("status", "open")
        self._creator = creator
        self._assignee = kwargs.get("assignee")
        self._created_at = datetime.now().isoformat()
        self._updated_at = self._created_at
        self._labels = kwargs.get("labels", [])
        self._priority = kwargs.get("priority")
        self._comments: List[MemoryComment] = []
    
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
    def assignee(self) -> Optional[str]:
        return self._assignee
    
    @property
    def created_at(self) -> str:
        return self._created_at
    
    @property
    def updated_at(self) -> str:
        return self._updated_at
    
    @property
    def labels(self) -> List[str]:
        return self._labels
    
    @property
    def priority(self) -> Optional[str]:
        return self._priority
    
    def get_comments(self) -> Iterator[Comment]:
        return iter(self._comments)
    
    def add_comment(self, comment: MemoryComment) -> None:
        self._comments.append(comment)
        self._updated_at = datetime.now().isoformat()
    
    def update(self, **kwargs) -> None:
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
            self._labels = kwargs["labels"]
        if "priority" in kwargs:
            self._priority = kwargs["priority"]
        
        self._updated_at = datetime.now().isoformat()


class MemoryIssueTrackerClient(IssueTrackerClient):
    """An in-memory implementation of an Issue Tracker Client."""
    
    def __init__(self):
        self._issues: Dict[str, MemoryIssue] = {}
        self._current_user = "default_user"  # In a real system, this would come from auth
    
    def set_current_user(self, username: str) -> None:
        """Set the current user for operations."""
        self._current_user = username
    
    def get_issues(self, filters: Optional[Dict[str, Any]] = None) -> Iterator[Issue]:
        """Return an iterator of issues, optionally filtered."""
        issues = self._issues.values()
    
        if filters:
            filtered_issues = []
            for issue in issues:
                match = True
                for key, value in filters.items():
                    if key == "labels" and isinstance(value, list):
                        # Check if any of the requested labels are in the issue's labels
                        if not any(label in issue.labels for label in value):
                            match = False
                            break
                    elif key == "status" and getattr(issue, key) != value:
                        match = False
                        break
                    elif key == "assignee" and getattr(issue, key) != value:
                        match = False
                        break
                if match:
                    filtered_issues.append(issue)
            return iter(filtered_issues)
        
        return iter(issues)
    
    def get_issue(self, issue_id: str) -> Issue:
        """Return a specific issue by ID."""
        if issue_id not in self._issues:
            raise ValueError(f"Issue with ID {issue_id} not found")
        return self._issues[issue_id]
    
    def create_issue(self, title: str, description: str, **kwargs) -> Issue:
        """Create a new issue and return it."""
        issue = MemoryIssue(title, description, self._current_user, **kwargs)
        self._issues[issue.id] = issue
        return issue
    
    def update_issue(self, issue_id: str, **kwargs) -> Issue:
        """Update an existing issue and return the updated version."""
        if issue_id not in self._issues:
            raise ValueError(f"Issue with ID {issue_id} not found")
        
        issue = self._issues[issue_id]
        issue.update(**kwargs)
        return issue
    
    def add_comment(self, issue_id: str, content: str) -> Comment:
        """Add a comment to an issue and return the created comment."""
        if issue_id not in self._issues:
            raise ValueError(f"Issue with ID {issue_id} not found")
        
        issue = self._issues[issue_id]
        comment = MemoryComment(self._current_user, content)
        issue.add_comment(comment)
        return comment
    
    def search_issues(self, query: str) -> Iterator[Issue]:
        """Search for issues matching the query string."""
        # Simple case-insensitive search in title and description
        query = query.lower()
        matching_issues = []
        
        for issue in self._issues.values():
            if (query in issue.title.lower() or 
                query in issue.description.lower()):
                matching_issues.append(issue)
        
        return iter(matching_issues)