---
name: drupaltools-markdownlint
description: Run the project markdownlint script in a Drupal project and fix the reported markdown violations. Use this skill whenever the user asks to run markdownlint, lint markdown, check the docs, or says "run scripts/markdownlint.sh and fix the errors".
---

# Markdownlint - Run and Fix Markdown Violations

Run the project markdownlint script and resolve the violations it reports.

## When to Use

- "Run markdownlint"
- "Run scripts/markdownlint.sh and fix the errors"
- "Lint the markdown and fix it"
- "Fix the markdown lint errors"
- "Check my docs for markdown issues"

## Step 1 - Detect DDEV

The markdownlint command may need to run inside DDEV. Before running anything, make sure you are at the project root (the folder containing `scripts/markdownlint.sh`), then check whether the project uses DDEV:

```bash
[ -f .ddev/config.yaml ] && echo "uses_ddev" || echo "no_ddev"
```

- If `uses_ddev`, prefix every command in this skill with `ddev exec`.
- If `no_ddev`, run every command directly with no prefix.

```bash
# With DDEV
ddev exec scripts/markdownlint.sh

# Without DDEV
scripts/markdownlint.sh
```

## Step 2 - Inspect the wrapper script

`scripts/markdownlint.sh` is a project-specific wrapper. Read it once before running it to learn which linter it calls (`markdownlint-cli` or `markdownlint-cli2`) and which config file it uses (for example `.markdownlint.json`, `.markdownlintrc`, or `.markdownlint-cli2.jsonc`):

```bash
cat scripts/markdownlint.sh
```

## Step 3 - Run markdownlint

Run the command and capture the full output:

```bash
scripts/markdownlint.sh
```

If the underlying linter is missing, install it first (use the same prefix from Step 1). Typical installs:

```bash
npm install --save-dev markdownlint-cli2
# or
npm install --save-dev markdownlint-cli
```

## Step 4 - Read the violations

Each violation lists the file, line number, and a rule id (`MDxxx`):

```
docs/guide.md:12:81 MD013/line-length Line length
docs/guide.md:3 MD012/no-multiple-blanks Multiple consecutive blank lines
```

## Step 5 - Fix the violations

Try the auto-fix first. Pass `--fix` through the linter the script wraps (use the same prefix rules):

```bash
# markdownlint-cli2
markdownlint-cli2 --fix "**/*.md"

# markdownlint-cli
markdownlint --fix "**/*.md"
```

Then fix any remaining violations manually. Common rules:

| Rule | How to fix |
|---|---|
| MD009 trailing whitespace | Remove trailing spaces |
| MD012 multiple blank lines | Keep at most one blank line |
| MD013 line length | Wrap long lines |
| MD001 heading increment | Do not skip heading levels (for example no `#` to `###`) |
| MD025 single H1 | Keep one top-level heading per file |
| MD033 inline HTML | Remove raw HTML |
| MD040 fenced code language | Add a language to fenced code blocks |

For each violation, open the file at the reported line, apply the fix, and move on.

## Step 6 - Re-run until clean

Run `scripts/markdownlint.sh` again. Repeat Step 5 until the run reports no violations.

Finish with a short summary: files changed, violations fixed, violations remaining.
