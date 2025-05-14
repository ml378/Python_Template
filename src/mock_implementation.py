from __future__ import annotations

from typing import Any, Iterator

from . import Comment, Issue, IssueTrackerClient


class MockComment(Comment):
    def __init__(self, content: str = "This is a comment"):
        self._content: str = content

    @property
    def id(self) -> str:
        return "comment-1"

    @property
    def author(self) -> str:
        return "user1"

    @property
    def content(self) -> str:
        return self._content

    @property
    def created_at(self) -> str:
        return "2025-05-09"


class MockIssue(Issue):
    def __init__(
        self,
        issue_id: str = "issue-1",
        title: str = "Test Issue",
        description: str = "A Description",
        status: str = "open",
        creator: str = "user1",
        assignee: str | None = "user2",
        created_at: str = "2025-05-09",
        updated_at: str = "2025-05-10",
        priority: str = "high",
    ):
        self._id = issue_id
        self._title = title
        self._description = description
        self._status = status
        self._comments: list[MockComment] = []
        self._creator = creator
        self._assignee = assignee
        self._created_at = created_at
        self._updated_at = updated_at
        self._labels = ["bug", "frontend"]
        self._priority = priority

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
        if not self._comments:
            self._comments.append(MockComment())
        yield from self._comments

    def add_mock_comment(self, comment: MockComment):
        self._comments.append(comment)

    def set_status(self, status: str):
        self._status = status

    def set_assignee(self, assignee: str | None):
        self._assignee = assignee


class MockIssueTrackerClient(IssueTrackerClient):
    def __init__(self):
        self._issues_store: dict[str, MockIssue] = {}
        self._next_issue_id = 1

    def get_issues(self, filters: dict[str, Any] | None = None) -> Iterator[Issue]:
        if not self._issues_store:
            yield MockIssue(issue_id="default-issue-for-get-issues")
        else:
            for issue in self._issues_store.values():
                if filters:
                    match = True
                    for key, value in filters.items():
                        if hasattr(issue, key) and getattr(issue, key) != value:
                            match = False
                            break
                    if match:
                        yield issue
                else:
                    yield issue

    def get_issue(self, issue_id: str) -> Issue:
        if issue_id in self._issues_store:
            return self._issues_store[issue_id]
        return MockIssue(issue_id=issue_id, title=f"Mock Issue {issue_id}")

    def create_issue(self, title: str, description: str, **kwargs: Any) -> Issue:  # noqa: ANN401
        new_id = f"issue-{self._next_issue_id}"
        self._next_issue_id += 1
        new_issue = MockIssue(issue_id=new_id, title=title, description=description)
        self._issues_store[new_id] = new_issue

        if (
            "status" in kwargs
            and hasattr(new_issue, "set_status")
            and callable(new_issue.set_status)
        ):
            new_issue.set_status(kwargs["status"])

        if (
            "assignee" in kwargs
            and hasattr(new_issue, "set_assignee")
            and callable(new_issue.set_assignee)
        ):
            new_issue.set_assignee(kwargs["assignee"])

        return new_issue

    def update_issue(self, issue_id: str, **kwargs: Any) -> Issue:  # noqa: ANN401
        if issue_id in self._issues_store:
            issue = self._issues_store[issue_id]
            if "title" in kwargs:
                issue._title = kwargs["title"]
            if "description" in kwargs:
                issue._description = kwargs["description"]
            if "status" in kwargs:
                issue.set_status(kwargs["status"])
            if "assignee" in kwargs:
                issue.set_assignee(kwargs["assignee"])
            if "priority" in kwargs:
                issue._priority = kwargs["priority"]
            issue._updated_at = "2025-05-11"  # In a real implementation, this would be the current date
            return issue
        return MockIssue(issue_id=issue_id, title="Updated Mock Issue")

    def add_comment(self, issue_id: str, content: str) -> Comment:
        new_comment = MockComment(content)
        if issue_id in self._issues_store:
            issue = self._issues_store[issue_id]
            issue.add_mock_comment(new_comment)
        return new_comment

    def search_issues(self, query: str) -> Iterator[Issue]:
        yield MockIssue(issue_id="search-result-issue", title=f"Search: {query}")
