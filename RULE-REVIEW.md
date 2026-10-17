# Provisional Rule Review — 2026-10-17

These findings come from an older AI Model Arsenal `AGENTS.md` example and documented user engineering preferences. **They are not a verified inventory of your current Mac Codex environment.**

| Rule | Disposition | Why |
| --- | --- | --- |
| Inspect relevant code before editing | Keep globally | Prevents unsafe assumptions |
| Make minimal, focused changes | Keep globally | Limits regression risk |
| Fully typed TypeScript and validate boundaries | Keep as stack-specific guidance | Practical quality standard |
| Always announce six implementation phases | Simplify | Adds ceremony on trivial tasks |
| Do not run lint/typecheck unless explicitly asked | Replace | Targeted automated verification is an essential engineering responsibility |
| Never commit unless asked | Replace | The owner now authorizes focused commits for completed personal-project work. Follow employer restrictions, do not commit unrelated work or secrets, and never equate committing with permission to publish. |
| Release notes written as developer change logs | Replace | Human-facing release notes must use everyday English, explain outcomes and limitations, and avoid technical terminology. |
| System theme for every UI | Move to project/skill | Different products have different design constraints |
| Ollama/Qwen/AI Model Arsenal architecture | Move to project | Does not apply to every repository |
| Separate manual acceptance from automated verification | Add globally | Prevents invented test confidence |
| No production-success claims without production evidence | Add globally | Evidence-backed release reporting |
| Privacy, authentication, idempotency and safe retries | Keep globally | Risk controls |
| Project-specific operational details | Keep in employer/project repositories | Respect ownership and confidentiality |

## Review method

1. Run `python3 bin/codex-portable.py audit` from each relevant local project.
2. Run `capture` and inspect the collected personal files; never push unreviewed captures.
3. Build a table with: rule, source path, applicable scope, why it exists, evidence, conflicts, decision, reviewer.
4. Merge duplicates and resolve incompatible instructions; use specialized skills for complex repetitive workflows.
5. Compare a fresh Codex session before/after each change with the same test tasks.
6. Track changes in Git with rationale; version global rules separately from project policies.

## Do not overstate completeness

Codex behavior can also reflect model/system instructions, managed policies, trust controls, selected profiles, command-line flags, connected tools, per-session user instructions and files outside the current audit scope. A local scanner is an inventory aid, not a complete effective-policy interpreter.
