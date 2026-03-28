---
name: drupaltools-code-search
description: Search the source code of all Drupal contributed modules on drupal.org via the GitLab API. Use this skill whenever the user wants to find code examples, usage patterns, or implementations in Drupal contrib modules - e.g. "find examples of hook_form_alter in contrib", "which modules use a specific class or interface", "show me how contrib modules implement X". Trigger even for vague requests like "how do contrib modules do X" or "find me a real-world example of Y in Drupal".
---

# Drupal Contrib Code Search

Search all Drupal contributed modules on git.drupalcode.org using the GitLab Blobs API.

Notice that `<TERM>`` is the keywords we search for. This is the code selection I have provided.

## Base search URL

```
https://git.drupalcode.org/api/v4/groups/2/search?scope=blobs&search=<TERM>&per_page=100&page=1
```

Always append these exclusions to avoid duplicates (modules bundled inside other projects):

```
-path:web/* -path:core/* -path:docroot -path:modules/contrib/*
```

Full base command:
```bash
curl -sS \
  --header "PRIVATE-TOKEN: $DRUPALORG_GITLAB_TOKEN" \
  "https://git.drupalcode.org/api/v4/groups/2/search?scope=blobs&search=<TERM>%20-path:web/*%20-path:core/*%20-path:docroot%20-path:modules/contrib/*&per_page=100&page=1"
```

## Input validation

Before building the search URL:

1. **Empty term** - refuse and ask for a search term.
2. **Term is only Drupal core paths** (e.g. `core/lib/`) - warn the user; these are excluded by default.
3. **URL-encode the term** - spaces → `%20`, `"` → `%22`, `|` → `%7C`, `+` → `%2B`, `*` stays `*`.
4. **Response validation** - if the API returns non-200 or an empty array `[]`, report it clearly:
   - 401 → "Token invalid or expired."
   - 403 → "Token lacks read_api scope."
   - 404 → "Group not found - check group ID 2."
   - Empty array → "No results found. Try a broader or different term."

## Search syntax

| Syntax | Description | Example |
|--------|-------------|---------|
| `"exact phrase"` | Exact match | `"hook_form_alter"` |
| `~` | Fuzzy match | `EntityTypeManger~` |
| `\|` | OR | `hook_install \| hook_update_N` |
| `+` | AND (both terms required) | `plugin +annotation` |
| `-` | Exclude term | `cache -backend` |
| `*` | Wildcard / partial | `EntityType*` |
| `\` | Escape special char | `\*md` |
| `filename:` | Filter by filename pattern | `filename:*.routing.yml` |
| `path:` | Filter by repo path | `path:src/Plugin/Block/` |
| `extension:` | Filter by file extension (exact) | `extension:php` |

## Optimizations

- Prefer return URLs for a specific branch or git tag and not for a random UUID version.
For example this URL: `https://git.drupalcode.org/project/webform_views/-/blob/1ec1904a3035027cc056d46ad941db4d8b1e7a85/src/Plugin/views/field/WebformSubmissionNotesEditField.php#L7` should return the first default branch equivalent which is `https://git.drupalcode.org/project/webform_views/-/blob/8.x-5.x/src/Plugin/views/field/WebformSubmissionNotesEditField.php?ref_type=heads#L7` in this case.

## Common search patterns with example URLs

### Find all uses of a hook
```
hook_form_alter -path:web/* -path:core/* -path:docroot -path:modules/contrib/*
```
URL: `https://git.drupalcode.org/api/v4/groups/2/search?scope=blobs&search=hook_form_alter%20-path:web/*%20-path:core/*%20-path:docroot%20-path:modules/contrib/*&per_page=100&page=1`

### Find implementations of a specific interface (PHP only)
```
implements TokenInterface extension:php -path:web/* -path:core/* -path:docroot -path:modules/contrib/*
```
URL: `https://git.drupalcode.org/api/v4/groups/2/search?scope=blobs&search=implements%20TokenInterface%20extension:php%20-path:web/*%20-path:core/*%20-path:docroot%20-path:modules/contrib/*&per_page=100&page=1`

### Find a service definition in YAML
```
"my_module.service" extension:yml -path:web/* -path:core/* -path:docroot -path:modules/contrib/*
```
URL: `https://git.drupalcode.org/api/v4/groups/2/search?scope=blobs&search=%22my_module.service%22%20extension:yml%20-path:web/*%20-path:core/*%20-path:docroot%20-path:modules/contrib/*&per_page=100&page=1`

### Find Block plugins
```
path:src/Plugin/Block/ extension:php -path:web/* -path:core/* -path:docroot -path:modules/contrib/*
```
URL: `https://git.drupalcode.org/api/v4/groups/2/search?scope=blobs&search=path:src/Plugin/Block/%20extension:php%20-path:web/*%20-path:core/*%20-path:docroot%20-path:modules/contrib/*&per_page=100&page=1`

### Find routing files that reference a specific controller
```
_controller filename:*.routing.yml -path:web/* -path:core/* -path:docroot -path:modules/contrib/*
```
URL: `https://git.drupalcode.org/api/v4/groups/2/search?scope=blobs&search=_controller%20filename:*.routing.yml%20-path:web/*%20-path:core/*%20-path:docroot%20-path:modules/contrib/*&per_page=100&page=1`

### Find modules using a specific Composer package
```
symfony/http-foundation -filename:composer.lock -path:web/* -path:core/* -path:docroot -path:modules/contrib/*
```
URL: `https://git.drupalcode.org/api/v4/groups/2/search?scope=blobs&search=symfony/http-foundation%20-filename:composer.lock%20-path:web/*%20-path:core/*%20-path:docroot%20-path:modules/contrib/*&per_page=100&page=1`

### Find schema definitions for a config key
```
"field.field." filename:*.schema.yml -path:web/* -path:core/* -path:docroot -path:modules/contrib/*
```
URL: `https://git.drupalcode.org/api/v4/groups/2/search?scope=blobs&search=%22field.field.%22%20filename:*.schema.yml%20-path:web/*%20-path:core/*%20-path:docroot%20-path:modules/contrib/*&per_page=100&page=1`

### OR search: two alternative hooks
```
hook_install | hook_uninstall -path:web/* -path:core/* -path:docroot -path:modules/contrib/*
```
URL: `https://git.drupalcode.org/api/v4/groups/2/search?scope=blobs&search=hook_install%20%7C%20hook_uninstall%20-path:web/*%20-path:core/*%20-path:docroot%20-path:modules/contrib/*&per_page=100&page=1`

## Pagination

The API returns up to 100 results per page. To fetch the next page, increment `page=`:
```
&per_page=100&page=2
```
If the result count equals `per_page`, there may be more pages.

## Presenting results

Each result contains:
- `project_id` - GitLab project (module) ID
- `ref` - branch
- `filename` - file path in the repo
- `startline` - line number of the match
- `data` - snippet of matched content

Construct a human-readable link:
```
https://git.drupalcode.org/project/<MODULE_NAME>/-/blob/<REF>/<FILENAME>#L<STARTLINE>
```
To get `<MODULE_NAME>`, use:
```bash
curl -sS --header "PRIVATE-TOKEN: $DRUPALORG_GITLAB_TOKEN" "https://git.drupalcode.org/api/v4/projects/<project_id>"
```
and read the `path_with_namespace` or `name` field.

### Getting stable branch/tag URLs

The API returns commit hashes (`ref`) which create unstable URLs. To get the default branch:

```bash
curl -sS --header "PRIVATE-TOKEN: $DRUPALORG_GITLAB_TOKEN" \
  "https://git.drupalcode.org/api/v4/projects/<project_id>/repository/branches" | jq -r '.[0].name // "main"'
```

For the latest release tag:
```bash
curl -sS --header "PRIVATE-TOKEN: $DRUPALORG_GITLAB_TOKEN" \
  "https://git.drupalcode.org/api/v4/projects/<project_id>/repository/tags" | jq -r '[.[] | select(.name | test("^[0-9]"))][0].name'
```

Then construct stable URLs:
```
https://git.drupalcode.org/project/<MODULE_NAME>/-/blob/<BRANCH_OR_TAG>/<FILENAME>?ref_type=heads#L<STARTLINE>
```

Always show the user:
1. The direct full link to the file on git.drupalcode.org.
2. The matching snippet from `data`.
3. The module name (not just the project ID).

---

## CLI Tool

A Python CLI tool `dsearch.py` is available for quick searches without invoking this skill.

### Usage

```bash
# Basic search
./dsearch.py "WebformSubmissionInterface"

# Limit results
./dsearch.py "hook_form_alter" --limit 5

# Filter by file extension
./dsearch.py "EntityTypeManager" --extension php

# Output as JSON
./dsearch.py "WebformHandler" --json

# Show all results (up to 100)
./dsearch.py "FormElement" --all

# Use faster unstable URLs (commit hashes)
./dsearch.py "TokenInterface" --no-branch
```

### Requirements

```bash
pip install requests
```

The CLI tool reads `DRUPALORG_GITLAB_TOKEN` from `.env` and automatically:
- Fetches module names
- Gets default branches for stable URLs
- Formats output with colors
- Shows code snippets
