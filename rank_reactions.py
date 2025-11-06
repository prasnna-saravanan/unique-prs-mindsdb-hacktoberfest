"""
MindsDB Hacktoberfest 2025 - PR Reaction Ranking Script

Usage:
1️⃣ Add your name and PR issue numbers (from mindsdb/mindsdb and mindsdb/examples) in ISSUE_MAP.
2️⃣ Insert your GitHub Personal Access Token (optional, for higher rate limits).
3️⃣ Run the script, it will fetch all reactions from both repos, deduplicate by user, and print the final leaderboard.

Example:
    "vigbav36": (11799, 4),
    "Aashish079": (11812, 7),
    "k0msenapati": (11801, 2),
"""

import os
from collections import defaultdict

import requests

# ---------------- CONFIGURATION ----------------
ISSUE_MAP = {
    # "submitter_name": (mindsdb_issue_id, examples_issue_id),
    "vigbav36": (11799, 4),
    "Aashish079": (11812, 7),
    "k0msenapati": (11801, 2),
    "krishThakur": (11841, None),
}

REPOS = {"mindsdb": "mindsdb/mindsdb", "examples": "mindsdb/examples"}
# ------------------------------------------------


def get_all_reactions(repo_full_name, issue_number):
    """Paginate through reactions for a given issue."""
    reactions = []
    page = 1
    while True:
        url = f"https://api.github.com/repos/{repo_full_name}/issues/{issue_number}/reactions?per_page=100&page={page}"

        resp = requests.get(url, headers=HEADERS)
        resp.raise_for_status()
        data = resp.json()

        reactions.extend(data)
        if len(data) < 100:
            break
        page += 1
    return reactions


def deduplicate_reactions(all_reactions):
    """Deduplicate by unique user ID (max one reaction per user)."""
    unique_users = {}
    for reaction in all_reactions:
        uid = reaction["user"]["id"]
        if uid not in unique_users:
            unique_users[uid] = reaction
    return list(unique_users.values())


def count_reactions(submitter, reactions):
    """Count total unique reactions for ranking."""
    unique_reactors = {r["user"]["login"] for r in reactions}
    return len(unique_reactors)


def main():
    ranking = defaultdict(int)
    all_data = {}

    for submitter, (mindsdb_issue, examples_issue) in ISSUE_MAP.items():
        all_reactions = []

        # Fetch both issues' reactions
        for repo_key, issue_number in [
            ("mindsdb", mindsdb_issue),
            ("examples", examples_issue),
        ]:
            if issue_number:
                repo_name = REPOS[repo_key]
                print(f"Fetching {repo_name} #{issue_number} for {submitter}")
                try:
                    repo_reactions = get_all_reactions(repo_name, issue_number)
                    all_reactions.extend(repo_reactions)
                except Exception as e:
                    print(f"Error fetching for {submitter}: {e}")

        # Deduplicate per user across both repos
        deduped = deduplicate_reactions(all_reactions)
        score = count_reactions(submitter, deduped)
        ranking[submitter] = score
        all_data[submitter] = deduped

    # Sort and print ranking
    sorted_ranking = sorted(ranking.items(), key=lambda x: x[1], reverse=True)
    print("\n===== FINAL RANKING =====")
    for i, (name, score) in enumerate(sorted_ranking, 1):
        print(f"{i}. {name}: {score} unique reactions")

    return all_data, sorted_ranking


if __name__ == "__main__":
    if os.getenv("GITHUB_TOKEN"):
        HEADERS = {
            "Accept": "application/vnd.github+json",
            "Authorization": f"token {os.getenv('GITHUB_TOKEN')}",  # Uncomment and add token if needed
        }
    else:
        HEADERS = {
            "Accept": "application/vnd.github+json",
        }
    all_data, sorted_ranking = main()
