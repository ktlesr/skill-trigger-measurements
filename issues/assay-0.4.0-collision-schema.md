# Note for the Assay repository — 0.4.0: collision-measurement schema

Recorded 2026-09-10 from the `marketingskills` collision run. **Not
implemented — a note to act on in the Assay repo, not a change here.**

Evidence: `reports/marketingskills.collide.md`, section 5, and run
`run-2026-09-10T11-01-34-914Z-0bec859e` (assay 0.3.2, 200 attempts).

## 1. No way to say "this case expects skill X to win" when X is not the target

A suite has exactly one `target.skill`. `expect.triggered` refers only to it.
For a collision suite — several skills installed, each case aimed at a
different one — the only per-case field that names another skill is
`not_triggered`, which is negative. There is no positive counterpart.

Workaround used: the expected winner was encoded in the case id
(`collide.<skill>.<shape>`) and read back by a separate analyser,
`tools/collide.py`. That works, but the verdict Assay itself prints knows
nothing about it.

## 2. `not_triggered` passes when nothing fires

A case whose only expectation is `not_triggered: [a, b]` passes whenever
neither `a` nor `b` fires — including when **no skill fires at all**. In a
collision suite that is the common failure, not an edge case.

In the run above Assay reported **179 pass / 21 fail**, while 7 of the 13
scored skills never activated on their own cases. **100 positive attempts in
which no marketing skill fired were scored as pass.** The 21 fails were the 20
target (`triggered: true`) attempts plus one real leak.

The run summary's `precision: no observations` and `recall: 0% (N=20)` are also
the target's alone, which in a collision suite is the least interesting row.

## 3. Case-id regex rejects hyphens

`CASE_ID = /^[a-z0-9]+(?:\.[a-z0-9_]+)+$/` — no `-` in any segment. Skill names
are commonly hyphenated (`copy-editing`, `cold-email`, `ai-seo`,
`programmatic-seo`, `product-marketing`), so a collision suite cannot put the
skill's own name in its case id. Worked around with `_`. The validator's
message ("case id must be hierarchical and lowercase") does not say that the
hyphen is the problem, and output truncation hid the fact that every hyphenated
id failed, not just three.

## Shape a 0.4.0 fix could take

- a per-case positive field, e.g. `expect.winner: <skill>` or
  `expect.triggered_skill: <skill>`, validated against `active_skills`
- a verdict for collision cases that is **fail**, not pass, when the expected
  winner did not fire — "the losers stayed quiet" is not the same claim as
  "the winner won"
- a run-level collision matrix (expected × first-to-fire) in the terminal and
  HTML reports, alongside or instead of the target-only precision/recall
- allow `-` in case-id segments, or name the hyphen in the validation message

Backwards compatibility: existing suites use none of these, and `not_triggered`
can keep its current meaning for single-target suites.
