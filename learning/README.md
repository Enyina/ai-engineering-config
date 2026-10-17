# Extensible learning pipelines (initial implementation)

This module extends, and does not override, [the learning protocol](../rules/LEARNING-PROTOCOL.md).

## First executable slice
Run `python3 learning/router.py 'https://youtu.be/example'` to classify and route a source.
Run `python3 -m unittest discover -s tests -v` for regression tests.

The registry declares seven initial pipelines. **Registered does not mean implemented.**
The router is functional but **does not watch videos, execute code, use Gemini, install Claude Watch, generate skills, or auto-modify rules**. A new input not handled by the registry produces a structured capability-gap proposal. Do not claim end-to-end media ingestion is working.

## Planned execution contract
Each pipeline must support: versioned manifest; allowed inputs and outputs; evidence bundle with provenance and timestamps; permission and cost constraints; isolated adapters; idempotent runs; quality/security tests; human-readable findings; rollback and evaluation metrics.

Video-to-Skill should prefer accessible captions/transcripts, then locally extracted frames/audio with ffmpeg and transcription if needed, and optionally a user-provided Gemini API key. Inspect third-party licenses and scripts before adopting Claude Watch. Video platform access and rights restrictions must be respected. Preserve source claims separately from verified behavior.

## Autonomous discovery governance
Route known source types first; compose existing pipelines if possible. Unknown types produce proposals only. Research evidence, implement isolated adapters, validate against fixtures, and review security/quality before registering new default capabilities. Promote verified reusable lessons using the existing learning protocol. Company repositories require separate authorization; never ingest secrets.

## Follow-on slices
1. Add media ingestion adapters, timestamps and evidence packaging.
2. Add pipeline composer and JSON-schema manifest checks.
3. Add fixture-based evaluations, costs and security gates.
4. Add candidate-generator in a sandbox with approval-gated promotion.
5. Wire an opt-in local project adapter for Codex and Claude Code.
