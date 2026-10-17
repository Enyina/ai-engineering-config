# Implementation Report — Hierarchical Multi-Agent Engineering Rules

**Date:** 2026-10-17
**Source of truth:** [Enyina/ai-engineering-config](https://github.com/Enyina/ai-engineering-config) (private)
**Canonical change:** [PR #11](https://github.com/Enyina/ai-engineering-config/pull/11), merged to main as `2fa5392dc21524c522b613cb6cc869fd3eace4f2`.

## Delivery summary

| Capability | Delivered | Evidence / limits |
| --- | --- | --- |
| Protected mandatory vs preferred rules | Yes | Deterministic JSON policy schema; tests for effective rules and overrides. Does **not** override native platform policies. |
| Multiple employers / organizations | Local policy packs | Employer packs are external to the personal repo, separate per employer. Example test packs are synthetic; no real employer policy was migrated. |
| Multiple employer projects | Yes | Synthetic `companya/api` and `companya/mobile` inheritance tested under same organization. |
| Connected project systems | Yes | DAG parent inheritance, independent projects, multiple system membership, cycle/conflict checks. |
| Feature-level preference overrides | Yes | Explicit project-feature selectors with source trace; cannot drop required rules. |
| Cross-company isolation | Guarded | Matching trust marker, policy owner, repo remote, and external employer pack requirement. These are **not** proof of real ownership or security sandboxes. |
| Codex | Source generated | `AGENTS.md` (project). No local app loading proof. |
| Claude Code | Source generated | `CLAUDE.md`. No local app loading proof. |
| Cursor | Source generated | `.cursor/rules/*.mdc` with frontmatter. No local app loading proof. |
| Google Antigravity | Source generated | Same `AGENTS.md` to avoid duplicate `GEMINI.md`; native context loading not tested. |
| Other agents | Generic fallback | `.ai-rules/INSTRUCTIONS.md`; needs an agent-specific integration to autoload. |
| Reverse Engineering First skill | Yes | `skills/reverse-engineer/SKILL.md` plus two reference-led briefs; no claim that new Moatt/game features were implemented by the brief. |
| Evidence-based learning | Proposal stage | `bin/ai-lessons` validates project identity, privacy acknowledgement and creates review-only proposals. No silent rule update. |
| Safe onboarding / sync | Local CLI and PR helper | Preview-first, managed receipt, drift detection, no unmanaged overwrite. PR helper needs local `git`, `gh` and rights. No automatic employer onboarding. |
| GitHub automated validation | Yes | [CI run](https://github.com/Enyina/ai-engineering-config/actions/runs/39029329316), **57/57 tests passed** on Linux, plus compile and policy validation. Additional documentation commits do not change tested Python behavior. |
| Portfolio personal project integration | Yes | [PR #2](https://github.com/Enyina/newPortfolio/pull/2) merged on main as `0961513e47a80439da5f615e813d3c0e65a81f30`; prior `AGENTS.md` retained; CI successful on branch. |
| Moatt personal project integration | Pending PR | [PR #1](https://github.com/Enyina/moatt/pull/1) adds trust marker, Claude/Cursor companion files and documentation, preserving `AGENTS.md`. Await CI result and safe merge confirmation. |
| Gaming lab prototype | Starter asset only | Source ZIP generated separately; private GitHub gaming repo not verified accessible; Godot binary and Mac controller runtime unavailable here. |

## Active hierarchy and precedence

`Trust domain / native managed security → required rules → global → organization → explicitly selected categories → connected system ancestry → project → feature`.

The resolver accumulates protected `required` rules, appends applicable guidance and chooses the most-specific explicit preference value. Conflicting sibling-system preference requires a project-level resolution. Each decision has a trace explaining source and override. A company can have several projects, including standalone projects and connected subsystems that share explicit contract rules. A project may be in more than one connected system.

## Security decisions

1. Never place real employer policies, company code, session data, local auth scripts, command approvals or customer information in this personal Git repository.
2. A different employer uses an independent policy pack stored in its approved repository or local workspace. No cross-company rule inheritance.
3. Command allowlists (`~/.codex/rules/*.rules`) remain separate from engineering instruction text; the user's original Mac snapshot had 104 auto-allow commands, including employer-specific and high-impact entries.
4. **No active Mac Codex permissions were changed.** The snapshot is Git-ignored; applying the optional safer proposal requires separate explicit on-device action.
5. No PR helper may overwrite existing manually authored instructions or silently push work.
6. Tests validate software logic and generated artifacts, not native agent permission controls or ownership.

## How to use the system

```sh
cd ai-engineering-config
git pull --ff-only
python3 -m unittest discover -s tests -v
python3 bin/ai-rules validate
python3 bin/ai-rules resolve --workspace /path/to/moatt --project moatt --feature garment-editor
python3 bin/ai-rules explain --workspace /path/to/moatt --project moatt --feature garment-editor
```

The real Moatt and portfolio branches add explicit personal trust markers. Until merged into the local branch, `resolve` intentionally denies unclassified target workspaces. The repository origin must match the declared manifest. Do not run `onboard --apply` against current Moatt or portfolio `AGENTS.md`; the generator refuses to overwrite them.

## Remaining acceptance items

- Owner reruns the Mac suite and validates native rule loading in installed Codex, Claude Code, Cursor and Antigravity. Linux CI alone is not native-runtime validation.
- Review/replace old Mac auto-allow entries through a separate protected backup/change/rollback workflow; confirm actual sandbox policy. Historical command analysis does not enforce safer permissions.
- The existing central duplicated legacy rules are not yet migrated into a single canonical registry; current engine's `policies/personal/policy.json` is the source for generated outputs, while legacy documentation still exists.
- Confirm target repositories' authorizations and real source behavior. Portfolio documentation-only merge is not a deployment acceptance test. Moatt PR should merge after its own CI passes.
- GitHub App lacks a verified private game repo creation action. The game starter is **not a proven playable Mac M1 build**, does not establish controller acceptance and cannot be described as complete Milestone 7.
- GitHub Actions validates configuration tests but does **not** automatically enumerate and open cross-repo rule-update PRs unattended. The `sync-pr` helper is explicit/local to prevent cross-employer automation mistakes. A recurring authorized GitHub App with narrowly scoped repo permissions is needed for safe background drift PRs.
- Native format adapters cover major requested tools, plus generic. An entirely unknown future tool cannot automatically consume `.ai-rules/INSTRUCTIONS.md` until its own instruction format is researched and adapter added.

## Evidence vs completeness

**Verified:** source files committed; deterministic resolver and test suite exercised in GitHub Actions; portfolio integration merged after successful checks.

**Not verified:** Mac native agent loading, employer policy authorization, real-time project behavior, Mac game playability/controller, deploying games/apps, blanket migration of all existing personal rules.

Keeping these separate is required by the engineering rules themselves. The implementation has meaningful completed components, but **the entire original seven-milestone program is not yet eligible for final acceptance**.
