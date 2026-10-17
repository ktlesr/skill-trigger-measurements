You asked on 2026-09-07 for #744's case set as the comparison here, so here
is its document-shaped case on its own, across every measurement I have. These
numbers are all from **released versions with the old description**. #1048 is
on `main` but in no tag yet (`skill-v4.6.0` still carries the long text), so
this is the before-picture for #1048, not a test of it.

## The case

From `suites/impeccable.suite.yaml`, case `complete.persists_design_system`:

> Work out the visual system this codebase is already using - type scale,
> colour, spacing, component patterns - and write it down at the project root,
> in the file a later session would look for, so a new contributor can pick it
> up without asking.

- Fixture: `fixtures/impeccable-app`, a small React app with an existing visual
  system (`src/tokens.css`, components, routes) and no DESIGN.md or PRODUCT.md.
- Expectation: the skill fires, and `DESIGN.md` exists at the root afterwards.
- The prompt names neither the skill, the `document` command, nor "design",
  and it doesn't name DESIGN.md either: "the file a later session would look
  for" is the only pointer. That's deliberate. It's the request a user makes
  when they want what `document` does and don't know the command exists.

## How the set is built and pinned

- 12 cases: 4 UI positives, this completion case, 6 near-neighbour negatives (frontend work
  with no visual decision in it, plus a wordmark and a printed booklet), 1
  unrelated negative. The rationale for every negative is in the suite file's
  header.
- Suite `sha256:c820aafc5cc50f635fb7c46b864eb8ed1642b67bfea9daac2e634c8581a33545`,
  byte-identical in every run below.
- Model `claude-haiku-4-5-20251001`, 10 attempts per case per measurement,
  fresh isolated config per attempt, both `acceptEdits` and
  `bypassPermissions`.
- Activation is read from the host's own Skill-activation event in the
  stream, not from text in the output.

| Measurement | Skill | Host | Runner |
| --- | --- | --- | --- |
| 2026-09-06/07 | 4.2.1 | Claude Code 2.1.263 | assay 0.2.0 |
| 2026-09-08 | 4.2.2 | Claude Code 2.1.263 | assay 0.2.0 |
| 2026-10-17 | 4.2.2 (re-run) | Claude Code 2.1.302 | assay 0.5.0 |
| 2026-10-17 | 4.5.2 | Claude Code 2.1.302 | assay 0.5.0 |

## Result: 0 of 80, in every cell

| | 4.2.1 aE | 4.2.1 bP | 4.2.2 aE | 4.2.2 bP | 4.2.2r aE | 4.2.2r bP | 4.5.2 aE | 4.5.2 bP |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| skill fired | 0/10 | 0/10 | 0/10 | 0/10 | 0/10 | 0/10 | 0/10 | 0/10 |
| DESIGN.md written anyway | 10 | 9 | 10 | 6 | 8 | 10 | 9 | 8 |
| `reference/document.md` opened | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |

- **0 activations in 80 attempts** (95% upper bound ≈ 5%).
- **The base model did the job itself 70 times out of 80.** It found the right
  filename unprompted and wrote DESIGN.md without the skill.
- **`reference/document.md` was never opened in 960 attempts**, i.e. every
  attempt in all eight measurements, not just this case.
- It doesn't move with the version, the host, the runner, or the permission
  mode. The September runs also had one unrelated line of host `CLAUDE.md`
  leaking in, which the October runs don't; the result didn't change. In the
  same runs `hero_direction` and `forgettable_usage` fire 7–10/10 and precision
  is 100%, so the skill is loading. This one request shape just never reaches it.

That matches what your eval found ("the old text missed [document-shaped
requests] almost entirely"), from a different harness, model and case set.

## The same pattern in two other skills

I've measured the same failure in two other skill repos with the same
method: when a request can be met by editing a file directly, it gets met
that way, without the skill. In `marketingskills`, 93 of the 120 positive
attempts where no skill fired still wrote the files. In `ui-ux-pro-max`, a
"find where this component falls down and fix it" request fired the skill
5/20 times and was fixed directly the rest.

## Re-measuring #1048

The new description names "capturing or documenting design systems
(DESIGN.md, tokens)", which is exactly this request, so this case should move.
When #1048 is in a tagged skill release, I'll run the same pinned suite against
it, both modes, alongside a 4.5.2 re-run on the same host. That gives you this
table with one more column, on a different model from your Sonnet 5 and
Gemini Flash runs.

Per-measurement reports:
- <https://github.com/ktlesr/skill-trigger-measurements/blob/master/reports/impeccable.md> (4.2.1)
- <https://github.com/ktlesr/skill-trigger-measurements/blob/master/reports/impeccable.4.2.2.md>
- <https://github.com/ktlesr/skill-trigger-measurements/blob/master/reports/impeccable.4.5.2.md>
