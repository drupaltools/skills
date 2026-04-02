#!/usr/bin/env python3
"""
Drupal Contrib Code Search CLI
Search Drupal contributed modules on git.drupalcode.org using the GitLab API.

Usage:
    ./dsearch.py "WebformSubmissionInterface"
    ./dsearch.py "hook_form_alter" --limit 5
    ./dsearch.py "EntityTypeManager" --json
    ./dsearch.py "path:src/Plugin/Block/" --extension php
"""

import argparse
import json
import os
import sys
from pathlib import Path
from urllib.parse import quote

try:
    import requests
except ImportError:
    print("Error: requests module required. Install with: pip install requests")
    sys.exit(1)


# Colors for terminal output
class Colors:
    CYAN = "\033[96m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    MAGENTA = "\033[95m"
    RED = "\033[91m"
    BOLD = "\033[1m"
    END = "\033[0m"


def load_token():
    """Load GitLab token from .env file."""
    # Resolve symlink to get the actual script directory
    script_path = Path(__file__).resolve().parent
    env_path = script_path / ".env"
    if not env_path.exists():
        print(f"{Colors.RED}Error: .env file not found at {env_path}{Colors.END}")
        sys.exit(1)

    with open(env_path) as f:
        for line in f:
            if line.startswith("DRUPALORG_GITLAB_TOKEN="):
                return line.strip().split("=", 1)[1]

    print(f"{Colors.RED}Error: DRUPALORG_GITLAB_TOKEN not found in .env{Colors.END}")
    sys.exit(1)


def search_api(token, term, page=1, per_page=100, extension=None):
    """Search GitLab API for code snippets."""
    exclusions = "-path:web/* -path:core/* -path:docroot -path:modules/contrib/*"
    search_term = f"{term} {exclusions}"
    if extension:
        search_term += f" extension:{extension}"

    encoded_term = quote(search_term, safe='')

    url = (
        f"https://git.drupalcode.org/api/v4/groups/2/search"
        f"?scope=blobs&search={encoded_term}&per_page={per_page}&page={page}"
    )

    headers = {"PRIVATE-TOKEN": token}
    response = requests.get(url, headers=headers)

    if response.status_code == 401:
        print(f"{Colors.RED}Error: Token invalid or expired.{Colors.END}")
        sys.exit(1)
    elif response.status_code == 403:
        print(f"{Colors.RED}Error: Token lacks read_api scope.{Colors.END}")
        sys.exit(1)
    elif response.status_code == 404:
        print(f"{Colors.RED}Error: Group not found - check group ID 2.{Colors.END}")
        sys.exit(1)

    return response.json()


def get_project_info(token, project_id):
    """Get project name from GitLab API."""
    url = f"https://git.drupalcode.org/api/v4/projects/{project_id}"
    headers = {"PRIVATE-TOKEN": token}
    response = requests.get(url, headers=headers)
    data = response.json()
    return data.get("path_with_namespace", data.get("name", ""))


def get_default_branch(token, project_id):
    """Get default branch name for stable URLs."""
    url = f"https://git.drupalcode.org/api/v4/projects/{project_id}/repository/branches"
    headers = {"PRIVATE-TOKEN": token}
    response = requests.get(url, headers=headers)
    branches = response.json()
    if branches and len(branches) > 0:
        return branches[0].get("name", "main")
    return "main"


def format_code_snippet(data, max_length=200):
    """Format code snippet for display."""
    if not data:
        return ""

    # Clean up the snippet
    lines = data.split("\n")[:3]
    snippet = "\n".join(lines)

    if len(snippet) > max_length:
        snippet = snippet[:max_length] + "..."

    return snippet


def print_result(result, token, show_branch=False):
    """Print a single search result with stable URL."""
    project_id = result.get("project_id")
    filename = result.get("filename")
    startline = result.get("startline")
    data = result.get("data", "")

    # Get module name
    module_name = get_project_info(token, project_id).replace("project/", "")

    # Get default branch for stable URL
    if show_branch:
        branch = get_default_branch(token, project_id)
        ref_part = branch
    else:
        ref_part = result.get("ref", "master")

    url = f"https://git.drupalcode.org/project/{module_name}/-/blob/{ref_part}/{filename}#L{startline}"

    # Print formatted result
    print(f"\n{Colors.BOLD}{Colors.CYAN}▸ {module_name}{Colors.END}")
    print(f"  {Colors.BLUE}File:{Colors.END} {filename}:{startline}")
    print(f"  {Colors.GREEN}Link:{Colors.END} {url}")

    snippet = format_code_snippet(data)
    if snippet:
        print(f"  {Colors.YELLOW}Code:{Colors.END}")
        for line in snippet.split("\n"):
            print(f"    {line}")


def print_json(results, token):
    """Print results as JSON."""
    output = []
    for result in results:
        project_id = result.get("project_id")
        module_name = get_project_info(token, project_id).replace("project/", "")
        branch = get_default_branch(token, project_id)

        output.append({
            "module": module_name,
            "branch": branch,
            "file": result.get("filename"),
            "line": result.get("startline"),
            "url": f"https://git.drupalcode.org/project/{module_name}/-/blob/{branch}/{result.get('filename')}#L{result.get('startline')}",
            "snippet": format_code_snippet(result.get("data", ""))
        })

    print(json.dumps(output, indent=2))


def main():
    parser = argparse.ArgumentParser(
        description="Search Drupal contributed modules on git.drupalcode.org",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s "WebformSubmissionInterface"
  %(prog)s "hook_form_alter" --limit 5
  %(prog)s "EntityTypeManager" --json
  %(prog)s "path:src/Plugin/Block/" --extension php
  %(prog)s "implements TokenInterface" --limit 3 --no-branch
        """
    )

    parser.add_argument("term", help="Search term")
    parser.add_argument("--limit", "-n", type=int, default=5, help="Number of results to show (default: 5)")
    parser.add_argument("--extension", "-e", help="Filter by file extension")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    parser.add_argument("--no-branch", action="store_true", help="Use commit hash instead of branch (faster, unstable URLs)")
    parser.add_argument("--all", "-a", action="store_true", help="Show all results (up to 100)")

    args = parser.parse_args()

    if not args.term.strip():
        print(f"{Colors.RED}Error: Search term cannot be empty.{Colors.END}")
        sys.exit(1)

    # Load token
    token = load_token()

    # Search
    print(f"{Colors.BOLD}Searching for: {args.term}{Colors.END}\n")

    results = search_api(token, args.term, extension=args.extension)

    if not results:
        print(f"{Colors.YELLOW}No results found. Try a broader or different term.{Colors.END}")
        sys.exit(0)

    # Limit results
    limit = 100 if args.all else args.limit
    results = results[:limit]

    print(f"Found {len(results)} results:\n")

    # Print results
    if args.json:
        print_json(results, token)
    else:
        for i, result in enumerate(results, 1):
            print(f"{Colors.MAGENTA}[{i}]{Colors.END}", end="")
            print_result(result, token, show_branch=not args.no_branch)

    print(f"\n{Colors.BOLD}Total: {len(results)} result(s){Colors.END}")


if __name__ == "__main__":
    main()
