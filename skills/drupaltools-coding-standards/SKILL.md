---
name: drupaltools-coding-standards
description: Check and fix Drupal PHP coding standards violations using PHPCS and PHPStan. Use this skill when you need to validate code against Drupal standards, fix coding style issues, or run automated code quality checks.
---

# Drupal Coding Standards

Check and fix PHP code against Drupal coding standards using PHPCS and PHPStan.

## When to Use

Use this skill when:
- "Check my module for coding standards"
- "Run PHPCS on my code"
- "Fix coding standards violations"
- "Validate against Drupal standards"

## Tools

| Tool | Purpose | Package |
|------|---------|---------|
| PHPCS | Code style (Drupal, DrupalPractice) | `drupal/coder` |
| PHPStan | Static analysis | `phpstan/phpstan` |
| PHPCBF | Auto-fix style issues | `squizlabs/php_codesniffer` |

## Check Coding Standards

### 1. Detect Available Tools

```bash
# Check PHPCS
vendor/bin/phpcs --version 2>/dev/null && echo "phpcs_available"

# Check PHPStan
vendor/bin/phpstan --version 2>/dev/null && echo "phpstan_available"
```

### 2. Run PHPCS

```bash
vendor/bin/phpcs --standard=Drupal,DrupalPractice --extensions=php,module,inc,install,test,profile,theme,css,info,txt,md,yml
```

### 3. Run PHPStan

```bash
vendor/bin/phpstan analyse --no-progress --error-format=table
```

## Fix Coding Standards

### Auto-fix with PHPCBF

```bash
vendor/bin/phpcbf --standard=Drupal,DrupalPractice --extensions=php,module,inc,install,test,profile,theme,css,info,txt,md,yml
```

### Common Fixes

| Issue | Command |
|-------|---------|
| Line length | PHPCBF auto-fixes |
| Indentation | PHPCBF auto-fixes |
| Trailing whitespace | PHPCBF auto-fixes |
| Missing docblocks | Manual fix required |

## Output Format

### PHPCS Output

```
FILE: src/Controller/MyController.php
--------------------------------------------------------------------------------
FOUND 3 ERRORS AFFECTING 3 LINES
--------------------------------------------------------------------------------

  2 | ERROR | [x] Missing file docblock
 15 | ERROR | [ ] Line exceeds 80 characters
 42 | ERROR | [ ] Missing function docblock

FILE: my_module.module
--------------------------------------------------------------------------------
FOUND 1 WARNING AFFECTING 1 LINE
--------------------------------------------------------------------------------

 23 | WARNING | [ ] Unused variable
```

### PHPStan Output

```
 ------ -------------------------------------------------------------------
  Line   src/Controller/MyController.php
 ------ -------------------------------------------------------------------
  23     Call to an undefined method Drupal\Core\Entity\EntityInterface::foo().
 ------ -------------------------------------------------------------------

 [ERROR] 1 error
```

## Drupal Coding Standards

### Key Rules

| Rule | Standard | Fix |
|------|----------|-----|
| Line length | Max 80 chars | Wrap line |
| File docblock | Required | Add file-level docblock |
| Function docblock | Required | Document all functions |
| Indentation | 2 spaces | Use spaces |
| Class names | PascalCase | Follow naming |
| Function names | camelCase | Follow naming |

### Install Tools

```bash
composer require --dev drupal/coder phpstan/phpstan
```

## Output Example

```
✅ CODING STANDARDS CHECK COMPLETE

PHPCS Results: 2 errors, 5 warnings

Errors:
- src/Controller/MyController.php:45 - Line exceeds 80 characters
- src/Plugin/Field/MyField.php:78 - Missing function docblock

Warnings:
- my_module.module:12 - Unused variable $foo
- my_module.module:23 - Line indented with tabs

PHPStan: 0 errors

Auto-fix available: Yes
Run: vendor/bin/phpcbf --standard=Drupal,DrupalPractice
```

## DDEV Commands

When checking coding standards in a Drupal project, first check if tools are installed:

```bash
# Check if composer dependencies exist
ddev composer validate 2>/dev/null && echo "vendor_exists" || echo "run composer install first"
```

Then run tools via DDEV:

```bash
# PHPCS via DDEV
ddev exec vendor/bin/phpcs --standard=Drupal,DrupalPractice --extensions=php,module,inc,install,test,profile,theme

# PHPStan via DDEV
ddev exec vendor/bin/phpstan analyse

# Auto-fix via DDEV
ddev exec vendor/bin/phpcbf --standard=Drupal,DrupalPractice
```

If vendor doesn't exist, run `ddev composer install` first.

## Frontend Linting

Drupal projects include linting configuration for JS/CSS. Check these files:

| File | Purpose |
|------|---------|
| `.editorconfig` | General code style |
| `.eslintrc.json` | JavaScript linting |
| `.stylelintrc.json` | CSS/SCSS linting |
| `.prettierrc.json` | Code formatting |
| `web/core/.eslintrc.json` | Core JS config |

## Using LSP for PHP

For PHP symbol navigation (classes, methods, references, inheritance), use LSP tools before grep:

1. **PHP LSP by Anthropic** - `php-lsp` plugin
2. **PHPStorm** - SSE at `http://localhost:64342/sse`
3. **cclsp** - `npx cclsp@latest setup --user`
4. **Intelephense** - VS Code extension

Use LSP for:
- Resolving PHP symbols (classes, interfaces, traits)
- Finding implementations, overrides, inheritance chains
- Locating references across the codebase
- Navigating unfamiliar codebases safely

## Resources

- [Drupal Coding Standards](https://www.drupal.org/docs/develop/standards)
- [Drupal Practice Standards](https://www.drupal.org/node/1886776)
- [PHPStan Drupal Extension](https://github.com/mglaman/phpstan-drupal)
