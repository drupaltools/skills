---
name: drupaltools-code-review
description: Review and score Drupal code across security, correctness, efficiency, complexity, duplication, testing, and documentation, producing a weighted score and a merge verdict. Use this skill whenever the user wants Drupal code reviewed, scored, or checked before merging — including custom modules, themes, plugins, services, Twig templates, config YAML, patches, and merge requests. Trigger for requests like "review this module", "code review this", "score this code", "is this ready to merge", "check this MR/patch", "review my changes before I commit", "what's wrong with this code", or "give me a second opinion on this code". Also trigger when reviewing code that you or another agent just wrote, and when auditing a Drupal.org contribution before submitting it.
---

# Drupal Code Review

Review Drupal code against seven dimensions, score it, and return a merge verdict.

This skill covers **code-level** review. For whole-site health (content model, hosting, module inventory) use `drupaltools-site-audit`. For an RFP/proposal technical report use `drupaltools-site-audit` as well.

## The one rule

**Review is read-only.** Do not edit the code under review. Report each finding with the fix as a snippet, and apply changes only when the user explicitly asks. A review that silently rewrites the code destroys the evidence and hides the problem from the author.

## Step 0 — Establish scope

Determine, and state at the top of the report:

| Question | How to resolve |
|---|---|
| **What is under review?** | A path from the user, pasted code, `git diff`, a patch file, or an MR diff. If nothing was given, ask — do not guess. |
| **Target version** | Drupal and PHP version. Check `composer.json`, `.info.yml` (`core_version_requirement`), or ask. Default assumption: Drupal 10/11, PHP 8.1+. Version changes which APIs are deprecated, so do not skip this. |
| **Custom or contrib?** | Custom code is reviewed against Drupal standards. Contrib code is also reviewed against [Drupal.org contribution requirements](https://www.drupal.org/docs/develop/contributing-code) — see `drupaltools-contrib-validator`. |
| **Scope of change** | For a diff, review the changed files *and* the code they call. A changed function whose contract is now violated elsewhere is a finding. |
| **Is this code you just wrote?** | If yes, stop and dispatch the `drupal-code-reviewer` agent instead. An author cannot objectively review their own work; a fresh context has no memory of the intentions behind the code. |

Detect the input type and check only the dimensions that apply:

| Input | Dimensions to check |
|---|---|
| Custom module (PHP) | All seven |
| Twig template | Security (XSS), Coding errors, Efficiency, Simplify, Duplication, Documentation |
| Config YAML | Security (access), Coding errors (schema, deps), Duplication, Documentation |
| `*.install` / update hooks | Coding errors (idempotency), Efficiency, Documentation |
| Patch / MR diff | All applicable to the changed lines + their callers |
| Test files | Testing coverage, Documentation, Duplication |

## Step 1 — Run the tooling gate first

Automated tools find style and type noise far more cheaply than reading. **Run them before reading a single line by hand**, so auto-fixable issues never consume review attention.

```bash
# Is tooling available?
vendor/bin/phpcs --version 2>/dev/null && echo "phpcs_available"
vendor/bin/phpstan --version 2>/dev/null && echo "phpstan_available"
test -f vendor/bin/phpunit && echo "phpunit_available"
```

Run them via DDEV when the project uses it (`ddev exec vendor/bin/phpcs ...`).

- **PHPCS** (`--standard=Drupal,DrupalPractice`) → delegate to `drupaltools-coding-standards` or `drupaltools-phpcs`.
- **PHPCBF** — report that auto-fixes are available. Do **not** run it as part of the review; offer it.
- **PHPStan** → delegate to `drupaltools-phpstan`.
- **PHPUnit** → delegate to `drupaltools-phpunit`. A failing suite is a Blocker.

Record in the report what ran and what did not. **Never imply a tool passed when it was not available** — an unrun check is unverified, not clean. If tooling is missing, say so and continue with manual review. Do not install tools into the user's project unasked.

## Step 2 — Review the seven dimensions

Score anchors, used for every dimension:

| Score | Meaning |
|---|---|
| 9–10 | Exemplary. Nothing to report. |
| 7–8 | Minor findings only. |
| 5–6 | Several Minor findings, or one Major. |
| 3–4 | More than one Major, or pervasive Minor issues. |
| 1–2 | A Blocker is present, or the problem is systemic. |
| 0 | The dimension is entirely absent (e.g. no tests exist at all). |

### A. Security issues — weight 25

Security is the blocking dimension. Any confirmed vulnerability is a **Blocker** and limits the total score to 49 (see Step 3).

**SQL injection**
- String-concatenated or interpolated queries: `$connection->query("... WHERE nid = $nid")`, `db_query("... $var")`.
- Fix: placeholders. `$connection->query('... WHERE nid = :nid', [':nid' => $nid]);`
- `LIKE` with unescaped wildcards, `ORDER BY` built from user input, identifiers interpolated instead of validated against an allowlist.

**XSS**
- `|raw` in Twig on user-supplied data; `{{ include(user_input) }}` (SSTI).
- `#markup` containing user input; `Markup::create()` on unsanitized strings; `drupalSettings` carrying raw HTML.
- Fix: rely on Twig autoescape, or `Xss::filter()` / `Xss::filterAdmin()` / `Html::escape()` / `#plain_text`.

**Access control**
- Routes without `requirements:`, or with `_access: 'TRUE'` on a sensitive route.
- `_role` used where `_permission` is correct; permission reused from another module instead of defined in `*.permissions.yml`.
- Controllers returning entity data without `->access('view', $account)`.
- Entity queries missing the `accessCheck()` call.
- `#access` absent on privileged form elements (disabling a field in the UI is not access control).
- `AccessResult` returned without `addCacheableDependency()`.
- Permission enforced only in the theme layer.
- Mutating routes reachable by `GET` without CSRF protection.

**CSRF**
- Custom POST handling that bypasses the Form API (and therefore the form token).
- REST/JSON:API write endpoints missing `_csrf_request_header_token`.

**Secrets and configuration**
- Credentials, API keys, or tokens in code, in `drupalSettings`, or committed in `settings.php`.
- Secrets in exported config.
- `$settings['trusted_host_patterns']` missing on a production site.
- Sensitive config not excluded from `drush cex`.

**File handling**
- `managed_file` / upload fields without `FileExtension` or `FileMimeType` validators.
- Sensitive uploads on the public scheme; filename used unsanitized in a path.
- `#type => 'file'` handling user-controlled destinations.

**Injection-adjacent**
- `unserialize()` on request data, `eval()`, `exec()`/`shell_exec()` with input, `include` on a dynamic path.

### B. Coding errors — weight 20

**Deprecated and removed APIs** — check against the target Drupal version. Frequent offenders:
- `db_query()`, `db_select()`, `db_insert()`, `db_update()`, `db_delete()` — use an injected `Connection`.
- `drupal_set_message()`, `l()`, `format_date()`, `file_load()`, `node_load()`, `entity_load()`, `arg()`, `drupal_render()`, `\Drupal::entityManager()`.
- Plugin annotations (`@Block`, `@FieldType`) — use PHP attributes (`#[Block(...)]`) on Drupal 10.2+.
- Procedural hooks — use `#[Hook]` classes in `src/Hook/` on Drupal 11.1+, and set `hooks_converted: true` in `.info.yml` once all hooks are converted.

**Type and signature errors**
- Signature incompatible with the parent method (LSP violation), missing return type, wrong nullable usage, missing return path.
- `@param`/`@return` docblock types disagreeing with the actual signature.
- Direct property access on a field that may not exist (`$entity->get('field_x')->value` without a `->hasField()` guard).

**Render and cache defects**
- Render arrays missing `#cache` tags/contexts → stale or wrongly-shared output. This is a correctness bug, not a performance nit.
- `#markup` where `#plain_text` or a renderable `#type` is correct.
- `#attached` placed below the element it should bubble from.

**Configuration and schema**
- Config read/written with no matching `config/schema/*.schema.yml` entry.
- Hardcoded UUIDs or config names baked into code.
- `core_version_requirement` missing or wrong in `.info.yml`; wrong dependency keys.

**Services and DI**
- Service definitions missing `arguments:` for constructor dependencies.
- `\Drupal::service()` in a class that could accept the dependency.

**Translation**
- `t()` called as a global in a class (use `$this->t()` or `StringTranslationTrait`).
- Placeholder misuse: `@var` (no escaping), `%var` (escaped), `:url` (URL-only). Using `@` for a value later rendered as HTML.
- `t()` wrapping a dynamic or user-supplied string.

**Update path**
- Schema or data change with no `hook_update_N()` or `hook_post_update_NAME()`.
- Non-idempotent update hook.
- Update hook without a docblock explaining what it does.

### C. Code efficiency — weight 15

**Queries**
- `getStorage()->load()` inside a `foreach` — the classic N+1. Fix: `loadMultiple()`, `loadByProperties()`, or `EntityQuery`.
- Any query inside a loop, a `hook_entity_view`, a preprocess function, or a block's `build()`.
- Unbounded result sets: no `range()`, no pager.
- Loading whole entities when only one field value is needed.
- Custom tables in `hook_schema()` without `indexes:` on the queried columns.

**Caching**
- Expensive computation with no local/static cache.
- `#cache` `max-age` of `0` on content that is not user-specific.
- Missing `addCacheableDependency()` for config or entity dependencies.
- Over-broad cache tags (invalidating a whole bin on every save); `user` context where `user.roles` suffices.
- `cache.backend.*` misuse, or a cache write on every request.

**Views and rendering**
- Views without pagination or with an unbounded result.
- `views_embed_view()` in a loop.
- Heavy logic in Twig templates; deeply nested loops in a template.
- A library attached per render rather than declared once.
- Unbundled/aggregation-hostile assets; a CDN where a local copy is faster.

**Background work**
- `hook_cron` doing unbounded work synchronously — should be queued.
- Blocking HTTP calls on a page render path.

**Bootstrap cost**
- `\Drupal::` static calls that force a full bootstrap where DI would allow a lazily-wired service.

### D. Simplify complex code — weight 12

- Functions longer than ~40 lines, nesting deeper than three levels, or branching that can be flattened by an early return.
- `\Drupal::` static calls inside service classes — the single most common Drupal-specific complexity smell. Use constructor injection.
- God classes and classes with more than one reason to change.
- Controllers holding business logic — it belongs in a service.
- Hook implementations containing logic — the hook should be thin and delegate.
- `switch`/`if-else` chains dispatching on bundle, entity type, or plugin id — these want a plugin, a tagged service, or a map.
- Mysterious names, unexplained abbreviations, and boolean traps (`doThing(TRUE, FALSE)`).
- Comments explaining *what* the code does instead of *why*; commented-out code left behind.
- Premature abstraction: an interface with one implementation, a config option nobody sets, speculative generality.
- Feature logic living in a shared or generic module.
- **A refactor that relocates complexity instead of removing it is not a simplification.** Count the concepts a reader must hold; prefer the change that makes a branch disappear.

### E. Duplicate code — weight 10

- Copy-pasted hook bodies or controller actions across modules.
- Near-duplicate helper functions — extract the third time, not the first.
- Repeated query or cache-metadata building — move to a repository or service method.
- Duplicated permission, route, or service definitions.
- Duplicated config schema across bundles.
- Duplicated logic that a contrib module already provides — check `drupaltools-code-search` and `drupaltools-contrib-search` before accepting a bespoke implementation.

A near-duplicate of a canonical helper in the same codebase is a Major finding, not a Nit — it is how two implementations of one rule drift apart.

### F. Testing coverage — weight 10

- **Existence** — are there tests for the changed logic? Untested new logic scores this dimension at 0–3.
- **Correct type** — `Unit` (no bootstrap, no DB), `Kernel` (services, entities, needs DB), `Functional` / `FunctionalJavascript` (UI), `ExistingSite` (against a real site). Using `Functional` for pure logic is a Major finding.
- **Behavior, not implementation** — tests asserting private internals or exact method-call order are brittle; they break on a safe refactor.
- **Edge cases** — empty, null, boundary, permission-denied, and exception paths. A suite that only walks the happy path is a Major finding.
- **Security-relevant paths** — access control callbacks, form validation, and sanitization must have tests. These are exactly the paths where a regression is a vulnerability.
- **Regression test** — a bug fix without a test that fails before and passes after is a Major finding.
- **Annotations** — `@covers`, `@group`, and data providers used appropriately.
- **Testability** — code untestable because of `\Drupal::` statics or hard-coded dependencies is itself a finding; fix the code, not the test.
- **Assertion quality** — deprecated `assertEqual()` instead of `assertEquals()`, meaningless assertions (`assertTrue(TRUE)`), or assertions that cannot fail.
- **Independence** — no ordering dependency, no leaked global state, temp files cleaned up.
- **Never acceptable**: weakening, skipping, or deleting an assertion to make a suite pass.

### G. Documentation — weight 8

- File-level docblock on every PHP file.
- Class docblock stating purpose, plus `@ingroup` or a reference link where the convention applies.
- Method docblocks: one-line imperative summary, then `@param`, `@return`, and `@throws` where they apply.
- Property docblocks including `@var` with the type — required by Drupal coding standards.
- Hook implementations documented with what the hook does and a link to the hook's API page.
- `hook_update_N()` / `hook_post_update_NAME()` with a comment explaining what changes and why.
- `README.md` with install, configuration, and usage; `CHANGELOG.md` for contributed modules.
- Inline comments for the *why* behind anything surprising — a workaround, a core bug, an unusual query.
- Config schema entries with meaningful `label` and `description`.
- `@todo` items tied to an issue link rather than floating.
- Docblock types that match the code they describe — a wrong docblock is worse than none, because it is trusted.

## Step 3 — Score

Score each dimension 0–10 using the anchors in Step 2, then apply the weights:

| Dimension | Weight | Score (0–10) | Weighted |
|---|---|---|---|
| Security issues | 25 | | |
| Coding errors | 20 | | |
| Code efficiency | 15 | | |
| Simplify complex code | 12 | | |
| Duplicate code | 10 | | |
| Testing coverage | 10 | | |
| Documentation | 8 | | |
| **Total** | **100** | | |

`Weighted = Score ÷ 10 × Weight`. Total is the sum of weighted values, rounded.

**Blocker cap.** If any Blocker finding exists, the total is capped at 49 and the verdict is FAIL — no matter how good the other dimensions are. A security vulnerability or a data-loss bug cannot be averaged away by clean documentation.

**Verdict:**

| Verdict | Condition |
|---|---|
| **PASS** | Total ≥ 85, and no Blocker or Major findings |
| **PASS WITH FIXES** | Total ≥ 70, and no Blocker findings |
| **CHANGES REQUESTED** | Total 50–69, and no Blocker findings |
| **FAIL** | Any Blocker finding, or total < 50 |

## Step 4 — Report

Use this structure. Keep every finding specific enough that the author can act without asking a follow-up question.

````markdown
## Drupal Code Review: <target>

**Scope:** <paths / diff range> · **Drupal:** <version> · **PHP:** <version> · **Code:** custom | contrib
**Tooling run:** PHPCS <n errors/n warnings> · PHPStan <n errors> · PHPUnit <pass/fail/not run>

### Score

| Dimension | Weight | Score | Weighted | Summary |
|---|---|---|---|---|
| Security issues | 25 | 8 | 20.0 | No injection or access gaps |
| Coding errors | 20 | 6 | 12.0 | Two deprecated API calls |
| Code efficiency | 15 | 5 | 7.5 | N+1 query in the listing builder |
| Simplify complex code | 12 | 7 | 8.4 | |
| Duplicate code | 10 | 6 | 6.0 | Validation repeated in two forms |
| Testing coverage | 10 | 4 | 4.0 | No Kernel test for the new service |
| Documentation | 8 | 9 | 7.2 | |
| **Total** | **100** | | **65.1** | |

### Verdict: CHANGES REQUESTED — 65/100

### Findings

#### Blocker
None.

#### Major
**1. N+1 query in the term listing** — `src/Service/TermListing.php:84`
`$storage->load()` is called inside the `foreach`, issuing one query per term.
*Why it matters:* ~200 extra queries on a 200-term vocabulary.
*Fix:*
```php
$terms = $this->termStorage->loadMultiple($tids);
```

#### Minor
**2. Deprecated `drupal_set_message()`** — `my_module.module:32`
Removed in Drupal 10. Use the messenger service.

#### Nit
**3. Line exceeds 80 characters** — `src/Form/SettingsForm.php:112` (PHPCS)

### Confirmed good practices
- Access control on the export route is enforced with a module-specific permission, not a reused one.
- Every render array in the block plugin carries `#cache` tags and contexts.

### Verification story
- PHPCS ran clean after PHPCBF (not applied).
- PHPStan: 3 errors, all pre-existing.
- PHPUnit: not run — no test suite in this project.
- Manual: reviewed the changed files and their direct callers.

### Recommended next steps
1. <highest-value fix>
2. <second>
````

**Empty sections say "None." — never omit them.** A reader must be able to tell "nothing found" apart from "not checked".

## Honesty rules

Review is where sycophancy does the most damage. These override any instinct to be agreeable.

- **No rubber-stamping.** "LGTM" without evidence is a failed review. If you did not read it, do not approve it.
- **Never soften a real defect.** Do not present a Blocker as a "consider" because the author explained their intent. Verdicts describe the code, not the effort.
- **Do not inflate nits into findings.** A long list of trivia buries the one structural problem that mattered. One architectural finding and ten style nits means the architectural finding *is* the review.
- **Do not comment on code you did not read.** Partial review is fine — say which parts were not reviewed.
- **Quantify where possible.** "This adds ~50ms per item" beats "this could be slow".
- **Lead with what is right.** Naming a genuine strength calibrates the author's trust in the rest of the report.
- **Score honestly.** A dimension with a Blocker scores 1–2, not 5 to spare feelings. An untested module scores 0, not 5.
- **Verdict is mandatory.** Never end a review without one.

## Common rationalizations

Recognize these — in the author's reasoning and in your own:

| Rationalization | Reality |
|---|---|
| "It works, that's good enough." | Working code still accrues debt, and Drupal's failure modes (cache metadata, access checks, translation escaping) work fine until they don't. |
| "The tests pass, so it's correct." | Tests do not check architecture, security, or cache correctness. A green suite with no access-control test proves nothing about access control. |
| "It's only a small addition to this file." | Small diffs still tangle control flow and push files past the size where anyone can hold them in context. |
| "We'll clean it up later." | Later does not arrive. Require the cleanup, or require a filed issue with an owner. |
| "AI-generated code is probably fine." | Generated code needs *more* scrutiny, not less — it is fluent and confident about APIs it invented. |
| "The refactor makes it cleaner." | Relocating complexity is not reducing it. If the reader holds more concepts afterwards, it got worse. |
| "Security review can wait for the security team." | By the time it reaches them it is a release blocker. Access control and escaping are review-time checks. |
| "It's just a version bump." | A bump is behavior you did not write. Read the changelog. |

## Drupal red flags

Treat any of these as a prompt to look closer:

- `\Drupal::` static calls in a service class.
- `|raw` anywhere in a Twig template.
- A query built with string interpolation.
- A route without `requirements:`.
- A render array without `#cache`.
- A `hook_cron` doing real work synchronously.
- A test that mocks the thing it is supposed to be testing.
- A `hook_update_N()` with no docblock and no idempotency guard.
- A permission reused from another module instead of defined locally.
- A file larger than ~1000 lines, or a class with more than one reason to change.
- Business logic duplicated in a Twig template instead of a preprocess function.

## Related skills and agents

| Need | Use |
|---|---|
| PHPCS / PHPStan / PHPCBF | `drupaltools-coding-standards`, `drupaltools-phpcs`, `drupaltools-phpstan` |
| Run the test suite | `drupaltools-phpunit` |
| Non-code conventions (naming, scaffolding, site building) | `drupaltools-best-practices` |
| Apply efficiency and complexity fixes | `drupaltools-optimize` |
| Drupal.org contribution readiness | `drupaltools-contrib-validator` |
| Whole-site audit | `drupaltools-site-audit` |
| Deep security follow-up | `drupal-security-engineer` agent |
| Fresh-context review of code you just wrote | `drupal-code-reviewer` agent |

## External references

- [Drupal coding standards](https://www.drupal.org/docs/develop/standards)
- [Drupal security team recommendations](https://www.drupal.org/docs/administering-a-drupal-site/security-team-recommendations)
- [Drupal practice standards (PHPCS)](https://www.drupal.org/node/1886776)
- [Writing secure code](https://www.drupal.org/docs/develop/security/writing-secure-code)
- [Automated testing in Drupal](https://www.drupal.org/docs/develop/automated-testing)
