# Proposal: Evidence-first career portfolio reviews

**Date:** 2026-10-17
**Status:** Candidate for owner review — NOT a promoted or automatically enforced rule
**Trust domain:** Personal only
**Scope suggested:** Portfolio project + web-product category; the general claim-verification rule may become a reusable personal guideline after review

## Problem observed

A production-bound personal engineering portfolio had a polished visual refresh, but its hard-coded experience and work list were not reconciled against the owner's latest résumé. Old showcase projects were weighted equally with newer production outcomes. A Figma Make design reference contained plausible-looking employment and success metrics that were not corroborated. The public React component rendered sections directly and did not consume the stored section-visibility settings, so source configuration and public behavior could diverge.

The user asked for an audit, stronger projects, and to be notified **before any change to the displayed project selection or descriptions**.

## Source and evidence boundaries

- Owner-controlled portfolio source: `Enyina/newPortfolio`, `main`, reviewed 2026-10-17.
- Owner's most recent identified résumé: `Matthew_Enyina_The_Flex_Senior_Full_Stack_Product_Engineer_CV.pdf`, dated/uploaded 2026-10-05. This is a self-authored CV claim source, not independent measurement evidence.
- Reference design: Figma Make project `ZAv7iF1KN3E839Z5ZDASDy`; use its UX structure as a reference, never import unverified employers or metrics.
- GitHub official guidance: https://docs.github.com/en/account-and-profile/tutorials/using-your-github-profile-to-enhance-your-resume — emphasize a small selection of relevant, explainable projects with useful README, working proof, tests and demos.
- NNGroup's UX careers research: https://www.nngroup.com/reports/user-experience-careers/ — hiring reviewers benefit from specific work-to-outcome explanations (UX hiring context, not proof of software-engineering interview results).
- Existing personal project-home alternatives in `knowledge/patterns/catalog.json`: proof-first, editorial, and hybrid.

**Evidence grading:** public repository code/build/test/working demo; résumé self-report; firsthand owner statement; independently verified metrics; inference and open questions must remain separate. Never represent a résumé metric as externally verified merely because it appears in a PDF.

## Candidate reusable workflow

1. **Define audience and intended opportunity:** recruiters scanning quickly, hiring engineers checking implementation depth, and customers deciding whether to contact; select which matters most now.
2. **Inventory truth sources:** latest identified résumé, owner-approved narratives, codebases, production demos and relevant asset permissions; note date and confidence.
3. **Build a claim-to-source ledger:** each role, date, outcome metric, technology, project contribution and public image has a source reference and publication permission; conflicting versions are explicitly escalated.
4. **Score possible case studies (proposal):** role relevance (30), engineering depth (20), demonstrable proof (20), differentiation (15), ease of understanding/demo (15). These weights are hypotheses, not researched industry standards.
5. **Compare three presentation modes:** proof-first, editorial, hybrid; use the existing personal advisor patterns rather than blindly inheriting a Figma mock-up.
6. **Create a proposed project change table:** KEEP/DEEPEN, COMBINE, ARCHIVE FROM FRONT PAGE, REPLACE ONLY IF PROVEN. Explain each proposed change and explicitly secure owner approval **before mutating project content or visibility**.
7. **Respect ownership:** company work may be shown only with approved public facts and independent redacted explanations; never reveal private source code, customer data, operational vulnerabilities or internal dashboards.
8. **Implement with reliable release checks:** public section visibility really drives rendered components; project slug links resolve; draft records never leak; a CV download opens; project images and alt text work; direct-load routing works; mobile/desktop contact CTA works; preview and production independently verified.
9. **Learn from outcomes, not taste:** assess a short recruiter task (identify specialty, best case study, and contact within a brief review), access logs/analytics when available and consented, and real outreach/interview responses; record observed findings before changing global rules.

## Distinct candidate layouts and trade-offs

- **Proof-first:** value proposition and 2-3 believable evidence links immediately; fastest work discovery but can feel overly transactional.
- **Editorial:** high-distinction Figma-inspired typography; more memorable, but substance and CTA can be buried.
- **Hybrid (initial hypothesis):** concise personal positioning + verified evidence near fold + 3-5 deep case studies + direct contact/resume; supports roles and clients but requires editorial discipline.

**Preferred hypothesis:** hybrid, conditional on owner approval and actual usability validation.

## Verification/approval before promotion

- Compare résumé field-by-field against site, with dates and discrepancies recorded.
- Run content contract tests that fail on unsourced fake statistics, missing public routes, hidden/draft leakage, broken résumé path and inconsistent section toggles.
- Have owner explicitly approve each project removal, strengthening narrative and employer-owned claim prior to public commit.
- Perform desktop/mobile task-based review and correct evidence citations; treat untested suggestions as proposed, not validated.
- Promote only sanitized, tested, broadly reusable guidance to active policy with a separately reviewed change.

## Rollback and privacy

Only review documentation is created by this proposal. No public portfolio project, live content or production data is changed. Do not copy owner résumé or internal company code into this private learning proposal.
