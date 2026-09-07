# `impeccable` — the launcher-approved run

The [main measurement](impeccable.md) was made under `--permission-mode
acceptEdits`, where all 55 launcher invocations were refused. That left one
question open, and it was the important one: **are findings 1 and 2 consequences
of finding 3, or independent of it?**

This run answers it. Same suite, same skill, same model, same case set hash —
only the permission mode changes.

| | |
| --- | --- |
| Skill | `impeccable` 4.2.1, `pbakaus/impeccable@831cabee8b4bc1a2b66e5ae22003e9a19b57d464` |
| Skill content hash | `sha256:c3185df7833a43644cc5756c802358f9345d41e353fb6166381026b6c5ca8cfd` |
| Suite | `suites/impeccable.suite.yaml` v1, `sha256:c820aafc…` — **identical to the `acceptEdits` run** |
| Model | `claude-haiku-4-5-20251001` |
| Host | `claude-code` 2.1.263, Windows 11 Pro 10.0.26200 |
| Runner | `@ktlsr/assay@0.2.0`, `--permission-mode bypassPermissions --allow-bypass-permissions` |
| Environment hash | `sha256:c8038f22…` (vs `sha256:1491f2d9…` for `acceptEdits` — the mode is folded in) |
| Attempts | 120, across 5 records of 24 — see *Why five records* |
| Cost | $12.86 · 124.1 min · 1,402 tool calls |

**The headline: finding 1 is independent and stands. Finding 2 was largely a
consequence of finding 3, and is downgraded but not closed.**

---

## Answers to the four questions

### 1. Are `init.md` and `new-work.md` really read? — Yes, confirmed

The N=2 probe signal holds at N=30 activations, though the proportions differ
from what two attempts suggested.

| File | Reads | Cases |
| --- | --- | --- |
| `new-work.md` | 12 | `hero_direction`, `forgettable_usage` |
| `init.md` | 3 | `hero_direction`, `forgettable_usage` |

`new-work.md` is the workhorse; `init.md` is uncommon — 3 reads across 30
activations, not the every-time step the probe implied.

### 2. Is `craft-floor.md` still skipped while UI is edited? — Refuted in absolute terms, survives in weakened form

The probe saw 0 reads and I flagged that as the part of finding 2 that survived
the launcher being approved. **That was too strong: it is read, 6 times.**

But the finding it was pointing at does not go away:

| | `acceptEdits` | `bypassPermissions` |
| --- | --- | --- |
| activations | 28 | 30 |
| of which edited UI | 28 | 29 |
| of those, opened `craft-floor.md` first | **0** | **6** |

`SKILL.md` step 3 calls `craft-floor.md` the quality floor and the absolute bans,
and says to load it *immediately before editing UI*. **23 of the 29 UI-editing
activations still did not.** The rate moved from 0% to 21%; it did not become
the reflex the instruction describes.

### 3. Is `document.md` read in the completion case? — No, still zero

Not read once, in any attempt. The completion case opened **no reference file at
all**, under either permission mode. The 27,844 bytes specifying the DESIGN.md
format, its token schema and its section order remain unreached.

### 4. Does the completion case trigger now? — No. Still 0/10

| | `acceptEdits` | `bypassPermissions` |
| --- | --- | --- |
| activations | 0/10 | **0/10** |
| `DESIGN.md` written | 10/10 | 9/10 |

Identical. Not one of the twenty attempts across both modes reached for the
skill, and nineteen of them wrote the artefact anyway.

---

## The comparison

`assay compare` **refuses** these two runs, correctly, with exit 3 — so the
table below is assembled by hand from the stored records.

```
cannot compare these runs
the runs are not comparable: systemPromptHash changed between them;
systemPromptHash could not be read in one or both runs, so the conditions
cannot be shown to match
```

A note on that message, because it names the wrong field. Every pin in the two
runs is byte-identical **except** `environmentHash`; `systemPromptHash` is
`not-provided-by-host` in both. The control settles it: two runs with matching
environment hashes and the same unreadable `systemPromptHash` compare fine, exit
0. So the environment hash is what blocks the comparison — which is right, since
the permission mode belongs in it — but the diagnostic misattributes the cause.

| | `acceptEdits` | `bypassPermissions` | |
| --- | --- | --- | --- |
| attempts | 120 | 120 | |
| cost / wall time | $8.11 · 90.9 min | $12.86 · 124.1 min | |
| tool calls | 964 | 1,402 | |
| **launcher attempted** | 55 | 57 | |
| **refused by the permission layer** | **55** | **0** | ← the mode change |
| **executed** | **0** | **42** | |
| failed for the skill's own reasons | 0 | 15 | see below |
| activations | 28 | 30 | |
| precision | 100% (N=28, 88%–100%) | 100% (N=30, 89%–100%) | unchanged |
| recall | 56% (N=50, 42%–69%) | 60% (N=50, 46%–72%) | within noise |
| false positives | 0 / 70 | 0 / 70 | unchanged |
| distinct reference files read | **0 of 35** | **7 of 35** | |
| total reference reads | 0 (1 attempted, refused) | 29 | |
| `craft-floor.md` / UI-editing activations | 0 / 28 | 6 / 29 | |
| completion case fired | 0/10 | 0/10 | unchanged |
| completion `DESIGN.md` | 10/10 | 9/10 | |

Per case:

| Case | `acceptEdits` | `bypassPermissions` |
| --- | --- | --- |
| `trigger.positive.hero_direction` | 10/10 | 9/10 |
| `trigger.positive.settings_rework` | 6/10 | 8/10 |
| `trigger.positive.forgettable_usage` | 10/10 | 10/10 |
| `trigger.positive.empty_state` | 2/10 | 3/10 |
| all seven negatives | 0/10 each | 0/10 each |
| `complete.persists_design_system` | 0/10 | 0/10 |

No per-case difference clears its confidence interval. Routing is not what the
permission mode changes.

---

## Which finding closed, which stood

**Finding 1 — the completion case — is independent of finding 3, and stands
entirely.** 0/10 activations under both modes. This was never a permission
result: the skill is not reached, so whether its launcher would have worked is
beside the point. With the launcher fully permitted, the base model still
produces `DESIGN.md` at the documented path without the skill, without
`document.md`, 9 times in 10.

**Finding 2 — the 35 reference files — was largely a consequence of finding 3,
and is downgraded rather than closed.** 0 → 7 distinct files, 0 → 29 reads. The
"none of them are read" claim does not survive a working launcher, and the
report and issue should be read with that correction. What survives is narrower
and still real:

- 28 of 35 reference files are never opened, in 120 attempts.
- `craft-floor.md`, which the skill mandates before every UI edit, is loaded
  before 6 of 29 such edits.
- `document.md` is never opened, including in the one case written to invoke it.

**Finding 3 — the launcher — is a permission-layer result, and it inverts
cleanly.** 55 of 55 refused becomes 0 of 57 refused. The launcher works.

**Finding 4 — the `<skill-base-dir>` ambiguity — is upgraded from cosmetic to
real.** Under `acceptEdits` I wrote that the 8 mis-resolved paths "cost nothing
in this run" because everything was refused anyway. With the calls permitted they
cost exactly what was predicted:

| Outcome of the 57 launcher calls | Count |
| --- | --- |
| ran | 42 |
| **failed: path does not exist** (`<plugin-root>/scripts/…` instead of `<plugin-root>/skills/impeccable/scripts/…`) | **9** |
| **failed: PowerShell `ParserError: Unexpected token 'context'`** (quoted `.cmd` path invoked without `&`) | **6** |
| refused by the permission layer | **0** |

```
Exit code 127  /usr/bin/bash: line 1: …\assay-skill-IWkden\scripts\impeccable.cmd:
               No such file or directory
Exit code 1    &: The term '…\assay-skill-IWkden\scripts\impeccable.cmd' is not
               recognized as a name of a cmdlet, function, script file…
Exit code 1    ParserError: … \scripts\impeccable.cmd" context
                            ~~~~~~~ Unexpected token 'context' in expression or statement.
```

**26% of the launcher calls fail for reasons that belong to the skill, not the
host.** That number was invisible while the permission layer was refusing
everything.

---

## Reference-file coverage

Full table: [`impeccable.launcher-approved.coverage.md`](impeccable.launcher-approved.coverage.md).

| | Files | Bytes |
| --- | --- | --- |
| ships in the skill directory | 58 | 2,150,761 |
| opened by the agent | **9** | 104,664 |
| loaded by the host on trigger (`SKILL.md`) | 1 | 11,374 |
| not observable (behind the compiled engine) | 2 | 1,102,570 |
| **never opened** | **46** | **932,153** |

Of the 35 documented reference files, **7 were read**:

| File | Reads | Reached from |
| --- | --- | --- |
| `new-work.md` | 12 | `hero_direction`, `forgettable_usage` |
| `craft-floor.md` | 6 | `hero_direction`, `forgettable_usage`, `empty_state` |
| `init.md` | 3 | `hero_direction`, `forgettable_usage` |
| `layout.md` | 3 | `settings_rework` |
| `bolder.md` | 2 | `forgettable_usage`, `hero_direction` |
| `onboard.md` | 2 | `empty_state` |
| `operate.md` | 1 | `settings_rework` |

The routing works when it runs: `layout.md` and `operate.md` for a settings
hierarchy rework, `bolder.md` for "make it memorable", `onboard.md` for an empty
state. Each is the reference its command table names. **28 of 35 were still
never reached**, among them `critique.md` (43 KB), `document.md` (28 KB),
`polish.md`, `harden.md` and every `degraded/` fallback.

---

## Why five records, not one

**A `bypassPermissions` measurement of this skill destroys its own runner, and
this is worth knowing before anyone plans one.**

Two attempts at a single 120-attempt run died at exit 255 with no error output
and no stored record — after 3 and 8 attempts respectively, both inside
`hero_direction`. The cause is in the traces. Under `bypassPermissions` the agent
actually executes what it merely attempted before:

```powershell
Get-NetTCPConnection -LocalPort 5175 | ForEach-Object {
  Stop-Process -Id (Get-Process -PID $_.OwningProcess).Id -Force
}
```

It starts dev servers to verify its work (`npm run dev`, `npx vite`) and kills
processes **by port**. Those servers outlive the attempt. Caught mid-run:

```
total node processes: 21
orphans from earlier attempts: 13
port 5173 ← node (13:10:14)      port 5176 ← node (13:14:31)
port 5173 ← node (13:21:01)      port 5177 ← node (13:33:13)
port 5174 ← node (13:12:42)      port 5178 ← node (13:36:46)
port 5175 ← node (13:13:26)      …
```

Vite climbs its port ladder because the previous attempt's server still holds the
one below. The assay runner is itself a `node` process in that same space, and a
kill-by-port eventually reaches it. Killing the 10 port owners took the count
from 21 processes to 1.

So the suite was run as **five records of `--repeat 2`**, with orphaned servers
cleared between them. The suite file is byte-identical across all five — same
`suiteHash`, same `skillHash`, same mode, same environment hash — and each
attempt is an independent session in a fresh workspace, so pooling 5 × 24 is
arithmetically the same measurement as 1 × 120. What it is not is a single run
record, so precision, recall and the per-case rates here are pooled by
`tools/` rather than read off the runner's own summary. One chunk still died and
was re-run; roughly 10 attempts and ~$2 were lost to crashes.

---

## Limitations

- **Pooled from five records.** Stated above. Identical pins, but no single
  record holds the measurement.
- **`bypassPermissions` is not a configuration anyone should ship.** It removes
  every boundary the sandbox observes. It is a diagnostic setting used here to
  isolate one variable, not a recommendation.
- **Rates are pinned to `claude-haiku-4-5-20251001`.** Recall 60% is a floor for
  this model.
- **One round of negatives.** 0 false positives in 70 attempts, in both modes.
- **The host is primed** with the impeccable engine already cached, so no attempt
  paid the first-run download. On a cold host the 42 successful launcher calls
  would have begun with a ~14 MB fetch.

## Reproduce

```
for i in 1 2 3 4 5; do
  npx @ktlsr/assay@0.2.0 run suites/impeccable.suite.yaml \
    --skill ./skills/impeccable \
    --permission-mode bypassPermissions --allow-bypass-permissions --repeat 2
  # kill orphaned dev servers on ports 5170-5210 before the next chunk
done
python tools/refcoverage.py --exec impeccable ./skills/impeccable .assay/runs/<the five>.json
```

$12.86 for the 120 attempts, plus about $2 lost to the crashed runs.

Method: <https://assayctl.dev/methodology>
