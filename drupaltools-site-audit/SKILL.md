---
name: drupaltools-site-audit
description: Generate comprehensive Drupal site audit reports before RFPs or project proposals. Use this skill when inspecting a Drupal site, preparing a technical report, or evaluating an existing Drupal project for fixes or changes.
---

# Drupal Site Audit Report

Generate a comprehensive audit report for Drupal sites before providing proposals or starting work.

## When to Use

Use this skill when:
- "Audit this Drupal site"
- "Prepare a report before starting"
- "Inspect Drupal project structure"
- "Generate a technical report for RFP"

## Before the Report

Gather this information before starting:

### Required

- [ ] Technical specification document (if exists)
- [ ] Drupal admin credentials (user 1 or Admin role)
- [ ] Brief project scope
- [ ] Project goals and success metrics
- [ ] Why changes are needed (fixes, update, upgrade, migration)
- [ ] New theme/skin required?

### Important

- [ ] Current process flow diagram (if integrating with other services)
- [ ] List of things that don't work well
- [ ] Number of different content authors
- [ ] User roles and permissions structure
- [ ] Total Drupal nodes count
- [ ] Data migration needs
- [ ] Third-party payment services (CDN, etc.)
- [ ] Current hosting provider and specs
- [ ] Technical support plan

## Common Reports

### Performance
- PageSpeed Insights
- GTmetrix
- Yellow Lab Tools

### SEO & UX
- SEO checklist
- Mobile responsiveness
- Heatmaps (Hotjar)

### Security
- Drupal Security Scanner (hackertarget.com)
- Security Headers
- Sucuri SiteCheck

## Drupal Specific Audit

### Content Structure
- [ ] Content types and taxonomy
- [ ] Fields and their usage
- [ ] Node count per type
- [ ] Paragraphs usage

### Functionality
- [ ] Core features and functionality (F&F)
- [ ] Drupal forms
- [ ] Views count and complexity
- [ ] Custom modules

### Users & Permissions
- [ ] User roles defined
- [ ] Role permissions
- [ ] Content access restrictions
- [ ] Create demo users for testing

### Theming
- [ ] Base theme used
- [ ] Template files structure
- [ ] CSS/JS architecture
- [ ] Responsive breakpoints
- [ ] Display modes

### Modules
- [ ] Total enabled modules
- [ ] Deprecated/unmaintained modules
- [ ] Security updates needed
- [ ] Recommended new modules

### Technical
- [ ] PHP and server settings
- [ ] Caching configuration
- [ ] Multilingual setup
- [ ] Block structure
- [ ] Menus and navigation

## Audit Commands

Run these commands to gather site information:

```bash
# List enabled modules
drush pm-list --type=module --status=enabled

# Check module security updates
drush ups

# Export configuration
drush cex

# Get site information
drush status

# List content types
drush entity-type-list node

# Count nodes by type
drush eval "print_r(node_type_get_types());"

# List user roles
drush role-list

# Check PHP settings
php -i | grep memory_limit
```

## Useful Audit Modules

| Module | Purpose |
|--------|---------|
| `audit_export` | Export audit data |
| `field_report` | Field analysis |
| `security_review` | Security checklist |
| `unused_modules` | Find unused modules |
| `mglaman/drupal-check` | Check module health |

## Report Structure

### 1. Executive Summary
Brief overview of site health and recommendations.

### 2. Technical Findings
Detailed analysis by category:
- Content structure
- Modules and updates
- Performance
- Security
- Best practices violations

### 3. Recommendations
Prioritized list of fixes with:
- Issue description
- Impact level (High/Medium/Low)
- Estimated effort (hours)
- Recommended approach

### 4. Deliverables
- PDF report with screenshots
- Itemized pricing
- Timeline estimate

## Best Practices

- **Do not give estimates before completing the audit**
- **Get credentials or demo access before starting**
- **Use agile methodology - fix one thing at a time, get paid by hour**
- **Treat the report as a doctor's diagnosis**
- **Avoid criticizing previous developers - focus on the site**
- **Consider refusing poorly structured projects**

## Resources

- [Drupal Audit Guide](https://github.com/axelerant/engineering/blob/main/audit.md)
- [Palantir Build Spec](https://docs.google.com/spreadsheets/d/15htLLWLguhwiuTLg_nndQNpgWVdUMy6UaR_d1q-v6iw)
- [Drupal Spec Tool](https://docs.google.com/spreadsheets/d/1h-SieCV9Dtrj8F4bqMvsbcHwIibN30j2oR9FMRDFT-8)
