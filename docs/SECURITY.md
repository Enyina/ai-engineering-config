# Security and privacy

This repository is **private**, but private Git repositories are **not secure secret vaults**. Treat all committed text and Git history as potentially copied, backed up or later exposed.

## Never commit
- OAuth tokens, API keys, passwords, SSH private keys, GitHub tokens, authentication state.
- `~/.codex/auth.json`, session transcripts, local history, credentials, or raw complete `config.toml`.
- Proprietary employer instructions, business data, customer records, source code or deployment details.
- Unreviewed skill scripts or permission rules. Those can execute commands or grant elevated capabilities.
- Local file paths and raw audit inventory if they reveal employer names, private projects or user identity.

## Capture checklist
1. Review every exported file and the staged `git diff --cached`.
2. Confirm `git remote -v` points to your **private** personal repository.
3. Optionally run an independent secret scanner.
4. Only commit user-owned, permissioned policy; remove employer-specific contents.
5. If secrets were committed, rotate them. Deleting a Git commit is not a reliable substitute.

## Restore checklist
Run the dry-run command first. Check the snapshot manifest and any scripts in skills. Back up existing local configuration before copying. A different agent does not necessarily honor Codex sandbox rules, so validate tool permission behavior separately.

## Reset checklist
Resetting instructions is not the same as deleting credentials, tool sessions, environment variables, shell history, downloaded files, IDE caches, or account authentication. Verify Git remote backup independently. Obey your organization's managed-device/offboarding rules.
