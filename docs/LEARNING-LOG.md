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


## 2026-10-17 — Separate unit and browser test discovery
Scope: shared/core
Status: validated by Moatt CI
Observed: Vitest automatically collected Playwright's `e2e/*.spec.ts` and failed before normal unit execution. A dedicated `vitest.config.ts` restricting discovery to unit tests resolved it.
Rule: When one repository uses multiple testing frameworks, configure mutually exclusive file globs and run each suite independently in CI. Never infer one framework will ignore another's test files.
Verification: Typecheck, five unit tests, production build and Playwright suites run as separate jobs/steps.
References: Moatt commits `de05d907` and the CI workflow.

## 2026-10-17 — Device-accurate interaction automation
Scope: category/web-product and 3D editor
Status: validated by Moatt browser runs
Observed: A mobile-emulated viewport required scrolling to the canvas and testing touch gestures instead of assuming desktop mouse coordinates worked on-screen. An unscoped Back locator also collided with a Send backward layer command.
Rule: In responsive UI acceptance tests, use visible-viewport scroll handling, device-appropriate input methods, and unambiguous accessible names/locators. Verify end-user outcomes, not just element presence.
Verification: Latest desktop/mobile Chromium Playwright suite passed 10 scenarios.
References: Moatt CI success `39025853488`.

## 2026-10-17 — Preview fidelity versus production fidelity
Scope: category (3D/web product)
Status: proposed; production-fidelity tests still pending
Observed: Moatt's initial flat rectangular 3D placeholder lacked a recognizable garment outline. A garment-shaped, UV-mapped preview improves silhouette fidelity, but remains distinct from verified print placement or physically accurate cloth construction.
Rule candidate: In visual configuration products, label the accuracy tier of every representation (conceptual mockup, visual approximation, calibrated manufacturing output). Never treat successful smoke tests or successful WebGL rendering as proof of real-world fidelity.
Verification needed before promotion: side-by-side screenshot reviews and measurements against calibrated outputs, plus memory/performance tests.
Reference: Enyina/moatt commit 1871598b, CI 39026492744.

## 2026-10-17 — Preserve backward compatibility in editable design schemas
Scope: shared/core + 3D editor category
Status: validated by Moatt versioned-document unit tests
Observed: Moatt added optional hem, sleeve and neck editing fields while existing saved v2 designs lacked those properties.
Rule: When extending a persisted project/document schema, supply deterministic defaults or migrations, and test round-trip serialization plus restoration of older versions before relying on the new fields in rendering.
Verification: Tests in Moatt's `tests/document.test.ts` and successful CI run 39026997451.
Reference: Moatt commit a2434262 and follow-up renderer/UI commits.

## 2026-10-17 — Asset acquisition must be independently verified
Scope: shared/core
Status: proposed
Observed: Publicly described CC0 3D mannequin assets were discoverable, but the connected repository interface could not retrieve/write binary GLB content. A license statement and download listing are not equivalent to an installed, verified asset.
Rule: Before claiming a third-party asset integration, verify permission/license, exact asset bytes/provenance, stable bundling, runtime loading, orientation/scale and fallback behavior. Record blockers explicitly; never substitute a live third-party CDN dependency without reliability and licensing review.
Verification: imported binary exists in the release tree and automated loading/visual smoke checks pass.
