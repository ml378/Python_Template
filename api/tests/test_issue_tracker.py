from __future__ import annotations

import pytest
import sys,os
from api.src.issue_tracker import MemoryIssueTrackerClient, MemoryIssue, MemoryComment

@pytest.fixture
def client():
    """Fixture to create a MemoryIssueTrackerClient instance."""
    return MemoryIssueTrackerClient()

@pytest.fixture
def client_with_issues(client):
    """Fixture to create a client with some pre-populated issues."""
    client.set_current_user("user1")
    client.create_issue("Bug 1", "Description for bug 1", status="open", labels=["bug", "ui"], priority="high")
    client.create_issue("Feature Request", "Add new feature", status="open", labels=["feature"], assignee="user2")
    client.set_current_user("user2")
    client.create_issue("Bug 2", "Another bug description", status="closed", labels=["bug", "backend"], assignee="user1")
    client.set_current_user("default_user") # Reset user for subsequent tests
    return client

def test_init(client):
    """Test client initialization."""
    assert isinstance(client.get_issue_dict(), dict)
    assert len(client.get_issue_dict()) == 0
    assert client.get_current_user() == "default_user"

def test_set_current_user(client):
    """Test setting the current user."""
    client.set_current_user("test_user")
    assert client.get_current_user() == "test_user"

def test_create_issue(client):
    """Test creating a new issue."""
    client.set_current_user("creator_user")
    issue = client.create_issue("New Issue", "Issue Description", labels=["test"], priority="medium", assignee="assignee_user")
    assert isinstance(issue, MemoryIssue)
    assert issue.title == "New Issue"
    assert issue.description == "Issue Description"
    assert issue.creator == "creator_user"
    assert issue.status == "open" # Default status
    assert issue.labels == ["test"]
    assert issue.priority == "medium"
    assert issue.assignee == "assignee_user"
    assert issue.id in client.get_issue_dict()
    assert client.get_issue_dict()[issue.id] == issue

def test_get_issue(client_with_issues):
    """Test retrieving a specific issue."""
    # Get the ID of the first created issue
    issue_id = next(iter(client_with_issues.get_issue_dict().keys()))
    issue = client_with_issues.get_issue(issue_id)
    assert issue.id == issue_id
    assert issue.title == "Bug 1"

def test_get_issue_not_found(client):
    """Test retrieving a non-existent issue raises ValueError."""
    with pytest.raises(ValueError, match="Issue with ID non_existent_id not found"):
        client.get_issue("non_existent_id")

def test_get_issues_no_filters(client_with_issues):
    """Test retrieving all issues without filters."""
    issues = list(client_with_issues.get_issues())
    assert len(issues) == 3
    assert {issue.title for issue in issues} == {"Bug 1", "Feature Request", "Bug 2"}

def test_get_issues_with_filters(client_with_issues):
    """Test retrieving issues with various filters."""
    # Filter by status
    open_issues = list(client_with_issues.get_issues(filters={"status": "open"}))
    assert len(open_issues) == 2
    assert {issue.title for issue in open_issues} == {"Bug 1", "Feature Request"}

    closed_issues = list(client_with_issues.get_issues(filters={"status": "closed"}))
    assert len(closed_issues) == 1
    assert closed_issues[0].title == "Bug 2"

    # Filter by assignee
    user1_assigned = list(client_with_issues.get_issues(filters={"assignee": "user1"}))
    assert len(user1_assigned) == 1
    assert user1_assigned[0].title == "Bug 2"

    user2_assigned = list(client_with_issues.get_issues(filters={"assignee": "user2"}))
    assert len(user2_assigned) == 1
    assert user2_assigned[0].title == "Feature Request"

    # Filter by labels (match any)
    bug_issues = list(client_with_issues.get_issues(filters={"labels": ["bug"]}))
    assert len(bug_issues) == 2
    assert {issue.title for issue in bug_issues} == {"Bug 1", "Bug 2"}

    ui_issues = list(client_with_issues.get_issues(filters={"labels": ["ui"]}))
    assert len(ui_issues) == 1
    assert ui_issues[0].title == "Bug 1"

    # Filter by multiple criteria
    open_bug_issues = list(client_with_issues.get_issues(filters={"status": "open", "labels": ["bug"]}))
    assert len(open_bug_issues) == 1
    assert open_bug_issues[0].title == "Bug 1"

def test_update_issue(client_with_issues):
    """Test updating an existing issue."""
    issue_id = next(iter(client_with_issues.get_issue_dict().keys())) # Get ID of "Bug 1"
    original_issue = client_with_issues.get_issue(issue_id)
    original_updated_at = original_issue.updated_at

    updated_issue = client_with_issues.update_issue(
        issue_id,
        title="Updated Bug 1",
        status="in_progress",
        assignee="user3",
        labels=["bug", "critical"],
        priority="critical"
    )

    assert updated_issue.id == issue_id
    assert updated_issue.title == "Updated Bug 1"
    assert updated_issue.status == "in_progress"
    assert updated_issue.assignee == "user3"
    assert updated_issue.labels == ["bug", "critical"]
    assert updated_issue.priority == "critical"
    assert updated_issue.updated_at != original_updated_at # Check timestamp updated

    # Verify the update is reflected in the internal store
    stored_issue = client_with_issues.get_issue(issue_id)
    assert stored_issue.title == "Updated Bug 1"
    assert stored_issue.status == "in_progress"

def test_update_issue_not_found(client):
    """Test updating a non-existent issue raises ValueError."""
    with pytest.raises(ValueError, match="Issue with ID non_existent_id not found"):
        client.update_issue("non_existent_id", title="Doesn't Matter")

def test_add_comment(client_with_issues):
    """Test adding a comment to an issue."""
    issue_id = next(iter(client_with_issues.get_issue_dict().keys())) # Get ID of "Bug 1"
    client_with_issues.set_current_user("commenter_user")
    comment_content = "This is a test comment."

    comment = client_with_issues.add_comment(issue_id, comment_content)

    assert isinstance(comment, MemoryComment)
    assert comment.author == "commenter_user"
    assert comment.content == comment_content
    assert comment.id is not None
    assert comment.created_at is not None

    # Verify comment is added to the issue
    issue = client_with_issues.get_issue(issue_id)
    comments = list(issue.get_comments())
    assert len(comments) == 1
    assert comments[0] == comment
    assert comments[0].content == comment_content

def test_add_comment_issue_not_found(client):
    """Test adding a comment to a non-existent issue raises ValueError."""
    with pytest.raises(ValueError, match="Issue with ID non_existent_id not found"):
        client.add_comment("non_existent_id", "Some comment")

def test_get_comments(client_with_issues):
    """Test retrieving comments from an issue.""" 
    issue_id = next(iter(client_with_issues.get_issue_dict().keys())) # Get ID of "Bug 1"
    client_with_issues.set_current_user("user_a")
    client_with_issues.add_comment(issue_id, "Comment 1")
    client_with_issues.set_current_user("user_b")
    client_with_issues.add_comment(issue_id, "Comment 2")

    issue = client_with_issues.get_issue(issue_id)
    comments = list(issue.get_comments())

    assert len(comments) == 2
    assert comments[0].content == "Comment 1"
    assert comments[0].author == "user_a"
    assert comments[1].content == "Comment 2"
    assert comments[1].author == "user_b"

def test_search_issues(client_with_issues):
    """Test searching issues by query string."""
    # Search in title
    results_bug = list(client_with_issues.search_issues("Bug"))
    assert len(results_bug) == 2
    assert {issue.title for issue in results_bug} == {"Bug 1", "Bug 2"}

    results_feature = list(client_with_issues.search_issues("Feature"))
    assert len(results_feature) == 1
    assert results_feature[0].title == "Feature Request"

    results_description = list(client_with_issues.search_issues("another bug")) # Search in description (case-insensitive)
    assert len(results_description) == 1
    assert results_description[0].title == "Bug 2"

    # Search matching both title and description
    results_desc_bug = list(client_with_issues.search_issues("description"))
    assert len(results_desc_bug) == 2 # Matches "Description for bug 1" and "Another bug description"
    assert {issue.title for issue in results_desc_bug} == {"Bug 1", "Bug 2"}

def test_search_issues_no_results(client_with_issues):
    """Test searching issues with a query that yields no results."""
    results = list(client_with_issues.search_issues("non_matching_query"))
    assert len(results) == 0