<!--
Reply draft for coreyhaines31/marketingskills discussion #584, to jimy-r's
2026-09-27 comment (#discussioncomment-18619124). NOT POSTED.
Meant to go right after issues/marketingskills-584-arms-DE.reply.md, also NOT
POSTED; the two can be merged into one reply. If they stay separate, the D/E
draft's "Limits" line about the four fork cases should point here (§11.1 gives
the pricing case an empty list).
Numbers: reports/marketingskills.phrase-binding.md §11. No new runs.
-->

All three are done. One of them is done as a stop, not a run.

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

## Arm C on the same engine: stopped before running

Two things blocked it, and the second is the one you asked me to check.

1. **C already ran on the same engine as D and E.** All three ran on
   Claude Code 2.1.271. The gap you named is C against A, 2.1.271 against
   2.1.270. The machine is on 2.1.283 today, so a re-run would put C on a third
   engine, level with neither.
2. **Under runner 0.4.8 the table doesn't load.** Since 0.4.5 the runner writes
   `claudeMdExcludes` for every directory above the working directory, and arm C's
   file lives in one of those. I checked it for free: the runner's own settings,
   the file in the ancestor, `claude -p` with no credentials. The host loads its
   instruction files and fires the hook before it reaches "Not logged in", so the
   check costs nothing.

   ```
   exclusions on:  canary fired · loaded: nothing
   exclusions off: canary fired · loaded: D:\pb-C8\CLAUDE.md
   ```

   A 0.4.8 run labelled "arm C" would really be a run with no table.

I could put the table in the fixture's own `CLAUDE.md` to get past the
exclusion. That would change the suite hash and move the file from workspace
scope to project scope, so it would be a new arm, not C again. For your review:
C's 52 of 100 and A's 40 are one patch apart, and that is the only confound
between them. Removing it means re-running B and all four table arms on one
host, with a runner that measures the context but lets an ancestor file
through. I'm happy to do that if the patch step matters for the review.

## `product-marketing` delivery, all five arms

Attempts that wrote any file on each case, out of 10:

| | A | B | C | D | E |
| --- | --- | --- | --- | --- | --- |
| **ICP** | **2** | 10 | **1** | **1** | **0** |
| ICP, shared context file | 2 | 0 | 1 | 1 | 0 |
| positioning | 0 | 9 | 0 | 0 | 0 |
| positioning, shared context file | 0 | 1 | 0 | 0 | 0 |

A correction: the 2 of 20 was arm A's, and both writes were on the ICP case.
Arm C wrote 1 of 20.

The number you most wanted to move hasn't moved. With the table, ICP writes 2,
1, 1 and 0 of 10 across the four arms. The standing default didn't change it,
and neither did the slot. Without the table, all ten ICP attempts write
something, but it's a new `POSITIONING.md`-style file every time and never the
shared one. So on this case the posture rule, in every form tried, loses to the
skill's own step of asking about the market before writing.

Report, §11: https://github.com/ktlesr/skill-trigger-measurements/blob/master/reports/marketingskills.phrase-binding.md
