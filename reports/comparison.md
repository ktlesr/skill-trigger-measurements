# Two skills, same measurement — comparison

Both skills were measured the same way: installed alone, no sibling skills
present, no prompt containing the skill's name, 10 cases × 10 attempts per round,
two rounds each (the second with deliberately tighter near neighbours because
round 1's negatives never broke). 400 attempts total, `claude-haiku-4-5-20251001`,
`npx @ktlsr/assay@0.1.2`, $18.84 and 3.0 hours of measured attempt time
(about 1.5 hours on the clock, with the two suites running in parallel).

| | `animate` | `better-typography` |
| --- | --- | --- |
| precision (pooled) | 100% (N=71, 95% CI 95%–100%) | 100% (N=68, 95% CI 95%–100%) |
| recall (pooled) | 90% (N=79, 95% CI 81%–95%) | 87% (N=78, 95% CI 78%–93%) |
| false positives | 0 / 120 | 0 / 120 |
| near-neighbour cases | 8 across two rounds, all 0/10 | 8 across two rounds, all 0/10 |
| shape of the misses | uniform ~10% on every positive | concentrated: one prompt at 9/18, the rest 59/60 |
| artefact assertions | passed on every completed attempt | passed on every completed attempt |

## Where they agree

Neither skill has a precision problem. Sixteen near-neighbour cases, 240 negative
attempts, zero false positives — including neighbours built directly on each
author's own declared hand-offs, with no sibling skill installed to catch a
deflected request. Both authors wrote boundaries in prose and both boundaries are
real.

Neither skill has a completion problem either. Every attempt that reached the work
produced the artefact it was asked for; `no_swallowed_errors` never fired. Every
single failure in 400 attempts was a *trigger* failure.

## Where they differ, and it matters

**`animate`'s gap is uniform.** 18/20 on each of the three positives, 17/19 on
the completion case. I looked for a phrasing pattern and there isn't one. That
reads as routing loss, not a describable blind spot — so there is probably no
sentence the author can add to close it. It is still worth reporting, because the
misses are not silent-and-harmless: they write `250ms ease-in-out` and
`0.3s ease-out`, invented values that the skill's Hard Rule 2 exists to forbid,
and one wrote *keyframes on a toast*, an example the skill names as a defect. A
missed attempt looks finished.

**`better-typography`'s gap is a specific prompt shape.** One prompt fires 9/18
while the same underlying work, phrased as a problem, fires 20/20. The difference
is that the low-firing prompt already names its own mechanism ("define a named
scale as CSS custom properties in a new file"). The description is an artefact
list, so a request that already contains the artefact word has nothing left to
match on. That is a diagnosis with an action attached, and it reproduced
independently in two rounds.

## Which is worth sharing

**`better-typography` first.** The effect is larger (50% vs. 90%), it is tied to
an identifiable prompt shape rather than to noise, it reproduced across two
independent runs, and it comes with a concrete description edit the author can
accept or reject on its merits. The output cost is legible too: the scales
invented without the skill are the fixture's ad-hoc sizes renamed as variables —
exactly what the skill's "use a type scale with semantic names" section exists to
prevent.

**`animate` second, and framed differently.** The number is close to what routing
noise looks like at this model tier, and the honest summary is "no lever found in
the description." What makes it worth a note anyway is the failure mode, not the
rate: the 10% that skips the skill ships the defect the skill was written to
prevent and reports success. The suggestions in that draft are therefore about
making a miss survivable (put the curve tokens in the project, restate the rule at
the top of the body) rather than about rewording the trigger.

Both drafts lead with the clean boundary result, because for both skills that is
the larger finding: an author-declared boundary that measures at 120/120 is
unusual and worth saying out loud.

## Caveats that apply to both

- Everything is pinned to `claude-haiku-4-5-20251001`. Trigger routing is a model
  behaviour; these recall figures are floors, not universal rates. Re-running on a
  larger model would be the obvious next measurement — and `assay compare` will
  refuse to compare the two runs, naming the model pin as drifted, which is the
  correct behaviour.
- Ten attempts per case. Every 0/10 above carries a 95% CI whose lower bound is
  72%: enough to see a coin flip, not enough to rule out a 1-in-20 leak.
- An OAuth token rotation killed the tail of both round-1 runs. Affected attempts
  are identified in each report; round 2 ran clean for both skills and reproduces
  both findings on its own.
- Trigger is *observed*, not enforced — assay reads the `Skill` tool call from the
  host's stream-json. A skill absorbed some other way would read as "did not
  trigger".

Per-skill detail: [`animate.md`](animate.md) · [`better-typography.md`](better-typography.md)
Issue drafts: [`../issues/animate.md`](../issues/animate.md) · [`../issues/better-typography.md`](../issues/better-typography.md)

Method: <https://assayctl.dev/methodology>
