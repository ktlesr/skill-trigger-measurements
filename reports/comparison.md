# Three skills, same measurement — comparison

Each skill was measured the same way: installed in isolation, no prompt
containing the skill's name, 10 cases × 10 attempts per round, two rounds each
(the second with deliberately tighter near neighbours, because in all three cases
round 1's negatives never broke). 600 attempts, `claude-haiku-4-5-20251001`,
$32.18 including smoke runs.

| | `animate` | `better-typography` | `ui-ux-pro-max` |
| --- | --- | --- | --- |
| precision (pooled) | 100% (N=71, CI 95–100%) | 100% (N=68, CI 95–100%) | 100% (N=40, CI 91–100%) |
| recall (pooled) | 90% (N=79, CI 81–95%) | 87% (N=78, CI 78–93%) | **50% (N=80, CI 39–61%)** |
| false positives | 0 / 120 | 0 / 120 | 0 / 120 |
| shape of the misses | uniform ~10% everywhere | one prompt at 9/18, rest 59/60 | one case at 0/20, one at 5/20 |
| artefact assertions | passed on every completed attempt | passed on every completed attempt | not measurable (see below) |
| shipped files | 2 | 8 | 72 (3.57 MB) |

## The result that survived all three

**Zero false positives in 360 negative attempts.** Twenty-four near-neighbour
cases, written against three different kinds of boundary — an author's declared
hand-off to sibling skills, a keyword list that overlaps ordinary frontend
vocabulary, and a deliberately comprehensive capability claim — and not one of
them fired.

The third measurement was designed to break that pattern. `ui-ux-pro-max`
advertises 79 styles, 192 palettes and 22 stacks and claims "designing, building,
reviewing, or fixing interfaces"; the near neighbours put a token rename, a
post-upgrade visual regression, a CMYK print palette and a wordmark brief in
front of it. It stayed quiet 120 times out of 120. Breadth in a description did
not produce breadth in firing.

Across three skills the failure mode is consistently **under-triggering, never
over-triggering.** That is worth saying plainly, because it inverts the intuition
that a broad description is the risky one.

## Where they differ

**`animate` — a uniform ~10% loss with a sharp consequence.** 18/20 on every
positive; no phrasing pattern behind the misses. The reason to report it is not
the rate but what a miss writes: `250ms ease-in-out`, `0.3s ease-out`, and once
keyframes on a toast — invented values that the skill's own Hard Rule 2 forbids
and that its second failure mode names by example. A missed attempt looks
finished.

**`better-typography` — one identifiable prompt shape.** The same work phrased as
a problem fires 20/20; phrased with its own mechanism named ("define a named
scale as CSS custom properties in a new file") it fires 9/18. Reproduced
independently in two rounds, with a concrete description edit attached.

**`ui-ux-pro-max` — half the requests never arrive, and most of the skill is
never read.** Both rounds returned recall 50% independently. One positive
(`chart_choice`) fired 0/20, losing every time to `dataviz`, a skill bundled with
Claude Code. And the reference-coverage pass — the measurement added for this
skill — found 58 of 72 shipped files, 82% of the bytes, never reached even under
the generous assumption that every attempted query had been allowed to run. That
includes all 22 stack files, both `references/*.md` files that `SKILL.md`
explicitly tells the model to read on demand, and 306 KB of the skill's own test
suite shipping inside the installed skill.

It also produced the only finding in this repository that needs no model, no host
and no statistics: **`--design-system` accepts `--stack` and silently ignores
it.** `--stack nextjs` alone opens `data/stacks/nextjs.csv`; combined with
`--design-system` it opens no stack file, exits successfully, and says nothing.

## Which is worth sharing

**`ui-ux-pro-max` first.** It has the only deterministic, reproduce-in-ten-seconds
defect of the three, plus a coverage finding with an obvious cheap action
(stop shipping `scripts/tests/`) and a real question for the author about the
on-demand reference tier. Its recall number is also the largest effect measured
anywhere in this repository.

**`better-typography` second.** A 50%-vs-100% split tied to an identifiable
prompt shape, reproduced across two runs, with a concrete description edit the
author can accept or reject on its merits.

**`animate` third, and framed differently.** The rate is close to routing noise at
this model tier and the honest summary is "no lever found in the description".
What makes it worth a note is the silence of the failure, not its frequency.

All three drafts lead with the clean precision result, because for all three that
is the larger finding.

## Caveats that apply to all three

- **Model pin.** Everything is `claude-haiku-4-5-20251001`. Trigger routing is a
  model behaviour; these recall figures are floors, not universal rates. Rerunning
  on a larger model is the obvious next measurement — and `assay compare` will
  refuse to compare the two, naming the model pin as drifted, which is correct.
- **Isolation is from the user's skills, not the host's.** The runner points
  `CLAUDE_CONFIG_DIR` at a fresh directory, which removes the user's own skills,
  plugins and CLAUDE.md, but Claude Code's *bundled* skills stay available and can
  win a request. Checked in every run: `better-typography` saw none;
  `animate` saw `run` co-fire on 3 attempts of one positive, changing no verdict;
  `ui-ux-pro-max` saw `dataviz` fire on 29 attempts and `run` on 17, and on one
  case that is the whole result.
- **The host's permission layer can block a skill's mechanism.** Assay's Claude
  Code adapter runs at `--permission-mode acceptEdits`: file edits are allowed,
  shell commands its parser flags as compound are refused. `ui-ux-pro-max` drives
  everything through a Python script, and **all 83 invocations were refused**, so
  its completion case measured the harness rather than the skill. A skill whose
  core mechanism is a shell command cannot currently be measured end to end this
  way. The two earlier skills are pure-markdown and were unaffected.
- **Trigger is observed, not enforced.** Assay reads the `Skill` tool call from
  the host's stream-json. A skill absorbed some other way reads as "did not
  trigger".
- **Ten attempts per case.** Every `0/10` above carries a 95% CI whose lower bound
  is 72%: enough to see a coin flip, not enough to rule out a 1-in-20 leak.

Per-skill detail: [`animate.md`](animate.md) · [`better-typography.md`](better-typography.md) · [`ui-ux-pro-max.md`](ui-ux-pro-max.md)
Issue drafts: [`../issues/animate.md`](../issues/animate.md) · [`../issues/better-typography.md`](../issues/better-typography.md) · [`../issues/ui-ux-pro-max.md`](../issues/ui-ux-pro-max.md)

Method: <https://assayctl.dev/methodology>
