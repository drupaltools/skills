---
name: drupaltools-contrib-readme
description: Generate and validate README.md files for Drupal.org contribution. Use this skill when you need to create a README.md for a Drupal module, check an existing README for Drupal.org compliance, or fix README structure issues.
---

# Drupal Contributed Module README

Generate and validate README.md files following Drupal.org contribution guidelines.

## When to Use

Use this skill when:
- "Generate a README.md for my Drupal module"
- "Check my README.md for Drupal.org compliance"
- "Fix README structure issues"
- "Add missing README sections"

## README.md Requirements

### Required Sections

| Section | Required | Description |
|---------|----------|-------------|
| About | **Yes** | Module purpose, first ~200 chars shown in listings |
| Features | **Yes** | Functionality and use cases |
| Extend and override | Recommended | Hooks, events, extension points |

### Optional Sections

| Section | When to Include |
|---------|-----------------|
| Requirements | If dependencies exist |
| Recommended modules | If complementary modules enhance functionality |
| Example code | For developer-facing modules |
| Similar projects | To differentiate from alternatives |
| Basic Services | Only if MODULE.services.yml exists |
| Supporting this Module | For sponsored/supported modules |
| Contributing | For community-contributed modules |
| Community Documentation | External resources, videos, demos |

### Prohibited Content

**Never include:**
- File structure diagrams/sections
- Installation instructions (`composer require`, `drush en`)
- "How to install" sections
- Beginner-friendly explanations
- `composer.lock` mentions

## Generate README.md

### Process

1. Read existing `MODULE.info.yml` to extract:
   - Module name and description
   - Core version requirement
   - Dependencies

2. Check for services file:
   ```bash
   ls MODULE.services.yml 2>/dev/null && echo "has_services"
   ```

3. Generate README with appropriate sections

### README Template

```markdown
# Module Name

About
-----
Introduction summarizing purpose and function. First ~200 characters shown in 
project listings. Accessible to users new to Drupal.

Features
--------
Basic functionality, unique features, and use cases.

Requirements
------------
Required modules and dependencies.

Example code
------------
Code examples for developers.

Extend and override
-------------------
Hooks, events, and extension points.

Supporting this Module
---------------------
Information about financial support or sponsorships.

Contributing
------------
Guidelines for contributing to the module.

Community Documentation
------------------------
Links to external resources, videos, demos.
```

## Validate README.md

### Check List

1. **Section presence** - All required sections exist
2. **Section order** - Follows Drupal.org ordering
3. **No prohibited content** - No install instructions, file structures
4. **Code examples** - Follow Drupal coding standards
5. **Content level** - Targets experienced developers

### Validation Output

```
✅ README.md VALIDATION PASSED

Required Sections: ✅ All present
- About section
- Features section
- Extend and override section

Content Quality: ✅ Good
- Targets experienced developers
- No installation instructions
- No file structure section

Recommendations:
- Consider adding "Example code" section for developer clarity
```

### Common Issues

| Issue | Fix |
|-------|-----|
| File structure section | Remove any file/folder diagrams |
| Installation instructions | Remove "How to install" sections |
| Beginner content | Rewrite for experienced developers |
| Missing About section | Add introduction, first ~200 chars |

## Resources

- [Drupal.org: Module Documentation](https://www.drupal.org/docs/develop/documentation)
- [Drupal.org: Readme Template](https://www.drupal.org/docs/develop/documentation/readme-template)
