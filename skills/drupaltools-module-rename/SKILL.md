---
name: drupaltools-module-rename
description: Rename a Drupal module's machine name throughout its codebase, updating all file names, class names, service names, and references. Use this skill when the user wants to rename an existing module to a new machine name, change module identifiers, or refactor a module's namespace without creating a copy.
---

# Drupal Module Rename

Rename an existing Drupal module's machine name throughout its entire codebase.

## When to use this vs module-clone

| Scenario | Skill |
|----------|-------|
| You want a **new** module based on an existing one (template/scaffold) | `drupaltools-module-clone` |
| You want to **rename an existing module** in-place | `drupaltools-module-rename` |

**Key difference**: Clone creates a copy with a new identity. Rename transforms the existing module.

---

## Step 1 — Identify source and target

- Locate the source module's `.info.yml` file to confirm the current `$OLD_MACHINE_NAME`
- Validate the new `$NEW_MACHINE_NAME` follows Drupal naming conventions (lowercase letters, underscores, no spaces)

## Step 2 — File structure changes

Rename files and folders:
- Rename `$OLD_MACHINE_NAME.info.yml` → `$NEW_MACHINE_NAME.info.yml`
- Rename `$OLD_MACHINE_NAME.module` → `$NEW_MACHINE_NAME.module`
- Rename `$OLD_MACHINE_NAME.install` → `$NEW_MACHINE_NAME.install` (if exists)
- Rename `$OLD_MACHINE_NAME.services.yml` → `$NEW_MACHINE_NAME.services.yml` (if exists)
- Rename `$OLD_MACHINE_NAME.links.menu.yml` → `$NEW_MACHINE_NAME.links.menu.yml` (if exists)
- Rename `$OLD_MACHINE_NAME.routing.yml` → `$NEW_MACHINE_NAME.routing.yml` (if exists)
- Rename `$OLD_MACHINE_NAME.permissions.yml` → `$NEW_MACHINE_NAME.permissions.yml` (if exists)
- Rename any plugin folders using the old machine name

## Step 3 — Content updates

Replace all occurrences inside files:

### File and directory names
```bash
# Rename files (deepest first to avoid path conflicts)
find "$MODULE_DIR" -depth -name "*<OLD_MACHINE_NAME>*" | while read f; do
  mv "$f" "${f//<OLD_MACHINE_NAME>/<NEW_MACHINE_NAME>}"
done
```

### File contents
Replace all three common casing forms:

| Pattern | Replace with |
|---------|-------------|
| `old_machine_name` (snake_case) | `new_machine_name` |
| `OldMachineName` (PascalCase) | `NewMachineName` |
| `old machine name` (human label) | `new machine name` |

```bash
# snake_case
grep -rl "<OLD_MACHINE_NAME>" "$MODULE_DIR" | xargs sed -i \
  "s/<OLD_MACHINE_NAME>/<NEW_MACHINE_NAME>/g"

# PascalCase (capitalize first letter)
sed -i 's/OldMachineName/NewMachineName/g' "$MODULE_DIR"/*.php

# Human labels (capitalize words)
sed -i 's/old machine name/new machine name/g' "$MODULE_DIR"/*.md
```

## Step 4 — Database considerations

Warn the user that renaming a module:
- Will cause config entity IDs to change (requires database updates)
- May break existing content referencing the old module name
- Requires `drush updb` or manual config re-export after renaming

## Step 5 — Testing checklist

After renaming:
- Clear all caches (`drush cr`)
- Run `drush updb` to check for schema updates
- Verify module still enables without errors
- Check for any remaining references using grep
- Re-export configuration if needed
