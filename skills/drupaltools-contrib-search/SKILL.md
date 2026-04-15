---
name: drupaltools-contrib-search
description: Search the source code of Drupal contributed modules and core via the tresbien.tech code search API. Use this skill whenever the user wants to find code examples, usage patterns, or implementations across Drupal projects - e.g. "find examples of hook_form_alter", "which modules use a specific class", "show me how modules implement X". Unlike drupaltools-code-search, this searches an indexed mirror that includes Drupal core and popular contrib modules with faster response times and no authentication required.
---

# Drupal Contrib Code Search (tresbien.tech)

Search Drupal source code using the tresbien.tech code search engine. This service indexes Drupal core and popular contributed modules, providing fast regex-based code search without authentication.

## Base URLs

- Web UI: `https://search.tresbien.tech`
- API: `https://api.tresbien.tech/v1/search`

## Base search URL

```
https://api.tresbien.tech/v1/search?q=<QUERY>&num=10&context=3
```

Parameters:
- `q` (required) — Search query (regex, see syntax below)
- `num` (optional) — Maximum number of file results to return
- `context` (optional) — Number of context lines before/after each match
- `maxmatches` (optional) — Stop after this many total matches
- `chunks` (optional, default: true) — Set `false` for LineMatches format

## Input validation

Before building the search URL:

1. **Empty term** — refuse and ask for a search term.
2. **URL-encode the query** — spaces become `+`, regex special chars like `(`, `)`, `.`, `$` must be escaped with `\` when used literally.
3. **Response validation** — if the API returns `"FilesSkipped": true` for all shards or an empty result set, report: "No results found. Try a broader or different term."

## Search syntax

Queries are regex by default. The syntax differs from GitLab code search:

### Text Search

| Pattern | Meaning |
|---------|---------|
| `foo bar` | Files containing both "foo" and "bar" |
| `"foo bar"` | Files containing the exact phrase "foo bar" |
| `foo OR bar` | Files containing "foo" or "bar" |
| `foo -bar` | Files containing "foo" but not "bar" |

### Field Filters

| Field | Example | Meaning |
|-------|---------|---------|
| `r:` or `repo:` | `r:webform` | Restrict to repos matching "webform" |
| | `r:^(webform\|token)$` | Restrict to multiple specific repos |
| `f:` or `file:` | `f:\.module$` | Restrict to file paths matching pattern |
| `lang:` | `lang:php` | Restrict to files of a specific language |
| `b:` or `branch:` | `b:main` | Restrict to a specific branch |
| `case:yes` | `case:yes Foo` | Case-sensitive search |
| `sym:` | `sym:className` | Search symbol definitions |

### Regex

Queries are regex by default. Special characters (`.`, `(`, `)`, `{`, etc.) must be escaped with `\`.

**Examples:**
- `hook_\w+_alter` — matches hook_form_alter, hook_node_alter, etc.
- `function\s+mymodule_` — matches function declarations in mymodule
- `once\(` — literal search for `once(` (parenthesis escaped)
- `\$form_state` — literal `$form_state` (dollar sign escaped)

### Important: Always Batch Queries

**Never loop over individual repos.** Always query multiple repositories in a **single call** using `r:^(repo1|repo2|repo3)$` regex alternation:

`/v1/search?q=hook_help+r:^(webform|token|pathauto)$&num=10`

**Bad** — 3 separate requests:
- `/v1/search?q=hook_help+r:webform`
- `/v1/search?q=hook_help+r:token`
- `/v1/search?q=hook_help+r:pathauto`

**Good** — 1 batched request:
- `/v1/search?q=hook_help+r:^(webform|token|pathauto)$`

## Common search patterns with example URLs

### Find all uses of a hook
```
hook_form_alter
```
URL: `https://api.tresbien.tech/v1/search?q=hook_form_alter&num=10&context=3`

### Find implementations of a specific interface (PHP only)
```
implements\s+TokenInterface lang:php
```
URL: `https://api.tresbien.tech/v1/search?q=implements%5Cs%2BTokenInterface%20lang:php&num=10&context=3`

### Find a service definition in YAML
```
"my_module.service" lang:yaml
```
URL: `https://api.tresbien.tech/v1/search?q=%22my_module.service%22%20lang:yaml&num=10&context=3`

### Find Block plugins in specific repos
```
class.*Block lang:php r:^(webform|block_field)$
```
URL: `https://api.tresbien.tech/v1/search?q=class.*Block%20lang:php%20r:%5E(webform%7Cblock_field)%24&num=10&context=3`

### Find routing files that reference a specific controller
```
_controller f:\.routing\.yml$
```
URL: `https://api.tresbien.tech/v1/search?q=_controller%20f:%5C.routing%5C.yml%24&num=10&context=3`

### Find modules using a specific Composer package
```
symfony/http-foundation f:composer\.json$
```
URL: `https://api.tresbien.tech/v1/search?q=symfony/http-foundation%20f:composer%5C.json%24&num=10&context=3`

### Search symbol definitions
```
sym:WebformSubmissionInterface
```
URL: `https://api.tresbien.tech/v1/search?q=sym:WebformSubmissionInterface&num=10`

### OR search: two alternative hooks
```
hook_install OR hook_uninstall
```
URL: `https://api.tresbien.tech/v1/search?q=hook_install%20OR%20hook_uninstall&num=10&context=3`

## Listing indexed repositories

```
https://api.tresbien.tech/v1/search/repo
```

For specific repos:
```
https://api.tresbien.tech/v1/search/repo?q=r:^(webform|token|pathauto)$
```

Each repo entry includes:
- `Repository.Name` — repo name
- `Repository.URL` — source URL (e.g., git.drupalcode.org)
- `Repository.RawConfig.drupal-core` — Drupal core compatibility
- `Repository.RawConfig.drupal-usage` — install count
- `Repository.Branches` — indexed branches

## Response Structure

### ChunkMatches (default)

```json
{
  "Result": {
    "Files": [
      {
        "Repository": "webform",
        "FileName": "webform.module",
        "Branches": ["10.5.x", "10.6.x"],
        "ChunkMatches": [
          {
            "Content": "<base64-encoded chunk content>",
            "ContentStart": {
              "ByteOffset": 1223,
              "LineNumber": 35,
              "Column": 1
            },
            "Ranges": [
              {
                "Start": { "ByteOffset": 1237, "LineNumber": 35, "Column": 15 },
                "End": { "ByteOffset": 1246, "LineNumber": 35, "Column": 24 }
              }
            ]
          }
        ]
      }
    ],
    "MatchCount": 150,
    "FileCount": 12
  }
}
```

> `Content` is **base64-encoded**. Decode it to get the actual source code snippet.

### LineMatches (`chunks=false`)

Legacy format with one entry per matched line. `Line` values are also **base64-encoded**.

## Presenting results

For each result, construct a human-readable link:

```
https://git.drupalcode.org/project/<REPO_NAME>/-/blob/<BRANCH>/<FILENAME>#L<LINE_NUMBER>
```

Use the `Repository.Branches` field from the response to pick a stable branch. The web UI at `https://search.tresbien.tech` can also be linked directly for interactive browsing.

Always show the user:
1. The repository name and file path.
2. The line number and branch.
3. The decoded code snippet.
4. A direct link to the file on git.drupalcode.org or search.tresbien.tech.

## Performance notes

- This API is typically faster than the GitLab API since it searches a pre-built index.
- No authentication token is required.
- Results may not include very small or newly created contrib modules.
- For the most up-to-date results, fall back to `drupaltools-code-search` (GitLab API).

---

## CLI Tool

A Python CLI tool `csearch.py` is available for quick searches without invoking this skill.

### Usage

```bash
# Basic search
./csearch.py "hook_form_alter"

# Limit results
./csearch.py "EntityTypeManager" --limit 5

# Filter by language
./csearch.py "implements TokenInterface" --lang php

# Include context lines
./csearch.py "hook_help" --context 5

# Output as JSON
./csearch.py "WebformHandler" --json

# Use LineMatches format (faster for simple line searches)
./csearch.py "use Drupal" --no-chunks
```

### Requirements

```bash
pip install requests
```

The CLI tool requires no authentication and automatically:
- Decodes base64 content
- Formats output with colors
- Shows code snippets with line numbers
- Constructs clickable git.drupalcode.org links
