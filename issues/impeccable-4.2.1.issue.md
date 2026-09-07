---
title: "[Bug] Follow-up to #736: 4.2.1 activates, but nothing behind the activation runs — 0 of 35 reference files read, 55 of 55 launcher calls refused"
labels: bug
---

## What happened?

First, thank you — #738 fixes #736 completely. In 4.2.1 the skill activated in
**28 of 28** attempts where the model reached for it, with zero refusals, so I
was able to run the full trigger-discrimination measurement that #736 blocked.

The headline is good news and I want to lead with it: **precision 100% (N=28,
95% CI 88%–100%), zero false positives in 70 negative attempts.** Seven negative
cases — four of them frontend work with no visual decision in it, one of those
in the same file a positive case targets; two of them a real visual decision
that is not an interface — and the boundary your description declares held on
every single one.

This issue is about what the measurement found *downstream* of activation. Two
findings are much stronger than the rest, so they go first.

### 1. The completion case: 0/10 activations, 10/10 `DESIGN.md` written

One case asks, in the skill's own terms but without naming any sub-command or
using the word "design":

> Work out the visual system this codebase is already using — type scale,
> colour, spacing, component patterns — and write it down at the project root,
> in the file a later session would look for, so a new contributor can pick it
> up without asking.

That is what `document` promises. Across ten attempts:

| | |
| --- | --- |
| activations | **0 / 10** |
| `DESIGN.md` written at project root | **10 / 10** |

No `Skill` call appears in any of the ten. The base model produced the artefact
the skill exists to produce, at the path the skill documents, and
`reference/document.md` — 27,844 bytes specifying the DESIGN.md format, its
token schema and its fixed eight-section order — was never opened. So the ten
files that got written are the model's idea of a design system, not yours.

From a user's side this looks like a success. From an author's side the format
spec never ran.

### 2. The 35 reference files are not being read

| | Files | Bytes |
| --- | --- | --- |
| ships under `reference/` | 35 | 352,712 |
| opened across 28 activations | **0** | **0** |

**One** reference file was reached for in 28 activations — `onboard.md`, once —
and the host refused that read because the plugin directory sits outside the
session workspace. The other 27 activations never named a reference file at all.

The specific consequence I would look at first: `SKILL.md` step 3 says to load
`reference/craft-floor.md` **immediately before editing UI**, and calls it the
quality floor and the absolute bans. All 28 activations edited UI. None loaded
it.

I do not think these two findings are independent of finding 3 below, and the
measurement cannot separate them — see *Expected behavior*.

### The other three, in brief

3. **Setup step 1 cannot execute in a non-interactive host.** 55 launcher
   invocations, 55 refused, 0 executed.
4. **`<skill-base-dir>` is ambiguous**, and 8 of those 55 resolved it to the
   plugin root rather than the skill directory, producing a path that does not
   exist.
5. **The hook runs outside the permission layer** and downloaded the engine
   binary during a session where every model-initiated call to that binary was
   denied. Relatedly, and this corrects my pilot report: the hook's output *does*
   reach the model.

## Steps to reproduce

1. `claude plugin marketplace add pbakaus/impeccable`, then
   `claude plugin install impeccable@impeccable` (4.2.1).

2. **Finding 1.** In a project with a small React frontend and no `DESIGN.md`,
   run a non-interactive session against the installed plugin:

   ```
   echo "Work out the visual system this codebase is already using - type \
   scale, colour, spacing, component patterns - and write it down at the \
   project root, in the file a later session would look for." | \
   claude -p --output-format stream-json --verbose \
     --model claude-haiku-4-5-20251001 \
     --permission-mode acceptEdits \
     --plugin-dir <plugin root>
   ```

   `DESIGN.md` appears at the project root. No `Skill` tool call appears
   anywhere in the stream. Ten out of ten, in my run.

3. **Finding 2.** Run any prompt that *does* activate the skill — a bland
   landing page and "give it a real visual direction and build it" works every
   time — and grep the stream for `reference/`. There will be no `Read` of one.
   Then confirm the model went on to edit UI, which is what step 3 of Setup
   gates on.

4. **Findings 3 and 4.** In the same activated run, find the `Bash` and
   `PowerShell` calls that follow the skill body. They are Setup step 1, and
   their paired `tool_result` carries an error; the `result` event's
   `permission_denials` array names them.

5. **Finding 5.** Move `~/.impeccable/bin/<version>/` aside, run any session
   that edits a file, and check whether the directory comes back. It does, even
   though every launcher call in the session was refused.

## Expected behavior

**1 and 2.** When the skill is loaded, its own reference material should reach
the model before the work happens — most sharply `craft-floor.md` before a UI
edit, and `document.md` before something writes a `DESIGN.md`. Today the model
loads `SKILL.md`, finds Setup step 1 refused, and proceeds on `SKILL.md` alone,
which is a strong enough prompt to produce plausible output.

I was careful here originally, because the first measurement could not separate
two explanations: steps 2 and 3 of Setup follow step 1, and step 1 was refused 55
times out of 55. **I have since made the run that separates them** — see *What
the launcher-approved run settled* below. Short version: finding 2 is
substantially caused by finding 3 and should be read as downgraded, finding 1 is
not caused by it at all.

**3.** Setup step 1 should either be executable without consent in a
non-interactive session, or `SKILL.md` should carry a documented degraded path:
what to load, what to assume, and what to tell the user, when the launcher
cannot run. Right now a refusal produces a silent improvisation rather than a
stated one. Note this is the same class of problem #736 was, one level down:
4.2.0 could not activate without consent; 4.2.1 activates but cannot perform the
first thing it instructs without consent.

**4.** `<skill-base-dir>` should be unambiguous — the host reports the plugin
root as "Base directory for this skill", and the launcher lives two levels below
it at `<plugin-root>/skills/impeccable/scripts/`. Spelling that out would remove
a path error that would bite in any session where the command *is* permitted.

**5.** No expectation to change, just to state: it would be worth documenting
that the hook fetches and caches a ~14 MB binary in `$HOME` on first edit,
including in sessions where the user's permission layer has denied every call to
that binary. The download is verified against its `.sha256` sidecar and the
4.2.1 launcher hardening around that is careful work — this is about
expectations, not integrity.

## Provider & environment

- **Provider** (Cursor / Claude Code / Gemini CLI / Codex / Copilot / Kiro / OpenCode): **Claude Code**
- **Provider version**: 2.1.263
- **OS**: Windows 11 Pro 10.0.26200

Plugin: `impeccable` 4.2.1,
`pbakaus/impeccable@831cabee8b4bc1a2b66e5ae22003e9a19b57d464`, skill content
`sha256:c3185df7…`. Model pinned to `claude-haiku-4-5-20251001`,
`--permission-mode acceptEdits`, runner `@ktlsr/assay@0.2.0`. Installed via the
documented marketplace path into an isolated `CLAUDE_CONFIG_DIR`; the resulting
plugin cache is what was measured, unmodified.

12 cases × 10 attempts = 120, against a small React fixture. **No prompt
contains the skill's name, the word "design", or any of the 23 sub-command
names.**

Host engine cache note: `~/.impeccable/bin/` already held the engine on this
machine, so the measurement ran against a primed host. It made no difference to
any number here, because the launcher never executed.

## Additional context

### Reference-file coverage in full

| | Files | Bytes |
| --- | --- | --- |
| ships in the plugin directory | 58 | 2,150,761 |
| loaded by the host on trigger (`SKILL.md`) | 1 | 11,374 |
| opened by the agent | **0** | **0** |
| not observable (behind the compiled engine) | 2 | 1,102,570 |
| **never opened** | **55** | **1,036,817** |

The one read that was attempted:

```
Read  …\skills\impeccable\reference\onboard.md
ERR   Claude requested permissions to read from …\reference\onboard.md,
      but you haven't granted it yet.
```

Largest never-opened: `new-work.md` (52,849 B), `critique.md` (43,488 B),
`live.md` (36,145 B), `document.md` (27,844 B).

One caveat I should give you, because it cuts against my own finding: the runner
stages the skill under test in a temp directory, so that refusal is partly a
property of the staging, and a normally-installed plugin may sit in a path the
host treats differently. In the same run the bundled `dataviz` skill's three
reference reads succeeded. But it is one attempted read out of 28 activations
either way, and the staging cannot explain the 27 that never reached at all.

### The launcher, finding 3 in detail

| Verb | Attempted | Refused | Ran |
| --- | --- | --- | --- |
| `context` | 55 | 55 | 0 |

Two shapes of refusal, both from the host's command parser rather than a policy
decision about the binary:

```
Bash        "…\skills\impeccable\scripts\impeccable.cmd" context
            → "This command requires approval"

PowerShell  & "…\skills\impeccable\scripts\impeccable.cmd" context
            → "This PowerShell command contains multiple operations. The
               following part requires approval: & "…impeccable.cmd" context"
```

Worth noting for whatever shape a fix takes: the PowerShell call operator `&` is
the correct way to invoke a quoted path, and it is exactly the form the parser
rejects as compound.

**Your launcher itself is fine.** Run by hand outside the sandbox against the
same fixture, `impeccable.cmd context --target src/routes/landing.tsx` returns
its full directive set — `NO_PRODUCT_MD`, `BUILD_INIT_REQUIRED`,
`RESOLVED_CONTEXT`, `MANUAL_DETECTOR_REQUIRED` and the rest — in about a second.
The blocker is entirely the permission layer.

I also tried `--permission-mode dontAsk` as an alternative and it is worse: it
refuses `Bash`, `PowerShell` **and** `Edit`, so nothing can be written either.
`bypassPermissions` is the only mode that lets these calls through.

**Update:** I have since made that run — same suite, same case-set hash, only the
permission mode changed. **0 of 57 launcher calls refused, 42 executed.** Two
things it changes in this issue, both stated in full at the end under *What the
launcher-approved run settled*: finding 1 is unaffected, and finding 2 is
substantially caused by this one and should be read as downgraded.

### The base-directory ambiguity, finding 4

```
…\<plugin-root>\scripts\impeccable.cmd context                        ← 8 of 55, does not exist
…\<plugin-root>\skills\impeccable\scripts\impeccable.cmd context      ← 47 of 55, correct
```

Both were refused here, so it cost nothing in this run. In a session where the
command is permitted, roughly one in seven attempts would run a path that is not
there.

### The hook, finding 5

`hooks/hooks.json` runs `scripts/impeccable hook` on `PostToolUse(Edit|Write)`
and `Stop`. Hooks run as harness subprocesses, not through the tool permission
layer. Controlled test — I moved `~/.impeccable/bin/0.1.2/` aside, ran a
four-attempt session, and afterwards:

| | |
| --- | --- |
| launcher calls by the model | 4 attempted, 4 refused, 0 ran |
| `~/.impeccable/bin/0.1.2/impeccable.exe` | **re-downloaded and cached during the run** |

And a correction to my own pilot report, which said the hook's output does not
reach the model. It does. In one attempt the model had already finished and
summed up its work, then said:

> I found a performance issue detected by the design hook. The progress bar is
> animating `width`, which causes layout thrash. I'll fix it to use
> `transform: scaleX()` instead, which is GPU-accelerated

— and made two more edits to switch it. That is the `Stop` hook doing exactly
what it is for. The only reason I can see it is that the model quoted it: the
host emits no `PostToolUse` hook event into `--output-format stream-json`, so a
transcript cannot distinguish a run where the hook fired from one where it did
not.

### Where recall goes

Precision is perfect, so this is the only place routing costs anything. Recall
was 56% (N=50, 95% CI 42%–69%) and it is not evenly distributed:

| Request | Fired |
| --- | --- |
| "reads like a wireframe — give it a real visual direction and build it" | 10/10 |
| "competent and completely forgettable — make it something they'd remember" | 10/10 |
| "where does this fall down on hierarchy and grouping, then rework it" | 6/10 |
| "a new workspace shows three zeroes and an empty table — what should they see" | 2/10 |
| "work out the visual system this codebase uses and write it down" | **0/10** |

The two that never miss ask for a *replacement* visual world. The two that miss
ask for a *judgement inside an existing screen*. Your description covers both —
"onboarding, and empty states" and "reusable design systems or tokens" are both
in it — but on this model the narrower, more diagnostic phrasing does not pull
the skill.

Every miss looks identical in the trace: `Read`, then `Edit`, no `Skill` call.
Nothing is refused and nothing errors; the work simply happens one layer down.

For what it is worth on the other side of the ledger, the negatives were built
to be hard and every one held. `src/routes/landing.tsx` appears twice in the
case set — once asking for a visual direction (10/10 fired) and once asking for
an `IntersectionObserver` analytics event with "nothing on screen changes"
(0/10 fired). A mechanical token substitution and a double-submit guard also
stayed quiet 10/10 each. And on a print-booklet brief the skill stayed quiet all
ten times while Claude Code's bundled `dataviz` took six of them, which is
exactly the boundary your last line declares.

### Caveats

Everything is pinned to `claude-haiku-4-5-20251001` and Claude Code 2.1.263;
trigger routing is model behaviour, so 56% is a floor for this model rather than
a universal result. The permission mode (`acceptEdits`) is part of the
measurement — a run with your launcher pre-approved produces different numbers
for findings 2 and 3, and the same numbers for finding 1; both runs are reported.
The Windows specifics
— the `&` operator and the `.cmd` launcher — do not apply on other platforms;
findings 1, 2, 4 and 5 do. This is one round of negatives, not two: 0 false
positives in 70 attempts bounds the false-positive rate at a 95% lower bound of
95%, but it does not show where the case set's discriminating power ends.

### Reproduce

```
npx @ktlsr/assay@0.2.0 run suites/impeccable.suite.yaml --skill ./skills/impeccable
node   tools/observability.mjs .assay/runs/<run>.json
python tools/refcoverage.py --exec impeccable ./skills/impeccable .assay/runs/<run>.json
```

Case set, fixture, coverage output and the full report:
<https://github.com/ktlesr/skill-trigger-measurements>
Run records stay local (`.assay/runs/`, not committed); happy to attach the JSON.

Method: <https://assayctl.dev/methodology>

## Willing to work on a fix?

Findings 4 and 5 I would happily open a PR for — the `<skill-base-dir>` wording
in `SKILL.md`, and a line in the docs about the hook's first-run download. Both
are small and neither needs a judgement about the skill's design.

Findings 1, 2 and 3 I would rather not guess at. Whether Setup step 1 should
degrade, and how hard the reference-loading steps should be worded so they
survive a refused step 1, are decisions about your instruction design, and the
right shape depends on context I do not have from outside the project.

What I can offer is the measurement. The case set is written and pinned, so I can
re-run all 120 attempts against a candidate fix and report the same numbers back
before it ships — in both permission modes, since they now have a baseline each.

---

## What the launcher-approved run settled

Same suite, same case-set hash, same skill hash, same model. Only
`--permission-mode` changed, from `acceptEdits` to `bypassPermissions`. 120
attempts each.

| | launcher refused | launcher ran |
| --- | --- | --- |
| `acceptEdits` | 55 / 55 | 0 |
| `bypassPermissions` | **0 / 57** | **42** |

**Finding 1 stands, unchanged, and is not a consequence of finding 3.** The
completion case fired **0/10 in both modes** and wrote `DESIGN.md` anyway 10/10
and 9/10. `document.md` was never opened in either. The skill is not reached, so
whether its launcher works is beside the point.

**Finding 2 is downgraded.** With the launcher working, reference reads go from
0 to 29, across 7 of the 35 files — `new-work.md` (12), `craft-floor.md` (6),
`init.md` (3), `layout.md` (3), `bolder.md` (2), `onboard.md` (2), `operate.md`
(1). The routing works when it runs; `layout.md` and `operate.md` for a settings
rework, `onboard.md` for an empty state, each the reference your command table
names. My "none of them are read" framing does not survive that, and I would
retract it. What survives is narrower: 28 of 35 files still never opened, and
`craft-floor.md` loaded before only **6 of the 29** UI-editing activations,
against a `SKILL.md` step that says to load it immediately before editing UI.

**Finding 4 gets worse, not better.** I wrote that the 8 mis-resolved
`<skill-base-dir>` paths "cost nothing in this run" because everything was
refused anyway. With the calls permitted, they cost exactly what you would
expect. Of the 57 launcher calls:

| Outcome | Count |
| --- | --- |
| ran | 42 |
| failed — path does not exist (`<plugin-root>/scripts/…`) | **9** |
| failed — `ParserError: Unexpected token 'context'` (quoted `.cmd` without `&`) | **6** |
| refused by the permission layer | 0 |

**26% of launcher calls fail for reasons that belong to the skill, not the
host** — and that number was invisible while the permission layer refused
everything.

Routing did not move: precision 100% in both modes (N=28 and N=30), 0 false
positives in 70 negative attempts each, and no per-case difference clears its
confidence interval.

One operational note, in case you ever measure this way yourselves: a
`bypassPermissions` run of this skill destroys its own runner. The agent starts
dev servers to verify its work and then kills processes *by port*; the servers
outlive the attempt and pile up on Vite's port ladder (I caught 13 orphans
holding 5173–5178), and the test runner is a `node` process in the same space.
Two attempts at a single 120-attempt run died at exit 255 with no output. The run
had to be split into five records of 24 with the orphans cleared between them.
