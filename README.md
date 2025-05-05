# Python Issue Tracker

***Overview***

This repository is a modern Python project template with robust CI/CD capabilities. The project provides the core backend logic for an issue tracking system that support in-memory issue storage or file-based persistant storage. It allows users to create, manage, comment on, and search for issues. This project also incorporates a AI chat agent, powered by Gemini API. This chat agent is integrated into the issue tracker client, so the user can ask the AI agent to do issue management tasks. The project is built with maintainability in mind, and showcases:

- A complete issue tracking client implementation in Python
- AI-Agent enabled issue management
- End-to-end testing strategy with both unit and integration tests
- Comprehensive code quality tools and automation
- Production-ready deployment pipeline with CircleCI

***Key Features***

- Issue Management: Create issues, retrive details, update issue properties, track issue status
- AI Chat agent: User can use natural language to ask the AI agent to manage issues for them
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
uv sync
```
Now you are ready to use this project! 

# Usage Examples of AI Enabled Issue Tracker
Start the ai-enabled issue tracker client: 
```
python -m src.ai_issue_integration
```
Now, you can ask the Ai to create issue, list issues, or close issues. Please note that the only user-facing front-end now is the AI chat agent, as a part of integrating the AI into our project. 

# Features of Issue Tracker by Itself

These features are available from the issue tracker itself: 


Create an issue



Add a comment 



Update the issue 


Get issue details


Filter issues



Search issues

Close an issue

# Project Structure

```
Python_Template/
├── .circleci/
├── .github/
├── src/                # Source code for the issue tracker
│   ├── __init__.py
│   ├── issue_tracker.py
│   ├── ai_issue_integration.py # AI integration module
│   └── ...
├── tests/              # Tests for the issue tracker
│   ├── test_issue_tracker.py
│   └── ...
├── nose2_tests/        # Optional: Nose2 specific tests
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
pytest --cov=src
```

4. Submit a pull request using the provided template (.github/pull_request_template.md)

# Pull Requests

1. Use the pull request template from .github/pull_request_template/

2. Provide a clear summary of the PR.

3. Explain the motivation behind the changes.

4. Describe any testing performed to ensure correctness.

# Tech Stack

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

# Authors
- William Zhou
- Yize Liu