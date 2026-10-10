<!--
Reply for coreyhaines31/marketingskills discussion #584, to jimy-r's 2026-10-09
comment (#discussioncomment-18836226): arm G and the arm A baseline.
NOT POSTED; ready to post: everything below this comment is the reply body.
No section signs in the body (GitHub dropped them on an earlier post).
Numbers: reports/marketingskills.phrase-binding.md section 15. Runs: arm A
re-run 0e10b188, arm G 2d4b4a5b, arm F aa524c4d, all Claude Code 2.1.288.
-->

G moved ICP. With write-first-ask-after on `product-marketing`'s save step, the
shared context file was written on ICP in 8 of 10 attempts, against 1 of 10 for
arm A on the same engine. Positioning moved with it, from 0 to 7 of 10.

## Setup

Arm G starts from the original skill, so arm F's single-question precondition
isn't in it. One precondition goes at the top of the skill's "Confirm, Version,
and Save" step:

> **Precondition: write first, ask after.** Before asking the user anything,
> write your best draft from what the prompt and the existing files already give
> you, set the version and changelog, and save it to `.agents/product-marketing.md`.
> Only then show it and ask what needs correcting. Keep the questions; they come
> after the save, not instead of it.

Arm A was re-run in the same batch, as you asked. Both are on Claude Code
2.1.288, the same as F. The machine had already updated past it, so I put a
2.1.288 binary first on the runner's PATH, and each record confirms that version
from the agent's own init event. A, F and G share the suite, the context and the
environment hashes. `assay compare` names one drift between them, the skill,
which is the variable.

## Delivery

| | arm A (re-run) | arm F | **arm G** |
| --- | --- | --- | --- |
| **ICP, shared context file written** | 1/10 | 0/10 | **8/10** |
| **positioning, shared context file written** | 0/10 | 0/10 | **7/10** |
| change requests, file written | 36/100 | 44/100 | **48/100** |
| activation, 16 scored cases | 160/160 | 160/160 | **160/160** |
| negatives fired | 0/30 | 0/30 | **0/30** |

- On ICP the intervals separate: 2–40% against 49–94%. Every write went to the
  shared file, not to a new one. Earlier arms on ICP were 0 to 2 of 10.
- F's 44 of 100 can now be read: arm A on the same engine is at 36, and F and G
  both overlap it. Of G's +12 on change requests, +7 is the positioning case.
  The other nine cases move by at most 2 of 10 either way.
- The engine moved nothing on its own. Arm A on 2.1.288 (36 of 100, ICP 1 of 10)
  sits where arm A sat on 2.1.270 (40, and 2 of 10).
- The precondition was skipped in 5 of 20 product-marketing attempts. Those
  asked first, as in A and F.

## Did the questions become assumptions?

For each G attempt that wrote, I took arm A's fork list for the same case and
checked the reply that came after the write. Each fork is either stated as an
assumption, still asked with no choice made, or gone (neither stated nor
asked).

| | stated | still asked | gone |
| --- | ---: | ---: | ---: |
| ICP (8 writes × 6 forks) | 40 | 3 | 5 |
| positioning (7 writes × 7 forks) | 31 | 7 | 11 |

- **The three you named became assumptions.** The segment was stated in 11 of 15
  writes ("platform teams at $10M–$500M ARR API companies"), the buyer in 15 of
  15 ("VP Eng for budget, Staff Eng for integration"), and draft-or-walkthrough
  was settled by the write itself.
- **What stayed a question is what the model can't invent:** customer names,
  testimonials, metrics. Those are asked after the save, and several documents
  leave `[ADD: ]` placeholders for them. That's the ordering the precondition
  asked for.
- **What disappeared is mostly "why did you make the shift?"** It's gone in 7 of
  7 positioning writes. Nobody states a reason for the pivot or asks for one. It's
  the one arm A question whose answer only the user has and that the document can
  be written without.
- Every write was followed by "what needs correcting?", so the question moved
  rather than vanished.

So for your rule: the lever is the write step. A precondition on one question
(arm F) removes that question and the skill finds another. A precondition that
orders the write before any question gets the shared file written, and turns
most of the questions into assumptions you can correct.

## Limits

- One skill, two cases, ten attempts each. Whether write-then-ask moves other
  skills' ask steps is untested.
- One model (Haiku 4.5), non-interactive, `acceptEdits`. In a conversation, A's
  questions would also get answered. What G changes is that the work exists
  before anyone answers.
- The assumption match is my reading of 15 replies. The saved documents weren't
  scored separately.

Report, section 15: https://github.com/ktlesr/skill-trigger-measurements/blob/master/reports/marketingskills.phrase-binding.md
