# drupaltools-skills

A collection of AI Skills for Drupal development.

## Install

Install individual skills with [npx skills](https://github.com/nicokosi/skills):

```bash
npx skills add https://github.com/nicokosi/skills --skill drupaltools-best-practices
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
| `drupaltools-best-practices` | Audit code against Drupal best practices |
| `drupaltools-code-search` | Search Drupal contrib module source code via GitLab API |
| `drupaltools-contrib-lookup` | Find the online source URL for a contrib code snippet |
| `drupaltools-git-blame` | Generate a git.drupalcode.org blame URL and fetch commit details for a contrib code snippet |
| `drupaltools-contrib-validator` | Validate modules for Drupal.org contribution readiness |
| `drupaltools-module-clone` | Clone a module as a structural scaffold with renamed machine name |
| `drupaltools-module-info` | Identify which module owns a file or code snippet |
| `drupaltools-oop-hooks` | Generate Drupal 11 OOP code for hooks, plugins, and events |
| `drupaltools-optimize` | Optimize Drupal PHP code for the current Drupal/PHP version |
| `drupaltools-patch` | Apply patches to contrib modules from any source |
| `drupaltools-postmortem` | Generate post-mortem reports for Drupal projects |
| `drupaltools-site-clone` | Clone a Drupal project as a clean starter template |
| `drupaltools-tip-generator` | Show or generate a random Drupal tip |

## Similar tools

- [skills.sh - Search for Drupal](https://skills.sh/trending?q=drupal) - Skill aggregator, search for Drupal skills
- [AI Skills](https://www.drupal.org/project/ai_skills) - Drupal module providing AI skills
- [claude-code-skill-factory](https://github.com/alirezarezvani/claude-code-skill-factory) - Skill factory for Claude Code
- [claude-skills/php-pro](https://github.com/Jeffallan/claude-skills/tree/main/skills/php-pro) - PHP Pro skill
- [claude_code_skills_drupal](https://github.com/askibinski/claude_code_skills_drupal) - Drupal skills for Claude Code
- [claude-toolbox](https://github.com/kanopi/claude-toolbox) - Kanopi's Claude toolbox
- [cms-cultivator](https://github.com/kanopi/cms-cultivator/tree/main/skills) - Kanopi's CMS skill collection
- [cursorrules](https://github.com/ivangrynenko/cursorrules) - Cursor rules for Drupal
- [Drupal DDEV Setup](https://github.com/jamieaa64/Drupal-DDEV-Setup-Claude-Skill) - DDEV setup skill
- [drupal-agent-resources](https://github.com/madsnorgaard/drupal-agent-resources) - Drupal agent resources
- [drupal-claude-code-sub-agent-collective](https://github.com/gkastanis/drupal-claude-code-sub-agent-collective/tree/main/templates/skills) - Sub-agent collective with Drupal skill templates
- [drupal-claude-skills](https://github.com/grasmash/drupal-claude-skills) - Grasmash's Drupal Claude skills
- [drupal-issue-queue](https://github.com/scottfalconer/drupal-issue-queue) - Drupal issue queue skill
- [drupal-skill](https://github.com/Omedia/drupal-skill) - Omedia's Drupal skill
- [drupaldev-claude-skill](https://github.com/nonzod/drupaldev-claude-skill) - Drupal dev skill for Claude
- [drupalorg-cli](https://github.com/mglaman/drupalorg-cli/tree/main/skills) - Skills for the drupalorg CLI
- [Surge](https://www.drupal.org/project/surge) - Drupal module with AI-assisted development tools
- [waap-drupal](https://github.com/proofoftom/waap-drupal/tree/main/.claude/skills) - WAAP Drupal skills

## License

[GPL v2](LICENSE) 2026
