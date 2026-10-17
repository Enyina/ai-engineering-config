# Execution Plan — Self-Improving AI Engineering System

**Status:** Approved planning baseline, implementation not completed.
**Created:** 2026-10-17
**Owner:** Personal engineering configuration (not a company-managed policy)
**Track:** Phase A — milestones 1–6; Phase B — milestone 7.
**Priorities:** security and reproducibility > accurate rule selection > portability > learning > automation > game prototype.

## North star

An authorized new repository can be onboarded with a declared project category, stack and selected feature tags. Codex, Claude Code and Cursor receive relevant, consistent local instruction files. The system can explain **which** rules applied and **why**, run appropriate tests, and propose evidence-backed changes through review. It cannot silently change its own binding rules, ignore higher-priority/managed policies, access unauthorized repositories, or misrepresent test/deployment status.

### Definition of done for the overall program

- Reviewed, secret-free, version-controlled personal rule inventory. Nothing from employer-owned repositories exported without approval.
- One canonical rule registry plus an explicit, deterministic resolver and documented conflict policy. Rules are not assumed to be loaded merely because they exist in a remote repo.
- Three adapters and golden/snapshot fixtures prove the *intended portable content* across Codex, Claude Code and Cursor. Tool-specific capabilities and policy enforcement remain distinct.
- Reverse-engineering workflow with evidence ledger, legal/asset provenance, tradeoffs, testable implementation brief; pilot on one Moatt feature and one original game mechanic.
- Learning proposals generated from sanitized evidence and scoped to rule changes, with human approval, test coverage, changelog and rollback.
- Onboarding and synchronization are preview-first, reversible, committed through PRs rather than unreviewed pushes.
- A new private Godot game-lab repo demonstrates source onboarding, rules, CI, playable Time Arena vertical slice and explicit Mac/controller acceptance evidence.

## Current reality (verified vs outstanding)

**Verified in the connected private repo:** `AGENTS.md`, `rules/CORE-ENGINEERING.md`, `rules/LEARNING-PROTOCOL.md`, `categories/*.md`, `projects/*.md`, `rules/categories/3D-EDITORS.md`, Moatt overlay, and `bin/codex-portable.py`. The repo also has safety/unit test sources and an initial audit document.

**Unresolved:**
- User's original Mac snapshot listed `config.safe.toml`, `rules/default.rules`, and bundled `.system` skills, but no user-level `AGENTS.md`. The content of the first two files has **not** been inspected here. Local revised capture and tests need their results confirmed.
- Legacy layout duplicates rule intent between root `AGENTS.md`, `rules/CORE-ENGINEERING.md`, `categories/` vs `rules/categories/`, and `projects/` vs `rules/projects/`. No automatic migration until inventory and golden tests protect intended behavior.
- Moatt and portfolio reference templates exist. Their actual repo-level agent integrations and local behavior have **not** been independently validated in this milestone.
- No deterministic rule engine, adapters, CI onboarding automation or usable Godot lab is verified as complete.

## Non-negotiable design constraints

1. **Ownership/privacy:** personal repos only by default. Exclude company instructions, customers, production settings, credentials, secrets, session history and unreviewed tool scripts. A private GitHub repo is not a secret vault.
2. **Rule authority:** organizational/agent/system instructions and actual platform controls outrank this custom registry. Within the user-owned generated bundle, use `mandatory security invariants → global → selected category → project → feature`. Later layers may refine or explicitly override **non-security** preferences, but cannot weaken mandatory security or claim to override vendor policies.
3. **Deterministic scope:** resolve from explicit manifest, paths, and feature tags; no free-form LLM guess is allowed to activate a rule. AI recommendations are suggestions for review.
4. **Single source:** one canonical `rules/` registry, unique IDs, version and ownership metadata. The root `AGENTS.md`, `CLAUDE.md` and Cursor artifacts become outputs/templates or compact bootstrap pointers—not competing manually edited copies. Preserve old paths behind compatibility mapping until retired.
5. **No surprise writes:** inspect, resolve, validate and dry-run are read-only. Onboard/sync writes only after preview, owner permissions and explicit `--apply`. No force push or editing unrelated files. Changes to existing projects go through branches/PRs.
6. **Verification truth:** distinguish planned, committed, tests executed, CI results, manual acceptance and deployed behavior. Never call a test "passed" unless it ran.
7. **Evidence-gated learning:** learning means rule improvement via reviewed proposals, not training the underlying model or auto-editing global prompts.
8. **Separation:** Moatt garment geometry/viewport rules must never affect game physics or backend systems. Similarly, personal work may not overwrite a company's repository policy.

## Phase A — Build and validate the engineering foundation

### M1. Audit and secure existing rules — FIRST

**Inputs:** updated Mac audit/capture, committed registry, project instruction discovery for *personally owned* repositories.

**Build:**
- Run local `git pull --ff-only`, Python test suite, `audit`, revised `capture`. Preserve initial capture locally for comparison; keep bundled `.system` skills out.
- Inspect sanitized `config.safe.toml` and `default.rules` and project `AGENTS.md` files; do not import employer content.
- Classify each rule: ID, owner, original path, active scope, rationale, observed evidence, conflict, disposition (keep/merge/move/retire), status and source hash.
- Compare root and nested AGENTS/overrides, existing core rules, category and project duplicates; document Codex config and permissions separately from textual guidance.
- Add secret/privacy gates and preserve fail-safe capture/restore/reset behavior; verify clean restore and recovery in isolated environments, then manually on an authorized noncritical setup.

**Acceptance:** reviewed rule inventory with zero known secrets or company-owned files in tracked artifacts; duplicate/conflict map and migration decision log; test results plus restore/rollback rehearsal. An unaudited Mac capture is **not** milestone completion.

**Blocked on user device:** access to local capture contents and Mac test results. Work on safe inventory tooling can proceed without them.

### M2. Deterministic rule-selection engine

**Build:** canonical rule registry with stable IDs and metadata (`scope`, `applies_to`, `priority`, `mandatory`, `version`, `source`, `tests`); documented manifest schema:
- `project_id`, allowed `repository`, `categories`, `stack`, `features`, `exclude`, `overrides`, `rule_version`, `managed_paths`.
- Support version-pinned YAML manifests under `manifests/moatt.yaml`, `portfolio.yaml`, `gaming.yaml` (real identifiers after repo verification), with JSON Schema validation and restricted override keys.
- A resolver produces ordered `effective_rules.json` plus human-readable `explain` trace: selected, skipped, overridden, conflicting rules, origin and fingerprint.
- Deduplicate legacy global/category/project files without losing behavior. Run migration golden fixtures *before* retiring old paths. Reject unknown categories, conflicting mandatory rules, cycles, invalid feature tags and path traversal.
- Explicit feature intent; never infer project scope based solely on repo name or AI classification.

**CLI:** `ai-rules inspect`, `resolve --project ... --feature ...`, `explain`, `validate`.

**Acceptance:** snapshot tests show Moatt gets product UX + 3D/garment rules but never game rules; Gaming gets performance/control/reverse-engineering but no garment rules; Portfolio gets public/admin UX but neither gaming nor garment rules; all share security constraints. `resolve` is deterministic and explains every inclusion/exclusion.

### M3. Three-agent adapters

**Build:** render local root/nested `AGENTS.md` for Codex, `CLAUDE.md` (plus scoped rules when warranted) for Claude Code, and `.cursor/rules/*.mdc` with valid frontmatter, globs and application mode for Cursor.
- Keep relevant global mandatory text in each generated adapter. Retain tool-specific capabilities only where supported. Never conflate `.rules` command approvals with Markdown instructions or Cursor MDC.
- Generated outputs include source manifest version/hash and a comment warning against direct editing.
- Validate conflict resolution, formatting, escaping, scope and generated-file drift; add golden fixtures.

**CLI:** `ai-rules render --agent codex|claude|cursor|all --project ...`, `diff`, `validate`.

**Acceptance:** all three adapters render consistent shared requirements, preserve feature scope and pass format/golden tests. In an actual test session for each available tool, confirm relevant instructions are read; document any tool not available rather than inventing results.

### M4. Reusable reverse-engineering skill

**Build:** `skills/reverse-engineer/SKILL.md` with a repeatable workflow:
1. Define user outcome, evidence threshold and non-goals.
2. Inspect existing solution and trace state/data/interaction boundaries.
3. Research lawful public references and original sources; record dates, licenses, uncertainty and links.
4. Compare UX, functionality, constraints, failure modes, differentiation and original implementation strategy.
5. Produce ranked feature parity/gap matrix, architecture choice, smallest viable vertical slice and measurable acceptance tests.
6. Implement independently; test, compare outcomes and capture lessons.

Provide evidence ledger, comparison and implementation-brief templates. No copying proprietary assets/code, bypassing access controls or source without a compatible license.

**Acceptance:** one Moatt garment editing/try-on feature and one game Time Arena mechanic each have an evidence-backed comparison, original design, risk assessment, acceptance tests and a reviewable implementation brief.

### M5. Evidence-based learning loop

**Build:** human-reviewed `lessons/` with `observed → cause → candidate rule → scope → affected projects → regression test → review → merge/retire` statuses. Append a provenance record with date, severity, verification and privacy review.
- Auto-detect candidates from opt-in local failure reports, incidents and corrected tests, **never** ingest arbitrary customer data or silently rewrite policy.
- Proposals open PRs with a generated rule diff and affected-project impact report.
- Run negative-scope tests so a Moatt-only interaction rule cannot affect backend or gaming.
- Support reject, amend, retire and rollback paths; measure usefulness and review instruction growth.

**Acceptance:** one sanitized actual engineering lesson becomes a test-backed, human-approved rule with traceability; its unrelated-project exclusion is demonstrated.

### M6. Safe onboarding, synchronization and CI

**Build:** `ai-rules onboard --repo ... --project-type ... [--dry-run|--apply]`; `sync --check` and `sync --pr`. Implement GitHub Actions that:
- validate schema, format, invariants and secret/exclusion scans;
- test resolver fixtures and all adapters;
- detect rule-version drift in opt-in registered personal repos;
- propose update PRs using least-privilege credentials and human review, without force-push, cross-owner writes or surprise deployments.
- surface impacted files, rule provenance, test evidence and rollback in PR.
- distinguish "no access" from "no drift"; run only for explicitly onboarded repositories.

**Acceptance:** new authorized repository gets correct generated instructions and traceable manifest; duplicate run is idempotent; existing project changes produce an optional reviewable PR, preserve custom manual files and offer rollback. No unapproved writes to employer repositories.

**Foundation exit gate:** milestones 1–6 tested together on a fresh example repository, with failure injection for invalid rules, secrets, mixed-scope instructions, unauthorized destination and rollback.

## Phase B — Prove the full system with a game

### M7. Private Game Reverse Engineering Lab

**Dependencies:** M1–M6 foundation exit gate. Creation and access must be under a user-authorized personal account, separate from company repositories.

**Build:**
- Private `game-reverse-engineering-lab` repository, onboarded via `ai-rules` and pinned gaming manifest.
- Godot 4 project with source and original/authorized assets; a compact Time Arena 3D vertical slice: movement, camera, controller actions, one time-based mechanic, one opponent/target, basic feedback, pause/restart.
- Prefer deterministic gameplay state, fixed-step tests where appropriate, and measured frame-time/input responsiveness.
- GitHub CI: import project headlessly, run script/unit smoke checks, create an export artifact with a pinned Godot version and export templates. Confirm hosted build cost/runner limits before depending on macOS remote exports.
- Manual Mac M1 check: download/run a signed or otherwise safely launchable original build; controller buttons mapped, no unintended action overlap; playtest performance, timing and feel; feed evidence into a reviewed learning proposal.

**Acceptance:** an original, playable Time Arena build runs on the Mac M1, gameplay/controller checks have real evidence, headless CI succeeds, and at least one proposed game lesson passes scope tests and approval. Automated checks do not substitute for physical-controller acceptance.

## Executable repository layout (target, migrate incrementally)

```text
ai-engineering-config/
├── AGENTS.md                        # minimal bootstrap; generated/derived after migration
├── manifests/
│   ├── moatt.yaml
│   ├── portfolio.yaml
│   └── gaming.yaml
├── rules/
│   ├── registry.yaml                # stable rule IDs + metadata
│   ├── global/{security,quality,reverse-engineering}.md
│   ├── categories/{frontend,backend,games,ai-media,3d-editors}/
│   └── projects/{moatt,portfolio,gaming}/
├── skills/reverse-engineer/
├── adapters/{codex,claude,cursor}/
├── bin/
│   ├── codex-portable.py            # device inventory and safe restore/reset
│   └── ai-rules                     # manifest resolver, render, onboard and sync
├── lessons/                          # reviewed and sanitized change evidence
├── tests/{fixtures,golden}/
├── docs/{ROADMAP,ARCHITECTURE,RULE-REVIEW}.md
└── .github/workflows/
```

**Migration policy:** existing `categories/`, `projects/`, `rules/CORE-ENGINEERING.md` and `rules/projects/` remain until a checked compatibility mapping and regression fixtures prove that each rule migrated exactly once. Do not rename/erase files first and hope generated outputs match.

## Delivery order / immediate next work

1. **First dependency:** user runs revised Mac capture, validates `tests`, reviews/redacts `default.rules` and `config.safe.toml`; keep snapshot uncommitted until classified. Meanwhile, implement inventory reporting, secret checks and migration fixture baseline using already safe repository content.
2. Map existing rules and document canonical ownership; write the rule schema and resolution decision table. Fix unsafe edge cases in portability CLI before relying on a device reset.
3. Implement M2 resolver and Moatt/Portfolio/Game negative-scope fixtures, then M3 outputs and comparison tests.
4. Implement M4 skill and two pilots; M5 lessons/PR gate; M6 onboarding/CI and rollback demonstration.
5. Only then create and complete the private Godot lab and actual Mac/controller acceptance.

### Concrete build tickets

- **A1:** Collect and classify original local user configuration (user-device input, blocked until delivered).
- **A2:** Inventory duplicate global/category/project rules and freeze golden expectations.
- **A3:** Hardening tests: capture excludes bundled tools, dangerous symlinks/unknown files, failed writes, config leaks, safe rollback.
- **B1:** Manifest/registry schema; validate strict precedence and protected invariants.
- **B2:** Resolver, explain trace, negative-scope fixtures.
- **C1:** Codex/Claude/Cursor renderer + golden fixtures.
- **D1:** Reverse-engineering skill + Moatt/game mechanic pilots.
- **E1:** Human-gated learning proposals + scope regression.
- **F1:** PR-only sync, onboarding, CI and rollback.
- **G1:** Godot repository, prototype, build and hardware acceptance.

## Agent integration compatibility notes

Cursor uses `.cursor/rules/*.mdc` for scoped project rules and may also read `AGENTS.md`; Claude Code uses `CLAUDE.md` and optional scoped rules; Codex uses `AGENTS.md` and separate command permission rules. Their rule-selection policies are **not identical**. The registry defines an intended portable content contract, not a guarantee that three tools give exactly the same response or permissions.

Official references: [Cursor Rules](https://cursor.com/docs/rules), [Claude Code guidance](https://support.claude.com/en/articles/14553240-give-claude-context-claude-md-and-better-prompts), [Codex AGENTS.md reference](https://github.com/openai/codex/blob/main/docs/agents_md.md).

## Decision log

- 2026-10-17: Phase A infrastructure precedes Phase B game lab.
- 2026-10-17: Security and tool-specific higher-priority policies cannot be overridden by feature/project manifests.
- 2026-10-17: Rules are resolved deterministically, with AI proposals reviewed separately.
- 2026-10-17: Existing rules migrate incrementally; no blanket overwrite.
- 2026-10-17: Famasi repositories excluded until explicitly approved company-level onboarding.
