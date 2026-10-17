# AI Engineering Config

Private, version-controlled home for personal Codex coding instructions, command rules, and reusable agent skills.

> **Current state:** Starter templates and tooling only. The actual rules on your Mac have **not** been imported, audited, or activated. Nothing in this repository changes your machine merely by being cloned.

## Goals

1. **Audit:** identify the instructions, local configuration, skills and command policies that may influence Codex in each project.
2. **Review:** know why each rule exists, its scope, and whether it is safe and useful.
3. **Capture:** keep reviewed **personal** rules in a private Git repository.
4. **Restore:** install approved rules on a new machine, backing up any files that would be replaced.
5. **Reset:** safely remove personal-managed rules before leaving a device; credentials and company configuration require separate cleanup.

## Quick start — current Mac

```bash
git clone git@github.com:Enyina/ai-engineering-config.git
cd ai-engineering-config
python3 bin/codex-portable.py audit
python3 bin/codex-portable.py capture
python3 -m unittest discover -s tests -v
```

Review `snapshot/` **file by file** before staging or pushing anything. In particular, remove credentials, secrets, internal business information and employer/project-specific instructions. The capture does **not** upload files automatically.

```bash
git status --short
git diff -- snapshot/
git add snapshot/
git diff --cached
git commit -m 'Capture and review personal Codex rules'
git push origin main
```

## Quick start — new Mac

```bash
git clone git@github.com:Enyina/ai-engineering-config.git
cd ai-engineering-config
python3 bin/codex-portable.py restore
python3 bin/codex-portable.py restore --apply
python3 bin/codex-portable.py audit
```

Restore defaults to user-owned instruction and rule files, not authentication or full MCP configuration. Review `docs/SECURITY.md` before use.

## Cleaning up before leaving a device

```bash
python3 bin/codex-portable.py reset
python3 bin/codex-portable.py reset --apply --confirmed-remote
```

The reset command is **not** secure erasure, organizational offboarding, or sign-out. It deliberately preserves credentials and session history. Follow your organization's process and manually check all other storage locations.

## Instructions and precedence

- `~/.codex/AGENTS.md`: global personal coding instructions.
- Project `AGENTS.md`: local repository instructions, not suitable for automatically exporting from company repos.
- Nested `AGENTS.override.md`: narrower directory-level instructions.
- `~/.codex/rules/*.rules`: Codex command approval rules; **not** a substitute for OS security boundaries.
- `~/.agents/skills/`: reusable workflows, which may include executable scripts.
- `~/.codex/config.toml`: runtime settings; snapshot handles a limited reviewed subset only.
- Codex defaults, managed policies, conversation instructions, CLI flags and cloud settings may also affect behavior. No local script can definitively export all of them.

See [RULE-REVIEW.md](RULE-REVIEW.md) for what to keep, change, or scope differently and [docs/SECURITY.md](docs/SECURITY.md) for privacy precautions.

## Cross-agent portability

`AGENTS.md` is a useful plain-language source of intent; not every other AI coding tool uses it or implements Codex `.rules`, sandboxing, or config keys. Apply adapters and verify behavior in each tool rather than blindly copying files.

**Do not commit company-owned or customer material to this repository.** Keep Famasi-specific instructions in authorized Famasi repositories.
