---
name: drupaltools-cost-estimation-helper
description: Extended parameters and automated analysis guidance for Drupal project cost estimation. Companion file to the main cost estimation skill.
---

# Drupal Project Cost Estimation - Helper & Extended Parameters

This file contains extended parameters, automated analysis capabilities, and additional estimation dimensions not covered in the main SKILL.md.

---

## Automated Project Analysis

### Local Folder Scan
- Detect Drupal version (from composer.json, core/VERSION)
- Count custom modules (web/modules/custom)
- Count custom themes (web/themes/custom)
- Identify contrib modules (web/modules/contrib)
- Scan for configuration files (config/sync)
- Detect test files (PHPUnit, Nightwatch, etc.)

### Git Analysis Metrics
| Metric | Purpose | Data Points |
|--------|---------|-------------|
| Commit count | Project activity level | Total commits, commits per month |
| Commit analytics | Efficiency patterns | Average commit size, refactor ratio |
| Commit dates | Timeline estimation | First/last commit, active periods |
| Duplicate titles | Code review quality | Revert frequency, repetitive fixes |
| PRs | Collaboration overhead | Open/closed ratio, review time |
| Authors | Team size/complexity | Unique contributors, core team size |
| Branches | Workflow complexity | Active branches, merge patterns |
| Issues (from commits) | Bug density | Issue references, fix frequency |
| Code lines | Project size | Total lines, growth rate |
| Tests | Quality coverage | Test files, coverage percentage |

### Composer.json Analysis
- Required packages count
- Dev dependencies
- Drupal core version constraint
- Custom module namespaces
- Patches applied (complexity indicator)

### Existing Analysis Tools
Check for:
- PHPStan / Psalm configuration
- PHP_CodeSniffer rules
- Deprecation scanning tools
- Drupal-check (drupal/core-dev)
- CI/CD pipeline scripts

---

## Project Management Resources

### Input Documents
| Resource Type | Estimation Value |
|---------------|------------------|
| Requirements spreadsheet | Feature scope, priorities |
| PDF specifications | Technical constraints |
| Mockups/wireframes | UI complexity, page count |
| User stories | Functional requirements |
| API documentation | Integration complexity |

### Estimation Parameters
- **Cost per hour**: Base rate for calculations
- **Features list**: Prioritized backlog items
- **Team composition**: Roles needed (PM, Dev, QA, Design)

---

## Advanced Metrics & Results

### Abstract Metrics
| Metric | Calculation | Use Case |
|--------|-------------|----------|
| Cost per commit | Total cost / commit count | Efficiency benchmark |
| Developer efficiency | Features delivered / hours spent | Team productivity |
| Overall cost | Sum(all tasks) + contingency | Budget planning |
| Complexity score | Config depth + module count + custom code | Risk assessment |
| Code coverage | Tested lines / total lines | Quality indicator |

### Key Feature Outcomes
- High-value features identified
- Quick wins vs long-term investments
- Maintenance burden forecast

### Time-based Analysis
- All-time tasks completed
- Outcomes per sprint/iteration
- Velocity trends

---

## Example Q&A Patterns

### Strategic Questions
1. "How should we spend the next X hours on this project?"
   - Analyze: Current backlog + technical debt + quick wins
   - Output: Prioritized task list with ROI

2. "Similar projects we have done already?"
   - Cross-reference: Module patterns, complexity scores, timelines
   - Output: Comparable project list with actuals

3. "What is the risk level?"
   - Calculate: Custom code ratio + untested code + integration count
   - Output: Risk classification (Low/Medium/High)

---

## Extended Task Types

### Development Tasks
| Task Type | Estimation Factor |
|-----------|-------------------|
| Site building | 1x (configuration) |
| Migration | 2-3x (data complexity) |
| External service integration | 2-4x (API reliability) |
| Theming | 1.5-2x (design complexity) |
| Service development | 2x (custom business logic) |
| Roles and permissions | 1x (configuration) |
| Data entry | 0.5x per 100 items |
| Testing (code/UAT/e2e/QA) | 1.5x development time |
| Plan and architecture | 0.2x total project |
| Documentation | 0.1x total project |
| Meetings and collaboration | 0.15x total project |
| Presentations | Per occurrence |
| Drupal contrib (publish) | 3x (review process) |

---

## Feature-Based Parameters

### Project Characteristics
| Parameter | Impact on Estimate |
|-----------|-------------------|
| Multilingual | +30% per language beyond primary |
| User access complexity | +20-50% for complex permission schemes |
| Deadlines | Rush multiplier: 1.5x for tight deadlines |
| Budget constraints | Scope adjustment recommendations |
| Scope defined | 0.8x if 100% defined, 1.2x if <50% defined |
| Multisite | +40% per additional site |
| Simple vs Distro | Distro: +50% initial, -20% per clone |
| Similar to existing project | -30% if patterns reusable |
| Maintenance and support | 15-20% of build cost annually |
| New site vs Migration vs Redesign | Migration: +50%, Redesign: +40% |
| Content exists | Migration: 0.5h per 100 nodes |

---

## Drupal Concept Complexity Factors

| Concept | Simple | Moderate | Complex |
|---------|--------|----------|---------|
| Node (Content types) | Basic fields | Entity references | Custom storage/handlers |
| Block | Static content | Visibility rules | Custom block plugins |
| Views | Basic listings | Relationships | Custom handlers/filters |
| Entity types | Standard entities | Paragraphs | Custom entity types |
| Roles and permissions | 3-4 roles | Workflow integration | Dynamic permissions |
| Services | Dependency injection | Event subscribers | Custom service providers |
| Theme | Sub-theme | Custom components | Design system integration |
| CKEditor | Standard config | Custom plugins | Widget development |
| Migration | CSV import | Database migration | Multi-source aggregation |
| Languages | 2 languages | 3-5 languages | 5+ with RTL |
| Search | Database search | Solr/Elasticsearch | Faceted/custom scoring |
| Forms | Webform config | Multi-step forms | Custom Form API handlers |
| Configuration | Standard export | Split config | Config ignore patterns |
| Development setup | DDEV/Lando | Custom containers | Multi-environment parity |

---

## Deliverable Options

### Automation Tools
- CLI tool for project scanning
- AI skill for estimation conversations
- AI agent for automated analysis
- CI task for ongoing project metrics

---

## Security Audit Checklist

| Area | Checks |
|------|--------|
| Core version | Up-to-date with security releases |
| Contrib modules | Known vulnerabilities scan |
| Custom code | Input sanitization, access checks |
| Permissions | Principle of least privilege |
| Configuration | Secure file permissions, no exposed keys |

---

## Evaluation Framework

### On Real Open Source Projects
1. Select reference projects (Drupal.org, GitHub)
2. Run automated analysis
3. Compare estimates vs actual effort
4. Calibrate multipliers
5. Document variance reasons

---

*This helper extends the main cost estimation skill with advanced parameters and automated analysis capabilities.*
