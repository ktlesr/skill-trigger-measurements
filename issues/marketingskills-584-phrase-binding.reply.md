<!--
Reply draft for coreyhaines31/marketingskills discussion #584, to jimy-r's
2026-09-13 comment. NOT POSTED. Numbers: reports/marketingskills.phrase-binding.md,
runs 6e03681d (A) and 5ec9e04b (B).
-->

I ran it. Same 14 skills, same 20 cases, same pinned model
(`claude-haiku-4-5-20251001`), 200 attempts per arm.

- **Arm A** had one `CLAUDE.md` with your standing rule word for word, under a
  `## Command shortcuts` heading, and one `Phrase family | Target` row per skill.
  The phrases come from my own case prompts, not from yours, so the delta is the
  mechanism rather than your wording.
- **Arm B** had no instruction file.

I put the file in an ancestor of every working directory, which is the
workspace-above-project layout from your write-up. It is in context from turn
one, and the agent never sees it as a workspace file. Nothing else differed:
the suite, skill and environment hashes are identical across the two arms.

## You were right about activation

| | without the table | with it |
| --- | --- | --- |
| the seven that never fired (`signup`, `popups`, `paywalls`, `onboarding`, `copy-editing`, `programmatic-seo`, `product-marketing`) | 0 / 90 | **90 / 90** |
| all 16 scored cases | 49 / 160 | **160 / 160** |
| edit-shaped bypass (no skill fires, the file gets edited anyway) | 84 / 160 | **0 / 160** |
| activations that reached the wrong skill | 1 | 0 |
| negative cases that fired a skill | 0 / 30 | 0 / 30 |

At ten attempts per case, the intervals separate for all seven plus `cro`. The
other five already fired without the table.

So the failure was the routing judgment. Given a lookup, the model followed it
160 times out of 160, including on the edit-shaped requests it otherwise answers
by editing the file.

<details>
<summary>The two activation matrices</summary>

**With the table** (rows: expected skill · columns: first skill to fire)

| expected \ fired | none | `signup` | `cro` | `popups` | `paywalls` | `onboarding` | `copy-editing` | `emails` | `cold-email` | `seo-audit` | `ai-seo` | `programmatic-seo` | `schema` | `product-marketing` |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `signup` | · | 10 | · | · | · | · | · | · | · | · | · | · | · | · |
| `cro` | · | · | 20 | · | · | · | · | · | · | · | · | · | · | · |
| `popups` | · | · | · | 20 | · | · | · | · | · | · | · | · | · | · |
| `paywalls` | · | · | · | · | 10 | · | · | · | · | · | · | · | · | · |
| `onboarding` | · | · | · | · | · | 10 | · | · | · | · | · | · | · | · |
| `copy-editing` | · | · | · | · | · | · | 10 | · | · | · | · | · | · | · |
| `emails` | · | · | · | · | · | · | · | 10 | · | · | · | · | · | · |
| `cold-email` | · | · | · | · | · | · | · | · | 10 | · | · | · | · | · |
| `seo-audit` | · | · | · | · | · | · | · | · | · | 10 | · | · | · | · |
| `ai-seo` | · | · | · | · | · | · | · | · | · | · | 10 | · | · | · |
| `programmatic-seo` | · | · | · | · | · | · | · | · | · | · | · | 10 | · | · |
| `schema` | · | · | · | · | · | · | · | · | · | · | · | · | 10 | · |
| `product-marketing` | · | · | · | · | · | · | · | · | · | · | · | · | · | 20 |

**Without** (rows: expected skill · columns: first skill to fire)

| expected \ fired | none | `cro` | `emails` | `cold-email` | `seo-audit` | `ai-seo` | `schema` |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `signup` | 10 | · | · | · | · | · | · |
| `cro` | 13 | 7 | · | · | · | · | · |
| `popups` | 20 | · | · | · | · | · | · |
| `paywalls` | 10 | · | · | · | · | · | · |
| `onboarding` | 10 | · | · | · | · | · | · |
| `copy-editing` | 10 | · | · | · | · | · | · |
| `emails` | 1 | · | 9 | · | · | · | · |
| `cold-email` | 3 | · | · | 7 | · | · | · |
| `seo-audit` | 2 | · | · | · | 7 | 1 | · |
| `ai-seo` | · | · | · | · | · | 10 | · |
| `programmatic-seo` | 10 | · | · | · | · | · | · |
| `schema` | 1 | · | · | · | · | · | 9 |
| `product-marketing` | 20 | · | · | · | · | · | · |

</details>

## The part I didn't expect: less of the work gets done

Once the table routes a request to a skill, the skill's own workflow tends to
ask the user something before it acts. These runs are non-interactive (`-p`),
so nobody answers, and the attempt ends there.

- **Prompts that ask for a change:** a file was written in 81 of 100 attempts
  without the table and **40 of 100 with it**. The newsletter form went from 8
  to 0, the one-page-per-integration build from 10 to 0, and the positioning
  update from 9 to 0.
- **Prompts that can be answered in the reply:** the answer was delivered in
  66 of 70 without the table and **51 of 70 with it**. I read every reply to
  classify these.

A typical attempt with the table reads the context file, diagnoses the problem
well, and ends with "Before I rework it, I need a few quick clarifications…" or
"Would you like me to implement these changes to your index.html?". Without the
table, the base model made a call and wrote the file. It didn't use the skill's
method, but the job got done.

In a conversation those questions would be answered and the work would go on,
and I haven't measured how much of the gap closes then. For anything that runs
these skills headless, though, the table trades a skill that never fires for a
skill that fires and waits: CI, scheduled agents, anything with nobody at the
keyboard. On change requests, that halves the work delivered.

## `product-marketing` fires, and its file still doesn't get updated

With the table, `product-marketing` fires 20 of 20 times on its two cases
(0 of 20 without). It finds `.agents/product-marketing.md`, summarises what is
stale, asks what the new market looks like, and stops. The file was updated in
**2 of 20** attempts with the table and 1 of 20 without.

What the table does change is the fork. Without it, the new positioning went
somewhere else in 18 of 20 attempts: host memory in 8, and a new
`POSITIONING.md`-style file in 10. With the table that happened 0 times. So the
table stops the parallel file, but headless it does not get the shared one
updated. Your other suggestion, putting the write-back obligation in the file's
own header, is the obvious next test. This run didn't include it.

Related: activated skills read the context file in 101 of 170 activations with
the table, against 5 of 50 without.

## What this doesn't show

- **This is the best case for the table.** Every row holds phrases lifted from
  the prompts it routes. It shows that a matching lookup is followed, not that
  "close variants" generalise. A paraphrased case set is the next run.
- **One model** (Haiku 4.5), **non-interactive**, `acceptEdits`.
- **A small side effect of activation:** after a skill loads, Haiku sometimes
  resolved workspace paths against the skill's own directory and had the read
  refused. That happened in 15 attempts with the table and 1 without, and three
  of those attempts ended by asking for permission to read files that were
  already in the workspace.

## Two corrections to my original post

- **The host version was wrong.** It was Claude Code 2.1.267, not 2.1.263; the
  run record is clear, and I misreported it.
- **Those runs had a stray instruction file loaded.** Like every run on this
  Windows machine until today, they loaded the host's own one-line
  `~/.claude/CLAUDE.md`, which is about an unrelated tool. `%TEMP%` sits under
  the home directory, and Claude Code picks the file up walking up from the
  working directory. Today's two arms ran without it, and the no-table arm
  reproduces the original picture: the same seven at 0.

Report, the table file and per-case numbers:
https://github.com/ktlesr/skill-trigger-measurements/blob/master/reports/marketingskills.phrase-binding.md

The table itself:
https://github.com/ktlesr/skill-trigger-measurements/blob/master/fixtures/phrase-binding/CLAUDE.md
