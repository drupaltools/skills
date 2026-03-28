---
name: drupaltools-module-clone
description: Clone a Drupal module as a structural scaffold - copy the file and folder structure of an existing local module, renaming all occurrences of the original machine name to a new one. Use this skill whenever the user wants to create a new module based on an existing one, says "clone this module", "use this module as a template", "scaffold a new module from X", or provides a module machine name and asks for a copy or starting point.
---

# Drupal module clone

Create a structural scaffold of an existing local Drupal module under a new machine name.

## Step 1 - Locate the source module

Use the `drupal-module-info` skill to identify and confirm the source module details.

Find the module directory by searching common locations:
```bash
find web/modules -type d -name "<source_machine_name>" | head -5
```

If not found, also try:
```bash
find modules -type d -name "<source_machine_name>" | head -5
```

If the module cannot be found, tell the user and stop.

Report what was found (module name, type, path) and ask the user to confirm before continuing.

## Step 2 - Ask for the new machine name

Once the source module is confirmed, ask:

"What should the new module machine name be?"

Validate the answer:
- Lowercase letters, digits, and underscores only.
- Must start with a letter.
- Must not already exist in the project (`find web/modules -type d -name "<new_name>"`).
- Should be prefixed with the project machine name if the project follows that convention (detect from sibling custom modules).

If validation fails, explain why and ask again.

## Step 3 - Determine the clone destination

Default destination: same parent directory as the source module.

```bash
SOURCE_DIR=web/modules/custom/<source_machine_name>
DEST_DIR=web/modules/custom/<new_machine_name>
```

If the source is not under `custom/`, ask the user where to place the clone.

## Step 4 - Copy and rename

Copy the entire directory structure, excluding non-structural content:

```bash
cp -r "$SOURCE_DIR" "$DEST_DIR"
```

Then remove data files that must not carry over:
```bash
# Remove compiled/generated files
find "$DEST_DIR" -name "*.min.js" -o -name "*.min.css" | xargs rm -f
# Remove any cached or built assets
rm -rf "$DEST_DIR/node_modules" "$DEST_DIR/vendor"
```

## Step 5 - Rename all occurrences

Replace every occurrence of the old machine name with the new one - in file names, directory names, and file contents.

**File and directory names:**
```bash
# Rename files (deepest first to avoid path conflicts)
find "$DEST_DIR" -depth -name "*<source_machine_name>*" | while read f; do
  mv "$f" "${f//<source_machine_name>/<new_machine_name>}"
done
```

**File contents** - replace all three common casing forms:

| Pattern | Replace with |
|---------|-------------|
| `source_machine_name` (snake_case) | `new_machine_name` |
| `SourceMachineName` (PascalCase) | `NewMachineName` |
| `source machine name` (human label) | `new machine name` |

```bash
grep -rl "<source_machine_name>" "$DEST_DIR" | xargs sed -i \
  "s/<source_machine_name>/<new_machine_name>/g"
```

Repeat for PascalCase and human-readable variants.

## Step 6 - Clean up the scaffold

After renaming, strip content that belongs to the source module but not the scaffold:

- Clear the `description:` field in `<new_machine_name>.info.yml` and prompt the user to set it.
- Remove the `version:` field from the info.yml (not relevant for a custom module).
- Empty the body of all hook implementations - leave the function signature and a `// TODO` comment.
- Empty the body of all service class methods - leave the signature and a `// TODO` comment.
- Keep all YAML structure (services.yml, routing.yml, schema.yml) but empty the values that are module-specific.

## Step 7 - Report

List every file created, grouped by type:

```
Created: web/modules/custom/<new_machine_name>/
  <new_machine_name>.info.yml
  <new_machine_name>.module
  <new_machine_name>.services.yml
  src/...
  templates/...
```

Then state:
- How many files were created.
- How many rename replacements were made.
- Which files still contain `// TODO` markers.
- That a `drush cr` is needed before the module can be enabled.

## Step 8 - Wait for follow-up questions

Stop and wait after the report. Typical follow-ups:

- "Enable the module" - run `drush en <new_machine_name>`.
- "Update the description" - edit the info.yml description field.
- "Show me the file list" - list all files under the new module directory.
- "Check it against best practices" - hand off to the `drupal-best-practices` skill.
