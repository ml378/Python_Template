# For running the issue tracker

from issue_tracker import GitHubAPI, Trello, IssueCard

GITHUB_TOKEN = "your_token"
TRELLO_KEY = "your_key"
TRELLO_TOKEN = "your_token"
OWNER = "your_username"
REPO = "your_repo"
TRELLO_LIST_ID = "your_list_id"

if __name__ == "__main__":
    github = GitHubAPI(GITHUB_TOKEN)
    trello = TrelloAPI(TRELLO_KEY, TRELLO_TOKEN)
