# drupaltools-skills

A collection of AI Skills for Drupal development.

## Install

Install individual skills with [npx skills](https://skills.sh):

```bash
npx skills add https://github.com/drupaltools/skills
```

Or install all at once by cloning this repo into your skills directory:

```bash
# Claude Code
git clone https://github.com/drupaltools/skills.git ~/.claude/skills/drupaltools-skills

# Agents that use ~/.agents/skills
git clone https://github.com/drupaltools/skills.git ~/.agents/skills/drupaltools-skills
```

## Skills

| Skill | Description |
|---|---|
| `drupaltools-checklist-development` | Guide teams through Drupal project development checklists |
| `drupaltools-coding-standards` | Check Drupal PHP code with PHPCS and PHPStan |
| `drupaltools-site-audit` | Generate Drupal site audit reports for RFPs and proposals |
| `drupaltools-contrib-gitlab-ci` | Generate GitLab CI for Drupal modules |
| `drupaltools-contrib-readme` | Generate and validate Drupal module README files |
| `drupaltools-contrib-validator` | Validate modules for Drupal.org contribution readiness |
| `drupaltools-developer-setup` | Optimize Drupal developer machine setup and tooling |
| `drupaltools-best-practices` | Audit code against Drupal best practices |
| `drupaltools-code-search` | Search Drupal contrib module source code via GitLab API |
| `drupaltools-contrib-lookup` | Find the online source URL for a contrib code snippet |
| `drupaltools-git-blame` | Generate a git.drupalcode.org blame URL and fetch commit details for a contrib code snippet |
| `drupaltools-cost-estimation` | Estimate costs and timeline for Drupal projects |
| `drupaltools-module-clone` | Clone a module as a structural scaffold with renamed machine name |
| `drupaltools-module-info` | Identify which module owns a file or code snippet |
| `drupaltools-maintenance-contract` | Drupal maintenance and support contract templates |
| `drupaltools-migration-plan` | Guide for planning Drupal site migrations and upgrades |
| `drupaltools-module-rename` | Rename a module's machine name throughout its codebase |
| `drupaltools-onboarding` | Step-by-step onboarding checklist for Drupal newcomers |
| `drupaltools-oop-hooks` | Generate Drupal 11 OOP code for hooks, plugins, and events |
| `drupaltools-optimize` | Optimize Drupal PHP code for the current Drupal/PHP version |
| `drupaltools-patch` | Apply patches to contrib modules from any source |
| `drupaltools-postmortem` | Generate post-mortem reports for Drupal projects |
| `drupaltools-site-clone` | Clone a Drupal project as a clean starter template |
| `drupaltools-tip-generator` | Show or generate a random Drupal tip |
| `drupaltools-translations` | Guide for Drupal multilingual and translation workflows |

## Agents

| Agent | Description |
|---|---|
| `drupal-backend-dev` | Backend development tasks including custom modules, services, plugins, and API integrations |
| `drupal-code-archaeologist` | Analyze legacy Drupal codebases for upgrade preparation and migration planning |
| `drupal-content-architect` | Design content models, configure entity relationships, and build editorial experiences |
| `drupal-core-contributor` | Work on Drupal core contributions, patches, and merge requests |
| `drupal-devops-engineer` | Design, deploy, and maintain Drupal hosting infrastructure with automation |
| `drupal-documentation-expert` | Create technical documentation, user guides, API specs, and architecture diagrams |
| `drupal-frontend-dev` | Frontend development tasks including theming, SDC components, and Twig templates |
| `drupal-performance-engineer` | Diagnose and resolve Drupal performance issues with data-driven solutions |
| `drupal-security-engineer` | Audit code for security vulnerabilities and implement hardening measures |
| `drupal-tech-lead` | Expert Drupal technical leadership for architecture decisions, team coordination, and project governance |

## Collections of Drupal skills

- [skills.sh - Search for Drupal](https://skills.sh/trending?q=drupal) - Skill aggregator, search for Drupal skills
- [skillsmp.com - Search for Drupal](https://skillsmp.com/search?q=drupal) - Skill aggregator, search for Drupal skills

## Similar tools

- [AI Skills](https://www.drupal.org/project/ai_skills) - Drupal module providing AI skills
- [claude-code-skill-factory](https://github.com/alirezarezvani/claude-code-skill-factory) - Skill factory for Claude Code
- [claude-skills/php-pro](https://github.com/Jeffallan/claude-skills/tree/main/skills/php-pro) - PHP Pro skill
- [claude-toolbox](https://github.com/kanopi/claude-toolbox) - Kanopi's Claude toolbox
- [claude_code_skills_drupal](https://github.com/askibinski/claude_code_skills_drupal) - Drupal skills for Claude Code
- [cms-cultivator](https://github.com/kanopi/cms-cultivator/tree/main/skills) - Kanopi's CMS skill collection
- [cursorrules](https://github.com/ivangrynenko/cursorrules) - Cursor rules for Drupal
- [Drupal DDEV Setup](https://github.com/jamieaa64/Drupal-DDEV-Setup-Claude-Skill) - DDEV setup skill
- [drupal-agent-resources](https://github.com/madsnorgaard/drupal-agent-resources) - Drupal agent resources
- [drupal-claude-code-sub-agent-collective](https://github.com/gkastanis/drupal-claude-code-sub-agent-collective/tree/main/templates/skills) - Sub-agent collective with Drupal skill templates
- [drupal-claude-skills](https://github.com/grasmash/drupal-claude-skills) - Grasmash's Drupal Claude skills
- [drupal-issue-queue](https://github.com/scottfalconer/drupal-issue-queue) - Drupal issue queue skill
- [drupal-skill](https://github.com/Omedia/drupal-skill) - Omedia's Drupal skill
- [drupal-workflow](https://github.com/gkastanis/drupal-workflow) - Drupal AI workflow resources
- [drupaldev-claude-skill](https://github.com/nonzod/drupaldev-claude-skill) - Drupal dev skill for Claude
- [drupalorg-cli](https://github.com/mglaman/drupalorg-cli/tree/main/skills) - Skills for the drupalorg CLI
- [lakedrops skills](https://gitlab.lakedrops.com/ai/skills) - Lakedrops Drupal skills
- [Surge](https://www.drupal.org/project/surge) - Drupal module with AI-assisted development tools
- [waap-drupal](https://github.com/proofoftom/waap-drupal/tree/main/.claude/skills) - WAAP Drupal skills

## Plan

> Some proposals for new Skills or Agents to add.

- drupaltools-tdd: PHPUnit kernel/functional/unit tests for Drupal
- drupaltools-upgrade: Drupal 9→10→11 upgrade patterns
- drupaltools-accessibility: WCAG 2.2 AA compliance for forms/components
- drupaltools-performance: xhprof, webprofiler, query optimization

## License

[GPL v2](LICENSE) 2026
