---
name: drupaltools-translations
description: Comprehensive guide for Drupal multilingual and translation workflows including interface translation, configuration translation, entity translation, PO/POT file management, and translation service integration. Use this skill when the user asks about Drupal translations, multilingual setup, i18n, translation modules, PO files, localization, or needs help with translation workflows, import/export, or external translation services.
---

# Drupal Translations Guide

Comprehensive guide for Drupal multilingual websites, translation workflows, and localization best practices.

Source: https://raw.githubusercontent.com/theodorosploumis/notes/refs/heads/master/drupal/translations.md

## Overview

Drupal translations involve multiple layers:
- **Interface translation**: UI strings (t(), trans())
- **Configuration translation**: Settings, labels, descriptions
- **Content translation**: Nodes, taxonomy terms, blocks
- **Entity translation**: Custom entities with multilingual support

## Translation Steps for Drupal Projects

### Initial Setup

1. Install profile with required modules
2. Enable additional languages (non-English)
3. Configure language negotiation at `/admin/config/regional/language`

### Translation Workflow

1. **Interface Translation UI** (`/admin/config/regional/translate`)
   - Add translations for interface strings
   - Search and translate individual strings

2. **Configuration Translation** (`/admin/config/regional/config-translation`)
   - Translate settings forms and configuration
   - Also accessible via "Translate" tab on each config form

3. **Export Translations**
   - Export PO files per language: `drush locale:export LANGCODE`
   - Store in `mymodule/translations/mymodule.LANGCODE.po`
   - Define path in `mymodule.info.yml`: `translation path: translations/mymodule.LANGCODE.po`

4. **Config Translation Export**
   - Export config YML files with translations
   - Copy files from `config/sync/language/*` to module's `config/install/language/*`

5. **Entity/Content Translation**
   - Use CSV import for bulk content translation
   - Manual translation through UI for menu items, blocks, nodes, taxonomy

## Translation Storage Matrix

| **Type** | **Configuration** | **Twig Templates** | **Module Strings** | **Drupal Entities** |
| :---: | :---: | :---: | :---: | :---: |
| Source | PO, YML | PO | PO | CSV |
| Location | YML: `install/language/LANG`<br>PO: `translations/` folder | `translations/` folder | `translations/` folder | Custom migration module |
| Translation Server | Yes (PO, POTX only) | Yes | Yes | No |

## Essential Drush Commands

```bash
# Install profile with specific language
drush si MYPROFILE --locale de -y

# Core locale commands
drush locale:check
drush locale:update
drush locale:export LANGCODE
drush locale:import LANGCODE PATH_TO_PO_FILE

# Examples
drush locale:import de modules/custom/MY_MODULE/translations/MY_MODULE.de.po
drush locale:import nl modules/custom/MY_MODULE/translations/MY_MODULE.nl.po

# Config language negotiation
drush cget system.site
drush config:set language.negotiation url.prefixes.el el
```

## Recommended Translation Modules

### Essential
- **tmgmt** - Translation Management Tool (comprehensive workflow)
- **potx** - Translation template extractor (PO/POT generation)
- **l10n_client** - On-page translation interface
- **babel** - Content translation workflow enhancement

### Specialized
- **config_import_locale** - Config translation import
- **config_translation_access** - Access control for config translation
- **potion** - Drush-based PO file management
- **multilingual_audit** - Audit multilingual setup
- **tmgmt_spreadsheet** - Spreadsheet-based translation workflow
- **translation_extractor** - Automated string extraction

### Utilities
- **interface_string_stats** - Translation statistics
- **l10n_tools** - Localization helper tools
- **locale_override** - Override specific translations
- **simple_entity_translations** - Simplified entity translation UI

## Translation Workflow with External Services

### Process A: Translate via Spreadsheet
```
Translator → Google Sheets (XLS) → CSV → PO (for non-entities)
```

### Process B: Translate via Translation Service
```
Translator → l10n_server (or Service) → Translate (manual or API) → Export PO → Import to /translations/PROJECT.LANGCODE.po
```

## Translation Spreadsheet Columns

Standard columns for collaborative translation (e.g., Google Sheets):

| Column | Purpose |
|--------|---------|
| location | Source location of string |
| source | English string to translate |
| target | Translated string |
| suggestion | Fuzzy/auto-suggestions |
| context | Unique key for disambiguation |
| comments | Notes for translators |
| updated | Last modified date |
| author | Latest editor |

## Key API Hooks and Functions

1. **locale.api.php** - Interface translation hooks
2. **hook_locale_translation_projects_alter** - Alter translation projects
3. **config_translation.api.php** - Config translation API
4. **hook_config_translation_info_alter** - Alter config translation metadata
5. **i18n group** - Internationalization utilities
6. **Translation class** - Core translation handling

## Complete Solution Requirements

When evaluating translation solutions, check for:
1. Export/import formats (PO, CSV, XLIFF, YML, XLSX, MO, REST)
2. Sync/update capabilities
3. Bulk translation cleanup options
4. Template export (POTX)
5. Translation status reports
6. On-page/in-place editing
7. Fuzzy suggestions
8. Translation user roles
9. Database storage for translation metadata
10. Translation merging capabilities
11. Context-based overrides
12. SEO validation for multilingual
13. Admin language toggle per user

## External Tools & Services

### Translation Services
- **localize.drupal.org** - Official Drupal localization server
- **drupal.org/project/l10n_server** - Self-hosted translation server
- **poeditor.com** - Online translation management
- **weblate.org** - Open source translation platform
- **localizejs.com** - JavaScript/on-the-fly translation

### Desktop & Online Utilities
- **poedit.net** - Desktop PO file editor
- **mlocati.github.io/jsgettext** - Online PO/POT/MO converter

## Common Translation Issues

### Known Core Issues
- Configuration language overwritten during module install ([#2905295](https://www.drupal.org/project/drupal/issues/2905295))
- Translated Config Override default behavior ([#2993984](https://www.drupal.org/project/drupal/issues/2993984))
- String context and location filters ([#2123543](https://www.drupal.org/project/drupal/issues/2123543))
- Cannot delete source strings in D8+ ([#2503893](https://www.drupal.org/project/drupal/issues/2503893))
- META: Modernize Locale module ([#3215707](https://www.drupal.org/node/3215707))

## Best Practices

1. **Structure**
   - Plan multilingual architecture early
   - Define content vs interface translation needs
   - Set up language negotiation strategies

2. **Development**
   - Use t() consistently in code
   - Provide context for ambiguous strings
   - Extract templates regularly with potx

3. **Workflow**
   - Separate interface and content translation workflows
   - Use CSV for bulk content translation
   - Keep PO files in version control

4. **Deployment**
   - Export/import translations before deployment
   - Test with all enabled languages
   - Verify RTL support if needed
