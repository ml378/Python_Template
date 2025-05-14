# Python Project with CI/CD Pipeline (CircleCI)

***Overview***

This project defines the core API for a Python-based Issue Tracker. The project contains automated unit tests, integration tests, and test coverage reports covered by CircleCI. The API establishes a clear contract for how components (`Comment`, `Issue`, and `IssueTrackerClient`) interact. The minimum viable version of this project would include a functional IssueTrackerClient, where users could raise issues that could then be viewed and managed. The project utilizes interface programming rather than concrete implementation, as well as a factory pattern for basic dependency injection.

***Features***

1. Protocol-Based Interfaces, with a functional mock backend

2. Automated unit tests with pytest, Test coverage report and general CI/CD pipeline provided by CircleCI

3. Dependency Injection via `get_issue_tracker_client()`

4. Quality Assurance and Tooling
- Pre-commit checks with mypy and ruff
- Modern dependency management using uv
- Static analysis and formatting checks

5. GitHub Actions for continuous integration

**How to run**

Follow these steps to set up and run the Issue Tracker:

1. **Clone the repository**
   ```sh
   git clone https://github.com/ml378/Python_Template.git
   cd Python_Template
   ```

2. **Create and activate a virtual environment**
   ```sh
   python -m venv venv
   
   # On macOS/Linux
   source venv/bin/activate
   
   # On Windows
   venv\Scripts\activate
   ```

3. **Install dependencies**
   ```sh
   python -m pip install --upgrade pip
   pip install uv
   # Use UV to install dependencies instead of pip
   uv sync
   ```

4. **Install the CLI tool in development mode**
   ```sh
   pip install -e .
   ```

5. **Run the issue tracker**
   ```sh
   # List all issues
   issue-tracker list
   
   # Create a new issue
   issue-tracker create --title "First issue" --description "This is my first issue" --priority "high"
   
   # View details of a specific issue (replace issue-id with an actual ID)
   issue-tracker view issue-id
   ```

For more CLI options and examples, see the "CLI Interface" section below.

## API Interface Design

The API is centered around three main protocols defined in `src/__init__.py`.

### Core Protocols:

1.  **`Comment` Protocol:**
    *   **Purpose:** Represents a single comment on an issue.
    *   **Key Attributes:** `id` (str), `author` (str), `content` (str), `created_at` (str, ISO 8601).
    *   *Example Snippet (Interface):*
        ```python
        class Comment(Protocol):
            @property
            def id(self) -> str: ...
            # ...
        ```

2.  **`Issue` Protocol:**
    *   **Purpose:** Represents a trackable issue.
    *   **Key Attributes:** `id` (str), `title` (str), `description` (str), `status` (str), `creator` (str), `assignee` (str | None), `labels` (list[str]), `priority` (str | None).
    *   **Key Methods:** `get_comments() -> Iterator[Comment]`.
    *   *Example Snippet (Interface):*
        ```python
        class Issue(Protocol):
            @property
            def title(self) -> str: ...
            def get_comments(self) -> Iterator[Comment]: ...
            # ... 
        ```

3.  **`IssueTrackerClient` Protocol:**
    *   **Purpose:** Defines operations for managing issues and comments.
    *   **Key Methods:**
        *   `get_issues(filters: dict | None) -> Iterator[Issue]`
        *   `get_issue(issue_id: str) -> Issue`
        *   `create_issue(title: str, description: str, **kwargs) -> Issue`
        *   `update_issue(issue_id: str, **kwargs) -> Issue`
        *   `add_comment(issue_id: str, content: str) -> Comment`
        *   `search_issues(query: str) -> Iterator[Issue]`
    *   *Example Snippet (Interface):*
        ```python
        class IssueTrackerClient(Protocol):
            def create_issue(self, title: str, description: str, **_kwargs: Any) -> Issue: ...
            # ...
        ```

## CLI Interface

The Issue Tracker comes with a command-line interface for easy interaction with the system.

### Installation

Install the CLI tool with:
```sh
pip install -e .
```

### Usage

```sh
issue-tracker [command] [options]
```

### Available Commands

1. **List Issues**
   ```sh
   issue-tracker list [--status STATUS] [--assignee USERNAME] [--labels LABEL1,LABEL2]
   ```
   Lists all issues matching the provided filters.

2. **View Issue Details**
   ```sh
   issue-tracker view ISSUE_ID
   ```
   Displays detailed information about a specific issue including comments.

3. **Create Issue**
   ```sh
   issue-tracker create --title "Issue title" --description "Issue description" [--assignee USERNAME] [--labels LABEL1,LABEL2] [--priority PRIORITY]
   ```
   Creates a new issue with the specified attributes.

4. **Update Issue**
   ```sh
   issue-tracker update ISSUE_ID [--title "New title"] [--description "New description"] [--status STATUS] [--assignee USERNAME] [--labels LABEL1,LABEL2] [--priority PRIORITY]
   ```
   Updates an existing issue with new values.

5. **Add Comment**
   ```sh
   issue-tracker comment ISSUE_ID "Your comment text"
   ```
   Adds a comment to the specified issue.

6. **Search Issues**
   ```sh
   issue-tracker search "search term"
   ```
   Searches for issues containing the search term in title or description.

### Examples

```sh
# List all open issues
issue-tracker list --status open

# Create a new bug report
issue-tracker create --title "Login page error" --description "Users can't log in with correct credentials" --labels bug,urgent --priority high

# Assign an issue to someone
issue-tracker update issue-123 --assignee "johndoe" --status "in-progress"

# Add a comment to an issue
issue-tracker comment issue-123 "I've started working on this bug"

# Search for issues about login
issue-tracker search "login"
```

For more details on specific commands, use:
```sh
issue-tracker [command] --help
```

### Dependency Management & Mock Implementation

*   A mock implementation (`src/mock_implementation.py`) provides concrete classes (`MockComment`, `MockIssue`, `MockIssueTrackerClient`) that implement these protocols. This allows for immediate testing and development against the interfaces.
*   The `get_issue_tracker_client()` function (in `src/__init__.py`) acts as a factory. It returns an instance of `IssueTrackerClient`. This approach allows a decoupling of the client to the specific mock implementation.

    ```python
    # Example usage:
    # from src import get_issue_tracker_client, Issue
    #
    # client = get_issue_tracker_client()
    # new_issue: Issue = client.create_issue("Bug Fix", "Fix the login redirect.")
    ```

## Project Structure

The project is organized to clearly separate interface definitions, mock implementations, and tests:

*   `src/`:
    *   `__init__.py`: contains the `Comment`, `Issue`, and `IssueTrackerClient` protocol definitions, and the `get_issue_tracker_client()` factory function
    *   `mock_implementation.py`: contains the `MockComment`, `MockIssue`, and `MockIssueTrackerClient` classes that implement the protocols
*   `tests/`: contains all tests related to the interface definition:
    *   `test_interfaces.py`: verifies protocol conformance of mock implementations
    *   `test_interfaces_behavior.py`: tests behavior of mock client methods
    *   `test_type_checking.py`: mypy target for validating protocol type definitions



## Run tests:
1.  Run Pytest tests:
    ```bash
    pytest
    ```
    To generate a coverage report:
    ```bash
    pytest --cov=src --cov-report=html
    ```

2.  Run Ruff Linter:
    ```bash
    ruff check .
    ```

3.  Run Ruff Formatter:
    ```bash
    ruff format --check .
    ```
    To automatically format: `ruff format .`

4.  Run Mypy Static Type Checker
    ```bash
    mypy src/ tests/
    ```

## CI/CD (CircleCI)

*   The CircleCI pipeline (`.circleci/config.yml`) is configured for this project.
*   On every push, CircleCI automatically:
    *   Installs dependencies.
    *   Runs `ruff check .` and `ruff format --check .`.
    *   Runs `mypy src/ tests/`.
    *   Executes all `pytest` tests.
*   A passing CircleCI build indicates that the project comprehensively functions correctly and adheres to coding standards and type safety.
*   CircleCI link: https://app.circleci.com/pipelines/circleci/PMKrmVKcMeLYLN4ZAWvPSF/MixxMSzUixT5Ap1GdSpFR8

## Tech Stack

*   **Python:** 3.10+
*   **Interface Definition:** `typing.Protocol`
*   **Testing:** `pytest`
*   **Linting & Formatting:** `Ruff`
*   **Static Type Checking:** `Mypy`
*   **Dependency Management:** `uv`
*   **Continuous Integration:** CircleCI


***Pull Requests***

1. Use the pull request template from .github/pull_request_template/

2. Provide a clear summary of the PR.

3. Explain the motivation behind the changes.

4. Describe any testing performed to ensure correctness.


***License***

This project is licensed under the MIT License.