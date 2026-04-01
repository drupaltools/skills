---
name: drupaltools-maintenance-contract
description: Drupal maintenance and support contract templates, task lists, SLA parameters, and handoff procedures. Use this skill when the user asks about Drupal maintenance contracts, support plans, SLA definitions, maintenance pricing, or needs guidance on dropping support/handoff procedures for a Drupal project.
---

# Drupal Maintenance Contract Guide

Templates and guidelines for Drupal maintenance and support contracts.

Source: https://raw.githubusercontent.com/theodorosploumis/notes/refs/heads/master/drupal/contract.md

## Overview

This skill helps define, price, and manage Drupal maintenance contracts including SLAs, task lists, and project handoff procedures.

## Parameters to Consider

Before drafting a contract, assess these project factors:

- **Drupal version** - Newer versions have different maintenance needs
- **Hosting environment** - Managed vs self-hosted affects responsibility
- **SLA requirements** - Define uptime guarantees ([uptime.is](https://uptime.is))
- **User accounts** - Anonymous registration increases security concerns
- **User permissions/roles** - Complexity affects maintenance effort
- **3rd party integrations** - APIs, auth, external JS (more = more issues)
- **Database size & growth** - Large databases need special handling
- **Migration history** - Older migrations may have legacy issues
- **Website activity** - Traffic, bandwidth, page impressions, peak loads
- **Custom code** - Custom modules/themes require specialized maintenance
- **Multisite setup** - Multiple sites multiply maintenance effort
- **eCommerce** - Commerce sites need special treatment and security
- **Special requirements** - Government, healthcare, etc. may have compliance needs

## Common Maintenance Tasks

### Security & Updates
- Drupal core security updates (with dependencies)
- Drupal core minor version upgrades (e.g., 8.9.2 → 8.9.11)
- Contributed module security updates
- Contributed theme security updates
- 3rd party integration updates (API endpoints, libraries)
- Apply patches when upstream commits land
- Database and entity updates after code changes

### Support & Monitoring
- Bug fixes (existing code & infrastructure)
- Offsite backups (db, public files, code) with restore testing
- Disaster recovery planning
- Support channels: phone, email, ticketing system
- 24×7 support availability (weekends/holidays)
- Response time commitments: 1/8/24/72 hours
- Uptime monitoring
- Version control with 3 environments (dev, stage, prod)

### Quality & Security
- Security auditing
- Spam filtering and cleansing
- Malware filtering and cleansing
- Hacked website repair
- Broken link scanning
- System/infrastructure updates

### Reporting & Documentation
- Weekly/monthly reports
- Knowledge database creation (maintenance documentation)
- Internal support sheet updates (versions, credentials)

## Time Estimates (Reference Only)

Monthly hours needed based on project complexity:

| Project Type | Monthly Hours |
|--------------|---------------|
| Simple D8+ site, few modules | ~1 hour |
| Multisite (5 simple sites) | ~3 hours |
| Complex site, many modules/integrations | 6-10 hours |
| Simple Commerce site | ~6 hours |
| Large site with user accounts, 3rd party | 10+ hours |

## Maintenance Plan Template

Proposed schedule (from AdciSolutions):

| Frequency | Task |
|-----------|------|
| Monthly (1st Wednesday) | Minor Drupal version update (bug fixes) |
| Monthly (3rd Wednesday) | Check security releases in contrib modules |
| Monthly + 2 days post-deploy | Track errors (GA, logs, QA) |
| Quarterly | SEO audit |
| Semi-annually | Accessibility compliance check |
| Semi-annually | Google PageSpeed optimization |
| Semi-annually | Refactor frontend code |
| Annually | PHP version update |
| 2 weeks before expiry | SSL certificate renewal |
| Every update | Check custom code functionality |
| Every update | Update internal Support Sheet |
| Annually | Review/renew Support Contract terms |

## Sample Maintenance Plans

### Plan A - Basic ($2000/yr)
- Core security updates ✓
- Core minor version upgrade ✓
- Contrib modules/themes security updates ✓
- Bug fixes (existing code) ✓
- Version control with dev/stage/prod ✓
- Email support ✓
- Response time: 24hr
- Monthly report ✓
- 12-month contract
- Extra tasks: $35/hr

### Plan B - Standard ($3000/yr)
- Everything in Plan A
- Response time: 8hr
- Extra tasks: $35/hr

### Plan C - Premium ($5000/yr)
- Everything in Plan B
- Phone support ✓
- 24×7 support ✓
- Response time: 2hr
- Extra tasks: $30/hr

## Drop Support / Handoff Procedure

When ending maintenance for a client:

### Pre-Handoff
- [ ] **Full backup** of Production (database, public files, code)

### Drupal Account Cleanup
- [ ] Change User 1 email or create new Admin accounts for new company
- [ ] Remove/change emails for non-admin company accounts
- [ ] Remove company emails from Security Updates alerts
- [ ] Change 3rd party credentials (SOLR, Elasticsearch, etc.)
- [ ] Remove your credentials from the website

### DNS & Infrastructure
- [ ] Remove DNS records pointing to `.mycompany.domain` subdomains (Cloudflare, etc.)
- [ ] Delete site aliases on server for company subdomains

### Hosting Cleanup
- [ ] Remove SSH keys and `known_hosts` entries
- [ ] Remove all `.git` folders
- [ ] Remove CI/CD credentials
- [ ] Remove your email from hosting provider

### Project Closure
- [ ] Disable testing tools (GitHub Actions, BitBucket Pipelines, CircleCI)
- [ ] Disable server health monitoring
- [ ] Archive project in internal PM tool (tasks/issues)
- [ ] Update internal documentation and Support Sheet
- [ ] Check company blog for project references (case studies) and update
- [ ] **Team retrospective**: Discuss why support was dropped (lessons learned)

## Contract Clauses to Define

- **SLA terms** - Uptime %, response times, resolution times
- **Support hours** - Business hours vs 24×7
- **Contact methods** - Email, phone, ticketing system
- **Included work** - What's covered vs billable
- **Excluded work** - New features, major upgrades, redesigns
- **Hourly rate** - For out-of-scope tasks
- **Contract duration** - 6/12 months with renewal terms
- **Termination clause** - Notice period, handoff procedure
- **Backup responsibilities** - Who maintains backups and for how long
- **Liability limits** - Max liability for data loss, downtime

## Resources

- [Wikipedia - Service Level Agreement](https://en.wikipedia.org/wiki/Service-level_agreement)
- [Appnovation Drupal Support](https://www.appnovation.com/services/drupal-development/support-maintenance)
- [OpenSense Labs - Support Guide](https://opensenselabs.com/blog/articles/a-drupal-support-and-maintenance-guide)
- [Drupal Partners - Maintenance](https://www.drupalpartners.com/services/drupal-maintenance-and-support-company)
- [Maintainn - WordPress/Dupal Maintenance Plans](https://maintainn.com/plans)
- [Freelock - Drupal Protection Plan](https://www.freelock.com/product/drupal-protection-plan)
- [Adci Solutions - Maintenance Importance](https://www.adcisolutions.com/knowledge/importance-website-maintenance)
