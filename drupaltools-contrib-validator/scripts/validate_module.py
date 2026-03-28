#!/usr/bin/env python3
"""
Drupal Contrib Module Validator

Validates Drupal 10+ custom modules for Drupal.org contribution readiness.
Checks required files, README structure, GitLab CI configuration, and coding standards.

Usage:
    python3 validate_module.py /path/to/module
    python3 validate_module.py .  # Validate current directory
"""

import os
import sys
import argparse
import json
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import re
import yaml


class ModuleValidator:
    """Validates Drupal modules for Drupal.org contribution readiness."""

    # Required files for Drupal.org contribution
    REQUIRED_FILES = [
        'info.yml',
        'README.md',
        'logo.png',
        '.gitlab-ci.yml',
    ]

    # Recommended files
    RECOMMENDED_FILES = [
        'composer.json',
    ]

    # Files that should NOT exist (Drupal.org adds automatically)
    PROHIBITED_FILES = [
        'LICENSE',
        'LICENSE.txt',
    ]

    # Required README sections
    REQUIRED_README_SECTIONS = [
        'About',
        'Features',
    ]

    # Optional README sections
    OPTIONAL_README_SECTIONS = [
        'Requirements',
        'Recommended modules',
        'Example code',
        'Similar projects',
        'Basic Services',
        'Extend and override',
        'Supporting this Module',
        'Contributing',
        'Community Documentation',
    ]

    # Prohibited README content
    PROHIBITED_README_CONTENT = [
        'file structure',
        'file-structure',
        'installation instructions',
        'how to install',
        'how-to-install',
        'composer require',
        'drush en',
        'drush enable',
    ]

    def __init__(self, module_path: str):
        """Initialize validator with module path.

        Args:
            module_path: Path to Drupal module directory
        """
        self.module_path = Path(module_path).resolve()
        self.validation_results = {
            'status': 'UNKNOWN',
            'missing_files': [],
            'incomplete_files': {},
            'recommendations': [],
            'module_info': {},
            'readme_issues': [],
            'coding_standards': {},
        }

    def validate(self) -> Dict:
        """Run complete validation on module.

        Returns:
            Dict with validation results
        """
        print(f"\n{'='*60}")
        print(f"DRUPAL CONTRIB MODULE VALIDATOR")
        print(f"{'='*60}")
        print(f"Module: {self.module_path.name}")
        print(f"Path: {self.module_path}")
        print(f"{'='*60}\n")

        # Step 1: Validate directory exists
        if not self._validate_directory():
            return self.validation_results

        # Step 2: Find info.yml file
        info_file = self._find_info_file()
        if not info_file:
            self._add_error('Missing required .info.yml file')
            return self.validation_results

        # Step 3: Parse info.yml
        self._parse_info_file(info_file)

        # Step 4: Check required files
        self._check_required_files()

        # Step 5: Check for prohibited files
        self._check_prohibited_files()

        # Step 6: Validate README.md
        if self._has_readme():
            self._validate_readme()
        else:
            self.validation_results['missing_files'].append('README.md')

        # Step 7: Validate .gitlab-ci.yml
        if self._has_gitlab_ci():
            self._validate_gitlab_ci()
        else:
            self.validation_results['missing_files'].append('.gitlab-ci.yml')

        # Step 8: Determine overall status
        self._determine_status()

        return self.validation_results

    def _validate_directory(self) -> bool:
        """Validate module directory exists and is accessible.

        Returns:
            True if directory is valid
        """
        if not self.module_path.exists():
            print(f"❌ Error: Directory not found: {self.module_path}")
            return False

        if not self.module_path.is_dir():
            print(f"❌ Error: Not a directory: {self.module_path}")
            return False

        return True

    def _find_info_file(self) -> Optional[Path]:
        """Find the .info.yml file in module directory.

        Returns:
            Path to info file or None
        """
        info_files = list(self.module_path.glob('*.info.yml'))

        if not info_files:
            print("❌ No .info.yml file found")
            return None

        if len(info_files) > 1:
            print(f"⚠ Warning: Multiple .info.yml files found, using {info_files[0].name}")

        return info_files[0]

    def _parse_info_file(self, info_file: Path) -> None:
        """Parse .info.yml file and extract module information.

        Args:
            info_file: Path to .info.yml file
        """
        try:
            with open(info_file, 'r') as f:
                info_data = yaml.safe_load(f)

            # Extract module info
            self.validation_results['module_info'] = {
                'name': info_data.get('name', 'Unknown'),
                'description': info_data.get('description', ''),
                'type': info_data.get('type', 'module'),
                'core_version': info_data.get('core_version_requirement', ''),
                'package': info_data.get('package', 'Custom'),
                'dependencies': info_data.get('dependencies', []),
                'configure': info_data.get('configure', ''),
                'php': info_data.get('php', ''),
            }

            print(f"✅ Info file: {info_file.name}")
            print(f"   Name: {self.validation_results['module_info']['name']}")
            print(f"   Core: {self.validation_results['module_info']['core_version']}")
            print(f"   PHP: {self.validation_results['module_info']['php'] or 'Not specified'}")

            # Validate required keys
            required_keys = ['name', 'type', 'core_version_requirement']
            missing_keys = [k for k in required_keys if not info_data.get(k)]

            if missing_keys:
                self._add_incomplete_file(
                    info_file.name,
                    f"Missing required keys: {', '.join(missing_keys)}"
                )

            # Check for 'configure' key (recommended)
            if not info_data.get('configure'):
                self.validation_results['recommendations'].append(
                    "Add 'configure' key to info.yml pointing to settings form (if applicable)"
                )

        except yaml.YAMLError as e:
            self._add_error(f"Invalid YAML in {info_file.name}: {e}")
        except Exception as e:
            self._add_error(f"Error reading {info_file.name}: {e}")

    def _check_required_files(self) -> None:
        """Check for required and recommended files."""
        module_name = self.module_path.name

        for file_spec in self.REQUIRED_FILES:
            file_path = self.module_path / file_spec

            # For info.yml, we already checked
            if file_spec == 'info.yml':
                continue

            # Check other required files
            if not file_path.exists():
                self.validation_results['missing_files'].append(file_spec)
                print(f"❌ Missing: {file_spec}")
            else:
                print(f"✅ Found: {file_spec}")

        # Check recommended files
        for file_spec in self.RECOMMENDED_FILES:
            file_path = self.module_path / file_spec
            if not file_path.exists():
                self.validation_results['recommendations'].append(
                    f"Add {file_spec} (recommended for Drupal.org)"
                )
                print(f"⚠ Missing (recommended): {file_spec}")
            else:
                print(f"✅ Found: {file_spec}")

    def _check_prohibited_files(self) -> None:
        """Check for files that should not exist."""
        for file_spec in self.PROHIBITED_FILES:
            file_path = self.module_path / file_spec
            if file_path.exists():
                self.validation_results['recommendations'].append(
                    f"Remove {file_spec} - Drupal.org adds LICENSE automatically"
                )
                print(f"⚠ Prohibited file found: {file_spec} (Drupal.org adds LICENSE)")

    def _has_readme(self) -> bool:
        """Check if README.md exists.

        Returns:
            True if README.md exists
        """
        readme_path = self.module_path / 'README.md'
        return readme_path.exists()

    def _validate_readme(self) -> None:
        """Validate README.md structure and content."""
        readme_path = self.module_path / 'README.md'

        try:
            with open(readme_path, 'r', encoding='utf-8') as f:
                content = f.read()

            print(f"\n📄 Validating README.md...")

            # Check for required sections
            self._check_readme_sections(content)

            # Check for prohibited content
            self._check_prohibited_readme_content(content)

            # Check for code examples with proper standards
            self._check_code_examples(content)

        except Exception as e:
            self.validation_results['readme_issues'].append(f"Error reading README: {e}")

    def _check_readme_sections(self, content: str) -> None:
        """Check README for required sections.

        Args:
            content: README content
        """
        content_lower = content.lower()
        missing_sections = []

        for section in self.REQUIRED_README_SECTIONS:
            if section.lower() not in content_lower:
                missing_sections.append(section)
                self.validation_results['readme_issues'].append(
                    f"Missing required section: {section}"
                )
                print(f"  ❌ Missing section: {section}")
            else:
                print(f"  ✅ Found section: {section}")

        # Check if Basic Services section is needed
        has_services = (self.module_path / f"{self.module_path.name}.services.yml").exists()
        if has_services:
            if 'basic services' not in content_lower and 'services' not in content_lower:
                self.validation_results['readme_issues'].append(
                    "Missing 'Basic Services' section (module has services.yml)"
                )
                print(f"  ❌ Missing section: Basic Services (services.yml exists)")
        else:
            print(f"  ℹ️ 'Basic Services' section not needed (no services.yml)")

        # Check for recommended sections
        for section in self.OPTIONAL_README_SECTIONS:
            if section.lower() not in content_lower:
                if section == 'Extend and override':
                    self.validation_results['recommendations'].append(
                        f"Consider adding '{section}' section to README"
                    )

    def _check_prohibited_readme_content(self, content: str) -> None:
        """Check README for prohibited content.

        Args:
            content: README content
        """
        content_lower = content.lower()

        for prohibited in self.PROHIBITED_README_CONTENT:
            if prohibited in content_lower:
                self.validation_results['readme_issues'].append(
                    f"Contains prohibited content: '{prohibited}'"
                )
                print(f"  ⚠ Prohibited content: {prohibited}")

    def _check_code_examples(self, content: str) -> None:
        """Check code examples for Drupal coding standards.

        Args:
            content: README content
        """
        # Look for code blocks
        code_blocks = re.findall(r'```[\w]*\n(.*?)```', content, re.DOTALL)

        for block in code_blocks:
            # Basic checks
            if '\t' in block:
                self.validation_results['readme_issues'].append(
                    "Code example uses tabs instead of spaces"
                )

            # Check for Drupal coding patterns
            if '$' in block and 'function ' in block:
                # This looks like PHP code
                if 'use ' not in block and 'namespace ' not in block:
                    self.validation_results['recommendations'].append(
                        "Code examples should include use statements"
                    )

    def _has_gitlab_ci(self) -> bool:
        """Check if .gitlab-ci.yml exists.

        Returns:
            True if .gitlab-ci.yml exists
        """
        ci_path = self.module_path / '.gitlab-ci.yml'
        return ci_path.exists()

    def _validate_gitlab_ci(self) -> None:
        """Validate .gitlab-ci.yml configuration."""
        ci_path = self.module_path / '.gitlab-ci.yml'

        try:
            with open(ci_path, 'r') as f:
                ci_content = yaml.safe_load(f)

            print(f"\n🔄 Validating .gitlab-ci.yml...")

            # Check for Drupal Association template include
            if 'include' in ci_content:
                includes = ci_content['include']
                if isinstance(includes, list):
                    for inc in includes:
                        if isinstance(inc, dict) and 'project' in inc:
                            if 'gitlab_templates' in inc['project']:
                                print(f"  ✅ Uses Drupal Association template")
                                break
                else:
                    print(f"  ℹ️ Custom .gitlab-ci.yml (not using template)")
            else:
                self.validation_results['recommendations'].append(
                    ".gitlab-ci.yml should include Drupal Association template"
                )
                print(f"  ⚠ Not using Drupal Association template")

        except yaml.YAMLError as e:
            self.validation_results['recommendations'].append(
                f".gitlab-ci.yml has invalid YAML: {e}"
            )
            print(f"  ❌ Invalid YAML: {e}")

    def _determine_status(self) -> None:
        """Determine overall validation status."""
        # FAIL if any required files are missing
        if self.validation_results['missing_files']:
            self.validation_results['status'] = 'FAIL'
        # FAIL if any critical issues in incomplete files
        elif self.validation_results['incomplete_files']:
            self.validation_results['status'] = 'FAIL'
        # PASS otherwise
        else:
            self.validation_results['status'] = 'PASS'

    def _add_error(self, message: str) -> None:
        """Add critical error that causes validation to fail.

        Args:
            message: Error message
        """
        if 'errors' not in self.validation_results:
            self.validation_results['errors'] = []
        self.validation_results['errors'].append(message)
        self.validation_results['status'] = 'FAIL'

    def _add_incomplete_file(self, filename: str, issue: str) -> None:
        """Add incomplete file issue.

        Args:
            filename: File with issue
            issue: Description of issue
        """
        self.validation_results['incomplete_files'][filename] = issue

    def print_results(self) -> None:
        """Print validation results in human-readable format."""
        status = self.validation_results['status']
        status_icon = '✅' if status == 'PASS' else '❌'

        print(f"\n{'='*60}")
        print(f"{status_icon} VALIDATION {status}")
        print(f"{'='*60}\n")

        if self.validation_results['missing_files']:
            print("Missing Required Files:")
            for f in self.validation_results['missing_files']:
                print(f"  - {f}")
            print()

        if self.validation_results['incomplete_files']:
            print("Incomplete Files:")
            for f, issue in self.validation_results['incomplete_files'].items():
                print(f"  - {f}: {issue}")
            print()

        if self.validation_results['readme_issues']:
            print("README.md Issues:")
            for issue in self.validation_results['readme_issues']:
                print(f"  - {issue}")
            print()

        if self.validation_results['recommendations']:
            print("Recommendations:")
            for rec in self.validation_results['recommendations']:
                print(f"  - {rec}")
            print()

        # Final summary
        if status == 'PASS':
            print("✅ Module is ready for Drupal.org contribution!")
        else:
            print("❌ Module needs fixes before Drupal.org contribution")
            print("\nType 'generate' to create missing files automatically.")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='Validate Drupal module for Drupal.org contribution'
    )
    parser.add_argument(
        'module_path',
        nargs='?',
        default='.',
        help='Path to Drupal module directory (default: current directory)'
    )
    parser.add_argument(
        '--json',
        action='store_true',
        help='Output results as JSON'
    )

    args = parser.parse_args()

    # Run validation
    validator = ModuleValidator(args.module_path)
    results = validator.validate()

    # Output results
    if args.json:
        print(json.dumps(results, indent=2))
    else:
        validator.print_results()

    # Exit with appropriate code
    sys.exit(0 if results['status'] == 'PASS' else 1)


if __name__ == '__main__':
    main()