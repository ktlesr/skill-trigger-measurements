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
| [`ui-ux-pro-max`](skills/ui-ux-pro-max) | [nextlevelbuilder/ui-ux-pro-max-skill](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill) `@f3ac195` | 100% (N=40, 95% CI 91%–100%) | 50% (N=80, 95% CI 39%–61%) | 0 / 120 |
| [`impeccable`](skills/impeccable) | [pbakaus/impeccable](https://github.com/pbakaus/impeccable) `@831cabe` | 100% (N=28, 95% CI 88%–100%) | 56% (N=50, 95% CI 42%–69%) | 0 / 70 |

720 attempts, `claude-haiku-4-5-20251001`. **Zero false positives in 430 negative
attempts across all four** — every failure measured here is a skill that did not
fire, never one that fired when it should not have.

The first three ran two rounds each; `impeccable` ran one, with the tighter
negatives built into the first set.

- **[Comparison across the first three](reports/comparison.md)** — start here
- [`animate` report](reports/animate.md) · [issue draft](issues/animate.md)
- [`better-typography` report](reports/better-typography.md) · [issue draft](issues/better-typography.md)
- [`ui-ux-pro-max` report](reports/ui-ux-pro-max.md) · [coverage](reports/ui-ux-pro-max.coverage.md) · [issue draft](issues/ui-ux-pro-max.md) · [follow-up](reports/ui-ux-pro-max.followup.md) — finding 1 fixed upstream and re-verified; the rest still open
- [`impeccable` report](reports/impeccable.md) · [coverage](reports/impeccable.coverage.md) · [issue draft](issues/impeccable.draft.md) · [as filed](issues/impeccable-4.2.1.issue.md) — preceded by a [feasibility pilot](reports/impeccable.pilot.md) that found the skill could not activate at all under `claude -p`, and the [issue](issues/impeccable.md) · [as filed](issues/impeccable.issue.md) that came out of it

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
  negative is easy to pass and proves little. `impeccable`, whose description is
  broad enough that almost nothing about a frontend interface sits outside it,
  needed a wider set: 4 positives, 6 near neighbours, 1 unrelated, 1 completion.
- **Two rounds.** When no negative broke in round 1 — which happened for all of
  them — a second, deliberately tighter set was written and run, because an
  unbroken negative set bounds the false-positive rate without showing where the
  set's discriminating power ends. `impeccable` is the exception: its first set
  was written tight, with a near neighbour in the same file a positive case
  targets, and only one round has been run.
- **Requests the skill's own description claims are never used as negatives.**
  A skill that lists accessibility or performance in its description is doing its
  job when it fires on them; scoring that as a false positive would measure the
  case set, not the skill.
- **Fixtures for every file-referencing prompt**, copied fresh into a temp
  workspace per attempt.
- **Completion cases assert an artefact**, not just a trigger: `file_exists` on
  the file the prompt names, plus a no-swallowed-errors trace rule.

### Reference-file coverage

For skills that ship more than a `SKILL.md`, a second measurement asks which of
those files a run actually opens. `tools/refcoverage.py` reads the stored traces
for files the agent opened directly, and — for a skill whose own script opens
data files that no tool call ever names — replays the queries that occurred under
a Python `open()` audit hook. It separates calls that *ran* from calls the host
*refused*, because a refused command opens nothing, and it excludes files the
host loads on trigger rather than counting them as unread.

A skill whose helper is a compiled binary (`--exec impeccable`) cannot be
replayed that way: an audit hook cannot see inside another process. There the
tool counts the invocations — attempted, refused, executed — and reports the
files only that binary could open as **not observable** rather than as
never-opened. A file the instrument cannot see is not a file the run did not
read.

## Layout

```
skills/<skill>/            vendored copy of the skill under test, pinned by commit
suites/<skill>.suite.yaml        round 1 case set
suites/<skill>.tight.suite.yaml  round 2, tighter near neighbours
fixtures/<app>/            mini projects the prompts refer to
reports/<skill>.md         the measurement report
reports/<skill>.coverage.md      which of the skill's own files a run opened
reports/<skill>.followup.md      re-check of a single finding after an upstream fix
reports/comparison.md      the first three side by side
issues/<skill>.md          issue text prepared for the skill's author
issues/<skill>.issue.md          the same text in the project's own bug template
tools/                     small scripts: report tables, trace inspection,
                           reference-file coverage
```

## Reproduce

Needs Node 22 and either `CLAUDE_CODE_OAUTH_TOKEN` (from `claude setup-token`) or
`ANTHROPIC_API_KEY` — each attempt runs in an isolated config directory that does
not inherit an interactive session.

```
npx @ktlsr/assay@0.1.3 validate suites/animate.suite.yaml
npx @ktlsr/assay@0.1.3 run suites/animate.suite.yaml       --skill ./skills/animate
npx @ktlsr/assay@0.1.3 run suites/animate.tight.suite.yaml --skill ./skills/animate
```

Same two commands for `better-typography` and `ui-ux-pro-max` (the latter needs
Python 3 for the skill's own search tool). A full suite is 100 attempts and cost
$4.30–$6.90 at the pinned model; those three came to $32.18.

`impeccable` is one 120-attempt suite on a newer runner, because 0.1.3 counted a
refused activation as a trigger and this skill's activations were being refused:

```
npx @ktlsr/assay@0.2.0 run suites/impeccable.suite.yaml --skill ./skills/impeccable
```

$8.11, plus $0.84 for the smoke test and the two permission probes.

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
- **Isolation is from the user's skills, not the host's.** The runner gives each
  attempt a fresh `CLAUDE_CONFIG_DIR`, which removes the user's own skills,
  plugins and CLAUDE.md — but Claude Code's bundled skills stay available and can
  win a request. Every report states what was observed on this axis.
- **The permission mode is part of the measurement.** Everything here is
  `acceptEdits`. A skill measured with its own shell access granted and the same
  skill measured without it are two different measurements, and from assay 0.2.0
  the mode is folded into the environment hash so the two do not silently
  compare.

Method: <https://assayctl.dev/methodology>

## Licensing and provenance

The skills under `skills/` are **unmodified copies of other people's work**,
vendored at a pinned commit so the measurement is reproducible. Each copy keeps
its upstream `LICENSE` — the first three are MIT, `impeccable` is Apache 2.0:

- `skills/animate/` — © Emil Kowalski, from
  [emilkowalski/skills](https://github.com/emilkowalski/skills) at
  `d23d7f88a2e21c9e4b1418c7abe420f5c1052ba7`
- `skills/better-typography/` — © Jakub Krehel, from
  [jakubkrehel/skills](https://github.com/jakubkrehel/skills) at
  `267330e1adfc66a718fb65fa6918c1f06d0a689e`
- `skills/ui-ux-pro-max/` — © Next Level Builder, from
  [nextlevelbuilder/ui-ux-pro-max-skill](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill)
  at `f3ac195224eac1eb0dfe1a3059c2a6add78ffbe3`. Repackaged as a minimal plugin
  directory holding this one skill, so its `${CLAUDE_PLUGIN_ROOT}` script path
  resolves; the skill's own files are unmodified.
- `skills/impeccable/` — Apache 2.0, from
  [pbakaus/impeccable](https://github.com/pbakaus/impeccable) at
  `831cabee8b4bc1a2b66e5ae22003e9a19b57d464`. This is the plugin cache produced
  by `claude plugin install impeccable@impeccable`, vendored verbatim.

The case sets, fixtures, reports and tooling in this repository are MIT licensed
(see [LICENSE](LICENSE)).

A measurement is not a verdict on a skill. All four measured here kept every
boundary their authors declared, across 430 negative attempts; the findings are
about where a request stops reaching them, and — for `impeccable` — what a skill
can still not do after it has been reached.
