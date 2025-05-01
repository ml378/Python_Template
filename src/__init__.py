from .ai_client import AIConversationClient
from .issue_tracker_interface import (
    Comment,
    Issue,
    IssueTrackerClient,
    get_issue_tracker_client,
)

# Re-export the interfaces so users can still import from src.api
__all__ = [
    "AIConversationClient",
    "Comment",
    "Issue",
    "IssueTrackerClient",
    "get_issue_tracker_client",
]
