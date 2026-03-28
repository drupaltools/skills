---
name: drupaltools-git-blame
description: Generate a git.drupalcode.org blame URL and fetch commit details for a code snippet from a Drupal contrib module or Drupal core. Use this skill when the user asks "who wrote this code", "git blame", "who is responsible for this line", "blame this code", or wants to see the commit history for a specific line or range in a contrib module or core file. Also trigger when the user references code from a contrib module and wants to trace its origin.
---

# Drupal Git Blame

Given a code snippet or file reference from a Drupal contrib module or Drupal core, generate the git.drupalcode.org blame URL and fetch commit details via the GitLab API.

## Step 1 — Identify the file and line numbers

- Determine the source file path containing the code snippet.
- Identify the exact line number(s) within that file.
- Format: `L11` for a single line, `L11-L15` for a range. Store as `$LINES`.
- If the file path is not provided, infer it from context (namespace, class name, module prefix) or ask the user.

## Step 2 — Identify project, version, and relative path

Use the `drupal-module-info` skill to locate the nearest `*.info.yml` above the file. Extract:

- `$MACHINE_NAME` — filename stem of the `.info.yml` (e.g. `devel`)
- `$PROJECT` — the `project:` field value; if absent walk up to the parent module's `.info.yml` (submodules inherit from their parent)
- `$VERSION` — the `version:` field value

**Drupal core files** (under `web/core` or `docroot/core`):
- `$PROJECT` = `drupal`
- `$VERSION` — from `composer show drupal/core` or `grep "const VERSION" web/core/lib/Drupal.php`

**Dev checkouts** where `version:` reads `VERSION` — inform the user that blame requires a tagged release and stop.

Compute `$RELATIVE_PATH` — the file path relative to the project root folder.
Example: `web/modules/contrib/devel/src/Foo.php` → `src/Foo.php`

Compute `$ENCODED_PATH` — URL-encode `$RELATIVE_PATH` (replace `/` with `%2F`).
Example: `src/Foo.php` → `src%2FFoo.php`

Version tag formats: `2.1.0` (Drupal 10+) or `8.x-3.4` (legacy). Use the exact string from the `.info.yml`.

## Step 3 — Build the blame browser URL

```
https://git.drupalcode.org/project/$PROJECT/-/blame/$VERSION/$RELATIVE_PATH?ref_type=tags#$LINES
```

Example:
```
https://git.drupalcode.org/project/devel/-/blame/5.4.0/src/DevelDumperPluginManagerInterface.php?ref_type=tags#L11
```

Present this URL to the user immediately as a clickable link.

## Step 4 — Fetch blame data via GitLab API

Check whether `$DRUPALORG_GITLAB_TOKEN` is set before fetching:
```bash
if [ -z "$DRUPALORG_GITLAB_TOKEN" ]; then
  echo "WARNING: No token set. API rate limits may apply. Set DRUPALORG_GITLAB_TOKEN for reliable access."
fi
```

Fetch:
```bash
curl -sS \
  ${DRUPALORG_GITLAB_TOKEN:+--header "PRIVATE-TOKEN: $DRUPALORG_GITLAB_TOKEN"} \
  "https://git.drupalcode.org/api/v4/projects/project%2F${PROJECT}/repository/files/${ENCODED_PATH}/blame?ref=${VERSION}"
```

The API returns an array. Each entry groups consecutive lines sharing the same commit:
```json
{
  "commit": {
    "id": "<sha>",
    "message": "Issue #12345 by user: Fix something\n",
    "authored_date": "2016-04-11T21:11:40.000+02:00",
    "author_name": "username"
  },
  "lines": ["line content 1", "line content 2"]
}
```

Track a running line counter (starting at 1) to map each entry's lines array to actual line numbers.

If the API returns a non-200 response:
- 401 → "Token invalid or expired."
- 403 → "Token lacks read_api scope."
- 404 → "Project or ref not found — check `$PROJECT` and `$VERSION`."

## Step 5 — Parse and filter

If `fetch-blame.py` exists at a known skill path, run it:
```bash
python3 fetch-blame.py "$PROJECT" "$ENCODED_PATH" "$VERSION"
```

Otherwise parse the JSON response directly:
- Build a line-number → commit map from the `lines` arrays.
- Filter to only commits touching the requested `$LINES` range.
- Deduplicate commits (the same commit may cover multiple lines).

## Step 6 — Output

**1. Summary table:**

| Variable       | Value |
|----------------|-------|
| `$PROJECT`     | e.g. `devel` |
| `$VERSION`     | e.g. `5.4.0` |
| `$RELATIVE_PATH` | e.g. `src/DevelDumperPluginManagerInterface.php` |
| `$LINES`       | e.g. `L11` |

**2. Blame URL** — already shown in Step 3.

**3. Commit details** for each unique commit touching the requested line range:

```
Commit: <first line of commit message>
Author: <author_name>
Date:   <YYYY-MM-DD>
URL:    https://git.drupalcode.org/project/<PROJECT>/-/commit/<sha>
Lines:  <line range(s) this commit covers>
```

If multiple commits touch the requested range, list all of them in line order.
