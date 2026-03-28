# Troubleshooting Guide

This guide helps resolve common issues when validating Drupal modules for Drupal.org contribution.

## Validation Fails

### Symptom: Required files missing

**Error:**
```
❌ VALIDATION FAILED
Missing Required Files:
- README.md
- logo.png
- .gitlab-ci.yml
```

**Solution:**
Generate missing files using the generator:
```bash
python3 scripts/generate_files.py /path/to/module --all
```

### Symptom: README.md sections missing

**Error:**
```
README.md Issues:
- Missing required section: About
- Missing required section: Basic usage
```

**Solution:**
Update README.md to include required sections. Use the generator as a template:
```bash
python3 scripts/generate_files.py /path/to/module --readme
```
Then customize the generated README.md for your module.

### Symptom: README.md contains prohibited content

**Error:**
```
README.md Issues:
- Contains prohibited content: 'installation instructions'
- Contains prohibited content: 'composer require'
```

**Solution:**
Remove prohibited sections from README.md:
- Delete "How to install" sections
- Remove `composer require` instructions
- Remove file structure diagrams
- Remove `drush en` instructions

Drupal.org provides installation instructions automatically.

### Symptom: LICENSE file exists

**Error:**
```
⚠ Prohibited file found: LICENSE (Drupal.org adds LICENSE)
```

**Solution:**
Delete the LICENSE file:
```bash
rm LICENSE
```

Drupal.org automatically injects the GPL LICENSE when packaging releases.

## GitLab CI Issues

### Symptom: .gitlab-ci.yml has invalid YAML

**Error:**
```
⚠ Not using Drupal Association template
❌ Invalid YAML: syntax error
```

**Solution:**
Regenerate .gitlab-ci.yml using the generator:
```bash
python3 scripts/generate_files.py /path/to/module --gitlab-ci
```

### Symptom: Pipeline fails on GitLab

**Error:**
```
Job failed: composer
Job failed: phpunit
```

**Solutions:**

1. **Update composer.lock:**
```bash
composer update
composer require drupal/core-dev --dev
git add composer.lock
git commit -m "Update composer.lock"
```

2. **Fix failing tests locally:**
```bash
ddev drush en simpletest
ddev exec vendor/bin/phpunit
```

3. **Use ddev-drupal-contrib:**
```bash
ddev drupal-contrib
ddev drupal-contrib run composer
```

### Symptom: PHP version mismatch

**Error:**
```
PHP version not compatible with core_version_requirement
```

**Solution:**

Update .gitlab-ci.yml `_TARGET_PHP` to match:
- Drupal 10: 8.1, 8.2, 8.3
- Drupal 11: 8.2, 8.3+

Or update `core_version_requirement` in .info.yml.

## Coding Standards Issues

### Symptom: PHPCS errors

**Error:**
```
PHPCS: 15 errors, 32 warnings
```

**Solution:**

1. **Auto-fix what you can:**
```bash
vendor/bin/phpcbf --standard=Drupal,DrupalPractice
```

2. **Check remaining issues:**
```bash
vendor/bin/phpcs --standard=Drupal,DrupalPractice
```

3. **Fix manually:**
   - Indentation: Use 2 spaces (not tabs)
   - Line length: Keep under 80 characters
   - Naming: Use snake_case for functions

### Symptom: PHPStan errors

**Error:**
```
PHPStan: 5 errors
```

**Solution:**

1. **Review errors:**
```bash
vendor/bin/phpstan analyze
```

2. **Add baseline (if needed):**
```bash
vendor/bin/phpstan analyze --generate-baseline
```

3. **Fix type issues:**
   - Add proper type hints
   - Fix null references
   - Add `@var` annotations

### Symptom: phpcs.xml not found

**Error:**
```
Could not find phpcs.xml
```

**Solution:**

Create a custom phpcs.xml:
```xml
<?xml version="1.0"?>
<ruleset name="Drupal Module">
  <description>Custom coding standards</description>
  <rule ref="Drupal"/>
  <rule ref="DrupalPractice"/>
  <file>./</file>
  <exclude-pattern>*/vendor/*</exclude-pattern>
</ruleset>
```

## Module Structure Issues

### Symptom: PSR-4 autoloading fails

**Error:**
```
Class not found: Drupal\my_module\Service\MyService
```

**Solution:**

1. **Check composer.json:**
```json
{
  "autoload": {
    "psr-4": {
      "Drupal\\MyModule\\": "src/"
    }
  }
}
```

2. **Verify namespace:**
- Class: `Drupal\my_module\Service\MyService`
- File: `src/Service/MyService.php`
- Namespace: `namespace Drupal\my_module\Service;`

3. **Regenerate autoload:**
```bash
composer dump-autoload
```

### Symptom: Hook not called

**Symptom:** Hook in .module file not executing.

**Solution:**

1. **Clear cache:**
```bash
drush cr
```

2. **Verify function name:**
```php
function my_module_help($route_name) {
  // Correct: module machine name
}

function MY_MODULE_help($route_name) {
  // WRONG: all caps
}
```

3. **Check .module file exists:**
The .module file must exist (can be empty) for hooks to work.

## GitLab CI Testing Locally

### Method 1: ddev-drupal-contrib (Recommended)

**Install:**
```bash
ddev add-on get ddev-drupal-contrib
ddev restart
```

**Use:**
```bash
ddev drupal-contrib run composer
ddev drupal-contrib run phpunit
ddev drupal-contrib run phpcs
```

### Method 2: gitlab-ci-local

**Install:**
```bash
npm install -g gitlab-ci-local
```

**Use:**
```bash
gitlab-ci-local --remote-variables \
  git@git.drupal.org:project/gitlab_templates=includes/include.drupalci.variables.yml=1.0.x \
  --variable="_GITLAB_TEMPLATES_REPO=project/gitlab_templates"
```

### Method 3: Manual Testing

**Composer:**
```bash
composer validate --strict
```

**PHPCS:**
```bash
vendor/bin/phpcs --standard=Drupal,DrupalPractice
```

**PHPStan:**
```bash
vendor/bin/phpstan analyze
```

**PHPUnit:**
```bash
ddev exec vendor/bin/phpunit
```

## Common Validation Errors

### Error: "Invalid YAML in .info.yml"

**Cause:** YAML syntax error in .info.yml file.

**Solution:**
```bash
# Check YAML syntax
python3 -c "import yaml; yaml.safe_load(open('MODULE.info.yml'))"

# Common fixes:
# - Use spaces, not tabs (2 spaces per level)
# - Quote strings with special characters
# - Ensure proper list formatting
```

### Error: "Missing required key: core_version_requirement"

**Cause:** Old Drupal 8/9 style .info.yml.

**Solution:**
Add to .info.yml:
```yaml
core_version_requirement: ^10.1 || ^11
```

Remove deprecated:
```yaml
core: 8.x
core_version_requirement: ^8 || ^9
```

### Error: "Package key missing"

**Cause:** No `package` key in .info.yml.

**Solution:**
Add to .info.yml:
```yaml
package: Custom  # or descriptive category
```

## Debugging Tips

### Enable verbose output

```bash
python3 scripts/validate_module.py /path/to/module --verbose
```

### Check file permissions

```bash
ls -la /path/to/module
```

Ensure files are readable:
```bash
chmod +r README.md
```

### Validate YAML syntax

```bash
# Python
python3 -c "import yaml; print(yaml.safe_load(open('file.yml')))"

# Online
# https://www.yamllint.com/
```

### Check PHP syntax

```bash
php -l src/Controller/MyController.php
```

## Getting Help

### Drupal.org Resources

- **GitLab CI Slack:** #gitlab channel on Drupal Slack
- **Issue Queue:** https://www.drupal.org/project/issues/gitlab_templates
- **Documentation:** https://www.drupal.org/docs/develop/git

### Local Validation

Before pushing to GitLab:
1. Run validation: `python3 scripts/validate_module.py .`
2. Generate missing files
3. Test locally with ddev-drupal-contrib
4. Review generated files
5. Commit and push

### When All Else Fails

1. **Start fresh:**
   - Delete .gitlab-ci.yml
   - Regenerate using this tool
   - Compare with working modules

2. **Check examples:**
   - https://git.drupalcode.org/project/views
   - https://git.drupalcode.org/project/token
   - https://git.drupalcode.org/project/pathauto

3. **Ask for help:**
   - Drupal Slack: #contribute channel
   - Drupal.org forum: https://www.drupal.org/forum