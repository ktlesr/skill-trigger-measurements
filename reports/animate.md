# Measurement report — `animate`

**Skill:** `emilkowalski/skills@d23d7f88a2e21c9e4b1418c7abe420f5c1052ba7`, `skills/animate/`
**Host:** Claude Code · **Model:** `claude-haiku-4-5-20251001` · **Runner:** `npx @ktlsr/assay@0.1.2`
**Measured:** 2026-09-03 · **Attempts:** 200 across two rounds

---

## What was measured

This skill declares its own boundary in its description, which is unusual and
makes it directly testable:

> Use when asked to animate something, add motion, make a component feel alive,
> or build a transition. **For critiquing existing motion use `review-animations`;
> for auditing a whole codebase use `improve-animations`.**

The near-neighbour cases were built on exactly that line: requests that are
entirely about motion but ask for critique or audit rather than construction.
The question under test is whether a boundary an author writes in prose is a
boundary the skill actually keeps.

## Method

- The skill was installed alone in an isolated directory. `active_skills` lists
  it and nothing else — none of the sibling skills it defers to
  (`review-animations`, `improve-animations`, `find-animation-opportunities`)
  was present to catch a deflected request. If the boundary held, it held on the
  skill's own description.
- **No prompt contains the word "animate" or "animation".** Prompts say *motion*,
  *transition*, *slide*, *fade*, *lift*. Triggering had to come from the request,
  not from a string match on the skill's name.
- Ten cases per round, ten attempts each: 3 positives, 4 near neighbours,
  2 unrelated negatives, 1 completion case.
- Prompts that name a file are backed by a fixture (`fixtures/animate-app/`),
  copied fresh into a temp workspace for every attempt. The fixture deliberately
  contains motion the skill would object to: `scale(0)` with `ease-in` on a modal,
  a 900ms drawer, a transition on a Cmd+K palette.
- The completion case asserts `file_exists` on `src/toast.css` and the
  `no_swallowed_errors` trace rule.
- Both case sets passed `assay validate` before running.

---

## Round 1 — the boundary the author declared

| Case | What it asks for | Skill the description assigns it to |
| --- | --- | --- |
| `critique_modal_feel` | why the modal entrance feels cheap, no edits | `review-animations` |
| `critique_drawer_diff` | the review comment to leave on a PR's transition | `review-animations` |
| `codebase_audit` | rank every existing motion under `src/`, report only | `improve-animations` |
| `opportunity_scan` | where motion would earn its keep on a static page | `find-animation-opportunities` |

### Pins

| Pin | Value |
| --- | --- |
| skill source | `emilkowalski/skills@d23d7f88a2e21c9e4b1418c7abe420f5c1052ba7` |
| skill content hash | `sha256:45ba81da9f54aa1d53cb7a5a9cddb141222cad7b11e1c1545175479fd2577d69` |
| model | `claude-haiku-4-5-20251001` |
| system prompt hash | `not-provided-by-host` |
| case set | v1 · `sha256:789aa7faedba46d0adea3c8d1971f39c52a616eb3623ebe466f9fcb88973fbf1` |
| environment hash | `sha256:06935ec7fdf935afec04e70a1c8c39ac1e6f8534978ce40d6cbf622ecc29e6ff` |
| run id | `run-2026-09-03T11-10-04-411Z-57205e2b` |
| repeats per case | 10 |

### Per case

| Case | Kind | Expected | Fired | Pass rate | Unknown | Verdict |
| --- | --- | --- | --- | --- | --- | --- |
| `trigger.positive.build_toast_entrance` | positive | fire | 10/10 | 100% (N=10, 95% CI 72%–100%) | 0 | pass |
| `trigger.positive.sidebar_collapse` | positive | fire | 9/10 | 90% (N=10, 95% CI 60%–98%) | 0 | FAIL |
| `trigger.positive.hover_card_lift` | positive | fire | 9/10 | 90% (N=10, 95% CI 60%–98%) | 0 | FAIL |
| `trigger.negative.near_neighbor.critique_modal_feel` | near neighbour | stay quiet | 0/10 | 100% (N=10, 95% CI 72%–100%) | 0 | pass |
| `trigger.negative.near_neighbor.critique_drawer_diff` | near neighbour | stay quiet | 0/10 | 100% (N=10, 95% CI 72%–100%) | 0 | pass |
| `trigger.negative.near_neighbor.codebase_audit` | near neighbour | stay quiet | 0/10 | 100% (N=10, 95% CI 72%–100%) | 0 | pass |
| `trigger.negative.near_neighbor.opportunity_scan` | near neighbour | stay quiet | 0/10 | 100% (N=10, 95% CI 72%–100%) | 0 | pass |
| `trigger.negative.unrelated.ci_workflow` | unrelated | stay quiet | 0/10 | 100% (N=10, 95% CI 72%–100%) | 0 | pass |
| `trigger.negative.unrelated.slow_query` | unrelated | stay quiet | 0/10 | 100% (N=10, 95% CI 72%–100%) | 0 | pass |
| `complete.writes_toast_motion` | completion | fire | 8/9 | 80% (N=10, 95% CI 49%–94%) | 0 | FAIL |

### Trigger accuracy

| | Fired | Stayed quiet |
| --- | --- | --- |
| **Should fire** | 36 (TP) | 3 (FN) |
| **Should stay quiet** | 0 (FP) | 60 (TN) |

| Metric | Value |
| --- | --- |
| precision | 100% (N=36, 95% CI 90%–100%) |
| recall | 92% (N=39, 95% CI 80%–97%) |
| F1 | 0.96 |
| unreadable trigger signals | 1 |

### Cost of the measurement

| | |
| --- | --- |
| attempts | 100 |
| tool calls | 567 |
| tokens (in/out) | 4759 / 204458 |
| cost | $4.9009 |
| wall time | 48.7 min |

### Reading

The declared boundary held: **40/40 attempts stayed quiet** on the four
critique-and-audit neighbours, with no sibling skill installed to absorb them.
Precision 100%, zero false positives across all 60 negative attempts.

Assay does not credit this as a clean bill:

> no negative case broke — that bounds the false-positive rate, not the set's
> discriminating power.

Hence round 2.

Every failure in this round is a **recall** miss — the skill was not consulted —
never an assertion failure. `file_exists` and `no_swallowed_errors` passed on
every attempt that completed.

---

## Round 2 — neighbours on the construction line itself

Round 1's neighbours all shared one escape hatch: they forbade edits. Round 2
removes it. Each of these asks for a real code change to motion, and none of them
asks for an animation to be built:

| Case | The ask |
| --- | --- |
| `strip_motion` | remove the Cmd+K palette transition entirely |
| `duration_swap` | change 900ms to 300ms, nothing else |
| `mount_flash_bug` | fix a first-paint flash caused by a transition on mount |
| `yes_no_question` | should this overlay move at all — one paragraph, no code |

`strip_motion` and `yes_no_question` are the sharpest of the four: both are
questions the skill's own Step 1 gate ("Should this animate at all?") answers,
and the skill's stated position on a keyboard-opened palette is *"No animation.
Ever."* — so a plausible argument exists for firing on them. It did not.

### Pins

| Pin | Value |
| --- | --- |
| skill source | `emilkowalski/skills@d23d7f88a2e21c9e4b1418c7abe420f5c1052ba7` |
| skill content hash | `sha256:45ba81da9f54aa1d53cb7a5a9cddb141222cad7b11e1c1545175479fd2577d69` |
| model | `claude-haiku-4-5-20251001` |
| system prompt hash | `not-provided-by-host` |
| case set | v1 · `sha256:eb0097822ff89be2448221428a6e25dde3e74191096c5dfdd09d63c10a0693e0` |
| environment hash | `sha256:ce053849688d40ad20af66e54e0d77afee09de6e729ab8561c1b257da6776dee` |
| run id | `run-2026-09-03T11-58-43-521Z-0244e644` |
| repeats per case | 10 |

### Per case

| Case | Kind | Expected | Fired | Pass rate | Unknown | Verdict |
| --- | --- | --- | --- | --- | --- | --- |
| `trigger.positive.build_toast_entrance` | positive | fire | 8/10 | 80% (N=10, 95% CI 49%–94%) | 0 | FAIL |
| `trigger.positive.sidebar_collapse` | positive | fire | 9/10 | 90% (N=10, 95% CI 60%–98%) | 0 | FAIL |
| `trigger.positive.hover_card_lift` | positive | fire | 9/10 | 90% (N=10, 95% CI 60%–98%) | 0 | FAIL |
| `trigger.negative.near_neighbor.strip_motion` | near neighbour | stay quiet | 0/10 | 100% (N=10, 95% CI 72%–100%) | 0 | pass |
| `trigger.negative.near_neighbor.duration_swap` | near neighbour | stay quiet | 0/10 | 100% (N=10, 95% CI 72%–100%) | 0 | pass |
| `trigger.negative.near_neighbor.mount_flash_bug` | near neighbour | stay quiet | 0/10 | 100% (N=10, 95% CI 72%–100%) | 0 | pass |
| `trigger.negative.near_neighbor.yes_no_question` | near neighbour | stay quiet | 0/10 | 100% (N=10, 95% CI 72%–100%) | 0 | pass |
| `trigger.negative.unrelated.ci_workflow` | unrelated | stay quiet | 0/10 | 100% (N=10, 95% CI 72%–100%) | 0 | pass |
| `trigger.negative.unrelated.slow_query` | unrelated | stay quiet | 0/10 | 100% (N=10, 95% CI 72%–100%) | 0 | pass |
| `complete.writes_toast_motion` | completion | fire | 9/10 | 90% (N=10, 95% CI 60%–98%) | 0 | FAIL |

### Trigger accuracy

| | Fired | Stayed quiet |
| --- | --- | --- |
| **Should fire** | 35 (TP) | 5 (FN) |
| **Should stay quiet** | 0 (FP) | 60 (TN) |

| Metric | Value |
| --- | --- |
| precision | 100% (N=35, 95% CI 90%–100%) |
| recall | 88% (N=40, 95% CI 74%–95%) |
| F1 | 0.93 |
| unreadable trigger signals | 0 |

### Cost of the measurement

| | |
| --- | --- |
| attempts | 100 |
| tool calls | 501 |
| tokens (in/out) | 4712 / 177802 |
| cost | $4.6884 |
| wall time | 45.1 min |

### Reading

The tighter set did not break either. Pooled across both rounds: **120 negative
attempts, 0 false positives**, precision **100% (N=71, 95% CI 95%–100%)**.

The boundary this skill declares in prose is the boundary it actually keeps —
measured against neighbours that share its subject matter, its vocabulary and,
in round 2, its willingness to edit code.

---

## Findings

### 1. Recall is 90%, and the misses are the specific defect the skill exists to prevent

Pooled across both rounds: **recall 90% (N=79, 95% CI 81%–95%)** — 8 misses out
of 79 attempts that should have fired. Every miss is a trigger miss; not one
assertion failed because of one.

The misses are not harmless. From the raw trace of
`trigger.positive.sidebar_collapse` #0:

```
msg:  I'll help you add a smooth animation to the sidebar width change.
call  Read   src/Sidebar.tsx
call  Read   src/sidebar.css
call  Edit   src/sidebar.css   -> transition: width 250ms ease-in-out;
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

Compare a passing attempt on the *same case*, where the skill was consulted:

```
SKILL animate
Write src/toast.css
  .toast                      { animation: toast-exit  150ms cubic-bezier(0.23, 1, 0.32, 1) forwards; }
  .toast[data-visible="true"] { animation: toast-enter 200ms cubic-bezier(0.23, 1, 0.32, 1) forwards; }
```

The skill's Hard Rule 2 is *"No approximated values. Every curve, duration, and
spring config comes from the tables below."* The missed attempts produce
`250ms ease-in-out` and `0.3s ease-out` — invented values, precisely the failure
mode the rule names. The skill also lists *"keyframes on a toast"* as an example
of its second failure mode, and a missed attempt wrote exactly that.

So the recall gap is not cosmetic: the 10% of attempts that skip the skill
produce the output the skill was written to prevent, and they look finished.

**The misses are spread, not clustered.** Pooled across both rounds, every
positive case sits at the same rate:

| Case | Fired |
| --- | --- |
| `trigger.positive.build_toast_entrance` | 18/20 |
| `trigger.positive.sidebar_collapse` | 18/20 |
| `trigger.positive.hover_card_lift` | 18/20 |
| `complete.writes_toast_motion` | 17/19 |

No phrasing pattern separates them: the request stated as a feel problem
("the toast pops in and out", "the cards feel dead on hover") misses as often as
the one stating the mechanism ("give the width change some motion"). That is what
a uniform ~10% routing loss looks like, not a describable blind spot. It means
there is no single sentence to add that would obviously close it — but also that
one attempt in ten on any request in scope ships hand-approximated values.

### 2. The declared boundary holds

Not a defect — a positive result worth recording, and the main thing this
measurement set out to test. Eight near-neighbour cases across two rounds, 80
attempts, zero false positives, with no sibling skill installed to catch
deflected requests. Both the description-level boundary (critique → 
`review-animations`, audit → `improve-animations`) and the sharper round-2 line
(edit existing motion vs. build new motion) held at 10/10 each.

---

## Threats to validity

- **Model pin.** Everything here is `claude-haiku-4-5-20251001`. Trigger routing
  is a model behaviour; a larger model may consult the skill on prompts this one
  executed directly. The recall figure is a *floor*, not a universal rate.
- **OAuth token revoked mid-run.** The host token rotated near the end of
  round 1. `complete.writes_toast_motion` #9 is recorded `fail` on `file_exists`,
  but the trace shows the skill *did* trigger and the session then died on a 401
  before it could write. That failure is an environment artefact, not a skill
  result; the trigger signal for it is correctly `unknown`. Round 2 ran clean
  with 0 unknowns. Note that assay routes a dead session to `unknown` for the
  trigger signal but still evaluates file assertions against the empty workspace,
  so an aborted attempt can surface as an assertion `fail`.
- **Trigger is observed, not enforced.** Assay reads the `Skill` tool call from
  the host's stream-json. A skill whose content the model absorbed some other way
  would read as "did not trigger".
- **Isolation is from the user's skills, not the host's.** The runner points
  `CLAUDE_CONFIG_DIR` at a fresh directory, which removes the user's own skills,
  plugins and CLAUDE.md — but Claude Code's *bundled* skills stay available. In
  round 1 the bundled `run` skill co-fired on 3 attempts of
  `trigger.positive.hover_card_lift`, alongside the target rather than instead of
  it; no verdict turned on it, and round 2 saw none. Checked after the fact from
  the full skill list in each trigger observation.
- **Siblings absent.** Measuring the boundary with `review-animations` and
  `improve-animations` installed would test something different — competition
  between skills rather than one skill's self-restraint. This run measures the
  latter deliberately.
- **Ten attempts per case.** Every 10/10 above carries a 95% CI whose lower bound
  is 72%. Ten attempts is enough to see a coin-flip; it is not enough to rule out
  a 1-in-20 leak.

---

## Reproduce

```
git clone <this repo> && cd assay-example
npx @ktlsr/assay@0.1.2 validate suites/animate.suite.yaml
npx @ktlsr/assay@0.1.2 run suites/animate.suite.yaml --skill ./skills/animate
npx @ktlsr/assay@0.1.2 run suites/animate.tight.suite.yaml --skill ./skills/animate
```

Requires `CLAUDE_CODE_OAUTH_TOKEN` or `ANTHROPIC_API_KEY`; each attempt runs in
an isolated config directory that does not inherit an interactive session.

Method: <https://assayctl.dev/methodology>
