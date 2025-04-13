#Issue Tracker implementation

import requests
from typing import List

# ---------- GitHub API Classes ----------

class Task:
    def __init__(self, issue_id, title, body, url, state):
        self.id = issue_id
        self.title = title
        self.body = body
        self.url = url
        self.state = state

class GitHubAPI:
    def __init__(self, token: str):
        self.token = token
        self.headers = {
            "Authorization": f"token {self.token}",
            "Accept": "application/vnd.github+json"
        }

    def fetch_issues(self, owner: str, repo: str) -> List[Task]:
        url = f"https://api.github.com/repos/ml378/Python_Template/issues"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return [
            Task(
                issue_id=item["number"],
                title=item["title"],
                body=item.get("body", ""),
                url=item["html_url"],
                state=item["state"]
            )
            for item in response.json()
        ]

    def close_issue(self, owner: str, repo: str, issue_id: int) -> bool:
        url = f"https://api.github.com/repos/ml378/Python_Template/issues/{issue_id}"
        data = {"state": "closed"}
        response = requests.patch(url, headers=self.headers, json=data)
        return response.status_code == 200

    def comment_on_issue(self, owner: str, repo: str, issue_id: int, comment: str) -> bool:
        url = f"https://api.github.com/repos/{owner}/{repo}/issues/{issue_id}/comments"
        response = requests.post(url, headers=self.headers, json={"body": comment})
        return response.status_code == 201


# ---------- Trello Connection Classes ----------

class IssueCard:
    def __init__(self, card_id, name, desc):
        self.id = card_id
        self.name = name
        self.desc = desc

class Trello:
    def __init__(self, key: str, token: str):
        self.key = key
        self.token = token

    def create_card(self, list_id: str, card: TrelloCard) -> bool:
        url = "https://api.trello.com/1/cards"
        params = {
            "key": self.key,
            "token": self.token,
            "idList": list_id,
            "name": card.name,
            "desc": card.desc
        }
        response = requests.post(url, params=params)
        return response.status_code == 200

    def move_card_to_list(self, card_id: str, list_id: str) -> bool:
        url = f"https://api.trello.com/1/cards/{card_id}"
        params = {
            "key": self.key,
            "token": self.token,
            "idList": list_id
        }
        response = requests.put(url, params=params)
        return response.status_code == 200

    def get_cards_from_list(self, list_id: str) -> List[TrelloCard]:
        url = f"https://api.trello.com/1/lists/{list_id}/cards"
        params = {
            "key": self.key,
            "token": self.token
        }
        response = requests.get(url, params=params)
        response.raise_for_status()
        return [
            IssueCard(
                card_id=item["id"],
                name=item["name"],
                desc=item["desc"]
            )
            for item in response.json()
        ]
