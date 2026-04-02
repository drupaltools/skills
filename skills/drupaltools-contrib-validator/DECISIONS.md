# Architecture Decisions

This document records all architectural and design decisions made during the development of drupal-contrib-validator.

## Technology Choices

### Python 3.8+

**Decision:** Use Python 3.8+ as the primary implementation language.

**Justification:**
- Python is pre-installed on most development systems
- Excellent YAML parsing via PyYAML
- Cross-platform compatibility (Linux, macOS, Windows)
- Easy integration with CI/CD systems
- Simple CLI argument parsing with argparse

**Alternatives considered:**
- **Bash scripting:** Rejected due to poor YAML handling and error-prone text processing
- **PHP:** Rejected because Drupal modules use PHP, but validation tools shouldn't require PHP runtime
- **Node.js:** Rejected because Python is more commonly available on developer systems

### YAML Configuration

**Decision:** Use YAML for all configuration files (.info.yml, .gitlab-ci.yml parsing).

**Justification:**
- Drupal's standard configuration format
- Human-readable and editable
- PyYAML provides robust parsing
- Industry standard for CI/CD configuration

**Alternatives considered:**
- **JSON:** Rejected because .info.yml and .gitlab-ci.yml are YAML
- **TOML:** Not used by Drupal ecosystem

## Module Detection

### Directory-Based Detection

**Decision:** Detect modules by scanning directories for `.info.yml` files.

**Justification:**
- Follows Drupal's module discovery mechanism
- Works with custom modules and contributed modules
- No external metadata required
- Handles nested structures correctly

**Detection logic:**
```python
info_files = list(module_path.glob('*.info.yml'))
if info_files:
    module_info = parse_info_yaml(info_files[0])
```

**Alternatives considered:**
- **Composer.json detection:** Rejected because not all modules have composer.json
- **Naming convention:** Rejected because not all modules follow machine_name pattern

### Multiple .info.yml Handling

**Decision:** If multiple .info.yml files exist, use the first one and warn.

**Justification:**
- Rare case (typically sub-modules have their own directories)
- Warning alerts user to potential issue
- First file is usually the main module

## Validation Strategy

### Fail-Fast Approach

**Decision:** Stop validation if .info.yml is missing or invalid.

**Justification:**
- .info.yml is the only truly required file
- Without it, can't determine module name or dependencies
- Clear error message helps user fix fundamental issue first

**Implementation:**
```python
if not info_file:
    self._add_error('Missing required .info.yml file')
    return self.validation_results
```

**Alternatives considered:**
- **Continue validation:** Rejected because results would be meaningless without module context
- **Interactive prompt:** Rejected because CLI should be non-interactive

### Section-Based README Validation

**Decision:** Validate README by checking for section headers, not full content.

**Justification:**
- Case-insensitive section matching
- Allows flexible formatting
- User can customize content
- Fast and reliable

**Implementation:**
```python
for section in REQUIRED_SECTIONS:
    if section.lower() not in content_lower:
        missing_sections.append(section)
```

**Alternatives considered:**
- **Full content parsing:** Rejected because too restrictive
- **AI-based analysis:** Rejected because overkill and unreliable

## File Generation Strategy

### Template-Based Generation

**Decision:** Generate files using templates with variable substitution.

**Justification:**
- Consistent output format
- Easy to maintain templates
- User can customize after generation
- Fast and reliable

**Template example:**
```python
content = f"""# {name}

About
-----
{description}

Basic usage
------------
{get_usage_content()}
"""
```

**Alternatives considered:**
- **Interactive generation:** Rejected because Claude should handle interaction
- **AI-based generation:** Rejected because templates produce more consistent results

### Non-Destructive Generation

**Decision:** Never overwrite existing files.

**Justification:**
- Preserves user customizations
- Prevents accidental data loss
- Clear communication about what was generated

**Implementation:**
```python
if readme_path.exists():
    print("⚠ README.md already exists. Skipping.")
    return
```

**Alternatives considered:**
- **Overwrite with backup:** Rejected because adds complexity
- **Interactive overwrite prompt:** Rejected because CLI should be non-interactive

## GitLab CI Integration

### Drupal Association Template

**Decision:** Use Drupal Association's official .gitlab-ci.yml template as base.

**Justification:**
- Official Drupal.org standard
- Automatically updated by Drupal Association
- Includes all necessary test jobs
- Supports multiple PHP and Drupal versions

**Template source:**
```yaml
include:
  - project: 'project/gitlab_templates'
    ref: 1.0.x
    file:
      - '/includes/include.drupalci.variables.yml'
      - '/includes/include.drupalci.workflows.yml'
      - '/includes/include.drupalci.main.yml'
```

**Alternatives considered:**
- **Custom .gitlab-ci.yml:** Rejected because maintenance burden
- **Travis CI:** Rejected because Drupal.org uses GitLab CI

### PHP Version Detection

**Decision:** Determine PHP versions from `core_version_requirement` in .info.yml.

**Justification:**
- Automatic and accurate
- No manual configuration needed
- Changes when core version requirement changes

**Implementation:**
```python
if '^11' in core_version:
    php_versions = ['8.2', '8.3']
elif '^10' in core_version:
    php_versions = ['8.1', '8.2', '8.3']
```

**Alternatives considered:**
- **Hardcoded versions:** Rejected because requires manual updates
- **All PHP versions:** Rejected because wastes CI resources

## Coding Standards Integration

### Optional Tool Detection

**Decision:** Check for PHPCS and PHPStan but don't require them.

**Justification:**
- Not all development environments have these tools
- Module can be validated without them
- Clear warning when tools are missing
- Allows basic validation anywhere

**Implementation:**
```python
phpcs_path = Path('vendor/bin/phpcs')
if phpcs_path.exists():
    # Run PHPCS
else:
    print("⚠ PHPCS not found. Skipping coding standards check.")
```

**Alternatives considered:**
- **Bundle tools:** Rejected because adds skill size
- **Require tools:** Rejected because limits usability
- **Install automatically:** Rejected because requires composer/pip

## Output Format

### Human-Readable Primary

**Decision:** Default to human-readable text output.

**Justification:**
- Easier for users to understand
- Clear action items
- Suitable for interactive use
- Better error messages

**Example:**
```
❌ VALIDATION FAILED

Missing Required Files:
- README.md
- logo.png

Recommendations:
- Add README.md with required sections
- Add logo.png (120x120px recommended)
```

**Alternatives considered:**
- **JSON only:** Rejected because not human-readable
- **XML:** Rejected because verbose and complex

### JSON Optional

**Decision:** Provide JSON output via `--json` flag for CI/CD integration.

**Justification:**
- Machine-readable for automation
- Easy to parse in scripts
- CI/CD systems can consume results
- Doesn't interfere with human use

**Implementation:**
```python
if args.json:
    print(json.dumps(results, indent=2))
else:
    validator.print_results()
```

## Error Handling

### Graceful Degradation

**Decision:** Continue validation when possible, fail gracefully when not.

**Justification:**
- Partial results better than no results
- User can see what passed and what failed
- Clear separation of critical and optional issues

**Implementation:**
```python
try:
    self._validate_readme()
except Exception as e:
    self.validation_results['readme_issues'].append(f"Error: {e}")
```

**Alternatives considered:**
- **Fail on any error:** Rejected because hides useful information
- **Silent failures:** Rejected because user doesn't know what happened

## File Structure

### Flat Script Structure

**Decision:** Keep scripts in flat `scripts/` directory, no nested packages.

**Justification:**
- Simple to understand
- Easy to maintain
- No complex imports needed
- Suitable for skill size

**Structure:**
```
scripts/
├── validate_module.py
├── generate_files.py
```

**Alternatives considered:**
- **Package structure:** Rejected because overkill for skill size
- **Monolithic script:** Rejected because harder to maintain

## Dependencies

### Minimal External Dependencies

**Decision:** Only require PyYAML for YAML parsing.

**Justification:**
- YAML parsing is non-trivial to implement correctly
- PyYAML is stable and widely-used
- All other functionality uses Python stdlib
- Easy installation: `pip install pyyaml`

**Stdlib modules used:**
- `argparse` - CLI parsing
- `json` - JSON output
- `pathlib` - Path operations
- `re` - Regular expressions
- `sys` - System operations

**Alternatives considered:**
- **No external dependencies:** Rejected because YAML parsing is complex
- **Many dependencies:** Rejected because increases installation burden

## Trade-offs Documented

### Logo Generation

**Decision:** Generate instructions for logo.png, not actual image.

**Trade-off:**
- ✅ No external image library dependencies
- ✅ Clear instructions for user
- ❌ User must create or source logo
- ❌ Not fully automated

**Justification:**
- Logo creation is design work, not automation
- Image libraries add complexity and dependencies
- Users prefer to create their own logos

### LICENSE Detection

**Decision:** Warn about LICENSE file but don't auto-delete.

**Trade-off:**
- ✅ Safe (doesn't delete files)
- ✅ Clear warning about Drupal.org behavior
- ❌ User must manually delete
- ❌ Validation might not pass on first run

**Justification:**
- Never delete files without explicit user action
- Clear warning is sufficient for users to fix