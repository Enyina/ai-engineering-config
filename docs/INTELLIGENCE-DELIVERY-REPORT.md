# Design and Engineering Intelligence — Delivery Report

**Date:** 17 October 2026
**Scope:** Personal projects only. Not an employer policy system.

## What people can now do

- Start a meaningful design or coding task and get several genuinely different approaches, rather than one fashionable answer.
- Compare what each option helps with, what it sacrifices, the public evidence sources to review and what would prove it works for the actual product.
- Keep guidance separated by personal project and relevant topic so clothing-editor patterns don't leak into the portfolio or game development.
- Flag changes to approved public design/engineering reference pages for a person's review each week.
- Turn actual, sanitized project results into suggested lessons without agents silently rewriting their active rules.

These are working reference, recommendation and review tools, **not an autonomous designer**, an AI model fine-tune or a background system that automatically changes code.

## Implementation and evidence

| Component | Result |
| --- | --- |
| Public source register | 16 curated original summaries with links, credibility type, scope, review date and rights notes |
| Problem and options catalog | 7 scoped comparison guides with 3 differentiated options each; 21 options total |
| Guidance provenance | Explicit source IDs for each newly added design/engineering policy |
| Personal hierarchy | Existing global → category → connected system → project → feature selection retained, plus additional relevant rules |
| Recommendation tool | `bin/ai-intelligence validate/suggest` is read-only; calls the existing workspace and Git-origin check |
| Isolation | Synthetic employer workspaces, wrong remotes and mismatched project topics are refused or excluded in unit tests |
| Source update detection | `bin/ai-source-watch`: allowlisted HTTPS metadata checks only, no redirects, no page copies, review-only revision signals |
| Scheduled monitoring | Weekly GitHub Actions workflow produces a temporary report artifact, using read-only repository permission |
| Learning proposals | Existing `bin/ai-lessons` provides sanitized human-approved rule proposals; 5 new routes are registered without pretending to ingest arbitrary web pages |
| Cross-agent instructions | Root instructions and three new skills describe how to apply this to Codex, Claude Code, Cursor, Antigravity and manually loaded generic agents |
| Automated tests | [Latest verified branch run](https://github.com/Enyina/ai-engineering-config/actions/runs/39049797169): **78 tests passed** |
| Central merge | [PR #16](https://github.com/Enyina/ai-engineering-config/pull/16) merged as `4861117909936caa1fcbfa2bf78309fb8c677e7b`, preserving concurrent `web.design-evidence` work |
| Portfolio adoption | [PR #4](https://github.com/Enyina/newPortfolio/pull/4) merged after passing project checks; no product code changed |
| Moatt adoption | [PR #3](https://github.com/Enyina/moatt/pull/3) merged as `c8875f8` after [CI](https://github.com/Enyina/moatt/actions/runs/39050026501) passed assets, type checks, tests, build, static release checks and browser journeys; no product code changed |

**Verification note:** One earlier parallel Moatt CI run failed on a browser canvas-size timeout. A later full run for the same reviewed change completed successfully. This is not proof that browser timing will never be flaky.\n\n## Why sources aren't automatically binding

Use W3C WCAG as a testable accessibility standard, NN/g and Baymard as research evidence, Apple/Material/Carbon/Atlassian/GOV.UK for platform and component alternatives; use OWASP/NIST and official platform/framework documentation for coding evidence. An original comparison option is **our hypothesis**, not a quotation, endorsement or proof by those publishers. Observe actual outcomes before making an implementation guideline permanent.

Source links and documentation licenses live in `knowledge/sources/catalog.json`.

Google's engineering-practices public repository is archived; its advice may still be useful, but it should not be presented as an actively maintained official source. Do not reproduce commercial or paid research.

## Explicit personal fallback

The personal rule package provides a shared set of general requirements for **authorized personal workspaces**, then applies only the categories, systems, projects and features registered for each workspace. When relevant specialist guidance is missing, the advisor offers a research-gap suggestion and the shared personal foundation remains effective.

**Personal is not a fallback override for employers.** A company can separately authorize relevant public-domain patterns inside its own organization-managed policy package, but the personal config cannot insert company-specific or owner-private rules into that workspace.

## Known limits and review gates

1. First source metadata baselines have deliberately not been accepted. The weekly watcher may flag all sources as needing an initial human-reviewed baseline; unstable/no-ETag pages may remain unverifiable automatically.
2. HEAD metadata cannot establish what research *means*, whether an article actually changed or whether an official source has a new recommended pattern. Changed or unavailable sources remain a review task, not a rule.
3. All reference options are untested against the user's actual Moatt/portfolio audience until appropriate task and usability tests take place.
4. Registered new pipeline names are not automatically executed; video-to-skill and other media ingestion are separate earlier roadmap tasks.
5. Runtime loading in Codex, Claude Code, Cursor and Antigravity on the user's Mac remains unverified. Their project instruction companions are present, but merely linking private central rules does not load them automatically.
6. No employer-owned code, tokens, policies, or customer data were copied or modified.
7. GitHub CI is not proof of production UI behavior or successful website deployment. Native project work and release claims need their own evidence.

## Local usage

```bash
cd ai-engineering-config
git pull --ff-only
python3 -m unittest discover -s tests -v
python3 bin/ai-intelligence validate

# Update the next line to the actual personal Moatt checkout with a registered Git origin.
python3 bin/ai-intelligence suggest --workspace ../moatt-verified --project moatt --feature garment-editor --domain design --task "garment editor layout"

# Read source-review status with no network calls.
python3 bin/ai-source-watch
```

Read [Personal Intelligence guide](PERSONAL-INTELLIGENCE.md) for category scope, evidence standards, weekly source checks and review-only learning.
