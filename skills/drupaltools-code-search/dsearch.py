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
import sys
import urllib.parse
import urllib.request
from pathlib import Path


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


GITLAB_API = "https://git.drupalcode.org/api/v4"


def load_token():
    """Load GitLab token from .env file."""
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


def gitlab_request(path, token=None):
    """Make an authenticated GET request to the GitLab API."""
    url = f"{GITLAB_API}{path}"
    headers = {"Accept": "application/json"}
    if token:
        headers["PRIVATE-TOKEN"] = token

    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        if e.code == 401:
            print(f"{Colors.RED}Error: Token invalid or expired.{Colors.END}")
        elif e.code == 403:
            print(f"{Colors.RED}Error: Token lacks read_api scope.{Colors.END}")
        elif e.code == 404:
            print(f"{Colors.RED}Error: Resource not found.{Colors.END}")
        else:
            print(f"{Colors.RED}Error: API returned HTTP {e.code}: {body}{Colors.END}")
        sys.exit(1)
    except urllib.error.URLError as e:
        print(f"{Colors.RED}Error: Could not reach API: {e.reason}{Colors.END}")
        sys.exit(1)


def search_api(token, term, page=1, per_page=100, extension=None):
    """Search GitLab API for code snippets."""
    exclusions = "-path:web/* -path:core/* -path:docroot -path:modules/contrib/*"
    search_term = f"{term} {exclusions}"
    if extension:
        search_term += f" extension:{extension}"

    encoded_term = urllib.parse.quote(search_term, safe="")

    path = (
        f"/groups/2/search?scope=blobs&search={encoded_term}"
        f"&per_page={per_page}&page={page}"
    )
    return gitlab_request(path, token)


def get_project_info(token, project_id):
    """Get project name from GitLab API."""
    data = gitlab_request(f"/projects/{project_id}", token)
    return data.get("path_with_namespace", data.get("name", ""))


def get_default_branch(token, project_id):
    """Get default branch name for stable URLs."""
    branches = gitlab_request(f"/projects/{project_id}/repository/branches", token)
    if branches and len(branches) > 0:
        return branches[0].get("name", "main")
    return "main"


def get_latest_tag(token, project_id):
    """Get the latest release tag for stable URLs."""
    tags = gitlab_request(f"/projects/{project_id}/repository/tags", token)
    if isinstance(tags, list):
        for tag in tags:
            name = tag.get("name", "")
            if name and name[0].isdigit():
                return name
    return None


def format_code_snippet(data, max_length=200):
    """Format code snippet for display."""
    if not data:
        return ""

    lines = data.split("\n")[:3]
    snippet = "\n".join(lines)

    if len(snippet) > max_length:
        snippet = snippet[:max_length] + "..."

    return snippet


def get_stable_ref(token, project_id, fallback_ref):
    """Get a stable ref (tag > branch > fallback commit hash)."""
    tag = get_latest_tag(token, project_id)
    if tag:
        return tag, "tags"
    branch = get_default_branch(token, project_id)
    if branch:
        return branch, "heads"
    return fallback_ref, None


def print_result(result, token, show_branch=False):
    """Print a single search result with stable URL."""
    project_id = result.get("project_id")
    filename = result.get("filename")
    startline = result.get("startline")
    data = result.get("data", "")
    ref = result.get("ref", "master")

    # Get module name
    module_name = get_project_info(token, project_id).replace("project/", "")

    # Get stable ref for URL
    if show_branch:
        stable_ref, ref_type = get_stable_ref(token, project_id, ref)
        if ref_type == "tags":
            url = f"https://git.drupalcode.org/project/{module_name}/-/blob/{stable_ref}/{filename}?ref_type=tags#L{startline}"
        elif ref_type == "heads":
            url = f"https://git.drupalcode.org/project/{module_name}/-/blob/{stable_ref}/{filename}?ref_type=heads#L{startline}"
        else:
            url = f"https://git.drupalcode.org/project/{module_name}/-/blob/{stable_ref}/{filename}#L{startline}"
    else:
        url = f"https://git.drupalcode.org/project/{module_name}/-/blob/{ref}/{filename}#L{startline}"

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
        tag = get_latest_tag(token, project_id)
        branch = get_default_branch(token, project_id)
        stable_ref = tag or branch or result.get("ref", "master")

        output.append({
            "module": module_name,
            "branch": stable_ref,
            "file": result.get("filename"),
            "line": result.get("startline"),
            "url": f"https://git.drupalcode.org/project/{module_name}/-/blob/{stable_ref}/{result.get('filename')}#L{result.get('startline')}",
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
