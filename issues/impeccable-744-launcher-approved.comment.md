# Comment prepared for pbakaus/impeccable#744

Delivers the run promised in my previous comment on that thread. Post as-is.

---

I said I had not yet made the run that would settle whether findings 1 and 2 are
consequences of finding 3. I have now made it, and it changes two of my own
claims — one of them against me. Both are below rather than buried.

**Version caveat first, because it matters:** this is **4.2.1**, the same pin as
the original #744 measurement. I deliberately did not move to 4.2.2, because the
only variable I wanted to change was the permission mode. So #750's clearer
skill-directory resolution and post-failure fallback are **not** in these
numbers. Read finding 4 below as the 4.2.1 baseline that #750 was aimed at, not
as a verdict on it.

## How the separation was set up

Same suite, same case-set hash, same skill hash, same model, 120 attempts. Only
`--permission-mode` changed.

| | launcher refused | ran |
| --- | --- | --- |
| `acceptEdits` (the #744 run) | 55 / 55 | 0 |
| `bypassPermissions` | **0 / 57** | **42** |

That inversion is clean, so anything that moves between the two runs is
downstream of the launcher, and anything that does not, is not.

## Finding 1 is independent, and stands

| | `acceptEdits` | `bypassPermissions` |
| --- | --- | --- |
| completion case fired | 0 / 10 | **0 / 10** |
| `DESIGN.md` written anyway | 10 / 10 | 9 / 10 |
| `document.md` opened | 0 | **0** |

Not one of the twenty attempts across both modes reached for the skill, and
nineteen wrote the artefact regardless. `document.md` was never opened in either.
The skill is not reached at all here, so whether its launcher works was never
relevant to this case.

You said you would coordinate activation coverage with #375 rather than expand
the description without evidence. That is the right instinct, and this is the
evidence for that specific question: the activation gap on a `document`-shaped
request is not a permission artefact and does not disappear when the skill's own
tooling works.

## Finding 2 is weaker than I claimed, and I withdraw part of it

**I was wrong about `craft-floor.md`.** From a small probe I said it was still
never read even with the launcher approved. It is read — 6 times. I retract that.

What survives is narrower, and I would restate the finding as this rather than
what I originally wrote:

| | `acceptEdits` | `bypassPermissions` |
| --- | --- | --- |
| activations that edited UI | 28 | 29 |
| of those, loaded `craft-floor.md` first | 0 | **6** |

0% → 21%. `SKILL.md` step 3 asks for it immediately before editing UI; 23 of the
29 UI-editing activations still went ahead without it. That is a real gap, but it
is not the "never read" I reported.

The wider claim also weakens. Reference reads go from 0 to 29, across 7 of the 35
files, and **the routing works when it runs** — `layout.md` and `operate.md` for
a settings hierarchy rework, `onboard.md` for an empty state, `bolder.md` for
"make it memorable". Each is the reference your command table names. My framing
in #744 was that the reference tier is unreachable; the accurate version is that
it was unreachable *in that configuration*, largely because of finding 3.

## Finding 4 got worse once the calls were permitted

In #744 I wrote that the mis-resolved `<skill-base-dir>` paths "cost nothing in
this run" because everything was refused anyway. With the calls permitted they
cost what you would expect. Of the 57 launcher invocations:

| Outcome | Count |
| --- | --- |
| ran | 42 |
| failed — path does not exist (`<plugin-root>/scripts/…`) | **9** |
| failed — `ParserError: Unexpected token 'context'` (quoted `.cmd` without `&`) | **6** |
| refused by the permission layer | **0** |

**26% of launcher calls fail for reasons that belong to the skill, not the
host** — a number that was invisible while the permission layer refused
everything. This is the part #750 most plausibly already addresses; I have not
measured 4.2.2, so I am not claiming it does or does not.

## Coverage

**7 of 35 reference files read**, against 0 before. `new-work.md` (12 reads),
`craft-floor.md` (6), `init.md` (3), `layout.md` (3), `bolder.md` (2),
`onboard.md` (2), `operate.md` (1). **28 of 35 still never opened**, including
`critique.md` (43 KB), `document.md` (28 KB), `polish.md`, `harden.md` and every
`degraded/` fallback.

## What did not move

Routing. Precision 100% in both modes (N=28 and N=30), 0 false positives in 70
negative attempts each, and no per-case difference clears its confidence
interval. Whatever the permission mode does, it does not change what the skill
fires on.

## One operational note

If you ever measure this way yourselves: a `bypassPermissions` run of this skill
destroys its own test runner. The agent starts dev servers to verify its work and
then kills processes *by port*; the servers outlive the attempt and pile up on
Vite's port ladder (I caught 13 orphans holding 5173–5178), and the runner is a
`node` process in the same space. Two attempts at a single 120-attempt run died
with no output. The run had to be split into five records of 24 with orphans
cleared between them — identical pins throughout, pooled rather than read off one
summary.

---

Full report, with the per-case tables and the method:
<https://github.com/ktlesr/skill-trigger-measurements/blob/master/reports/impeccable.launcher-approved.md>

The original `acceptEdits` numbers are unchanged and still stand as that
measurement; I have annotated the corrections in place rather than editing them
away.

Standing offer from my last comment still holds: the case set is pinned, so I can
run the same 120 attempts against 4.2.2 and post the numbers here — that would
show what #750 does to findings 2 and 4 specifically.
