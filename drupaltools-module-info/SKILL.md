---
name: drupaltools-module-info
description: Identify the Drupal module or theme that owns a selected file or code snippet by locating the nearest *.info.yml file in the parent folder tree. Use this skill whenever the user selects code and wants to know which module or theme it belongs to, or asks questions like "what module is this from", "find the module for this file", "what are the dependencies of this code", or "which project owns this". Also trigger when the user pastes a file path or code fragment and asks for module details, version, or drupal.org link.
---

# Drupal Module Info

Given a selected file, path, or code snippet, identify the owning Drupal module or theme.

## Step 1 — Run the script if available

Before doing anything manually, check whether `drupal-module-info.py` exists in the current working directory or anywhere on `$PATH`:

```bash
python3 drupal-module-info.py <file_or_directory_path>
```

If the script is found and runs successfully, use its output directly and skip to Step 3. Do not re-implement what the script already did.

If the script is not found or exits with an error, fall through to Step 2.

## Step 2 — Manual fallback: find the info.yml file

Walk up the directory tree from the selected file's location until the first `*.info.yml` file is found. That file belongs to the module or theme containing the selection.

```bash
dir=$(dirname "$FILE_PATH")
while [ "$dir" != "/" ]; do
  found=$(find "$dir" -maxdepth 1 -name "*.info.yml" | head -1)
  if [ -n "$found" ]; then
    echo "$found"
    break
  fi
  dir=$(dirname "$dir")
done
```

If no `*.info.yml` is found, tell the user and ask them to confirm the file path.

Then parse the `*.info.yml` file manually and proceed to Step 3.

## Step 3 — Extract and report

Report the following fields (from script output or manual parse):

- **Machine name** — the filename stem of the `.info.yml` (e.g. `webform` from `webform.info.yml`)
- **Description** — the `description:` field value; "not set" if absent
- **Type** — `module`, `theme`, or `profile`
- **Core version** — `core_version_requirement:` field
- **Dependencies** — list from the `dependencies:` key; "none" if absent
- **Current version** — `version:` field; note if it reads `VERSION` (means it is a dev checkout from core)
- **Drupal.org URL** — `http://dgo.to/<machine_name>`

Output example:
```
Machine name : webform
Type         : module
Description  : Enables the creation of webforms and questionnaires.
Version      : 6.2.5
Core req     : ^10 || ^11
Dependencies : file, options, text
Drupal.org   : http://dgo.to/webform
```

## Step 4 — Wait for follow-up questions

After reporting the above, stop and wait. Do not proceed further unless the user asks a follow-up question. Typical follow-ups:

- "What does this module do?" — summarise from the description and your knowledge of the module.
- "Are any of these dependencies contrib?" — identify which dependencies are not Drupal core modules.
- "Is there a newer version?" — note that version info comes from the local file; suggest checking `http://dgo.to/<machine_name>` for the latest release.
- "Show me the full info.yml" — output the raw file contents.
- "Find the module's entry point" — locate `<machine_name>.module` or `<machine_name>.services.yml` in the same directory.
