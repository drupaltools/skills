---
name: drupaltools-patch
description: Apply a patch to a Drupal contrib module or theme from any source — a URL, a Drupal.org issue, an issue comment, a GitLab merge request, a git commit hash, a local file, or a natural language description. Use this skill whenever the user wants to patch a Drupal contrib project, mentions a Drupal.org issue number, a merge request, a patch file URL, or says "apply this patch", "patch this module", "fix this issue locally", or "add this patch to composer.json".
---

# Drupal Patch

Apply a patch to a Drupal contrib project from any source.

## Step 1 — Identify the target module

Derive the module machine name from context in this order:

1. **Selected code or file** — walk up to the nearest `*.info.yml` using the `drupal-module-info` skill. The filename stem is the machine name.
2. **Selected folder** — same as above.
3. **Selected composer.json line** — extract from `"drupal/<machine_name>"` pattern.
4. **Natural language** — if the user named the module explicitly, use that.
5. **Not found** — ask the user: "Which module should the patch be applied to?"

Once identified, locate the module directory:
```bash
find web/modules/contrib -maxdepth 1 -type d -name "<machine_name>" | head -1
# Also try docroot/ or html/ if web/ not found
```

Store as `$MODULE_DIR`.

## Step 2 — Get the patch

Identify the patch source from the user prompt and follow the matching path below.

---

### Source A — Direct URL
User provides a URL ending in `.patch` or `.diff`.

```bash
curl -L -o /tmp/<machine_name>.patch "<URL>"
```

---

### Source B — Git commit hash
User provides a commit hash for the module.

Check if `$MODULE_DIR` has a `.git` folder:
```bash
[ -d "$MODULE_DIR/.git" ] && echo "git repo"
```

If yes:
```bash
cd "$MODULE_DIR" && git format-patch -1 <HASH> --stdout > /tmp/<machine_name>.patch
```

If no, generate a diff patch from drupalcode.org:
```
https://git.drupalcode.org/project/<machine_name>/-/commit/<HASH>.diff
```

---

### Source C — Drupal.org issue ID
User provides an issue number or URL like `https://www.drupal.org/node/<issue_number>`.

Fetch the issue page and find patch attachments:
```bash
curl -sS "https://www.drupal.org/node/<issue_number>" | \
  grep -oE 'https://[^"]+\.patch' | tail -1
```

If no `.patch` found, look for a GitLab MR link on the page (see Source E).

Store the latest patch URL and download it:
```bash
curl -L -o /tmp/<machine_name>.patch "<PATCH_URL>"
```

---

### Source D — Drupal.org issue comment
User provides a comment URL like `https://www.drupal.org/project/.../issues/<issue>#comment-<id>`.

Fetch the specific comment and extract its patch attachment:
```bash
curl -sS "<COMMENT_URL>" | grep -oE 'https://[^"]+\.patch' | head -1
```

Download the patch as in Source C.

---

### Source E — GitLab merge request number
User provides an MR number (e.g. `15137`) or full URL.

Construct the diff URL:
```
https://git.drupalcode.org/project/<machine_name>/-/merge_requests/<MR_NUMBER>/diffs.patch
```

```bash
curl -L -o /tmp/<machine_name>.patch \
  "https://git.drupalcode.org/project/<machine_name>/-/merge_requests/<MR_NUMBER>/diffs.patch"
```

---

### Source F — Local file changes (IDE or git)

Try in order:

**PHPStorm MCP** — if available, request a diff of uncommitted changes in `$MODULE_DIR` from the MCP and save to `/tmp/<machine_name>.patch`.

**Git CLI fallback:**
```bash
cd "$MODULE_DIR" && git diff > /tmp/<machine_name>.patch
# Or for staged changes:
cd "$MODULE_DIR" && git diff --cached > /tmp/<machine_name>.patch
```

---

### Source G — Natural language
Parse the user's description to extract one of the above source types:

| Phrase pattern | Maps to |
|---------------|---------|
| "latest patch from issue 12345" | Source C, issue 12345, latest patch |
| "patch from comment 6789 on issue 12345" | Source D |
| "patch that solves 12345" | Source C, issue 12345 |
| "MR 456 for <module>" | Source E |
| "commit abc123" | Source B |

Once identified, proceed with the matching source above.

---

Store the final patch file path as `$PATCH_PATH`. If the patch could not be obtained, tell the user and stop.

## Step 3 — Offer dry-run

Before applying, always offer:

"Patch ready at `$PATCH_PATH`. Run a dry-run first to check for conflicts?"

If yes, or no response implies yes, run:

```bash
# For git repos
git apply --summary "$PATCH_PATH"

# For non-git
patch --dry-run -p1 < "$PATCH_PATH"
```

Show the dry-run output. If it is clean, confirm with the user before applying for real. If it has conflicts, skip straight to Step 5.

## Step 4 — Apply the patch

Choose the method by priority:

### Priority 1 — Module is a git repo (`$MODULE_DIR/.git` exists)

First check if the `drupalorg` CLI is available:
```bash
which drupalorg 2>/dev/null && echo "available"
```

If available and the patch source is a Drupal.org issue or MR, prefer `drupalorg` over `git apply`:
```bash
# From an issue number
drupalorg patch:apply <issue_number> --directory="$MODULE_DIR"

# From a specific MR
drupalorg patch:apply --mr=<MR_NUMBER> --directory="$MODULE_DIR"
```

If `drupalorg` is not available, or the patch source is a local file or direct URL, fall back to:
```bash
cd "$MODULE_DIR" && git apply "$PATCH_PATH"
```

### Priority 2 — Project uses cweagans/composer-patches
Check:
```bash
grep -q "cweagans/composer-patches" composer.json && echo "yes"
```

If yes, add to `composer.json` under `extra.patches`:
```json
{
  "extra": {
    "patches": {
      "drupal/<machine_name>": {
        "https://dgo.to/<issue_number> | <description>": "<PATCH_URL>"
      }
    }
  }
}
```

Use the pattern `https://dgo.to/<issue_number> | <description>` as the key. If there is no issue number, use the patch URL or a short description as the key.

Then apply:
```bash
ddev composer install
```

### Priority 3 — Raw patch command
```bash
cd "$MODULE_DIR" && patch -p1 < "$PATCH_PATH"
```

## Step 5 — Report

Show the stdout/stderr from the apply command and state clearly:

- **OK** — patch applied cleanly. State which method was used and which files were modified.
- **ERROR** — show the exact error lines from stderr.

## Step 6 — Error diagnosis

If the apply failed, identify the cause:

| Symptom in stderr | Likely cause |
|------------------|-------------|
| `error: patch does not apply` | Version mismatch between local code and patch |
| `Hunk #N FAILED` | Line number mismatch — patch is for a different revision |
| `No such file or directory` | File was moved or renamed in the local copy |
| `already applied` | Patch was applied previously |
| Other | Show raw stderr and label as unknown |

## Step 7 — Retry with alternative patches

If the error is a version or line mismatch, and the source was a Drupal.org issue (Source C or D):

1. Fetch all patch URLs from the issue page:
```bash
curl -sS "https://www.drupal.org/node/<issue_number>" | \
  grep -oE 'https://[^"]+\.patch'
```

2. Try each patch from newest to oldest, repeating Steps 3–5 for each.
3. Stop at the first one that applies cleanly.
4. If none apply, proceed to Step 8.

## Step 8 — Offer to fix the patch

If all patches fail, offer:

"No patch applied cleanly. I can attempt minor adjustments to the patch (line number offsets, context line fixes) so it applies to your local version. Proceed?"

If yes:
- Show a diff between what the patch expects and what the local file contains.
- Propose specific line changes.
- Ask for confirmation before modifying the patch file.
- Re-run Step 3 (dry-run) with the modified patch before applying.

## Related skills

The following skills may be available alongside this one. Use them when relevant:

| Skill | When to use |
|-------|------------|
| `drupalorg-cli` | General `drupalorg` CLI usage reference — check here if unsure of a command |
| `drupalorg-issue-search` | Search for Drupal.org issues when the user gives a keyword instead of an issue number |
| `drupalorg-issue-summary-update` | Update the issue summary after a patch is applied or a fix is confirmed |
| `drupalorg-work-on-issue` | Full issue workflow — use when the user wants to not just apply but actively work on an issue |

## Notes

- Patch key format in composer.json: always `"https://dgo.to/<issue_number> | Description"` when an issue number is known.
- For MR-sourced patches with no issue number, use the MR URL as the key.
- Never silently modify `composer.json` — show the diff and confirm first.
- If `ddev` is not running when needed, warn the user: "DDEV must be running. Start with `ddev start` first."
