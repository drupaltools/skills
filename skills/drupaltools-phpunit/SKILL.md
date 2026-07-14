---
name: drupaltools-phpunit
description: Run the custom PHPUnit test suite in a Drupal project and fix the reported failures and errors. Use this skill whenever the user asks to run phpunit, run the tests, run the custom testsuite, or says "run phpunit and fix the errors".
---

# PHPUnit - Run and Fix Test Failures

Run the custom test suite in the project and resolve the failures and errors it reports.

## When to Use

- "Run phpunit"
- "Run phpunit and fix the errors"
- "Run the custom testsuite"
- "Run the tests and fix them"
- "Fix the failing tests"

## Step 1 - Detect DDEV

The PHPUnit command may need to run inside DDEV. Before running anything, make sure you are at the project root (the folder containing `vendor/`), then check whether the project uses DDEV:

```bash
[ -f .ddev/config.yaml ] && echo "uses_ddev" || echo "no_ddev"
```

- If `uses_ddev`, prefix every command in this skill with `ddev exec`.
- If `no_ddev`, run every command directly with no prefix.

```bash
# With DDEV
ddev exec vendor/bin/phpunit --testsuite custom

# Without DDEV
vendor/bin/phpunit --testsuite custom
```

## Step 2 - Run PHPUnit

Run the command and capture the full output:

```bash
vendor/bin/phpunit --testsuite custom
```

If PHPUnit is not installed, install it first (use the same prefix from Step 1):

```bash
composer require --dev phpunit/phpunit drupal/core-dev
```

## Step 3 - Read the results

PHPUnit separates problems into three kinds:

- **FAILURES** - an assertion did not match. Shows `Failed asserting that X matches Y`.
- **ERRORS** - the test threw an exception or crashed. Shows a stack trace.
- **WARNINGS / RISKY** - skipped, incomplete, or risky tests.

For each problem note the test class, the test method, and the message with its stack trace.

## Step 4 - Fix the problems

For each failure or error, first decide whether the bug is in the code or in the test:

- If the code does the wrong thing, fix the code.
- If the test asserts the wrong thing, fix the test.

Read the test method and the code it exercises before editing. Common ones:

| Problem | How to fix |
|---|---|
| Failed asserting X matches Y | Fix the code so it produces the expected value, or correct the expectation |
| Class not found | Add a `use` statement or fix the namespace / autoloading |
| Call to undefined method | Correct the method name or add the method |
| Missing service / dependency | Declare the service and inject it, or add it to the test container |
| Exception thrown in test | Read the stack trace, fix the cause at the source |
| Database / kernel not bootstrapped | Extend `KernelTestBase` or `BrowserTestBase` as appropriate |

Re-run a single failing test while iterating to get feedback fast (same prefix rules):

```bash
vendor/bin/phpunit --testsuite custom --filter TestName
```

## Step 5 - Re-run until green

Run the full command again. Repeat Step 4 until all tests pass and the run reports `OK` or `Tests: N, Assertions: M` with no failures or errors.

Finish with a short summary: tests fixed, tests still failing, anything skipped.
