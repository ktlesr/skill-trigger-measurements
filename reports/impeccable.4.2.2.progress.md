# 4.2.2 measurement — progress record

**Purpose:** resumable state for the impeccable 4.2.2 run requested in
pbakaus/impeccable#744. If the session resets, continue from here; do not
restart from zero.

## Pins (must not change mid-run)

| | |
| --- | --- |
| Skill | `impeccable` 4.2.2, clean marketplace install |
| Suite | `suites/impeccable.suite.yaml` v1, `sha256:c820aafc…` (must stay identical to 4.2.1) |
| Model | `claude-haiku-4-5-20251001` |
| Runner | `npx @ktlsr/assay@0.2.0` — DO NOT CHANGE, tool must stay constant |
| Modes | `acceptEdits` and `bypassPermissions` (the latter is an instrument, not advice) |
| Attempts | 120 per mode, in chunks (orphan dev-server mitigation) |

## Status

- [ ] Phase 0 — install 4.2.2, record hashes, diff vs 4.2.1
- [ ] Phase 1 — acceptEdits, 120 attempts
- [ ] Phase 2 — bypassPermissions, 120 attempts
- [ ] Phase 3 — analysis (4 separate axes + document case)
- [ ] Phase 4 — reports/impeccable.4.2.2.md + #744 comment draft

## Chunk ledger

| Mode | Chunk | Attempts | Record file | State |
| --- | --- | --- | --- | --- |
| — | — | — | — | not started |

## Open problems

- none recorded yet
