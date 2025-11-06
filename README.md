# MindsDB Hacktoberfest 2025 — Reaction Ranking Script

This script helps the community fairly aggregate reactions for Hacktoberfest PRs after they were moved from the main `mindsdb/mindsdb` repo to `mindsdb/examples`.

## Features

- Combines reactions from both repos
- Handles pagination & deduplication per user
- Outputs a clean leaderboard
- Easy to extend — just add your name and PR IDs in `ISSUE_MAP`

## Usage

### Configuration

1. Open `rank_reactions.py`
2. Add your name and PR issue numbers in the `ISSUE_MAP` dictionary:

```python
ISSUE_MAP = {
    "your_username": (mindsdb_issue_number, examples_issue_number),
    "Aashish079": (11812, 7),
    "k0msenapati": (11801, 2),
}
```

3. (Optional) Add your GitHub Personal Access Token for higher rate limits:

```python
HEADERS = {
    "Accept": "application/vnd.github.squirrel-girl-preview+json",
    "Authorization": f"token YOUR_GITHUB_TOKEN"
}
```

### Run the Script

```bash
python3 rank_reactions.py
```

## Output

The script will:
1. Fetch all reactions from both `mindsdb/mindsdb` and `mindsdb/examples` repos
2. Deduplicate reactions by user (one reaction per user across both repos)
3. Display a ranked leaderboard

Example output:

```
Fetching mindsdb/mindsdb #11812 for Aashish079
Fetching mindsdb/examples #7 for Aashish079
Fetching mindsdb/mindsdb #11801 for k0msenapati
Fetching mindsdb/examples #2 for k0msenapati

===== FINAL RANKING =====
1. Aashish079: 121 unique reactions
2. k0msenapati: 56 unique reactions
```

## How It Works

1. **Pagination**: Fetches all reactions from GitHub API (100 per page)
2. **Deduplication**: Ensures each user is counted only once across both repos
3. **Ranking**: Counts unique reactors per submitter and sorts by total


