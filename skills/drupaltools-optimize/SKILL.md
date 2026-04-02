---
name: drupaltools-optimize
description: Optimize selected Drupal PHP code for the Drupal and PHP versions currently in use in the project. Use this skill whenever the user selects code and asks to optimize, modernize, refactor, or improve it for their current environment — e.g. "optimize this for my Drupal version", "update this code to use modern PHP", "refactor this hook for Drupal 11", "make this more idiomatic", or any request to improve existing Drupal PHP code quality.
---

# Drupal Code Optimizer

Optimize selected PHP code for the Drupal and PHP versions active in the current project.

## Step 1 — Detect versions

Do not assume versions. Detect them from the project files before touching any code.

**Drupal version** — check in order, stop at first match:
```bash
grep -A1 '"name": "drupal/core"' composer.lock | grep version
cat web/core/lib/Drupal.php | grep "const VERSION"
drush status --field=drupal-version 2>/dev/null
```

**PHP version** — check in order, stop at first match:
```bash
php --version | head -1
grep '"php"' composer.json
cat .php-version 2>/dev/null || grep php .tool-versions 2>/dev/null
```

If either version cannot be determined, ask the user before proceeding.

## Step 2 — Analyse the selection

Identify what the selected code is:

| Type | Examples |
|------|---------|
| Hook implementation | `my_module_entity_presave()`, `my_module_form_alter()` |
| Service / injectable class | Constructor, methods using `\Drupal::*` |
| Plugin | Block, FieldFormatter, QueueWorker |
| Twig preprocess | `my_module_preprocess_node()` |
| Controller / form class | Extending `ControllerBase`, `FormBase` |
| Procedural utility | Standalone functions, static helpers |
| Other | Route subscriber, access checker, event subscriber |

Only apply optimizations available in the detected versions. Do not suggest features from newer versions.

## Step 3 — Apply optimizations

### PHP version-gated improvements

| Available from | Optimization |
|---------------|-------------|
| PHP 8.0 | Union types, `match` expression, named arguments, nullsafe operator `?->`, constructor property promotion |
| PHP 8.1 | Enums, readonly properties, `never` return type, array unpacking with string keys |
| PHP 8.2 | Readonly classes, `true`/`false`/`null` as standalone types, DNF types |
| PHP 8.3 | Typed class constants, `json_validate()`, `#[Override]` attribute |

Always add `declare(strict_types=1)` if absent.

### Drupal version-gated improvements

| Available from | Optimization |
|---------------|-------------|
| Drupal 10.0 | Symfony 6 compatibility; verify no removed D9 APIs are used |
| Drupal 10.2 | Single-file component (SDC) support |
| Drupal 11.0 | `#[Hook]` attributes stable (`\Drupal\Core\Hook\Attribute\Hook`); jQuery UI removed; CKEditor 5 only |

Do not suggest `#[Hook]` attributes for projects on Drupal 9.x or 10.x — they were experimental and not stable before D11.

### Always apply (version-independent)

- Replace `\Drupal::service()` / `\Drupal::*()` inside injectable classes with constructor injection.
- Keep `\Drupal::service()` only at hook entry points as a bridge to the service layer.
- Replace procedural hook bodies with thin wrappers delegating to a service class.
- Replace deprecated `@Annotation` plugin discovery with PHP 8 `#[Attribute]` where the Drupal version supports it.
- Add missing return types and parameter types.
- Use interface type hints, not concrete class type hints.
- Remove unused `use` statements; add missing ones.
- Replace `array()` with `[]`.
- Replace `strpos() !== false` with `str_contains()` (PHP 8.0+).
- Replace `substr()` prefix/suffix checks with `str_starts_with()` / `str_ends_with()` (PHP 8.0+).
- Flag any calls to APIs removed or deprecated in the detected Drupal version.

## Step 4 — Output format

**Versions detected**
- Drupal: X.Y.Z
- PHP: X.Y.Z

**Changes made** — one bullet per change, stating what changed and why.

**Optimized code** — complete rewritten code, ready to drop in. No fragments.

**Remaining notes** — anything requiring human review: deprecations with no direct replacement, schema/routing/YAML changes needed alongside the PHP change.

## Step 5 — Flag but do not auto-change

Flag these separately rather than silently rewriting them:

- Business logic that may have unintended side effects if restructured.
- Hooks touching entity saves where infinite resave loops are possible.
- Any change requiring a cache rebuild, config import, or schema update.
- Backwards-compatibility code that may still be needed for older environments.