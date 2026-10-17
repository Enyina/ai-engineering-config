---
name: reverse-engineer
description: Evidence-driven, lawful product or implementation benchmarking to independent feature design.
---

# Reverse Engineering First — repeatable skill

Use when solving a substantial feature, diagnosing an unfamiliar system, or selecting between established approaches. Skip heavyweight competitor research for trivial fixes. **This is not permission to access private code, bypass paywalls, evade anti-cheat, copy protected assets, or reverse engineer credentials.**

## 1. Define the outcome
Write the user need, existing implementation, measurable acceptance, constraints, scope, decision owner and non-goals. Name the current repository and trust domain. Stop if authorization is missing.

## 2. Inspect our implementation
Trace user interaction, state owner, main data flow, persistence, API contracts and failure points. Separate observed behavior from unverified assumptions. Run relevant existing tests before modifying. Never replace code based on a guess about the current state.

## 3. Collect proven references
Use official demos, product documentation, public source with compatible licenses, reproducible screenshots or permitted UX observation. Record URL, access date, exact observable behavior, licensing/terms, applicability and uncertainties. Do not infer proprietary internals merely from a demo.

## 4. Compare alternatives
At minimum compare: core user journey, reliability, constraints, usability, learnability, performance, security, accessibility, development cost and measurable differences. A large checklist is not itself a product strategy. Prioritize the problems real users experience.

## 5. Produce an original feature plan
Create a feature-gap matrix; a decision log explaining why one pattern was chosen; a small independent vertical slice; data and interface contracts; a rollback plan; unit, integration, visual and manual acceptance scenarios. Work in the owning project's repository.

## 6. Implement and validate
Compare the implemented behavior against the stated acceptance contract, not merely against an attractive screenshot. Verify broken-state cases, repeatability and regression boundaries. Report measured results, missing evidence and open risks.

## 7. Learn
Classify each conclusion as `no rule change`, `project lesson`, or `candidate shared rule`. Candidate shared changes require sanitized evidence, trust-domain clearance, a rule diff, affected-project tests, human approval and rollback. Never silently change mandatory rules.

### Output templates

**Evidence ledger**
`reference | observed behavior | tested/reproduced? | source/license | relevant strength | known limitation | uncertainty`

**Comparison**
`user need | our current behavior | reference A | reference B | independent implementation choice | verification`

**Implementation brief**
`problem | why now | success metric | relevant references | architecture/data ownership | scope | tasks | edge cases | failure/rollback | tests | manual acceptance`

**Lesson proposal**
`sanitized observation | reproducible evidence | applicability | proposed rule | conflicts | required regression | owner approval`

Only use information that belongs in the current trust domain. If comparing two employers, abstract to a lawful generic principle without leaking private implementation details.
