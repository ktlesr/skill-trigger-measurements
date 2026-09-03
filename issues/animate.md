# Measurement: `animate` keeps its declared boundary; recall is 90% and the misses reproduce the defect Hard Rule 2 forbids

I ran a trigger-discrimination measurement against `skills/animate/` and wanted
to share the numbers, because one of them is a clean result worth knowing and the
other is a gap that has a concrete cost in the output.

## Setup

- Skill: `emilkowalski/skills@d23d7f88a2e21c9e4b1418c7abe420f5c1052ba7`,
  `skills/animate/` (content hash `sha256:45ba81da…2577d69`)
- Host: Claude Code. Model pinned to `claude-haiku-4-5-20251001`.
- **The skill was installed alone.** `review-animations`, `improve-animations`
  and `find-animation-opportunities` were *not* present, so nothing else could
  absorb a deflected request. Whatever the boundary did, it did on this skill's
  own description.
- **No prompt contains the words "animate" or "animation."** Prompts say motion,
  transition, slide, fade, lift — so triggering could not come from a name match.
- Two case sets of 10 cases × 10 attempts = 200 attempts. Each set: 3 positives,
  4 near neighbours, 2 unrelated negatives, 1 completion case asserting
  `file_exists` plus a no-swallowed-errors trace rule. Every file-referencing
  prompt is backed by a fixture copied fresh per attempt.

## Result

Pooled over both rounds (200 attempts):

| | Value |
| --- | --- |
| precision | 100% (N=71, 95% CI 95%–100%) |
| recall | 90% (N=79, 95% CI 81%–95%) |
| false positives | 0 / 120 negative attempts |

Per round:

| Round | precision | recall |
| --- | --- | --- |
| 1 — critique / audit neighbours | 100% (N=36, 95% CI 90%–100%) | 92% (N=39, 95% CI 80%–97%) |
| 2 — edit-existing-motion neighbours | 100% (N=35, 95% CI 90%–100%) | 88% (N=40, 95% CI 74%–95%) |

### The boundary in the description holds

Round 1 tested the line the description draws, one case per sibling skill:

| Near-neighbour case | Assigned by the description to | Fired |
| --- | --- | --- |
| critique why a modal entrance feels cheap, no edits | `review-animations` | 0/10 |
| write the review comment for a PR's transition | `review-animations` | 0/10 |
| rank every existing motion under `src/`, report only | `improve-animations` | 0/10 |
| where motion would earn its keep on a static page | `find-animation-opportunities` | 0/10 |

Because assay flags an unbroken negative set as *bounding the false-positive rate,
not proving discrimination*, I ran a second round with neighbours that ask for a
real code change to existing motion:

| Near-neighbour case | Fired |
| --- | --- |
| strip the Cmd+K palette transition out entirely | 0/10 |
| change 900ms to 300ms, nothing else | 0/10 |
| fix a first-paint flash caused by a transition on mount | 0/10 |
| should this overlay move at all — one paragraph, no code | 0/10 |

Two of those (`strip_motion`, the yes/no question) are questions the skill's own
Step 1 gate answers, and its stated position on a keyboard-opened palette is
*"No animation. Ever."* — a reasonable case exists for firing. It stayed quiet
all 20 times. 120 negative attempts, zero false positives.

## The gap: 8 of 79 attempts that should reach the skill do not

No negative leaked. The finding is on the other side — the misses.

All 8 are trigger misses; none is an assertion failure. The model does the work
directly and the work looks finished. From the raw trace of
`trigger.positive.sidebar_collapse` #0:

```
msg:  I'll help you add a smooth animation to the sidebar width change.
call  Read   src/Sidebar.tsx
call  Read   src/sidebar.css
call  Edit   src/sidebar.css  ->  transition: width 250ms ease-in-out;
skills observed: []
```

And `complete.writes_toast_motion` #8:

```
Write src/toast.css
  @keyframes toastEnter { ... }
  .toast          { animation: toastEnter 0.3s ease-out; }
  .toast.exiting  { animation: toastExit  0.3s ease-in;  }
skills observed: []
```

A passing attempt on the same case, with the skill consulted:

```
SKILL animate
Write src/toast.css
  .toast                      { animation: toast-exit  150ms cubic-bezier(0.23, 1, 0.32, 1) forwards; }
  .toast[data-visible="true"] { animation: toast-enter 200ms cubic-bezier(0.23, 1, 0.32, 1) forwards; }
```

`250ms ease-in-out` and `0.3s ease-out` are invented values — the exact thing
Hard Rule 2 forbids ("No approximated values. Every curve, duration, and spring
config comes from the tables below"), and one miss wrote *keyframes on a toast*,
which the skill names as an example of its second failure mode. So the 10% is not
cosmetic: those attempts ship the defect the skill exists to prevent, and they
read as complete.

### The misses are spread, not clustered

Pooled over both rounds, every positive case sits at the same rate:

| Case | Fired |
| --- | --- |
| toast has no transition, give it an entrance and exit | 18/20 |
| sidebar snaps between 260px and 64px, give the width motion | 18/20 |
| feature cards feel dead on hover, add a lift | 18/20 |
| completion case, same toast request naming the output file | 17/19 |

I looked for a phrasing pattern and did not find one — a request stated as a feel
problem misses as often as one stating the mechanism. This reads as a uniform
~10% routing loss rather than a describable blind spot, which matters for what
you can do about it: there is probably no single sentence that closes it.

## Suggestion

Since the loss is uniform, a description edit is unlikely to be the lever. Two
things that might be, in order of how cheap they are:

1. **Move the invariant into the artefact, not just the skill.** The values in
   the tables are what a miss loses. A short `tokens.css` (or a snippet in the
   README) that a project can paste once — `--ease-out-quint`, the duration
   scale — means a missed routing still lands on the right curve, because the
   codebase already has it and Hard Rule 3 tells the skill to extend it.
2. **Say the cost of skipping in the first line of the body.** The description
   is what routing sees, but the body is what a partially-primed model sees. A
   sentence like *"if you are about to write a curve or a duration from memory,
   stop and read the tables"* costs nothing and catches the case where the skill
   loads late.

Neither is a fix for the routing itself, and the boundary needs no change at all
— it measured clean at 120/120. Worth knowing mainly because the failure is
silent: a missed attempt produces plausible-looking CSS and reports success.

## Reproduce

```
npx @ktlsr/assay@0.1.2 validate suites/animate.suite.yaml
npx @ktlsr/assay@0.1.2 run suites/animate.suite.yaml       --skill ./skills/animate
npx @ktlsr/assay@0.1.2 run suites/animate.tight.suite.yaml --skill ./skills/animate
```

Case sets, fixtures and stored run records are in the workspace linked above.
Needs `CLAUDE_CODE_OAUTH_TOKEN` or `ANTHROPIC_API_KEY`; each attempt runs in an
isolated config directory.

Two caveats on the numbers. Everything is pinned to
`claude-haiku-4-5-20251001` — routing is a model behaviour, so 90% is a floor,
not a universal rate. And one round-1 attempt was killed mid-session by an OAuth
token rotation; it is recorded as a `file_exists` failure but the trace shows the
skill had already triggered, so that one is an environment artefact and is
excluded from the reading above.

Method: <https://assayctl.dev/methodology>
