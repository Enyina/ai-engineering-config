# AI Engineering Config

Canonical personal engineering rules: [AGENTS.md](AGENTS.md). **Reverse Engineering First** is the default for significant projects.

## Scoping
- Global: `AGENTS.md` — stable standards.
- Opt-in categories: `categories/` — web product, backend reliability, game development, AI media.
- Project templates: `projects/` — Moatt, portfolio, game lab.
- Documentation: `docs/RULE-SCOPING.md` and `docs/SECURITY.md`.

Local project `AGENTS.md` files include only the relevant rule set, so gaming instructions cannot accidentally alter clothing or backend code. Links alone do not make AI coding tools load remote instructions. Each project must carry its selected rules locally and track an upstream version.

## Safety and portability
Only sync personally owned, reviewed rules. Do not upload company instructions, credentials or secrets. Existing Mac-specific Codex config has not yet been captured or audited; previous local restore/reset automation is not yet available. Company repos are deliberately excluded until independently authorized.

## Workflow
Review the global rule and relevant category; add a project-level AGENTS.md; link to this canonical repository; implement and test; update overlays through reviewed commits. Keep a documented changelog.
