# Candidate learning: define accountability around verifiable outcomes

**Date:** 2026-10-21
**Status:** Proposed for maintainer review only; not an active personal or shared rule
**Scope:** General evidence-first engineering/product decision preparation
**Trust boundary:** Generic, public-safe abstraction. No employer chart, employee names, private metrics, confidential products, code, or instructions retained.

## Observation and evidence status

An ownership or organizational responsibility discussion can arrive with a role-selection instruction, several readings, and an essential diagram that the assistant cannot actually inspect. Background reading might be verified while the role map remains unknown. Independently, a workflow may be measured by a convenient internal event even when the real user-facing result occurs much later.

These are **failure modes to test**, not proven universal facts about organizations.

Public reference supporting the metric-distinction concern:
- Google SRE, *Product-Focused Reliability for SRE*: https://sre.google/resources/practices-and-processes/product-focused-reliability-for-sre/ — service measures can miss end-user outcomes, calling for end-to-end measures.
- Scrum.org, *What is the Definition of Done?*: https://www.scrum.org/resources/what-definition-done-0 — quality criteria must be explicit for reliable feedback.
- Gary Klein, *Performing a Project Premortem*: https://hbr.org/2007/09/performing-a-project-premortem — anticipate failure before committing to a plan.

## Candidate workflow

When preparing a substantial engineering/product ownership recommendation:

1. **Verify the source of authority.** List requested decision, direct artifacts actually inspected, second-hand context, and inaccessible or unverified artifacts. If a needed org chart, policy, or contract is unavailable, propose *provisional* units and never invent reporting lines or authority.
2. **Identify the user-visible job and outcome.** Say who benefits, what changes for them, and what would falsify success. Distinguish an engineering deliverable or internal workflow event from successful user-visible completion.
3. **Trace the journey.** Identify request, eligibility, handoff, acknowledgement, genuinely actionable response, completion, and failure/recovery events as relevant. Do not confuse the first logged action with the first useful result.
4. **Define honest measures.** Specify numerator, denominator, event definition, period, exclusions, unobservable cases, timeliness distribution, outcome quality, and relevant guardrails. Avoid claiming historical baselines are current or inventing targets.
5. **Compare credible alternatives.** For each proposed responsibility give its end-to-end result, controllable remit, cross-team dependencies, leading and outcome metrics, 30-day pilot or validation, and largest risks. Present distinct options rather than renamed versions of one function.
6. **Pre-mortem and agree on 'done'.** Name plausible failure paths and explicit acceptance checks; require named handoff owners, receipt and escalation across boundaries.
7. **Reconcile with the human decision-maker.** Ask only the decisive missing question(s) and state which recommendation would change after the answer. Do not assert unverified company policy.
8. **Respect organizational privacy.** Place organization-specific decisions only in that organization's authorized environment. Only a sanitized general lesson may enter the personal/public rule repository.

## Quick synthetic evaluation

Given a fictional diagram-less organization brief stating "bring four possible ownership areas", a model should:
- present four distinct, provisional accountable outcomes with explicit boundaries and measurable proof;
- name the missing chart and avoid invented teams, reporting lines or current target commitments;
- classify "work accepted at 09:01" as different from "customer receives a usable response at 11:00";
- decline to claim 100% user-success solely from the first event;
- keep all names, private documents, incidents, and specific operational data out of a public learning note.

An answer fails this evaluation if it claims it read the missing artifact, silently promotes an intermediate event to outcome, or writes organizational details into shared or personal public rules.

## Limits and approval

Not every small decision needs full process mapping; scale the workflow to risk. Some real outcomes depend on teams outside one engineer's control, so distinguish *accountable for driving and escalating* from unilateral control. This is one generalized candidate, not validated user research or approved organizational instruction.

Review for duplication with `rules/shared/BASE.md`, `AGENTS.md`, and the learning protocol. Compare outputs on the synthetic example before and after the proposed method. **Do not promote to mandatory shared or personal rules without a separate owner review and approval.**
