# `impeccable` 4.2.2 — what #750 fixed, and what it did not

Requested on [pbakaus/impeccable#744](https://github.com/pbakaus/impeccable/issues/744):
the same 120 attempts that produced the 4.2.1 numbers, re-run against 4.2.2, so
the effect of #750 can be read off directly. Standing offer from the previous
comment, now delivered.

**Only the skill version changed.** Same suite at the same case-set hash, same
model, same host, same measurement tool at the same pin. Changing the instrument
at the same time as the subject would have made the comparison worthless.

| | |
| --- | --- |
| Skill | `impeccable` 4.2.2, clean marketplace install (`marketplace add pbakaus/impeccable` -> `plugin install impeccable@impeccable`) into an isolated `CLAUDE_CONFIG_DIR`, vendored verbatim |
| Marketplace commit | `2bc2879276c1f321a53c4ca99d3371e411329b52` |
| Skill content hash | `sha256:5c526077…` (4.2.1 was `sha256:c3185df7…`) |
| Suite | `suites/impeccable.suite.yaml` v1, `sha256:c820aafc…` — **byte-identical to both 4.2.1 runs** |
| Model | `claude-haiku-4-5-20251001` |
| Host | `claude-code` 2.1.263, Windows 11 Pro 10.0.26200 |
| Runner | `@ktlsr/assay@0.2.0` — **unchanged from the 4.2.1 runs** |
| Attempts | 120 per permission mode, 240 total |
| Cost | $8.19 · 106.8 min (`acceptEdits`) · $12.96 · 179.0 min (`bypassPermissions`), plus ~$4 lost to two dead runs |

> **`bypassPermissions` is a measurement instrument, not a configuration
> recommendation.** It removes every boundary the sandbox observes. It is used
> here for one reason: it is the only way to hold the permission layer constant
> so that the skill's own behaviour can be separated from the host's refusals.
> Nobody should ship it.

---

## What 4.2.2 actually changes

The whole diff against 4.2.1 is five files. Three are packaging and a
production-safety note in `live.md` / `live-setup.md`. The engine pin moves
`0.1.2` -> `0.1.3`. Everything that could move a number in this report is in
`SKILL.md`, and it is three edits:

1. **`<skill-base-dir>` becomes `${CLAUDE_SKILL_DIR}`**, with the ambiguity
   spelled out — "the directory that contains this SKILL.md (the skill folder,
   not a plugin root two levels above it)". Aimed at finding 4.
2. **Step 3 hardened** — "read `reference/craft-floor.md` immediately before any
   UI edit, including small refinements". Aimed at finding 2.
3. **A new "Launcher unavailable" paragraph** — if the launcher is refused,
   missing or failed, *first tell the user*, then carry on with permitted tools.
   Aimed at the `acceptEdits` refusal path.

Each of the three is measured separately below.

---

## Headline

| Finding | 4.2.1 | 4.2.2 | Verdict |
| --- | --- | --- | --- |
| 1 — completion case never fires | 0/10 both modes | 0/10 both modes | **unchanged** |
| 2 — craft floor skipped before UI edits | 6/29 (21%) | **16/30 (53%)** | **materially improved, not closed** |
| 3 — launcher refused under `acceptEdits` | 55/55 refused | 36/36 refused | unchanged (host, not skill) |
| 4a — launcher resolves the wrong base dir | 11/57 | **1/56** | **essentially fixed** |
| 4b — launcher quoting / parser failures | 6/57 | 4/56 | **not addressed** |
| new — tells the user when the launcher fails | 3/27 (11%) | **16/27 (59%)** | new behaviour, working |
| reference *breadth* | 7 of 35 files | **5 of 35** | **regressed** |

---

## 1. Activation — which case fired, how often

Routing is not what #750 touched, and routing did not move. No per-case
difference clears its confidence interval in either direction.

| Case | 4.2.1 AE | 4.2.2 AE | 4.2.1 BP | 4.2.2 BP |
| --- | --- | --- | --- | --- |
| `trigger.positive.hero_direction` | 10/10 | 10/10 | 9/10 | 9/10 |
| `trigger.positive.forgettable_usage` | 10/10 | 10/10 | 10/10 | 10/10 |
| `trigger.positive.settings_rework` | 6/10 | 7/10 | 8/10 | 6/10 |
| `trigger.positive.empty_state` | 2/10 | 5/10 | 3/10 | 7/10 |
| all seven negatives | 0/10 each | 0/10 each | 0/10 each | 0/10 each |
| `complete.persists_design_system` | 0/10 | 0/10 | 0/10 | 0/10 |

| | 4.2.1 AE | 4.2.2 AE | 4.2.1 BP | 4.2.2 BP |
| --- | --- | --- | --- | --- |
| activations | 28 | 32 | 30 | 32 |
| precision | 100% (N=28) | 100% (N=32) | 100% (N=30) | 100% (N=32) |
| recall | 56% (42-69%) | 64% (50-76%) | 60% (46-72%) | 64% (50-76%) |
| false positives | 0 / 70 | 0 / 70 | 0 / 70 | 0 / 70 |
| unreadable trigger signals | 0 | 0 | 0 | 0 |

`empty_state` looks like it doubled (2/10 -> 5/10 under `acceptEdits`) and it is
the one worth watching, but at N=10 its interval runs 6%-51% against 24%-76%.
That is not a result. **Precision stays at 100% with zero false positives in 280
negative attempts across the four measurements**, which is the part of the
routing picture that is solid.

---

## 2. Launcher — path resolution and execution

This is the axis #750 aimed at, and it has to be read in two halves, because the
two halves behaved completely differently.

### Under `acceptEdits` — still refused, but attempted half as often

| | 4.2.1 | 4.2.2 |
| --- | --- | --- |
| invocations naming the launcher | 55 | **36** |
| calls per activation | 1.96 | **1.12** |
| refused by the permission layer | 55 (100%) | 36 (100%) |
| ran | 0 | 0 |
| resolved the base dir correctly | 47 (85%) | 33 (92%) |
| **resolved the wrong base dir** | **8 (15%)** | **3 (8%)** |

The refusal rate is a host property and did not change: the `&` call operator is
still read by the command parser as a compound command, and a bare quoted `.cmd`
still needs approval. What changed is that the model stops arguing with it — 1.12
calls per activation instead of 1.96. That is the new fallback paragraph working.

### Under `bypassPermissions` — the calls execute, so the failures are real

| Outcome | 4.2.1 | 4.2.2 |
| --- | --- | --- |
| ran | 42 | **46** |
| failed: **path does not exist** (`<plugin-root>/scripts/…`) | **9** | **1** |
| failed: **quoting / parser** (quoted `.cmd` without `&`) | **6** | **4** |
| failed: host shell broken (see caveat) | 0 | 5 |
| refused by the permission layer | 0 | 0 |
| total | 57 | 56 |
| base dir resolved wrongly | **11 (19%)** | **1 (2%)** |

**Caveat, and it matters.** This host's Git bash is intermittently broken
(`bash.exe: *** fatal error - add_item …`). It hit 11 of 390 Bash calls today
against 0 of 403 during the 4.2.1 `bypassPermissions` run, so it inflates
4.2.2's failure column for a reason that has nothing to do with the skill.
Excluding it from both sides:

| | 4.2.1 | 4.2.2 |
| --- | --- | --- |
| skill-attributable launcher calls | 57 | 51 |
| of those, failed for the skill's own reasons | **15 (26%)** | **5 (10%)** |

**Finding 4a is essentially fixed.** The mis-resolved `<plugin-root>/scripts/…`
path went from 11 of 57 calls to 1 of 56. Naming `${CLAUDE_SKILL_DIR}` and
saying in as many words that it is not the plugin root two levels up did the job.

**Finding 4b is untouched.** `ParserError: Unexpected token 'context'` — a quoted
`.cmd` path invoked without the `&` call operator — is still there at 4 calls in
56, against 6 in 57. #750 changed *which directory* the command names; it did not
change *how the command is quoted*, and that was the other half of the failure.
`SKILL.md` still says only "call `"${CLAUDE_SKILL_DIR}/scripts/impeccable.cmd"`
instead" without saying how to invoke a quoted path in PowerShell.

One more thing that has not changed: **the reference files still carry the old
`<skill-base-dir>` placeholder**. 4.2.2 works around this by instructing the
model to substitute it ("In reference files, replace the skill-base-dir
placeholder with this directory before running commands; it is not a shell
variable") rather than by fixing the reference files. No call in 240 attempts
emitted a literal unexpanded placeholder, so the instruction is holding — but it
is holding by asking the model to do a text substitution correctly every time.

---

## 3. Command-reference reads — routing is right, breadth got narrower

Under `acceptEdits`, **zero reference files are read in either version**. The
skill directory sits outside the attempt workspace, so reading it needs a
permission `acceptEdits` does not grant, and the launcher that would have loaded
them is refused. Unchanged from 4.2.1, and nothing in #750 addresses it.

Under `bypassPermissions`:

| | 4.2.1 | 4.2.2 |
| --- | --- | --- |
| distinct reference files read | **7 of 35** | **5 of 35** |
| total reference reads | 29 | **42** |
| never opened | 28 of 35 | **30 of 35** |

| File | 4.2.1 | 4.2.2 | Reached from (4.2.2) |
| --- | --- | --- | --- |
| `craft-floor.md` | 6 | **16** | all four positives |
| `new-work.md` | 12 | 14 | `hero_direction`, `forgettable_usage` |
| `onboard.md` | 2 | 7 | `empty_state` |
| `init.md` | 3 | 4 | `hero_direction`, `forgettable_usage` |
| `bolder.md` | 2 | 1 | `forgettable_usage` |
| `layout.md` | 3 | **0** | — |
| `operate.md` | 1 | **0** | — |

**Where it runs, the routing is the one the Commands table names.** `onboard.md`
for an empty state, `new-work.md` for a replacement visual world, `bolder.md` for
"make it memorable". That was true in 4.2.1 and is still true.

**But the reference tier got narrower, not wider.** Volume is up 45% (29 -> 42
reads) and that is almost entirely `craft-floor.md`. Meanwhile `settings_rework`
— the case whose command-table entry is `layout` — stopped reaching `layout.md`
and `operate.md` altogether. In 4.2.1 it read them 4 times between them; in
4.2.2, zero. Its only reference read is now `craft-floor.md`.

So step 3 got louder and step 2 got quieter. 30 of 35 documented reference files
are still never opened in 120 attempts, including `critique.md` (43 KB),
`document.md` (28 KB), `polish.md`, `harden.md` and every `degraded/` fallback.
Full table: [`impeccable.4.2.2.coverage.md`](impeccable.4.2.2.coverage.md).

---

## 4. `craft-floor.md` before a UI edit — the clearest win

`SKILL.md` step 3 was reworded from "load it immediately before editing UI" to
"read it immediately before **any** UI edit, **including small refinements**".

| | 4.2.1 | 4.2.2 |
| --- | --- | --- |
| activations that edited UI | 29 | 30 |
| **of those, read `craft-floor.md` first** | **6 (21%, 10-38%)** | **16 (53%, 36-70%)** |
| read it only after the first edit | 0 | 0 |

Per case, 4.2.2: `hero_direction` 6/8, `empty_state` 3/7, `forgettable_usage`
4/9, `settings_rework` 3/6.

21% -> 53%. The intervals barely touch, so this is a real movement rather than
noise, and it is the single clearest thing #750 bought. **It is still not the
reflex the instruction describes**: 14 of 30 UI-editing activations went ahead
without the quality floor, and the two cases that ask for a judgement inside an
existing screen (`settings_rework`, `forgettable_usage`) are the ones that skip
it most.

Under `acceptEdits` it remains 0 of 32, for the same reason as section 3: the
file cannot be read at all in that configuration.

---

## New in 4.2.2: does it tell the user when the launcher fails?

The new paragraph says: "If refused, missing, or failed, **first send the user a
message** that context loading did not run." That is a testable instruction, so
it is measured here even though it has no 4.2.1 counterpart to fix.

Of the activations under `acceptEdits` where every launcher call failed:

| | 4.2.1 | 4.2.2 |
| --- | --- | --- |
| activations where every launcher call failed | 27 | 27 |
| **of those, told the user** | **3 (11%)** | **16 (59%)** |

**Method, because this one is a text classification and not an exact count.** An
attempt counts as disclosing if, after the last failed launcher call, the agent
emits a sentence that both names the launcher/context step and says something
went wrong with it. Both negative lists were read by hand and contain no missed
disclosures; several pattern widths were tried and all gave the same shape (a
4-5x increase). Treat 59% as approximate and the direction as solid.

The other half of the instruction — carry on with permitted tools — was already
happening in 4.2.1 and still happens: every activation that edited UI did so
regardless.

---

## The `document`-shaped completion case — to be coordinated with #375

Kept separate, as agreed on the thread, because this is the activation-coverage
question rather than a #750 question.

| | 4.2.1 AE | 4.2.2 AE | 4.2.1 BP | 4.2.2 BP |
| --- | --- | --- | --- | --- |
| skill activated | **0/10** | **0/10** | **0/10** | **0/10** |
| `DESIGN.md` written anyway | 10/10 | 10/10 | 9/10 | 6/10 |
| `reference/document.md` opened | 0 | 0 | 0 | 0 |
| any reference opened | 0 | 0 | 0 | 0 |

**Nothing moved.** Forty attempts across two versions and two permission modes,
and the skill was not reached once. `document.md` — 28 KB specifying the
DESIGN.md format, its token schema and its section order — has now never been
opened in 480 measured attempts.

This was already established as independent of the launcher in the 4.2.1
launcher-approved run, and 4.2.2 confirms it is also independent of the skill
version: the base model produces the artefact the skill exists to produce, at the
path the skill documents, without the skill.

The `6/10` in the last column is the one cell that moved, and it should not be
read as a finding: 9/10 against 6/10 at N=10 is well inside noise (intervals
59-98% and 31-83%).

---

## Operational note: this measurement still destroys its own runner

Repeating the warning from the 4.2.1 report because the mitigation only half
worked. Under `bypassPermissions` the agent starts dev servers to verify its work
and then kills processes **by port**; the assay runner is a `node` process in the
same space.

The run was chunked from the start and orphans were cleared between chunks — the
cleanup caught 2, 1 and 4 orphaned servers before chunks 3, 4 and 5. **It was not
enough.** Chunk 5 died at exit -1 with no record twice in a row, once inside
`hero_direction` and once inside `forgettable_usage`, because the fatal kill
happens *inside* a chunk where nothing can intervene. It was recovered by
halving the window to two `--repeat 1` records of 12, which both survived.

Cost of this failure mode: ~40 minutes and ~$4 here, on top of the ~10 attempts
and ~$2 the 4.2.1 run lost the same way. Anyone planning this measurement should
budget for it and chunk in twelves, not twenty-fours.

---

## Limitations

- **Pooled from several records, not one run.** `acceptEdits` is 5 x 24;
  `bypassPermissions` is 4 x 24 + 2 x 12. All pins byte-identical within each
  mode, each attempt an independent session in a fresh workspace, so pooling is
  arithmetically the same measurement — but no single record holds it. The
  analysis tool refuses to pool records whose pins differ.
- **The host's Git bash is intermittently broken** and was not during the 4.2.1
  `bypassPermissions` run. Quantified above and excluded from the headline
  launcher comparison; it is a genuine confounder on the raw counts.
- **The engine pin moved 0.1.2 -> 0.1.3 with the skill version.** These are not
  separable in this design: they ship together. The host was primed with 0.1.3 by
  hand (sha256-verified against the release sidecar) so that the comparison is
  primed-host against primed-host, as the 4.2.1 runs were.
- **The launcher cannot self-download on this host.** `C:\Windows\System32` is
  not on this shell's PATH, so its `where curl.exe` probe fails and it goes to
  `:fail` with exit 127. Host property, worked around by the priming above, but
  worth knowing: the download path fails closed and silently on a PATH like this.
- **Rates are pinned to `claude-haiku-4-5-20251001`.** Recall in the low 60s is a
  floor for this model, not a universal result.
- **One round of negatives.** 0 false positives in 70 attempts per measurement
  bounds the false-positive rate; it does not show where the set's
  discriminating power ends.
- **The disclosure metric is a text classifier**, described in its own section.
- **`bypassPermissions` is not a configuration anyone should ship.**

---

## Reproduce

```
# clean marketplace install into an isolated config dir, then vendor it
CLAUDE_CONFIG_DIR=<tmp> claude plugin marketplace add pbakaus/impeccable
CLAUDE_CONFIG_DIR=<tmp> claude plugin install impeccable@impeccable

# prime the engine the skill pins (scripts/VERSION), verified against its sidecar
#   ~/.impeccable/bin/0.1.3/impeccable.exe

pwsh tools/run-chunks.ps1 -Mode acceptEdits                       # 5 x 24
pwsh tools/run-chunks.ps1 -Mode bypassPermissions                 # 5 x 24
pwsh tools/run-chunks.ps1 -Mode bypassPermissions -Only 5 -Repeat 1 -Tag chunk5a
python tools/four_axes.py "<label>=<record.json>[,<record.json>…]" …
python tools/refcoverage.py --exec impeccable ./skills/impeccable <records…>
```

`tools/run-chunks.ps1` is resumable: it skips chunks already recorded with exit 0
and rewrites the ledger in `reports/impeccable.4.2.2.progress.md` after each one.

`tools/four_axes.py` was validated against both stored 4.2.1 measurements before
any 4.2.2 attempt was run, and reproduces every published 4.2.1 figure exactly —
28/30 activations, 42/9/6 launcher outcomes, 7 files / 29 reads with identical
per-file counts, 6/29 craft-floor, 0/10 completion. Differences reported here are
therefore differences in the skill, not in the instrument.

Method: <https://assayctl.dev/methodology>

