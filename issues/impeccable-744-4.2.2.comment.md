# Comment prepared for pbakaus/impeccable#744

The 4.2.2 measurement promised in my last comment. Post as-is.

---

Here are the 4.2.2 numbers I offered to run. Same suite at the same case-set
hash, same model, same host, **same measurement tool at the same pin** — only the
skill version changed, so anything that moves is #750.

240 attempts: 120 under `acceptEdits`, 120 under `bypassPermissions`. As before,
**`bypassPermissions` is an instrument, not a recommendation** — it is the only
way to hold the permission layer constant so the skill''s own behaviour can be
separated from the host''s refusals. Nobody should ship it.

Short version: **#750 fixed the path half of finding 4 and moved finding 2 a long
way. It did not touch the quoting half of finding 4, finding 1 is exactly where
it was, and reference breadth got slightly worse.**

## What moved

| | 4.2.1 | 4.2.2 |
| --- | --- | --- |
| launcher resolved the wrong base dir | **11 / 57** | **1 / 56** |
| launcher failed for the skill''s own reasons | **26%** | **10%** |
| `craft-floor.md` read before a UI edit | **6 / 29 (21%)** | **16 / 30 (53%)** |
| told the user when the launcher failed | 3 / 27 (11%) | 16 / 27 (59%) |
| launcher calls per activation (`acceptEdits`) | 1.96 | 1.12 |

**Finding 4a is essentially fixed.** Naming `${CLAUDE_SKILL_DIR}` and saying in
as many words that it is *not* the plugin root two levels up took mis-resolved
`<plugin-root>/scripts/…` paths from 11 of 57 calls to 1 of 56.

**Finding 2 moved more than I expected.** `craft-floor.md` went from the
sixth-most-read reference to the most-read one, and from 21% to 53% of UI-editing
activations. The intervals barely touch, so this is real. Step 3''s rewording did
what it was meant to do.

**The new "Launcher unavailable" paragraph works on both halves.** The model
retries far less (1.96 → 1.12 calls per activation) and now usually says out loud
that context loading did not run. One caveat on that last row: it is a text
classification, not an exact count — a sentence naming the launcher *and* saying
something went wrong with it. I read both negative lists by hand and tried
several pattern widths; every variant gave the same 4-5x shape. Treat 59% as
approximate, the direction as solid.

## What did not move

**Finding 4b — the quoting failure — is untouched.** `ParserError: Unexpected
token 'context'`, a quoted `.cmd` invoked without the `&` call operator, is still
4 calls in 56 against 6 in 57. #750 changed *which directory* the command names;
it did not change *how the command is quoted*, and that was the other half of the
26%. `SKILL.md` still says to call `"${CLAUDE_SKILL_DIR}/scripts/impeccable.cmd"`
on Windows without saying how to invoke a quoted path in PowerShell. That one
line is probably the rest of the fix.

**Finding 1 is exactly where it was.** The completion case:

| | 4.2.1 AE | 4.2.2 AE | 4.2.1 BP | 4.2.2 BP |
| --- | --- | --- | --- | --- |
| skill activated | 0/10 | **0/10** | 0/10 | **0/10** |
| `DESIGN.md` written anyway | 10/10 | 10/10 | 9/10 | 6/10 |
| `document.md` opened | 0 | **0** | 0 | **0** |

Forty attempts across two versions and two permission modes, and the skill is not
reached once. `document.md` has now never been opened in 480 measured attempts.
This is not a permission artefact and not a version artefact — it is the
activation-coverage question, and it is still the right one to settle with #375
rather than by widening the description. (The 6/10 is the only cell that moved
and it is inside noise at N=10; I am not claiming it.)

**Reference breadth went the wrong way.** Total reference reads are up 45%
(29 → 42), but distinct files read fell from **7 of 35 to 5 of 35**. Almost all
the extra volume is `craft-floor.md`. Meanwhile `settings_rework` — whose
Commands-table entry is `layout` — stopped reaching `layout.md` and `operate.md`
entirely; it read them 4 times between them in 4.2.1 and zero times in 4.2.2. Its
only reference read now is the craft floor.

So step 3 got louder and step 2 got quieter. Where the routing does run it is
still the reference your Commands table names — `onboard.md` for an empty state,
`new-work.md` for a replacement visual world, `bolder.md` for "make it
memorable". But 30 of 35 documented references are still never opened in 120
attempts, up from 28.

**Routing itself did not change**, which is the expected result: precision 100%
in all four measurements, 0 false positives in 280 negative attempts, and no
per-case difference clears its interval.

## Two caveats against myself

**This host''s Git bash is intermittently broken** (`fatal error - add_item …`)
and it was not during the 4.2.1 `bypassPermissions` run — 11 of 390 Bash calls
today against 0 of 403 then. That inflates 4.2.2''s raw failure column for a
reason that is nothing to do with the skill, so the "26% → 10%" row above
excludes it from both sides. The raw counts are in the report.

**The engine pin moved 0.1.2 → 0.1.3 with the skill version** and the two are not
separable — they ship together. I primed the host with 0.1.3 by hand
(sha256-verified against your release sidecar) so this is primed-host against
primed-host, matching the 4.2.1 condition. Worth knowing separately: the
launcher''s self-download path fails closed and silently if `System32` is off the
shell PATH, because `where curl.exe` is its gate.

## Operational note, again

The orphaned-dev-server problem from my last comment is real and my mitigation
only half worked. I chunked from the start and cleared orphans between chunks —
that caught 2, 1 and 4 servers — but the kill that matters happens *inside* a
chunk. A 24-attempt chunk died at exit -1 with no record twice in a row before I
halved the window to 12, which survived. If you ever run this yourselves, chunk
in twelves.

---

Full report, with per-case tables, the method, and the instrument validation:
<https://github.com/ktlesr/skill-trigger-measurements/blob/master/reports/impeccable.4.2.2.md>

The analysis tool was checked against both stored 4.2.1 measurements before any
4.2.2 attempt ran, and reproduces every previously published 4.2.1 figure exactly
— so the differences above are differences in the skill, not in my tooling.
