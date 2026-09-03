# skill-trigger-measurements

Trigger-discrimination measurements for published Agent Skills: does a skill fire
on the request it claims, stay quiet on the request next to it, and produce the
artefact it promised.

This repository is the **case sets and the reports**, not a tool. Anyone can clone
it, re-run the suites and get their own numbers.

## What has been measured

| Skill | Source | Precision | Recall | False positives |
| --- | --- | --- | --- | --- |
| [`animate`](skills/animate) | [emilkowalski/skills](https://github.com/emilkowalski/skills) `@d23d7f8` | 100% (N=71, 95% CI 95%–100%) | 90% (N=79, 95% CI 81%–95%) | 0 / 120 |
| [`better-typography`](skills/better-typography) | [jakubkrehel/skills](https://github.com/jakubkrehel/skills) `@267330e` | 100% (N=68, 95% CI 95%–100%) | 87% (N=78, 95% CI 78%–93%) | 0 / 120 |

400 attempts, two rounds each, `claude-haiku-4-5-20251001`.

- **[Comparison across both skills](reports/comparison.md)** — start here
- [`animate` report](reports/animate.md) · [issue draft](issues/animate.md)
- [`better-typography` report](reports/better-typography.md) · [issue draft](issues/better-typography.md)

## How the case sets are built

Every suite follows the same shape, and the constraints matter more than the
counts:

- **One skill active per run.** Sibling skills are not installed, so a boundary
  that holds, holds on the skill's own description rather than because something
  else caught the request.
- **No prompt contains the skill's name** — or, for `animate`, even the word
  *animation*. Triggering has to come from the request, not a string match.
- **3 positives, 4 near neighbours, 2 unrelated negatives, 1 completion case**,
  ten attempts each. The near neighbours are the whole point: requests that sit
  just outside the skill's job while sharing its subject matter. An unrelated
  negative is easy to pass and proves little.
- **Two rounds.** When no negative broke in round 1 — which happened for both
  skills — a second, deliberately tighter set was written and run, because an
  unbroken negative set bounds the false-positive rate without showing where the
  set's discriminating power ends.
- **Fixtures for every file-referencing prompt**, copied fresh into a temp
  workspace per attempt.
- **Completion cases assert an artefact**, not just a trigger: `file_exists` on
  the file the prompt names, plus a no-swallowed-errors trace rule.

## Layout

```
skills/<skill>/            vendored copy of the skill under test, pinned by commit
suites/<skill>.suite.yaml        round 1 case set
suites/<skill>.tight.suite.yaml  round 2, tighter near neighbours
fixtures/<app>/            mini projects the prompts refer to
reports/<skill>.md         the measurement report
reports/comparison.md      both skills side by side
issues/<skill>.md          issue text prepared for the skill's author
tools/                     three small scripts that build the report tables
```

## Reproduce

Needs Node 22 and either `CLAUDE_CODE_OAUTH_TOKEN` (from `claude setup-token`) or
`ANTHROPIC_API_KEY` — each attempt runs in an isolated config directory that does
not inherit an interactive session.

```
npx @ktlsr/assay@0.1.2 validate suites/animate.suite.yaml
npx @ktlsr/assay@0.1.2 run suites/animate.suite.yaml       --skill ./skills/animate
npx @ktlsr/assay@0.1.2 run suites/animate.tight.suite.yaml --skill ./skills/animate
```

Same two commands for `better-typography`. A full suite is 100 attempts and cost
about $4.70 at the pinned model; all four runs came to $18.84.

**Run records are not committed.** They land in `.assay/runs/` locally and are
gitignored, along with the raw run logs. The reports carry every number the
records contain, including the pins (skill content hash, model id, case set
hash) needed to tell whether two runs are comparable at all.

## Reading the numbers

Three conventions from the runner, worth knowing before reading a report:

- **Verdicts are three-valued.** `pass`, `fail`, `unknown`. A signal that could
  not be read is `unknown`, never a quiet `pass`.
- **No rate appears without N and a confidence interval.** `100% (N=10, 95% CI
  72%–100%)` — ten attempts say as much as ten attempts say. Every `0/10` in
  these reports has a lower bound around 72%: enough to see a coin flip, not
  enough to rule out a 1-in-20 leak.
- **Rates are pinned to a model.** Everything here is
  `claude-haiku-4-5-20251001`. Trigger routing is a model behaviour, so the
  recall figures are floors, not universal results.

Method: <https://assayctl.dev/methodology>

## Licensing and provenance

The skills under `skills/` are **unmodified copies of other people's work**,
vendored at a pinned commit so the measurement is reproducible. Both are MIT
licensed and each copy keeps its upstream `LICENSE`:

- `skills/animate/` — © Emil Kowalski, from
  [emilkowalski/skills](https://github.com/emilkowalski/skills) at
  `d23d7f88a2e21c9e4b1418c7abe420f5c1052ba7`
- `skills/better-typography/` — © Jakub Krehel, from
  [jakubkrehel/skills](https://github.com/jakubkrehel/skills) at
  `267330e1adfc66a718fb65fa6918c1f06d0a689e`

The case sets, fixtures, reports and tooling in this repository are MIT licensed
(see [LICENSE](LICENSE)).

A measurement is not a verdict on a skill. Both skills measured here kept every
boundary their authors declared; the findings are about where a request stops
reaching them.
