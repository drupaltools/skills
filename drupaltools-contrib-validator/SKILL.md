---
name: drupaltools-contrib-validator
description: Validates Drupal 10+ custom modules for Drupal.org contribution readiness, checking required files (info.yml, README.md, logo.png, .gitlab-ci.yml), generating missing files, and ensuring Drupal coding standards compliance for contributed modules.
version: 1.0.0
---

# Drupal Contributed Module Validator

A comprehensive validation and scaffolding tool for Drupal 10+ custom modules destined for Drupal.org contribution. This skill ensures your module meets all contribution requirements, follows Drupal coding standards, and includes all necessary documentation and CI/CD configuration.

## When to Use This Skill

Use this skill when you need to:

- **Validate** a custom Drupal module for Drupal.org contribution readiness
- **Check** if all required files are present (.info.yml, README.md, logo.png, .gitlab-ci.yml)
- **Generate** missing module files automatically
- **Ensure** README.md follows Drupal.org contribution guidelines
- **Add** GitLab CI configuration following Drupal Association templates
- **Verify** compliance with Drupal coding standards
- **Prepare** a module for sandbox or full project submission on Drupal.org

**Typical questions:**
- "Is my module ready for Drupal.org?"
- "What files are missing for contribution?"
- "Generate a .gitlab-ci.yml for my module"
- "Check if my README.md follows Drupal.org standards"
- "Add a logo to my Drupal module"
- "Validate this module against coding standards"

## How It Works

The validator performs a comprehensive analysis of your Drupal module directory structure, checking against Drupal.org contribution requirements and best practices. It provides detailed feedback on missing files, incomplete content, and coding standards violations.

### Validation Process

1. **File Structure Analysis** - Scans module directory for required files
2. **Content Validation** - Checks README.md sections, info.yml completeness
3. **CI/CD Configuration** - Validates .gitlab-ci.yml if present
4. **Coding Standards** - Runs PHPCS and PHPStan when available
5. **Generate Suggestions** - Provides specific recommendations to pass validation

### Required Files for Drupal.org Contribution

| File | Status | Description |
|------|--------|-------------|
| `MODULE_NAME.info.yml` | **REQUIRED** | Module definition file |
| `README.md` | **REQUIRED** | Documentation for developers |
| `logo.png` | **REQUIRED** | Module logo (recommended: 120x120px) |
| `.gitlab-ci.yml` | **REQUIRED** | GitLab CI configuration |
| `composer.json` | **RECOMMENDED** | For namespace/dependencies |
| `.cspell-project-words.txt` | **OPTIONAL** | Custom spell-check words |
| `LICENSE` | **DO NOT ADD** | Drupal.org injects automatically |

## Data Source: Drupal.org Standards

This validator is based on official Drupal.org documentation:

- **Module Structure**: [Drupal.org: Basic Module Structure](https://www.drupal.org/docs/develop/creating-modules/basic-module-building-tutorial-lorem-ipsum-generator/basic-structure)
- **GitLab CI**: [Drupal.org: GitLab CI Documentation](https://www.drupal.org/node/3356364)
- **Coding Standards**: [Drupal Coding Standards](https://project.pages.drupalcode.org/coding_standards)

The GitLab CI template uses the official Drupal Association template from:
`https://git.drupalcode.org/project/gitlab_templates/-/blob/1.0.x/gitlab-templates/.gitlab-ci.yml`

## Workflows

### 1. Validate Module for Contribution Readiness

**Prompt**: "Validate my Drupal module for Drupal.org contribution"

**Process**:
1. Detect current module directory
2. Scan for required files (.info.yml, README.md, logo.png, .gitlab-ci.yml)
3. Parse .info.yml to extract module metadata
4. Validate README.md structure and content
5. Check for services.yml to determine if services section needed
6. Run coding standards checks if tools available
7. Return PASS/FAIL with specific recommendations

**Example Output**:
```
❌ VALIDATION FAILED

Missing Required Files:
- README.md (not found)
- logo.png (not found)
- .gitlab-ci.yml (not found)

Incomplete Files:
- graphql_compose_debug.info.yml: Missing 'configure' key

Recommendations:
1. Add README.md with required sections (About, Basic usage, etc.)
2. Add logo.png (120x120px recommended)
3. Generate .gitlab-ci.yml using Drupal Association template
4. Add 'configure: graphql_compose_debug.settings' to info.yml if applicable

Type "generate" to create missing files automatically.
```

### 2. Generate Missing Files

**Prompt**: "Generate missing files for my module"

**Process**:
1. Read existing .info.yml to extract module name, description, dependencies
2. Check for MODULE.permissions.yml, MODULE.routing.yml, MODULE.services.yml
3. Generate README.md with appropriate sections
4. Create .gitlab-ci.yml from Drupal Association template
5. Add placeholder logo.png or instructions
6. Create .cspell-project-words.txt if custom terms detected

**Generated README.md Structure**:
```markdown
# Module Name

About
-----
Introduction summarizing purpose and function. First ~200 characters shown in project listings. Accessible to users new to Drupal.

Features
--------
Basic functionality, unique features, and use cases.

Requirements
------------
Required modules and dependencies.

Recommended modules
-------------------
Complementary modules that enhance functionality.

Example code
------------
Code examples for developers.

Similar projects
----------------
Alternative modules and differentiators.

Basic Services
--------------
(Optional) Services provided by this module (if services.yml exists).

Extend and override
-------------------
Hooks, events, and extension points.

Supporting this Module
-----------------------
Information about financial support or sponsorships.

Contributing
------------
Guidelines for contributing to the module.

Community Documentation
------------------------
Links to external resources, videos, demos.
```

### 3. Validate README.md Content

**Prompt**: "Check my README.md for Drupal.org compliance"

**Process**:
1. Parse README.md
2. Check for required sections
3. Validate NO file structure section exists
4. Validate NO installation instructions exist
5. Check content targets experienced developers
6. Verify Drupal coding standards in code examples

**Required Sections**:
- About (REQUIRED) - Introduction, first ~200 chars shown in listings
- Features (REQUIRED) - Functionality and use cases
- Requirements (OPTIONAL) - Dependencies
- Recommended modules (OPTIONAL) - Complementary modules
- Example code (OPTIONAL) - Code examples
- Similar projects (OPTIONAL) - Alternatives and differentiators
- Basic Services (OPTIONAL if MODULE.services.yml exists)
- Extend and override (RECOMMENDED)
- Supporting this Module (OPTIONAL)
- Contributing (OPTIONAL)
- Community Documentation (OPTIONAL)

**Prohibited Content**:
- File structure diagrams/sections
- Installation instructions (composer require, drush en)
- "How to install" sections
- Beginner-friendly explanations

### 4. Generate GitLab CI Configuration

**Prompt**: "Add GitLab CI configuration to my module"

**Process**:
1. Fetch latest Drupal Association .gitlab-ci.yml template
2. Configure for module type (not Drupal 7)
3. Set appropriate PHP versions based on core_version_requirement
4. Include default testing jobs (phpunit, phpcs, phpstan)
5. Configure for Drupal 10/11 testing

**Generated .gitlab-ci.yml** includes:
- Composer validation
- PHP syntax linting
- PHPCS with Drupal standards
- PHPStan static analysis
- PHPUnit tests (if tests/ directory exists)
- Multiple PHP version testing

### 5. Validate Coding Standards

**Prompt**: "Check my module against Drupal coding standards"

**Process**:
1. Detect available tools (phpcs, phpstan, phpcbf)
2. Run PHPCS with Drupal and DrupalPractice standards
3. Run PHPStan if configuration exists
4. Parse errors and warnings
5. Provide specific file/line fixes

**Commands Used** (if available):
```bash
vendor/bin/phpcs --standard=Drupal,DrupalPractice
vendor/bin/phpstan analyze
vendor/bin/phpcbf --standard=Drupal,DrupalPractice
```

## Available Scripts

### `scripts/validate_module.py`

Main validation script that performs comprehensive module analysis.

**Usage**:
```bash
python3 scripts/validate_module.py /path/to/module
```

**Returns**:
```python
{
    "status": "PASS" | "FAIL",
    "missing_files": ["list", "of", "missing"],
    "incomplete_files": {"file": "issues"},
    "recommendations": ["list", "of", "fixes"],
    "module_info": {
        "name": "module_name",
        "description": "Module description",
        "dependencies": ["list"],
        "core_version": "^10.1 || ^11"
    }
}
```

### `scripts/generate_files.py`

Generates missing files based on module analysis.

**Usage**:
```bash
python3 scripts/generate_files.py /path/to/module --readme --gitlab-ci --logo
```

**Options**:
- `--readme`: Generate README.md
- `--gitlab-ci`: Generate .gitlab-ci.yml
- `--logo`: Create placeholder logo instructions
- `--all`: Generate all missing files

### `scripts/check_readme.py`

Validates README.md structure and content.

**Usage**:
```bash
python3 scripts/check_readme.py /path/to/module/README.md
```

**Checks**:
- Required sections present
- No prohibited sections
- Code examples use Drupal coding standards
- Content targets experienced developers

### `scripts/generate_gitlab_ci.py`

Generates .gitlab-ci.yml from Drupal Association template.

**Usage**:
```bash
python3 scripts/generate_gitlab_ci.py /path/to/module
```

**Features**:
- Uses latest Drupal Association template
- Configures for module type
- Sets appropriate PHP versions
- Includes default testing jobs

### `scripts/apply_coding_standards.py`

Checks and fixes coding standards violations.

**Usage**:
```bash
python3 scripts/apply_coding_standards.py /path/to/module
```

**Actions**:
- Runs PHPCS validation
- Auto-fixes with PHPCBF
- Runs PHPStan if configured
- Generates report

## Available Analyses

### Module Structure Validation

Analyzes the complete module directory structure against Drupal.org requirements.

**Checks**:
- .info.yml file exists and is valid YAML
- README.md exists with required sections
- logo.png exists (recommended dimensions)
- .gitlab-ci.yml exists with valid syntax
- composer.json exists (recommended)
- No LICENSE file (Drupal.org adds automatically)
- Proper PSR-4 structure in src/

### README Content Analysis

Detailed analysis of README.md content quality and compliance.

**Metrics**:
- Section completeness (required sections)
- Content appropriateness (experienced developers)
- Code example quality (Drupal standards)
- Prohibited content detection
- Readability and clarity

### Dependency Analysis

Extracts and validates module dependencies from .info.yml.

**Checks**:
- All dependencies exist (if checking within Drupal codebase)
- Versions specified appropriately
- No conflicts between dependencies
- Composer dependencies align with .info.yml

### GitLab CI Validation

Validates .gitlab-ci.yml configuration.

**Checks**:
- Valid YAML syntax
- Includes Drupal Association template
- Configured for correct Drupal version
- Appropriate PHP versions
- Required jobs defined

### Coding Standards Report

Generates comprehensive coding standards report.

**Includes**:
- PHPCS errors and warnings by file
- PHPStan analysis results
- Auto-fix suggestions
- Severity levels

## Error Handling

### Module Not Found
```
Error: Module directory not found at /path/to/module
Please provide a valid Drupal module directory containing a .info.yml file.
```

### Invalid Info File
```
Error: Invalid .info.yml file
The file at module_name.info.yml contains invalid YAML or missing required keys.
Required keys: name, type, description, core_version_requirement
```

### GitLab CI Template Fetch Failed
```
Warning: Could not fetch latest GitLab CI template
Using cached template. Some features may be outdated.
```

### PHPCS Not Available
```
Warning: PHPCS not found at vendor/bin/phpcs
Skipping coding standards check. Install with:
composer require --dev drupal/coder
```

## Mandatory Validations

### Info File Validation

Every module MUST have a valid .info.yml file with:

```yaml
name: 'Module Name'
type: module
description: 'Brief description'
core_version_requirement: ^10.1 || ^11
package: Custom
# Optional but recommended:
# dependencies:
#   - node:node
# configure: module.settings
```

### README Section Validation

README.md MUST contain (in order):
1. About section (module purpose)
2. Basic usage (how to use)
3. Basic Services (if services.yml exists)
4. Extend and override (hooks/events)
5. Security notices (if applicable)

README.md MUST NOT contain:
- File structure diagrams
- Installation instructions
- "How to install" sections

### GitLab CI Validation

.gitlab-ci.yml MUST:
- Include Drupal Association template
- Be valid YAML
- Configure for Drupal 10/11 (not Drupal 7)

## Performance and Cache

The validator caches:
- Drupal Association GitLab CI template (24 hours)
- Module validation results (until files change)
- PHPCS baseline (first run)

Cache location: `~/.cache/drupal-contrib-validator/`

## Keywords for Automatic Activation

This skill activates when you mention:

**Drupal module validation**:
- "validate drupal module"
- "check module for drupal.org"
- "validate contrib module"
- "module contribution ready"
- "drupal module standards"

**File generation**:
- "generate drupal module files"
- "scaffold drupal module"
- "add gitlab ci to module"
- "create readme for drupal module"
- "add logo to drupal module"

**Coding standards**:
- "check drupal coding standards"
- "validate module against phpcs"
- "phpcs my module"
- "fix coding standards"

**Negative scope** (won't activate):
- "create a new drupal module" (use different skill)
- "how to write drupal code" (educational question)
- "drupal core development" (different scope)

## Usage Examples

### Example 1: Validate Current Module

**User**: "Is my graphql_compose_debug module ready for Drupal.org?"

**Claude**: I'll validate your module for Drupal.org contribution readiness.

[Runs validation]

**Result**:
```
❌ VALIDATION FAILED for graphql_compose_debug

Missing Required Files:
- README.md
- logo.png
- .gitlab-ci.yml

Info File: ✅ Valid
- Name: GraphQL Compose: Debug
- Core: ^10.1 || ^11
- Dependencies: graphql, graphql_compose

Recommendations:
1. Add README.md with sections: About, Basic usage, Extend and override
2. Add logo.png (120x120px recommended)
3. Generate .gitlab-ci.yml for automated testing

Would you like me to generate these files? Type "generate" to proceed.
```

### Example 2: Generate Missing Files

**User**: "Generate all missing files for my module"

**Claude**: I'll generate the missing files for your module.

[Generates files]

**Result**:
```
✅ Generated 3 files:

1. README.md (245 words)
   - About: Debug queries for GraphQL Compose entity fields
   - Basic usage: Usage examples for developers
   - Extend and override: Hook documentation

2. .gitlab-ci.yml (from Drupal Association template)
   - PHP 8.1, 8.2, 8.3 testing
   - PHPCS with Drupal standards
   - PHPUnit tests

3. logo-instructions.txt
   - Your logo is missing
   - Recommended: 120x120px PNG
   - Place as: logo.png in module root

Next steps:
1. Review README.md and customize for your module
2. Create or source a logo.png file
3. Commit .gitlab-ci.yml and test on GitLab
```

### Example 3: Check README Compliance

**User**: "Check if my README.md follows Drupal.org guidelines"

**Claude**: I'll validate your README.md against Drupal.org contribution guidelines.

[Analyzes README]

**Result**:
```
✅ README.md VALIDATION PASSED

Required Sections: ✅ All present
- About section
- Basic usage section
- Extend and override section

Content Quality: ✅ Good
- Targets experienced developers
- No installation instructions
- No file structure section
- Code examples follow Drupal standards

Recommendations:
- Consider adding "Security notices" section if applicable
- Add more usage examples for complex features

Status: READY FOR DRUPAL.ORG
```

### Example 4: Add GitLab CI

**User**: "Add GitLab CI to my module"

**Claude**: I'll add GitLab CI configuration using the Drupal Association template.

[Generates .gitlab-ci.yml]

**Result**:
```
✅ Created .gitlab-ci.yml

Configuration:
- Template: Drupal Association v1.0.x
- Drupal versions: 10.3, 11.0
- PHP versions: 8.1, 8.2, 8.3
- Jobs: composer, phpunit, phpcs, phpstan

Next steps:
1. Review .gitlab-ci.yml
2. Push to your GitLab repository
3. Verify pipeline runs successfully

View pipelines at: https://git.drupalcode.org/PROJECT/-/pipelines
```

### Example 5: Validate Coding Standards

**User**: "Check my module for coding standards violations"

**Claude**: I'll run Drupal coding standards checks on your module.

[Runs PHPCS and PHPStan]

**Result**:
```
❌ CODING STANDARDS ISSUES FOUND

PHPCS Results: 3 errors, 7 warnings

Errors:
- src/Controller/DebugController.php:45 - Line exceeds 80 characters
- src/Plugin/GraphQL/DataProducer/Debug.php:78 - Missing function comment
- graphql_compose_debug.permissions.yml:3 - Invalid YAML indentation

Warnings:
- graphql_compose_debug.info.yml:5 - Missing 'package' key
- src/Controller/DebugController.php:23 - Unused variable $debug

PHPStan: 0 errors

Auto-fix available? Yes
Run: vendor/bin/phpcbf --standard=Drupal,DrupalPractice

Would you like me to apply auto-fixes?
```

## Troubleshooting

### Validation Passes But Module Rejected

If your module passes validation but is rejected from Drupal.org:

1. **Manual Review Required**: Some issues require human review
2. **GitLab CI Failures**: Check your pipeline results on git.drupalcode.org
3. **Namespace Issues**: Ensure composer.json has proper autoload
4. **Security Issues**: Run security advisor: `composer audit`

### README.md Always Fails

Common README.md issues:
- **File structure section**: Remove any file/folder diagrams
- **Installation instructions**: Remove "How to install" sections
- **Beginner content**: Rewrite for experienced Drupal developers
- **Missing sections**: Ensure About, Basic usage, Extend and override exist

### GitLab CI Fails on GitLab

Common GitLab CI issues:
- **Template outdated**: Regenerate from latest template
- **PHP version mismatch**: Update `core_version_requirement` in info.yml
- **Missing composer.lock**: Run `composer update` and commit
- **Tests fail**: Fix failing tests locally first with `vendor/bin/phpunit`

## Advanced Features

### Batch Validation

Validate multiple modules at once:

```bash
find web/modules/custom -name "*.info.yml" -exec \
  python3 scripts/validate_module.py {} \;
```

### CI/CD Integration

Add to your project's CI:

```yaml
validate-contrib:
  script:
    - python3 /path/to/drupal-contrib-validator/scripts/validate_module.py .
  artifacts:
    reports:
      junit: validation-report.xml
```

### Custom Configuration

Create `~/.drupal-contrib-validator.json`:

```json
{
  "phpcs_standard": "Drupal,DrupalPractice",
  "skip_phpstan": false,
  "logo_dimensions": "120x120",
  "required_readme_sections": ["About", "Basic usage", "Extend and override"]
}
```

---

**Version**: 1.0.0
**Last Updated**: 2025-01-21
**Drupal Version**: 10.1+, 11.0+
**Python**: 3.8+