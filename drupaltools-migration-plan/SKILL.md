---
id: drupaltools-migration-plan
name: drupaltools-migration-plan
version: 1.0.0
description: Generate comprehensive Drupal migration plans with entity mapping, ETL strategies, rollback procedures, and source analysis based on best practices from the Drupal migration guide.
author: Theodoros Ploumis
---

# Drupal Migration Plan Generator

A comprehensive skill for planning Drupal migrations from older versions (7.x, 6.x) to modern Drupal (9+, 10+). This skill provides structured guidance for source analysis, entity mapping, migration architecture, testing strategies, and rollback procedures.

## Overview

When assisting with Drupal migrations, this skill provides:

- **Source Site Analysis**: Identify entities, fields, and configurations to migrate
- **Entity Mapping**: Document mappings between source and target structures
- **ETL Strategy**: Define extract, transform, and load procedures
- **Testing Plans**: Comprehensive checklists for validation
- **Rollback Procedures**: Backup and recovery strategies

## When to Use

Activate this skill when the user asks about:

- Planning a migration from Drupal 7.x/6.x to Drupal 9+/10+
- Creating migration documentation for stakeholders
- Designing ETL strategies for content migration
- Preparing testing procedures for migrated content
- Planning rollback strategies and disaster recovery
- Documenting entity mappings between source and target sites
- Migration module recommendations

**Trigger phrases:**
- "How do I plan a Drupal 7 to 10 migration?"
- "What entities do I need to migrate?"
- "How do I test my migration?"
- "What's the rollback procedure?"
- "Which migration modules should I use?"
- "How do I map old fields to new ones?"
- "migration plan for drupal"
- "drupal upgrade strategy"

## Migration Planning Process

### Step 1: Source Site Analysis

Document all entities on the source site:

**Entities to inventory:**

| Entity Type | Check For | Notes |
|-------------|-------------|-------|
| Nodes | Content types, fields, revisions | Count per type |
| Users | Roles, profile fields | Include blocked users? |
| Taxonomy | Vocabularies, term hierarchy | Deep nesting? |
| Files | Public, private, attached to fields | Size and count |
| Paragraphs | Paragraph types, parent references | Revisions? |
| Blocks | Custom blocks, placements | Block types |
| Menus | Menu links, hierarchy depth | Custom menus |
| Views | Displays, exposed filters | Complex views? |
| Forms | Webforms, contact forms | Submissions? |
| URL Aliases | Patterns, redirects | Custom aliases |

**Tools for analysis:**
- For Drupal 7.x/6.x: Use [drupal-report](https://github.com/theodorosploumis/drupal-report)
- Create Views on source site to get entity overviews
- Document database credentials

### Step 2: Migration Architecture

**Required modules:**

| Module | Type | Purpose |
|--------|------|---------|
| migrate | Core | Migration framework |
| migrate_drupal | Core | Drupal-to-Drupal migrations |
| migrate_plus | Contrib | Enhanced migration tools |
| migrate_tools | Contrib | Drush commands |
| migrate_devel | Contrib (optional) | Debugging |
| config_devel | Contrib (optional) | YAML management |

**Custom module structure:**

```
modules/custom/migrate_[source]_[target]/
├── migrate_[source]_[target].info.yml
├── migrations/
│   ├── migrate_plus.migration_group.[group].yml
│   └── migrate_plus.migration.[entity].yml
├── src/
│   ├── Plugin/migrate/source/
│   ├── Plugin/migrate/process/
│   └── Plugin/migrate/destination/
└── README.md
```

### Step 3: Entity Mapping

Create mapping documentation:

| Source | Source Fields | Target | Target Fields | Process | Notes |
|--------|---------------|--------|---------------|---------|-------|
| node:article | title, body, field_tags | node:blog | title, body, field_categories | default | Tags → Categories |
| user | name, mail, field_bio | user | name, mail, field_profile | default | Bio → Profile |

**Field migration considerations:**

- `vid` (revision ID): Let Drupal generate new ones
- `uuid`: Let Drupal generate to avoid conflicts
- `nid`: Store old nid in custom field for reference
- Text with embedded files: Use DOMDocument for parsing
- Multilingual: Track translation sources carefully
- Paragraphs: Watch for asymmetric translations

### Step 4: Migration Groups

Organize migrations by dependency:

```yaml
# Group 1: Foundation (no dependencies)
- users
- taxonomy_terms
- files

# Group 2: Content (depends on foundation)
- nodes_basic
- nodes_with_media
- nodes_with_paragraphs

# Group 3: Navigation (depends on content)
- menu_links
- url_aliases
```

### Step 5: ETL Strategy

**Extract:**
- Use custom source plugins for complex SQL
- Use `prepareRow()` for row-level filtering (not `query()` for distinct)
- Skip rows: `return FALSE` in `prepareRow()`

**Transform:**
- Process plugins for field transformations
- DOMDocument for HTML parsing
- Migrate files before content that references them

**Load:**
- Migrate data only, not settings
- Use Drush commands, not UI
- Continuous config import/export during development

### Step 6: Testing Checklist

**Pre-migration:**
- [ ] Database connectivity verified
- [ ] Source site Views created for data overview
- [ ] Custom plugins tested independently

**Post-migration content:**
- [ ] Random `/node/NID` paths resolve
- [ ] Node counts match (source vs target)
- [ ] Sample field values verified
- [ ] Paragraph references intact
- [ ] Media/file references working

**Post-migration multilingual:**
- [ ] Non-source translations have new nids
- [ ] Translation relationships preserved
- [ ] Language switcher functional
- [ ] Browser language redirect works

**Post-migration navigation:**
- [ ] Path aliases exist and resolve
- [ ] Menu links present and functional
- [ ] URL redirects work correctly

**Post-migration workflows:**
- [ ] Translation add form works
- [ ] Translation edit form works
- [ ] Translation delete works
- [ ] Unpublish hides menu link and language switch
- [ ] Content moderation states functional

### Step 7: Rollback Strategy

**Pre-production backups:**

```bash
# Database backup
drush sql:dump --result-file=/backup/pre-migration.sql

# Configuration export
drush config:export --destination=/backup/config-pre-migration
```

**Rollback commands:**

```bash
# Stop running migration
drush migrate:stop [migration_id]

# Reset migration status
drush migrate:reset-status [migration_id]

# Rollback migration
drush migrate:rollback [migration_id]

# Restore database (if needed)
drush sql:cli < /backup/pre-migration.sql
```

**Post-migration cleanup:**
- Uninstall migration modules
- Remove migration DB credentials from settings.php
- Archive migration YAML files

## Database Configuration

Add to `sites/default/settings.php`:

```php
$databases['migrate']['default'] = [
  'database' => 'drupal7',
  'username' => 'drupal7',
  'password' => 'drupal7',
  'prefix' => '',
  'host' => 'database.7x-website.host',
  'port' => '3306',
  'namespace' => 'Drupal\\Core\\Database\\Driver\\mysql',
  'driver' => 'mysql',
];
```

## Essential Drush Commands

```bash
# List all migrations
drush migrate:status

# Run specific migration
drush migrate:import [migration_id]

# Update existing content
drush migrate:import [migration_id] --update

# Rollback migration
drush migrate:rollback [migration_id]

# Run group of migrations
drush migrate:import --group=[group_id]
```

## Best Practices

1. **Get an overview** of source site before planning (follow Main menu as anonymous user)
2. **Always use migrate_plus** for enhanced migration capabilities
3. **Create a custom module** to hold migration plugins and YAML files
4. **Migrate only data**, never settings or permissions
5. **Clone core YAML files** to your module, don't reference directly
6. **Keep migrations simple** - prefer custom plugins over complex dependencies
7. **Use generic module names** for easy reuse in future projects
8. **Group related migrations** that run together
9. **Always use Drush**, never the UI for running migrations
10. **Document everything** in README with mappings and commands
11. **Use config_devel** for easier YAML management during development
12. **Copy private files** with rsync before content migration
13. **Store old nid** in custom field for testing reference
14. **Avoid vid/uuid conflicts** - let Drupal generate new values
15. **Filter rows** by returning `FALSE` in `prepareRow()`
16. **Parse HTML** with PHP DOMDocument for embedded content
17. **Clean up** - uninstall migration modules after production

## Common Issues and Solutions

| Issue | Solution |
|-------|----------|
| vid/uuid errors | Don't migrate these, let Drupal generate new |
| Multilingual revision conflicts | Track translation sources separately |
| HTML embedded images | Use DOMDocument to extract and migrate |
| Distinct rows in query | Use `prepareRow()` filtering, not SQL DISTINCT |
| Demo content ID conflicts | Clear demo content before production migration |
| Asymmetric paragraph translations | Handle each language variant separately |

## References

- [Drupal.org Migrate API Documentation](https://www.drupal.org/docs/drupal-apis/migrate-api)
- [drupalmigrate.org](https://drupalmigrate.org)
- [Migration modules directory](https://drupalmigrate.org/search/modules)
- [migrate_tools Drush commands](https://www.drupal.org/node/1561820)
- [Drupal core migration YAML files](https://git.drupalcode.org/project/drupal/-/tree/10.0.x/core/modules/node/migrations)
- [Drupal core source plugins](https://git.drupalcode.org/project/drupal/-/tree/10.0.x/core/modules/node/src/Plugin/migrate/source)

## Keywords

drupal migration, migrate api, migrate_plus, drupal 7 to 10, drupal 6 to 9, upgrade drupal, migration plan, entity mapping, content migration, etl, rollback migration, migration testing, migration drush, migrate_tools, migration architecture, migrate_devel
