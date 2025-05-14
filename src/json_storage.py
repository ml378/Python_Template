"""JSON file storage implementation for the issue tracker.
Provides persistent storage of issues in a JSON file.
"""
import json
import os
import time
import uuid
from pathlib import Path
from typing import Any, Dict, List, Optional


class JsonIssueTrackerClient:
    """An issue tracker client that stores issues in a JSON file.
    
    Provides persistent storage with basic CRUD operations for tracking issues.
    """

    def __init__(self, storage_path: Optional[str] = None):
        """Initialize the JSON issue tracker client.
        
        Args:
            storage_path (str, optional): Path to the JSON storage file.
                If not provided, defaults to ~/.issue_tracker/issues.json

        """
        if storage_path is None:
            # Default to user's home directory
            storage_path = os.path.join(
                str(Path.home()),
                ".issue_tracker",
                "issues.json"
            )

        self.storage_path = storage_path
        self.issues = self._load_issues()

        # Ensure directory exists
        os.makedirs(os.path.dirname(self.storage_path), exist_ok=True)

    def _load_issues(self) -> Dict[str, Dict]:
        """Load issues from the JSON file.
        
        Returns:
            dict: Dictionary of issues with ID as key

        """
        if not os.path.exists(self.storage_path):
            return {}

        try:
            with open(self.storage_path) as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            # Return empty dict if file is empty or invalid
            return {}

    def _save_issues(self) -> None:
        """Save issues to the JSON file.
        
        Raises:
            IOError: If unable to write to the file

        """
        with open(self.storage_path, "w") as f:
            json.dump(self.issues, f, indent=2)

    def create_issue(self, title: str, description: str, **kwargs) -> Dict[str, Any]:
        """Create a new issue and save it to storage.
        
        Args:
            title (str): Title of the issue
            description (str): Detailed description of the issue
            **kwargs: Additional issue attributes
            
        Returns:
            dict: The created issue data

        """
        issue_id = str(uuid.uuid4())
        created_at = time.time()

        issue = {
            "id": issue_id,
            "title": title,
            "description": description,
            "created_at": created_at,
            "updated_at": created_at,
            "status": kwargs.get("status", "open"),
        }

        # Add any additional attributes
        for key, value in kwargs.items():
            if key not in issue:
                issue[key] = value

        self.issues[issue_id] = issue
        self._save_issues()

        return issue

    def get_issue(self, issue_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve an issue by its ID.
        
        Args:
            issue_id (str): ID of the issue to retrieve
            
        Returns:
            dict or None: The issue data if found, None otherwise

        """
        return self.issues.get(issue_id)

    def update_issue(self, issue_id: str, **kwargs) -> Optional[Dict[str, Any]]:
        """Update an existing issue.
        
        Args:
            issue_id (str): ID of the issue to update
            **kwargs: Issue attributes to update
            
        Returns:
            dict or None: The updated issue data if found, None otherwise

        """
        issue = self.issues.get(issue_id)
        if not issue:
            return None

        for key, value in kwargs.items():
            issue[key] = value

        issue["updated_at"] = time.time()
        self._save_issues()

        return issue

    def delete_issue(self, issue_id: str) -> bool:
        """Delete an issue by its ID.
        
        Args:
            issue_id (str): ID of the issue to delete
            
        Returns:
            bool: True if the issue was deleted, False if not found

        """
        if issue_id in self.issues:
            del self.issues[issue_id]
            self._save_issues()
            return True
        return False

    def list_issues(self, status: Optional[str] = None) -> List[Dict[str, Any]]:
        """List all issues, optionally filtered by status.
        
        Args:
            status (str, optional): Filter issues by this status
            
        Returns:
            list: List of issue dictionaries

        """
        issues = list(self.issues.values())

        if status:
            issues = [issue for issue in issues if issue.get("status") == status]

        # Sort by creation date, newest first
        issues.sort(key=lambda x: x.get("created_at", 0), reverse=True)

        return issues
