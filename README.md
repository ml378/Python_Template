# Python Issue Tracker

***Overview***

This repository provides a modern Python project template with robust CI/CD capabilities. The project provides the core backend logic for an in-memory issue tracking system. It allows users to (programmatically) create, manage, comment on, and search for issues. The project is built with maintainability in mind, and showcases:

- A complete issue tracking client implementation in Python
- End-to-end testing strategy with both unit and integration tests
- Comprehensive code quality tools and automation
- Production-ready deployment pipeline with CircleCI

***Key Features***

- Issue Management: Create issues, retrive details, update issue properties, track issue status
- Collaboration, organization and search of all issues, using keywords and other properties
- Automated unit tests with thorough coverage, a robust CI/CD pipeline, Github actions for continuous integration 
- Pre-commit checks, dependency management, static analysis and formatting checks 

***Prerequisites***

1. Python 3.8 or higher
2. UV for Python dependency management
3. Git installed on your system
4. A GitHub account for accessing the repository
5. CircleCI account (for viewing CI/CD pipeline results)

# Setup & Installation

Clone the repository:
```sh
git clone https://github.com/ml378/Python_Template.git
cd Python_Template
```

Install dependencies:
```sh
python -m venv venv
source venv/bin/activate  # On Windows, use: venv\Scripts\activate
pip install uv
uv pip install -r requirements.txt
```

Configure pre-commit hooks:
```sh
pre-commit install
```

Run tests:
```sh
pytest --cov=src --cov-report=html
```

```sh
nose2 -v nose2_tests
```

View test coverage:

```sh
open htmlcov/index.html  # macOS
xdg-open htmlcov/index.html  # Linux
start htmlcov/index.html  # Windows
```

# Usage Examples

Ensure the package is accessible from the local python environment, or that the api directory is in your PYTHONPATH. 

```
from api.src import get_issue_tracker_client, Issue

client = get_issue_tracker_client()

client.set_current_user("dev_user_1")
```

Create an issue

```
new_issue = client.create_issue(
     title="Issue Name",
     description="Issue description.",
     priority="medium",
     labels=["bug", "ui"],
     assignee="dev_user_2"
 )
```

Add a comment 

```
comment = client.add_comment(
     issue_id=new_issue.id,
     content="Issue comment"
 )
```

Update the issue 

```
updated_issue = client.update_issue(
     issue_id=new_issue.id,
     status="in_progress",
     assignee="dev_user_1" # Reassigning
 )
```

Get issue details

```
fetched_issue = client.get_issue(new_issue.id)
print(f"Fetched Issue Title: {fetched_issue.title}")
print("Comments:")
for c in fetched_issue.get_comments():
  print(f"- {c.content} (by {c.author})")
```

Filter issues

```
ui_bugs = client.get_issues(filters={"status": "open", "labels": ["ui"]})
for issue in ui_bugs:
  print(f"- {issue.id}: {issue.title}")
```

Search issues

```
search_results = client.search_issues("Name")
for issue in search_results:
  print(f"- {issue.id}: {issue.title}")
```
Close an issue

```
client.close_issue(issue_id=issue.id, resolution="fixed")
```

***Project Structure***

```
Python_Template/
├── .circleci/        
├── .github/
├── .api/                
   ├── src/                # Source code for the issue tracker
   │   ├── __init__.py
   │   ├── issue_tracker.py
   │   └── ...
   ├── tests/             # Tests for the issue tracker  
   │   ├── test_issue_tracker.py
   │   └── ...
├── tests/             
├── nose2_tests/        
├── .pre-commit-config.yaml
├── pyproject.toml      # Project configuration, metadata 
├── requirements.txt    # Project dependencies
└── README.md           # This file
```

# Development Workflow

1. Create a new branch for your feature or bugfix

```
git checkout -b feature/your-feature-name
```

2. Make your changes and write tests

3. Run tests locally to ensure pre-commit checks passes
   
```
pytest --cov=api/src
```

4. Submit a pull request using the provided template (.github/pull_request_template.md)

# Pull Requests

1. Use the pull request template from .github/pull_request_template/

2. Provide a clear summary of the PR.

3. Explain the motivation behind the changes.

4. Describe any testing performed to ensure correctness.

***Tech Stack***

Python 3.8+

Pytest, Coverage.py, (Nose2)

CircleCI

Coverage.py

Ruff (Linting)

Mypy (Type Checking)

uv, pip (Dependency Management)

# Further Improvements

We plan to enhance this issue tracker with the following features:

- Database Persistence, User Authentication
- RESTful API and a web client
- More sophisticated attributes in issue tracking, file attachments, real-time updates
- Dockerization

***License***

This project is licensed under the MIT License.

**Links from Circleci Tests**

https://app.circleci.com/pipelines/circleci/PMKrmVKcMeLYLN4ZAWvPSF/MixxMSzUixT5Ap1GdSpFR8/17/workflows/50d909cf-6753-407d-b258-e848e0d91251/jobs/17

# Test Coverage Report

## Running Tests with Coverage
To measure test coverage and generate a browsable report, run:

```sh
pytest --cov=src --cov-report=html
```

# Authors
- William Zhou
- Yize Liu