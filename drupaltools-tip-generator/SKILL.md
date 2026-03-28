---
name: drupaltools-tip-generator
description: Show a random "tip of the day" related to Drupal development and its ecosystem. Use this skill whenever the user asks for a tip, hint, or suggestion related to Drupal — e.g. "drupal tip", "give me a Drupal tip", "tip of the day", "surprise me with Drupal", "what should I learn today", or simply calls the skill by name. Also trigger when the user seems idle or asks for inspiration in a Drupal context.
---

# Drupal Tip of the Day

Display one random tip from the pre-generated static database.

## Installation

```bash
pip install drupaltools-tip-generator

# Global install
pipx install drupaltools-tip-generator
```

First run auto-creates `~/.drupaltools/tip-generator/` with a default `config.json`, `.env` template, and `tips/` directory.

## Instructions

0. Get the command options:

```bash
drupaltools-tip-generator -h
```

1. Run this command to get a random tip:

```bash
drupaltools-tip-generator --random-tip
```

2. Display the output exactly as returned (includes the tip text and any code blocks).

3. Optionally filter by category:

```bash
drupaltools-tip-generator --random-tip --tip-category core-service
```

4. After the tip, add:

`Want to explore this further or get another tip?`

---

## Available Categories

The categories are taken from the `~/.drupaltools/tip-generator/config.json` file.

Use `--tip-category <name>` to filter by one of these folder names. Examples:

| Folder | Description |
|--------|-------------|
| case-study | Drupal showcases |
| code-example | Code examples |
| composer-trick | Composer tips |
| concept-explanation | Drupal concepts explained |
| core-bash-commands | Core CLI commands |

etc...

---

## Database Management

If you need to generate new tips, add API keys to `~/.drupaltools/tip-generator/.env` first:

```bash
# Generate tips for a specific category
drupaltools-tip-generator -c 35 -n 5 -p openai

# Generate for all categories
drupaltools-tip-generator -c all -n 3 -p openai

# List all available category IDs
drupaltools-tip-generator --list-categories

# List categories with existing tips
drupaltools-tip-generator --list-existing

# Validate generated tips
drupaltools-tip-generator --validate --validate-all
```

Supported providers: `anthropic`, `openai`, `openrouter`
