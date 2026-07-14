---
name: drupaltools-phpcs
description: Run PHPCS in a Drupal project and fix the reported coding standards violations. Use this skill whenever the user asks to run phpcs, check coding standards, fix code style errors, lint PHP/Drupal code, or says things like "run phpcs and fix the errors" or "clean up my coding standards".
---

# PHPCS - Check and Fix Coding Standards

Run PHPCS in the project and resolve the violations it reports.

## When to Use

- "Run phpcs"
- "Run phpcs and fix the errors"
- "Check coding standards and fix them"
- "Lint my code with phpcs"
- "Fix the phpcs violations"

## Step 1 - Detect DDEV

The PHPCS command may need to run inside DDEV. Before running anything, make sure you are at the project root (the folder containing `vendor/`), then check whether the project uses DDEV:

```bash
[ -f .ddev/config.yaml ] && echo "uses_ddev" || echo "no_ddev"
```

- If `uses_ddev`, prefix every command in this skill with `ddev exec`.
- If `no_ddev`, run every command directly with no prefix.

```bash
# With DDEV
ddev exec vendor/bin/phpcs

# Without DDEV
vendor/bin/phpcs
```

## Step 2 - Run PHPCS

Run the command and capture the full output:

```bash
vendor/bin/phpcs
```

If PHPCS is not installed, install it first (use the same prefix from Step 1):

```bash
composer require --dev drupal/coder
```

## Step 3 - Read the violations

PHPCS groups violations per file and lists each one with a line number, severity (ERROR/WARNING), and a fixable flag:

```
FILE: src/Controller/MyController.php
FOUND 2 ERRORS AFFECTING 2 LINES
 15 | ERROR | [x] Line exceeds 80 characters
 42 | ERROR | [ ] Missing function docblock
```

`[x]` means PHPCS can auto-fix it. `[ ]` means a manual fix is required.

## Step 4 - Fix the violations

Auto-fix everything fixable first with PHPCBF (same prefix rules):

```bash
vendor/bin/phpcbf
```

Then fix the remaining `[ ]` violations manually, one file at a time. Common ones:

| Issue | How to fix |
|---|---|
| Line exceeds 80 characters | Wrap or break the line |
| Missing file docblock | Add the standard Drupal file docblock |
| Missing function docblock | Add a real docblock or `@inheritdoc` |
| Format of docblock | Match the Drupal docblock style |
| Use of tabs | Replace with 2 spaces |
| Trailing whitespace | Remove it |

For each violation, open the file at the reported line, apply the fix, and move on. Read each file before editing.

## Step 5 - Re-run until clean

Run PHPCS again. Repeat Step 4 until the run reports 0 errors. Stop when output says "No violations found" or shows a clean file list.

Finish with a short summary: files changed, errors fixed, warnings remaining.
