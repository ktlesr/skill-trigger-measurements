# A missed trigger writes the curves Hard Rule 2 forbids

I measured trigger discrimination on `skills/animate/`. The headline is not the
rate — it is that a miss is silent. When the skill is not consulted, the model
writes the animation anyway, invents the curve and the duration, and reports
success. The output looks finished and violates the rule the skill opens with.

## Setup

- `emilkowalski/skills@d23d7f88a2e21c9e4b1418c7abe420f5c1052ba7`, `skills/animate/`
- Claude Code, model pinned to `claude-haiku-4-5-20251001`
- **Skill installed alone** — `review-animations`, `improve-animations` and
  `find-animation-opportunities` absent, so nothing else could absorb a request
- **No prompt contains "animate" or "animation"** — motion, transition, slide, lift
- Two case sets, 10 cases × 10 attempts = 200 attempts. Each set: 3 positives,
  4 near neighbours, 2 unrelated negatives, 1 completion case asserting
  `file_exists` and a no-swallowed-errors trace rule

## What a miss produces

`trigger.positive.sidebar_collapse` #0 — the skill was never called:

```
call  Edit  src/sidebar.css  ->  transition: width 250ms ease-in-out;
skills observed: []
```

`complete.writes_toast_motion` #8 — same:

```
Write src/toast.css
  @keyframes toastEnter { ... }
  .toast          { animation: toastEnter 0.3s ease-out; }
  .toast.exiting  { animation: toastExit  0.3s ease-in;  }
skills observed: []
```

A passing attempt on that same case, with the skill consulted:

```
SKILL animate
Write src/toast.css
  .toast                      { animation: toast-exit  150ms cubic-bezier(0.23, 1, 0.32, 1) forwards; }
  .toast[data-visible="true"] { animation: toast-enter 200ms cubic-bezier(0.23, 1, 0.32, 1) forwards; }
```

`250ms ease-in-out` and `0.3s ease-out` are invented values — exactly what Hard
Rule 2 forbids ("No approximated values. Every curve, duration, and spring config
comes from the tables below"). One miss wrote *keyframes on a toast*, which the
skill itself names as an example of its second failure mode.

Every miss also passed its assertions: `file_exists` and `no_swallowed_errors`
held on every completed attempt. Nothing in the run signals that the wrong thing
was written — only that the skill was absent.

## Rate

Pooled over both rounds: recall **90% (N=79, 95% CI 81%–95%)**, precision
**100% (N=71, 95% CI 95%–100%)**, **0 false positives in 120 negative attempts**.

The 8 misses are spread evenly — 18/20 on each of the three positives, 17/19 on
the completion case — and I could not find a phrasing pattern behind them. So I
am not claiming a describable blind spot in the description; the cause is
unknown. What is measurable is the consequence above.

Worth saying separately: **the boundary you declared holds.** Eight near-neighbour
cases, 80 attempts, 0 firings — critique a modal, review a PR's transition, audit
every motion under `src/`, find where motion would help, strip a Cmd+K
transition, swap 900ms for 300ms, fix a first-paint flash, answer
should-this-move-at-all. With no sibling skill installed to catch any of them.

## Suggestion

The cause of the loss is unknown, so I would not restructure anything around it.
One cheap thing that targets the consequence rather than the routing: **restate
the cost of skipping at the top of the body.** The description is what routing
sees; the body is what a partially-primed model sees. A line near the top — *"if
you are about to write a curve or a duration from memory, stop and read the
tables"* — costs nothing and catches the case where the skill loads late.

## Reproduce

```
npx @ktlsr/assay@0.1.2 validate suites/animate.suite.yaml
npx @ktlsr/assay@0.1.2 run suites/animate.suite.yaml       --skill ./skills/animate
npx @ktlsr/assay@0.1.2 run suites/animate.tight.suite.yaml --skill ./skills/animate
```

Case sets, fixtures and both reports: <https://github.com/ktlesr/skill-trigger-measurements>
Run records stay local (`.assay/runs/`, not committed); happy to attach the JSON.

Caveats: everything is pinned to `claude-haiku-4-5-20251001`, and routing is a
model behaviour, so 90% is a floor rather than a universal rate. One round-1
attempt was killed mid-session by an OAuth token rotation — recorded as a
`file_exists` failure, but the trace shows the skill had already triggered, so it
is an environment artefact and is excluded above.

Method: <https://assayctl.dev/methodology>
