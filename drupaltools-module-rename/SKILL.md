---
name: drupaltools-module-rename
description: Rename a Drupal module's machine name throughout its codebase, updating all file names, class names, service names, and references. Use this skill when the user wants to rename an existing module to a new machine name, change module identifiers, or refactor a module's namespace without creating a copy.
---

# Drupal Module Rename

Rename an existing Drupal module's machine name throughout its entire codebase.

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
- Function names: `function ${OLD_MACHINE_NAME}_` → `function ${NEW_MACHINE_NAME}_`
- Service names: `$OLD_MACHINE_NAME.` → `$NEW_MACHINE_NAME.`
- Config keys: Any config storage using the old prefix
- Class namespaces: Update if namespace includes machine name
- Route names: `$OLD_MACHINE_NAME.` → `$NEW_MACHINE_NAME.`
- Permission names: Update any module-specific permissions
- Hook implementations: All `hook_[name]()` implementations

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
