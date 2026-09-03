# Measurement report — `better-typography`

**Skill:** `jakubkrehel/skills@267330e1adfc66a718fb65fa6918c1f06d0a689e`, `skills/better-typography/`
**Host:** Claude Code · **Model:** `claude-haiku-4-5-20251001` · **Runner:** `npx @ktlsr/assay@0.1.2`
**Measured:** 2026-09-03 · **Attempts:** 200 across two rounds

---

## What was measured

Whether the skill fires on a request that needs a typographic decision, stays
quiet on a request that touches text without needing one, and produces the file
it was asked for.

The skill's description is a keyword list:

> Focuses on type scale, spacing, sizing, variable fonts, OpenType features,
> wrapping, truncation and other details that make typography feel great across
> your product.

Every one of those words — *spacing*, *sizing*, *wrapping*, *truncation* — has a
common non-typographic meaning in a frontend codebase. The near-neighbour cases
were built on exactly that overlap.

## Method

- The skill was installed alone in an isolated directory. `active_skills` lists
  it and nothing else, so no sibling skill could absorb or deflect a request.
- **No prompt contains the word "typography" or the skill's name.** Triggering
  had to come from the request, not from a string match.
- Ten cases per round, ten attempts each: 3 positives, 4 near neighbours,
  2 unrelated negatives, 1 completion case.
- Prompts that name a file are backed by a fixture (`fixtures/typography-app/`),
  copied fresh into a temp workspace for every attempt.
- The completion case asserts `file_exists` on the artefact the prompt names and
  the `no_swallowed_errors` trace rule.
- Both case sets passed `assay validate` before running.

---

## Round 1 — neighbours that touch type without deciding anything

Four near neighbours, each landing on one description keyword while asking for
something that is not a type decision:

| Case | The overlap it exploits |
| --- | --- |
| `signed_off_value` | changes a `font-size`, but the value is already decided |
| `copy_rewrite` | rewrites headline words, styling explicitly untouched |
| `font_file_plumbing` | fetches `.woff2` files and writes `@font-face` |
| `server_side_truncate` | "truncate", but as string handling in `src/api.ts` |

### Pins

| Pin | Value |
| --- | --- |
| skill source | `jakubkrehel/skills@267330e1adfc66a718fb65fa6918c1f06d0a689e` |
| skill content hash | `sha256:1223227c97759e0ad81133e34026c58b0d6c78e1829d5056346c23fb6c28f4c5` |
| model | `claude-haiku-4-5-20251001` |
| system prompt hash | `not-provided-by-host` |
| case set | v1 · `sha256:b3efb3213f3128f784b68baad52b345200fcc82875bfc8cec6a3ae530ef28b18` |
| environment hash | `—` |
| run id | `run-2026-09-03T11-10-19-914Z-ac10d159` |
| repeats per case | 10 |

### Per case

| Case | Kind | Expected | Fired | Pass rate | Unknown | Verdict |
| --- | --- | --- | --- | --- | --- | --- |
| `trigger.positive.ad_hoc_sizes` | positive | fire | 10/10 | 100% (N=10, 95% CI 72%–100%) | 0 | pass |
| `trigger.positive.measure_and_widows` | positive | fire | 10/10 | 100% (N=10, 95% CI 72%–100%) | 0 | pass |
| `trigger.positive.variable_font_numerals` | positive | fire | 10/10 | 100% (N=10, 95% CI 72%–100%) | 0 | pass |
| `trigger.negative.near_neighbor.signed_off_value` | near neighbour | stay quiet | 0/10 | 100% (N=10, 95% CI 72%–100%) | 0 | pass |
| `trigger.negative.near_neighbor.copy_rewrite` | near neighbour | stay quiet | 0/10 | 100% (N=10, 95% CI 72%–100%) | 0 | pass |
| `trigger.negative.near_neighbor.font_file_plumbing` | near neighbour | stay quiet | 0/10 | 100% (N=10, 95% CI 72%–100%) | 0 | pass |
| `trigger.negative.near_neighbor.server_side_truncate` | near neighbour | stay quiet | 0/10 | 100% (N=10, 95% CI 72%–100%) | 0 | pass |
| `trigger.negative.unrelated.rate_limit` | unrelated | stay quiet | 0/10 | 100% (N=10, 95% CI 72%–100%) | 0 | pass |
| `trigger.negative.unrelated.docker_build` | unrelated | stay quiet | 0/10 | 100% (N=10, 95% CI 72%–100%) | 0 | pass |
| `complete.writes_scale_tokens` | completion | fire | 4/8 | 44% (N=9, 95% CI 19%–73%) | 1 | FAIL |

### Trigger accuracy

| | Fired | Stayed quiet |
| --- | --- | --- |
| **Should fire** | 34 (TP) | 4 (FN) |
| **Should stay quiet** | 0 (FP) | 60 (TN) |

| Metric | Value |
| --- | --- |
| precision | 100% (N=34, 95% CI 90%–100%) |
| recall | 89% (N=38, 95% CI 76%–96%) |
| F1 | 0.94 |
| unreadable trigger signals | 2 |

### Cost of the measurement

| | |
| --- | --- |
| attempts | 100 |
| tool calls | 531 |
| tokens (in/out) | 4463 / 224690 |
| cost | $4.9337 |
| wall time | 47.2 min |

### Reading

Precision is 100% and no negative broke — including `font_file_plumbing`, which
is the closest call of the four, since the skill's own body does discuss serving
`.woff2`. The skill draws that line itself ("How the files load is the project's
concern") and the line held 10/10.

Assay flags this result rather than crediting it:

> no negative case broke — that bounds the false-positive rate, not the set's
> discriminating power.

Which is why round 2 exists.

The one case that failed is the completion case, and it did **not** fail on the
artefact. Every measurable attempt wrote `src/type-scale.css`; `file_exists` and
`no_swallowed_errors` passed every time. It failed because the skill was not
consulted before the file was written.

---

## Round 2 — neighbours the skill hands to sibling skills by name

The round-1 negatives were arguably far from the skill on a second axis (they
were all "don't decide anything" requests). Round 2 removes that escape: every
neighbour is a genuine design decision about text, and every one is assigned to
a **different** skill inside `better-typography`'s own SKILL.md:

> The words themselves belong to `better-writing`. Semantic heading structure
> belongs to `better-accessibility`. Spatial RTL layout and logical properties
> belong to `better-layout`. Contrast measurement belongs to `better-colors`.

| Case | Skill that owns it, per SKILL.md |
| --- | --- |
| `contrast` | `better-colors` |
| `heading_outline` | `better-accessibility` |
| `logical_properties` | `better-layout` |
| `grid_gap` | layout spacing, not type spacing |

Positives, unrelated cases and the completion case are carried over unchanged, so
the two rounds differ on one axis only.

### Pins

| Pin | Value |
| --- | --- |
| skill source | `jakubkrehel/skills@267330e1adfc66a718fb65fa6918c1f06d0a689e` |
| skill content hash | `sha256:1223227c97759e0ad81133e34026c58b0d6c78e1829d5056346c23fb6c28f4c5` |
| model | `claude-haiku-4-5-20251001` |
| system prompt hash | `not-provided-by-host` |
| case set | v1 · `sha256:b793b0beed4e6730f007fdf2cadeeba4a6a33b45a296974cb2d19e0b1e0653fd` |
| environment hash | `sha256:8bd3328072e0408164062ae77593e572345cdd94b493a0a7474d06ba3cabfc88` |
| run id | `run-2026-09-03T11-51-48-766Z-eb0eedc8` |
| repeats per case | 10 |

### Per case

| Case | Kind | Expected | Fired | Pass rate | Unknown | Verdict |
| --- | --- | --- | --- | --- | --- | --- |
| `trigger.positive.ad_hoc_sizes` | positive | fire | 10/10 | 100% (N=10, 95% CI 72%–100%) | 0 | pass |
| `trigger.positive.measure_and_widows` | positive | fire | 9/10 | 90% (N=10, 95% CI 60%–98%) | 0 | FAIL |
| `trigger.positive.variable_font_numerals` | positive | fire | 10/10 | 100% (N=10, 95% CI 72%–100%) | 0 | pass |
| `trigger.negative.near_neighbor.contrast` | near neighbour | stay quiet | 0/10 | 100% (N=10, 95% CI 72%–100%) | 0 | pass |
| `trigger.negative.near_neighbor.heading_outline` | near neighbour | stay quiet | 0/10 | 100% (N=10, 95% CI 72%–100%) | 0 | pass |
| `trigger.negative.near_neighbor.logical_properties` | near neighbour | stay quiet | 0/10 | 100% (N=10, 95% CI 72%–100%) | 0 | pass |
| `trigger.negative.near_neighbor.grid_gap` | near neighbour | stay quiet | 0/10 | 100% (N=10, 95% CI 72%–100%) | 0 | pass |
| `trigger.negative.unrelated.rate_limit` | unrelated | stay quiet | 0/10 | 100% (N=10, 95% CI 72%–100%) | 0 | pass |
| `trigger.negative.unrelated.docker_build` | unrelated | stay quiet | 0/10 | 100% (N=10, 95% CI 72%–100%) | 0 | pass |
| `complete.writes_scale_tokens` | completion | fire | 5/10 | 50% (N=10, 95% CI 24%–76%) | 0 | FAIL |

### Trigger accuracy

| | Fired | Stayed quiet |
| --- | --- | --- |
| **Should fire** | 34 (TP) | 6 (FN) |
| **Should stay quiet** | 0 (FP) | 60 (TN) |

| Metric | Value |
| --- | --- |
| precision | 100% (N=34, 95% CI 90%–100%) |
| recall | 85% (N=40, 95% CI 71%–93%) |
| F1 | 0.92 |
| unreadable trigger signals | 0 |

### Cost of the measurement

| | |
| --- | --- |
| attempts | 100 |
| tool calls | 370 |
| tokens (in/out) | 3531 / 188770 |
| cost | $4.3187 |
| wall time | 37.3 min |

### Reading

The tighter set did not break either. Forty attempts across four cases that are
each one word away from the description's keyword list, and the skill stayed
quiet in all forty. Pooled across both rounds: **120 negative attempts, 0 false
positives**, precision **100% (N=68, 95% CI 95%–100%)**.

The boundary this skill declares in prose is the boundary it actually keeps.

The completion case reproduced its round-1 result on a clean run — 50% (N=10),
again entirely on trigger, with `file_exists` passing 10/10.

---

## Findings

### 1. The completion prompt reaches the skill about half the time

Pooled across both rounds, the completion case fired **9 of 18 measurable
attempts — 50% (N=18, 95% CI 29%–71%)**.

It is the same underlying request as `trigger.positive.ad_hoc_sizes`, which fired
**20/20**. The difference is how the request is phrased:

| | Prompt | Fired |
| --- | --- | --- |
| positive | *"src/app.css has eight text sizes that were each picked by eye. Replace them with a proper scale and move every class onto it."* | 20/20 |
| completion | *"Define a named scale as CSS custom properties in a new file src/type-scale.css, and point the classes in app.css at it."* | 9/18 |

From the raw trace of a missed attempt:

```
msg:  I'll read the current app.css to see what text sizes need to be organized
      into a type scale.
call  Read     src/app.css
msg:  Now I'll create a type-scale.css file with a named scale using CSS custom
      properties, and then update app.css to use it.
call  Write    src/type-scale.css   :root { --type-xs: 10px; --type-sm: 11px; ...
call  Edit     src/app.css
skills observed: []
```

And from a *hit* on the same case, for contrast:

```
msg:  Now I'll consult the typography skill before defining the scale, then
      create the type scale and update app.css.
call  Skill    better-typography
SKILL better-typography
```

Nothing in the request is out of scope — a type scale is the first thing the
skill's body teaches. What changes is that the second phrasing already names the
mechanism (custom properties, a new file, repoint the classes), so the work reads
as transcription rather than as a decision, and the model executes it directly.

The cost is visible in the output. Scales invented without the skill in context
came out as `10px / 11px / 12px / 14px / 15px / 19px / 21px / 23px / 52px` —
the fixture's ad-hoc sizes renamed, which is what the skill's "use a type scale
with semantic names" section exists to prevent.

**Condition in the description that a request like this does not meet:** the
description names *artefacts* the skill knows about ("type scale, spacing,
sizing") but never names the *situation* that should summon it. A request that
already contains the artefact word has nothing left to match on.

### 2. The declared boundary holds

Not a defect — a positive result worth recording. Eight near-neighbour cases
across two rounds, 80 attempts, zero false positives. The four sibling-skill
boundaries the SKILL.md declares in prose were each measured directly and each
held 10/10.

---

## Threats to validity

- **Model pin.** Everything here is `claude-haiku-4-5-20251001`. Trigger routing
  is a model behaviour; a larger model may consult the skill on prompts this one
  executed directly. The finding is a *floor*, not a universal rate.
- **Fixture edited mid-run.** `fixtures/typography-app/` was extended (adding
  `.caption-muted`, `.card-grid`, `src/cards.tsx`) while round 1 was still
  running, for the round-2 cases. Attempts from roughly #63 onward — part of
  `server_side_truncate` and the completion case — saw the extended fixture.
  Neither case's subject matter is affected, and no verdict in those cases turned
  on the added lines, but the round-1 record is not fixture-identical throughout.
  Round 2 ran entirely against the final fixture.
- **OAuth token revoked mid-run.** The host token rotated near the end of
  round 1. `complete.writes_scale_tokens` #8 is correctly recorded `unknown`;
  #9 is recorded `fail` on `file_exists`, but the session died on a 401 before it
  could write, so that failure is an environment artefact, not a skill result.
  Round 2 ran clean with 0 unknowns. Note that assay routes a dead session to
  `unknown` for the trigger signal but still evaluates file assertions against the
  empty workspace, so an aborted attempt can surface as an assertion `fail`.
- **Trigger is observed, not enforced.** Assay reads the `Skill` tool call from
  the host's stream-json. A skill whose content the model absorbed some other way
  would read as "did not trigger".
- **Ten attempts per case.** Every 10/10 above carries a 95% CI whose lower bound
  is 72%. Ten attempts is enough to see a coin-flip; it is not enough to rule out
  a 1-in-20 leak.

---

## Reproduce

```
git clone <this repo> && cd assay-example
npx @ktlsr/assay@0.1.2 validate suites/better-typography.suite.yaml
npx @ktlsr/assay@0.1.2 run suites/better-typography.suite.yaml \
  --skill ./skills/better-typography
npx @ktlsr/assay@0.1.2 run suites/better-typography.tight.suite.yaml \
  --skill ./skills/better-typography
```

Requires `CLAUDE_CODE_OAUTH_TOKEN` or `ANTHROPIC_API_KEY`; each attempt runs in
an isolated config directory that does not inherit an interactive session.

Method: <https://assayctl.dev/methodology>
