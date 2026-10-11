<!--
Reply for coreyhaines31/marketingskills discussion #584, to jimy-r's 2026-10-11
comment (#discussioncomment-18857216): arm H, the open-list line.
NOT POSTED; ready to post: everything below this comment is the reply body.
No section signs in the body (GitHub dropped them on an earlier post).
Numbers: reports/marketingskills.phrase-binding.md section 16. Runs: arm H
56966467, arm G 2d4b4a5b, arm A re-run 0e10b188, all Claude Code 2.1.288.
-->

The line was followed and the "gone" column didn't move. Every write in arm H
ended with a list of what was left open, and the reason for the pivot was on
none of them.

## Setup

Arm G's skill plus one line, directly after the write-first precondition:

> **After the save, list what's open.** Next to asking what needs correcting,
> list what you left open: the questions the document could be written without,
> but whose answer only the user has.

I gave it no example, since "why the shift happened" would have named the fork
being scored. Same case set, same table, runner 0.4.9, Claude Code 2.1.288.

## Did the open list bring the forks back?

Same method as last time: arm A's fork list for each case, and each fork in the
reply after the write is stated, still asked, or gone.

| | stated | still asked | gone |
| --- | ---: | ---: | ---: |
| ICP, arm G (8 writes × 6) | 40 | 3 | 5 |
| **ICP, arm H (9 writes × 6)** | **43** | **6** | **5** |
| positioning, arm G (7 writes × 7) | 31 | 7 | 11 |
| **positioning, arm H (3 writes × 7)** | **12** | **4** | **5** |

- **All 12 writes carried the list**, as a separate block: "What's still open
  (only you can fill in)", "Sections left open (only you know these for
  certain)".
- **"Gone" held still.** ICP 5 of 54 against 5 of 48, positioning 5 of 21
  against 11 of 49: roughly 10% and 23% in both arms.
- **The pivot reason came back in 0 of 3 positioning writes** (G: gone in 7 of
  7). No attempt in arm H, writer or not, asked why the shift happened.
- **What the list did pull into "still asked" is proof.** On ICP, proof and
  customer mix went from 3 asked and 2 gone to 6 asked and 0 gone.

What the model files under "only you know" is customer names, testimonials,
metrics, pricing, and competitors it might have missed. Every one of those is a
blank in the document's template (Proof Points, Goals). The reason for the
pivot has no field there, so it never makes the list. My reading: the agent
lists the gaps in the document, not the decisions it made without asking. To
catch a dropped question, the line probably has to name what kind of answer
belongs on it ("decisions you made without asking, and the reason for the
change"), or the template needs a field for it. I didn't run either.

## Delivery

| | arm A | arm G | **arm H** |
| --- | --- | --- | --- |
| **ICP, shared context file written** | 1/10 | 8/10 | **9/10** |
| **positioning, shared context file written** | 0/10 | 7/10 | **3/10** |
| change requests, file written | 36/100 | 48/100 | **40/100** |
| activation, 16 scored cases | 160/160 | 160/160 | **159/160** |
| negatives fired | 0/30 | 0/30 | **0/30** |

- **The new line didn't break the writing on ICP.** It's at 9 of 10.
- **Positioning dropped from 7 to 3 of 10.** The intervals overlap (40–89% and
  11–60%). In six of those attempts the skill asked before writing, as in arm A.
  The line sits after the save, so I don't see how it would cause that, and ten
  attempts can't separate it from noise.
- **Skipped precondition: 7 of 19** attempts where the skill fired, against 5 of
  20 in G. Same caveat, and it backs your point about advice the model can pass
  over.
- **The one activation miss** is a positioning attempt that never opened the
  skill. It wrote the new positioning into the project's `CLAUDE.md`, which is
  the table itself.

That edit also cost the run its context hash. The runner hashes the loaded
instruction files when an attempt ends, so the attempt that edited `CLAUDE.md`
reported a different hash from the other 199. With the environments
disagreeing, the record carries neither an environment block nor a context
hash. The table did load: a probe right before the batch shows the same file
hash and context hash as G. The engine is pinned by the environment hash, which
leaves memory out and matches G's 2.1.288 record. But `assay compare` can't
confirm the context for H, so this comparison rests on the probe, not on the
record. Hashing at load time instead is noted as a runner fix.

## Limits

- Three positioning writes, so that row is soft. The ICP row, with 9 writes, is
  the one to read.
- One reader, one model (Haiku 4.5), non-interactive, `acceptEdits`, ten
  attempts per case.

Report, section 16: https://github.com/ktlesr/skill-trigger-measurements/blob/master/reports/marketingskills.phrase-binding.md
