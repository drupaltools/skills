# drupaltools-skills

A collection of Claude Code skills for Drupal development.

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
| `drupaltools-contrib-validator` | Validate modules for Drupal.org contribution readiness |
| `drupaltools-module-clone` | Clone a module as a structural scaffold with renamed machine name |
| `drupaltools-module-info` | Identify which module owns a file or code snippet |
| `drupaltools-oop-hooks` | Generate Drupal 11 OOP code for hooks, plugins, and events |
| `drupaltools-optimize` | Optimize Drupal PHP code for the current Drupal/PHP version |
| `drupaltools-patch` | Apply patches to contrib modules from any source |
| `drupaltools-postmortem` | Generate post-mortem reports for Drupal projects |
| `drupaltools-site-clone` | Clone a Drupal project as a clean starter template |
| `drupaltools-tip-generator` | Show a random Drupal tip of the day |
