# `impeccable` — trigger discrimination and resource usage

The pilot ([`reports/impeccable.pilot.md`](impeccable.pilot.md)) could not measure
this skill: version 4.2.0 declared `allowed-tools` in its frontmatter, which turns
activation into a permission prompt, and under `claude -p` there is nobody to
answer it. Every activation was denied and the pilot measured the base model.

Version 4.2.1 removes those two lines. **The skill now activates.** This is the
measurement the pilot could not run.

| | |
| --- | --- |
| Skill | `impeccable` 4.2.1 |
| Source | [`pbakaus/impeccable`](https://github.com/pbakaus/impeccable) `@831cabee8b4bc1a2b66e5ae22003e9a19b57d464` |
| Installed via | `claude plugin marketplace add pbakaus/impeccable` → `claude plugin install impeccable@impeccable`, into an isolated `CLAUDE_CONFIG_DIR`; the resulting plugin cache is vendored verbatim to `skills/impeccable/` |
| Skill content hash | `sha256:c3185df7833a43644cc5756c802358f9345d41e353fb6166381026b6c5ca8cfd` |
| Host | `claude-code` 2.1.263, Windows 11 Pro 10.0.26200 |
| Model | `claude-haiku-4-5-20251001` |
| System prompt hash | `not-provided-by-host` (Assay records `environmentHash` `sha256:1491f2d9…` instead — model, version, tool set, skill set, plugin set, **and now the permission mode**; not a system prompt hash) |
| Suite | `suites/impeccable.suite.yaml` v1, `sha256:c820aafc…` |
| Run | `run-2026-09-06T09-53-14-345Z-c3d2b624` · 120 attempts · 964 tool calls · 8,031/387,996 tokens · $8.11 · 90.9 min |
| Runner | `@ktlsr/assay@0.2.0`, `--permission-mode acceptEdits` |

---

## Headline

**Precision 100% (N=28, 95% CI 88%–100%). Recall 56% (N=50, 95% CI 42%–69%).
Zero false positives in 70 negative attempts. Zero unreadable trigger signals in
120.**

Three things sit behind those numbers, and each is worth more than the number:

1. **The activation defect is fixed.** 28 confirmed activations, 0 refusals.
   Under 4.2.0 the same instrument recorded 4 activations and 0 of them ran.
2. **The skill loads and then cannot use itself.** All **55** launcher
   invocations across the run were refused by the host permission layer, and of
   35 documented reference files, **one** was reached for and the host refused
   that read too. The body loads; nothing behind it does.
3. **The skill's own hook runs anyway**, outside the permission layer, and
   downloaded a binary during a run in which every model-initiated launcher call
   was denied.

---

## Suite A — routing

12 cases × 10 attempts. No prompt contains the skill's name, the word *design*,
or any of the 23 sub-command names.

The near neighbours are the point of this set. The skill's description is the
broadest of the four measured in this repository — it claims essentially every
verb that can be applied to a frontend interface, plus accessibility,
performance, responsive behaviour, i18n, UX copy and design systems — which
leaves a narrow strip where a genuine near neighbour can stand. One of the four
frontend-with-no-visual-decision cases targets the *same file* a positive case
targets - `src/routes/landing.tsx`, once for a visual direction and once for an
analytics event - so between those two the only difference is whether a visual
decision is asked for. Requests the description does claim (accessibility, UI performance,
responsive behaviour) are deliberately not used as negatives: firing on those is
the skill doing its job, and scoring them as false positives would be unfair.

### Per case

| Case | Kind | Expected | Fired | Pass rate | Verdict |
| --- | --- | --- | --- | --- | --- |
| `trigger.positive.hero_direction` | positive | fire | 10/10 | 100% (N=10, 95% CI 72%–100%) | pass |
| `trigger.positive.forgettable_usage` | positive | fire | 10/10 | 100% (N=10, 95% CI 72%–100%) | pass |
| `trigger.positive.settings_rework` | positive | fire | 6/10 | 60% (N=10, 95% CI 31%–83%) | FAIL |
| `trigger.positive.empty_state` | positive | fire | 2/10 | 20% (N=10, 95% CI 6%–51%) | FAIL |
| `trigger.negative.near_neighbor.undefined_email` | near neighbour | stay quiet | 0/10 | 100% (N=10, 95% CI 72%–100%) | pass |
| `trigger.negative.near_neighbor.cta_instrumentation` | near neighbour | stay quiet | 0/10 | 100% (N=10, 95% CI 72%–100%) | pass |
| `trigger.negative.near_neighbor.token_substitution` | near neighbour | stay quiet | 0/10 | 100% (N=10, 95% CI 72%–100%) | pass |
| `trigger.negative.near_neighbor.double_submit` | near neighbour | stay quiet | 0/10 | 100% (N=10, 95% CI 72%–100%) | pass |
| `trigger.negative.near_neighbor.wordmark` | near neighbour | stay quiet | 0/10 | 100% (N=10, 95% CI 72%–100%) | pass |
| `trigger.negative.near_neighbor.print_booklet` | near neighbour | stay quiet | 0/10 | 100% (N=10, 95% CI 72%–100%) | pass |
| `trigger.negative.unrelated.slow_query` | unrelated | stay quiet | 0/10 | 100% (N=10, 95% CI 72%–100%) | pass |
| `complete.persists_design_system` | completion | fire | 0/10 | 0% (N=10, 95% CI 0%–28%) | FAIL |

### Trigger accuracy

| | Fired | Stayed quiet |
| --- | --- | --- |
| **Should fire** | 28 (TP) | 22 (FN) |
| **Should stay quiet** | 0 (FP) | 70 (TN) |

| Metric | Value |
| --- | --- |
| precision | 100% (N=28, 95% CI 88%–100%) |
| recall | 56% (N=50, 95% CI 42%–69%) |
| F1 | 0.72 |
| unreadable trigger signals | 0 |

### Where the recall goes

Every miss has the same shape. The model reads the target file and edits it
directly, without reaching for the skill. All four `settings_rework` misses are
exactly this and nothing else:

```
#2  "I'll review the settings file for UX issues."     tools: Read, Edit
#6  "I'll examine the settings file to identify the
     hierarchy, grouping, and button placement issues." tools: Read, Edit
```

The eight `empty_state` misses have the same opening — `Read`, then `Edit` — and
in five of them a `Skill` call does appear afterwards, but it is `run`, reached
for to launch the app and look at what had already been built.

This is the same failure mode `ui-ux-pro-max` showed at 50% recall: the request
is answerable without the skill, so it is answered without the skill. Nothing is
refused and nothing errors — the work simply happens one layer down.

The two positives that never missed are the two that ask for a *replacement*
visual world (`hero_direction`, `forgettable_usage`). The two that miss are the
two that ask for a *judgement inside an existing screen* — where hierarchy falls
down, what a first-time visitor should see. The narrower and more diagnostic the
design question, the less likely the skill is reached for.

### The completion case is the sharpest result in the suite

`complete.persists_design_system` asks for the visual system to be worked out
and written down at the project root, in the file a later session would look
for. That is exactly what the skill's `document` command promises.

**0/10 activations. 10/10 wrote `DESIGN.md`.**

No `Skill` call appears in any of the ten attempts. The base model produced the
artefact the skill exists to produce, at the path the skill documents, without
the skill. `reference/document.md` — 27,844 bytes specifying the DESIGN.md
format, its token schema and its eight-section order — was never opened, so what
those ten files contain is the model's idea of a design system, not the skill's.

An assertion on the artefact alone would have scored this case 10/10. It is the
case for pairing `file_exists` with a trigger expectation.

### What else fired

One skill active per run, but Claude Code's own bundled skills stay available
and competed:

| Skill | Attempts it fired in | Where |
| --- | --- | --- |
| `impeccable:impeccable` | 28 | the four positives |
| `run` | 24 | after an edit, to launch the app — 7 of them on `empty_state` |
| `dataviz` | 6 | `print_booklet`, 6 of 10 attempts |

`dataviz` taking six of the ten print-booklet attempts is the negative working
as designed: a request to choose chart types for a printed page is a visual
decision that is not a frontend interface, impeccable stayed quiet on all ten,
and a bundled skill scoped to charts took it instead.

`run` is noisier. It fired in 24 attempts, always after impeccable had already
edited a file, and it accounts for most of the shell traffic in the run —
including `npm install` and `npm run dev` calls that the permission layer then
refused.

---

## Suite C — resource usage

Full output: [`reports/impeccable.coverage.md`](impeccable.coverage.md), from
`tools/refcoverage.py --exec impeccable`.

### Reference files

The skill ships **35** documented reference files under `reference/`, plus four
sub-agent fallbacks under `reference/degraded/`. `SKILL.md` routes to them by
relative markdown link, which the model resolves with a `Read`.

| | Files | Bytes |
| --- | --- | --- |
| ships in the skill directory | 58 | 2,150,761 |
| loaded by the host on trigger (`SKILL.md`) | 1 | 11,374 |
| opened by the agent | **0** | **0** |
| not observable (behind the compiled engine) | 2 | 1,102,570 |
| **never opened** | **55** | **1,036,817** |

**Across 28 confirmed activations, exactly one reference file was reached for,
and the host refused the read.**

```
trigger.positive.empty_state #7
  Read  …\assay-skill-sboeLx\skills\impeccable\reference\onboard.md
  ERR   Claude requested permissions to read from …\reference\onboard.md,
        but you haven't granted it yet.
```

Two separate things are visible here and they should not be merged.

- **The model does not reach for them.** 27 of 28 activations never named a
  reference file at all. `SKILL.md` step 3 says to load
  `reference/craft-floor.md` immediately before editing UI; every one of the 28
  activations edited UI, and none of them loaded it.
- **When it does reach, the host refuses.** The skill's own directory sits
  outside the attempt workspace, so reading it needs a permission
  `acceptEdits` does not grant. In the same run, the bundled `dataviz` skill's
  three reference reads succeeded — bundled skills live in a path the host
  already trusts. *Caveat:* Assay stages the skill under test in a temp
  directory, so this refusal is a property of that staging as much as of the
  skill; a plugin installed normally may sit in a path the host treats
  differently. It is one read out of 28 activations either way.

The two are not independent, and the report cannot separate them: steps 2 and 3
of Setup follow step 1, and step 1 was refused 55 times out of 55. Whether the
model would load the playbook and the craft floor in a session where `impeccable
context` succeeds is exactly the question a run with the launcher pre-approved
would answer, and that run has not been made.

Largest never-opened files: `reference/new-work.md` (52,849 B),
`reference/critique.md` (43,488 B), `reference/live.md` (36,145 B),
`reference/document.md` (27,844 B). 352,712 bytes of documented reference
material shipped, none of it read.

### The launcher

`SKILL.md` Setup step 1 is not a judgement call — it instructs a shell-out
before anything else. The model followed it.

| Verb | Attempted | Refused | Ran |
| --- | --- | --- | --- |
| `context` | 55 | 55 | 0 |
| (no verb) | 1 | 1 | 0 |

The `(no verb)` row is a `Get-ChildItem` listing of the scripts directory, not a
launcher call — the coverage tool counts any shell command naming the launcher.

**55 invocations, 55 refusals, 0 executions.** Two shapes of refusal, both from
the host's command parser rather than a policy decision about the binary:

```
Bash       "…\skills\impeccable\scripts\impeccable.cmd" context
           → "This command requires approval"

PowerShell & "…\skills\impeccable\scripts\impeccable.cmd" context
           → "This PowerShell command contains multiple operations.
              The following part requires approval: & "…impeccable.cmd" context"
```

The `&` call operator — the correct way to invoke a quoted path in PowerShell —
is read by the parser as a compound command.

Two further observations on the invocation itself:

- **8 of the 55 resolved the base directory wrongly**, producing
  `<plugin-root>/scripts/impeccable.cmd` instead of
  `<plugin-root>/skills/impeccable/scripts/impeccable.cmd`. The host reports the
  plugin root as "Base directory for this skill"; the launcher lives two levels
  below it. `<skill-base-dir>` in `SKILL.md` is ambiguous about which one it
  means.
- **The launcher itself works on this host.** Run by hand outside the sandbox
  against the same fixture, `impeccable.cmd context --target src/routes/landing.tsx`
  returns its full directive set — `NO_PRODUCT_MD`, `RESOLVED_CONTEXT`,
  `MANUAL_DETECTOR_REQUIRED` and the rest — in about a second. Nothing is broken
  in the skill's own tooling. The blocker is entirely the permission layer.

`--permission-mode dontAsk` was tried as an alternative and is worse: it refuses
`Bash`, `PowerShell` **and** `Edit`, so the launcher is refused 4/4 and no file
can be written either. `bypassPermissions` is the only mode that would let these
calls through; it was not run, so **no configuration in which the launcher
executes has been measured here.**

### The hook runs outside all of this

`hooks/hooks.json` registers `PostToolUse` on `Edit|Write` and `Stop`, both
invoking `scripts/impeccable hook`. The pilot established that the hook fires and
that Assay cannot see it. Two things are new, and the first corrects the pilot.

**The hook's output does reach the model.** The pilot answered *no* to this, on
the strength of a probe where the hook demonstrably fired and no marker text
appeared anywhere. That answer was wrong, or at least too strong. In
`forgettable_usage` attempt 4 the model said, unprompted:

> I found a performance issue detected by the design hook. The progress bar is
> animating `width`, which causes layout thrash. I'll fix it to use
> `transform: scaleX()` instead, which is GPU-accelerated

The progress bar was the model's own, written moments earlier, and the message
lands immediately after it had already summed up and declared the work finished
— the `Stop` hook, doing exactly what it is for. Two more `Edit` calls follow and
the animation is changed to `transform: scaleX()`. So the hook's
`additionalContext` reached the model and changed what the run produced. It
appears nowhere as a trace event: Assay 0.2.0 now parses
`system/hook_started` and `system/hook_response`, and **0 hook events appeared in
120 attempts** — consistent with the pilot's finding that the host emits those
only for `SessionStart`. The only reason this one instance is visible is that the
model quoted it. So the honest statement is narrower than either the pilot's or
its opposite: the hook's output reaches the model at least sometimes, and the
transcript cannot tell you when.

**The hook executes the launcher the permission layer is refusing.** Controlled
test: the cached engine at `~/.impeccable/bin/0.1.2/` was moved aside, a 4-attempt
run was executed, and afterwards:

| | |
| --- | --- |
| launcher calls by the model | 4 attempted, 4 refused, 0 ran |
| `~/.impeccable/bin/0.1.2/impeccable.exe` | **re-downloaded and cached during the run** |

Hooks run as harness subprocesses, not through the tool permission layer. So the
skill's engine binary was fetched over the network and cached in the user's home
directory in a session where every model-initiated call to that same binary was
denied. The cache was restored afterwards; this is the mechanism that also
explains why the pilot found itself on a primed host.

**Note on priming:** this host has `~/.impeccable/bin/0.1.0` and `0.1.2` present.
The measurement therefore ran against a primed host. It made no difference to any
number above, because the launcher never executed — but a cold host would have
had the hook perform that download on the first edit instead.

---

## Suite B — behaviour

**Not measured. Skipped by the decision rule, not by omission.**

Suite B asks what the skill does once it runs: whether it produces the artefacts
it documents, follows its own quality floor, spawns its sub-agents. Every one of
those is reachable only through the launcher and the reference files, and in this
configuration:

- 55 of 55 launcher calls refused
- 0 of 35 reference files read
- 0 of 4 sub-agents spawned

There is no behaviour downstream of the activation to observe. What the 28
activated attempts produced is the base model plus an 11 KB `SKILL.md`, which is
a real thing to measure but is not Suite B.

This is a narrower failure than the pilot's. The pilot could not measure Suite B
because the skill never loaded. It now loads; what it cannot do is act.

---

## What changed since the pilot

| | Pilot (4.2.0, assay 0.1.3) | This run (4.2.1, assay 0.2.0) |
| --- | --- | --- |
| `allowed-tools` in frontmatter | yes | **removed** |
| `Skill` tool result | `is_error: true`, permission prompt title | no error, body injected |
| Activations | 4 recorded, **0 real** | 28 recorded, **28 real** |
| Trigger signal | inferred from the call | verified against the paired result |
| Refused activations | counted as `triggered: true` | counted as `unknown` (0 occurred) |
| Launcher calls | 0 attempted (body never loaded) | 55 attempted, 55 refused |
| Reference files read | 0 (nothing to name them) | 0 (1 attempted, refused) |
| Suite A | not meaningful | **measured** |
| Suite B / C | not runnable | C measured; B still not runnable |

Both defects the pilot reported upstream are addressed by 4.2.1: `allowed-tools`
is gone, and with it both the activation block and the mismatch between the
allowlist pattern and the instructed command. The runner defect the pilot
reported is addressed by assay 0.2.0, which is why the `unknown` column above
reads 0 rather than being absent.

---

## Limitations

- **One round, not two.** The three earlier measurements in this repository ran a
  second, tighter negative set after a clean first round, because an unbroken
  negative set bounds the false-positive rate without showing where the set's
  discriminating power ends. This set was written tight from the start — four
  frontend-no-visual-decision neighbours, one of them in a file a positive case
  also targets — but it is still one round, and 0/70 with a lower bound of 95%
  is not the same as a boundary that has been found.
- **The suite file's header comment overstates one thing.** It says two of the
  four near neighbours share a file with a positive; only one does
  (`src/routes/landing.tsx`). The file is left byte-identical to what was
  measured, because its content hash is the case-set pin — correcting the
  comment would break the pin for a comment.
- **Rates are pinned to `claude-haiku-4-5-20251001`.** Trigger routing is model
  behaviour; 56% recall is a floor for this model, not a universal result.
- **Isolation is from the user's skills, not the host's.** `run` and `dataviz`
  are bundled with Claude Code and competed on 30 of 120 attempts.
- **The permission mode is part of the measurement.** Everything here is
  `acceptEdits`. A run with the skill's shell access pre-granted would be a
  different measurement, and Suite C's launcher numbers would not carry over.
- **The skill under test is staged in a temp directory** by the runner. The
  refused reference read is at least partly a property of that staging.
- **The host is primed** with the impeccable engine binary already cached.

---

## Reproduce

```
npx @ktlsr/assay@0.2.0 validate suites/impeccable.suite.yaml
npx @ktlsr/assay@0.2.0 run suites/impeccable.suite.yaml \
  --skill ./skills/impeccable --html reports/impeccable.html
node   tools/observability.mjs .assay/runs/<run-id>.json
python tools/refcoverage.py --exec impeccable ./skills/impeccable \
  .assay/runs/<run-id>.json > reports/impeccable.coverage.md
```

Needs Node 22, Python 3 and `CLAUDE_CODE_OAUTH_TOKEN` or `ANTHROPIC_API_KEY`.
120 attempts, $8.11 at the pinned model; the smoke test, the `dontAsk` probe and
the hook control add $0.84.

The hook control is: move `~/.impeccable/bin/<version>` aside, run any suite that
edits a file, and check whether the directory comes back.

Run records land in `.assay/runs/` and are gitignored.

Method: <https://assayctl.dev/methodology>
