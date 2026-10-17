# Hierarchical AI Rules — implementation guide

**Status:** Core resolver, safe renderer, local proposal workflow and opt-in GitHub PR helper implemented. Cross-agent source generation is CI-tested, **not guaranteed to be loaded in the user's local app without verification**. Device-side system/organization policies still prevail.

## Concept: two orthogonal dimensions

**Trust domain:** Personal, Employer A, Employer B, etc. Never mix policy packages. A company can have any number of projects, and those projects can belong to one or more systems. Every employer owns its **own** policy package in its approved repository or local storage; the personal `Enyina/ai-engineering-config` GitHub repository stores **only personal policies, generic tooling and synthetic employer fixtures**.

**Importance/specificity:** Trust domain is checked first. Then rule kinds:
- `required`: cumulative mandatory instructions; cannot be removed by a lower layer. These do not grant CLI permissions or override native organization/agent safety controls.
- `guidance`: additive implementation guidance from selected layers.
- `preferences`: explicit key-value choices; more specific layers override earlier values. At sibling-system conflicts, a project must explicitly choose an outcome (or validation rejects resolution).

Inheritance within an authorized policy pack:

```text
platform/system safety and employer-managed restrictions (external authority)
           |
      policy pack
           |
     global rules
           |
    organization rules
           |
    selected categories
           |
    connected systems (DAG: parents first)
           |
     project rules
           |
    feature preferences/rules
```

**Connected system:** A group of projects that share APIs, schemas, data ownership, deployment or design contracts, or a reusable capability. A single project can join multiple systems. Parent systems are resolved transitively, with cycle rejection. Individual projects can also belong to zero systems. A system does not grant authorization for all its member repos.

## Personal example: real known repository mappings

`policies/personal/policy.json` has registered:
- `moatt` -> `Enyina/moatt`: web product + 3D editor + garment workbench (itself built on web foundation), with `garment-editor` feature.
- `portfolio` -> `Enyina/newPortfolio`: web foundation + public/admin UX, with `admin-dashboard` feature.
- `gaming` -> planned `Enyina/game-reverse-engineering-lab`: game ecosystem, with `time-arena` feature. This GitHub repo was not verified accessible during implementation.

These are inherited **policy groups**, not claims that Moatt and portfolio share APIs or deployments.

## Synthetic employer example (do not commit actual company policies here)

A company-owned policy pack at `~/work/company-a-rules/policy.json` can define:

```json
{
  "schema_version": 1,
  "trust_domain": "employer",
  "owner": "company-a",
  "rules": [{"id":"security.required","kind":"required","text":"Follow company-approved access controls."}],
  "global": {"rules":["security.required"],"preferences":{}},
  "organizations": {"company-a":{"rules":[],"preferences":{"reviews":"Team review"}}},
  "categories": {},
  "systems": {"orders-platform":{"organization":"company-a","parents":[],"rules":[],"preferences":{"interface":"Stable contracts"}}},
  "projects": {
    "api":{"organization":"company-a","repository":"CompanyA/api","systems":["orders-platform"],"categories":[],"rules":[],"preferences":{},"features":{}},
    "mobile":{"organization":"company-a","repository":"CompanyA/mobile","systems":["orders-platform"],"categories":[],"rules":[],"preferences":{},"features":{}}
  }
}
```

The example is **fabricated**. Do not add actual employer architecture, user records, identifiers, tokens or commands to this personal repo. The company must authorize the use and storage of employer policies before you apply the tool in a work workspace.

## Workspace markers and authorization

The CLI requires exactly one `.ai-rules/workspace.json` or `.ai-rules/workspace.local.json` file. For a **personal** repo, create:

```json
{"schema_version":1,"trust_domain":"personal","policy_owner":"personal"}
```

Employer repos require `trust_domain=employer`, `policy_owner=organization`, and an employer-owned policy pack outside the personal configuration repository. A marker alone is **not** proof of authorization. The resolver additionally verifies `origin` against the policy's allowed `owner/repo` value. Users must still authenticate their git/gh identity and respect employer permission rules.

## Commands

Run from this cloned central repository. `--workspace` is the **target repository**, not this policy repository.

```bash
python3 bin/ai-rules validate

# Preview effective Moatt rules (requires Moatt's repo marker and matching GitHub origin):
python3 bin/ai-rules resolve --workspace ../moatt --project moatt --feature garment-editor
python3 bin/ai-rules explain --workspace ../moatt --project moatt --feature garment-editor

# Preview output files across supported adapters; no write.
python3 bin/ai-rules render --workspace ../moatt --project moatt --feature garment-editor

# Opt-in only, after reviewing existing AGENTS/CLAUDE/Cursor files.
python3 bin/ai-rules onboard --workspace ../moatt --project moatt --feature garment-editor --apply

# Detect drift, read-only. Returns 1 when generated outputs or receipt mismatch.
python3 bin/ai-rules sync --workspace ../moatt --project moatt --feature garment-editor

# Prepare a clean-branch PR, preview first, opt-in explicit remote writes.
python3 bin/ai-rules-sync-pr --workspace ../moatt --project moatt
python3 bin/ai-rules-sync-pr --workspace ../moatt --project moatt --apply
```

**Existing AGENTS.md:** Moatt and the portfolio already have hand-authored `AGENTS.md`. The CLI **refuses to overwrite them**. To integrate, review their existing behavior and prepare a manual merge (or preserve and render only Claude/Cursor). This is a safety feature, not incomplete silent integration. The PR helper requires a clean checkout and local `gh` authentication; without permissions it fails.

**Existing user edits:** the CLI tracks generated-file hashes and refuses to overwrite hand edits or unmanaged paths. The default command is a preview. It does not commit changes automatically except through the explicit PR helper. Reset/rollback uses Git PR revert for project rules; do not use `codex-portable.py reset` for employer offboarding.

## Agent adapters

| Agent | Generated project file | Notes |
| --- | --- | --- |
| Codex | `AGENTS.md` | Native project instructions; command approvals remain separate |
| Google Antigravity | `AGENTS.md` | Antigravity officially discovers AGENTS.md; don't also generate duplicate GEMINI.md by default |
| Claude Code | `CLAUDE.md` | Native project instructions; higher-priority managed policies prevail |
| Cursor | `.cursor/rules/ai-engineering-managed.mdc` | YAML frontmatter `alwaysApply: true`; review native global/team rules |
| Any other agent | `.ai-rules/INSTRUCTIONS.md` | Generic output; may need manual attachment or agent-specific adapter |

The renderer does not claim identical agent behavior or permissions. Install/download the correct native application and verify actual context loading. Adapter support can grow as new tools document stable instruction formats.

References: [Antigravity rules](https://antigravity.google/docs/rules/), [Claude Code context](https://support.claude.com/en/articles/14553240-give-claude-context-claude-md-and-better-prompts), [Cursor rules](https://docs.cursor.com/context/rules).

## Learning loop

`bin/ai-lessons` accepts one sanitized JSON evidence event, checks the workspace against its policy domain and Git origin, and previews a **human-review proposal**. `--apply` writes only the review proposal to the policy pack; it never activates a rule or changes the canonical registry. Employer-specific proposals stay in employer-owned policy stores. Review/approve through Git PR with tests and affected-project diff, then edit the approved domain's `policy.json`.

Sample event:

```json
{
 "schema_version":1,"project":"moatt","title":"Gesture collision lesson",
 "observation":"A pointer gesture modified drawing and camera controls",
 "evidence":"Synthetic pointer regression test, sanitized",
 "candidate_rule":"When editing interactive 3D canvases, enforce a single active gesture owner.",
 "scope":"category","affected_projects":["moatt"],
 "regression_test":"Draw while orbit is locked, then orbit without drawing",
 "privacy_review":"sanitized_and_authorized"
}
```

Save in a **local, reviewed** file and run `python3 bin/ai-lessons --event /path/to/sanitized.json --workspace ../moatt`. Add `--apply` only if you want to write a proposed event in your policy pack. A heuristic scanner is not sufficient to determine whether text is safe to share; review ownership and privacy yourself.

## Limits / explicit follow-ups

- Runtime authorization is controlled by each agent, sandbox, git host and organization, not by a Markdown rule or workspace marker.
- The registry uses JSON (which is valid YAML 1.2); it is strict and dependency-free.
- No auto-import of all local employer configuration. No employer packages were created from real company sources.
- Actual Mac rule activation and native agent loading need owner-side tests.
- CI tests generated content, hierarchy and file guards, **not the live Moatt UI or the future game**.
