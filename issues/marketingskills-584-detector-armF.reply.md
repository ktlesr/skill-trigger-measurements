<!--
Reply for coreyhaines31/marketingskills discussion #584: the spread-based fork
detector and arm F. NOT POSTED; ready to post: everything below this comment
is the reply body.
Order: issues/marketingskills-584-combined.reply.md (D/E, fork list, C re-run)
is also NOT POSTED and should go first. This reply refers to its fork list.
Numbers: reports/marketingskills.phrase-binding.md §13 (detector) and §14
(arm F, run aa524c4d).
-->

Both are in. Short version: the spread detector doesn't work as a fork
detector, and the one-skill precondition removed the question it named and
nothing else.

## The spread detector: high on noise, deaf to signal

I measured your idea on the existing records. For each attempt I took what it
left behind: the files it wrote, rebuilt from the fixture plus its edits, or
its final reply if it wrote nothing. Then I measured how far apart a case's ten
outputs are, in two ways: their structure (form fields, controls and sections,
wording ignored) and their content words.

On the face of it, it agrees with the fork list from arm A's questions. Run
over the no-table arm's outputs, the four cases with an empty list have the
four lowest spreads, and all sixteen listed cases sit above them. That holds
after adjusting for output length (AUC 1.00). On arm A's own outputs it is
weaker (0.75 after the length adjustment), because in 13 of A's 20 cases the
output is the stop-and-ask message itself.

Two cases show why that agreement doesn't make it a detector:

- **High on noise.** The form-crash case is the same decision in all twenty
  attempts: one optional chain on line 14. It still scores a spread of 0.36 to
  0.47, because how the line was rewritten changes which words survive. The
  `$49 or $79` case gets the same answer in 20 of 20 replies ("$49") and scores
  0.44 to 0.62. Identical decisions land on the same scale as real forks.
- **Deaf to signal.** `$49 or $79` is the one case whose prompt spells out the
  choice. Every attempt resolves it the same way, by reading the current price
  off the page, so there is no spread to see. A variance detector finds forks
  where the model is unsure. It can't find a fork the model settles the same
  way, without noticing, every time, and that is the failure we were trying to
  catch. The question-based list is blind to the same case, which is why the
  two agree.

So what the spread mostly measures is how open-ended the prompt is: the
empty-list cases are the closed tasks. One thing it did catch is worth keeping.
On the signup form, which nobody asked about, the writers kept anywhere from 6
to 11 fields in the no-table arm, and 3 to 6 with the table. That's a real
fork, taken silently every time, and the question list missed it. So as a
second opinion on a fork list it has some use. As a replacement for
self-report it doesn't work.

## Arm F: one precondition in `product-marketing`

Arm A's setup (the table, no standing default) plus one line in
`product-marketing`'s SKILL.md only, placed directly above "Ask which sections
they want to update":

> Precondition for the next step: if the prompt already states the market (who
> the product is now sold to), do not ask about the market — take it from the
> prompt and continue

Run on Claude Code 2.1.288 with runner 0.4.9, the table declared through the
case set's `context` field. The host loaded it, and the run has a context hash.

| | A | old C | D | E | C re-run | **F** |
| --- | --- | --- | --- | --- | --- | --- |
| **ICP, file written** | 2/10 | 1/10 | 1/10 | 0/10 | 0/10 | **0/10** |
| positioning, file written | 0/10 | 0/10 | 0/10 | 0/10 | 0/10 | **0/10** |
| change requests, file written | 40 | 52 | 40 | 32 | 51 | **44** of 100 |
| activation, 16 scored cases | 160/160 | 160/160 | 160/160 | 160/160 | 160/160 | **160/160** |

Without the table, ICP writes a file 10 of 10 times, never the shared one.

The precondition was followed exactly as written. None of the ten ICP attempts
asked what the new market is. They asked the next thing instead:

| final message | ICP attempts |
| --- | ---: |
| which platform teams exactly (internal or external, size, org shape) | 4 |
| who the buyer or decision-maker is | 3 |
| auto-draft or walk through it section by section | 2 |
| drafts the positioning in the reply, asks what to correct | 1 |

The questions moved one level down, from the market to the segment and the
buyer. Those are the same forks arm A raised on this case. The positioning case
behaves the same way. One attempt wrote a full context document into its reply
and still didn't save it: "Ready to use this, or does something need
adjusting?"

My reading: a precondition on one question removes that one question. The
skill's posture ("Summarize each section and confirm before moving on", "Ask
relevant questions") finds the next thing to ask. If ICP is to move, the
precondition probably has to be on the save, write first and ask after, rather
than on any particular question. I can run that as arm G if you want it.

## Limits

- **F has no baseline on its own engine.** I didn't re-run arm A on 2.1.288,
  so F against A crosses host, runner and where the table sits. On ICP that
  barely matters, since every table arm is at 0 or 1 of 10. On the 44 of 100
  it does: F overlaps every table arm and separates only from no table.
- **The detector rests on four negative cases** from one fixture. The ICP
  classification above is my reading of ten final messages.
- One model (Haiku 4.5), non-interactive, `acceptEdits`.

Report, §13 and §14: https://github.com/ktlesr/skill-trigger-measurements/blob/master/reports/marketingskills.phrase-binding.md
