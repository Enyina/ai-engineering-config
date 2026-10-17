# Initial personal Codex capture — 2026-10-17

This is a **metadata-only** review of the paths that appeared in a user-provided local `find snapshot -type f` listing. We do not possess the contents of the local files.

## Observed (not yet analyzed)

- `snapshot/codex/config.safe.toml`: top-level configuration values; values not inspected.
- `snapshot/codex/rules/default.rules`: command approval policy; content not inspected.
- No `snapshot/codex/AGENTS.md` or `snapshot/codex/AGENTS.override.md` was listed.
- `snapshot/codex/skills/.system/{imagegen,openai-docs,review-agent,skill-creator,skill-installer}`: bundled Codex skill directories, not evidence of custom personal rules.
- `snapshot/manifest.json`: checksums/inventory of that capture.

## Interpretation

There is currently **no captured global user AGENTS file**, not proof one never existed. The user's actual project-level instructions may be in individual repositories, or rules may have been supplied to Codex in sessions. Those aren't included automatically in a personal-home snapshot.

**Do not commit the first snapshot:** it includes bundled `.system` skills. A revised capture tool now excludes that directory and preserves the previous capture locally as `snapshot.previous-*`. Review the revised manifest and all captured text before Git commit.

## Next local actions

From your cloned repository:

```bash
git pull --ff-only
python3 -m unittest discover -s tests -v
python3 bin/codex-portable.py audit
python3 bin/codex-portable.py capture
find snapshot -type f | sort
```

After the updated capture, the expected shortlist is **only whatever personal files actually exist**, likely `config.safe.toml`, `default.rules`, and `manifest.json` based on the previous listing. This is a prediction, not an observed new result.

To review contents: read `snapshot/codex/config.safe.toml` and `snapshot/codex/rules/default.rules` locally; **redact any names, paths, usernames, domain names, identifiers, tokens or organization-specific commands** before sharing them. Do not paste your full `~/.codex/config.toml` or credentials.

## Discover project instructions

Run a bounded search only across directories that actually hold your own repositories. For example:

```bash
# Replace ~/Projects with your real source-code parent directory
find ~/Projects -type f \( -name AGENTS.md -o -name AGENTS.override.md \) \
  -not -path '*/node_modules/*' -not -path '*/.git/*' -print 2>/dev/null
```

Do **not** upload employer-owned project instructions to a personal repo. For a repository being examined, running `audit` from within it can report the instruction chain relevant to that current working directory, but it is not a comprehensive per-machine inventory.

## 2026-10-17 Mac results — revised capture and tests

The user ran the revised capture after a `git pull --ff-only`. **Capture succeeded** and the new inventory has just:

- `snapshot/codex/config.safe.toml`
- `snapshot/codex/rules/default.rules`
- `snapshot/manifest.json`

No bundled `.system` skills were captured, and no personal global `AGENTS.md` was found. This is a scope observation, not proof that Codex uses no project-level or session rules.

The user reported **10 tests: 6 passed, 4 failed**. Three restore tests rejected the system-level `/var` symlink on macOS; one reset test expected an error even though an installation receipt was absent and safe reset intentionally does nothing. No restore or reset was reported as applied to the user's live configuration.

Remediation lives in branch `fix/mac-portable-tests-and-safe-reset`: trust the HOME path boundary while still rejecting symlinks inside personal managed paths; fix the stale reset test; add macOS path-alias and unsafe symlink regressions; add CI and ignore unreviewed snapshots. **Do not describe these fixes as passing on a Mac until a new local result is supplied.**

After the fix is merged, run `git pull --ff-only`, `python3 -m unittest discover -s tests -v`, and `python3 bin/codex-portable.py audit`. No new capture is necessary to review the already-clean three-file inventory.

## Current tool safety notes

- Updated capture skips Codex-bundled `.system` skills.
- Updated restore adds individual files without replacing entire skill directories; existing files are backed up.
- Updated reset works only for files installed by this toolkit and whose fingerprints remain unchanged; without an install receipt it does nothing. It is not secure erasure.
- All scripts are still subject to environment/platform verification on the actual Mac.
