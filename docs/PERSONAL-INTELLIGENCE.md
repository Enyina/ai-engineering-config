# Personal UX/UI and Engineering Intelligence

**Implementation status (2026-10-17):** Personal-only curated public sources, comparison patterns, deterministic scoped recommendations, mandatory personal fallback, safe reference metadata watch, dedicated research skills, human-approved lesson proposals, and CI tests. **Not** a trained model, web crawler, autonomous product redesign, or an automatic rule-mutation system.

## The three levels

1. **Knowledge:** Public research, standard documentation and credible patterns in `knowledge/sources/catalog.json`; original comparison options in `knowledge/patterns/catalog.json`. Each rule recommendation has source references in `knowledge/rule-evidence.json`. Provenance does not imply a study validates our implementation.
2. **Rules:** `policies/personal/policy.json` contains *approved* instructions, mandatory or guidance, with category/project/feature scope. The design and engineering catalog does not automatically become active rules.
3. **Experiments and learning:** Compare options, choose based on actual task and constraints, test the change, then pass sanitized observations through `bin/ai-lessons` for **review-only** proposals. Changes go through reviewed Git commits, not live self-edits.

## Categories

Design: foundations and visual hierarchy; design tokens and component systems; navigation and information architecture; forms, input, feedback and recovery; mobile and accessibility; commerce; analytics and dashboards; creative editors and 3D canvases; animation and affordances.

Engineering: source verification; code review and architecture; frontend state; backend reliability; security/privacy; integrated systems; performance; testing and release integrity; AI-assisted development.

The catalogs are deliberately small and extensible. Sources are trusted for **specific kinds of evidence**, not universally. New categories and candidate sources can be suggested, but require review and tests.

## How to use

From `ai-engineering-config`, with an authorized personal project checkout already updated with `.ai-rules/workspace.json` and the right `origin`:

```sh
python3 bin/ai-intelligence validate

# Generate research-backed, distinct design alternatives without writing project files
python3 bin/ai-intelligence suggest --workspace ../moatt-verified \
    --project moatt --feature garment-editor \
    --domain design --task "garment editor canvas layout"

# Compare engineering options for a personal project
python3 bin/ai-intelligence suggest --workspace ../moatt-verified \
    --project moatt --feature garment-editor \
    --domain engineering --task "frontend editor state"
```

The advisor reports the **reason for each option**, tradeoffs, sources and what to test. It does not select a winner automatically. It declines unsuitable project/domain matches and emits a research gap for unknown topics instead of inventing a rule.

To inspect the source catalog's status without network:

```sh
python3 bin/ai-source-watch
```

To check the real official URLs (network use explicitly requested):

```sh
python3 bin/ai-source-watch --network --output public-source-review.json
```

A weekly GitHub Action also checks those public sources and uploads a time-limited report artifact. It does not edit rules, pull in restricted content or publish employer data. Some websites block automated checks; **unavailable** means unknown, not unchanged.

### Explicit metadata baseline

Initial `knowledge/sources/checkpoints.json` is deliberately empty; this means initial online checks flag potential baselines. After examining the **complete** report and confirming official URLs:

```sh
python3 bin/ai-source-watch --adopt-baseline public-source-review.json
# Review and commit the checkpoint file separately.
```

This stores only public metadata such as ETag/Last-Modified, where available; it is **not** rule approval. Later runs can flag changes to those markers, though websites may update layout without updating actual advice. A version update requires reading the authoritative source and examining real meaning.

### Turning experience into a better rule

Take one actually observed and sanitized experiment result; record the actual task, behavior, failures, competing options, evidence and proposed scope. Use existing `bin/ai-lessons --workspace <authorized repo> --event <reviewed local event.json>`, and then `--apply` only to create a **proposal**, not to modify the live rules. Approval requires an attributable reason, tests and a cross-project scope check.

No ML training or unattended design iteration is implied. The agents use the library when invoked on a task; periodic scheduled source checks run independently but only flag potential research.

## Personal fallback, other organizations and agents

**Personal projects** receive personal security/global rules first; approved category, connected-system, project and feature guidance refines those rules. Missing specialist advice falls back to general personal guidance, and the advisor recommends researching gaps. The same mechanism supports Codex, Claude Code, Cursor, Antigravity and explicitly loaded generic instructions via the existing adapters, but **actual local loading still requires testing**.

**Employer-owned repositories** never automatically inherit personal policy, Moatt design patterns, personal command allowances or private learning artifacts. The advisor refuses to run under an employer trust marker; employers must authorize their own policy packs. When an employer lacks a topic, the agent may suggest independently sourced general publicly available guidance within that employer's approved process, not sync this private personal configuration repo.

Security/ownership and platform constraints outrank personal preferences; a category preference cannot weaken mandatory accessibility, privacy or authorization.

## Source and licensing policy

Only link to public source URLs and store short **original interpretations** and metadata. Distinguish official standards, design-system examples, research findings and historical/archived coding guidance; obey attribution and each publisher's content licensing. Don't duplicate subscription reports, commercial design files, proprietary code, designs or other brand assets. Always verify source versions before high-impact implementation.

## Current limits

- Patterns are authored candidate comparisons, **not user-tested recommendations** and not claims that a particular publisher endorses the options.
- The 12 learning routes are registered but not fully automated end-to-end processors; the working parts are controlled catalog, advisor, monitoring and existing proposal workflow.
- Scheduled HEAD checks may be blocked or noisy. They provide a review queue, not a summary of changed research text.
- Source metadata baselines are not yet approved; a fresh check is needed before meaningful revision comparison.
- Design implementation, screenshots, Figma artifacts, usability studies and user metrics are not created by the advisor. Carry them out in an authorized project and verify the results.
