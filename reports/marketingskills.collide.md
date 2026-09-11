# `marketingskills` — collision between co-installed skills

> **Two runs, one picture.** This report is the full run: **200 attempts** on
> suite **v2**, `run-2026-09-10T11-01-34-914Z-0bec859e` (assay 0.3.2, 10 attempts
> per case). The matrix published on
> [assayctl.dev](https://assayctl.dev/suites/marketing-skills%3Aproduct-marketing)
> is a fast run: **60 attempts** on suite **v3** (the same cases with expected
> winners declared), `run-2026-09-11T14-54-16-671Z-912ad216` (assay 0.4.3,
> `--fast`, 3 attempts per case, trigger layer only). Same picture, different
> resolution: the fast run is an early warning with wide intervals, this one is
> the measurement.

The first measurement in this repository with more than one skill loaded. The
question is not "does this skill fire" but **"when fourteen related skills are
installed together, which one wins each request?"** — and whether the README's
claim that every skill reads `product-marketing` first holds.

| | |
| --- | --- |
| Skills | `coreyhaines31/marketingskills` 2.11.1 @ `5b2c0007766c6a1cf1d53fd8fc73e979e0821022`, clean marketplace install |
| Loaded together | 14 of the 50: `cro`, `signup`, `onboarding`, `popups`, `paywalls`, `copywriting`, `copy-editing`, `emails`, `cold-email`, `seo-audit`, `ai-seo`, `programmatic-seo`, `schema`, `product-marketing` — one plugin, `skills/marketing-skills-collide/` |
| Skill hash | `sha256:aff03848…` |
| Suite | `suites/marketingskills.collide.suite.yaml` v2, `sha256:1d73ceae…` |
| Model | `claude-haiku-4-5-20251001` |
| Host | `claude-code` 2.1.263, Windows 11 Pro |
| Runner | `@ktlsr/assay@0.3.2`, `acceptEdits`, `--concurrency 4` |
| Run | `run-2026-09-10T11-01-34-914Z-0bec859e` · 200 attempts · 0 unknown · $10.18 · 26 min wall |
| Early warning | `--fast` run on v1, 57 attempts, $2.82 — same picture, see *Suite history* |

---

## Headline

1. **The skills almost never collide with each other.** 50 activations; **49
   were the skill the descriptions route to.** The one miss is a newsletter form
   that reached `signup` instead of `cro`. The explicit cross-references in the
   descriptions ("for popup copy, see popups") do their job *whenever a skill
   fires at all*.
2. **The problem is that most of them do not fire.** 7 of the 13 skills scored
   here **never activated once** on a request squarely inside their own
   description — 0 of 10 each, 0 of 20 for `popups` and `product-marketing` —
   and `cro` managed 4 of 20.
   They were not beaten by a sibling. They were beaten by the base model, which
   did the work itself in 93 of those 120 attempts.
3. **`product-marketing` — the skill the README calls the foundation — fired
   0 times in 200 attempts**, including 0/20 on its own two cases. The context
   file it owns is read in 34% of other skills' activations (17/50), against 9%
   when no skill fired (14/150). And when asked to update positioning, the model
   wrote a parallel `POSITIONING.md` in 9 of 10 attempts, **leaving the file
   every other skill is told to read stale.**

---

## 1. Who won each case

Expected winners are taken from the skills' **own descriptions**, not this
suite's opinion — they route to each other explicitly: "For signup/registration
flows, see signup", "For popup copy, see popups", "Distinct from public pricing
pages (see cro)", "For editing existing copy, see copy-editing". No prompt
contains a skill name.

| Case | Expected | Won | Also fired |
| --- | --- | --- | --- |
| registration form abandons half | `signup` | **none ×10** | — |
| newsletter form gets no submissions | `cro` | `cro` ×4, **`signup` ×1**, none ×5 | — |
| rewrite the exit modal's words | `popups` | **none ×10** | — |
| when/whom the exit modal shows to | `popups` | **none ×10** | — |
| public pricing page doesn't convert | `cro` | **none ×10** | — |
| in-app limit-reached screen | `paywalls` | **none ×10** | — |
| empty first-session dashboard | `onboarding` | **none ×10** | — |
| tighten a wordy paragraph with typos | `copy-editing` | **none ×10** | — |
| plan the week-one message sequence | `emails` | `emails` ×10 | — |
| first message + 2 follow-ups to leads | `cold-email` | `cold-email` ×6, none ×4 | — |
| page not found when people search | `seo-audit` | `seo-audit` ×10 | — |
| never cited by ChatGPT / Perplexity | `ai-seo` | `ai-seo` ×10 | — |
| one page per integration from a CSV | `programmatic-seo` | **none ×10** | — |
| star rating + FAQ in Google results | `schema` | `schema` ×9, none ×1 | — |
| update stale positioning context | `product-marketing` | **none ×10** | — |
| work out the new ICP and positioning | `product-marketing` | **none ×10** | — |
| *contested:* write a better headline | `copywriting` or `copy-editing` | none ×10 | not scored |
| *negative:* pick $49 vs $79 | none | none ×10 | — |
| *negative:* fix a null-reference crash | none | none ×10 | — |
| *negative:* missing Postgres index | none | none ×10 | — |

### Collision matrix

Rows are the expected winner, columns the first skill to fire.

| expected \ fired | none | `cro` | `signup` | `emails` | `cold-email` | `seo-audit` | `ai-seo` | `schema` |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `signup` | **10** | | | | | | | |
| `cro` | **15** | 4 | **1** | | | | | |
| `popups` | **20** | | | | | | | |
| `paywalls` | **10** | | | | | | | |
| `onboarding` | **10** | | | | | | | |
| `copy-editing` | **10** | | | | | | | |
| `emails` | | | | 10 | | | | |
| `cold-email` | 4 | | | | 6 | | | |
| `seo-audit` | | | | | | 10 | | |
| `ai-seo` | | | | | | | 10 | |
| `programmatic-seo` | **10** | | | | | | | |
| `schema` | 1 | | | | | | | 9 |
| `product-marketing` | **20** | | | | | | | |

Everything off the diagonal is in the **none** column, bar one cell. That is the
shape of an under-triggering problem, not a collision problem.

Host-bundled skills barely competed: `run` fired once. Negatives were clean,
0 of 30.

## 2. The one real collision

`cro.lead_form` — "the newsletter form in the footer barely gets submissions" —
reached `signup` once in ten:

> I'll help you improve the newsletter form submission rate. Let me first
> examine the current form and then use the signup skill…

`signup`'s own description says "For lead capture forms (not account creation),
see cro", and a newsletter form is not account creation. 1 in 10 is a real but
small leak, and it is the only one in 50 activations.

## 3. What actually decides whether a skill fires

The five skills that fire are the ones whose requests sound like a marketing
job the model would not otherwise do: plan a message sequence, write outreach,
diagnose search visibility, get cited by AI, add structured data. The seven
that never fire, and `cro` on its pricing-page case, are the ones whose requests
point at a file to change — a form, a modal, a pricing page, an upgrade screen,
a dashboard, a paragraph, a CSV to turn into pages.

The work still happens. Of the 120 positive attempts where no marketing skill
fired, **93 wrote files** — the base model redesigned the form, rewrote the
modal, restructured the pricing page, built the integration pages. It just did
so without the skill.

This is the same failure mode measured on `ui-ux-pro-max` and `impeccable` in
this repository: when a request is answerable by editing a file directly, it is
answered by editing the file directly.

## 4. The `product-marketing` claim

The README: "The `product-marketing` skill is the foundation — every other skill
checks it first to understand your product, audience, and positioning." In the
skill bodies this is concrete: each one says **"If `.agents/product-marketing.md`
exists, read it before asking questions."** The fixture ships that file, so the
instruction is testable.

**Does each activated skill read the context file?**

| | read it | rate |
| --- | --- | --- |
| attempts where a marketing skill fired | 17 / 50 | **34%** |
| attempts where none fired (control) | 14 / 150 | 9% |

Every read came before the skill's first edit, so where it is read, it is read
"first". But two activations in three never read it at all. By skill:

| Skill | Read the context file |
| --- | --- |
| `cold-email` | 6/6 |
| `ai-seo` | 5/10 |
| `emails` | 4/10 |
| `seo-audit` | 1/10 |
| `schema` | 1/9 |
| `cro` | 0/4 |
| `signup` | 0/1 |

The skills whose work most depends on audience (`cold-email`, `emails`) read it
most; the technical ones (`seo-audit`, `schema`) almost never. That may be
reasonable behaviour, but it is not "every other skill checks it first".

**Does `product-marketing` itself fire?** 0 of 200 attempts. Two cases were
written for it:

- *"Our positioning notes are stale… update the shared context that every later
  session reads first."* — 0/10. All ten went to the **host's own memory**
  instead: Claude Code's `MEMORY.md`, a new memory file, or `CLAUDE.md`. That is
  a collision, but with the host rather than a sibling skill. In fairness, this
  prompt's wording is close to how host memory is described.
- *"Work out who our ideal customer is now and how we should position against
  hand-rolled metering, and write it up."* — 0/10, with wording that uses the
  description's own trigger words ("ideal customer", "position"). Added in v2
  specifically to rule out the first case's wording as the cause. It did not.

**The consequence is the sharpest result in the run.** In the ICP case the model
wrote the new positioning to a new root-level `POSITIONING.md` in **9 of 10**
attempts and updated `.agents/product-marketing.md` in 1. So after a real
change of audience, the file every other skill is instructed to read still says
"indie developers" — and the 34% of activations that do read it get the old
answer.

## 5. A note on the instrument

assay 0.3.2 scores this run **179 pass, 21 fail**. That is not the finding.

A suite has one `target.skill`, and `expect` has no field for "this case expects
skill X to win" when X is not the target. Collision cases can only say which
skills must *not* fire (`not_triggered`), and a case where nothing fires
satisfies that. So the **100 positive attempts in which no marketing skill
fired score as pass**; the 21 fails are the 20 `product-marketing` attempts (the
target, `triggered: true`) and the single `signup` leak. The run summary's
`precision: no observations`, `recall: 0% (N=20)` describe the target alone.

The winners and the matrix above come from `tools/collide.py`, which reads the
expected winner from the case id (`collide.<skill>.<shape>`) and the fired set
from each attempt's confirmed activations.

---

## Suite history

- **v1, `--fast`** (57 attempts, `run-…ca6f250f`): same diagonal-or-none shape,
  17 activations all correct, `product-marketing` 0/3 on its one case, which
  went 3/3 to host memory.
- **v2, full** (this report): added `collide.product_marketing.icp` to test
  whether v1's positioning wording caused that. Nothing else changed.

## Limitations

- **14 of 50 skills loaded.** Collisions with the other 36 (`ab-testing`,
  `pricing`, `content-strategy`, `marketing-psychology`…) are not measured. The
  `pricing_decision` negative is where `pricing` would have been the right
  answer; with it absent, none of the loaded skills overreached.
- **One model.** `claude-haiku-4-5-20251001`. Activation is model behaviour;
  a larger model may reach for skills more readily. Rates here are a floor.
- **The context file is present in every fixture.** Its absence is not tested;
  whether skills *check for* it when missing is a different question.
- **`acceptEdits`.** No effect on activation (these skills declare no
  `allowed-tools`), and the context file sits inside the workspace. Reads of a
  skill's own reference files outside the workspace would be refused, but no
  finding here depends on them.
- **One fixture, one product.** Ten attempts per case.
- **The committed fixture is not byte-identical to the measured one.** After
  the run, invented names that could coincide with real people or companies
  were replaced in `outreach/prospects.csv`, `content/integrations.csv` and
  `.agents/product-marketing.md` — see *Fixture data is fictional* in the
  README. Structure and task are unchanged; a re-run reads different bytes.

## Reproduce

```
npx @ktlsr/assay@0.3.2 validate suites/marketingskills.collide.suite.yaml
npx @ktlsr/assay@0.3.2 run suites/marketingskills.collide.suite.yaml \
  --skill ./skills/marketing-skills-collide --concurrency 4
python tools/collide.py .assay/runs/<run-id>.json
```

`skills/marketing-skills-collide/` is the 14 skill directories copied verbatim
from the marketplace install, under the upstream `plugin.json` so that names
resolve as `marketing-skills:<skill>`.
