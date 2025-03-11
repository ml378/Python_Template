    # Python Project with CI/CD Pipeline (CircleCI)

    ***Overview***

    This repository contains a Python project with automated unit tests, integration tests, and test coverage reports powered by CircleCI.

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
    git clone https://github.com/JeffereyChasing/Python_Template.git
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

    ****Pass examples:****

    1. https://app.circleci.com/pipelines/circleci/67ZqchNqYFV96fgwW7SXdk/9C4m9dcUHJDbrPi91BUCAo/14/workflows/9815ba0b-0c20-44d8-9c1a-fecfeb31f857

    2. https://app.circleci.com/pipelines/circleci/67ZqchNqYFV96fgwW7SXdk/9C4m9dcUHJDbrPi91BUCAo/11/workflows/8730b599-a41f-4038-88fe-3b2eb57e05ff

    ****Fail examples:****

    1. https://app.circleci.com/pipelines/circleci/67ZqchNqYFV96fgwW7SXdk/9C4m9dcUHJDbrPi91BUCAo/6/workflows/cddd8e60-0e4d-496a-bf30-72d43a05a5d5

    2. https://app.circleci.com/pipelines/circleci/67ZqchNqYFV96fgwW7SXdk/9C4m9dcUHJDbrPi91BUCAo/8/workflows/b5407d3b-f39b-423b-a5f1-6ee09fdfbfd4

    **Links from Circleci Test Coverage Report**

    1.https://output.circle-artifacts.com/output/job/b9f869e6-aa89-4789-b353-271a6f64d992/artifacts/0/test-coverage/class_index.html


    # Test Coverage Report

    ## Running Tests with Coverage
    To measure test coverage and generate a browsable report, run:

    ```sh
    pytest --cov=src --cov-report=html
    ```

