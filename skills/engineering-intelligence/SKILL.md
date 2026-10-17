---
name: engineering-intelligence
description: Compare credible coding and architecture strategies for authorized personal projects, validate implementation tradeoffs, and propose tested rules.
---

# Evidence-led engineering

1. Inspect current code, user outcome, architecture, repository state, tests and failure evidence in an authorized environment. Check exact tool/framework versions before relying on documentation. If an employer has no specific rule, still compare official public guidance and **general** reusable personal approaches, naming their provenance and checking employer policy before adoption. Suggestions do not become company rules automatically. Use `bin/ai-intelligence suggest --advisory-for-employer` with a non-confidential topic when needed.
2. Use the curated `knowledge/sources/catalog.json` and actual official upstream docs, standards and working examples. Prefer OWASP/NIST for security, official languages/frameworks for API semantics, Playwright/Storybook for UI testing, and scoped Google engineering advice for review discipline. Its upstream engineering-practices repo is archived; do not treat it as a current evolving standard.
3. From central config run `python3 bin/ai-intelligence suggest --workspace <repo> --project <id> --domain engineering --task "<specific technical problem>"` to inspect genuinely different options; this never writes code or selects a winner.
4. Record benefits, tradeoffs, failure cases, complexity and costs; independently choose based on project constraints. Never infer that a source explicitly endorses our own comparison option.
5. Verify via proportionate targeted tests, integration boundaries, performance/security measurements and important end-to-end user journeys. Capture actual results.
6. Propose sanitized, scoped corrections and tested rules with human review via `bin/ai-lessons`. Reject unproved generalizations and avoid copying employer-owned code or operational context.
7. Make a focused commit when authorized. Write release notes in plain language and keep technical testing details in separate evidence.

## Topics
Architecture, frontend/mobile, backend, systems integration, security/privacy, resiliency/retries/idempotency, CI/testing, performance, observability, AI engineering.

Avoid large research rituals for trivial fixes. Treat source docs as evidence, not as an automatic order to rewrite a working codebase.
