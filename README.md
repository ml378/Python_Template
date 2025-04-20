    # Python Project with CI/CD Pipeline (CircleCI)

    ***Overview***

    This repository contains a Python project with automated unit tests, integration tests, and test coverage reports powered by CircleCI.The minimum viable version of this project would include a functional issue tracker client, where user could raise an issue, others will be able to comment on it, and the issues could be managed. 

    ***Features***

    1. Automated unit tests with pytest

    2. Test coverage report generated and browsable from CircleCI UI

    3. CI/CD pipeline using CircleCI

    4. Pre-commit checks with mypy and ruff

    5. Modern dependency management using uv

    6. Static analysis and formatting checks

    7. GitHub Actions for continuous integratio


    ***Prerequisites***

    1. Python 3.8 or higher

    2. UV for Python dependency management

    ***Setup & Installation***

    Clone the repository:
    ```sh
    git clone https://github.com/ml378/Python_Template.git
    cd Python_Template
    ```
    Install dependencies:
    ```sh
    python -m venv venv
    source venv/bin/activate
    pip install uv
    uv pip install -r requirements.txt
    ```
    Run tests:
    ```sh
    pytest --cov=src --cov-report=html
    ```

    ```sh
    nose2 -v nose2_tests
    ```

    View test coverage:

    ```sh open htmlcov/index.html  # macOS
    xdg-open htmlcov/index.html  # Linux
    ```

    ***CI/CD Pipeline (CircleCI)***

    ****How it Works****

    Push to GitHub → CircleCI triggers the pipeline➡️ Runs:

    1. Unit tests (pytest)

    2. Coverage report (pytest-cov)

    3. Linting (ruff)

    Test results are visible in the CircleCI "Tests" tab➡️ Coverage reports are stored as "Artifacts", browsable in CircleCI UI.

    ***View Test Coverage in CircleCI***

    1️⃣ Go to CircleCI Dashboard2️⃣ Open the latest Job Run3️⃣ Navigate to Artifacts4️⃣ Click on test-coverage/index.html to browse the report



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

