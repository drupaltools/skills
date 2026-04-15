---
name: drupaltools-issue-generate
description: >
  Create a Drupal.org issue title and summary body that is ready to paste into
  the issue form. Use when the user asks to draft, improve, or rewrite an issue
  from a bug report, feature request, patch, MR, commit, or discussion.
  When the user says "issue title", "issue body", "issue summary", or similar.
---

## About

Produce a single fenced Markdown code block containing a Drupal.org issue title
and summary body. The output can be pasted directly into the
[Drupal.org issue form](https://www.drupal.org/docs/develop/issues/fields-and-other-parts-of-an-issue/issue-summary-field).

## Input contract

Extract the following facts from the user prompt and nearby file context:

| Fact                  | Source                                          |
|-----------------------|-------------------------------------------------|
| What is broken/missing| User description, stack trace, error log        |
| Affected project      | `composer.json`, `.info.yml`, user statement    |
| Current behavior      | Reproduction steps, bug description             |
| Expected behavior     | User statement, spec, comparable working case   |
| Related links         | Issue URL, MR, commit hash, patch, discussion   |

If the core problem or affected module cannot be determined, ask **one** short
clarifying question before drafting.

## Output contract

Return **exactly one** fenced `md` code block. No prose before or after the
block. Use this exact structure:

```md
Title: <short, specific, action-oriented title>
Description:
<h3 id="problem-motivation">Problem/Motivation</h3>
[1-3 sentences: what is wrong, who is affected, why it matters. Include brief reproduction steps if known.]

<h3 id="proposed-resolution">Proposed resolution</h3>
[1-3 sentences: what should change, in plain language. Reference specific functions, hooks, or config if known.]

<h3 id="remaining-tasks">Remaining tasks</h3>
- [ ] TASK 1
- [ ] TASK 2

<h3 id="user-interface-changes">User interface changes</h3>
[brief UI impact or `n/a`]

<h3 id="api-changes">API changes</h3>
[API impact or `n/a`]

<h3 id="data-model-changes">Data model changes</h3>
[schema/config/content model impact or `n/a`]
```

## Writing rules

### Title
- Start with a verb: `Fix`, `Add`, `Remove`, `Update`, `Allow`, `Prevent`
- Keep under 80 characters
- Include the affected component: `Fix views_handler_field fatal when…`
- Avoid vague words like `Issue with`, `Problem in`

### Problem/Motivation
- State the error or gap in the first sentence
- Mention who is affected (site builder, developer, end user)
- Include reproduction steps when known
- Reference error messages, log entries, or stack traces if provided
- Do not speculate about root causes beyond available evidence

### Proposed resolution
- Describe the fix in concrete terms
- Name specific functions, services, or config keys when known
- Prefer minimal, targeted changes over broad refactors
- If a patch exists, reference it by filename or interdiff

### Remaining tasks
- List actionable, verifiable steps
- Include test updates when the fix changes behavior
- Use `n/a` only when no follow-up work is needed beyond the patch itself

### Impact sections (UI, API, data model)
- Use `n/a` exactly when there is no impact
- For API changes, name the specific function, hook, event, or service
- For data model changes, name the specific entity type, field, or config key
- Keep to one sentence

### General
- Preserve module, theme, and project names exactly as provided
- No extra sections unless explicitly requested
- No screenshots or images
- No filler language or hedging
- Short paragraphs over bullet lists where possible
- Drupal 9/10/11 compatibility note only when the issue spans versions

## Common anti-patterns to avoid

| Anti-pattern                          | Instead                                   |
|---------------------------------------|-------------------------------------------|
| "This PR fixes…" or "The patch does…" | Describe the change directly              |
| Vague titles like "Bug in views"      | "Fix views_query_alter double-encoding"   |
| Long stack traces in Problem section   | Summarize error, link to full trace       |
| Speculative root cause statements     | State observed behavior only              |
| Blank impact sections                 | Write `n/a` or a one-sentence answer      |
| Multiple issues in one draft          | Split into separate issue drafts          |

## Example output

```md
Title: Fix token browser fatal when field label is empty
Description:
<h3 id="problem-motivation">Problem/Motivation</h3>
When a site builder opens the token browser on an entity field with an empty label, the page triggers a fatal error. This blocks token discovery in common editorial workflows. Reproduction: enable the module, create a field without a label, then open the token browser for that entity type.

<h3 id="proposed-resolution">Proposed resolution</h3>
Add a defensive fallback in `TokenBrowserController::buildFieldTokens()` for empty labels. Use the field machine name as a safe default when `getFieldDefinition()->getLabel()` returns an empty string.

<h3 id="remaining-tasks">Remaining tasks</h3>
- [ ] Add kernel test for empty-label field in token browser
- [ ] Verify output for entity types with unlabeled fields

<h3 id="user-interface-changes">User interface changes</h3>
Token labels show the machine name fallback instead of triggering an error.

<h3 id="api-changes">API changes</h3>
n/a

<h3 id="data-model-changes">Data model changes</h3>
n/a
```

## Extra resources

- Drupal.org issue summary guidance: https://www.drupal.org/docs/develop/issues/fields-and-other-parts-of-an-issue/issue-summary-field

## Similar skills
- [drupalorg-issue-writer](https://github.com/balintbrews/drupal-canvas-dev/tree/main/agents/canvas/skills/drupalorg-issue-writer)
- [drupalorg-issue-summary-update](https://github.com/mglaman/drupalorg-cli/blob/main/skills/drupalorg-issue-summary-update/SKILL.md)
- [drupalorg-issue-helper](https://github.com/kanopi/cms-cultivator/blob/main/skills/drupalorg-issue-helper/SKILL.md)
- [drupal-issue](https://github.com/abderrahimghazali/drupal-issue-md-skills)
