#!/usr/bin/env python3
"""
Drupal Contrib Code Search CLI (tresbien.tech)
Search Drupal source code using the tresbien.tech code search engine.

No authentication required. Searches a pre-built index of Drupal core
and popular contributed modules.

Usage:
    ./csearch.py "hook_form_alter"
    ./csearch.py "EntityTypeManager" --limit 5
    ./csearch.py "implements TokenInterface" --lang php
    ./csearch.py "hook_help" --context 3
"""

import argparse
import base64
import json
import sys
import urllib.parse
import urllib.request


API_BASE = "https://api.tresbien.tech/v1/search"
WEB_BASE = "https://search.tresbien.tech"
GITLAB_BASE = "https://git.drupalcode.org"

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


def search_api(query, num=10, context=3, maxmatches=None, chunks=True):
    """Search the tresbien.tech API."""
    params = urllib.parse.urlencode({
        "q": query,
        "num": num,
        "context": context,
        "chunks": chunks,
    })
    if maxmatches:
        params = urllib.parse.urlencode({
            "q": query,
            "num": num,
            "context": context,
            "chunks": chunks,
            "maxmatches": maxmatches,
        })

    url = f"{API_BASE}?{params}"
    req = urllib.request.Request(url)
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            if resp.status != 200:
                print(f"{Colors.RED}Error: API returned status {resp.status}{Colors.END}")
                sys.exit(1)
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        print(f"{Colors.RED}Error: API returned HTTP {e.code}{Colors.END}")
        sys.exit(1)
    except urllib.error.URLError as e:
        print(f"{Colors.RED}Error: Could not reach API: {e.reason}{Colors.END}")
        sys.exit(1)


def decode_content(b64_str):
    """Decode base64-encoded content."""
    try:
        return base64.b64decode(b64_str).decode("utf-8", errors="replace")
    except Exception:
        return b64_str


def build_gitlab_url(repo_name, filename, branch, line_number):
    """Build a clickable link to git.drupalcode.org."""
    return f"{GITLAB_BASE}/project/{repo_name}/-/blob/{branch}/{filename}#L{line_number}"


def print_file_result(file_data, index, show_all_chunks=False):
    """Print a single file result with its matches."""
    repo = file_data.get("Repository", "unknown")
    filename = file_data.get("FileName", "")
    branches = file_data.get("Branches", [])
    language = file_data.get("Language", "")
    branch = branches[0] if branches else "main"

    print(f"\n{Colors.BOLD}{Colors.MAGENTA}[{index}]{Colors.END} {Colors.BOLD}{repo}{Colors.END}")
    print(f"  {Colors.BLUE}File:{Colors.END} {filename}")
    if language:
        print(f"  {Colors.BLUE}Language:{Colors.END} {language}")
    if branches:
        print(f"  {Colors.BLUE}Branches:{Colors.END} {', '.join(branches)}")

    url = build_gitlab_url(repo, filename, branch, 0)
    print(f"  {Colors.GREEN}Link:{Colors.END} {url}")

    # Print chunk matches
    chunks_data = file_data.get("ChunkMatches", [])
    if not chunks_data:
        # Try line matches
        line_matches = file_data.get("LineMatches", [])
        for match in line_matches:
            line_num = match.get("LineNumber", 0)
            content = decode_content(match.get("Line", ""))
            print(f"\n  {Colors.YELLOW}Line {line_num}:{Colors.END}")
            for line in content.split("\n"):
                print(f"    {line}")
            if not show_all_chunks:
                break
    else:
        for i, chunk in enumerate(chunks_data):
            content_start = chunk.get("ContentStart", {})
            line_num = content_start.get("LineNumber", 0)
            content = decode_content(chunk.get("Content", ""))

            print(f"\n  {Colors.YELLOW}Match at line {line_num}:{Colors.END}")
            for line in content.split("\n"):
                print(f"    {line}")

            if not show_all_chunks and i >= 0:
                if len(chunks_data) > 1:
                    print(f"    {Colors.BLUE}... +{len(chunks_data) - 1} more match(es) in this file{Colors.END}")
                break


def print_json_output(result_data):
    """Print results as JSON."""
    files = result_data.get("Result", {}).get("Files", [])
    output = []
    for f in files:
        repo = f.get("Repository", "unknown")
        filename = f.get("FileName", "")
        branches = f.get("Branches", [])
        branch = branches[0] if branches else "main"

        matches = []
        for chunk in f.get("ChunkMatches", []):
            content_start = chunk.get("ContentStart", {})
            line_num = content_start.get("LineNumber", 0)
            content = decode_content(chunk.get("Content", ""))
            matches.append({
                "line": line_num,
                "content": content,
            })

        if not matches:
            for lm in f.get("LineMatches", []):
                line_num = lm.get("LineNumber", 0)
                content = decode_content(lm.get("Line", ""))
                matches.append({
                    "line": line_num,
                    "content": content,
                })

        output.append({
            "repository": repo,
            "file": filename,
            "branches": branches,
            "language": f.get("Language", ""),
            "url": build_gitlab_url(repo, filename, branch, 0),
            "matches": matches,
        })

    print(json.dumps(output, indent=2))


def print_stats(result_data):
    """Print search statistics."""
    result = result_data.get("Result", {})
    print(f"\n{Colors.BOLD}Search Statistics:{Colors.END}")
    print(f"  Files with matches: {result.get('FileCount', 0)}")
    print(f"  Total matches: {result.get('MatchCount', 0)}")
    print(f"  Files scanned: {result.get('FilesLoaded', 0)}")
    print(f"  Files skipped: {result.get('FilesSkipped', 0)}")


def main():
    parser = argparse.ArgumentParser(
        description="Search Drupal source code via tresbien.tech",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s "hook_form_alter"
  %(prog)s "EntityTypeManager" --limit 5
  %(prog)s "implements TokenInterface" --lang php
  %(prog)s "hook_help" --context 3
  %(prog)s "WebformHandler" --json
  %(prog)s "class.*Block" --no-chunks
        """
    )

    parser.add_argument("query", help="Search query (regex)")
    parser.add_argument("--limit", "-n", type=int, default=10, help="Number of file results (default: 10)")
    parser.add_argument("--context", "-c", type=int, default=3, help="Context lines around matches (default: 3)")
    parser.add_argument("--lang", "-l", help="Filter by language (e.g., php, yaml, twig)")
    parser.add_argument("--repo", "-r", help="Filter by repository name")
    parser.add_argument("--no-chunks", action="store_true", help="Use LineMatches format instead of ChunkMatches")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    parser.add_argument("--all-matches", "-a", action="store_true", help="Show all chunk matches per file")
    parser.add_argument("--stats", action="store_true", help="Show search statistics")
    parser.add_argument("--maxmatches", type=int, help="Stop after this many total matches")

    args = parser.parse_args()

    if not args.query.strip():
        print(f"{Colors.RED}Error: Search query cannot be empty.{Colors.END}")
        sys.exit(1)

    # Build query with language/repo filters
    query = args.query
    if args.lang:
        query += f" lang:{args.lang}"
    if args.repo:
        query += f" r:{args.repo}"

    print(f"{Colors.BOLD}Searching for: {query}{Colors.END}")
    print(f"{Colors.BLUE}Web UI: {WEB_BASE}{Colors.END}\n")

    # Search
    result_data = search_api(
        query=query,
        num=args.limit,
        context=args.context,
        maxmatches=args.maxmatches,
        chunks=not args.no_chunks,
    )

    files = result_data.get("Result", {}).get("Files", [])

    if not files:
        print(f"{Colors.YELLOW}No results found. Try a broader or different term.{Colors.END}")
        if args.stats:
            print_stats(result_data)
        sys.exit(0)

    # Print results
    if args.json:
        print_json_output(result_data)
    else:
        for i, file_data in enumerate(files, 1):
            print_file_result(file_data, i, show_all_chunks=args.all_matches)


        print(f"{Colors.BOLD}Total: {len(files)} file(s) shown{Colors.END}")

    # Print stats if requested
    if args.stats:
        print_stats(result_data)


if __name__ == "__main__":
    main()
