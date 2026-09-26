# `marketingskills` — does a phrase-binding table make the skills fire?

> **The question.** [jimy-r suggested](https://github.com/coreyhaines31/marketingskills/discussions/584)
> that the seven skills which never fired in the [collision run](marketingskills.collide.md)
> would fire if an instruction file bound phrases to skills — "the routing is a
> lookup, not a judgment". Arm A has that file, arm B does not; nothing else
> differs.
>
> **Arm C, added later**, answers the follow-up: the table made the skills fire
> and the skills then asked instead of acting (§4). Arm C keeps the table and
> adds one standing default — act unless the step must block — to see whether
> the delivery comes back. Sections 1–6 are the A/B measurement and are
> unchanged; arm C is §7.
>
> **Arms D and E, added after C**, ask why C's marker appeared in only 5 of 170
> attempts: was the instruction too loose to follow? Arm D gives the fork line
> as a literal template; arm E drops the default and makes a closing slot
> mandatory on every reply. §8 is D, §9 is E, §10 puts all five arms side by
> side. Sections 1–7 are unchanged.

| | Arm A — phrase-binding table | Arm B — no instruction file | Arm C — table + standing default | Arm D — C with a literal fork template | Arm E — table + mandatory closing slot |
| --- | --- | --- | --- | --- | --- |
| Run | `run-2026-09-13T13-42-08-147Z-6e03681d` | `run-2026-09-13T13-18-44-877Z-5ec9e04b` | `run-2026-09-23T05-36-00-561Z-71c261de` | `run-2026-09-26T16-11-21-616Z-097d7682` | `run-2026-09-26T16-32-52-854Z-e4e274a9` |
| Attempts | 200 · 0 unknown · $9.91 | 200 · 0 unknown · $9.52 | 200 · 0 unknown · $10.22 | 200 · 0 unknown · $9.74 | 200 · 0 unknown · $9.26 |
| Suite | v3, `sha256:ee4ae643…` | same | same | same | same |
| Skills | 14, `sha256:aff03848…` | same | same | same | same |
| Environment | `sha256:b041fb3c…` | same | `sha256:7eabde5b…` — the host moved (below) | `sha256:7eabde5b…`, as C | `sha256:7eabde5b…`, as C |
| Model · host · runner | `claude-haiku-4-5-20251001` · Claude Code 2.1.270 · `@ktlsr/assay@0.4.4`, `acceptEdits`, `--concurrency 4`, 10 attempts per case | same | same but Claude Code **2.1.271** | as C (2.1.271) | as C (2.1.271) |
| Instruction file | [`fixtures/phrase-binding/CLAUDE.md`](../fixtures/phrase-binding/CLAUDE.md) in an ancestor of every working directory | none | [`fixtures/phrase-binding-stop/CLAUDE.md`](../fixtures/phrase-binding-stop/CLAUDE.md) — arm A's file byte for byte, plus one line | [`fixtures/phrase-binding-template/CLAUDE.md`](../fixtures/phrase-binding-template/CLAUDE.md) — arm C's, one sentence changed | [`fixtures/phrase-binding-slot/CLAUDE.md`](../fixtures/phrase-binding-slot/CLAUDE.md) — arm A's byte for byte, plus one line |

---

## Headline

1. **With the table, every skill fired on its own cases.** The seven that never
   fire went from **0/90 to 90/90**; all sixteen scored cases from **49/160 to
   160/160**. Not one activation reached the wrong skill, and no negative case
   fired in either arm (0/30 each). For eight skills the per-skill intervals
   separate; the other five already fired without the table.
2. **The edit-shaped bypass disappeared.** Attempts that skipped every skill and
   edited the file anyway: **84/160 without the table, 0/160 with it.**
3. **But fewer requests were carried out.** Once a skill fires, its workflow
   tends to ask the user questions before acting — and in a non-interactive run
   nobody answers. Where the prompt asks for a change, a file was written in
   **81/100 attempts without the table and 40/100 with it**. Where the prompt can
   be answered in the reply, the answer was delivered in **66/70 vs 51/70** (read
   by hand). The table moves the work from the base model to the skills, and the
   skills stop to ask.
4. **`product-marketing` now fires 20/20 — and still does not update its file.**
   It updated `.agents/product-marketing.md` in 2 of 20 attempts (1 of 20 without
   the table) and asked questions in the rest. What changed is that it no longer
   forks: without the table, positioning went to host memory or a new file in
   18/20; with it, 0/20.
5. **The shared context file is read far more often.** 101 of 170 activations
   read `.agents/product-marketing.md` with the table (59%), 5 of 50 without (10%).
6. **Arm C (§7): a standing "act unless it must block" rule keeps the routing
   and does not buy the work back.** Activation stays at arm A's 160/160;
   change requests written rise 40 → 52 of 100 and answers delivered 51 → 56 of
   70, both still overlapping arm A. The rule's own marker — one line naming
   the fork taken — appears in 5 of 170 attempts.
7. **Arms D and E (§8–§10): a mandatory slot gets followed, but it isn't
   honest; a template barely moves the line, and neither buys the work back.**
   Activation is 160/160 in every arm that has the table. Change requests
   written: D **40/100**, E **32/100** (A 40, C 52, B 81). Arm E's slot closes
   169 of 200 replies, and 162 of those say "none". That includes **34 of 40**
   attempts on the four cases built around a choice, and all ten "$49 or $79"
   replies, which answer "$49" and then write "Forks: none". Arm D's template
   line, read by hand, appears in 15 of 170 attempts (C: 5), and 12 of the 15
   name the table's skill routing as "the fork", not a choice in the work.

**What this says about the seven.** The design asked whether they fail on
routing judgment or because edit-shaped requests skip routing altogether. It is
routing: given a lookup, the model follows it 160 times in 160, including on
the edit-shaped requests it otherwise answers by editing the file. Nothing about
these skills stops the model from using them. It does not pick them when it has
only the descriptions to go on. The fix works, and it has a price: the skills
it routes to ask before they act.

---

## 1. Activation matrices

Rows are the expected winner, columns the first marketing skill to fire. Each
cell is **A · B** — arm A left of the dot, arm B right. (Arm C's matrix, which
is arm A's, is in §7.1.)

| expected \ fired | none | `ai-seo` | `cold-email` | `copy-editing` | `cro` | `emails` | `onboarding` | `paywalls` | `popups` | `product-marketing` | `programmatic-seo` | `schema` | `seo-audit` | `signup` |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `signup` | 0 · **10** | | | | | | | | | | | | | **10** · 0 |
| `cro` | 0 · **13** | | | | **20** · 7 | | | | | | | | | |
| `popups` | 0 · **20** | | | | | | | | **20** · 0 | | | | | |
| `paywalls` | 0 · **10** | | | | | | | **10** · 0 | | | | | | |
| `onboarding` | 0 · **10** | | | | | | **10** · 0 | | | | | | | |
| `copy-editing` | 0 · **10** | | | **10** · 0 | | | | | | | | | | |
| `emails` | 0 · 1 | | | | | 10 · 9 | | | | | | | | |
| `cold-email` | 0 · 3 | | 10 · 7 | | | | | | | | | | | |
| `seo-audit` | 0 · 2 | 0 · 1 | | | | | | | | | | | 10 · 7 | |
| `ai-seo` | | 10 · 10 | | | | | | | | | | | | |
| `programmatic-seo` | 0 · **10** | | | | | | | | | | **10** · 0 | | | |
| `schema` | 0 · 1 | | | | | | | | | | | 10 · 9 | | |
| `product-marketing` | 0 · **20** | | | | | | | | | **20** · 0 | | | | |

Arm A is a clean diagonal. Arm B is the collision report's picture again:
everything off the diagonal sits in *none*, bar one `seo-audit` case that
reached `ai-seo`.

The contested headline case (either `copywriting` or `copy-editing` accepted):
**A `copywriting` ×10, B none ×10.** In arm A it is no longer contested — the
table puts "write a better headline" under `copywriting`, by construction.

Host-bundled skills: `run` fired 5 times in A, always after a marketing skill
(`signup` ×4, `onboarding` ×1), and once in B, on its own, on the onboarding case.

## 2. Win rate per skill

Own cases only; a win is the expected skill firing first. 95% Wilson intervals.
`·` marks the seven that never fired in the v2 collision run.

| skill | A | B | intervals |
| --- | --- | --- | --- |
| `signup` · | 10/10 (72–100%) | 0/10 (0–28%) | **separate** |
| `popups` · | 20/20 (84–100%) | 0/20 (0–16%) | **separate** |
| `paywalls` · | 10/10 (72–100%) | 0/10 (0–28%) | **separate** |
| `onboarding` · | 10/10 (72–100%) | 0/10 (0–28%) | **separate** |
| `copy-editing` · | 10/10 (72–100%) | 0/10 (0–28%) | **separate** |
| `programmatic-seo` · | 10/10 (72–100%) | 0/10 (0–28%) | **separate** |
| `product-marketing` · | 20/20 (84–100%) | 0/20 (0–16%) | **separate** |
| `cro` | 20/20 (84–100%) | 7/20 (18–57%) | **separate** |
| `cold-email` | 10/10 (72–100%) | 7/10 (40–89%) | overlap |
| `seo-audit` | 10/10 (72–100%) | 7/10 (40–89%) | overlap |
| `emails` | 10/10 (72–100%) | 9/10 (60–98%) | overlap |
| `schema` | 10/10 (72–100%) | 9/10 (60–98%) | overlap |
| `ai-seo` | 10/10 (72–100%) | 10/10 (72–100%) | overlap |

| pooled | A | B | intervals |
| --- | --- | --- | --- |
| the seven | 90/90 (96–100%) | 0/90 (0–4%) | **separate** |
| all sixteen scored cases | 160/160 (98–100%) | 49/160 (24–38%) | **separate** |

**The main question — do the seven fire with the table? Yes, every time.**
Eight skills separate. The five that overlap are the ones that already fired
without the table; they have no room to improve. Their point estimates all rise,
but at ten attempts none of those gains is distinguishable from noise.

## 3. The edit-shaped bypass

Scored attempts in which no marketing skill fired and files were written anyway:

| | A | B |
| --- | --- | --- |
| bypass | **0/160** (0–2%) | **84/160** (45–60%) |
| no marketing skill fired at all | 0 | 110 |
| a skill fired after the first edit | 0 | 0 |

With the table the bypass is gone. A skill fires first in every scored attempt,
before any edit.

## 4. What the table costs: the skills ask before acting

**Action cases** — ten prompts that ask for a change in the workspace, so a
written file is what completion looks like:

| case | A wrote files | B wrote files |
| --- | --- | --- |
| registration form, fix it | 9 | 10 |
| newsletter form, get more submissions | **0** | 8 |
| exit modal, rewrite the words | 6 | 7 |
| limit-reached screen, rework it | 7 | 10 |
| empty first session, fix it | 4 | 10 |
| wordy paragraph, tighten it | 6 | 10 |
| not cited by ChatGPT, change that | 0 | 0 |
| one page per integration, build them | **0** | 10 |
| star rating in Google, make it happen | 8 | 7 |
| stale positioning, update the context | **0** | 9 |
| **total** | **40/100** (31–50%) | **81/100** (72–87%) — **separate** |

**Answer cases** — seven prompts that can be finished in the reply (pricing
diagnosis, when and to whom to show the modal, the headline, the email plan, the
cold emails, the SEO diagnosis, the ICP write-up). Each reply was read and
classed as *delivered* (the thing asked for is in it; an offer or question
afterwards is fine) or *not* (it asks before delivering, or stops):

| | delivered | not delivered |
| --- | --- | --- |
| A | **51/70** | 19 — emails 6, ICP 7, and one or two each on modal timing, pricing, headline, cold email, SEO |
| B | **66/70** | 4 — emails 2, cold email 2 |

The replies make the mechanism plain. With the table, a typical attempt reads
the context file, diagnoses the problem, and then ends:

> Before I rework it, I need a few quick clarifications: …

> Would you like me to implement these changes to your index.html?

(limit-reached screen and newsletter form. The newsletter form wrote nothing in
any of its ten arm-A attempts; each ended on an offer to make the change or a
question.)

Without the table, the base model makes a call and writes the file. The skills
are written for a conversation, and in one the user would answer and the work
would continue. So part of this cost belongs to non-interactive measurement.
But it is still what these skills do when they fire: they ask first. The table
decides which path a request takes, and the skills' path starts with questions.

**A side effect of activation.** Loading a skill tells the model the skill's base
directory. In 15 arm-A attempts (1 in B) Haiku then resolved workspace files
against that directory — `…/assay-skill-…/pricing.html` — and the read was
refused as outside the working directory. Three of those attempts ended by
asking the user for permission to read files that were in the workspace all
along: "I found your pricing page and product marketing context, but I need
permission to read them". This follows activation, not the table; arm A has three times as many
activations.

## 5. `product-marketing` and its context file

| | A | B |
| --- | --- | --- |
| `product-marketing` fired on its two cases | **20/20** | 0/20 |
| updated `.agents/product-marketing.md` | 2/20 | 1/20 |
| wrote positioning somewhere else | **0/20** | **18/20** — host memory 8, a new `POSITIONING*.md` or similar 10 |
| wrote nothing | 18/20 | 1/20 |

In arm A the skill fires, finds the file, summarises what is stale, and asks
what the new market looks like. In a conversation that is the right move. Here
the file stays stale — but it is no longer contradicted by a parallel file, which
is what happened in 18 of 20 attempts without the table.

**Does every activated skill read the context file first?**

| | read it | before the first edit |
| --- | --- | --- |
| A, activations | 101/170 (59%) | all 101 |
| B, activations | 5/50 (10%) | all 5 |
| B, attempts where nothing fired | 14/150 | — |

The v2 collision run measured 17/50 for arm B's condition, on Claude Code 2.1.267.
The host has moved since, so this report compares only its own two arms.

## 6. Guard rails

- **Negatives:** 0/30 fired in either arm. The Postgres case has no query in the
  prompt, and both arms asked for it in 10/10. The crash fix was written in
  10/10 in both.
- **The rule's "add a row" clause** was never acted on: no arm-A attempt touched
  a `CLAUDE.md`. (Six arm-B attempts searched for one, four of them on the
  positioning cases, looking for somewhere to store the new positioning.)
- **Host `CLAUDE.md` leak:** 0/400 attempts mention it — see *Instrument* below.

---

## 7. Arm C — the table plus a standing default

§4 measured what the table costs: the skills it routes ask before they act.
Shown that, [jimy-r replied](https://github.com/coreyhaines31/marketingskills/discussions/584)
with the rule he runs next to the table, and asked for it as a third arm:

> The fires-and-waits result is the one to act on first. A skill that asks
> before it acts is right in a conversation and fatal headless, and the table
> only exposed it. What I run is a declared posture per skill. A step that must
> block carries an explicit gate marker. Everything else takes a reasoned
> default and prepends one line to its output naming the fork it took and why,
> so a headless run finishes and a human redirects it afterwards. […] I would
> expect most of the gap on change requests to close under that rule.

Asked where the posture lives, he split it:

> The default lives once in the instruction file, as the rule from my last
> reply. The exceptions live in the skill body, as a gate marker on the specific
> step that has to block […]. For your arm, that makes it one row in the
> instruction file. It measures the rule, not how many skill authors adopted a
> field.

So arm C is arm A plus that one rule, and **no skill was edited**: the gate
markers are the skill author's half and these fourteen skills are not ours.
The question is whether the default alone brings the delivery back **without**
disturbing the routing.

The file is arm A's, byte for byte, with one block appended:

> ## Default
>
> Default: if a step does not clearly require blocking, take a reasonable default
> and continue. Add one line at the top of your output: which fork you took and
> why. Stop and ask only on steps that are destructive, irreversible, or that
> need input only the user can give.

Everything else matches arm A: same suite
bytes, same skills and hash, same model, same permission mode, same layout one
letter apart (`TEMP=D:\pb-C\tmp`, the file at `D:\pb-C\CLAUDE.md`).

**Two deviations from the request, both measured before the run.**

1. **Runner 0.4.4, not 0.4.5.** 0.4.5 closes the host `CLAUDE.md` leak by
   excluding every instruction file in every **ancestor** of the working
   directory — which is exactly where this experiment's table lives. Through the
   published adapters, in arm C's layout, with a canary line in the file:

   | adapter | canary in the request the host sends | table row in it | record |
   | --- | --- | --- | --- |
   | 0.4.4 | 1 | 1 | not measured |
   | 0.4.5 | 0 | 0 | `environment.memory: []` |

   On 0.4.5 arm C would have been arm B with extra steps. Arms A and B are on
   0.4.4, so 0.4.4 is also what "everything else the same" requires.
2. **Host 2.1.271, not 2.1.270.** The machine's Claude Code moved on between the
   arms. The old binary is still on disk but the version files are launchers:
   staged first on `PATH`, the run record still says 2.1.271. Pinning it back
   means changing the installed version on the user's machine, which was not
   done. So arm C's environment hash differs from arm A's by design of the host,
   not of the experiment — and a patch-level host change is the one confound
   this arm cannot rule out.

### 7.1 Activation: arm A's numbers, unchanged

| | A | B | C |
| --- | --- | --- | --- |
| the seven that never fired | 90/90 | 0/90 | **90/90** |
| all 16 scored cases | 160/160 | 49/160 | **160/160** |
| activations that reached another skill | 0 | 1 | **0** |
| contested headline case | `copywriting` ×10 | none ×10 | `copywriting` ×10 |
| edit-shaped bypass | 0/160 | 84/160 | **0/160** |
| negatives that fired | 0/30 | 0/30 | **0/30** |

Arm C's matrix is arm A's: every scored case's expected skill fires first in
every attempt, nothing lands off the diagonal, and the *none* column is empty.
Per skill, all thirteen rows are 10/10 or 20/20, as in arm A.

**The rule does not touch routing.** That was the thing to check first: a
standing default that tells the model to act could have pulled it back to the
edit-shaped bypass of arm B. It did not, in 160 of 160.

### 7.2 Delivery: the estimate rises, the interval does not separate

**Action cases** — the ten prompts that ask for a change, where a written file is
what completion looks like:

| case | A | B | C |
| --- | --- | --- | --- |
| registration form, fix it | 9 | 10 | 10 |
| newsletter form, get more submissions | 0 | 8 | 0 |
| exit modal, rewrite the words | 6 | 7 | **10** |
| limit-reached screen, rework it | 7 | 10 | **10** |
| empty first session, fix it | 4 | 10 | 5 |
| wordy paragraph, tighten it | 6 | 10 | 6 |
| not cited by ChatGPT, change that | 0 | 0 | 0 |
| one page per integration, build them | 0 | 10 | 2 |
| star rating in Google, make it happen | 8 | 7 | 9 |
| stale positioning, update the context | 0 | 9 | 0 |
| **total** | **40/100** (31–50%) | **81/100** (72–87%) | **52/100** (42–62%) |

A vs C **overlap**; B vs C separate. The gain is +12 attempts and it is
concentrated in two cases (exit modal 6→10, limit screen 7→10). The three cases
that wrote nothing in arm A write nothing in arm C either: the newsletter form,
the integration pages (2/10), and the positioning file — the places where the
skill's workflow wants an answer from the user before it will act.

**Answer cases** — the seven prompts that can be finished in the reply, read by
hand under §4's rule (delivered = the thing asked for is in the reply; a question
or offer afterwards is fine):

| case | A | B | C |
| --- | --- | --- | --- |
| pricing diagnosis | — | — | 9/10 |
| when and to whom the modal should appear | — | — | 8/10 |
| a better headline | — | — | 10/10 |
| the welcome-email plan | — | — | 7/10 |
| the cold emails | — | — | 10/10 |
| the SEO diagnosis | — | — | 10/10 |
| the ICP write-up | — | — | 2/10 |
| **total** | **51/70** (61–82%) | **66/70** (86–98%) | **56/70** (69–88%) |

(Arm A and B were not re-read; their totals and the not-delivered breakdown in §4
stand as published. Arm C's per-case column is new.)

Arm C overlaps both A and B here. The ICP case is where it stays stuck: 2 of 10
replies contain a positioning write-up, the other 8 summarise the stale file and
ask which sections to work through. `product-marketing` is the skill whose
workflow asks the most, and one line of standing default does not overrule it.

**Both kinds of work together:** A 91/170 (46–61%), B 147/170 (81–91%),
C **108/170** (56–70%). A vs C overlap; B vs C separate.

### 7.3 Was the rule actually taken?

The rule asks for a visible marker: one line at the top of the output naming the
fork taken. Counting attempts whose output declares a choice anywhere — the same
detector on all three arms:

| | A | B | C |
| --- | --- | --- | --- |
| a fork line at the top of the first output | 0/170 | 0/170 | 1/170 |
| a choice declared anywhere in the output | 0/170 | 0/170 | **5/170** (1–7%) |

Zero in the two arms without the rule, so the detector has no false positives on
340 attempts. The five in arm C read like the rule asked:

> **→ Fork taken: Minimal fields + proper UX.** 50% drop-off is form structure,
> not marketing message.

> **Taking the CRO fork:** analyzing your pricing page as a conversion blocker
> for a technical product (Meterly) where cold traffic lands with no product
> context.

**In 165 of 170 attempts the model did not do what the line asked.** That is the
honest reading of this arm: the instruction was in context (the table in the same
file routed 160 of 160), and the half of it that is externally visible was
ignored. So the small, non-separating delivery gain sits on top of a rule that
was mostly not followed — not on a rule that was followed and did not help.

### 7.4 Guard rails

- Negatives: 0/30 fired, as in both other arms.
- Host `CLAUDE.md` leak: 0/200 attempts mention `graphify`.
- `CLAUDE.md` touched by the agent: 2 attempts, both a `Glob` that found nothing
  (arm A 0, arm B 6).
- Positioning written somewhere else: 0/20 (arm A 0/20, arm B 18/20). One attempt
  updated `.agents/product-marketing.md`; the other 19 wrote nothing.
- Reads refused because the path was resolved against the skill's own directory:
  17 attempts (arm A 15, arm B 1) — a side effect of activation, not of the rule.

### 7.5 What arm C says

- **The routing and the asking are separable, and the rule only reached one of
  them.** Activation stayed at arm A's 160/160 — adding a "just act" default did
  not pull the model back to editing files without routing.
- **Delivery did not measurably recover.** 40 → 52 of 100 action cases and
  51 → 56 of 70 answers; both intervals still overlap arm A, and both remain
  below arm B, which has no instruction file at all.
- **The likeliest reason is that the rule was not followed.** Its own marker
  appears in 5 of 170 attempts. A one-line default in the instruction file does
  not outrank a skill body that says to ask; jimy-r's architecture marks those
  exceptions inside the skills, and those skills are not ours to edit.
- **Against the expectation.** jimy-r expected "most of the gap on change
  requests to close under that rule". The gap between arm A and arm B on those
  cases is 41 attempts; arm C closes 12 of them, and the interval still covers
  arm A. On this suite, with this model, the rule alone does not do it.
- **What this does not say.** It measures the default, not the posture. The
  other half of jimy-r's design — a gate marker on the specific step that must
  block, inside each skill body — is not in these skills and was not added; his
  own split predicts that is where the asking would be overruled. Untested too:
  whether a larger model follows the line more often than 5 of 170, and whether
  the patch-level host change (2.1.270 → 2.1.271) accounts for part of the +12.

---

## 8. Arm D — the fork line as a literal template

Arm C's rule described the marker ("one line at the top of your output: which
fork you took and why"), and the model produced it 5 times in 170. Arm D asks
whether the wording was the problem. The file is arm C's, with one sentence
changed from an instruction to the template itself:

> Add one line at the top of your output, in exactly this form: "Picking X over
> Y because R; redirect if wrong."

Everything else is arm C's: the table, the default, the stop conditions, the
runner (0.4.4), the host (2.1.271), and the layout (`D:\pb-D`).

### 8.1 Is the line there?

Scored with `file_content_matches` (§10.3) over each attempt's messages, then
every hit read by hand:

| | C | D |
| --- | --- | --- |
| the template, exactly (`Picking … over … because …; redirect if wrong`), first line of the first output | 0/170 | **1/170** |
| `Picking … over … because` anywhere | 0/170 | 3/170 |
| a line declaring the fork taken, any form, read by hand | 5/170 (1–7%) | **15/170** (5–14%) |

The intervals overlap. And the fifteen are not what the template asks for. In
**12** of them the "fork" is the routing the table has just made:

> Picking `marketing-skills:signup` skill because the phrase "never finish
> creating their account" / "fix the form" is in the command shortcuts table;
> redirect if wrong.

In **3** it is a choice in the work itself:

> **Picking a value-focused rewrite over generic "Wait!" because the current
> copy lacks any compelling reason to stay.** Redirect if this misses the mark.

Most drop the "over Y" part. Once the model is given the template, the fork it
most often reports is the one it did not make: the skill was chosen by a lookup.

### 8.2 Delivery

Change requests written: **D 40/100** (31–50%), the same as arm A. Against C
(52/100), D overlaps; against B (81/100), it separates. The case-by-case table
is in §10.2. The template did not keep C's point-estimate gain.

## 9. Arm E — a mandatory closing slot

Arm E drops the default altogether and asks for something every reply has to
carry, whether or not there was a fork. The file is arm A's, byte for byte,
with one block appended:

> ## Forks
>
> End every reply with either "Forks: none" or "Forks: picked X over Y because R".

So a missing slot is itself a measurement, and "none" is an answer that can be
wrong.

### 9.1 Is the slot there?

Scored with `file_content_matches` on the attempt's last message — the reply —
anchored at its end:

| | E |
| --- | --- |
| reply ends with the slot in the given form | **169/200** (79–89%) |
| — of which `Forks: none` | 162 |
| — of which `Forks: picked X over Y because R` | 7 |
| a `Forks:` line in the reply, any form | 188/200 (90–97%) |
| no `Forks:` line at all | 12/200 |

Arms A–D: 0/200 each, so the check has no false positives on 800 attempts.

The 19 replies with a `Forks:` line in some other form, read by hand: 15 name a
fork in their own words ("Forks: Chose exit-intent-only approach over always-on
newsletter because …"), 3 say none and give a reason, and 1 is neither. The 12
without a slot all stop short of the work: 4 ask for permission to read files
already in the workspace (the skill-directory side effect of §4), and the other
8 end by asking the user for input or by listing what they would do next.

**The slot is followed where the fork line was not**: 188 of 200 replies carry
it, against C's 5 of 170 and D's 15 of 170. A requirement at a fixed place in
every reply is taken up; one that depends on whether there was a fork, and
belongs at the top, mostly is not.

### 9.2 Is it honest? "none" on the cases built around a choice

Four cases ask the model to choose between alternatives. They were fixed before
any arm E attempt was read:

| case | the choice in the prompt | slot | `none` |
| --- | --- | --- | --- |
| Pro plan price (negative) | "$49 or $79" | 10/10 | **10** |
| exit modal timing | "when and to whom" | 8/10 (+2 in another form, both naming a fork) | **8** |
| stale positioning | update the shared file, or write elsewhere (§5) | 8/10 | **8** |
| ICP write-up | which customer, which position | 8/10 (+1 in another form, neither) | **8** |
| **total** | | 34/40 in the given form | **34/40** (71–93%) |

**Every slot in the given form on these cases says "none".** The only forks
declared on them are the two exit-modal replies that used their own wording.
The pricing case shows the miss most clearly: all ten replies answer "$49", the
price already in `pricing.html`, and end with "Forks: none". The model does not
treat "$49 or $79" as a choice it made; it reports the current value and marks
no fork. That is a scorable miss by the arm's own rule, in 10 of 10.

Across the whole run, 22 of 188 slot lines name a fork (7 in the given form, 15
in another). "None" is the default the model reaches for, not a report.

### 9.3 Delivery

Change requests written: **E 32/100** (24–42%). It overlaps A (40) and D (40)
and separates from both C (52) and B (81). The drop is concentrated on the
empty first session (A 4 → E 0) and the registration form (9 → 5; four of the
five that wrote nothing asked for permission to read files, the side effect of
§4 — 17 attempts in E hit it, 15 in A). The
slot is appended at the end of a reply; it does not change whether the reply
acts first.

`product-marketing`: 20/20 activations, nothing written in 20/20 (A 18/20).

## 10. All five arms side by side

### 10.1 Activation — the rules do not disturb the table

| | A | B | C | D | E |
| --- | --- | --- | --- | --- | --- |
| the seven that never fired | 90/90 | 0/90 | 90/90 | **90/90** | **90/90** |
| all 16 scored cases | 160/160 | 49/160 | 160/160 | **160/160** | **160/160** |
| activations that reached another skill | 0 | 1 | 0 | 0 | 0 |
| contested headline case | `copywriting` ×10 | none ×10 | `copywriting` ×10 | `copywriting` ×10 | `copywriting` ×10 |
| edit-shaped bypass | 0/160 | 84/160 | 0/160 | 0/160 | 0/160 |
| negatives that fired | 0/30 | 0/30 | 0/30 | 0/30 | 0/30 |

Every arm with the table has the same clean diagonal; all thirteen per-skill
rows are 10/10 or 20/20 in C, D and E. None of the three rules pulled the model
off the lookup. Activation and output format are separate layers here: the
rules change what the reply says, not which skill writes it. The full five-arm
matrix is in the [analysis file](marketingskills.phrase-binding.analysis.md).

### 10.2 Delivery — change requests written

| case | A | B | C | D | E |
| --- | --- | --- | --- | --- | --- |
| registration form, fix it | 9 | 10 | 10 | 7 | 5 |
| newsletter form, get more submissions | 0 | 8 | 0 | 0 | 0 |
| exit modal, rewrite the words | 6 | 7 | 10 | 6 | 4 |
| limit-reached screen, rework it | 7 | 10 | 10 | 5 | 6 |
| empty first session, fix it | 4 | 10 | 5 | 4 | 0 |
| wordy paragraph, tighten it | 6 | 10 | 6 | 8 | 9 |
| not cited by ChatGPT, change that | 0 | 0 | 0 | 0 | 0 |
| one page per integration, build them | 0 | 10 | 2 | 0 | 0 |
| star rating in Google, make it happen | 8 | 7 | 9 | 10 | 8 |
| stale positioning, update the context | 0 | 9 | 0 | 0 | 0 |
| **total** | **40/100** (31–50%) | **81/100** (72–87%) | **52/100** (42–62%) | **40/100** (31–50%) | **32/100** (24–42%) |

B separates from all four table arms. Among the table arms only C and E
separate, and they sit at opposite ends. The three cases that never write with
the table — newsletter form, integration pages, positioning — write nothing
under any of the three rules. Answer cases were not read by hand for D and E;
the question put to these arms was change requests and the output markers.

### 10.3 How the output format is scored

`tools/slot.mjs` passes each attempt's final reply (or, for the template, each
message's first line) to Assay's own `file_content_matches` evaluator from
`@ktlsr/assay-core` 0.4.4, as a one-file workspace. The suite is unchanged
(its hash is the same in all five runs), no assertion was added to it, and each
check is pass or fail — no new verdict state. The patterns tolerate markdown
emphasis around the line and nothing else. The script checks itself on
constructed replies before it reads a run, and it scores 0 on arms A–C (600
attempts) for both markers. The per-attempt slot lines are in the analysis
file for reading.

### 10.4 What D and E say

- **The wording of the rule is not what was missing.** A literal template
  moved C's 5/170 to 15/170. The intervals overlap, and 12 of the 15 name the
  table's routing as the fork.
- **A slot the reply must always carry is followed, and it says "none".** 188
  of 200 replies carry it; on the four cases built around a choice, every slot
  in the given form says "none", including ten "$49 or $79" replies that pick
  $49. The format is taken up; the self-report inside it is not reliable at this
  model size.
- **No output rule brought the work back.** Change requests: C 52, D 40, E 32
  against A's 40 and B's 81. What stops the work is the skills' own
  ask-first steps (§4), and a rule about what to print does not reach them.
- **The table's routing held under every rule**: 160/160 in A, C, D and E.

---

## Fast run first, then the full run

The request was to start with `--fast` (3 attempts per case) and decide.

| `--fast` | A `09c739c7` | B `480df1cd` |
| --- | --- | --- |
| the seven | 27/27 | 0/27 |
| all scored | 48/48 | 16/48 |
| bypass | 0/48 | 26/48 |
| action cases wrote files | 15/30 | 27/30 |

The delta was unmistakable, and the full run was still needed, for three reasons:

1. **The per-skill question cannot be answered at N=3.** Under Wilson, 0/3 is
   0–56% and 3/3 is 44–100%: they overlap. Ten of the thirteen skills have one
   case, so at three attempts they cannot separate whatever happens.
2. **The fast runs carried a host leak** (below). The full runs were moved to a
   location where it does not happen.
3. **The cost in item 3 of the headline** showed up in the fast run (15/30 vs 27/30)
   and needed the larger N to size.

The fast runs are kept as the early warning. Every number in the sections above
comes from the full runs.

## Instrument

**A host leak, found during this experiment.** Assay starts each attempt with an
empty `CLAUDE_CONFIG_DIR`, so the user's `~/.claude/CLAUDE.md` should not load.
It did. On Windows `%TEMP%` lives under the home directory, so every working
directory has the home directory as an ancestor, and Claude Code's walk up the
tree loads `<home>/.claude/CLAUDE.md` as if it were a project's. On this host
that file names one tool, `graphify`, which is how the leak showed: the model
called the fixture's product "graphify" in outputs. It surfaced in 4 of 60 fast
arm-B attempts (the fast arm A loaded the file too, but never used the name) and
in earlier run records, including the v2 collision run.
A two-attempt check through the real adapter settled the cause: working
directory under the home directory → the model quotes the line; on `D:` → it
does not. **The full runs were made with `TEMP` on `D:`** (`D:\pb-A\tmp`,
`D:\pb-B\tmp`), and 0 of 400 attempts mention it. The fix belongs in Assay.

**Runs that were discarded.** The first full arm A
(`run-2026-09-13T12-23-34-523Z-7b1eae19`) hit the account's session limit after
184 attempts; 16 negatives were left `unknown`. The arm B started straight after
it (`run-2026-09-13T12-45-56-739Z-865682c3`) was 200/200 `unknown`. Neither is
used. Arm B was re-run after the limit reset, then arm A was re-run in full, so
both measured runs are complete records of the same suite. Before arm A
started, a scripted check confirmed that B had no unknowns and that both B's
recorded host and the installed `claude` were 2.1.270.

**The analyser** is `tools/phrase_binding.py`, built on `tools/collide.py`. Its
matrix, activation and bypass counts reproduce `collide.py`'s on the published v3
fast run (`912ad216`), checked before any new attempt was read. Its full output
for the measured runs is
[`marketingskills.phrase-binding.analysis.md`](marketingskills.phrase-binding.analysis.md).
It takes any number of arms; adding arm C left every arm A and arm B count in
sections 1–6 identical, which was checked against the two-arm output before the
file was regenerated. Adding D and E was checked the same way: the three-arm
output was byte-identical to the committed file before the five-arm output
replaced it. The output-format checks for §8–§10 are in `tools/slot.mjs`,
appended to the same analysis file.

## Limitations

- **Best case for the table.** Every row holds phrases lifted from the prompts
  it routes. This measures whether a matching lookup is followed — it is, 160
  times in 160 — not whether it generalises to wording nobody wrote down.
  jimy-r's rule covers "close variants"; that needs a paraphrased suite.
- **One model, Haiku 4.5.** A larger model may reach for skills more readily
  without the table, and may ask fewer questions with it.
- **Non-interactive.** The cost in §4 is measured where no one answers. In a
  conversation the questions would be answered and the work would go on; how
  much of the gap closes then is not measured here.
- **The answer-case classification is a reading**, 140 replies by one reader,
  with the rule stated above. The action-case numbers need no judgement.
- **One fixture, one product, ten attempts per case.**
- **Arm C carries a host drift.** Arms A and B ran on Claude Code 2.1.270,
  arm C on 2.1.271, because the machine updated between them and the installed
  version could not be pinned back without changing it for the user. The
  environment hashes differ accordingly; a patch-level host change is the one
  confound §7 cannot rule out.
- **Arms D and E carry the same host drift as C.** They ran on 2026-09-26 on
  Claude Code **2.1.271**, as the run records and the run logs' own
  `claude --version` line show — the same host as C, one patch past A and B.
  So D and E compare to C with no host change, and to A and B across the
  2.1.270 → 2.1.271 step. (The version was expected to have moved to 2.1.281 by
  then; it had not, and nothing was changed on the machine.)
- **Arms C, D and E had to stay on runner 0.4.4.** From 0.4.5 on, Assay excludes
  instruction files in every ancestor of the working directory, which is where
  this experiment's table lives; measured in §7.
- **The output markers are pattern checks plus a reading.** `file_content_matches`
  decides whether a line in the given form is present; whether a declared fork is
  a real one, and whether a "none" is wrong, is read by hand against four cases
  fixed before the arm E attempts were read. Other readers may count more cases
  as forked; none would count fewer than the "$49 or $79" case.

## Reproduce

```
# arm A: the table in an ancestor of every working directory
mkdir D:\pb-A\tmp ; copy fixtures\phrase-binding\CLAUDE.md D:\pb-A\
set TEMP=D:\pb-A\tmp & set TMP=D:\pb-A\tmp
npx @ktlsr/assay@0.4.4 run suites/marketingskills.collide.v3.suite.yaml --skill ./skills/marketing-skills-collide --concurrency 4

# arm B: the same with an empty D:\pb-B and no file

# arm C: the table plus the standing default, same runner as A and B
mkdir D:\pb-C\tmp ; copy fixtures\phrase-binding-stop\CLAUDE.md D:\pb-C\
set TEMP=D:\pb-C\tmp & set TMP=D:\pb-C\tmp
npx @ktlsr/assay@0.4.4 run suites/marketingskills.collide.v3.suite.yaml --skill ./skills/marketing-skills-collide --concurrency 4

# arms D and E: the same, with fixtures\phrase-binding-template (D:\pb-D)
# and fixtures\phrase-binding-slot (D:\pb-E)

python tools/phrase_binding.py .assay/runs/<A>.json .assay/runs/<B>.json .assay/runs/<C>.json .assay/runs/<D>.json .assay/runs/<E>.json
node tools/slot.mjs <npx cache>/@ktlsr/assay-core/dist/index.js .assay/runs/<A>.json … .assay/runs/<E>.json
```

On Windows, keep `TEMP` off the home directory in both arms, or the host's
`~/.claude/CLAUDE.md` loads into every attempt.

---

## Design

### Where this comes from

After the [collision measurement](marketingskills.collide.md) was posted as
[marketingskills discussion #584](https://github.com/coreyhaines31/marketingskills/discussions/584),
**jimy-r** replied that the 0/200 for `product-marketing` matched his own roster
of about forty skills, and that the fix that held for him was not in the
descriptions:

> My instruction file carries a table of phrase families to skills […] with a
> standing rule that on a matching phrase the model goes straight to the target,
> with no description matching involved. Activation for those became
> deterministic, because the routing is a lookup, not a judgment.

He then shared the shape and a working subset of his table in the same thread,
and asked for exactly this experiment: "keep the rule and the two-column shape
and write one row per skill with the phrases your cases actually use. The delta
you measure will then be about the mechanism, not about my phrases."
The public sample is
[`samples/CLAUDE.md.example`](https://github.com/jimy-r/agent-workspace-architecture/blob/main/samples/CLAUDE.md.example);
the write-up is
[META_ARCHITECTURE §Command Shortcuts](https://github.com/jimy-r/agent-workspace-architecture/blob/main/META_ARCHITECTURE.md#command-shortcuts).

### Why two arms

The collision run showed *that* seven skills never fire. It could not say
*why*: the model may be judging the descriptions and choosing none of them
(**routing judgment**), or it may skip the choice altogether because the request
is answerable by editing a file (**edit-shaped bypass**). A lookup table takes
the judgment away. So:

- if the seven start firing with the table, the failure was in the routing
  judgment, and a table is a fix;
- if they still do not fire, the model is not consulting routing at all on
  edit-shaped requests, and no description or table rewrite will help.

One arm with the table, one without, everything else identical, is the smallest
design that tells those apart.

| | Arm A | Arm B |
| --- | --- | --- |
| Instruction file | `CLAUDE.md` with the rule and table, in an **ancestor** of every attempt's working directory | none |
| Suite | `suites/marketingskills.collide.v3.suite.yaml`, byte-identical | same |
| Skills | the same 14, `skills/marketing-skills-collide/`, same hash | same |
| Model, mode | `claude-haiku-4-5-20251001`, `acceptEdits` | same |
| Runner | `@ktlsr/assay@0.4.4 run … --concurrency 4` (first `--fast`, then full) | same |
| Attempts | 20 cases × 10 (fast: × 3) | 20 cases × 10 (fast: × 3) |
| `TEMP` | `D:\pb-A\tmp`, the table at `D:\pb-A\CLAUDE.md` | `D:\pb-B\tmp`, no file |

Arm B is run fresh, not taken from the published v3 fast run (`912ad216`):
that run is on assay 0.4.3 and Claude Code 2.1.268, and the host has moved since.

### Where the table lives, and how it gets there

jimy-r's table is in his **workspace** `CLAUDE.md` ("A verbal-shortcut table in
the workspace CLAUDE.md"), with each project in a subdirectory beneath it. That
is Claude Code's project scope, loaded from the working directory and every
ancestor of it, not the user-level `~/.claude/CLAUDE.md`.

The assay adapter starts each attempt with an empty, throwaway
`CLAUDE_CONFIG_DIR`, so the user scope cannot be seeded on 0.4.4 without a code
change. The project scope can. The runner creates every working directory with
`mkdtemp(os.tmpdir())`, and `TEMP`/`TMP` are on the adapter's environment
allowlist. Arm A runs with `TEMP=D:\pb-A\tmp` and the table at
`D:\pb-A\CLAUDE.md`; arm B runs with `TEMP=D:\pb-B\tmp` and no file. (The fast
runs used the same layout under the default `%TEMP%`; that location turned out
to leak the host's own `CLAUDE.md` — see *Instrument* — so the full runs moved
to `D:`.) Every working directory in arm A is then a project under a workspace
that carries the table — the layout jimy-r describes. Between the arms only that
file and one letter of the parent directory's name differ; the runner and suite
bytes are the same in both.

**Smoke test before the run.** Through the real 0.4.4 adapter class, with a
canary line in the ancestor file ("If you are asked for the canary word, it is
HELIOTROPE-7") and the same 14-skill plugin: arm A answered `HELIOTROPE-7`, the
no-file control answered `NONE`. In both the fast and the full run, the attempt
and config directories were confirmed to be created under arm A's `tmp`.

Side effects of this placement, all of which favour a clean measurement:

- the file is outside the working directory, so it never shows up in the
  agent's `Glob`/`ls` and cannot be edited under `acceptEdits`;
- it is present on the one case with no fixtures (the Postgres negative);
- `CLAUDE.md` content and the skill listing are both in context from the first
  request, which is what "loads before any skill description is read" amounts to
  in Claude Code.

Rejected: putting the file inside the fixture (visible and editable; in v2 the
positioning case wrote to host memory, `CLAUDE.md` included, in 10 of 10
attempts), and a plugin `SessionStart` hook (changes the plugin under test and
is a different mechanism).

### What was taken from jimy-r, and what was not

**Taken, verbatim:** the standing rule —

> On a matching phrase or a close variant, go directly to the target with no
> clarifying question. For a new target not in the map, ask once, then add a
> row. When there is genuine doubt between two targets, ask.

— and the two-column shape, `Phrase family | Target`, with the left cell a
phrase family separated by `/`, and the section heading his sample uses
(`## Command shortcuts`).

**Not taken:** any of his phrases. His rows point at his own skills; copying
them would measure his wording. Each of our 14 rows instead uses phrases lifted
from **our** case prompts: 34 phrases, 32 verbatim substrings of the case they
route, 2 with a file path replaced by "it". Every positive case has at least one
verbatim phrase in its skill's row. A script checked that no phrase occurs in
another case's prompt or in any of the three negatives.

**Also not taken:** the rest of his instruction file (working principles,
lessons loop, token discipline). Only the mechanism under test goes in.

**Adapted:** targets are written as the plugin-qualified names the Skill tool
uses (`marketing-skills:cro` skill) rather than bare names, so a miss cannot be
put down to name resolution. Rows run two to four phrases, within his two to
seven.

The file: [`fixtures/phrase-binding/CLAUDE.md`](../fixtures/phrase-binding/CLAUDE.md).

### What is measured

Read with `tools/phrase_binding.py`, which takes its per-attempt facts from
`tools/collide.py` — the analyser behind the published collision report. It was
checked against the stored v3 fast run before any new attempt was read: its
matrix, activation and bypass counts reproduce `collide.py`'s on `912ad216`.

- **Activation matrix** per arm: expected winner × first marketing skill to fire.
- **Win rate per skill** on its own cases, 95% Wilson intervals, and whether the
  two arms' intervals separate.
- **The seven** — `signup`, `popups`, `paywalls`, `onboarding`, `copy-editing`,
  `programmatic-seo`, `product-marketing`, which fired 0 times on their own cases
  in the v2 full run — pooled and one by one. This is the main question.
- **Edit-shaped bypass**: scored attempts in which no marketing skill fired and
  files were written anyway.
- **Whether the request was carried out**: for prompts that ask for a change, a
  written file; for prompts answerable in the reply, a reading of the reply.
  (A `?` in the last message was tried as a signal for "asked instead of acted"
  and dropped: read by hand, it missed requests phrased "Please share: …".)
- Guard rails: negatives firing, activations that reached the wrong skill,
  attempts that touched `CLAUDE.md`, and the host `CLAUDE.md` leak.

### What this design cannot say

- **Best case for the table.** The phrases are the prompts' own words, so this
  measures whether a lookup is *followed* when it matches, not whether it
  generalises to phrasings nobody wrote down. jimy-r's rule covers "close
  variants"; this run does not test them.
- **One model, Haiku 4.5.** As in the collision report, rates are a floor.
- **Three attempts per case in `--fast`.** Under Wilson, 0/3 and 3/3 overlap
  (0–56% vs 44–100%), so a single-case skill cannot separate at that N whatever
  happens. That is why the full run (ten per case) was made.
