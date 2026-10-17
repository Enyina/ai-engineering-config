# Moatt project overlay (private personal planning only)

Project: https://github.com/Enyina/moatt (public source)
Audience: casual creators first; progressively expose professional garment construction.

Priority: prove a reliable usable slice (select garment, customize fit/material, edit independent front/back designs, save/reopen/export) before expensive cloth physics or speculative AI features.

Benchmarks: CLO 3D for 2D/3D construction, Tailornova for garment customization, Canva for layer tooling and UX, Pacdora for presentation, Printful for printing workflows, Browzwear for advanced fit.

Required regression: drawing on garment should never orbit camera; changing side should not overwrite other side; save/reload should reconstruct identical design; exported results must not overpromise production accuracy.

Current repo has an initial prototype committed 2026-10-17, **not build-tested or production-verified**. Reconcile any earlier local Moatt project before replacing code. See project docs/ROADMAP.md.

Future design decisions must reference core + category rules, then add project-specific restrictions here only when justified by evidence.

## Usability release gate (2026-10-17)

Moatt source of truth: `https://github.com/Enyina/moatt/blob/main/docs/PRODUCT-TO-USABLE.md`.

A successful first complete experience: pick T-shirt/hoodie and mannequin preset, edit shape/color, position multiple front/back text/image/brush layers, see accurate 2D and 3D preview, undo/redo, autosave, reload/import, and export design plus mockup with clear limitations. Keyboard/touch accessibility, build/tests and browser e2e verification are mandatory.

Work through dependency phases without asking the owner for approval at interim checkpoints. Only request hands-on owner acceptance after all objective release gates are met. If external code or execution environments are unavailable, document that blocker and do not misrepresent progress as tested or finished.

Promote lessons by evidence and scope: shared, 3D editor, or Moatt-only. Do not turn specialized garment rules into global constraints or leak private/company materials into public Moatt files.
