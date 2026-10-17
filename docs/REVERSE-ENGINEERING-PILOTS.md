# Reverse-engineering pilot briefs (reference-driven, not implementation proof)

## Pilot A — Moatt: independent 2D garment editing with 3D mannequin preview

**Owner domain:** personal. **Actual repository:** `Enyina/moatt`. This brief does not represent a browser test or source patch.

### Problem and outcomes
Allow a user to edit a front/back design using text, image and drawing tools, immediately see the appropriate mannequin surface, undo/redo, save and reopen, and export a mockup. Distinguish a visual mockup from validated manufacturing patterns or true cloth fit.

### Authorized references
- [CLO 3D official Modes](https://support.clo3d.com/hc/en-us/articles/115000297567-Modes): 2D pattern editing and 3D garment/pose interactions are distinct concepts in its simulation workflow. Reference for separation of editing surfaces and 3D preview, **not** for copying underlying simulation internals.
- [CLO Simulation](https://support.clo3d.com/hc/en-us/articles/53856382869657-Simulation): CLO draping is a separate physical-simulation behavior. Do not claim Moatt has this without actual fit data and tested simulation.
- [CLO 3D Arrangement](https://support.clo3d.com/hc/en-us/sections/115000641628-Pattern-3D-Arrangement): known 3D garment arrangement mechanisms and camera/object interaction vocabulary.

### Comparison / decisions
| Problem | Observed reference | Independent Moatt implementation choice | Proof needed |
| --- | --- | --- | --- |
| Editing versus preview | CLO separates 2D editing and 3D display | Canonical design document with two surface IDs and derived WebGL material preview | Edit front and verify back remains unchanged |
| Input conflicts | 2D pattern and 3D tools have different modes | `select / draw / erase / pan / orbit` explicit gesture ownership | No camera orbit during drawing |
| Fidelity claims | CLO runs simulated draping | Moatt labels texture/material previews, not engineering-grade garment fit | Visible export disclaimer |
| Persistence | Reference demonstrates separate editable design concepts | Serializable layers, revisions, undo history; idempotent save/reopen | Deterministic round-trip test |

### Implementation brief
Audit current Moatt repo first. Build a canonical design document for garment/material/front/back/layer positions; isolate tools by active mode; map UV/surface IDs explicitly; debounce autosave; verify race and stale loads; add screenshot diff and pointer tests. Use original assets. Verify on desktop/touch and export fidelity. **No code changes or browser execution claimed here.**

## Pilot B — Game lab: original Time Arena slow-motion mechanic

**Owner domain:** personal. **Proposed repo:** `Enyina/game-reverse-engineering-lab` (not yet verified accessible at time of writing).

### Problem and outcomes
Build an original compact 3D action arena where movement, one opponent, directional attack and temporary slow-motion feel predictable. Measure input latency and stable frame time.

### Authorized reference
- [Godot Engine time_scale documentation](https://docs.godotengine.org/en/4.4/classes/class_engine.html): engine time scale modifies simulations using delta; has implications for timers/physics, does not scale audio playback automatically, and values at zero can behave unexpectedly. This is official documented API behavior, not a claim of playing a comparable commercial game.

### Independent design
- Start with normal speed 1.0; on time-action use a bounded slowdown (for example 0.35) with a fixed time limit and recovery interpolation; keep player input responsive.
- Avoid global time_scale if the player must remain at normal speed while enemies slow; instead implement per-entity simulation clocks with explicit clock domains. Begin with the simpler global slow-time vertical slice, document limitations, then compare with a local-time prototype before choosing.
- Do not use a copied commercial game controller or ripped assets. Ensure paused/restarted state fully resets scale, cooldown, animation and audio properties.

### Acceptance
Automated: timer/cooldown transitions, input action idempotency, state cleanup on restart, enemy response under slow-time, no NaN/unbounded velocities. CI: headless Godot import and unit script tests. Manual Mac M1: play 10 minutes, verify keyboard/controller mapping and movement/camera coexistence, measure frame-time distribution. **Not yet implemented or tested on user hardware.**

## Transferable lesson candidate
Observation from product research: interactive viewports benefit from explicit interaction modes; not a global backend rule. Scope to 3D editor category; only promote to shared scope if additional non-editor evidence justifies it. Existing `rules/categories/3D-EDITORS.md` documents this as a proposed principle.
