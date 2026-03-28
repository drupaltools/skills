---
name: drupaltools-site-clone
description: Clone an entire Drupal project as a clean starter template — copying custom code, config structure, and tooling while stripping all site-specific data, credentials, UUIDs, and history. Use this skill whenever the user wants to create a new Drupal project based on an existing one, says "clone this site", "use this project as a template", "create a new site from this codebase", or asks to scaffold a new Drupal project from an existing one.
---

# Drupal site clone

Create a clean starter template from an existing local Drupal project.

## Step 1 — Confirm the source project

Ask the user to confirm the source project root if not already clear from context. Verify it looks like a Drupal project:

```bash
test -f composer.json && test -f composer.lock && \
test -d web/core && echo "Valid Drupal project root"
```

Also detect the webroot — it may be `web/`, `docroot/`, or `html/`:
```bash
for d in web docroot html; do
  [ -d "$d/core" ] && echo "Webroot: $d" && break
done
```

Store the detected webroot as `$WEBROOT` for all subsequent steps. If detection fails, ask the user.

## Step 2 — Ask for destination and new project name

Ask the user:
1. Full path where the clone should be created (e.g. `/home/user/projects/newsite`).
2. New project machine name (used for composer.json `name`, directory name, and any project-specific strings).

Validate the machine name: lowercase letters, digits, hyphens only, no spaces.
Validate the destination: must not already exist.

## Step 3 — Create the destination structure

```bash
mkdir -p "$DEST"
```

Then create the skeleton of folders that will be populated in later steps:
```bash
mkdir -p "$DEST/$WEBROOT/modules/custom"
mkdir -p "$DEST/$WEBROOT/themes/custom"
mkdir -p "$DEST/$WEBROOT/sites/default"
mkdir -p "$DEST/config"
mkdir -p "$DEST/drush"
mkdir -p "$DEST/scripts"
mkdir -p "$DEST/patches"
```

## Step 4 — Copy custom code

Copy each of the following, preserving internal structure:

```bash
# Custom modules
cp -r "$SOURCE/$WEBROOT/modules/custom/." "$DEST/$WEBROOT/modules/custom/"

# Custom themes
cp -r "$SOURCE/$WEBROOT/themes/custom/." "$DEST/$WEBROOT/themes/custom/"

# Drush commands and config
[ -d "$SOURCE/drush" ] && cp -r "$SOURCE/drush/." "$DEST/drush/"

# Project scripts
[ -d "$SOURCE/scripts" ] && cp -r "$SOURCE/scripts/." "$DEST/scripts/"

# Patches
[ -d "$SOURCE/patches" ] && cp -r "$SOURCE/patches/." "$DEST/patches/"

# CI/CD config
for f in .github .gitlab-ci.yml .gitlab .circleci; do
  [ -e "$SOURCE/$f" ] && cp -r "$SOURCE/$f" "$DEST/$f"
done
```

## Step 5 — Copy and strip config files

Copy all config directories, then strip UUIDs from every YAML file.

```bash
# Find and copy config dirs (handles config/sync, config/default, etc.)
find "$SOURCE" -type d -name "config" | grep -v "$WEBROOT/core" | while read d; do
  rel="${d#$SOURCE/}"
  mkdir -p "$DEST/$rel"
  cp -r "$d/." "$DEST/$rel/"
done
```

Strip UUIDs from all copied YAML files:
```bash
find "$DEST/config" -name "*.yml" | xargs sed -i '/^uuid:/d'
```

Also remove the `_core` block (contains site-specific hash) from config YAML:
```bash
find "$DEST/config" -name "*.yml" | xargs sed -i '/^_core:/,/^[^ ]/{ /^_core:/d; /^  default_config_hash:/d }'
```

## Step 6 — Copy and rewrite composer.json

Copy the file then prompt the user for new values:

```bash
cp "$SOURCE/composer.json" "$DEST/composer.json"
```

Ask the user for:
- **name** — format `vendor/project` (e.g. `mycompany/newsite`)
- **description** — one line describing the new project
- **authors** — name and email (can be empty)

Rewrite with the provided values using `jq` if available, otherwise sed:

```bash
# With jq (preferred)
jq --arg name "$NEW_NAME" \
   --arg desc "$NEW_DESC" \
   '.name = $name | .description = $desc | .authors = []' \
   "$DEST/composer.json" > /tmp/composer.tmp && mv /tmp/composer.tmp "$DEST/composer.json"
```

Do not copy `composer.lock` — the clone starts without a lock file. The user must run `composer install` to generate a fresh one.

## Step 7 — Copy README.md as a template

```bash
cp "$SOURCE/README.md" "$DEST/README.md"
```

Then replace the body content with placeholder sections, preserving only the top-level heading structure:

```bash
cat > "$DEST/README.md" << 'README'
# [Project name]

## Overview

[Describe the project.]

## Requirements

- Drupal: [version]
- PHP: [version]
- Composer: [version]

## Installation

[Describe installation steps.]

## Configuration

[Describe configuration steps.]

## Development

[Describe local development setup.]

## Maintainers

[List maintainers.]
README
```

## Step 8 — Strip sensitive and environment-specific files

Do not copy the following. If any were accidentally copied, remove them:

```bash
# Git history
rm -rf "$DEST/.git"

# Environment files
rm -f "$DEST/.env" "$DEST/.env.local" "$DEST/.env.*.local"

# IDE/editor config
rm -rf "$DEST/.vscode" "$DEST/.idea"
rm -f "$DEST/.editorconfig" 2>/dev/null  # keep only if intentional

# Drupal-generated and sensitive files
rm -f "$DEST/$WEBROOT/sites/default/settings.php"
rm -f "$DEST/$WEBROOT/sites/default/settings.local.php"
rm -f "$DEST/$WEBROOT/sites/default/services.yml"
rm -rf "$DEST/$WEBROOT/sites/default/files"

# Composer lock
rm -f "$DEST/composer.lock"
```

## Step 9 — Report

List what was created, what was stripped, and what the user must do next:

**Created:**
- Directory structure under `$DEST`
- Custom modules, themes, drush, scripts, patches, CI config
- Config files (UUIDs and `_core` hashes stripped)
- `composer.json` (rewritten)
- `README.md` (template)
- `default.settings.php`
- Fresh git repository (if confirmed)

**Stripped:**
- `.git`, `.env`, IDE config, `composer.lock`
- `settings.php`, `services.yml`, `sites/default/files/`
- All config UUIDs and `_core` hashes

**Required next steps for the user:**
1. `composer install` — generate a fresh `composer.lock`.
2. Create `sites/default/settings.php` from `default.settings.php`.
3. Create a new database and update `settings.php` with credentials.
4. `drush site:install` or import config with `drush cim`.
5. Fill in `README.md`.
6. Set a remote git origin if needed.

## Step 12 — Wait for follow-up questions

Stop after the report. Typical follow-ups:

- Init a ddev project `ddev config`
- "Check the custom modules against best practices" — hand off to `drupal-best-practices`.
- "Show me what config files were copied" — list `$DEST/config/**/*.yml`.
- "Update the composer.json further" — edit specific fields on request.
- "What modules are in the custom folder?" — hand off to `drupal-module-info` for each.
