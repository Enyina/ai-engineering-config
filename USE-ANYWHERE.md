# Use my evidence-first engineering process

This is a **portable, self-contained instruction** for ChatGPT, Codex, Claude Code, Cursor, Antigravity or another assistant. You can share the public link or copy the paragraph below into a new session when the full personal repository is not connected.

## Copy this into any assistant

> For substantial debugging, engineering or product decisions, follow **Understand → Investigate → Gather evidence → Eliminate possibilities → Verify → Recommend → Learn**. First understand my desired result and inspect the actual available code, logs, documents and constraints. Distinguish observed facts from reports and hypotheses. Investigate the relevant system and keep a compact evidence ledger with its sources. Consider plausible competing explanations and try to disprove them with discriminating checks; **lack of evidence is not a ruled-out cause**. Before claiming a root cause is confirmed, trace the specific failure and verify the mechanism, preferably through reproduction or a decisive check. If evidence is insufficient, say what is unknown and provide the single most useful next check. Recommend a proportionate fix with risks and validation, but **do not modify anything if I ask for diagnosis only**. Record reusable, sanitized lessons as proposals, never automatic global rules. Honor the active project, employer, privacy and authorization policies. Give me a short, plain-English explanation of what was found, ruled out, concluded, and should happen next. Never claim access to tools, files or research that you have not actually used.

## Everyday triggers

You do not need a particular command or phrase. Say:

- “Investigate why this payment approval failed. Don't fix anything.”
- “Find the cause of this failing test.”
- “Why did this design break on mobile? Compare solutions.”
- “Use my evidence-first process to improve this feature.”

The assistant must use what it can actually inspect, not invent access to your private systems.

## Where each part lives

- **Personal coding agents on your computer:** `AGENTS.md`, `CLAUDE.md` and Cursor project rules can carry the process after the local `python3 bin/setup` wizard is rerun for verified personal projects.
- **ChatGPT and other web/mobile chats:** Share this URL or paste the instruction. Access depends on the specific app's browsing, connector permissions and instruction controls. Merely naming a GitHub repo **does not automatically install its rules or grant private repository access**.
- **Employer projects:** The portable process can guide your reasoning, and public/general personal research may be suggested **with clear provenance**. Do not inject personal project instructions or upload employer incident details to the personal repository; organization policy still controls access and implementation.
- **Automated evidence checks:** For personal or authorized local evidence records, `bin/evidence-check` can validate the *structure* of a diagnosis. It cannot establish whether someone fabricated or misinterpreted an observation.

## Durable rule versus real action

This process is a **quality gate**, not an autonomous investigator. It requires the assistant to gather and interpret real evidence using available tools. It cannot inspect production or verify fixes without authorized repository/environment access.

When a lesson is useful, follow the existing `bin/ai-lessons` human-reviewed proposal workflow in the appropriate trust domain. Do not automatically add it to permanent global rules.
