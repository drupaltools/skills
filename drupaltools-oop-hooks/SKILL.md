---
name: drupaltools-oop-hooks
description: Generate production-grade Drupal 11 OOP code for any Drupal extension point - hooks, plugins, event subscribers, services, form alters, preprocess functions, access checkers, route subscribers, queue workers, block plugins, field formatters, and more. Use this skill whenever the user selects or pastes a Drupal API symbol, hook name, service call, annotation, attribute, event name, or code fragment and asks for an implementation, explanation, or example. Trigger for requests like "generate code for hook_entity_presave", "how do I implement this hook in OOP", "show me the Drupal 11 way to do X", "write a service for this hook", or any time a Drupal hook or extension point is mentioned alongside a request for code.
---

# Drupal 11 OOP Hook & Extension Point Generator

Target audience: experienced Drupal developers. Be technically dense, skip basics.

## Step 1 - Identify the selection

The user will provide a Drupal API symbol, hook name, service call, event name, plugin class, or code fragment. Before generating code:

1. **Ambiguous input** - state the most likely Drupal 11 interpretation first; mention alternatives briefly.
2. **Vague input** - infer the closest API (e.g. `presave` → `hook_entity_presave()`, `form alter` → `hook_form_alter()`).
3. **Non-existent API** - say so clearly; do not invent service IDs or hook names.
4. **Drupal version** - assume Drupal 11 unless the symbol is clearly older or removed; flag deprecated APIs explicitly.

Classify the input as one of:

| Type | Examples |
|------|---------|
| Hook (procedural entry point) | `hook_entity_presave`, `hook_form_alter`, `hook_cron` |
| Alter hook | `hook_theme_alter`, `hook_views_data_alter` |
| Preprocess hook | `hook_preprocess_node`, `hook_preprocess_block` |
| Event subscriber target | `KernelEvents::REQUEST`, `EntityHookEvents::*` |
| Plugin | `BlockBase`, `FieldFormatterBase`, `QueueWorkerBase` |
| Service call / static accessor | `\Drupal::entityTypeManager()`, `\Drupal::messenger()` |
| Other OOP extension point | route subscriber, access checker, param converter, normalizer |

Also state whether the API is: idiomatic in Drupal 11 / legacy-but-valid / deprecated / better replaced.

## Step 2 - Core OOP principle to apply

### For hooks (procedural entry points)
Hooks are procedural by design and remain so in Drupal 11. The correct pattern:

1. Implement the hook in `my_module.module` (or `.install`, `.theme` as required).
2. Keep the hook body to 1–3 lines.
3. Delegate all logic to a service class.
4. Using `\Drupal::service()` inside a hook is acceptable as a bridge.

```php
// my_module.module
function my_module_entity_presave(EntityInterface $entity): void {
  \Drupal::service('my_module.entity_presave_handler')->handle($entity);
}
```

The service class carries the real implementation with constructor injection.

### For non-hook extension points
Generate the canonical OOP class directly - event subscriber, plugin, service, access checker, etc. Do not force a hook where the framework provides a better mechanism.

## Step 3 - Required output structure

Always produce all applicable sections. Skip a section only if genuinely irrelevant; say so in one line.

### A. What this is
One short paragraph: what the selected symbol is, where it fits in Drupal's architecture, and whether it is the preferred Drupal 11 approach.

### B. Drupal 11 recommendation
State the preferred pattern. If a hook, explain the hook-to-service delegation. If an event/plugin/service, explain the OOP class to use.

### C. Minimal working example
The smallest valid implementation. Enough to run, not enough to be production-safe.

### D. Production-grade OOP version
Full implementation with:
- constructor injection (not `\Drupal::*` inside classes)
- typed properties and return types
- `declare(strict_types=1)`
- interfaces in type hints
- realistic conditions (bundle checks, entity type checks, etc.)
- services YAML registration

### E. File structure
Show exact paths. Example:
```
web/modules/custom/my_module/
  my_module.info.yml
  my_module.module
  my_module.services.yml
  src/Hook/EntityPresaveHandler.php
```

### F. Complete file contents
Include every file shown in E, with full contents. No truncation.

### G. How it works
Short prose: execution flow from Drupal's invocation to the service call and return.

### H. When to use / when not to use
Tradeoffs vs alternatives (e.g. hook vs event subscriber, hook vs plugin).

### I. Common Drupal-specific mistakes
Bullet list. Focus on mistakes specific to this API (not generic PHP advice).

### J. Advanced patterns (include when relevant)
Add whichever of these apply:
- **Testing** - unit test for the service, kernel test for Drupal integration
- **Cacheability** - cache tags, contexts, max-age, render array metadata
- **Translation/multilingual** - current language vs untranslated entity, config translation
- **Revisions/moderation** - default vs pending revisions, Content Moderation interaction
- **Performance** - avoid repeated entity loads, static cache, lazy builders
- **Security/access** - access checks, sanitised output, never trust raw form input
- **Deprecation** - flag deprecated APIs; show Drupal 11-safe replacements

## Step 4 - Code quality requirements

Every PHP file must open with:
```php
<?php

declare(strict_types=1);
```

Use:
- typed properties and constructor property promotion where appropriate
- interfaces in all type hints (`EntityTypeManagerInterface`, not `EntityTypeManager`)
- early returns
- `use` statements, not inline fully-qualified names
- namespaces under `Drupal\my_module\...`

Avoid:
- `\Drupal::*` inside injectable classes (except at hook bridge points)
- deprecated APIs without an explicit warning
- invented service IDs or non-existent hooks
- giant hook bodies
- pseudo-code unless labeled as such

## API-specific generation notes

### hook_entity_presave / hook_entity_insert / hook_entity_update
Include: bundle/entity-type checks, translation awareness (`$entity->isTranslatable()`), avoiding infinite resave loops (`$entity->original`), revision notes, Content Moderation implications.

### hook_form_alter / hook_form_FORM_ID_alter
Include: when `FORM_ID` variant is better than generic alter, submit handler injection pattern, AJAX caveats, validation ordering, `#attached` for libraries.

### hook_preprocess_node / hook_preprocess_*
Include: `$variables` array handling, cache metadata (`CacheableMetadata`), why heavy logic does not belong here, alternative with view builders or field formatters.

### hook_cron
Include: why Queue API is usually preferable, lock acquisition with `LockBackendInterface`, idempotency, state storage with `StateInterface`.

### hook_theme
Include: Twig template registration, render array `#theme` linkage, template suggestions.

### hook_page_attachments
Include: library attachment pattern, cache contexts/tags, route-conditional attachment.

### Event subscribers (KernelEvents::*, EntityHookEvents::*)
Do not use a hook. Generate: subscriber class, `getSubscribedEvents()`, service YAML with `event_subscriber` tag, priority example, request-scope caveats.

### Plugin classes (BlockBase, FieldFormatterBase, QueueWorkerBase, etc.)
Generate: full plugin class with PHP 8 attribute annotation, `ContainerFactoryPluginInterface` when services needed, `build()` / `viewElements()` / `processItem()` as applicable, cache metadata.

### Static service accessors (\Drupal::entityTypeManager(), etc.)
Show: why this is not preferred in injectable classes, equivalent constructor injection, before/after comparison, exceptions (hooks, static factory methods).

## YAML templates

### services YAML
```yaml
services:
  my_module.some_handler:
    class: Drupal\my_module\SomeHandler
    arguments:
      - '@entity_type.manager'
      - '@logger.factory'
```

### event subscriber tag
```yaml
  my_module.some_subscriber:
    class: Drupal\my_module\EventSubscriber\SomeSubscriber
    tags:
      - { name: event_subscriber }
```

### plugin (queue worker example)
```yaml
# No YAML needed - discovered via PHP attribute annotation.
```

## Fallback behaviour

If the input is too vague:
1. State the most likely interpretation.
2. Generate the closest Drupal 11 OOP pattern for it.
3. Note alternative interpretations in two lines.
4. Never refuse - always return a useful example.