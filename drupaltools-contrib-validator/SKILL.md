---
name: drupaltools-contrib-validator
description: Validates Drupal 10+ custom modules for Drupal.org contribution readiness. Use this skill when you need to check if a module is ready for Drupal.org, validate required files, or get recommendations for contribution.
---

# Drupal Contributed Module Validator

Validate Drupal 10+ custom modules for Drupal.org contribution readiness.

## Related Skills

This skill orchestrates specialized sub-skills:

| Sub-skill | Use When |
|-----------|----------|
| `drupaltools-contrib-readme` | Generating or validating README.md |
| `drupaltools-contrib-gitlab-ci` | Creating .gitlab-ci.yml |
| `drupaltools-coding-standards` | PHPCS/PHPStan validation |

## When to Use

- "Is my module ready for Drupal.org?"
- "What files are missing for contribution?"
- "Validate my module for Drupal.org"

## Required Files

| File | Status | Description |
|------|--------|-------------|
| `MODULE.info.yml` | **REQUIRED** | Module definition file |
| `README.md` | **REQUIRED** | Module documentation |
| `logo.png` | **REQUIRED** | Module logo (120x120px) |
| `.gitlab-ci.yml` | **REQUIRED** | GitLab CI configuration |
| `composer.json` | Recommended | For namespace/dependencies |
| `.cspell-project-words.txt` | Optional | Custom spell-check words |
| `LICENSE` | **DO NOT ADD** | Drupal.org injects automatically |

## Validation Process

### Step 1: File Structure Check

Scan for required files:

```bash
ls MODULE.info.yml README.md logo.png .gitlab-ci.yml 2>/dev/null
```

### Step 2: Parse Info File

Read `MODULE.info.yml`:

```yaml
name: 'Module Name'
type: module
description: 'Brief description'
core_version_requirement: ^10.1 || ^11
```

Required keys: `name`, `type`, `description`, `core_version_requirement`

### Step 3: Delegate Validation

Hand off to sub-skills for specialized checks:

- **README validation**: Use `drupaltools-contrib-readme`
- **GitLab CI validation**: Use `drupaltools-contrib-gitlab-ci`  
- **Coding standards**: Use `drupaltools-coding-standards`

### Step 4: Report Results

```
❌ VALIDATION FAILED

Missing Required Files:
- README.md (not found)
- logo.png (not found)
- .gitlab-ci.yml (not found)

Info File: ✅ Valid
- Name: Module Name
- Core: ^10.1 || ^11
- Dependencies: node, text

Recommendations:
1. Generate README.md with required sections
2. Add logo.png (120x120px recommended)
3. Generate .gitlab-ci.yml

Type "generate" to create missing files.
```

## Generate Missing Files

### Generate README.md

Hand off to `drupaltools-contrib-readme`:

```
"Generate a README.md for my module"
```

### Generate GitLab CI

Hand off to `drupaltools-contrib-gitlab-ci`:

```
"Add GitLab CI to my module"
```

### Generate All Files

1. Run `drupaltools-contrib-readme`
2. Run `drupaltools-contrib-gitlab-ci`
3. Provide logo instructions

## Quick Reference

### Info File Template

```yaml
name: 'Module Name'
type: module
description: 'Brief description'
core_version_requirement: ^10.1 || ^11
package: Custom
# Optional:
# dependencies:
#   - node:node
# configure: module.settings
```

## Resources

- [Drupal.org: Module Structure](https://www.drupal.org/docs/develop/creating-modules)
- [Drupal.org: GitLab CI](https://www.drupal.org/node/3356364)
- [Drupal Coding Standards](https://project.pages.drupalcode.org/coding_standards)
