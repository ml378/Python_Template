#ifndef ISSUE_TRACKER_CLIENT_H
#define ISSUE_TRACKER_CLIENT_H

#include <string>
#include <vector>
#include <iostream>

// ---------- GitHub API ----------

struct GitHubIssue {
    int id;
    std::string title;
    std::string body;
    std::string url;
    std::string state;
};

class GitHubAPI {
public:
    GitHubAPI(const std::string& token)
        : authToken(token) {}

    std::vector<GitHubIssue> fetchIssues(const std::string& owner, const std::string& repo) {
        // TODO: Implement HTTP GET to GitHub API
        std::cout << "Fetching issues for " << owner << "/" << repo << std::endl;
        return {}; // placeholder
    }

    bool closeIssue(const std::string& owner, const std::string& repo, int issueId) {
        // TODO: Implement HTTP PATCH to close issue
        std::cout << "Closing issue #" << issueId << " on " << owner << "/" << repo << std::endl;
        return true; // placeholder
    }

    bool commentOnIssue(const std::string& owner, const std::string& repo, int issueId, const std::string& comment) {
        // TODO: Implement HTTP POST to comment
        std::cout << "Commenting on issue #" << issueId << ": " << comment << std::endl;
        return true; // placeholder
    }

private:
    std::string authToken;
};

// ---------- Trello API ----------

struct TrelloCard {
    std::string id;
    std::string name;
    std::string desc;
};

class TrelloAPI {
public:
    TrelloAPI(const std::string& key, const std::string& token)
        : apiKey(key), apiToken(token) {}

    bool createCard(const std::string& listId, const TrelloCard& card) {
        // TODO: Implement HTTP POST to create card
        std::cout << "Creating Trello card: " << card.name << std::endl;
        return true; // placeholder
    }

    bool moveCardToList(const std::string& cardId, const std::string& listId) {
        // TODO: Implement HTTP PUT to move card
        std::cout << "Moving card " << cardId << " to list " << listId << std::endl;
        return true; // placeholder
    }

    std::vector<TrelloCard> getCardsFromList(const std::string& listId) {
        // TODO: Implement HTTP GET to fetch cards
        std::cout << "Fetching cards from list " << listId << std::endl;
        return {}; // placeholder
    }

private:
    std::string apiKey;
    std::string apiToken;
};

// ---------- Issue Sync Manager ----------

class IssueSyncManager {
public:
    IssueSyncManager(GitHubAPI* github, TrelloAPI* trello)
        : githubApi(github), trelloApi(trello) {}

    void syncGitHubIssuesToTrello(const std::string& owner, const std::string& repo, const std::string& listId) {
        std::vector<GitHubIssue> issues = githubApi->fetchIssues(owner, repo);
        for (const auto& issue : issues) {
            TrelloCard card;
            card.name = issue.title;
            card.desc = issue.body + "\n\nGitHub URL: " + issue.url;
            trelloApi->createCard(listId, card);
        }
    }

    void closeGitHubIssueFromTrelloCard(const std::string& cardId, const std::string& owner, const std::string& repo, int issueId) {
        bool closed = githubApi->closeIssue(owner, repo, issueId);
        if (closed) {
            std::cout << "Closed issue #" << issueId << " due to Trello card " << cardId << std::endl;
        }
    }

private:
    GitHubAPI* githubApi;
    TrelloAPI* trelloApi;
};

#endif // ISSUE_TRACKER_CLIENT_H
