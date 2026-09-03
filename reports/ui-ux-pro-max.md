# Measurement report — `ui-ux-pro-max`

**Skill:** `nextlevelbuilder/ui-ux-pro-max-skill@f3ac195224eac1eb0dfe1a3059c2a6add78ffbe3`, `.claude/skills/ui-ux-pro-max/`
**Host:** Claude Code · **Model:** `claude-haiku-4-5-20251001` · **Runner:** `npx @ktlsr/assay@0.1.3`
**Measured:** 2026-09-03 · **Attempts:** 200 across two rounds

---

## What was measured

This is the third skill measured in this repository and the first built to be
comprehensive. Its description advertises 79 styles, 192 palettes, 74 font
pairings, 119 UX guidelines, 25 chart types and 22 stacks, and claims
"designing, building, reviewing, or fixing interfaces". The two skills measured
before it returned zero false positives between them, so the question here was
the opposite one: **does a skill this broad fire on work that is merely next to
design?**

The answer is no — and the interesting results turned out to be elsewhere.

A second measurement runs alongside the usual trigger suite: **reference-file
coverage.** The skill ships 72 files and 3.57 MB. Which of them does a run
actually open?

## Method

- **Installed as a minimal single-skill plugin.** This skill ships as a plugin
  whose `SKILL.md` invokes its own search tool at
  `${CLAUDE_PLUGIN_ROOT}/.claude/skills/ui-ux-pro-max/scripts/search.py`.
  Installing only the skill subdirectory — as the two earlier measurements did —
  would break that path and measure a packaging mistake instead of the skill. So
  the skill directory was placed in a plugin directory with the project's own
  `plugin.json` and the same `.claude/skills/` layout, containing this skill and
  nothing else. Isolation and the documented path both hold.
- **No prompt contains the skill's name, or the bare tokens "UI" and "UX."**
  Prompts say interface, screen, page, component.
- Ten cases per round, ten attempts each: 3 positives, 4 near neighbours,
  2 unrelated negatives, 1 completion case. The two unrelated controls are the
  same prompts used in the other two measurements in this repository.
- The near neighbours come in the two flavours the question calls for: frontend
  work with no design decision in it, and a real design decision that is not an
  interface.
- Prompts naming a file are backed by a fixture (`fixtures/uiux-app/`), a small
  Next.js project copied fresh into a temp workspace per attempt.

---

## Round 1 — frontend without a decision, decisions without an interface

| Case | Flavour |
| --- | --- |
| `render_loop` | a `useEffect` refetch loop; nothing visual changes |
| `css_modules_migration` | styled-components → CSS module, rendered result identical |
| `print_report` | chart types and a CMYK palette for a printed annual report |
| `wordmark` | three directions for the wordmark itself |

### Pins

| Pin | Value |
| --- | --- |
| skill source | `nextlevelbuilder/ui-ux-pro-max-skill@f3ac195224eac1eb0dfe1a3059c2a6add78ffbe3` |
| skill content hash | `sha256:dbffccf82b28bc19e7d448225f334dac60e5bdd6f7c73525df4dff224937239c` |
| model | `claude-haiku-4-5-20251001` |
| system prompt hash | `not-provided-by-host` |
| case set | v1 · `sha256:3fbfb4a8980e80638f5ad91c9ae4fff717373e16ab496bbf99e865e7d2054e56` |
| environment hash | `sha256:b989cbb10ba6ccf3457c875a6095782be9199102d00d631c26dbe80f412a6d72` |
| run id | `run-2026-09-03T16-34-04-660Z-2a900c03` |
| repeats per case | 10 |

### Per case

| Case | Kind | Expected | Fired | Pass rate | Unknown | Verdict |
| --- | --- | --- | --- | --- | --- | --- |
| `trigger.positive.pricing_page` | positive | fire | 7/10 | 70% (N=10, 95% CI 40%–89%) | 0 | FAIL |
| `trigger.positive.review_component` | positive | fire | 3/10 | 30% (N=10, 95% CI 11%–60%) | 0 | FAIL |
| `trigger.positive.chart_choice` | positive | fire | 0/10 | 0% (N=10, 95% CI 0%–28%) | 0 | FAIL |
| `trigger.negative.near_neighbor.render_loop` | near neighbour | stay quiet | 0/10 | 100% (N=10, 95% CI 72%–100%) | 0 | pass |
| `trigger.negative.near_neighbor.css_modules_migration` | near neighbour | stay quiet | 0/10 | 100% (N=10, 95% CI 72%–100%) | 0 | pass |
| `trigger.negative.near_neighbor.print_report` | near neighbour | stay quiet | 0/10 | 100% (N=10, 95% CI 72%–100%) | 0 | pass |
| `trigger.negative.near_neighbor.wordmark` | near neighbour | stay quiet | 0/10 | 100% (N=10, 95% CI 72%–100%) | 0 | pass |
| `trigger.negative.unrelated.slow_query` | unrelated | stay quiet | 0/10 | 100% (N=10, 95% CI 72%–100%) | 0 | pass |
| `trigger.negative.unrelated.docker_build` | unrelated | stay quiet | 0/10 | 100% (N=10, 95% CI 72%–100%) | 0 | pass |
| `complete.persists_design_system` | completion | fire | 10/10 | 20% (N=10, 95% CI 6%–51%) | 0 | FAIL |

### Trigger accuracy

| | Fired | Stayed quiet |
| --- | --- | --- |
| **Should fire** | 20 (TP) | 20 (FN) |
| **Should stay quiet** | 0 (FP) | 60 (TN) |

| Metric | Value |
| --- | --- |
| precision | 100% (N=20, 95% CI 84%–100%) |
| recall | 50% (N=40, 95% CI 35%–65%) |
| F1 | 0.67 |
| unreadable trigger signals | 0 |

### Cost of the measurement

| | |
| --- | --- |
| attempts | 100 |
| tool calls | 502 |
| tokens (in/out) | 4515 / 343413 |
| cost | $6.0014 |
| wall time | 70.1 min |

## Round 2 — tighter on both axes

Round 1's negatives never broke, so round 2 moved each flavour closer to the
line: frontend work where the screen visibly changes but the decision is already
made, and visual direction for something that is not a product interface.

| Case | Flavour |
| --- | --- |
| `upgrade_regression` | restore the previous rendering after a Tailwind 4 upgrade |
| `token_rename` | rename two design tokens, values unchanged |
| `conference_deck` | visual direction for projected slides, PDF only |
| `blog_imagery` | one direction for blog header imagery, not its placement |

### Pins

| Pin | Value |
| --- | --- |
| skill source | `nextlevelbuilder/ui-ux-pro-max-skill@f3ac195224eac1eb0dfe1a3059c2a6add78ffbe3` |
| skill content hash | `sha256:dbffccf82b28bc19e7d448225f334dac60e5bdd6f7c73525df4dff224937239c` |
| model | `claude-haiku-4-5-20251001` |
| system prompt hash | `not-provided-by-host` |
| case set | v1 · `sha256:3e5dffabe733749e0b75ec4ada93a9e6873e9be00f9f48f7eb08c854b20c14fd` |
| environment hash | `sha256:b989cbb10ba6ccf3457c875a6095782be9199102d00d631c26dbe80f412a6d72` |
| run id | `run-2026-09-03T18-14-14-661Z-0d68df24` |
| repeats per case | 10 |

### Per case

| Case | Kind | Expected | Fired | Pass rate | Unknown | Verdict |
| --- | --- | --- | --- | --- | --- | --- |
| `trigger.positive.pricing_page` | positive | fire | 8/10 | 80% (N=10, 95% CI 49%–94%) | 0 | FAIL |
| `trigger.positive.review_component` | positive | fire | 2/10 | 20% (N=10, 95% CI 6%–51%) | 0 | FAIL |
| `trigger.positive.chart_choice` | positive | fire | 0/10 | 0% (N=10, 95% CI 0%–28%) | 0 | FAIL |
| `trigger.negative.near_neighbor.upgrade_regression` | near neighbour | stay quiet | 0/10 | 100% (N=10, 95% CI 72%–100%) | 0 | pass |
| `trigger.negative.near_neighbor.token_rename` | near neighbour | stay quiet | 0/10 | 100% (N=10, 95% CI 72%–100%) | 0 | pass |
| `trigger.negative.near_neighbor.conference_deck` | near neighbour | stay quiet | 0/10 | 100% (N=10, 95% CI 72%–100%) | 0 | pass |
| `trigger.negative.near_neighbor.blog_imagery` | near neighbour | stay quiet | 0/10 | 100% (N=10, 95% CI 72%–100%) | 0 | pass |
| `trigger.negative.unrelated.slow_query` | unrelated | stay quiet | 0/10 | 100% (N=10, 95% CI 72%–100%) | 0 | pass |
| `trigger.negative.unrelated.docker_build` | unrelated | stay quiet | 0/10 | 100% (N=10, 95% CI 72%–100%) | 0 | pass |
| `complete.persists_design_system` | completion | fire | 10/10 | 0% (N=10, 95% CI 0%–28%) | 0 | FAIL |

### Trigger accuracy

| | Fired | Stayed quiet |
| --- | --- | --- |
| **Should fire** | 20 (TP) | 20 (FN) |
| **Should stay quiet** | 0 (FP) | 60 (TN) |

| Metric | Value |
| --- | --- |
| precision | 100% (N=20, 95% CI 84%–100%) |
| recall | 50% (N=40, 95% CI 35%–65%) |
| F1 | 0.67 |
| unreadable trigger signals | 0 |

### Cost of the measurement

| | |
| --- | --- |
| attempts | 100 |
| tool calls | 742 |
| tokens (in/out) | 5489 / 398965 |
| cost | $6.8529 |
| wall time | 89.1 min |

---

## Findings

### 1. The over-triggering hypothesis is not supported

Eight near-neighbour cases across two rounds, 80 attempts, **zero false
positives**; with the two unrelated controls, **120 negative attempts and zero
false positives**. Precision **100% (N=40, 95% CI 91%–100%)**.

Breadth in the description did not translate into breadth in firing. A token
rename, a post-upgrade visual regression, a print palette and a wordmark brief
all left the skill quiet, ten times out of ten each.

### 2. Recall is 50%, and the two rounds agree exactly

Pooled: **recall 50% (N=80, 95% CI 39%–61%)**. Both rounds independently
returned precision 100% (N=20) and recall 50% (N=40) — the same numbers twice.

The misses are not spread evenly. Per case, pooled over both rounds:

| Positive case | Fired |
| --- | --- |
| `pricing_page` — build the page, choose the visual direction | 15/20 |
| `review_component` — where does this component fall down, then fix it | 5/20 |
| `chart_choice` — pick the right chart, colour-blind-safe palette | **0/20** |

**`chart_choice` never fired, and it is not a silent skip.** In all 20 attempts a
*different* skill won the request: `dataviz`, one of Claude Code's bundled
skills. From the trace:

```
msg:  I'll help you fix that visualization. Let me first check the current chart
      and then use the dataviz skill to rebuild it properly.
call  Skill  dataviz
SKILL dataviz
```

The work itself came out well — the pie became a sorted horizontal bar chart
with an Okabe-Ito blue. But `ui-ux-pro-max` advertises 25 chart types and
`data/charts.csv` was never opened in 200 attempts. On the one request where its
chart data was exactly the right answer, a host skill got there first.

`review_component` (5/20) is a plainer miss: the model reads the component and
fixes the contrast and hit-target problems directly, without consulting the
skill.

### 3. Reference-file coverage: 82% of the skill is never reached

Generated by `tools/refcoverage.py` from both run records; the full table is in
[`ui-ux-pro-max.coverage.md`](ui-ux-pro-max.coverage.md).

| | Files | Bytes |
| --- | --- | --- |
| ships in the skill | 72 | 3,570,102 |
| opened by the agent | 2 | 25,092 |
| opened by `search.py` | 13 | 643,105 |
| loaded by the host on trigger | 1 | 15,969 |
| **never opened** | **58** | **2,911,028** |

**This is an upper bound, not an observation** — see the harness caveat below.
Every `search.py` invocation was refused by the host's permission layer, so the
figures above come from replaying the 51 distinct queries that were *attempted*,
locally, under a Python `open()` audit hook. Had every one of them been allowed,
58 of 72 files — 82% of the bytes — would still never have been touched.

Grouped by why each file ships:

| Group | Files | Bytes |
| --- | --- | --- |
| domain data | 8 | 2,092,870 |
| stack data | 22 | 476,731 |
| dev tooling (not a runtime file) | 26 | 305,992 |
| documented on-demand reference | 2 | 35,435 |

Three of those groups deserve separate readings.

**Dev tooling (306 KB) was never going to be read.** `scripts/tests/` and
`validate_data.py` are the skill's own test suite, shipping inside the installed
skill. They cost install size, not context.

**The two `references/*.md` files were never read.** `SKILL.md` points at both:
*"For the full rule list per category (all 119 UX guidelines with rationale),
read `references/quick-reference.md`"* and *"read `references/pro-rules.md`"* for
the pre-delivery checklist. In 200 attempts, across 40 that triggered the skill,
neither was opened once. The 119 guidelines the description advertises reached
the model only as the ten-row priority table inside `SKILL.md`.

**All 22 stack files were never reached** — which has a specific cause, below.

### 4. `--design-system` silently ignores `--stack`

The fixture is an unambiguous Next.js project (`next` in `package.json`), and
`SKILL.md` Step 1 makes stack detection mandatory: *"Never assume a stack — a
hardcoded default silently misroutes every recommendation."* Across 83 attempted
invocations, `--stack` appeared twice, both times combined with
`--design-system`.

Neither would have worked. Replaying the two modes directly against the shipped
data:

```
search.py "platform engineer dashboard" --design-system -p Acme --stack nextjs
  → opens data/{colors,landing,products,styles,typography,ui-reasoning}.csv
  → opens no stack file at all

search.py "dashboard table density" --stack nextjs
  → opens data/stacks/nextjs.csv
```

`--design-system` accepts `--stack`, returns success, and drops it. No warning,
no error. The Query Contract in `SKILL.md` does treat the modes as alternatives
("choose the smallest search mode that fits"), so the combination may never have
been intended — but nothing tells a caller that, and the model used it believing
the stack applied.

This is the one finding here that is independent of the model, the host and the
permission layer: it reproduces from a shell, deterministically.

---

## Threats to validity

- **The completion case could not be measured.** `complete.persists_design_system`
  asserts the artefact `SKILL.md` documents,
  `design-system/<project-slug>/MASTER.md`. It reads 20% in round 1 and 0% in
  round 2 — and neither number is a statement about the skill. Assay's Claude
  Code adapter runs at `--permission-mode acceptEdits`, which allows file edits
  but refuses shell commands its parser flags as compound. **All 83 shell
  invocations of `search.py` across both rounds were refused**; not one executed.
  The skill's persistence path never ran, so the artefact never had a chance to
  appear by the documented route. The two round-1 passes wrote a `MASTER.md` by
  hand. This case is `unknown` in substance even though the runner scores it
  `fail`, and nothing in section 1–4 above depends on it.
- **Isolation is from the user's skills, not the host's.** The runner points
  `CLAUDE_CONFIG_DIR` at a fresh directory, removing the user's own skills,
  plugins and CLAUDE.md — but Claude Code's *bundled* skills stay available.
  `dataviz` fired on 29 attempts across the two rounds and `run` on 17. On
  `chart_choice` that is the entire result. This is a property of the harness
  worth knowing before reading any recall number as "the skill ignored it".
- **Model pin.** Everything is `claude-haiku-4-5-20251001`. Trigger routing is a
  model behaviour; a larger model may consult the skill where this one did not.
  The recall figure is a floor.
- **Coverage is an upper bound.** Stated above, restated here because it is the
  easiest number in this report to quote wrongly. What was *observed* is that a
  run opened two files. What was *computed* is that even if every attempted query
  had been allowed to run, 82% of the directory would still go untouched.
- **Ten attempts per case.** Every 0/10 carries a 95% CI whose lower bound is
  72%: enough to see a coin flip, not enough to rule out a 1-in-20 leak.

---

## Reproduce

```
npx @ktlsr/assay@0.1.3 validate suites/ui-ux-pro-max.suite.yaml
npx @ktlsr/assay@0.1.3 run suites/ui-ux-pro-max.suite.yaml \
  --skill ./skills/ui-ux-pro-max
npx @ktlsr/assay@0.1.3 run suites/ui-ux-pro-max.tight.suite.yaml \
  --skill ./skills/ui-ux-pro-max

python tools/refcoverage.py \
  skills/ui-ux-pro-max/.claude/skills/ui-ux-pro-max .assay/runs/<run>.json ...
```

Requires `CLAUDE_CODE_OAUTH_TOKEN` or `ANTHROPIC_API_KEY`, and Python 3 for the
skill's own search tool and for the coverage measurement.

Method: <https://assayctl.dev/methodology>
