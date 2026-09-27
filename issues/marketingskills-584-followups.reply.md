<!--
Reply draft for coreyhaines31/marketingskills discussion #584, to jimy-r's
2026-09-27 comment (#discussioncomment-18619124). NOT POSTED.
Updated the same day with the arm C re-run on 0.4.9 (run affc439d, §12).
Meant to go right after issues/marketingskills-584-arms-DE.reply.md, also NOT
POSTED; the two can be merged into one reply. If they stay separate, the D/E
draft's "Limits" line about the four fork cases should point here (§11.1 gives
the pricing case an empty list).
Numbers: reports/marketingskills.phrase-binding.md §11 and §12. Ready to post:
everything below this comment is the reply body. compare re-verified 2026-09-27
(exit 3, drifted suiteHash + environmentHash, unavailable contextHash).
-->

All three are done.

## The fork list from arm A's own questions

I did it your way. I took every arm A reply that ended by asking the user
something, dropped the permission-only questions and the question marks inside
drafted copy, and took the union per case across the ten attempts. The list per
case is in §11.1 of the report.

Arm E's last `Forks:` line, scored against it:

| | attempts |
| --- | ---: |
| "none" where the case's list is non-empty: **miss** | **134** |
| names a listed fork: **hit** | **5** |
| names something off the list: read by hand | 18 |
| "none" where the list is empty | 31 |
| no `Forks:` line | 12 |

The five hits are exit intent over the timer (two), substance over a newsletter
ask on the exit modal, and one headline variant over another (two). Of the 18
off-list slots, 6 name the table's routing, 8 name real choices A never asked
about (email-only over social auth on the signup form, tightening over a
rewrite on the paragraph), 3 are priorities written as forks, and 1 isn't a
fork at all. None of the 18 turned out to be a lying slot.

So the check works as you described: 18 reads instead of 200. What it shows is
that the slot misses 134 times and hits 5 times.

Two things came out of building the list:

- **Most of what arm A asked for is missing input, not a choice.** Conversion
  rates, traffic sources, who the buyer is. Thirteen of the sixteen non-empty
  lists do contain an explicit X-or-Y choice, and 107 of the 134 misses fall on
  those cases. The five hits are all choices between named options; a missing
  input never shows up in a slot.
- **By this method, the `$49 or $79` case has no fork.** Arm A answered it
  10 of 10 times without asking. I'd counted it as forked because the prompt
  names two prices, and your method doesn't. So E's ten "none" there aren't
  misses by your definition. I'd rather use your list than my framing.

## Arm C again, on a runner that measures context

It's re-run. One caveat first: it is not on D and E's engine. They ran on
Claude Code 2.1.271; the machine is on 2.1.283 now, and I didn't downgrade it.

Runner 0.4.8 would have dropped the table: it excludes every instruction file
above the working directory, and C's file lived there. 0.4.9 lets a case set
declare its instruction file, and copies it into each working directory as
`CLAUDE.md`. So this is arm C's file byte for byte, the table plus the Default
block, now at project scope instead of workspace scope. The record confirms the
host loaded it (`Project ./CLAUDE.md sha256:b33a9173…`, the same hash as the
fixture), and the run has a `contextHash` for the first time.

| | old C (2.1.271, runner 0.4.4) | new C (2.1.283, runner 0.4.9) |
| --- | --- | --- |
| activation, 16 scored cases | 160 / 160 | 160 / 160 |
| change requests, file written | 52 / 100 | **51 / 100** |
| ICP, file written | 1 / 10 | **0 / 10** |
| fork line, same detector | 6 / 170 | **3 / 170** |

Your 52 of 100 holds on the new engine at 51. It still separates from no table
(81) and overlaps A (40), D (40) and E (32), as before. Of the three fork lines,
one names the routing, one states a default ("Default taken: using the Meterly
product context…"), and one labels an ordinary plan as the fork.

`assay compare` refuses to compare the two C runs. The suite hash moved (the
declaration is part of the case set), the host moved, the host now ships two
plugins of its own, and old C never measured its context. So the table above is
a side-by-side, not something `compare` signs off on. The JSON puts
`contextHash` under `unavailable` on a line of its own ("even without that
change the conditions could not be shown to match"), so 0.4.8's context gate
fires on a real pair, though here it is one of three reasons, not the only one.
For your review, I'd cite
new C as the baseline: it's the only table arm whose context is pinned.

## `product-marketing` delivery, all six runs

Attempts that wrote any file on each case, out of 10:

| | A | B | C | D | E | new C |
| --- | --- | --- | --- | --- | --- | --- |
| **ICP** | **2** | 10 | **1** | **1** | **0** | **0** |
| ICP, shared context file | 2 | 0 | 1 | 1 | 0 | 0 |
| positioning | 0 | 9 | 0 | 0 | 0 | 0 |
| positioning, shared context file | 0 | 1 | 0 | 0 | 0 | 0 |

A correction: the 2 of 20 was arm A's, and both writes were on the ICP case.
Arm C wrote 1 of 20.

The number you most wanted to move hasn't moved. With the table, ICP writes 2,
1, 1, 0 and 0 of 10 across the five table runs. The standing default didn't
change it, and neither did the slot. Without the table, all ten ICP attempts write
something, but it's a new `POSITIONING.md`-style file every time and never the
shared one. So on this case the posture rule, in every form tried, loses to the
skill's own step of asking about the market before writing.

Report, §11 and §12: https://github.com/ktlesr/skill-trigger-measurements/blob/master/reports/marketingskills.phrase-binding.md
