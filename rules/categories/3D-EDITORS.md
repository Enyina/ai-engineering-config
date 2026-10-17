# 3D / garment editor category rules

Scope: products with 3D viewports and editable 2D surfaces; **not** a global requirement for APIs or backend projects.

- Keep design document authoritative; render 2D and 3D as derived representations. Version document schemas, and test migrations plus save/reload.
- Define tool modes (select, orbit, draw, erase, pan) with ownership of pointer capture. Only one gesture interpretation may mutate per pointer sequence.
- Separate front/back surfaces and layer identities. Verify image/texture orientation, normals, wrapping and color-space consistency.
- Treat stylized/approximate geometry as a preview; never describe it as validated tailoring, fit simulation or production-grade patterns.
- Use explicit texture/resource lifecycle management to avoid GPU leaks during edits; measure response time and memory under sustained painting.
- Reference established interactive editor patterns and construction tools, but implement with our own source and properly licensed assets.
- Test pointer interactions on touch and mouse, mobile WebGL fallback, undo/redo, export/import fidelity and object disposal.

First motivating project: Moatt, 2026-10-17. Rules should be tested and refined, not assumed already validated.

## Validated Moatt learning — 2026-10-17

**Reuse WebGL GPU textures during interactive editing.** When a user changes drawing layers, fabric colors or garment settings frequently, keep a stable `CanvasTexture` per garment surface and update its canvas contents. Do not allocate a fresh GPU texture on every keystroke or color change; dispose textures only when the surface actually unmounts. Before promotion, measure renderer resource counts during sustained edits and compare against a baseline.

Evidence: Moatt run 39028527243 tested repeated fabric/silhouette changes in desktop and mobile Chromium. Renderer texture count remained 2 → 2 and geometry count remained 4 → 4 across edits after the change to persistent side textures. This verifies that scenario, not every possible browser or asset.

**Review screenshots, not merely WebGL canvas presence.** A canvas can render successfully while a mannequin faces sideways, passes through the garment, or appears wildly oversized. Capture reference viewpoints, inspect visual proportions and outfit visibility, and retain screenshots with the test artifacts.
