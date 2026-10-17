# Rule source catalog

| Source | Typical path | Scope | Backup stance |
| --- | --- | --- | --- |
| Personal instructions | `~/.codex/AGENTS.md` | Global | Review and capture |
| Personal override | `~/.codex/AGENTS.override.md` | Global | Review and capture |
| Project instructions | `<repo>/AGENTS.md` | Repository | Keep in authorized project repo |
| Nested overrides | `<repo>/path/AGENTS.override.md` | Directory | Keep in authorized project repo |
| Command policies | `~/.codex/rules/*.rules` | User | Review and capture |
| Personal skills | `~/.agents/skills/*`, `~/.codex/skills/*` | User | Capture text only after review |
| Project skills | `<repo>/.agents/skills/*` | Repository | Project-owned |
| Runtime config | `~/.codex/config.toml` | User | Only allowlisted, non-secret values |
| Project config | `<repo>/.codex/config.toml` | Trusted project | Keep in authorized project repo |
| CLI flags and profiles | Per invocation | Session | Document, not reliably captured |
| Managed policy | Organization/system | Higher-priority | May not be exportable |
| Conversation messages | Per task | Session | Not automatically persistent |

## Review questions
For each rule: **Who owns it? What precise behavior does it change? Why was it introduced? What breaks if removed? What does it conflict with? Can we test it? Which agent(s) should adopt it?**

Keep global rules short and stable. Push specialized standards into project files or skills. Avoid assuming a textual rule provides a hard security guarantee.
