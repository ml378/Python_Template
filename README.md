# Team 14 Template Repository
# Python Project with CI/CD Pipeline (CircleCI)

## Description

This repository contains a Python project with automated, comprehensive test coverage, unit tests, integration tests, and test coverage reports powered by CircleCI.

## Prerequisites

1. Python 3.8 or higher

2. UV for Python dependency management

## Project Setup & Installation 

Clone the repository:
```bash
git clone https://github.com/ml378/Python_Template.git
cd Python_Template
```
Install dependencies:
```bash
python -m venv venv
source venv/bin/activate
pip install uv
uv pip install -r requirements.txt
```
Run tests:
```bash
pytest --cov=src --cov-report=html
```

```bash
nose2 -v nose2_tests
```

View test coverage:
For MacOS:
```bash 
open htmlcov/index.html  
```

For Windows:
```bash 
start htmlcov\index.html
```

## The CI/CD Pipeline (CircleCI)
This project uses CircleCI, which 
- Runs unit tests (via pytest)
- Generates coverage reports (pytest-cov)
- Does Linting (via ruff)
Test results are available in CircleCI; reports are stored as Artifacts. 

## Contributing & Making a Pull Request
1. Create a new branch:
```bash
git checkout -b branch-name
```

3. Make your changes and commit them:
```bash
git add .
git commit -m "Commit message"
```

4. Push your changes and create a pull request:
```bash
git push origin pull-request-name
```

## Tech Stack

Python 3.12

Pytest

CircleCI

Coverage.py

Ruff (Linting)

Mypy (Type Checking)

UV (Dependency Management)

## License

This project is licensed under the MIT License.

## Links from Circleci Tests

https://app.circleci.com/pipelines/circleci/PMKrmVKcMeLYLN4ZAWvPSF/MixxMSzUixT5Ap1GdSpFR8/17/workflows/50d909cf-6753-407d-b258-e848e0d91251/jobs/17

# Test Coverage Report

## Running Tests with Coverage
To measure test coverage and generate a browsable report, run:

```bash
pytest --cov=src --cov-report=html
```
