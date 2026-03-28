---
name: drupaltools-contrib-lookup
description: Find the equivalent online source code URL on git.drupalcode.org for a pasted code snippet from a Drupal contrib module. Use this skill whenever a user pastes PHP/Drupal code and asks to find it online, find the source, locate it on drupalcode.org, or wants a link to the code on the Drupal git repository. Trigger even if the user just says "find this online" or "where is this code" or "drupalcode" or when Drupal module code is present.
---

# Drupal contrib project online code lookup

Given a pasted code snippet from a Drupal contrib module or from Drupal core, find the equivalent URL on git.drupalcode.org.

## Workflow

### Step 1: Identify lines in the file

- Count or identify the line numbers ($lines) of the pasted code within its source file.
- Format: `L17-L34` style (e.g. `#L17-L34`).
- If the user has not provided the file path, ask for it OR infer it from context clues in the code (hook names, module prefixes, namespaces).

### Step 2: Identify the parent module path

- Determine the module folder containing the code file.
- Typical Drupal path: `modules/contrib/<module_name>/` or a subfolder within it.
- Example: `modules/contrib/admin_toolbar/admin_toolbar_tools/`

### Step 3: Find the machine name from \*.info.yml

- Look for a `*.info.yml` file in the module directory.
- The machine name ($machine_name) = the filename prefix of that `.info.yml` file.
- Example: `admin_toolbar_tools.info.yml` → $machine_name = `admin_toolbar_tools`

### Step 4: Extract project and version

From the `*.info.yml` file, read:
- `project:` → $project
- `version:` → $version

Example values:
```
project: admin_toolbar
version: 8.x-3.4
```

### Step 5: Walk up if project/version not found

- If the `*.info.yml` in the current folder does not contain `project:` or `version:`, move up one directory level.
- Repeat Steps 3-4 until you find an `*.info.yml` that contains both values.
- The $project value is typically the top-level contrib module name (e.g. `admin_toolbar`, not the submodule).

### Step 6: Check if this code is from Drupal core

- If the `*.info.yml` has no parent with a `version` and is under folders like `web/core` or `docroot/core` then it is probably a Drupal core module or code snippet.
- In this case get the project is "drupal" and the version can be found with one of the methods below (prefer this order):
  - From the `const VERSION` variable on `core/lib/Drupal.php`
  - With jq to parse composer.lock directly: `cat composer.lock | jq '.packages[] | select(.name=="drupal/core-recommended") | .version'`
  - With composer: `composer show drupal/core --format=json | jq -r '.versions[0]'` or if need ddev `ddev composer show drupal/core --format=json | jq -r '.versions[0]'`

### Step 7: Identify the relative path

- $relative_path = path of the code file **relative to the $project folder**.
- Example: if file is at `modules/contrib/admin_toolbar/admin_toolbar_tools/admin_toolbar_tools.module`
  and $project = `admin_toolbar`, then:
  $relative_path = `admin_toolbar_tools/admin_toolbar_tools.module`

### Step 8: Build the URL

`https://git.drupalcode.org/project/$project/-/blob/$version/$relative_path?ref_type=tags#L$lines`

Example:
`https://git.drupalcode.org/project/admin_toolbar/-/blob/8.x-3.4/admin_toolbar_tools/admin_toolbar_tools.module?ref_type=tags#L17-L34`

## Output Format

Return:

1. The URL as a clickable link.
2. A simple markdown table of resolved values:

| Variable        | Value                                          |
|-----------------|------------------------------------------------|
| $lines          | L17-L34                                        |
| $machine_name   | admin_toolbar_tools                            |
| $project        | admin_toolbar                                  |
| $version        | 8.x-3.4                                        |
| $relative_path  | admin_toolbar_tools/admin_toolbar_tools.module |

## Notes

- If `project:` is missing from the `.info.yml`, the module was likely installed from source (git clone) and may not have a tagged release. Inform the user.
- For Drupal 10+ modules, versions may look like `2.1.0` instead of `8.x-3.4` - both are valid tag formats.
- If the user does not know the file path, ask for: the module name and the function/class name, then infer the likely file.
