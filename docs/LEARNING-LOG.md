# Learning log

## 2026-10-17 — Moatt editor rule scoping
Scope: category (3D editing) + project
Status: proposed — code-level regression not yet validated
Observed: Earlier Moatt discussion described the draw tool rotating a mannequin, rather than painting the clothing. The currently connected remote repo began as an empty scaffold, and the latest prototype has not been run/tested.
Cause (hypothesis): pointer/OrbitControls event ownership may conflict with drawing interaction.
Rule: When adding drawing to an orbitable 3D viewport, explicitly switch input modes and disable conflicting camera interactions; add a regression test covering drag-to-draw and drag-to-orbit.
Verification: replay pointer gestures on front/back garment sides, verify no unintended camera change, and exercise touch and mouse.
References: rules/categories/3D-EDITORS.md and Moatt docs/ROADMAP.md.

## 2026-10-17 — Verify status before reporting completion
Scope: shared/core
Status: validated as reporting policy, not a code test
Observed: Remote commits can succeed even when build and browser verification have not been performed.
Rule: Report separate states for created, committed, typechecked, built, browser-tested and deployed.
Verification: Every delivery summary includes performed checks and unverified checks.
References: rules/CORE-ENGINEERING.md.
