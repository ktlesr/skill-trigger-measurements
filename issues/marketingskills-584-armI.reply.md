The field was filled every time, and never with your reason. With "What
changed from the current positioning, and why" in the template, all 16 writes
filled it. In 7 the model supplied a motive of its own and stated it as fact;
in the other 9 it described how platform teams differ, which is the "what".
None of them asked.

## Setup

Arm G's skill, not H's, so the "list what's open" line isn't in it. One line
added to the document template, in Product Overview, after Business model:

> `**What changed from the current positioning, and why:**`

Same case set, same table, Claude Code 2.1.288. The runner moved from 0.4.9 to
0.5.0. Between the two, the only code change is that instruction files are
hashed when they load, which is the fix for the context hash arm H lost.
Launching is unchanged, the record has its context hash back, and `assay
compare` against G names the skill as the only drift.

## Delivery

| | arm A | arm G | arm H | **arm I** |
| --- | --- | --- | --- | --- |
| **ICP, shared context file written** | 1/10 | 8/10 | 9/10 | **9/10** |
| **positioning, shared context file written** | 0/10 | 7/10 | 3/10 | **7/10** |
| change requests, file written | 36/100 | 48/100 | 40/100 | **49/100** |
| precondition skipped (fired, asked first, no write) | — | 5/20 | 7/19 | **4/20** |
| activation, 16 scored cases | 160/160 | 160/160 | 159/160 | **160/160** |
| negatives fired | 0/30 | 0/30 | 0/30 | **0/30** |

The field cost nothing on the write. Positioning is back at G's 7, so H's 3
looks like noise.

## The field

The prompt gives no reason for the pivot, only that it happened. So whatever
lands in the field is either your answer, asked for, or the model's.

| | positioning (7 writes) | ICP (9 writes) |
| --- | ---: | ---: |
| field filled | 7 | 9 |
| …with a motive for the move, as fact | 2 | 5 |
| …with what changed and how the audience differs, no motive | 5 | 4 |
| …left open, marked as an assumption, or `[ADD: ]` | 0 | 0 |
| reason asked after the write | 0 | 0 |

The motives read like findings: "This is a bigger TAM with higher LTV and less
price sensitivity." "This is where we're winning… Indie developers often stay
on free tier or leave when complexity grows." "We discovered that the biggest
pain point isn't indie developers…". None is flagged as a guess, and all of
them now sit at the top of the file every other skill reads first.

The "only you know" lists after the save look like H's: customer names,
testimonials, metrics. The model hands back the blanks it left. This one it
never left.

One thing I hadn't looked at before. G's changelog rule already asks for
"what changed and why", and G's 7 positioning entries name what changed and
none says why. Arm I's 16 entries are the same. So the field is the second
place the template asks for the reason, and it's the one that got an answer.
The answer was the model's.

## Assumption match, same method as before

| | stated | still asked | gone |
| --- | ---: | ---: | ---: |
| ICP, arm G (8 writes × 6) | 40 | 3 | 5 |
| **ICP, arm I (9 writes × 6)** | **46** | **7** | **1** |
| positioning, arm G (7 writes × 7) | 31 | 7 | 11 |
| **positioning, arm I (7 writes × 7)** | **33** | **7** | **9** |

In the reply, "why the shift happened" is gone in 7 of 7, as in G. Counting
the document as well, it's in the field 7 of 7: as the model's motive in 2, as
an audience description in 5, and as the user's in none. The ICP "gone" drop to
1 is the softest number here; it's one reader across three sessions.

## Your refutation condition

You said that if the reason still goes missing with a field in place, the fork
is lost before the write, at the ask step. **It holds, in a stronger form.** The
reason didn't go missing as an empty slot. It was replaced: the field moved it
from *gone* to *filled by the model*, not to *asked*.

The ask step is the only place it ever appeared. Across arms A, G, H and I, on
both cases, four attempts asked for the reason ("What's driving the shift?",
"Why did you…"), and all four asked before writing and never wrote the file. In
43 writes across G, H and I, no reply asked it.

So a field gives the model a place to put an answer, not a reason to ask for
one. Two things I haven't run: wording the field as the user's ("ask; don't
infer"), or an exception in the write-first precondition for answers only the
user has. Either would be one more arm.

## Limits

- One reader for the field split and the assumption match. Three borderline
  calls on motive versus description; moving them gives between 6 and 9
  motives out of 16.
- Ten attempts per case, one model (Haiku 4.5), non-interactive, `acceptEdits`.
  In a conversation someone would correct an invented motive. In an unattended
  write it stays.

Report, section 17: https://github.com/ktlesr/skill-trigger-measurements/blob/master/reports/marketingskills.phrase-binding.md
