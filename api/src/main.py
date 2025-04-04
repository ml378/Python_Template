from issue_tracker import GitHubAPI, TrelloAPI, IssueSyncManager, TrelloCard

GITHUB_TOKEN = "your_token"
TRELLO_KEY = "your_key"
TRELLO_TOKEN = "your_token"
OWNER = "your_username"
REPO = "your_repo"
TRELLO_LIST_ID = "your_list_id"

if __name__ == "__main__":
    github = GitHubAPI(GITHUB_TOKEN)
    trello = TrelloAPI(TRELLO_KEY, TRELLO_TOKEN)
    sync = IssueSyncManager(github, trello)

    sync.sync_issues_to_trello(OWNER, REPO, TRELLO_LIST_ID)
