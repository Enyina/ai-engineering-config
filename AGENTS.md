# Global Engineering Instructions
Source: this repository. Scope: personal projects only; company-owned repositories follow their own approved policies. This repository is NOT an employer policy source.

## Reverse Engineering First
For significant engineering/product work: define the outcome; inspect existing code and proven references; establish evidence; compare trade-offs; adapt an original solution; test against outcomes; record lessons. Investigate proportionately: a trivial fix does not require three competitor studies. Never bypass DRM, anti-cheat, credentials or licensing; do not copy proprietary code/assets.

## Engineering quality
Understand the current system before adding a new one. Prefer small, reversible changes and explicit acceptance criteria. Preserve existing behavior unless a change is requested. Validate failure modes, edge cases, accessibility, performance, security and regression risk. Never claim tests passed unless executed. State uncertainties.

## Commit and release-note discipline

When you finish an authorized change, make a focused Git commit, rather than leaving completed work uncommitted. Explain the outcome in clear words. Do not include unrelated changes, secrets or incomplete work. Respect higher-priority employer restrictions, project-specific release processes and an explicit user request not to commit. A commit does not authorize a push, merge, deployment, or publication. If a commit cannot be made, report the blocker clearly.

For every meaningful delivered change, create or update the project's human-facing `RELEASE_NOTES.md` (or its existing approved release-note location). **Release notes are for nontechnical readers.** Use short, ordinary English to say what changed, what people can now do or expect, and any remaining limitation. Avoid technical jargon, command names, filenames, implementation details, test frameworks and unexplained abbreviations. Keep technical verification and implementation reporting in separate engineering documents. Do not say a change is available to customers until the release has actually been verified.

## Trust-domain isolation
Before selecting category/project/feature rules, classify the workspace as personal, employer-owned, or unclassified. Apply personal rules only to explicitly approved personal workspaces. Never import employer-specific instructions, code, data, credentials or one-off command approvals into this repository; never inject personal project overlays into employer repositories. Unknown or mixed ownership fails closed. See [docs/TRUST-DOMAINS.md](docs/TRUST-DOMAINS.md).

## Scope resolution
1. Applicable safety/security/company policies cannot be weakened here.
2. Repository AGENTS.md defines project constraints and may override personal preferences.
3. Nested AGENTS.md provides directory-specific detail.
4. A feature-specific approved brief controls the feature within those constraints.
5. Category rules are selectively imported by the project's AGENTS.md; NEVER auto-apply every category.

Other coding agents: read the applicable instructions explicitly; mere remote links are not automatically loaded.
