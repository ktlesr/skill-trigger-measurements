# `impeccable` — pilot: what Assay can and cannot observe

**This is a feasibility report, not a finding report.** It asks whether Assay
can see this skill at all, and answers no for most of it. The trigger numbers
below are printed for completeness and should not be quoted: they were produced
in a sandbox where the skill under test never actually ran.

| | |
| --- | --- |
| Skill | `impeccable` 4.2.0 |
| Source | [`pbakaus/impeccable`](https://github.com/pbakaus/impeccable) `@8dac6ae7e020c43ab10ce9b41939f6fd42627b96` |
| Installed via | `claude plugin marketplace add pbakaus/impeccable` → `claude plugin install impeccable@impeccable`, into an isolated `CLAUDE_CONFIG_DIR`; the resulting plugin cache is vendored verbatim to `skills/impeccable/` |
| Skill content hash | `sha256:cd74d14bb2ff290f07cc8eb5932eb816ef854a081940ce984c22f8e64b1284d8` |
| Host | `claude-code` 2.1.261, Windows 11 Pro 10.0.26200 |
| Model | `claude-haiku-4-5-20251001` |
| System prompt hash | `not-provided-by-host` (Assay records `environmentHash` `sha256:d7d8ece8…` instead — model, version, tool set, skill set, plugin set; **not** a system prompt hash) |
| Suite | `suites/impeccable.pilot.suite.yaml` v1, `sha256:355de968…` |
| Run | `run-2026-09-05T08-18-31-328Z-fd96eaae` · 12 attempts · 45 tool calls · 474/24784 tokens · $0.5445 · 5m37s |
| Runner | `@ktlsr/assay@0.1.3`, `--permission-mode acceptEdits` (not overridable from the CLI in 0.1.3) |

---

## The headline

**The skill never executed. Not once, in any of the 12 attempts.**

Every `Skill(impeccable:impeccable)` call in the run came back with
`is_error: true` and the body `"Execute skill: impeccable:impeccable"`. That
string is not an error message — it is the *title of a permission prompt*.
Under `claude -p` there is nobody to answer it, so the activation is denied and
the model carries on from general knowledge. Assay recorded those calls as
`triggered: true`.

The cause is isolated, and it is in the skill's own frontmatter:

```yaml
allowed-tools:
  - Bash(npx impeccable *)
```

A skill that declares `allowed-tools` is asking for tool permissions it does
not otherwise have, so activating it needs consent. I ran the control: same
plugin, same prompt, same flags, with those two lines deleted from `SKILL.md`
and nothing else changed.

| | Skill tool result | `permission_denials` | Skill body loaded |
| --- | --- | --- | --- |
| 4.2.0 as published | `is_error: true` · `"Execute skill: impeccable:impeccable"` | 1 entry | no |
| identical, `allowed-tools` removed | `is_error: undefined` · `"Launching skill: impeccable:impeccable"` | empty | yes — `Base directory for this skill: …` followed by the full text |

So the pilot's 12 attempts measured the base model doing design work while a
denied skill request sat in the transcript. Everything downstream of that —
reference files, the CLI, the sub-agents, the design system artefacts — was
never reachable.

### Does this invalidate the three earlier measurements?

**No. Checked, not assumed.**

Every stored run record was rescanned for `Skill` tool calls whose paired
`tool_result` carried `is_error: true`:

| Skill | Runs | `Skill` calls | `is_error: true` | Body injected after |
| --- | --- | --- | --- | --- |
| `animate` | 2 full + 2 smoke | 75 | **0** | 75 / 75 |
| `better-typography` | 2 full | 69 | **0** | 69 / 69 |
| `ui-ux-pro-max` | 2 full + 2 smoke | 90 | **0** | 86 / 86 (full runs) |
| `impeccable` | 1 pilot | 6 | **4** | 0 / 4 |

The middle column alone would only show an absence. The right-hand column is
the positive check: after each of those 230 calls in the six reported runs, the
host injected the skill body into the transcript — `Base directory for this
skill: …` followed by the frontmatter. Those skills did not merely fail to
error; they demonstrably loaded and ran, every time.

The mechanism agrees. `allowed-tools` is what turns activation into a
permission prompt, and of the four vendored skills only `impeccable` declares
it:

```
skills/animate/SKILL.md                                    allowed-tools: no
skills/better-typography/SKILL.md                          allowed-tools: no
skills/ui-ux-pro-max/.claude/skills/ui-ux-pro-max/SKILL.md allowed-tools: no
skills/impeccable/skills/impeccable/SKILL.md               allowed-tools: YES
```

**No number in the three published reports changes, and no correction comment
is owed on the three open issues.** The defect is real and it is the runner's,
but its blast radius is exactly the set of skills that declare `allowed-tools`
— which is why it went unseen until a skill that declares them was measured.
The fix in *What to change* item 1 still stands: the trigger signal should
verify activation rather than infer it, so the next such skill fails loudly
instead of silently.

---

## The five questions

### 1. Does the skill appear in the tool trace when it triggers? By what signal?

**Yes, but the signal means the wrong thing.**

The signal is a `Skill` tool call in `--output-format stream-json`, read from
`input.skill`. It appeared as `impeccable:impeccable` — the `plugin:skill`
namespaced form — in 4 of 12 attempts, and Assay's `skillMatches` handles that
namespacing correctly.

The problem is that the `Skill` tool call records a *request to activate*, not
an activation. Assay reads the call and stops there; it never checks whether
the paired `tool_result` came back with `is_error: true`. For this skill the
two always disagreed:

```
CALL   Skill {"skill":"impeccable:impeccable","args":"Redesign the landing page for Meterly…"}
>>>    SKILL impeccable:impeccable          ← Assay records triggered: true
ERR    Execute skill: impeccable:impeccable ← the host denied it
msg    Let me redesign this with a cohesive visual direction…   ← base model, no skill
```

Assay reports `precision 100%` on this run. The true precision of the trigger
signal, read as "the skill ran", is **0%**: 4 recorded triggers, 0 activations.

The host does report this properly. The `result` event carries
`permission_denials`, and in the isolated reproduction it named the Skill call
by `tool_use_id`. Assay's stream parser does not read that field.

### 2. Does the PostToolUse hook run? Does it leave a trace, or is it invisible to Assay?

**It runs. It is invisible to Assay — twice over.**

`hooks/hooks.json` registers two hooks, `PostToolUse` on `Edit|Write` and
`Stop`, both invoking `scripts/impeccable hook`. `claude plugin details`
confirms the host sees them and labels them *"harness-only — no model context
cost"*.

Three things had to be checked separately.

**Does `--plugin-dir` wire plugin hooks at all?** Yes. I built a throwaway
plugin whose PostToolUse hook appends to a file, loaded it with `--plugin-dir`,
and made the model perform one `Edit`. The marker file was written. Two of
three sessions fired it; the third did not, on a host where Git Bash
intermittently dies with `bash.exe: *** fatal error - add_item … errno 1` —
the same crash the session's own `SessionStart` hooks reported in-stream as
`exit_code: 5, outcome: "error"`.

**Does the hook's output reach the model?** No. The impeccable hook, run
directly against a synthetic PostToolUse payload, emits:

```json
{"hookSpecificOutput":{"hookEventName":"PostToolUse","additionalContext":
"[impeccable@1] Design hook scanned src/routes/landing.tsx. No deterministic
design-quality issues found. …"}}
```

In a probe where the hook demonstrably fired, no such text appeared anywhere in
the stream, and the model — asked directly to report any text containing the
marker string — reported none.

**Does the stream carry hook events?** Partly, and Assay drops what there is.
`--output-format stream-json` emits `system/hook_started` and
`system/hook_response` events with `output`, `stdout`, `stderr`, `exit_code`
and `outcome` — but in every probe only for `SessionStart`, never for
`PostToolUse`. And Assay's parser ignores every `system` event except
`subtype: "init"`, so even the events that do exist never reach a trace.

Net: a `PostToolUse` hook is unobservable through Assay today. It is observable
through the filesystem, which is how it was established here.

### 3. Do `npx impeccable` calls get through the host permission layer?

**Nothing got through. But almost nothing was attempted, and not for the reason expected.**

In the 12 pilot attempts, the skill's CLI was invoked **zero** times. Eleven
shell calls were made in total (9 `Bash`, 2 `PowerShell`), all of them ordinary
shell work — `ls`, `find`, `npm run` — and **all eleven issued after Claude
Code's own bundled `run` skill had taken over**; 3 were denied for want of
approval and 1 more was rejected by the host's command parser. The impeccable
launcher was never reached, because the skill body that instructs it never
loaded.

To measure the layer that question 3 is actually about, I ran the control
plugin (skill loads) and told the model to follow the Setup section verbatim.
It did, correctly, and was refused both times:

| # | Command | Outcome |
| --- | --- | --- |
| 1 | `"…\scripts\impeccable.cmd" context --target src/routes/landing.tsx` | rejected by the host's command parser — *"malformed syntax that cannot be parsed: Unexpected token 'context'"* |
| 2 | `& "…\scripts\impeccable.cmd" context --target src/routes/landing.tsx` | **denied** — *"requires approval"*, recorded in `permission_denials` |

**2 attempted, 0 passed.** And the declared allowlist could not have saved
either one: `Bash(npx impeccable *)` matches a bare `npx` invocation, while
4.2.0's own `SKILL.md` instructs an absolute path to
`<skill-base-dir>/scripts/impeccable` (or `.cmd` on Windows). The frontmatter
grants permission for a command the skill no longer tells the model to run.

Two further ceilings sit behind the permission layer, both verified:

- **No engine binary ships with the plugin.** The launcher resolves
  `scripts/bin/<os>-<arch>/impeccable`, then `~/.impeccable/bin/<version>/`,
  then `PATH`, then downloads from the GitHub release channel. Nothing is
  bundled; the first run downloads ~14 MB (`engine-v0.1.0`, verified against a
  `.sha256` sidecar, refusing to exec if either the sidecar or a local
  `sha256` tool is missing).
- **The sandbox's shell cannot perform that download.** Claude Code's Bash tool
  on this host runs a Git Bash with a stripped `PATH`: `cat`, `head` and
  `curl` are all absent (`/usr/bin/bash: line 1: curl: command not found`, and
  the same for `head` in the earlier `ui-ux-pro-max` traces). The launcher's
  `fetch_url` needs `curl` or `wget` and has neither, so it exits 127 with an
  installation message.

  On this machine the engine is now cached at `~/.impeccable/bin/0.1.0/` —
  because I ran the hook once by hand while probing. **The pilot therefore ran
  against a primed host, not a cold one.** A genuinely cold sandbox cannot
  install the engine at all, and every impeccable script path in it is dead
  regardless of permissions.

**Answer to the critical question, stated plainly: Suite B (behaviour) and Suite C
(resource usage) cannot be measured in this environment.** Not because the
calls are denied — although they are — but because the skill does not execute.
There is no behaviour to observe and no resources to count. Fixing the
permission layer alone would not change this; the activation denial in
question 1 has to be fixed first, and then the launcher problem in question 3,
and then the cold-start problem behind it.

### 4. Which of the reference files are read in the trace?

**None. Zero, across all 12 attempts.**

The premise needs a correction: the skill ships **35** reference files, not
seven — `adapt.md` through `visualize.md` plus a `degraded/` subdirectory, one
per sub-command in the 23-command table, largest `critique.md` at 40 KB.

`SKILL.md` routes to them by relative markdown link, which the model resolves
by `Read`ing the path. Because the skill body never loaded, no path was ever
named, so no `Read` was ever issued. The instrument works — `tools/observability.mjs`
matches `reference/<name>.md` against `Read`/`Grep`/`Glob` arguments, and it
correctly reports the empty set. There is simply nothing to report.

This question stays open until question 1 is fixed, and it is the one most
worth reopening: 35 files behind one 85-line `SKILL.md` is exactly the shape
that the `ui-ux-pro-max` coverage measurement was built for.

### 5. Does another bundled skill compete on these cases?

**Yes — but not one of Impeccable's.**

Impeccable bundles one skill and four sub-agents
(`impeccable-asset-producer`, `-documenter`, `-finish-reviewer`,
`-manual-edit-applier`). None of the four was ever spawned; they are invoked
from the skill body, which never loaded. Internally the plugin has no
competing skill.

The competition came from the **host**. Assay isolates each attempt from the
user's skills and plugins with a fresh `CLAUDE_CONFIG_DIR`, but Claude Code's
own bundled skills stay available — the init event lists 16 of them alongside
`impeccable:impeccable`, including `dataviz`, `design-sync` and `run`. `run` fired in 2 of 12 attempts, both times
immediately after impeccable's activation was denied, and it consumed a
disproportionate share of the run: **all 11** shell calls, every permission
denial, and roughly half the tool calls in the whole suite.

```
CALL Skill {"skill":"impeccable:impeccable", …}
ERR  Execute skill: impeccable:impeccable
…
CALL Skill {"skill":"run"}
msg  Base directory for this skill: …\bundled-skills\2.1.261\…\run
     **Running means launching the actual app and in…
```

Note the contrast in that excerpt: `run` returns its body, impeccable returns
an error. `run` declares no `allowed-tools`.

---

## The trigger numbers, for the record

Do not quote these. They describe a base model that was denied a skill.

| Case | Expected | Result |
| --- | --- | --- |
| `trigger.positive.hero_direction` | trigger | 100% (N=3, 95% CI 44%–100%) |
| `trigger.positive.settings_rework` | trigger | 33% (N=3, 95% CI 6%–79%) |
| `trigger.negative.near_neighbor.undefined_email` | quiet | 100% (N=3, 95% CI 44%–100%) |
| `trigger.negative.unrelated.slow_query` | quiet | 100% (N=3, 95% CI 44%–100%) |

Precision 100% (N=4), recall 67% (N=6), F1 0.80. At three attempts a case, none
of these intervals excludes a coin flip. The one observation that survives the
caveat is qualitative and consistent with the three earlier measurements: the
near neighbour held. All three attempts at the `InviteForm` exception fix
stayed quiet, read one file, added a guard, and stopped — a frontend request
with no design decision in it did not pull a design skill.

---

## Verdict

### Runnable today

- **Suite A — trigger discrimination**, with one correction applied. The `Skill`
  tool call is readable and the namespacing works. It must be paired with its
  `tool_result` before a call counts as a trigger, or every number is inflated
  by denied activations.

### Not runnable in this environment

- **Suite B — behaviour.** The skill does not execute. There is no behaviour.
- **Suite C — resource usage.** Same cause; also, the 45 tool calls and $0.54
  in this run are the base model's, not the skill's.
- **Reference-file coverage.** Nothing is read because nothing is loaded.
- **Hook behaviour.** The hook runs and is invisible: no `PostToolUse` hook
  event in the stream, and Assay drops the `system` events that do exist.
- **Sub-agent usage.** Reachable only from the skill body.

### What to change before the full measurement

1. **Fix the runner's trigger signal first.** A `Skill` call whose
   `tool_result` has `is_error: true` is a denial, not a trigger. Read
   `result.permission_denials` too — the host already reports it and the parser
   already ignores it. Without this, a full run produces confident, wrong
   numbers rather than `unknown` ones, which is the failure mode the
   three-valued verdict exists to prevent.
2. **Give the runner a permission mode.** `acceptEdits` is hardcoded in 0.1.3
   and cannot activate a skill that declares `allowed-tools`. Either expose
   `--permission-mode`, or add an explicit allow-list for the skill under test
   so its own declared tools are pre-granted. Whichever is chosen has to be
   stated in the report: a skill measured with its tools granted and one
   measured without are two different measurements.
3. **Parse `system/hook_started` and `system/hook_response`.** They are already
   in the stream with `stdout`, `stderr`, `exit_code` and `outcome`. That gives
   hooks a trace at no cost. It will not cover `PostToolUse`, which the host
   does not emit — for that, a hook-observability measurement needs a
   filesystem side-channel, as used here.
4. **Decide the engine question and state it.** Either pre-install the engine
   binary and declare the sandbox primed, or leave it cold and report that the
   skill's scripts cannot run. Do not let it happen by accident, as it did
   here.
5. **Fix the Windows shell before trusting any of it.** Git Bash on this host
   crashes intermittently (`add_item … errno 1`) and the Bash tool's `PATH` is
   missing `cat`, `head` and `curl`. Both corrupt hook results and shell-based
   skill work. Neither is Impeccable's fault, and both belong in the
   environment section of any report that follows.
6. **Widen the case set once 1 and 2 are done.** Four cases at three attempts
   was the right size for a feasibility probe and is the wrong size for
   anything else. The near neighbour needs a second flavour — a visual decision
   that is not a frontend interface — matching the two-axis design used for
   `ui-ux-pro-max`.

Two of these are Impeccable's to fix, and both are worth reporting upstream:
the `allowed-tools` entry no longer matches the command `SKILL.md` instructs,
and declaring `allowed-tools` at all makes the skill undeployable in any
non-interactive host. The rest are the runner's.

---

## Reproduce

```
npx @ktlsr/assay@0.1.3 validate suites/impeccable.pilot.suite.yaml
npx @ktlsr/assay@0.1.3 run suites/impeccable.pilot.suite.yaml \
  --skill ./skills/impeccable --html reports/impeccable.pilot.html
node tools/observability.mjs .assay/runs/<run-id>.json
```

Needs Node 22 and `CLAUDE_CODE_OAUTH_TOKEN` or `ANTHROPIC_API_KEY`. 12 attempts,
$0.54 at the pinned model. Run records land in `.assay/runs/` and are
gitignored.

The control that isolated the activation denial is a copy of
`skills/impeccable/` with the two `allowed-tools` lines removed from
`skills/impeccable/SKILL.md`, run with the same flags.
