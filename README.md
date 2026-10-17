# AI Engineering Config

Canonical personal engineering rules: [AGENTS.md](AGENTS.md). **Reverse Engineering First** is the default for significant projects.

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

## First-time Mac import

The October 17 initial local snapshot contained `config.safe.toml`, `rules/default.rules`, and bundled `.system` skills, but **no captured personal global AGENTS.md**. The revised capture excludes bundled skills; use `git pull --ff-only`, run `python3 -m unittest discover -s tests -v`, then run `python3 bin/codex-portable.py capture` again. The old snapshot is retained locally. Review each file before committing. See [docs/INITIAL-AUDIT.md](docs/INITIAL-AUDIT.md).
