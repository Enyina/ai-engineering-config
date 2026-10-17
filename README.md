# AI Engineering Config

Canonical personal engineering rules: [AGENTS.md](AGENTS.md). **Reverse Engineering First** is the default for significant projects.

## Personal design + engineering intelligence

The private personal config now includes a sourced [design and engineering knowledge system](docs/PERSONAL-INTELLIGENCE.md): [public source catalog](knowledge/sources/catalog.json), [comparison patterns](knowledge/patterns/catalog.json), an evidence-linked [rule map](knowledge/rule-evidence.json), a deterministic `bin/ai-intelligence` advisor, scoped research skills and a weekly **review-only** source-update check. It does not copy employers' rules or automatically promote research into policies.

```sh
python3 bin/ai-intelligence validate
python3 bin/ai-intelligence suggest --workspace ../moatt-verified --project moatt --feature garment-editor --domain design --task "garment editor layout"
python3 bin/ai-source-watch
```

Design suggestions include alternatives and measurable checks, not untested claims. Existing personal fallback hierarchy is preserved; native agent loading and actual product tests must still be verified.

## Clear commits and release notes

Completed authorized work should end in a focused commit and short release notes written in ordinary English for people who aren't developers. Describe what changed, the benefit, and any remaining limitations. Keep internal implementation and test details in technical engineering reports. Respect each project's release process and employer policies. See [plain-English delivery standard](docs/PLAIN-ENGLISH-DELIVERY.md) and [example release notes](RELEASE_NOTES.md).

## Execution roadmap

**[Self-Improving AI Engineering System — 7 milestones](docs/SELF-IMPROVING-ROADMAP.md)**

Phase A: audit + secure current Mac rules; deterministic scope resolution; Codex/Claude Code/Cursor adapters; reverse-engineering skill; evidence-gated lessons; opt-in onboarding/CI. Phase B: private Godot Time Arena lab proving the complete workflow. **Milestone 1 is open** because the local `default.rules` and `config.safe.toml` are not yet inspected; do not commit unreviewed snapshots or run irreversible resets.

## Employer isolation

Personal rule guidance and Codex command permissions are separate. We never store employer-specific rules or debugging commands in this repository, and we never auto-inject personal overlays into employer projects. Read [trust-domain architecture](docs/TRUST-DOMAINS.md); the new `bin/workspace-boundary.py` preflight is read-only, with fail-closed personal-operation decisions. **It is not yet integrated into the future `ai-rules` resolver.**

## Working hierarchical rule engine (preview-first)

Read [Hierarchy, connected systems and AI agent support](docs/HIERARCHY-AND-AGENTS.md). The `bin/ai-rules` CLI resolves an explicit organizational hierarchy with protected rules, shared system groups, project choices and feature preferences. It can generate native Codex/Antigravity `AGENTS.md`, Claude Code `CLAUDE.md`, Cursor `.mdc`, and generic AI guidance. It checks trust-domain declarations and Git origin, and refuses overwriting untracked agent files. `bin/ai-lessons` drafts only human-review proposals; `bin/ai-rules-sync-pr` opens opt-in GitHub PRs from a clean local checkout when `gh` authentication is available.

```bash
python3 bin/ai-rules validate
python3 -m unittest discover -s tests -v
# Run resolve/onboard with --workspace <authorized project repo> and --project <id>
```

Existing Moatt and portfolio `AGENTS.md` files are intentionally protected and require manual merging. Do not copy employer-owned policies into this personal repository or use the default personal pack in employer workspaces.

## Scoping
- Global: `AGENTS.md` — stable standards.
- Opt-in categories: `categories/` — web product, backend reliability, game development, AI media.
- Project templates: `projects/` — Moatt, portfolio, game lab.
- Documentation: `docs/RULE-SCOPING.md` and `docs/SECURITY.md`.

Local project `AGENTS.md` files include only the relevant rule set, so gaming instructions cannot accidentally alter clothing or backend code. Links alone do not make AI coding tools load remote instructions. Each project must carry its selected rules locally and track an upstream version.

## Safety and portability
Only sync personally owned, reviewed rules. Do not upload company instructions, credentials or secrets. The Mac-specific Codex snapshot is **local and unreviewed** (not committed here). The `bin/codex-portable.py` toolkit can audit, capture, restore, and safely revert only toolkit-installed files. Never publish an unreviewed snapshot; see [initial audit](docs/INITIAL-AUDIT.md). Company repos are deliberately excluded until independently authorized.

## Workflow
Review the global rule and relevant category; add a project-level AGENTS.md; link to this canonical repository; implement and test; update overlays through reviewed commits. Keep a documented changelog.

## Easy command-permission review

Avoid opening or sharing your full `default.rules` file. Run `python3 bin/review-codex-rules.py` locally for a sanitized summary. See [command policy findings](docs/COMMAND-PERMISSIONS-REVIEW.md) and the [opt-in minimal approval template](templates/codex/minimal-approvals.proposed.rules). Never commit raw local command approvals, especially project-specific operations.

## First-time Mac import

The October 17 initial local snapshot contained `config.safe.toml`, `rules/default.rules`, and bundled `.system` skills, but **no captured personal global AGENTS.md**. The revised capture excludes bundled skills; use `git pull --ff-only`, run `python3 -m unittest discover -s tests -v`, then run `python3 bin/codex-portable.py capture` again. The old snapshot is retained locally. Review each file before committing. See [docs/INITIAL-AUDIT.md](docs/INITIAL-AUDIT.md).
