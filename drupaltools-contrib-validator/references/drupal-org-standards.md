# Drupal.org Contribution Standards

This reference provides detailed information about Drupal.org contribution requirements for custom modules.

## Overview

Contributing a module to Drupal.org requires meeting specific standards for file structure, documentation, and CI/CD configuration. This document outlines all requirements and best practices.

## Required Files

### 1. MODULE.info.yml (REQUIRED)

The `.info.yml` file is the only strictly required file for a Drupal module. However, for Drupal.org contribution, additional files are required.

**Minimum content:**
```yaml
name: 'Module Name'
type: module
description: 'A brief description of the module'
core_version_requirement: ^10.1 || ^11
package: Custom
```

**Recommended additions:**
```yaml
dependencies:
  - node:node
  - views:views

configure: module.settings

php: 8.1
```

**Field descriptions:**
- `name`: Human-readable module name
- `type`: Must be "module" for modules
- `description`: Brief description (shown on modules page)
- `core_version_requirement`: Supported Drupal core versions
- `package`: Grouping on modules page (use descriptive names)
- `dependencies`: List of module dependencies
- `configure`: Route to settings form (if applicable)
- `php`: Minimum PHP version

### 2. README.md (REQUIRED)

The README.md file is critical for Drupal.org contribution. It must follow specific guidelines.

**Required Sections:**

#### About
Introduction that summarizes the module's purpose and function. The first ~200 characters appear in project listings. Should be accessible to users new to Drupal while useful for experienced developers.

```markdown
About
-----

This module provides GraphQL debugging capabilities for Drupal sites.
It exposes entity field information in GraphQL queries for development
and debugging purposes. Designed for both beginners and experienced developers,
this module helps troubleshoot GraphQL queries by providing detailed field
resolution information.
```

#### Features
Describes the module's functionality, unique features, and use cases.

```markdown
Features
--------

### Basic Functionality

This module adds debug output to GraphQL queries showing:
- Field resolution paths
- Query execution time
- Data type information
- Cache hit/miss status

### Unique Features

- **Real-time debugging**: See field data as GraphQL resolves it
- **Performance metrics**: Identify slow field resolvers
- **Type inspection**: View underlying data types

### Use Cases

- Debugging complex GraphQL queries during development
- Understanding field resolution order
- Optimizing query performance
- Learning GraphQL schema structure
```

**Optional Sections:**

#### Requirements
Lists required modules and dependencies.

```markdown
Requirements
------------

### Drupal Version
- Drupal 10.1+ or 11.x

### Required Modules
- GraphQL (graphql)
- GraphQL Compose (graphql_compose)
```

#### Recommended Modules
Suggests complementary modules.

```markdown
Recommended modules
-------------------

### GraphQL Devel
Provides additional debugging tools for GraphQL development.

### Devel
Essential development and debugging tools for Drupal.
```

#### Example Code
Provides code examples for developers.

```markdown
Example code
-------------

### Basic Usage

```graphql
query GetNodeWithDebug {
  node(id: "1") {
    id
    title
    _debug {
      queryTime
      fieldCount
    }
  }
}
```

### Programmatic Usage

```php
$debug = \\Drupal::service('graphql_compose_debug.collector');
$info = $debug->getDebugInfo();
```
```

#### Similar Projects
Lists alternative modules and differentiators.

```markdown
Similar projects
----------------

### GraphQL Devel
- **Similarities**: Provides GraphQL debugging
- **Differences**: This module focuses on field-level debugging
- **When to use GraphQL Devel**: For query explorer functionality

### GraphQL Developer
- **Similarities**: Development tools for GraphQL
- **Differences**: Different approach to debugging interface
```

#### Supporting this Module
Information about financial support or sponsorships.

```markdown
Supporting this Module
----------------------

This module is maintained by volunteers. If you find it useful:

- Report bugs and issues
- Submit patches for improvements
- Sponsor development through Drupal Association

Consider supporting the [Drupal Association](https://www.drupal.org/association)
to fund Drupal infrastructure.
```

#### Contributing
Guidelines for contributing to the module.

```markdown
Contributing
------------

We welcome contributions! Please:

1. Check the [issue queue](https://www.drupal.org/project/issues/PROJECT)
2. Follow Drupal coding standards
3. Include tests with new features
4. Document your changes

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.
```

#### Community Documentation
Links to external resources, videos, demos.

```markdown
Community Documentation
-----------------------

### Video Tutorials
- [Drupal GraphQL Debugging Tutorial](https://youtube.com/example)

### Demo Sites
- [DrupalPod Demo](https://drupalpod.com/project/PROJECT)

### Articles
- [Debugging GraphQL in Drupal](https://example.com/article)
```

#### Basic Services (if applicable)
Only include if your module has a `.services.yml` file.

```markdown
Basic Services
--------------

This module provides the following services:

### graphql_compose_debug.debug_collector

Collects debug information during GraphQL query execution.

```php
$debug = \\Drupal::service('graphql_compose_debug.debug_collector');
$debug->start();
// ... query execution
$info = $debug->collect();
```
```

#### Extend and Override
How other modules can extend functionality.

```markdown
Extend and override
-------------------

### Alter hooks

Modify debug output:

```php
function mymodule_graphql_compose_debug_info_alter(&$info) {
  $info['custom_metric'] = mymodule_calculate_metric();
}
```
```

**Prohibited Content:**
- File structure diagrams or sections
- Installation instructions ("How to install", composer require, drush en)
- Screenshots (use issue queue instead)

### 3. logo.png (REQUIRED)

Every Drupal.org project requires a logo image.

**Specifications:**
- **Format:** PNG with transparency
- **Size:** 120x120 pixels minimum (recommended)
- **Content:** Simple, recognizable at small sizes
- **Style:** Professional, matches module purpose

**Design Guidelines:**
- Use simple icons or symbols
- Avoid text (doesn't scale well)
- Use Drupal colors or module branding
- Test at 32x32 pixels (small view)

**Creation Tools:**
- GIMP (free, open source)
- Inkscape (vector graphics)
- Figma (online)
- Canva (online)

**Placement:**
Save as `logo.png` in the module root directory.

### 4. .gitlab-ci.yml (REQUIRED)

GitLab CI configuration is required for automated testing on Drupal.org.

**Basic Configuration:**

```yaml
include:
  - project: 'project/gitlab_templates'
    ref: 1.0.x
    file:
      - '/includes/include.drupalci.variables.yml'
      - '/includes/include.drupalci.workflows.yml'
      - '/includes/include.drupalci.main.yml'

variables:
  _TARGET_PHP: "8.1,8.2,8.3"
  _TARGET_CORE: "10.3"
```

**Drupal 7 vs Drupal 10/11:**

The template automatically detects module type. For Drupal 7, you need to uncomment specific lines. Most modules now target Drupal 10+.

**Custom Jobs:**

Add custom testing jobs as needed:

```yaml
my_custom_test:
  extends: .phpunit-base
  script:
    - cd web
    - ../vendor/bin/phpunit --testsuite=custom
```

**Testing PHP Versions:**

Configure based on `core_version_requirement`:
- Drupal 10: PHP 8.1, 8.2, 8.3
- Drupal 11: PHP 8.2, 8.3+

### 5. composer.json (RECOMMENDED)

While not strictly required, composer.json is highly recommended for Drupal.org modules.

**Basic Structure:**

```json
{
  "name": "drupal/module_name",
  "description": "Module description",
  "type": "drupal-module",
  "license": "GPL-2.0-or-later",
  "require": {
    "php": ">=8.1",
    "drupal/core": "^10"
  },
  "autoload": {
    "psr-4": {
      "Drupal\\ModuleName\\": "src/"
    }
  }
}
```

**Key Points:**
- `name`: Must be `drupal/machine_name`
- `type`: Must be `drupal-module`
- `license`: GPL-2.0-or-later for Drupal modules
- `autoload`: PSR-4 autoloading for your namespace

### 6. LICENSE (DO NOT ADD)

Drupal.org automatically injects the GPL LICENSE file. Do NOT include:
- LICENSE
- LICENSE.txt
- LICENSE.md

## Directory Structure

### Standard Module Structure

```
module_name/
├── module_name.info.yml          (REQUIRED)
├── README.md                     (REQUIRED)
├── logo.png                      (REQUIRED)
├── .gitlab-ci.yml                (REQUIRED)
├── composer.json                 (RECOMMENDED)
├── module_name.module            (optional - hooks)
├── module_name.permissions.yml   (if defining permissions)
├── module_name.routing.yml       (if defining routes)
├── module_name.services.yml      (if defining services)
├── config/                       (if providing config)
│   ├── install/
│   │   └── module_name.settings.yml
│   └── schema/
│       └── module_name.schema.yml
├── src/                          (PSR-4 classes)
│   ├── Controller/
│   ├── Plugin/
│   ├── Form/
│   └── Service/
└── tests/                        ( PHPUnit tests)
    └── src/
```

## Drupal Coding Standards

### PHP Coding Standards

Drupal follows specific coding standards enforced by PHPCS.

**Key Standards:**
- Indentation: 2 spaces (no tabs)
- Line length: 80 characters soft limit, 120 hard
- Control structures: K&R style
- Function names: lowercase_with_underscores
- Class names: UpperCamelCase
- Constants: UPPER_CASE_WITH_UNDERSCORES

**Example:**

```php
<?php

namespace Drupal\my_module\Service;

use Drupal\Core\Logger\LoggerChannelFactoryInterface;

/**
 * Example service.
 */
class ExampleService {

  /**
   * The logger channel.
   *
   * @var \Drupal\Core\Logger\LoggerChannelFactoryInterface
   */
  protected $logger;

  /**
   * Constructs an ExampleService object.
   *
   * @param \Drupal\Core\Logger\LoggerChannelFactoryInterface $logger
   *   The logger channel factory.
   */
  public function __construct(LoggerChannelFactoryInterface $logger) {
    $this->logger = $logger->get('my_module');
  }

  /**
   * Performs an action.
   *
   * @param string $input
   *   The input string.
   *
   * @return string
   *   The processed output.
   */
  public function doSomething($input) {
    $output = $this->process($input);
    $this->logger->info('Processed: @output', ['@output' => $output]);
    return $output;
  }

}
```

### YAML Standards

- Use 2 spaces for indentation
- No tabs
- Quote strings when necessary
- Use proper list formatting

**Example:**

```yaml
# Correct
my_module.settings:
  path: '/custom/path'
  options:
    - option_one
    - option_two
  enabled: true
```

### Twig Standards

- Use 2 spaces for indentation
- Variables: snake_case
- Filters: pipe syntax
- Comments: {# Comment #}

**Example:**

```twig
{#
  /**
   * @file
   * Default theme implementation.
   */
#}
<div{{ attributes.addClass('my-module-class') }}>
  <h2>{{ label }}</h2>
  {% if items %}
    <ul>
      {% for item in items %}
        <li>{{ item.value }}</li>
      {% endfor %}
    </ul>
  {% endif %}
</div>
```

## GitLab CI Testing

### Available Test Types

The Drupal Association GitLab CI template provides:

1. **Composer Validation** - Validates composer.json syntax
2. **PHP Lint** - Checks PHP syntax errors
3. **PHPCS** - Drupal coding standards
4. **PHPStan** - Static analysis
5. **PHPUnit** - Automated tests

### Configuration Options

**Test Matrix:**

Test multiple PHP and Drupal versions:

```yaml
variables:
  _TARGET_PHP: "8.1,8.2,8.3"
  _OPT_IN_TEST_PREVIOUS_MINOR: 1
  _OPT_IN_TEST_NEXT_MINOR: 1
```

**Skip Tests:**

```yaml
phpunit:
  rules:
    - when: never
```

**Custom PHPStan:**

Add `phpstan.neon.dist` to module root for custom configuration.

## Common Issues and Solutions

### Issue: README.md validation fails

**Symptoms:** Validator reports missing sections or prohibited content.

**Solutions:**
- Ensure all required sections exist (About, Basic usage, Extend and override)
- Remove installation instructions
- Remove file structure diagrams
- Target content to experienced developers

### Issue: .gitlab-ci.yml fails on GitLab

**Symptoms:** Pipeline jobs fail on git.drupalcode.org.

**Solutions:**
- Verify YAML syntax is valid
- Check PHP versions match core_version_requirement
- Run tests locally with `ddev-drupal-contrib`
- Review job logs for specific errors

### Issue: PHPCS errors

**Symptoms:** Coding standards violations reported.

**Solutions:**
- Run `vendor/bin/phpcbf` to auto-fix
- Manually fix remaining issues
- Add custom ruleset if needed: `phpcs.xml`

### Issue: Missing dependencies

**Symptoms:** Tests fail due to missing modules.

**Solutions:**
- Add to `require-dev` in composer.json
- Use `"drupal/module_name": "*"` for flexibility
- Run `composer update` after changes

## Resources

- [Drupal.org: Creating Modules](https://www.drupal.org/docs/develop/creating-modules)
- [Drupal.org: GitLab CI](https://www.drupal.org/node/3356364)
- [Drupal Coding Standards](https://project.pages.drupalcode.org/coding_standards)
- [GitLab Templates](https://git.drupalcode.org/project/gitlab_templates)
- [ddev-drupal-contrib](https://github.com/weitzman/drupal-ddev-contrib)