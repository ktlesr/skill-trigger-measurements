# impeccable 4.5.2 — four axes, re-measured for pbakaus/impeccable#744

Requested by @pbakaus on 2026-10-15: re-run the same pinned case set against
4.5.2 in both permission modes, and say whether the path failures and the
craft-floor gap are closed. Measured 2026-10-17.

**Short answer.** The path failures are closed. The PowerShell quoting failure
is not: every PowerShell call without the `&` call operator failed, and every
call with it reached the engine. The craft-floor gap is closed only where the
launcher runs (bypassPermissions, 9/17). Under acceptEdits the launcher is
refused, #756's fallback message now fires almost every time, and then
craft-floor.md is read before a UI edit in **0 of 21** activations. The
fallback's "follow applicable steps 2–3" doesn't happen. `document.md` has now
gone unopened in 960 measured attempts.

## Method

| | |
| --- | --- |
| Subject | `impeccable` 4.5.2, marketplace pinned to tag `skill-v4.5.2` (`d631a88`), `skillHash sha256:cd56611e…` |
| Baseline | `impeccable` 4.2.2 (`skillHash sha256:d33f1488…`), **re-measured in the same session under the same instrument** |
| Suite | `suites/impeccable.suite.yaml`, `sha256:c820aafc…`, byte-identical to every earlier run: 12 cases (5 positive incl. the completion case, 7 negative) |
| Model | `claude-haiku-4-5-20251001` |
| Host | Claude Code **2.1.302** (from each record's `environment.version`) |
| Runner | `@ktlsr/assay@0.5.0`; `contextHash` recorded, host memory "none loaded" in every record |
| Attempts | 120 per version per mode = 480. Chunks of 12, interleaved round-robin across the four cells, so time-of-day drift lands on all of them |
| Engines | 0.1.14 (4.5.2) and 0.1.3 (4.2.2), both pre-cached, sha256-verified against the release sidecars |

**Why a re-baseline.** Since the 2026-09-08 measurement the runner moved
0.2.0 → 0.5.0, the host moved to 2.1.302, and a host-context leak
(`~/.claude/CLAUDE.md` reaching attempts through `%TEMP%`) was removed. On the
new host both versions activate less often (below), so comparing 4.5.2 against
the old 4.2.2 numbers would charge the skill for the host. **The attributable
delta is 4.2.2-rebase → 4.5.2.** The 4.2.1 and old 4.2.2 columns are history,
measured on a different host.

**Instrument validation.** `tools/four_axes.py` was re-run on the stored 4.2.1
and 4.2.2 records before any 4.5.2 number was read. It reproduces every
published figure except one reclassification, added for this run: refusals
whose text is the host's PowerShell pre-parse ("Command contains malformed
syntax that cannot be parsed") are now split out from permission refusals. On
the old records that moves 5 of 55 (4.2.1) and 3 of 36 (4.2.2) acceptEdits
refusals into the new class. All 8 are `Unexpected token 'context'`, which is
the quoting defect showing up as a refusal. On this host the PowerShell errors
come back in Turkish (tr-TR locale), so the parser and not-found classes also
match the Turkish texts.

Run records: `reports/impeccable.{4.5.2,4.2.2-rebase}.{acceptEdits,bypassPermissions}.ledger.tsv`.
Full analyser output: [impeccable.4.5.2.axes.txt](impeccable.4.5.2.axes.txt).

## Axis 1 — activation

Fired / 10. aE = acceptEdits, bP = bypassPermissions. The two right-hand columns
of each mode are the comparable pair.

| Case | 4.2.1 aE | 4.2.2 aE | **4.2.2r aE** | **4.5.2 aE** | 4.2.1 bP | 4.2.2 bP | **4.2.2r bP** | **4.5.2 bP** |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| hero_direction | 10 | 10 | 9 | 10 | 9 | 9 | 7 | 10 |
| forgettable_usage | 10 | 10 | 10 | 10 | 10 | 10 | 9 | 9 |
| settings_rework | 6 | 7 | 0 | 2 | 8 | 6 | 0 | 1 |
| empty_state | 2 | 5 | 0 | 0 | 3 | 7 | 1 | 0 |
| complete.persists_design_system | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| recall | 56% | 64% | 38% | 44% | 60% | 64% | 35% | 41% |
| false positives (70 negatives) | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |

- **4.2.2 → 4.5.2 on the same host: no change.** Recall 38 → 44% (aE) and
  35 → 41% (bP). Both intervals overlap almost entirely. Precision is 100% in
  every cell, with 0 false positives in 280 negative attempts.
- **The host moved activation, not the skill.** `settings_rework` and
  `empty_state` fell from 6–8 and 2–7 of 10 to 0–2 of 10 for both versions.
  The host's built-in `design` skill never fired in 480 attempts, so it is not
  the competitor here. The built-in `run` skill fired in 19–22 attempts per
  cell, mostly in the same attempts as impeccable. It also fired on `empty_state` (3–5 per cell),
  where impeccable fired 0–1 times. That matters for #375, not for this
  comparison.

## Axis 2 — launcher path and execution

Every shell call that names the launcher, by outcome.

| | 4.2.1 bP | 4.2.2 bP | **4.2.2r bP** | **4.5.2 bP** |
| --- | ---: | ---: | ---: | ---: |
| launcher calls | 57 | 56 | 26 | 36 |
| ran (engine answered) | 42 | 46 | 24 | 28 + 2¹ |
| resolved the plugin root (wrong base) | **11** | **1** | **0** | **2** |
| failed: path does not exist | 9 | 1 | 0 | 1 |
| failed: PowerShell parser / quoting | **6** | **4** | **2** | **4** |
| failed: host Git bash broken | 0 | 5 | 0 | 0 |
| failed: agent wrote `cd /d` in bash² | — | — | 0 | 1 |

¹ `NO_PRODUCT_MD` (concept-seed before init) and `"init" is not a CLI command`:
the engine ran and declined. Not launcher failures.
² The launcher was never reached. Recorded so the column adds up.

| | 4.2.1 aE | 4.2.2 aE | **4.2.2r aE** | **4.5.2 aE** |
| --- | ---: | ---: | ---: | ---: |
| launcher calls | 55 | 36 | 23 | 23 |
| refused by the permission layer | 50 | 33 | 19 | 20 |
| refused at host pre-parse | 5 (quoting) | 3 (quoting) | 4 (cmd line too long) | 3 (cmd line too long) |
| resolved the plugin root | 8 | 3 | 2 | **0** |

**Path: closed.** Wrong-base resolution was 11/57 → 1/56 → 2/36 in
bypassPermissions and 2/23 → 0/23 under acceptEdits. That is noise around
zero; #750's wording holds on 4.5.2.

**Quoting: open, and the rule is exact.** Every PowerShell launcher call in the
two bypassPermissions cells:

| | without `&` | with `&` |
| --- | --- | --- |
| 4.2.2r bP | 2 / 2 failed (parser) | 2 / 2 ran |
| 4.5.2 bP | **4 / 4 failed** (parser) | 2 / 3 ran (the third used the plugin root) |

The error is always `Unexpected token 'context'` (here `İfade veya deyimde
'context' belirteci beklenmiyordu`). A quoted path followed by arguments is a
string expression to PowerShell, not a command. SKILL.md still says
`"${CLAUDE_SKILL_DIR}/scripts/impeccable.cmd"` with no `&`. One sentence would
close it, for example: "In PowerShell, prefix the quoted path with the call
operator: `& "…/impeccable.cmd" context`."

New on host 2.1.302, and not the skill's fault: under acceptEdits the
PowerShell pre-parse itself fails with "The command line is too long" on 3–4
launcher calls per cell, for both versions alike.

## Axis 3 — command-reference reads

bypassPermissions only. Under acceptEdits no attempt in any version read a
reference file. No read was refused either: none was attempted.

| | 4.2.1 bP | 4.2.2 bP | **4.2.2r bP** | **4.5.2 bP** |
| --- | ---: | ---: | ---: | ---: |
| distinct reference files | 7 | 5 | 6 | 7 |
| total reads | 29 | 42 | 19 | 27 |

4.5.2 bP, file × case:

| Reference | Reads | Cases |
| --- | ---: | --- |
| craft-floor.md | 9 | hero_direction 4, forgettable_usage 4, settings_rework 1 |
| new-work.md | 8 | forgettable_usage 5, hero_direction 3 |
| init.md | 5 | hero_direction 4, forgettable_usage 1 |
| mode-operate.md | 2 | forgettable_usage 2 (new in 4.5.x) |
| mode-persuade.md | 1 | hero_direction 1 (new in 4.5.x) |
| shape.md | 1 | forgettable_usage 1 |
| operate.md | 1 | forgettable_usage 1 |

4.2.2r bP for comparison: craft-floor 6, init 4, new-work 4, delight 2,
bolder 2, onboard 1. The routing still goes where the Commands table points.
The new `mode-*.md` files are being reached. Breadth is about the same (6 → 7
distinct files), and 30+ references are still never opened. `layout.md`, the
Commands-table entry for `settings_rework`, was opened 0 times in both cells,
but that case barely fires on this host, so the zero says nothing about routing.

## Axis 4 — craft-floor before a UI edit

| | 4.2.1 | 4.2.2 | **4.2.2r** | **4.5.2** |
| --- | --- | --- | --- | --- |
| bP: read craft-floor before the first UI edit | 6 / 29 (21%) | 16 / 30 (53%) | **6 / 14 (43%)** | **9 / 17 (53%, CI 31–74%)** |
| aE: read craft-floor before the first UI edit | 0 / 28 | 0 / 32 | **0 / 18** | **0 / 21** (CI 0–15%) |
| read it only after the first edit | 0 | 0 | 0 | 0 |

**Where the launcher runs, the gap is where 4.2.2 left it.** 43% → 53% is
inside noise at N=14/17. The 21% → 53% jump came with 4.2.2 (#750) and has held.

**Where the launcher is refused, the gap is total, and #756 doesn't reach
it.** Under acceptEdits:

| #756 fallback, per activation whose every launcher call failed | 4.2.2r aE | 4.5.2 aE |
| --- | ---: | ---: |
| activations with every launcher call failed | 19 | 21 |
| told the user | 10 | 17 |
| …in a message before the next tool call | 5 | **16** |
| …said it *before* even calling the launcher | 10 | 4 |
| …with the fixed 4.5.2 sentence ("Context loading did not run") | 0 | **21** |
| then edited UI | 18 | 21 |
| …and read craft-floor.md before that edit | **0** | **0** |

The message half of #756 works. The fixed sentence appears in 21/21
activations, and 16 of them place it correctly. The "follow applicable steps
2–3" half doesn't happen: after saying "I'll read the existing project context
directly", the agent reads the project files and starts editing. It never
opens a single file under `reference/`. A guess, not measured: the fallback
sentence names *project* context, and nothing in the fallback paragraph points
at `reference/craft-floor.md` by path, so once the launcher fails nothing
connects the next step to the skill's own files.

## Completion case — for #375, not pooled into the routing numbers

`complete.persists_design_system` (a request phrased like the `document`
command's job, without naming it):

| | 4.2.1 aE | 4.2.1 bP | 4.2.2 aE | 4.2.2 bP | 4.2.2r aE | 4.2.2r bP | 4.5.2 aE | 4.5.2 bP |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| skill fired | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| wrote a DESIGN.md anyway | 10 | 9 | 10 | 6 | 8 | 10 | 9 | 8 |
| opened `reference/document.md` | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |

80 attempts on this case, 0 activations. The base model writes the file
itself, 70 times out of 80. `document.md` has never been opened in any of the
**960** measured attempts: three versions (4.2.2 measured twice), two hosts
and two modes. This
case and its 80 attempts are for #375.

## Limitations

- N=10 per case. Per-case differences of 1–2 are noise; the Wilson intervals
  are in the axes file.
- One host, Windows 11 tr-TR. The quoting failure is a PowerShell parser rule,
  not a locale effect, but the error text is localised.
- Claude Code reaped the background driver twice for low system memory. Those
  chunks were discarded whole and re-run. Only complete exit-0 chunks are
  counted, and the 4 interrupted journals were not recovered into the record.
- The record's `skillSource` field comes from the suite file's `target.source`
  (the 4.2.1 commit) and identifies nothing. Use `skillHash`.
- 4.6.0 was released 8 hours after the request and is not measured here.
