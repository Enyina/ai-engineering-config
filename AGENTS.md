# Global Engineering Instructions
Source: this repository. Scope: personal projects only; company-owned repositories follow their own approved policies. This repository is NOT an employer policy source.

## Everyday requests

The preferred user experience is natural language: describe the desired improvement, and the assistant identifies the relevant project guidance. For substantial decisions, the assistant should assess current project behavior and credible public references, explain a practical recommendation and meaningful alternatives, and name the sources used. When the central personal library is genuinely accessible, the local `bin/ask` tool offers a concise interface; otherwise rely on authorized existing instructions and sources. Distinguish employer-owned policy from outside guidance, and never describe an unavailable private library as already consulted.

## Evidence-first problem solving

For meaningful debugging, production incidents, regressions and uncertain architecture decisions, use this process by default: **Understand → Investigate → Gather evidence → Eliminate possibilities → Verify → Recommend → Learn**. Do not wait for the user to say the exact phrase. Start with the actual authorized code and observable behavior; distinguish facts, reports and hypotheses. List competing explanations when relevant, then use discriminating checks to rule out only what evidence contradicts. Do not label a root cause confirmed without directly supporting and verifying its mechanism. If the cause remains unclear, state that and identify the next most useful check. Honor requests for diagnosis only; no code changes in that mode. Recommend with the right confidence and propose sanitized lessons for approval, not silent global rule changes.

Use [the investigative skill](skills/evidence-first-investigation/SKILL.md) when accessible, and [portable instructions](USE-ANYWHERE.md) for contexts without this repository. `bin/evidence-check` validates the **structure** of local investigation notes, not the truth of the observations. Never disclose employer incident evidence into this personal repository.

## Reverse Engineering First
For significant engineering/product work: define the outcome; inspect existing code and proven references; establish evidence; compare trade-offs; adapt an original solution; test against outcomes; record lessons. Investigate proportionately: a trivial fix does not require three competitor studies. Never bypass DRM, anti-cheat, credentials or licensing; do not copy proprietary code/assets.

## Engineering quality
Understand the current system before adding a new one. Prefer small, reversible changes and explicit acceptance criteria. Preserve existing behavior unless a change is requested. Validate failure modes, edge cases, accessibility, performance, security and regression risk. Never claim tests passed unless executed. State uncertainties.

## Research-backed design and engineering

For substantial personal UX/UI or architecture choices, consult the curated public references and alternative patterns under `knowledge/`. Start with existing product behavior and actual project constraints, then suggest distinct options, benefits, tradeoffs, acceptance checks and source links. Do not assume an elegant picture is proof of good usability or copy protected source designs. Scope design standards to interface projects and backend guidance to relevant systems. The `bin/ai-intelligence` advisor is read-only and requires a verified personal workspace. New findings go through human-reviewed proposals, not silent self-edits. Read [docs/PERSONAL-INTELLIGENCE.md](docs/PERSONAL-INTELLIGENCE.md) for details.

## External advice for employer projects

When solving an authorized employer problem and company rules do not cover a choice, do not stop thinking or wait for a company rule to be written. Suggest credible public approaches and relevant **general** reusable personal lessons, explicitly labeling each source and its status as a suggestion. Explain alternatives, benefits, trade-offs, and what to verify. Company rules, actual access controls, security and law take precedence; never imply suggestions are approved employer policy or automatically install them. Do not transfer personal project-specific instructions (such as Moatt, portfolio or games), company code, credentials or operational details into other organizations. The shared `bin/ai-intelligence --advisory-for-employer` mode provides **read-only, credited suggestions** from generic public and personal sources. See [docs/EMPLOYER-ADVISORY.md](docs/EMPLOYER-ADVISORY.md).

## Commit and release-note discipline

When you finish an authorized change, make a focused Git commit, rather than leaving completed work uncommitted. **Write the commit headline itself in ordinary English**: describe what someone gained, what was corrected, or what risk was reduced. A reader should understand it without opening the code. Avoid jargon, unexplained abbreviations, file names, and developer-only prefixes when project rules permit. If a repository enforces a particular commit format, preserve its required structure while making the description clear; do not silently bypass project checks. Do not include unrelated changes, secrets or incomplete work. Respect higher-priority employer restrictions, project-specific release processes and an explicit user request not to commit. A commit does not authorize a push, merge, deployment, or publication. If a commit cannot be made, report the blocker clearly.

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
