# Rule scoping and precedence
**No blanket inheritance across projects.** `categories/*.md` and `projects/*.md` are **reference templates**, not magically auto-loaded instructions.

A personal project's `AGENTS.md` must state which selected categories apply and carry enough actual instructions locally for offline agents. Use a commit-pinned permalink to the canonical source for traceability, not a floating main-only link. For rule changes: review upstream diff, adapt locally, run project tests, then commit. Prefer a PR for important changes.

Example:
```md
# Project instructions
Canonical policy: https://github.com/Enyina/ai-engineering-config
Applies: global + web-product; excludes gaming + ai-media.
Follow local architecture, security requirements and acceptance tests.
Research existing implementations before major features; implement independently and verify.
```

Codex instruction loading depends on root and nested AGENTS.md files. Other agents may require their own adapters. A URL pointer is documentation, **not** automatic execution. Avoid network requirements for basic work.

Company repos are excluded from automatic injection. Do not copy sensitive architecture or internal code into this personal repository. Project safety/security policies and human instructions remain authoritative.

## Review and portability
Capture local rules only after secret scanning and personal/company segregation. Keep snapshots as explicit reviewed commits. Reset and restore should be dry-run-by-default, backed up, and never erase credentials implicitly.
