# Naming the mechanism halves the trigger rate: 9/18 vs 20/20

I ran a trigger-discrimination measurement against `skills/better-typography/`.
The boundary result is clean and worth knowing; one prompt shape is a reproducible
gap with a visible cost in the output.

## Setup

- Skill: `jakubkrehel/skills@267330e1adfc66a718fb65fa6918c1f06d0a689e`,
  `skills/better-typography/` (content hash `sha256:1223227c…c28f4c5`)
- Host: Claude Code. Model pinned to `claude-haiku-4-5-20251001`.
- **The skill was installed alone** — no `better-writing`, `better-colors`,
  `better-accessibility` or `better-layout` present to absorb a deflected request.
- **No prompt contains the word "typography"** or the skill's name, so triggering
  could not come from a name match.
- Two case sets of 10 cases × 10 attempts = 200 attempts. Each set: 3 positives,
  4 near neighbours, 2 unrelated negatives, 1 completion case asserting
  `file_exists` plus a no-swallowed-errors trace rule. Every file-referencing
  prompt is backed by a fixture copied fresh per attempt.

## Result

Pooled over both rounds (200 attempts):

| | Value |
| --- | --- |
| precision | 100% (N=68, 95% CI 95%–100%) |
| recall | 87% (N=78, 95% CI 78%–93%) |
| false positives | 0 / 120 negative attempts |

Per round:

| Round | precision | recall |
| --- | --- | --- |
| 1 — touches type, decides nothing | 100% (N=34, 95% CI 90%–100%) | 89% (N=38, 95% CI 76%–96%) |
| 2 — sibling skills' territory | 100% (N=34, 95% CI 90%–100%) | 85% (N=40, 95% CI 71%–93%) |

### Both boundaries hold

The description is a keyword list — *type scale, spacing, sizing, variable fonts,
OpenType features, wrapping, truncation* — and every one of those words has a
common non-typographic meaning in a frontend codebase. Round 1 built a neighbour
on each overlap:

| Near-neighbour case | The overlap | Fired |
| --- | --- | --- |
| change `.price` from 14px to 16px, value already signed off | *sizing* | 0/10 |
| rewrite the hero headline words, styling untouched | (adjacent to *wrapping*) | 0/10 |
| fetch Inter `.woff2` into `public/fonts/`, write `@font-face` | *variable fonts* | 0/10 |
| cut 300-char vendor titles to 80 in `src/api.ts` | *truncation* | 0/10 |

Because assay flags an unbroken negative set as *bounding the false-positive rate,
not proving discrimination*, round 2 used neighbours that are genuine design
decisions about text — each one handed to a different skill by this skill's own
SKILL.md:

| Near-neighbour case | SKILL.md assigns it to | Fired |
| --- | --- | --- |
| is `#999` on white readable, pick a value that clears the threshold | `better-colors` | 0/10 |
| fix the h1/h2 document outline for screen readers | `better-accessibility` | 0/10 |
| convert `margin-left`/`padding-left` to logical properties for RTL | `better-layout` | 0/10 |
| open up the cramped 8px `.card-grid` gap | layout spacing, not type spacing | 0/10 |

120 negative attempts, zero false positives. The four hand-offs written in prose
are hand-offs the skill actually keeps, even with no sibling installed to catch
the request.

## The gap: naming the mechanism halves the trigger rate

No negative leaked. The finding is on the recall side, and it is concentrated in
one prompt shape rather than spread evenly.

Two prompts ask for the same work on the same fixture. One fires every time; the
other fires half the time:

| Prompt | Fired |
| --- | --- |
| *"src/app.css has eight text sizes that were each picked by eye. Replace them with a proper scale and move every class onto it."* | **20/20** |
| *"Define a named scale as CSS custom properties in a new file src/type-scale.css, and point the classes in app.css at it."* | **9/18 — 50% (N=18, 95% CI 29%–71%)** |

The second reproduced across both rounds independently (4/8 measurable in round 1,
5/10 in a clean round 2), so it is not a one-run artefact.

Every miss is a trigger miss, never an artefact failure: `file_exists` on
`src/type-scale.css` passed on all 10 attempts of the clean round. The work gets
done — just without the skill in context. Raw trace of a missed attempt:

```
msg:  I'll read the current app.css to see what text sizes need to be organized
      into a type scale.
call  Read   src/app.css
msg:  Now I'll create a type-scale.css file with a named scale using CSS custom
      properties, and then update app.css to use it.
call  Write  src/type-scale.css   :root { --type-xs: 10px; --type-sm: 11px; ...
call  Edit   src/app.css
skills observed: []
```

A hit on the same case, for contrast:

```
msg:  Now I'll consult the typography skill before defining the scale, then
      create the type scale and update app.css.
call  Skill  better-typography
SKILL better-typography
```

The cost shows up in what gets written. Scales invented without the skill in
context came back as `10px / 11px / 12px / 14px / 15px / 19px / 21px / 23px /
52px` — the fixture's ad-hoc sizes renamed as variables, which is the outcome the
"use a type scale with semantic names" section exists to prevent. The prompt asked
for a system; without the skill it got a rename.

### Why this shape misses

The description names the **artefacts** the skill knows about — "type scale,
spacing, sizing" — but never the **situation** that should summon it. When a
request already contains the artefact word and spells out the mechanism (custom
properties, a new file, repoint the classes), the work reads as transcription
rather than as a decision, and there is nothing left in the request for the
description to match on. Requests phrased as a *problem* ("picked by eye",
"runs the full 1400px", "the numbers jitter") fired 59/60 pooled across both
rounds — 20/20, 19/20 and 20/20 — against 9/18 for the mechanism-phrased one.

## Suggestion

Adding the situation to the description, alongside the artefact list. Something
along the lines of:

> …and other details that make typography feel great across your product. Use it
> whenever type sizes, spacing or wrapping need a decision — including when the
> request already names the mechanism (a scale, custom properties, a tokens file).

The wording is yours; the measurable claim is that the artefact list alone does
not reach a request that has already named the artefact. The sibling hand-offs
need no change — they measured clean at 120/120.

## Reproduce

```
npx @ktlsr/assay@0.1.2 validate suites/better-typography.suite.yaml
npx @ktlsr/assay@0.1.2 run suites/better-typography.suite.yaml \
  --skill ./skills/better-typography
npx @ktlsr/assay@0.1.2 run suites/better-typography.tight.suite.yaml \
  --skill ./skills/better-typography
```

Case sets, fixtures and both reports: <https://github.com/ktlesr/skill-trigger-measurements>
Run records stay local (`.assay/runs/`, not committed); happy to attach the JSON.
Needs `CLAUDE_CODE_OAUTH_TOKEN` or `ANTHROPIC_API_KEY`; each attempt runs in an
isolated config directory.

Three caveats on the numbers. Everything is pinned to
`claude-haiku-4-5-20251001` — routing is a model behaviour, so these rates are a
floor, not a universal result. An OAuth token rotation killed the last two
attempts of round 1 (one recorded `unknown`, one an environment artefact recorded
as a `file_exists` failure); round 2 ran clean with zero unknowns and reproduces
the finding on its own. And the fixture was extended mid-run in round 1 for the
round-2 cases, so round 1 is not fixture-identical throughout — round 2 ran
entirely against the final fixture.

Method: <https://assayctl.dev/methodology>
