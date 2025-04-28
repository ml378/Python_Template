# Python Project with CI/CD Pipeline (CircleCI)

***Overview***

This repository provides a modern Python project template with robust CI/CD capabilities. It implements a functional issue tracking system that allows users to create, comment on, and manage issues effectively. Built with industry best practices, this template showcases:

- A complete issue tracking client implementation in Python
- End-to-end testing strategy with both unit and integration tests
- Comprehensive code quality tools and automation
- Production-ready deployment pipeline with CircleCI

***Features***

1. Automated unit tests with pytest

2. Test coverage report generated and browsable from CircleCI UI

3. CI/CD pipeline using CircleCI

4. Pre-commit checks with mypy and ruff

5. Modern dependency management using uv

6. Static analysis and formatting checks

7. GitHub Actions for continuous integration

   - Automatic testing on push and pull requests
   - Configurable workflows for different environments
   - Parallel test execution for faster feedback

***Prerequisites***

1. Python 3.8 or higher
2. UV for Python dependency management
3. Git installed on your system
4. A GitHub account for accessing the repository
5. CircleCI account (for viewing CI/CD pipeline results)

***Setup & Installation***

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

***Project Structure***

```
Python_Template/
├── .circleci/          # CircleCI configuration
├── .github/            # GitHub templates and workflows
├── src/                # Source code for the issue tracker
│   ├── __init__.py
│   └── ...
├── tests/              # Pytest test files
├── nose2_tests/        # Nose2 test files
├── .pre-commit-config.yaml
├── pyproject.toml      # Project configuration
├── requirements.txt    # Project dependencies
└── README.md           # This file
```

***Development Workflow***

1. Create a new branch for your feature or bugfix
2. Make your changes and write tests
3. Run tests locally to ensure everything passes
4. Submit a pull request for review

***Usage Examples***

Issue Tracker Client Usage:
```python
from src.issue_tracker import IssueTracker

# Initialize the client
tracker = IssueTracker(project_id="my-project")

# Create a new issue
issue = tracker.create_issue(
    title="Bug: Application crashes on startup",
    description="When launching the app on Windows, it crashes immediately",
    priority="high"
)

# Add a comment to an issue
tracker.add_comment(issue_id=issue.id, text="I can reproduce this on Windows 11")

# Close an issue
tracker.close_issue(issue_id=issue.id, resolution="fixed")
```

***Pull Requests***

1. Use the pull request template from .github/pull_request_template/

2. Provide a clear summary of the PR.

3. Explain the motivation behind the changes.

4. Describe any testing performed to ensure correctness.



***Tech Stack***

Python 3.12

Pytest

CircleCI

Coverage.py

Ruff (Linting)

Mypy (Type Checking)

UV (Dependency Management)

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

