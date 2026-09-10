# Issue draft for coreyhaines31/marketingskills

Not posted. Title and body below.

---

**Title:** `product-marketing` never activated in 200 attempts, and positioning updates bypass `.agents/product-marketing.md`

---

I measured how 14 of these skills behave when installed together — which one a
request reaches, and whether the "every skill checks `product-marketing` first"
claim from the README holds. 200 attempts, one model, pinned; method and raw
numbers are linked at the end. Most of it is good news for the design. Two
parts are not.

## What works: the skills do not fight each other

I loaded `cro`, `signup`, `onboarding`, `popups`, `paywalls`, `copywriting`,
`copy-editing`, `emails`, `cold-email`, `seo-audit`, `ai-seo`,
`programmatic-seo`, `schema` and `product-marketing` together, and wrote each
case so that its expected winner is the one **your own descriptions route to**
("For popup copy, see popups", "Distinct from public pricing pages (see cro)").
No prompt named a skill.

**Of 50 activations, 49 reached the skill the descriptions point to.** The one
leak was a newsletter form that reached `signup` once in ten, although
`signup`'s description sends lead-capture forms to `cro`. The cross-references
in the descriptions work.

## 1. `product-marketing` never activates, and the context file goes stale

`product-marketing` fired **0 times in 200 attempts**, including 0 of 20 on two
cases written for it. The second used your description's own trigger words:

> We moved from selling to indie developers to selling to platform teams at API
> companies. Work out who our ideal customer is now and how we should position
> against hand-rolled metering, and write it up.

The model did the work every time — but wrote it to a new root-level
`POSITIONING.md` in **9 of 10** attempts, and updated
`.agents/product-marketing.md` in 1. So after a real change of audience, the
file every other skill is told to read still described the old one.

The other case ("update the shared context that every later session reads
first") went 10 of 10 to Claude Code's own memory — `MEMORY.md` or `CLAUDE.md`
— instead. That wording is close to how host memory is described, so I would
not lean on it; the ICP case is the clean one.

## 2. The context file is read in about a third of activations

Every skill says "If `.agents/product-marketing.md` exists, read it before
asking questions." The test fixture had the file.

| | read it |
| --- | --- |
| attempts where one of these skills activated | **17 / 50 (34%)** |
| attempts where none activated | 14 / 150 (9%) |

So the skills do raise the rate, and whenever the file is read it is read
before the first edit. But two activations in three never open it. It varies a
lot by skill: `cold-email` 6/6, `ai-seo` 5/10, `emails` 4/10, `seo-audit` 1/10,
`schema` 1/9, `cro` 0/4.

"Every other skill checks it first" is accurate for `cold-email` and not yet
for the rest.

## 3. Most of the conversion and editing skills never activate

This is not a conflict between skills, but it is the larger number, so
mentioning it:

| Activated on its own cases | Skills |
| --- | --- |
| reliably | `emails` 10/10, `seo-audit` 10/10, `ai-seo` 10/10, `schema` 9/10, `cold-email` 6/10 |
| sometimes | `cro` 4/20 |
| **never** | `signup` 0/10, `popups` 0/20, `paywalls` 0/10, `onboarding` 0/10, `copy-editing` 0/10, `programmatic-seo` 0/10, `product-marketing` 0/20 |

The ones that never fire are the ones whose requests point at a file to change —
a registration form, an exit modal, an upgrade screen, a first-run dashboard, a
wordy paragraph. In 93 of those 120 attempts the model changed the file anyway,
just without the skill. That is a pattern I have measured on other large skill
sets too, not something specific to these descriptions.

## Caveats

- **One model: `claude-haiku-4-5-20251001`.** A larger model may reach for
  skills more readily; treat these rates as a floor.
- **14 of the 50 skills were installed.** Collisions with the other 36 are not
  measured.
- **One fixture** (a small SaaS marketing site), 10 attempts per case, Claude
  Code 2.1.263.

## What might help

For #1, the two facts together suggest the cheapest fix is in the other skills
rather than in `product-marketing`'s description: if a skill that edits
positioning-dependent copy also *writes back* to `.agents/product-marketing.md`
when the user states a change of audience or positioning, the file stays
current whether or not `product-marketing` ever fires. I have not tested that.

Full report, suite and per-case tables:
https://github.com/ktlesr/skill-trigger-measurements/blob/master/reports/marketingskills.collide.md
