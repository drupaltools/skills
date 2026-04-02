# Drupal Contrib Validator

Validates Drupal 10+ custom modules for Drupal.org contribution readiness. Checks required files, generates missing files, and ensures compliance with Drupal coding standards.

## Features

- **File Structure Validation** - Ensures all required files are present (.info.yml, README.md, logo.png, .gitlab-ci.yml)
- **README.md Analysis** - Validates README structure and content against Drupal.org guidelines
- **GitLab CI Generation** - Creates .gitlab-ci.yml using Drupal Association template
- **File Scaffolding** - Generates missing files automatically
- **Coding Standards** - Checks PHPCS and PHPStan when available
- **Professional Output** - Clear, actionable feedback with specific recommendations

## Installation

### Via Claude Code Marketplace (Recommended)

```bash
/plugin marketplace add drupal-contrib-validator
```

### Manual Installation

```bash
# Clone or download this skill
mkdir -p ~/.claude/skills
cp -r drupal-contrib-validator-cskill ~/.claude/skills/

# Install Python dependencies (optional, for advanced usage)
pip3 install pyyaml
```

## Usage

### Basic Validation

Validate the current directory:

```
"Is my module ready for Drupal.org?"
"Validate my Drupal module for contribution"
"Check module for drupal.org"
```

### Generate Missing Files

Generate all missing required files:

```
"Generate missing files for my module"
"Add gitlab ci to my module"
"Scaffold drupal module"
```

### Specific Validations

Validate README.md specifically:

```
"Check my README.md for Drupal.org compliance"
"Validate readme structure"
```

Check coding standards:

```
"Check my module for coding standards violations"
"Validate module against phpcs"
"Fix coding standards"
```

## Scripts

### validate_module.py

Main validation script. Performs comprehensive module analysis.

```bash
python3 scripts/validate_module.py /path/to/module
python3 scripts/validate_module.py .  # Current directory
python3 scripts/validate_module.py . --json  # JSON output
```

**Exit codes:**
- 0: Validation passed
- 1: Validation failed

### generate_files.py

Generate missing files automatically.

```bash
python3 scripts/generate_files.py /path/to/module --readme
python3 scripts/generate_files.py /path/to/module --gitlab-ci
python3 scripts/generate_files.py /path/to/module --logo
python3 scripts/generate_files.py /path/to/module --all  # All files
```

## Validation Criteria

### Required Files

| File | Status | Description |
|------|--------|-------------|
| `MODULE.info.yml` | **REQUIRED** | Module definition file |
| `README.md` | **REQUIRED** | Documentation for developers |
| `logo.png` | **REQUIRED** | Module logo (120x120px recommended) |
| `.gitlab-ci.yml` | **REQUIRED** | GitLab CI configuration |

### Required README Sections

- **About** - Module description for experienced developers
- **Basic usage** - How to use the module (NO installation instructions)
- **Extend and override** - Hooks, events, and extension points
- **Basic Services** - Required only if `.services.yml` exists
- **Security notices** - Optional but recommended

### Prohibited README Content

- File structure diagrams
- Installation instructions ("How to install")
- `composer require` examples
- `drush en` examples
- Beginner-friendly explanations

## Example Output

### Validation Passed

```
============================================================
DRUPAL CONTRIB MODULE VALIDATOR
============================================================
Module: my_module
Path: /var/www/html/web/modules/custom/my_module
============================================================

✅ Info file: my_module.info.yml
   Name: My Module
   Core: ^10.1 || ^11
   PHP: 8.1
✅ Found: README.md
✅ Found: logo.png
✅ Found: .gitlab-ci.yml

📄 Validating README.md...
  ✅ Found section: About
  ✅ Found section: Basic usage
  ✅ Found section: Extend and override
  ℹ️ 'Basic Services' section not needed (no services.yml)

🔄 Validating .gitlab-ci.yml...
  ✅ Uses Drupal Association template

============================================================
✅ VALIDATION PASS
============================================================

✅ Module is ready for Drupal.org contribution!
```

### Validation Failed

```
============================================================
❌ VALIDATION FAIL
============================================================

Missing Required Files:
  - README.md
  - logo.png
  - .gitlab-ci.yml

Recommendations:
  - Add README.md with sections: About, Basic usage, Extend and override
  - Add logo.png (120x120px recommended)
  - Generate .gitlab-ci.yml for automated testing

Type "generate" to create missing files automatically.
```

## Testing

### Test with Example Module

```bash
# Clone a test module
cd /tmp
git clone https://git.drupalcode.org/project/views.git

# Validate
python3 ~/.claude/skills/drupal-contrib-validator-cskill/scripts/validate_module.py views
```

### Test Local Module

```bash
# Navigate to your module
cd web/modules/custom/my_module

# Validate
python3 ~/.claude/skills/drupal-contrib-validator-cskill/scripts/validate_module.py .
```

## Requirements

- Python 3.8+
- PyYAML (optional, for .info.yml parsing)
- PHPCS (optional, for coding standards checks)
- PHPStan (optional, for static analysis)

## Integration with CI/CD

### GitLab CI Example

Add to your project's `.gitlab-ci.yml`:

```yaml
validate-contrib:
  stage: test
  script:
    - python3 /path/to/validate_module.py .
  artifacts:
    reports:
      junit: validation-report.xml
```

### GitHub Actions Example

```yaml
name: Validate Drupal Module

on: [push, pull_request]

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Validate Module
        run: |
          python3 scripts/validate_module.py .
```

## Troubleshooting

### Module Not Found

**Error:** `Module directory not found`

**Solution:** Ensure you're pointing to a valid module directory containing a `.info.yml` file.

### Invalid Info File

**Error:** `Invalid .info.yml file`

**Solution:** Check YAML syntax. Use 2 spaces for indentation, not tabs.

### GitLab CI Template Fetch Failed

**Error:** `Could not fetch latest GitLab CI template`

**Solution:** Check internet connection. The tool uses a cached template as fallback.

### PHPCS Not Available

**Warning:** `PHPCS not found at vendor/bin/phpcs`

**Solution:** Install with:
```bash
composer require --dev drupal/coder
```

## Contributing

This skill is part of the Claude Code ecosystem. To contribute improvements:

1. Fork the skill repository
2. Make your changes
3. Test with various Drupal modules
4. Submit a pull request

## Resources

- [Drupal.org: Creating Modules](https://www.drupal.org/docs/develop/creating-modules)
- [Drupal.org: GitLab CI](https://www.drupal.org/node/3356364)
- [Drupal Coding Standards](https://project.pages.drupalcode.org/coding_standards)
- [GitLab Templates](https://git.drupalcode.org/project/gitlab_templates)

## License

GPL-2.0-or-later

## Version

1.0.0