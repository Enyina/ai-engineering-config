# Command approval audit — sanitized, 2026-10-17

**Source:** a user-provided excerpt of personal `config.safe.toml` and `default.rules`. The original contains employer/project-specific code, internal paths and operations that inspect authentication and user data. **It is not included in this repository.**

## Findings

- Config keys visible in that user-provided export: `model = "gpt-5.6-sol"` and `model_reasoning_effort = "low"`. The export did not include `approval_policy` or `sandbox_mode`, so their effective values **are unknown**, not necessarily unset. This records historical state, not current platform availability.
- 104 `prefix_rule` entries were visible and each specified `decision="allow"`.
- A conservative *exclusive* heuristic classified **48** as project-specific or potentially sensitive, **23** as high-impact auto-allow, **18** as read-oriented candidates, and **15** as task-specific. The classification is a prioritization tool, not security validation.
- Explicitly concerning auto-allow prefixes include broad Git staging/commit/push/restore/removal and branch operations, process termination, filesystem deletion, arbitrary shell/JavaScript execution, Docker build/run, and project-specific scripts/data queries.
- Several long approvals refer to particular API, database, testing and simulated-auth sessions. Their actual source code, paths and parameters must stay outside personal Git history. There are **no observed actual token values** in the analyzed text; some commands read credentials at runtime and can output data.
- No global `~/.codex/AGENTS.md` was present in the captured file list. A GitHub root `AGENTS.md` does not automatically become a global Mac instruction.

## Recommended disposition

| Group | Decision | Rationale |
| --- | --- | --- |
| Broad write/destructive/remote operations | Remove from automatic global approvals | Keep explicit authorization for commits, pushes, deletion, process operations, DB writes, production changes |
| Company-specific and one-time debugging | Exclude from personal repository; review local removal | They are not portable and may reveal private operations or user information |
| Read-oriented candidate commands | Review, then keep a narrow allowlist if desired | Read commands still require proper scope; avoid overly broad tool arguments |
| Build/test/developer scripts | Approve per project/task | npm, node, shell and container scripts can perform arbitrary side effects |
| Engineering behavior standards | Manage separately in canonical rule registry | Command approvals are not code-quality rules |

**No existing Mac approval rules have been changed. No snapshot content has been committed.** The review is advisory and must not be interpreted as a validated effective command policy (vendor defaults, sandbox and other user/config layers also apply).

## Run future reviews without pasting raw files

From your local clone:

```bash
git pull --ff-only
python3 -m unittest discover -s tests -v
python3 bin/review-codex-rules.py
```

The script reads `~/.codex/rules/default.rules` locally and prints a **sanitized aggregate**: counts, decisions and categories. It does **not** mutate the approval file, upload contents, list identifiers or reproduce embedded commands. The classifier is deliberately conservative, and raw snapshots remain Git-ignored.

If you later choose to simplify permissions, keep a copy outside the repository and write a separate, minimal personal allowlist only after reviewing your actual Codex sandbox/approval behavior. Prefer leaving an operation subject to default approval checks over allowing it globally.

## Further audit

1. Verify GitHub CI and Mac test run for the review tool.
2. Confirm the actual Codex approval policy, sandbox and per-project runtime behavior; an absent key in the sanitized export is not a determination.
3. Inventory separate `AGENTS.md` and `AGENTS.override.md` files in authorized personal project roots, and compare to canonical GitHub rules.
4. Revisit the portable capture tool: prefer **metadata-only command capture** with explicit review before exporting `.rules` text into `snapshot/`.
5. Never copy these employer-specific operations into Codex/Claude/Cursor common global rules.

This audit supports [M1](https://github.com/Enyina/ai-engineering-config/issues/1).
