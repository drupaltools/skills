#!/usr/bin/env python3
"""Parse D.O. GitLab blame API JSON and print commit details."""

import sys
import json
import re
import urllib.request
import urllib.parse


def parse_issue_url(title):
    """Extract Drupal.org issue URL from commit title like 'Issue #2191395 ...'."""
    semantic = r"(?:chore|feat|fix|docs|perf|refactor|style|task|test)\w*(?:\([^)]*\))?\s*:\s*#"
    m = re.search(rf"(?:Issue\s+#|{semantic})(\d+)", title, re.IGNORECASE)
    return f"https://www.drupal.org/i/{m.group(1)}" if m else None


def parse_contributors(title):
    """Extract Drupal.org user links from 'by user1, user2' in commit title."""
    m = re.search(r"\bby\s+([\w\s,.-]+?)(?::|$)", title)
    if not m:
        return []
    names = [n.strip() for n in m.group(1).split(",") if n.strip()]
    return [f"dgo.re/@{n}" for n in names]


def main():
    if len(sys.argv) != 4:
        print(f"Usage: {sys.argv[0]} <project> <encoded_path> <version>", file=sys.stderr)
        sys.exit(1)

    project, encoded_path, version = sys.argv[1], sys.argv[2], sys.argv[3]

    url = (
        f"https://git.drupalcode.org/api/v4/projects/"
        f"project%2F{project}/repository/files/"
        f"{encoded_path}/blame?ref={version}"
    )

    with urllib.request.urlopen(url) as resp:
        data = json.loads(resp.read().decode())

    line_num = 1
    commits = {}
    for entry in data:
        commit = entry["commit"]
        cid = commit["id"]
        start = line_num
        end = line_num + len(entry["lines"]) - 1
        if cid not in commits:
            commits[cid] = {
                "title": commit["message"].strip().split("\n")[0],
                "author": commit["author_name"],
                "date": commit["committed_date"][:10],
                "sha": cid,
                "lines": [],
            }
        commits[cid]["lines"].append(f"{start}-{end}" if start != end else str(start))
        line_num = end + 1

    for cid, c in commits.items():
        print(f"Commit: {c['title']}")
        print(f"Author: {c['author']}")
        print(f"Date:   {c['date']}")
        print(f"URL:    https://git.drupalcode.org/project/{project}/-/commit/{cid}")
        issue = parse_issue_url(c["title"])
        if issue:
            print(f"Issue:  {issue}")
        contributors = parse_contributors(c["title"])
        if contributors:
            print(f"Drupal.org: {', '.join(contributors)}")
        print(f"Lines:  {', '.join(c['lines'])}")
        print()


if __name__ == "__main__":
    main()
