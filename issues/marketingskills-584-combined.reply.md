<!--
Reply for coreyhaines31/marketingskills discussion #584, to jimy-r's 2026-09-25
(#discussioncomment-18606188) and 2026-09-27 (#discussioncomment-18619124)
comments. Merges and supersedes issues/marketingskills-584-arms-DE.reply.md and
issues/marketingskills-584-followups.reply.md. NOT POSTED; ready to post:
everything below this comment is the reply body.
Numbers: reports/marketingskills.phrase-binding.md §8–§12. Runs: D 097d7682,
E e4e274a9, new C affc439d (old C 71c261de, A 6e03681d, B 5ec9e04b).
-->

All of it is in: arms D and E, your fork-list check, the `product-marketing`
row, and arm C re-run on a runner that measures context. Same suite, the same
14 skills, the same model and permission mode throughout.

## The slot: filled almost every time, and it almost never names a real fork

Arm E is arm A's table plus your line: every reply ends with "Forks: none" or
"Forks: picked X over Y because R". The format is followed. 188 of 200 replies
carry a `Forks:` line, against 5 of 170 for arm C's fork line. What goes inside
it is mostly "none".

To judge the "none", I used the method from your last comment rather than my
own framing. I took every arm A reply that stopped to ask the user something,
dropped the permission-only questions and the question marks inside drafted
copy, and took the union per case across the ten attempts. That gives each
case's known forks, taken from the model's own questions. The per-case lists
are in §11.1 of the report.

Arm E's last `Forks:` line against those lists:

| | attempts |
| --- | ---: |
| "none" where the case's list is non-empty: **miss** | **134** |
| names a listed fork: **hit** | **5** |
| names something off the list: read by hand | 18 |
| "none" where the list is empty | 31 |
| no `Forks:` line | 12 |

So 195 of 200 slots do not name a fork the model itself had raised, and 134 of
those are outright misses. The five hits are exit intent over the timer (two),
substance over a newsletter ask on the exit modal, and one headline variant over
another (two). Of the 18 off-list slots, 6 name the table's routing, 8 name real
choices A never asked about (email-only over social auth on the signup form,
tightening over a rewrite on the paragraph), 3 are priorities written as forks,
and 1 isn't a fork at all. None of the 18 is a lying slot. The check works as
you described: 18 reads instead of 200.

Two things the list changed:

- **Most of what arm A asked for is missing input, not a choice.** Conversion
  rates, traffic sources, who the buyer is. Thirteen of the sixteen non-empty
  lists do contain an explicit X-or-Y choice, and 107 of the 134 misses fall on
  those cases. The five hits are all choices between named options; a missing
  input never shows up in a slot.
- **The `$49 or $79` case has no fork by this method.** I had counted it as
  forked because the prompt names two prices. Arm A answered it 10 of 10 times
  without asking, so its list is empty, and E's ten "none" there aren't misses.
  Your list comes from the model's own questions, which makes it the stronger
  test, so I've dropped my framing.

The literal template (arm D, "Picking X over Y because R; redirect if wrong.")
did no better. It appeared in exact form in 3 of 170 attempts, and 15 of 170
contained any fork line when read by hand. In 12 of those 15 the "fork" is the
skill the table routed to. Given a template, the fork the model most often
reports is the one the lookup made for it.

This fits your own count, seven flag lines in six weeks with one useful. The
slot makes the line appear. It doesn't make the model notice that it chose.

## Delivery: no output rule brought the work back

Change requests where a file was written, out of 100:

| A (table) | B (no file) | C (default) | D (template) | E (slot) |
| --- | --- | --- | --- | --- |
| 40 | 81 | **51** (re-run; 52 before) | 40 | 32 |

None of the rules gets near B, and among the table arms none separates from A.
The slot arm wrote the fewest files. Old C's 52 separated from E's 32; the
re-run's 51 only overlaps it. The newsletter form and the positioning file get
nothing written in any table arm, and the integration pages get 0 to 3 of 10. A
rule about what to print doesn't reach the skills' own ask-first steps.

Routing was untouched throughout: 160 of 160 on the scored cases in every table
arm, no misroutes, no bypass, and 0 of 30 negatives fired.

## `product-marketing`: the ICP number didn't move

Attempts that wrote any file, out of 10:

| | A | B | C (old) | D | E | C (re-run) |
| --- | --- | --- | --- | --- | --- | --- |
| **ICP** | **2** | 10 | **1** | **1** | **0** | **0** |
| ICP, shared context file | 2 | 0 | 1 | 1 | 0 | 0 |
| positioning | 0 | 9 | 0 | 0 | 0 | 0 |
| positioning, shared context file | 0 | 1 | 0 | 0 | 0 | 0 |

A correction first: the "2 of 20" I gave earlier was arm A's, and both writes
were on the ICP case. Arm C wrote 1 of 20.

Across the five table runs, ICP writes 2, 1, 1, 0 and 0 of 10. The standing
default didn't move it, and neither did the template or the slot. Without the
table, all ten ICP attempts write something, but it's a new
`POSITIONING.md`-style file every time and never the shared one. So on the
cleanest test of the posture rule, every form of it tried here loses to the
skill's own step of asking about the market before it writes.

## Arm C, re-run and checked

You asked for C beside D and E. Runner 0.4.8 couldn't do it, because it
excludes every instruction file above the working directory, and that's where
C's file lived. A free check confirmed the table didn't load under it. 0.4.9
lets a case set declare its instruction file and copies it into each working
directory as `CLAUDE.md`. So the re-run uses C's file byte for byte, the table
plus the Default block, now at project scope instead of workspace scope. The
record shows the host loaded it (`Project ./CLAUDE.md sha256:b33a9173…`, the
fixture's own hash), and it is the first table arm with a `contextHash`.

| | old C (2.1.271, runner 0.4.4) | new C (2.1.283, runner 0.4.9) |
| --- | --- | --- |
| activation, 16 scored cases | 160 / 160 | 160 / 160 |
| change requests, file written | 52 / 100 | **51 / 100** |
| ICP, file written | 1 / 10 | **0 / 10** |
| fork line, same detector | 6 / 170 | **3 / 170** |

Your 52 of 100 holds at 51. It still separates from no table and overlaps A, D
and E. Of the three fork lines, one names the routing, one states a default,
and one labels an ordinary plan as the fork.

`assay compare` refuses to compare the two C runs (exit 3). The suite hash
moved, because the declaration is part of the case set, and the host moved too,
to a new version that also ships two plugins of its own. The JSON also puts
`contextHash` under `unavailable` on a line of its own ("even without that
change the conditions could not be shown to match"). So 0.4.8's context gate
fires on a real pair, though here it is one of three reasons, not the only one.
The old-versus-new table above is a side-by-side, not something `compare` signs
off on. For your review I'd cite the re-run as C, since it's the only table arm
whose context is pinned.

## Limits

- **Not one engine.** A and B ran on Claude Code 2.1.270; old C, D and E on
  2.1.271; the re-run of C on 2.1.283. The machine updated and wasn't
  downgraded, so D and E sit one patch from A and B, and the re-run of C sits
  with neither.
- **Scope moved for C.** The re-run has the file in the working directory, not
  above it, which is how 0.4.9 places a declared file. Delivery came out the
  same, but the two C runs differ in host, runner, scope and suite hash at once.
- **The fork list is one reader's reading.** Dropping permission questions and
  copy, then labelling what was left, was done by hand over 1,200 lines of arm A
  output. The extraction script is in the repo, so it can be read again.
- **Best case for the table.** Every row holds phrases lifted from the prompts
  it routes. A paraphrased case set is still the open test.
- **One model** (Haiku 4.5), **non-interactive**, `acceptEdits`, ten attempts
  per case.

Report, §8–§12: https://github.com/ktlesr/skill-trigger-measurements/blob/master/reports/marketingskills.phrase-binding.md
