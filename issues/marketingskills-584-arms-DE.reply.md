<!--
Reply draft for coreyhaines31/marketingskills discussion #584, to jimy-r's
2026-09-25 comment (#discussioncomment-18606188), following our 2026-09-26 reply
(#discussioncomment-18614237) that announced arms D and E. NOT POSTED.
Numbers: reports/marketingskills.phrase-binding.md §8–§10,
runs 097d7682 (D) and e4e274a9 (E).
-->

Both arms are in. Same suite, same 14 skills, same model and permission mode,
200 attempts each. Neither rule did what we hoped.

## The slot is filled, and it says "none"

Arm E is arm A's table plus your line: every reply ends with "Forks: none" or
"Forks: picked X over Y because R".

| | arm E |
| --- | --- |
| reply ends with the slot in the given form | **169 / 200** |
| of those, "Forks: none" | **162** |
| on the four cases built around a choice | **34 / 40 "none"** |

The pricing case is the cleanest example. The prompt is "Should our Pro plan be
$49 or $79 a month? Decide from what is in pricing.html and tell me the
number." All ten replies answer "$49", which is the price already in the file,
and end with "Forks: none". The model doesn't treat $49 over $79 as a choice it
made; it reads off the current value and reports no fork.

The reflexive "none" you warned about is what happened. Every in-form slot on
the four fork cases says "none". The only forks declared on those cases are two
exit-modal replies that used their own wording. Across the whole run, 22 of the
188 replies with any `Forks:` line name a fork. So you were right that the slot
removes the noticing: it's there in 188 of 200 replies, against 5 of 170 for
arm C's fork line. The judgement that's left, filling it, mostly defaults to
"none".

I said I expected the slot to be the arm that moved the number. It moved the
presence of the line. It didn't move what the line reports, and it didn't move
the work.

## Delivery didn't come back

Change requests where a file was written, out of 100:

| A (table) | B (no file) | C (default) | D (template) | E (slot) |
| --- | --- | --- | --- | --- |
| 40 | 81 | 52 | 40 | 32 |

None of the three rules gets near B. Among the arms with the table, the
intervals separate only between C and E, and in the wrong direction: the slot
arm wrote the fewest files. The three cases that never write with the table
(the newsletter form, the integration pages, the positioning file) write
nothing under any of the rules. A rule about what to print doesn't reach the
skills' own ask-first steps.

## The template: 3 exact, 15 by hand, and mostly the wrong fork

Arm D is arm C's file with the instruction replaced by your template, "Picking X
over Y because R; redirect if wrong."

- Exact form: **3 / 170**, and 1 of those on the first line.
- Any fork line, read by hand: **15 / 170**, against 5 / 170 in C. The intervals
  overlap.
- In **12 of the 15**, the "fork" is the skill the table routed to: "Picking
  `marketing-skills:signup` skill because the phrase … is in the command
  shortcuts table; redirect if wrong." Only 3 name a choice in the work itself.

Given the template, the fork the model most often reports is the one it didn't
make, because the lookup made it.

## Activation held in every arm

160 / 160 on the scored cases in A, C, D and E; 0 misroutes, no bypass, and 0 of
30 negatives fired. None of the output rules disturbed the table. That matches
the layer split: routing and output shape are separate, and these rules only
reached the second.

## How it was scored

No assertion was added to the suite, so its hash is the same across all five
runs. The slot and the template are scored by a separate script that hands each
reply to assay-core's own `evaluateAssertion` as a one-file workspace and checks
it with `file_content_matches`: pass or fail, no new verdict state. On the 600
attempts of arms A–C it scores zero for both markers.

## Limits

- Host: D and E ran on Claude Code 2.1.271, the same as C. A and B were on
  2.1.270.
- The four fork cases (pricing, exit-modal timing, stale positioning, ICP
  write-up) were fixed before any arm E reply was read. Whether a "none" is wrong
  is a reading against those four; the pricing case is the one where the fork
  is written in the prompt itself.
- One model (Haiku 4.5), non-interactive, `acceptEdits`, runner 0.4.4.

## Where that leaves it

Your hypothesis was that a template, and then a slot, would get the fork
reported where an instruction didn't. That's now measured, and it didn't hold.
That's a result, and it fits your own count: seven flag lines in six weeks, one
of them useful. The slot makes the line appear. It doesn't make the model notice
that it chose. For your review's kill test, the slot answers "flags never
appear". What it doesn't answer is whether what appears is true, and on the four
cases where we know there was a choice, it mostly wasn't.

Report, §8–§10: https://github.com/ktlesr/skill-trigger-measurements/blob/master/reports/marketingskills.phrase-binding.md
