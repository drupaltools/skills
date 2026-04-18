---
name: drupaltools-cost-estimation
description: Estimate costs and timeline for Drupal projects using a structured breakdown of tasks, roles, content types, and development work. Use this skill when the user asks for a project quote, cost breakdown, timeline estimation, budget planning, or resource allocation for a Drupal website. Trigger for requests like "how much would this Drupal project cost", "estimate this project", "create a quote", "plan the budget", or any discussion about pricing/timeline for Drupal development.
---

# Drupal Project Cost Estimation

Help estimate costs and timelines for Drupal projects using a structured approach that breaks down all components.

Source: https://raw.githubusercontent.com/theodorosploumis/notes/refs/heads/master/drupal/cost.md

> **Extended Parameters**: See HELPER.md for automated project analysis, git metrics, advanced task types, and feature-based parameters.

## Overview

Provide comprehensive cost estimates by analyzing project scope across multiple dimensions:
- Content structure and architecture
- User management complexity
- Theming and display requirements
- Module requirements (contrib and custom)
- Integration needs
- Timeline and resource allocation

## Detailed Cost Breakdown Table

For each project, create estimates using these categories:

| **Work/Tasks** | **Units** | **Title/Description** | **Cost/Unit** | **Total Cost** |
|----------------|-----------|-----------------------|---------------|----------------|
| **Operations** | | | | |
| User roles | count | Admin, Editor, Authenticated, etc. | | |
| User permissions | count | Granular permission sets | | |
| **Content Structure** | | | | |
| Node types (Content types) | count | Articles, Pages, Products, etc. | | |
| Node fields | count | Per-field type complexity | | |
| User profiles | count | Profile types needed | | |
| User profile fields | count | Fields per profile | | |
| Taxonomy types (Vocabularies) | count | Categories, Tags, etc. | | |
| Taxonomy fields | count | Fields per vocabulary | | |
| **Forms** | | | | |
| Form types (Webforms) | count | Contact forms, applications, etc. | | |
| Form fields | count | Fields per form | | |
| **Theming & Display** | | | | |
| Custom template files | count | Twig templates, overrides | | |
| Ready contrib modules | count | Off-the-shelf modules | | |
| Custom modules | count | Bespoke development | | |
| Custom theme(s) | count | Themes to build/adapt | | |
| Custom mixed content pages | count | Panel pages, landing pages | | |
| Custom views | count | Listings, filters, displays | | |
| Custom blocks | count | Block plugins, content blocks | | |
| **Quality & Compliance** | | | | |
| WAI/Accessibility compliance | hours | WCAG 2.1 AA implementation | | |
| **Scale Estimates** | | | | |
| Estimated deadline | weeks | Project timeline | | |
| Estimated users | count | Registered users expected | | |
| Estimated contents | count | Nodes, terms, media items | | |
| Estimated pageviews/traffic | per month | Traffic expectations | | |
| **Integrations** | | | | |
| External services | count | APIs, payment gateways, CRM | | |
| Website translation(s) | languages | Multilingual requirements | | |
| Content integrating | hours | Migration, import work | | |
| Content edit | hours | Editorial workflow setup | | |
| Other requirements | | Custom/specific needs | | |
| **Contingency** | | | | |
| Unforeseen expenses | 20% | Buffer for scope changes | | |
| **TOTAL** | | | | |

## Task Group Timeline Summary

Group tasks by phase for timeline visualization:

| **Task Groups** | **Tasks** | **Timeline** | **Cost** |
|-----------------|-----------|--------------|----------|
| **Structure** | Sitemap, Content scheme, Menus, Content types (nodes, taxonomies) | | |
| **Display** | Theme, Content pages, Views, Blocks, User pages | | |
| **Users** | Roles, Permissions, Actions, Workflows | | |
| **Translations** | Content type translations, interface translation | | |
| **Modules** | Contrib modules selection, Custom modules development | | |
| **3rd Party Services** | API integrations, External service connections | | |
| **TOTAL** | | | |

## Estimation Guidelines

### Complexity Multipliers
- **Simple**: Basic configuration, minimal custom code (1x)
- **Moderate**: Some custom theming, standard contrib modules (1.5x)
- **Complex**: Heavy customization, bespoke modules, multiple integrations (2-3x)

### Cost Per Unit Guidelines
- **Small site** (blog, brochure): $500-$2,000
- **Medium site** (corporate, small e-commerce): $3,000-$10,000
- **Large site** (enterprise, complex integrations): $10,000-$50,000+

### Timeline Guidelines
- **Discovery & Planning**: 1-2 weeks
- **Development**: 2-8 weeks (depending on scope)
- **Testing & QA**: 1-2 weeks
- **Deployment**: 3-5 days

## Usage

When a user asks for a cost estimate:

1. **Gather requirements** - Ask about project scope, features needed, integrations
2. **Fill the breakdown table** - Estimate units and costs for each row
3. **Create timeline summary** - Group into phases with durations
4. **Add 20% contingency** - Account for unforeseen work
5. **Present total** - Show both detailed breakdown and summary totals

Always remind users that these are estimates and actual costs may vary based on:
- Discovery findings
- Third-party service availability
- Content migration complexity
- Testing and revision rounds
- Ongoing maintenance needs
