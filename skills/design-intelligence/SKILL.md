---
name: design-intelligence
description: Research authoritative UX/UI evidence and compare tailored visual, interaction, accessibility and workflow options for authorized personal projects.
---

# Evidence-led UX/UI design

1. Identify the trust domain and ownership first. For personal work, resolve active personal project rules. For authorized employer work, **suggest** evidence-backed public patterns and general reusable personal lessons, explicitly marking where each came from; company design policy and access controls still take precedence. No copying another employer's design system, company assets or Moatt-specific preferences into company rules. Use the read-only `--advisory-for-employer` mode with a non-confidential task when no company pack exists.
2. Read the product's existing design system, user flows, sketches and actual screens. Preserve identity where it is working. Use a credible **public** evidence source only for the relevant problem, not to copy branding, Figma files or restricted assets.
3. Look up `knowledge/sources/catalog.json`; for alternatives run `python3 bin/ai-intelligence suggest --workspace <repo> --project <id> --domain design --task "<specific design challenge>"` from the canonical config repo.
4. Compare 2–3 genuinely different viable patterns for substantial decisions: first-use task clarity, visual hierarchy, navigation, status and errors, responsive/touch behavior, accessibility and emotional fit. For trivial changes, use the existing component consistently and move on.
5. Never proclaim one option universally best. Show who it serves, why it fits the specific product, what it sacrifices, what evidence is still missing, and a small test/measurement plan. Treat usability heuristics as guidance, not proof that users prefer the option.
6. Prototype independently; evaluate real screenshots **and** interactive task flow. Test keyboard/focus, error/empty/loading states, undo/recovery, small screens and relevant accessibility criteria.
7. Turn anonymized findings into `no change / project lesson / category rule proposal / shared principle`; use the human-reviewed `bin/ai-lessons` proposal workflow. No auto-activation.
8. Write final release notes for nontechnical readers in everyday language. Evidence details belong in the separate engineering report.

## Design learning categories
Visual foundations, typography, identity, information architecture, navigation, forms, commerce, dashboards, mobile, complex editing and 3D viewport gestures, accessible interaction, feedback and motion.

Use official W3C standards for accessibility checks; research-led NN/g/Baymard for usability hypotheses; Apple HIG/Material/Carbon/Atlassian/GOV.UK for platform or component examples. Read only what is relevant; verify dates, licensing, real product constraints and user outcomes. Never pass off a screen mockup as a validated UX study.
