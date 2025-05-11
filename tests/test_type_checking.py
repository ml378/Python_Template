import unittest
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src import Comment, Issue, IssueTrackerClient


class TypeCheckingTests(unittest.TestCase):
    """Use this class to verify type annotations with mypy.

    These tests don't actually run code but serve as a place for mypy
    to validate the type correctness of our mock implementations.
    """

    def test_comment_types(self) -> None:
        comment: Comment  # noqa: F842
        # If mypy passes, the type annotations are correct
        # This doesn't execute at runtime

    def test_issue_types(self) -> None:
        issue: Issue  # noqa: F842
        # If mypy passes, the type annotations are correct

    def test_client_types(self) -> None:
        client: IssueTrackerClient  # noqa: F842
        # If mypy passes, the type annotations are correct


if __name__ == "__main__":
    unittest.main()
