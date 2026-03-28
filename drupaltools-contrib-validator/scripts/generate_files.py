#!/usr/bin/env python3
"""
Generate missing files for Drupal contributed modules.

Generates README.md, .gitlab-ci.yml, and other required files
based on module analysis.

Usage:
    python3 generate_files.py /path/to/module --readme --gitlab-ci
    python3 generate_files.py /path/to/module --all
"""

import os
import sys
import argparse
import json
from pathlib import Path
from typing import Dict, List, Optional
import yaml


class FileGenerator:
    """Generates missing files for Drupal modules."""

    def __init__(self, module_path: str):
        """Initialize generator with module path.

        Args:
            module_path: Path to Drupal module directory
        """
        self.module_path = Path(module_path).resolve()
        self.module_info = {}
        self.generated_files = []

    def generate(self, options: Dict[str, bool]) -> List[str]:
        """Generate files based on options.

        Args:
            options: Dict with boolean flags for each file type

        Returns:
            List of generated file paths
        """
        # Parse module info first
        self._parse_module_info()

        if not self.module_info:
            print("❌ Could not parse module info. Aborting.")
            return []

        print(f"\n{'='*60}")
        print(f"GENERATING FILES FOR: {self.module_info.get('name', 'Module')}")
        print(f"{'='*60}\n")

        # Generate files based on options
        if options.get('readme') or options.get('all'):
            self._generate_readme()

        if options.get('gitlab_ci') or options.get('all'):
            self._generate_gitlab_ci()

        if options.get('logo') or options.get('all'):
            self._generate_logo_instructions()

        if options.get('composer') or options.get('all'):
            self._generate_composer_json()

        # Summary
        print(f"\n{'='*60}")
        print(f"✅ Generated {len(self.generated_files)} files")
        print(f"{'='*60}\n")

        for f in self.generated_files:
            print(f"  - {f}")

        return self.generated_files

    def _parse_module_info(self) -> None:
        """Parse module info from .info.yml file."""
        info_files = list(self.module_path.glob('*.info.yml'))

        if not info_files:
            return

        try:
            with open(info_files[0], 'r') as f:
                info_data = yaml.safe_load(f)

            self.module_info = {
                'machine_name': info_files[0].stem.replace('.info', ''),
                'name': info_data.get('name', 'Module Name'),
                'description': info_data.get('description', ''),
                'package': info_data.get('package', 'Custom'),
                'core_version': info_data.get('core_version_requirement', '^10'),
                'dependencies': info_data.get('dependencies', []),
                'configure': info_data.get('configure', ''),
                'php': info_data.get('php', '8.1'),
            }

            # Check for services
            services_file = self.module_path / f"{self.module_info['machine_name']}.services.yml"
            self.module_info['has_services'] = services_file.exists()

        except Exception as e:
            print(f"⚠ Warning: Could not parse info file: {e}")

    def _generate_readme(self) -> None:
        """Generate README.md with appropriate sections."""
        readme_path = self.module_path / 'README.md'

        if readme_path.exists():
            print("⚠ README.md already exists. Skipping.")
            return

        # Build README content
        content = self._build_readme_content()

        try:
            with open(readme_path, 'w', encoding='utf-8') as f:
                f.write(content)

            self.generated_files.append('README.md')
            print(f"✅ Generated README.md ({len(content.split())} words)")
        except Exception as e:
            print(f"❌ Error generating README.md: {e}")

    def _build_readme_content(self) -> str:
        """Build README.md content based on module info.

        Returns:
            README content as string
        """
        name = self.module_info.get('name', 'Module Name')
        description = self.module_info.get('description', '')
        machine_name = self.module_info.get('machine_name', 'module_name')

        sections = []

        # Title
        sections.append(f"# {name}\n")

        # About section - Focus on users new to Drupal, first 200 chars shown in project listing
        sections.append("About")
        sections.append("-" * len("About"))
        sections.append(self._get_about_content(description))
        sections.append("")

        # Features section - What functionality, unique features, use cases
        sections.append("Features")
        sections.append("-" * len("Features"))
        sections.append(self._get_features_content())
        sections.append("")

        # Requirements section - Dependencies
        sections.append("Requirements")
        sections.append("-" * len("Requirements"))
        sections.append(self._get_requirements_content())
        sections.append("")

        # Recommended modules section
        sections.append("Recommended modules")
        sections.append("-" * len("Recommended modules"))
        sections.append(self._get_recommended_content())
        sections.append("")

        # Example code section
        sections.append("Example code")
        sections.append("-" * len("Example code"))
        sections.append(self._get_example_code_content())
        sections.append("")

        # Similar projects section
        sections.append("Similar projects")
        sections.append("-" * len("Similar projects"))
        sections.append(self._get_similar_projects_content())
        sections.append("")

        # Basic Services section (if applicable)
        if self.module_info.get('has_services'):
            sections.append("Basic Services")
            sections.append("-" * len("Basic Services"))
            sections.append(self._get_services_content())
            sections.append("")

        # Extend and override section (renamed from Contributing)
        sections.append("Extend and override")
        sections.append("-" * len("Extend and override"))
        sections.append(self._get_extend_content())
        sections.append("")

        # Supporting this Module (optional)
        sections.append("Supporting this Module")
        sections.append("-" * len("Supporting this Module"))
        sections.append(self._get_supporting_content())
        sections.append("")

        # Contributing (optional)
        sections.append("Contributing")
        sections.append("-" * len("Contributing"))
        sections.append(self._get_contributing_content())
        sections.append("")

        # Community Documentation (optional)
        sections.append("Community Documentation")
        sections.append("-" * len("Community Documentation"))
        sections.append(self._get_community_docs_content())
        sections.append("")

        return "\n".join(sections)

    def _get_usage_content(self) -> str:
        """Get basic usage content.

        Returns:
            Usage content string
        """
        machine_name = self.module_info.get('machine_name', 'module_name')

        content = """This module provides functionality for Drupal sites.

Installation via Composer:
```bash
composer require drupal/{machine_name}
```

Enable the module:
```bash
drush en {machine_name}
```

After enabling, configure the module at:
/admin/config/development/{machine_name}

For Developers
--------------

The module provides the following APIs:

```php
// Example usage
\\Drupal::service('{machine_name}.service')->doSomething();
```

See the `src/` directory for implementation details.
"""
        return content.format(machine_name=machine_name)

    def _get_about_content(self, description: str) -> str:
        """Get About section content.

        Args:
            description: Module description

        Returns:
            About content string
        """
        # The first ~200 characters will be shown in project listing
        return f"""{description}

This module is designed for users who are new to Drupal as well as experienced developers. It provides a straightforward solution to specific Drupal challenges.

This introduction summarizes the purpose and function of this project, focusing on users brand new to Drupal while remaining useful for experienced developers.
"""

    def _get_features_content(self) -> str:
        """Get Features section content.

        Returns:
            Features content string
        """
        return """### Basic Functionality

This module provides core functionality that integrates seamlessly with your Drupal site. Enable the module to access these features.

### Unique Features

- **Feature 1**: Description of unique functionality that sets this module apart
- **Feature 2**: Another distinctive feature
- **Feature 3**: Additional capabilities

### Use Cases

This module is particularly useful when:
- You need specific functionality in your Drupal site
- You want to integrate with external systems
- You require enhanced debugging or development tools

### When to Use

Enable this module when:
- Your project requires the specific solution this module provides
- You need the features described above
- You want to extend Drupal's core capabilities in this domain
"""

    def _get_requirements_content(self) -> str:
        """Get Requirements section content.

        Returns:
            Requirements content string
        """
        machine_name = self.module_info.get('machine_name', 'module_name')
        dependencies = self.module_info.get('dependencies', [])

        content_lines = ["### Drupal Version"]

        core_version = self.module_info.get('core_version', '^10')
        content_lines.append(f"- Drupal {core_version}")

        if dependencies:
            content_lines.append("\n### Required Modules")
            for dep in dependencies:
                dep_parts = dep.split(':')
                if len(dep_parts) > 1:
                    module_name = dep_parts[1].replace('_', ' ').title()
                    content_lines.append(f"- {module_name} (`{dep_parts[1]}`)")

        content_lines.append("\n### Configuration")
        content_lines.append("No special configuration required.")
        content_lines.append("Simply enable the module and it will work out of the box.")

        return "\n".join(content_lines)

    def _get_recommended_content(self) -> str:
        """Get Recommended modules section content.

        Returns:
            Recommended content string
        """
        return """The following modules enhance or complement the functionality of this project:

### Module Name

Brief description of how this module enhances functionality.

### Another Module

Description of additional capabilities.

### Development Tools

For development environments, consider:
- **Devel**: Essential development tools
- **Stage File Proxy**: Proxies files from production during development

*Note: These recommendations are optional and depend on your specific use case.*
"""

    def _get_example_code_content(self) -> str:
        """Get Example code section content.

        Returns:
            Example code content string
        """
        machine_name = self.module_info.get('machine_name', 'module_name')

        return """### Basic Usage

```php
// Example of using the module's API
$service = \\Drupal::service('{machine_name}.service');
$result = $service->methodName();
```

### Advanced Example

```php
// More complex usage example
use Drupal\\{machine_name}\\Service\\ExampleService;

/**
 * Custom implementation.
 */
function mymodule_custom_function() {
  $service = \\Drupal::service('{machine_name}.service');
  $service->advancedMethod();
}
```

### Twig Template Example

```twig
{# Example usage in Twig templates #}
{{ drupal_{machine_name}_method() }}
```

### Configuration Example

```php
// Programmatically configuring the module
$config = \\Drupal::configFactory()->getEditable('{machine_name}.settings');
$config->set('option_name', 'value')->save();
```
"""

    def _get_similar_projects_content(self) -> str:
        """Get Similar projects section content.

        Returns:
            Similar projects content string
        """
        return """### Alternative Modules

Several Drupal modules provide similar functionality. Here's how this module differs:

#### Module A

- **Similarities**: Provides similar core features
- **Differences**: This module offers [specific advantage]
- **When to choose Module A**: When you need [specific use case]

#### Module B

- **Similarities**: Addresses similar problem space
- **Differences**: This module uses [different approach]
- **When to choose Module B**: When [specific condition]

### Why Choose This Module?

This module stands out because:
- More actively maintained
- Better performance
- Simpler configuration
- More comprehensive feature set
- Better integration with Drupal ecosystem

### Migration from Other Modules

If you're switching from another module, see the documentation for migration guides.
"""

    def _get_supporting_content(self) -> str:
        """Get Supporting this Module section content.

        Returns:
            Supporting content string
        """
        return """This module is maintained by volunteers and community members like you.

### How to Support

- **Report Issues**: Help improve the module by reporting bugs
- **Submit Patches**: Contribute code fixes and new features
- **Review Patches**: Test and review community contributions
- **Documentation**: Improve documentation and examples
- **Spread the Word**: Share your positive experience

### Funding

If you'd like to financially support the development of this module, consider:
- **Drupal Association**: https://www.drupal.org/association
- **Drupalize.Me**: https://drupalize.me

### Sponsors

This module is sponsored by:
- [Organization Name] - Description of sponsorship

*Interested in sponsoring? Contact the maintainers.*
"""

    def _get_contributing_content(self) -> str:
        """Get Contributing section content.

        Returns:
            Contributing content string
        """
        machine_name = self.module_info.get('machine_name', 'module_name')

        return """We welcome contributions from the community!

### Getting Started

1. Fork the repository on git.drupalcode.org
2. Create a feature branch for your work
3. Make your changes following Drupal coding standards
4. Test thoroughly
5. Create a merge request with detailed description

### Coding Standards

All code must follow:
- [Drupal Coding Standards](https://www.drupal.org/docs/develop/standards)
- [PHP Best Practices](https://www.drupal.org/docs/develop/standards/php)
- [JavaScript Standards](https://www.drupal.org/docs/develop/standards/javascript)

### Testing

- Write PHPUnit tests for new functionality
- Ensure all tests pass before submitting
- Include test instructions in your MR description

### Commit Messages

Follow these guidelines:
- Use clear, descriptive commit messages
- Reference issue numbers when applicable
- Example: "Fix #12345: Resolve issue with feature X"

### Issue Queue

- Check existing issues before creating new ones
- Provide detailed reproduction steps for bugs
- Use the issue template for feature requests

### Code Review

All contributions go through review:
- Be responsive to review feedback
- Address requested changes promptly
- Engage constructively with reviewers

For more information, see:
- [Drupal Contribution Guide](https://www.drupal.org/contribute)
- [GitLab Handbook](https://www.drupal.org/docs/develop/git/using-gitlab-to-contribute-to-drupal)
"""

    def _get_community_docs_content(self) -> str:
        """Get Community Documentation section content.

        Returns:
            Community docs content string
        """
        return """Looking for more resources? Here's community-created content to help you get started:

### Video Tutorials

- **[YouTube: Module Overview](https://youtube.com/example)** - Introduction to this module
- **[YouTube: Advanced Features](https://youtube.com/example2)** - Deep dive into advanced features

### External Documentation

- **[Project Wiki](https://git.drupalcode.org/project/PROJECT/-/wikis/home)** - Community-maintained wiki
- **[API Documentation](https://api.drupal.org/api/drupal/PROJECT/)** - Generated API docs

### Demo Sites

- **[DrupalPod Demo](https://drupalpod.com/project/PROJECT)** - Interactive demo (DrupalPod)
- **[Simplytest.me Demo](https://simplytest.me/project/PROJECT)** - Quick test environment

### Blog Posts & Articles

- **[Blog Post Title](https://example.com)** - Description of content
- **[Tutorial: Use Case](https://example.com)** - Step-by-step guide

### Community Support

- **Drupal Slack**: #module-name channel
- **Drupal.org Forum**: [Project support forum](https://www.drupal.org/forum/123)
- **Stack Overflow**: Tag questions with `drupal-module-name`

*Have a resource to share? Submit a merge request to add it here!*
"""

    def _get_services_content(self) -> str:
        """Get services content.

        Returns:
            Services content string
        """
        return """This module provides the following services:

### Service Name

Description of what the service does.

```php
// Use the service
$service = \\Drupal::service('module.service_name');
$result = $service->methodName();
```

See the `src/` directory for all available services and their methods."""

    def _get_extend_content(self) -> str:
        """Get extend and override content.

        Returns:
            Extend content string
        """
        return """This module can be extended using Drupal hooks and events.

### Hooks

Implement hooks in your custom module to modify behavior:

```php
/**
 * Implements hook_module_hook().
 */
function mymodule_module_hook($data) {
  // Modify $data as needed
  return $data;
}
```

### Events

Subscribe to events dispatched by this module:

```yaml
services:
  mymodule.event_subscriber:
    class: Drupal\\mymodule\\Event\\ModuleEventSubscriber
    tags:
      - { name: event_subscriber }
```

### Plugins

Extend functionality by providing plugins:

```php
namespace Drupal\\mymodule\\Plugin\\ModulePlugin;

use Drupal\\module\\PluginBase;

/**
 * @ModulePlugin(
 *   id = "custom_plugin",
 *   label = @Translation("Custom Plugin")
 * )
 */
class CustomPlugin extends PluginBase {
  // Implementation
}
```

See the `src/Plugin/` directory for plugin examples."""

    def _generate_gitlab_ci(self) -> None:
        """Generate .gitlab-ci.yml from Drupal Association template."""
        ci_path = self.module_path / '.gitlab-ci.yml'

        if ci_path.exists():
            print("⚠ .gitlab-ci.yml already exists. Skipping.")
            return

        # Build .gitlab-ci.yml content
        content = self._build_gitlab_ci_content()

        try:
            with open(ci_path, 'w', encoding='utf-8') as f:
                f.write(content)

            self.generated_files.append('.gitlab-ci.yml')
            print(f"✅ Generated .gitlab-ci.yml")
        except Exception as e:
            print(f"❌ Error generating .gitlab-ci.yml: {e}")

    def _build_gitlab_ci_content(self) -> str:
        """Build .gitlab-ci.yml content.

        Returns:
            GitLab CI content as string
        """
        # Determine PHP versions from core_version_requirement
        core_version = self.module_info.get('core_version', '^10')

        if '^11' in core_version:
            php_versions = ['8.2', '8.3']
        elif '^10' in core_version:
            php_versions = ['8.1', '8.2', '8.3']
        else:
            php_versions = ['8.1']

        php_versions_str = ','.join(php_versions)

        content = f"""# GitLab CI configuration for Drupal contributed modules
# Based on Drupal Association template: https://git.drupalcode.org/project/gitlab_templates

include:
  - project: 'project/gitlab_templates'
    ref: 1.0.x
    file:
      - '/includes/include.drupalci.variables.yml'
      - '/includes/include.drupalci.workflows.yml'
      - '/includes/include.drupalci.main.yml'

# Override variables as needed
variables:
  # PHP versions to test
  _TARGET_PHP: "{php_versions_str}"

  # Drupal core version
  _TARGET_CORE: "10.3"

# Define any custom jobs
phpcs:
  extends: .phpcs-base
  rules:
    - if: '$CI_PIPELINE_SOURCE == "merge_request_event"'
    - if: '$CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH'

phpunit:
  extends: .phpunit-base
  rules:
    - if: '$CI_PIPELINE_SOURCE == "merge_request_event"'
    - if: '$CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH'

# Optional: Add custom testing jobs
# custom_test:
#   script:
#     - your custom commands
"""
        return content

    def _generate_logo_instructions(self) -> None:
        """Generate logo instructions file."""
        logo_instructions_path = self.module_path / 'logo-instructions.txt'

        if (self.module_path / 'logo.png').exists():
            print("✅ logo.png already exists.")
            return

        content = """LOGO INSTRUCTIONS
================

Your module is missing a logo.png file.

RECOMMENDATIONS:
- Size: 120x120 pixels (minimum)
- Format: PNG with transparency
- Style: Simple, recognizable at small sizes
- Content: Module icon or related imagery

WHERE TO PLACE:
Save your logo as: logo.png
In the module root: {module_path}/logo.png

CREATION OPTIONS:
1. Design your own using image editing software
2. Use online tools: Canva, Figma, or GIMP
3. Hire a designer for professional results
4. Use a simple icon from icon libraries

EXAMPLE REFERENCE:
See other Drupal modules for logo examples:
- https://www.drupal.org/project/views
- https://www.drupal.org/project/token

After creating the logo:
1. Save as logo.png in module root
2. Add to git: git add logo.png
3. Commit: git commit -m "Add module logo"
4. Delete this instructions file
""".format(module_path=self.module_path)

        try:
            with open(logo_instructions_path, 'w', encoding='utf-8') as f:
                f.write(content)

            self.generated_files.append('logo-instructions.txt')
            print(f"✅ Generated logo-instructions.txt")
        except Exception as e:
            print(f"❌ Error generating logo instructions: {e}")

    def _generate_composer_json(self) -> None:
        """Generate composer.json if missing."""
        composer_path = self.module_path / 'composer.json'

        if composer_path.exists():
            print("⚠ composer.json already exists. Skipping.")
            return

        machine_name = self.module_info.get('machine_name', 'module_name')
        name = self.module_info.get('name', 'Module Name')
        description = self.module_info.get('description', '')
        php_version = self.module_info.get('php', '8.1')

        # Convert machine_name to PSR-4 namespace (e.g., graphql_compose_debug -> Graphql_Compose_Debug)
        namespace_parts = [p.title() for p in machine_name.split('_')]
        namespace = '\\'.join(namespace_parts)

        composer_content = {
            "name": f"drupal/{machine_name}",
            "description": description,
            "type": "drupal-module",
            "license": "GPL-2.0-or-later",
            "require": {
                "php": f">={php_version}",
                "drupal/core": "^10"
            },
            "autoload": {
                "psr-4": {
                    f"Drupal\\{namespace}\\": "src/"
                }
            }
        }

        try:
            with open(composer_path, 'w', encoding='utf-8') as f:
                json.dump(composer_content, f, indent=2, ensure_ascii=False)
                f.write('\n')  # Add trailing newline

            self.generated_files.append('composer.json')
            print(f"✅ Generated composer.json")
        except Exception as e:
            print(f"❌ Error generating composer.json: {e}")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='Generate missing files for Drupal contributed modules'
    )
    parser.add_argument(
        'module_path',
        nargs='?',
        default='.',
        help='Path to Drupal module directory (default: current directory)'
    )
    parser.add_argument(
        '--readme',
        action='store_true',
        help='Generate README.md'
    )
    parser.add_argument(
        '--gitlab-ci',
        action='store_true',
        help='Generate .gitlab-ci.yml'
    )
    parser.add_argument(
        '--logo',
        action='store_true',
        help='Generate logo instructions'
    )
    parser.add_argument(
        '--composer',
        action='store_true',
        help='Generate composer.json'
    )
    parser.add_argument(
        '--all',
        action='store_true',
        help='Generate all missing files'
    )

    args = parser.parse_args()

    # If no specific options, show help
    if not any([args.readme, args.gitlab_ci, args.logo, args.composer, args.all]):
        parser.print_help()
        sys.exit(1)

    # Run generator
    generator = FileGenerator(args.module_path)

    options = {
        'readme': args.readme,
        'gitlab_ci': args.gitlab_ci,
        'logo': args.logo,
        'composer': args.composer,
        'all': args.all,
    }

    generator.generate(options)

    print("\nNext steps:")
    print("1. Review generated files")
    print("2. Customize content for your module")
    print("3. Create logo.png if needed")
    print("4. Test .gitlab-ci.yml on GitLab")
    print("5. Commit and push to repository")


if __name__ == '__main__':
    main()