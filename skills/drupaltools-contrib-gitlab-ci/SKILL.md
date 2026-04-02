---
name: drupaltools-contrib-gitlab-ci
description: Generate and validate .gitlab-ci.yml files for Drupal modules using Drupal Association templates. Use this skill when you need to create GitLab CI configuration, update existing CI, or validate CI setup for a Drupal module.
---

# Drupal GitLab CI Generator

Generate `.gitlab-ci.yml` configuration for Drupal modules using the official Drupal Association template.

## When to Use

Use this skill when:
- "Add GitLab CI to my module"
- "Generate .gitlab-ci.yml for Drupal"
- "Update CI configuration"
- "Validate CI setup"

## Process

### 1. Detect Drupal Version

Read `MODULE.info.yml` to determine `core_version_requirement`:

```bash
grep "core_version_requirement" MODULE.info.yml
```

### 2. Determine PHP Versions

| Drupal Version | PHP Versions |
|---------------|-------------|
| ^10 | 8.1, 8.2, 8.3 |
| ^11 | 8.2, 8.3, 8.4 |

### 3. Fetch Template

Fetch the official Drupal Association template:

```bash
curl -sS "https://git.drupalcode.org/project/gitlab_templates/-/raw/1.0.x/gitlab-templates/.gitlab-ci.yml"
```

### 4. Generate Configuration

The generated `.gitlab-ci.yml` includes:

| Job | Purpose |
|-----|---------|
| `composer_validate` | Validate composer.json |
| `php_syntax` | PHP syntax checking |
| `phpcs` | Drupal coding standards (PHPCS) |
| `phpstan` | Static analysis (PHPStan) |
| `phpunit` | Unit tests (if tests/ exists) |

## Template Structure

```yaml
image: git.drupal.orgqa/travis-ci:latest

stages:
  - Static analysis
  - Testing

variables:
  SIMPLETEST: "https://git.drupalcode.org/project/drupal.git"
  # ...

phpcs:
  stage: Static analysis
  script:
    - composer install --no-interaction
    - composer validate --strict
    - ./vendor/bin/phpcs --standard=Drupal,DrupalPractice --extensions=php,module,inc,install,test,profile,theme,css,info,txt,md,yml

phpstan:
  stage: Static analysis
  script:
    - composer install --no-interaction
    - ./vendor/bin/phpstan analyse --no-progress

phpunit:
  stage: Testing
  script:
    - composer install --no-interaction
    - ./vendor/bin/phpunit --configuration=phpunit.xml
```

## Customization

### Enable PHPUnit

If your module has tests:

```bash
ls tests/ 2>/dev/null && echo "has_tests"
```

### PHP Version Matrix

```yaml
phpunit:
  stage: Testing
  matrix:
    - PHP_VERSION: "8.1"
    - PHP_VERSION: "8.2"  
    - PHP_VERSION: "8.3"
```

### Drupal Version Matrix

```yaml
phpcs:
  stage: Static analysis
  matrix:
    - Drupal: "10.3"
    - Drupal: "11.0"
```

## Validate Existing CI

Check if `.gitlab-ci.yml` is properly configured:

1. **Template included** - Uses Drupal Association template
2. **Valid YAML** - Passes `yamllint`
3. **Correct Drupal version** - Configured for D10/D11
4. **Jobs defined** - PHPCS, PHPStan, PHPUnit present

## Common Issues

| Issue | Solution |
|-------|----------|
| Template outdated | Regenerate from latest template |
| PHP version mismatch | Update based on `core_version_requirement` |
| Missing composer.lock | Run `composer update` and commit |
| Tests fail | Fix locally with `vendor/bin/phpunit` |

## Resources

- [Drupal.org: GitLab CI](https://www.drupal.org/node/3356364)
- [Drupal Association CI Templates](https://git.drupalcode.org/project/gitlab_templates)
