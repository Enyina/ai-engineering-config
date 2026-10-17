# Employer and Personal Workspace Isolation

**Design status:** binding architectural policy for this personal AI-engineering repository. A read-only preflight and deterministic `bin/ai-rules` resolver/onboard/sync CLI are implemented with additional trust-domain, Git-origin and policy-pack checks. Native agent behavior and external GitHub authorization must still be validated. This document is not a technical guarantee that existing Codex sessions are isolated.

## Three different types of "rules"

1. **Engineering guidance:** how to build and verify software; can be reusable if generic, lawful and personally owned.
2. **Project / employer instructions:** business workflows, architecture, API, definitions, role responsibilities, deployment procedures; the owning organization determines whether and where these are stored.
3. **Command permissions:** actions an agent is preapproved to run (`~/.codex/rules/*.rules` for Codex). These can be much more sensitive than text guidelines. Broad globally persisted approvals can affect unrelated repositories.

A successful company-specific debugging command does **not** become a portable engineering standard or an automatic global command approval. Keep those concepts separate.

**Suggestion is not inheritance:** an employer project can be offered outside public-source-backed design and engineering alternatives and clearly attributed general personal guidance, without treating them as company rules. The absence of a company-specific preference does not prevent engineering judgment. Every suggestion identifies its public or personal origin and must be reconciled with the company's actual policies before adoption. This is **read-only advisory**, not a method of copying Moatt-specific rules or company information across trust domains. See [external advice](EMPLOYER-ADVISORY.md).

## Trust domains

| Domain | Source of instructions | Where stored | Automatic central sync |
| --- | --- | --- | --- |
| Personal (Moatt, portfolio, game lab) | Approved general rules + selected personal project overlays | Personal config repo and authorized personal project repo | Opt-in only |
| Employer A | Organization policy and that employer's authorized project-level rules | Employer A's approved storage | **Never** from personal central repo |
| Employer B | Employer B's own policies and project instructions | Employer B's approved storage | **Never** from personal central repo |
| Unclassified / mixed ownership | No assumed rule owner | Inspect only until explicitly classified | **Denied** |

Do not put one employer's rules in another's repo or in personal GitHub, even if that repository is private. Do not rely on repository folder names, hostname guesses, personal email identity or AI classification to establish ownership.

## Selection order: trust before functionality

`workspace trust boundary -> applicable organization/vendor policy -> mandatory safety constraints -> permitted general engineering principles -> project/category/feature guidance`

Trust-domain mismatches **fail closed**. Category and feature overrides never cross an organization boundary. Personal preferences cannot weaken an employer's policy or Codex/Claude/Cursor enforced settings. Instructions from each tool may have a different runtime precedence; our generator is not an authority over them.

For work repositories, use the employer's own `AGENTS.md`, `CLAUDE.md`, `.cursor/rules/`, managed policies and credentials only when the employer permits them. Do not auto-inject personal `AGENTS.md` or links to a private personal repository into employer-owned source.

## Technical defense in depth

- **Global defaults:** use short generic code-quality instructions and minimal command approvals; remove one-off `allow` entries for git push/commit/restore, shell evaluation, DB access, deletion, Docker execution, etc., after an appropriate local review.
- **Workspaces:** separate personal and each employer's repositories and agent sessions, ideally with separate OS users/managed devices when required by employer policy. Where supported, separate agent home/config profiles and connected tools, plus dedicated Git credentials and environment variables. A folder name is not isolation.
- **Storage:** no credentials, raw company scripts, customer records, internal URLs or authentication data in personal snapshots or Git history. Employer-controlled instructions stay in employer-approved repositories.
- **Cross-border learning:** only a general principle that you have the right to reuse may be proposed for shared scope, with sensitive details removed, provenance and review; no direct cross-company copying of code, instructions, models or private assets.
- **Automation:** `ai-rules resolve/render/onboard/sync` now implement equivalent trust-domain checks directly: exactly one marker, package-owner matching, and Git origin matching. Personal policy packs refuse employer/unknown workspaces; employer policy packs live outside the personal repo. The separate preflight remains a minimal read-only check, not a grant of authority. Require opt-in, PRs and authorization even in personal projects. This is enforced by the CLI's existing scope checks but does **not** replace host/organization security controls.
- **Offboarding:** reset only personally managed files on a device you are authorized to administer. Never erase employer policy or credentials through the personal cleanup tool; follow organization offboarding procedures.

## Optional local-only workspace declaration (non-secret)

From an authorized **personal** project root, the file `.ai-rules/workspace.json` can contain:

```json
{"schema_version":1,"trust_domain":"personal","policy_owner":"personal"}
```

For an employer project, if permitted to use the preflight tool, put the marker only in an authorized employer-controlled place or locally untracked `.ai-rules/workspace.local.json`:

```json
{"schema_version":1,"trust_domain":"employer","policy_owner":"organization"}
```

Do **not** commit a local employer marker to a company repository without approval. An employer marker blocks all personal-rule operations. These markers are not proof of ownership; they merely make scope explicit, and future production onboarding must also verify repository ownership/authorization with the Git provider. Two conflicting markers or no marker block operations.

Run without writing to the project:

```bash
python3 bin/workspace-boundary.py --workspace /path/to/a/repo --operation inspect
python3 bin/workspace-boundary.py --workspace /path/to/a/repo --operation personal-rules
```

The second command returns exit status 2 if the repo is unclassified, employer-owned, or its declaration invalid. It prints no rules or company details. The preflight does not activate, change or remove any Codex rule.

## Acceptance tests for future milestones

- Two different employer workspace declarations never resolve to one another's rules or to personal project overlays.
- A work project containing a `frontend` category must **not** automatically pull personal Moatt UI/3D policies.
- Missing/conflicting declarations deny personal onboarding, sync and exports.
- A personal `git push` approval discovered in a work session cannot be promoted to universal policy.
- No company content appears in generated GitHub PRs, CI logs, portable snapshots or learning suggestions.
- Attempts to bypass the check via project name, local file path, symlink, manual manifest edit, or cross-owner remote are covered by tests and authorization checks.
- The actual Codex, Claude Code and Cursor behavior is separately checked; text policy is not a substitute for tool access controls.

**Implementation:** scope checks are now covered by synthetic M2/M6 regression tests. Owner-side and native agent integration verification remain open.
