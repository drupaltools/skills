---
name: drupaltools-phpstan
description: Run PHPStan static analysis in a Drupal project and resolve the reported errors. Use this skill whenever the user asks to run phpstan, run static analysis, fix type errors, or says "run phpstan and fix the errors".
---

# PHPStan - Run and Fix Static Analysis Errors

Run PHPStan in the project and resolve the errors it reports.

## When to Use

- "Run phpstan"
- "Run phpstan and fix the errors"
- "Run static analysis and fix it"
- "Fix the phpstan errors"
- "Clean up my type errors"

## Step 1 - Detect DDEV

The PHPStan command may need to run inside DDEV. Before running anything, make sure you are at the project root (the folder containing `vendor/`), then check whether the project uses DDEV:

```bash
[ -f .ddev/config.yaml ] && echo "uses_ddev" || echo "no_ddev"
```

- If `uses_ddev`, prefix every command in this skill with `ddev exec`.
- If `no_ddev`, run every command directly with no prefix.

```bash
# With DDEV
ddev exec vendor/bin/phpstan analyze --memory-limit=2048M

# Without DDEV
vendor/bin/phpstan analyze --memory-limit=2048M
```

## Step 2 - Run PHPStan

Run the command and capture the full output:

```bash
vendor/bin/phpstan analyze --memory-limit=2048M
```

If PHPStan is not installed, install it first (use the same prefix from Step 1):

```bash
composer require --dev phpstan/phpstan mglaman/phpstan-drupal
```

## Step 3 - Read the errors

PHPStan lists one error per line with the file, line number, and a message:

```
 ------ -------------------------------------------------------------------
  Line   src/Controller/MyController.php
 ------ -------------------------------------------------------------------
  23     Call to an undefined method Drupal\Core\Entity\EntityInterface::foo().
 ------ -------------------------------------------------------------------

 [ERROR] Found 1 error
```

Read every message. Each one names a real type or symbol problem in the code.

## Step 4 - Fix the errors

PHPStan errors are not auto-fixable. Fix each one manually. Read the file before editing. Common ones:

| Message | How to fix |
|---|---|
| Call to an undefined method | Correct the method name, or add the method on the right class |
| Cannot call method on unknown type | Add a type hint, instanceof check, or phpdoc `@var` |
| Access to an undefined property | Declare the property with a type |
| Class not found | Add a `use` statement or fix the namespace |
| Property is never written | Initialize it in `__construct` or add a default |
| Return type mismatch | Fix the declared return type or the returned value |

Fix project code with real changes. For errors that originate in third-party or contrib code (not your project), a `phpstan baseline` entry or `ignoreErrors` in `phpstan.neon` is acceptable, but prefer a real fix whenever the code is yours.

## Step 5 - Re-run until clean

Run PHPStan again. Repeat Step 4 until the run reports `[OK] No errors`. Stop when the output is green.

Finish with a short summary: files changed, errors fixed, errors remaining.
