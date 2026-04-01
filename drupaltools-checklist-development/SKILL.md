---
name: drupaltools-checklist-development
description: Guide Drupal projects through development lifecycle checklists. Use this skill when starting a new project, preparing for deployment, checking project completeness, or managing a Drupal project from setup to production launch.
---

# Drupal Project Development Checklist

Guide projects through the Drupal development lifecycle.

## Scope

**This skill covers:**
- Project planning and architecture decisions
- Development workflow checklists
- Testing strategy and implementation
- Deployment preparation and checklists
- Post-launch maintenance tasks

**For machine setup**, use `drupaltools-developer-setup`.

## Project Phases

### 1. Project Initiation

| Task | Status |
|------|--------|
| Define content types and taxonomy |
| Plan view configurations |
| Design paragraph/component architecture |
| Choose contributed modules |
| Document custom module requirements |

### 2. Development Standards

- Follow `drupaltools-best-practices` for code standards
- Use `drupaltools-coding-standards` for PHPCS/PHPStan
- Implement automated testing (PHPUnit, Behat)
- Configure git hooks with CaptainHook

### 3. Testing Checklist

| Test Type | Tool | When |
|-----------|------|-------|
| Unit tests | PHPUnit | Every commit |
| Browser tests | Behat | Feature completion |
| Code standards | PHPCS/PHPStan | CI/CD pipeline |
| Accessibility | WAVE/axe | Before release |
| Performance | PageSpeed/Lighthouse | Pre-launch |

### 4. Pre-Deployment

| Task | Command |
|------|---------|
| Disable dev modules | `drush pm-uninstall devel kint` |
| Enable caches | `drush cr` |
| Configure syslog | Settings.php |
| Run update.php | `drush updb` |
| Export config | `drush cex` |

### 5. Post-Launch

- Monitor with Uptime Robot
- Setup log aggregation
- Schedule regular updates
- Review error logs weekly
- Backup verification monthly

## Module Recommendations

When choosing modules, prefer:
- Actively maintained (>6 months recent commits)
- Compatible with target Drupal version
- Has test coverage
- Has clear documentation

Use `drupaltools-code-search` to find examples of module usage.

## Automation

Suggest Drush commands for repetitive tasks:
```bash
# Update all contrib modules
drush upc -y

# Run database updates
drush updb -y

# Clear cache
drush cr
```

## Resources

- [Drupal.org: Creating Modules](https://www.drupal.org/docs/develop/creating-modules)
- [Drupal.org: Deployments](https://www.drupal.org/docs/managing-accessed-sites)
