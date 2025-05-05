from __future__ import annotations

import json
import logging
from pathlib import Path

import pytest

from src.issue_tracker import FileIssueTrackerClient, MemoryComment, MemoryIssue


@pytest.fixture
def data_file(tmp_path: Path) -> Path:
    """Provides a temporary, unique file path for issue data for each test."""
    data_dir = tmp_path / "test_data"
    return data_dir / "issues_test.json"


@pytest.fixture
def client(data_file: Path) -> FileIssueTrackerClient:
    """Fixture to create a FileIssueTrackerClient instance using a temp file."""
    instance = FileIssueTrackerClient(filepath=str(data_file))
    return instance


@pytest.fixture
def client_with_issues(client: FileIssueTrackerClient) -> FileIssueTrackerClient:
    """Fixture to create a client with some pre-populated issues.

    Relies on the client fixture which uses a unique temp file. Operations will save to that temp file. 

    Operations here will trigger saves to that temp file.
    """
    client.set_current_user("user1")
    client.create_issue(
        "Bug 1",
        "Description for bug 1",
        status="open",
        labels=["bug", "ui"],
        priority="high",
    )
    client.create_issue(
        "Feature Request",
        "Add new feature",
        status="open",
        labels=["feature"],
        assignee="user2",
    )
    client.set_current_user("user2")
    client.create_issue(
        "Bug 2",
        "Another bug description",
        status="closed",
        labels=["bug", "backend"],
        assignee="user1",
    )
    client.set_current_user("default_user")  # reset user for subsequent tests
    return client

def test_init(client: FileIssueTrackerClient, data_file: Path):
    """Test client initialization with a non-existent file."""
    assert isinstance(client.get_issue_dict(), dict)
    assert len(client.get_issue_dict()) == 0
    assert client.get_current_user() == "default_user"
    assert data_file.parent.exists()


def test_set_current_user(client: FileIssueTrackerClient):
    """Test setting the current user."""
    client.set_current_user("test_user")
    assert client.get_current_user() == "test_user"


def test_create_issue(client: FileIssueTrackerClient, data_file: Path):
    """Test creating a new issue."""
    client.set_current_user("creator_user")
    issue = client.create_issue(
        "New Issue",
        "Issue Description",
        labels=["test"],
        priority="medium",
        assignee="assignee_user",
    )
    assert isinstance(issue, MemoryIssue)
    assert issue.title == "New Issue"
    assert issue.description == "Issue Description"
    assert issue.creator == "creator_user"
    assert issue.status == "open"  # Default status
    assert issue.labels == ["test"]
    assert issue.priority == "medium"
    assert issue.assignee == "assignee_user"
    assert issue.id in client.get_issue_dict()
    assert client.get_issue_dict()[issue.id] == issue

    assert data_file.exists()
    client2 = FileIssueTrackerClient(filepath=str(data_file))
    assert issue.id in client2.get_issue_dict()
    loaded_issue = client2.get_issue(issue.id)
    assert loaded_issue.title == "New Issue"
    assert loaded_issue.creator == "creator_user"


def test_get_issue(client_with_issues: FileIssueTrackerClient):
    """Test retrieving a specific issue (should load from file implicitly)."""    # Get the ID of the first created issue
    issue_id = None
    for issue in client_with_issues.get_issues():
        if issue.title == "Bug 1":
            issue_id = issue.id
            break

    assert issue_id is not None, "Failed to find 'Bug 1' in fixture setup"

    issue = client_with_issues.get_issue(issue_id)
    assert issue.id == issue_id
    assert issue.title == "Bug 1"


def test_get_issue_not_found(client: FileIssueTrackerClient):
    """Test retrieving a non-existent issue raises ValueError."""
    with pytest.raises(ValueError, match="Issue with ID non_existent_id not found"):
        client.get_issue("non_existent_id")


def test_get_issues_no_filters(client_with_issues: FileIssueTrackerClient):
    """Test retrieving all issues without filters."""
    issues = list(client_with_issues.get_issues())
    assert len(issues) == 3
    assert {issue.title for issue in issues} == {"Bug 1", "Feature Request", "Bug 2"}


def test_get_issues_with_filters(client_with_issues: FileIssueTrackerClient):
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
    open_bug_issues = list(
        client_with_issues.get_issues(filters={"status": "open", "labels": ["bug"]}),
    )
    assert len(open_bug_issues) == 1
    assert open_bug_issues[0].title == "Bug 1"


def test_update_issue(client_with_issues: FileIssueTrackerClient, data_file: Path):
    """Test updating an existing issue."""
    issue_id = next(issue.id for issue in client_with_issues.get_issues() if issue.title == "Bug 1")
    original_issue = client_with_issues.get_issue(issue_id)
    original_updated_at = original_issue.updated_at

    updated_issue = client_with_issues.update_issue(
        issue_id,
        title="Updated Bug 1",
        status="in_progress",
        assignee="user3",
        labels=["bug", "critical"],
        priority="critical",
    )

    assert updated_issue.id == issue_id
    assert updated_issue.title == "Updated Bug 1"
    assert updated_issue.status == "in_progress"
    assert updated_issue.assignee == "user3"
    assert updated_issue.labels == ["bug", "critical"]
    assert updated_issue.priority == "critical"
    assert updated_issue.updated_at != original_updated_at

    # persistence check
    client2 = FileIssueTrackerClient(filepath=str(data_file))
    loaded_issue = client2.get_issue(issue_id)
    assert loaded_issue.title == "Updated Bug 1"
    assert loaded_issue.status == "in_progress"


def test_update_issue_not_found(client: FileIssueTrackerClient):
    """Test updating a non-existent issue raises ValueError."""
    with pytest.raises(ValueError, match="Issue with ID non_existent_id not found"):
        client.update_issue("non_existent_id", title="Doesn't Matter")


def test_add_comment(client_with_issues: FileIssueTrackerClient, data_file: Path):
    """Test adding a comment to an issue and that it persists."""
    issue_id = next(issue.id for issue in client_with_issues.get_issues() if issue.title == "Bug 1")
    client_with_issues.set_current_user("commenter_user")
    comment_content = "This is a test comment."

    comment = client_with_issues.add_comment(issue_id, comment_content)

    assert isinstance(comment, MemoryComment)
    assert comment.author == "commenter_user"
    assert comment.content == comment_content
    assert comment.id is not None
    assert comment.created_at is not None

    # persistence check
    client2 = FileIssueTrackerClient(filepath=str(data_file))
    loaded_issue = client2.get_issue(issue_id)
    loaded_comments = list(loaded_issue.get_comments())
    assert len(loaded_comments) > 0
    assert loaded_comments[-1].content == comment_content
    assert loaded_comments[-1].author == "commenter_user"


def test_add_comment_issue_not_found(client: FileIssueTrackerClient):
    """Test adding a comment to a non-existent issue raises ValueError."""
    with pytest.raises(ValueError, match="Issue with ID non_existent_id not found"):
        client.add_comment("non_existent_id", "Some comment")


def test_get_comments(client_with_issues: FileIssueTrackerClient, data_file: Path):
    """Test retrieving comments from an issue."""
    issue_id = next(issue.id for issue in client_with_issues.get_issues() if issue.title == "Feature Request")
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

     # retrieve issue again from the same client, test if comment(s) in memory
    issue = client_with_issues.get_issue(issue_id)
    comments = list(issue.get_comments())

    assert len(comments) == 2
    assert comments[0].content == "Comment 1"
    assert comments[1].content == "Comment 2"

    # verify persistence
    client2 = FileIssueTrackerClient(filepath=str(data_file))
    loaded_issue = client2.get_issue(issue_id)
    loaded_comments = list(loaded_issue.get_comments())
    assert len(loaded_comments) == 2


def test_search_issues(client_with_issues: FileIssueTrackerClient):
    """Test searching issues by query string."""
    results_bug = list(client_with_issues.search_issues("Bug"))
    assert len(results_bug) == 2
    assert {issue.title for issue in results_bug} == {"Bug 1", "Bug 2"}

    results_feature = list(client_with_issues.search_issues("Feature"))
    assert len(results_feature) == 1
    assert results_feature[0].title == "Feature Request"

    results_description = list(
        client_with_issues.search_issues("another bug"),
    )
    assert len(results_description) == 1
    assert results_description[0].title == "Bug 2"

    results_desc_bug = list(client_with_issues.search_issues("description"))
    assert (
        len(results_desc_bug) == 2
    )
    assert {issue.title for issue in results_desc_bug} == {"Bug 1", "Bug 2"}


def test_search_issues_no_results(client_with_issues: FileIssueTrackerClient):
    """Test searching issues with a query that yields no results."""
    results = list(client_with_issues.search_issues("non_matching_query"))
    assert len(results) == 0


def test_close_issue(client_with_issues: FileIssueTrackerClient, data_file: Path):
    """Test closing an issue and that it persists."""
    issue_id = next(issue.id for issue in client_with_issues.get_issues() if issue.title == "Bug 1")

    closed_issue = client_with_issues.close_issue(issue_id, "fixed")

    assert closed_issue.status == "closed"

    comments = list(closed_issue.get_comments())
    assert len(comments) > 0
    assert "Closed with resolution: fixed" in comments[-1].content

    # persistence check
    client2 = FileIssueTrackerClient(filepath=str(data_file))
    loaded_issue = client2.get_issue(issue_id)
    assert loaded_issue.status == "closed"
    loaded_comments = list(loaded_issue.get_comments())
    assert "Closed with resolution: fixed" in loaded_comments[-1].content

# file-persistence specific tests

def test_load_existing_file(data_file: Path):
    """Test loading data from a pre-existing valid JSON file."""
    # manually created test issues
    issue_id_1 = "issue_abc"
    issue_id_2 = "issue_def"
    initial_data = {
        issue_id_1: {
            "id": issue_id_1, "title": "Pre-existing Issue", "description": "Loaded from file",
            "status": "open", "creator": "file_creator", "assignee": None,
            "created_at": "2023-01-01T10:00:00Z", "updated_at": "2023-01-01T11:00:00Z",
            "labels": ["persistent"], "priority": None, "comments": [],
        },
         issue_id_2: {
            "id": issue_id_2, "title": "Another Pre-existing", "description": "Also loaded",
            "status": "closed", "creator": "file_creator_2", "assignee": "someone",
            "created_at": "2023-01-02T12:00:00Z", "updated_at": "2023-01-02T13:00:00Z",
            "labels": [], "priority": "low", "comments": [
                {"id": "comment_123", "author": "commenter", "content": "Pre-loaded comment", "created_at": "2023-01-02T12:30:00Z"},
            ],
        },
    }
    data_file.parent.mkdir(parents=True, exist_ok=True)
    data_file.write_text(json.dumps(initial_data, indent=2))

    client = FileIssueTrackerClient(filepath=str(data_file))

    assert len(client.get_issue_dict()) == 2
    assert issue_id_1 in client.get_issue_dict()
    assert issue_id_2 in client.get_issue_dict()

    loaded_issue_1 = client.get_issue(issue_id_1)
    assert loaded_issue_1.title == "Pre-existing Issue"
    assert loaded_issue_1.labels == ["persistent"]

    loaded_issue_2 = client.get_issue(issue_id_2)
    assert loaded_issue_2.status == "closed"
    assert loaded_issue_2.assignee == "someone"
    comments = list(loaded_issue_2.get_comments())
    assert len(comments) == 1
    assert comments[0].content == "Pre-loaded comment"
    assert comments[0].author == "commenter"


def test_load_empty_file(data_file: Path, caplog):
    """Test loading from an empty file (should start fresh)."""
    data_file.parent.mkdir(parents=True, exist_ok=True)
    data_file.touch()
    assert data_file.read_text() == ""

    with caplog.at_level(logging.WARNING):
        client = FileIssueTrackerClient(filepath=str(data_file))
        assert len(client.get_issue_dict()) == 0
        assert f"Failed to decode JSON from {data_file}" in caplog.text \
            or f"Invalid data format in {data_file}" in caplog.text \
            or "Starting fresh" in caplog.text

def test_load_invalid_json_file(data_file: Path, caplog):
    """Test loading from a file with invalid JSON."""
    data_file.parent.mkdir(parents=True, exist_ok=True)
    data_file.write_text("this is not json {")

    with caplog.at_level(logging.ERROR):
        client = FileIssueTrackerClient(filepath=str(data_file))
        assert len(client.get_issue_dict()) == 0
        assert f"Failed to decode JSON from {data_file}" in caplog.text

def test_load_wrong_json_type(data_file: Path, caplog):
    """Test loading from valid JSON that isn't a dictionary."""
    data_file.parent.mkdir(parents=True, exist_ok=True)
    data_file.write_text(json.dumps([{"id": "a"}, {"id": "b"}]))

    with caplog.at_level(logging.ERROR):
        client = FileIssueTrackerClient(filepath=str(data_file))
        assert len(client.get_issue_dict()) == 0
        assert f"Invalid data format in {data_file}" in caplog.text


def test_directory_creation(tmp_path: Path):
    """Test that the client creates the data directory if it doesn't exist."""
    non_existent_dir = tmp_path / "new_data_dir"
    data_file = non_existent_dir / "issues.json"

    assert not non_existent_dir.exists()

    client = FileIssueTrackerClient(filepath=str(data_file))
    assert non_existent_dir.exists()
    assert non_existent_dir.is_dir()


def test_save_and_reload(data_file: Path):
    """Test saving data and reloading it in a new client instance."""
    # client 1 creates data,
    client1 = FileIssueTrackerClient(filepath=str(data_file))
    client1.set_current_user("first_user")
    issue1 = client1.create_issue("Save Test", "Data to be saved")
    client1.add_comment(issue1.id, "A comment to save")

    # client 2 loads data added by client 1
    client2 = FileIssueTrackerClient(filepath=str(data_file))
    assert len(client2.get_issue_dict()) == 1
    loaded_issue = client2.get_issue(issue1.id)

    assert loaded_issue.title == "Save Test"
    assert loaded_issue.creator == "first_user"
    comments = list(loaded_issue.get_comments())
    assert len(comments) == 1
    assert comments[0].content == "A comment to save"
