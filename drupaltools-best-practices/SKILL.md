---
name: drupaltools-best-practices
description: Audit code or a folder against Drupal best practices. Use this skill whenever the user wants to review, check, or improve Drupal code quality — including custom modules, themes, config YAML files, machine names, field definitions, Views config, Twig templates, composer.json, settings.php, or any Drupal-related file. Trigger for requests like "check my module against best practices", "review this Drupal code", "is this the right way to do X in Drupal", "audit my theme/config/field setup", or any time the user pastes Drupal PHP, YAML, or Twig and asks for a review. Also trigger when the user asks about Drupal naming conventions, scaffolding, or project structure.
---

# Drupal Best Practices Auditor

Source: https://raw.githubusercontent.com/theodorosploumis/drupal-best-practices/refs/heads/master/README.md
Covers Drupal 8.x and above.

## Step 1 — Detect context

Before auditing, identify:

1. **No input provided** — ask the user to paste code, a file path, or a folder structure.
2. **Drupal version** — if unknown, assume 9.x/10.x and flag if advice may differ.
3. **What was given** — detect the type(s) from the table below and audit only the applicable categories.
4. **Minified or generated files** — warn that results may be incomplete; ask for source.

| Input type | Categories to check |
|------------|-------------------|
| PHP (module/plugin) | Coding, Naming, Permissions, Documentation |
| Twig template | Theming, Naming |
| YAML (config) | Naming, Site building (entity/field/view type) |
| composer.json / composer.lock | Scaffolding, Third-party libraries |
| settings.php | Scaffolding, Infrastructure |
| Folder structure | Scaffolding, Naming, Coding |
| Machine names only | Naming |

## Step 2 — Audit categories

Check every applicable category below. For each category not applicable to the input, write one line: "Not applicable: [category]."

### A. Naming conventions
- Machine names: letters only, no special chars, no spaces, singular (not plural).
- Custom module names must be prefixed with `projectmachinename_`.
- Theme machine name: one word, no `theme` in the name, no base-theme name embedded.
- Field machine names follow pattern: `field_[content_type]_[short_name]` for specific fields; `field_[generic_name]` for shared fields.
- View modes: generic names not tied to a field or dimension (e.g. `wide` not `wide_1920x570`).
- Views: no `_1` suffix on display machine names; remove default suffix.
- Image styles: generic, not dimension-based (e.g. `large` not `large_600x300`).
- User roles: one word (e.g. `author` not `authors`, `admin` not `super_administrator`).
- Avoid names that shadow existing Drupal core or contrib names.

### B. Site building
- Nodes: no nodes used as dynamic blocks; use custom block types or entities instead.
- Revisions: not enabled by default unless content requires workflow states.
- Taxonomy: terms used only when categorized pages are needed, not just for filtering.
- Fields: all fields have a Description; image field directories are named (not default date-based); `gif` removed from image fields unless required.
- Views: one display per View (except when required); `Format > Show: Content` used (not fields); Ajax disabled by default; "No results" text provided; Access set to Permission not Role; unused Views disabled.
- Menus: real `<menu>` elements used, not block-as-menu workarounds; `<nolink>` for placeholder paths.
- Text formats: one HTML-allowed format; CKEditor buttons match allowed HTML tags; no PHP in WYSIWYG.
- Users/roles: roles split by persona; no shared accounts; `authenticated` role has no extra permissions.

### C. Theming
- One base theme only; subtheme name independent of base theme name.
- Preprocess functions used for custom attributes/classes, not inline Twig logic.
- CSS classes: `twig-` prefix for Twig-added classes, `js-` prefix for JS-triggered classes.
- No non-semantic utility classes (e.g. `clearfix`, `full-width` as CSS class names).
- SASS/SCSS used; large SCSS files split by entity or concern.
- Twig templates overridden only from the source module (not copied from random places).
- Special pages templated: 404, 403, maintenance, login.
- Path aliases not used as CSS class hooks.

### D. Coding (PHP / module)
- All functions/classes documented with docblocks.
- Private functions at bottom of file; never called outside declaring module.
- Custom permissions defined per module; never reuse existing permissions.
- Permission titles start with a verb: "View …", "Administer …", "Delete …".
- Machine names are human-readable (no abbreviations like `field_mytype_ac_y_d`).
- Drupal coding standards followed: https://www.drupal.org/docs/develop

### E. Scaffolding / project structure
- `drupal/recommended-project` used as base; not core's own `composer.json`.
- One `settings.php` that includes environment-specific files; settings.php tracked in git; env-specific files are not.
- Credentials and passwords in `.env` files, never in tracked files.
- `config/` folder outside web root, tracked in git.
- `vendor/` outside web root.
- Composer used for all dependencies; only `composer.json` and `composer.lock` tracked.
- Specific version pinned for all packages (e.g. `"drupal/core": "10.2.3"` not `"^10"`).
- Patches via `cweagans/composer-patches` using static patch files only.
- Less modules is better; prefer core modules over contrib when possible.

### F. Third-party libraries
- Check if the library is already in Drupal core before adding it.
- Prefer specific releases over branches.
- Prefer local copies over CDN for performance.

### G. Infrastructure / environment
- `dblog` module not enabled on live; use `monolog` or `syslog`.
- Cron run externally (not via Drupal core cron).
- Dev modules listed (should not be on live): `devel`, `stage_file_proxy`, `reroute_email`, etc.

## Step 3 — Output format

For each issue found:

---

**Issue N — [Short title]**

- **Category:** [A–G from above]
- **Severity:** [Critical / High / Medium / Low]
- **Affected code or name:** [paste verbatim]
- **Problem:** [One or two sentences.]
- **Fix:** [Corrected code, name, or action.]

---

If a category has no issues: "No issues found: [category]."
If everything passes: write a short paragraph summarising what is correct and why.

## Severity scale

| Severity | Definition |
|----------|------------|
| Critical | Security risk, data loss risk, or blocks core Drupal functionality (e.g. credentials in tracked files, PHP in WYSIWYG, keyboard trap). |
| High | Will cause bugs, config sync failures, or significant maintenance pain (e.g. wrong naming pattern, revisions on all nodes, role-based Views access). |
| Medium | Degrades maintainability or DX (e.g. missing field descriptions, `_1` suffix on Views display, non-generic View mode names). |
| Low | Minor convention deviation with negligible impact (e.g. slightly generic machine name, missing admin comment on a View). |

## Machine name quick reference

| Type | Bad | Good |
|------|-----|------|
| User role | `super_administrator` | `admin` |
| Entity bundle | `newsarticle`, `events` | `news`, `event` |
| Field (specific) | `field_a_l_of_links` | `field_article_links` |
| Field (shared) | `field_countries` | `field_taxonomy_country` |
| View mode | `news_simple`, `wide_teaser` | `simple`, `wide` |
| Views display | `views.news.page_1` | `views.news.page` |
| Image style | `large_600_300`, `3_2` | `large`, `ratio_3_2` |
| Theme | `my_bootstrap_theme` | `myproject` |
| Module | `mymodule` | `projectname_mymodule` |

## External references

- Best practices source: https://github.com/theodorosploumis/drupal-best-practices
- Drupal development standards: https://www.drupal.org/docs/develop
- Drupal coding standards: https://www.drupal.org/docs/develop/standards
- Drupal-spec-tool (automated testing): https://github.com/acquia/drupal-spec-tool
- Composer best practices: https://www.lullabot.com/articles/drupal-8-composer-best-practices
- Module incompatibilities (Acquia): https://docs.acquia.com/acquia-cloud/develop/drupal/module-incompatibilities
