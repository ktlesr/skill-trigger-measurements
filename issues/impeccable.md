# The skill cannot activate in a non-interactive host, and its `allowed-tools` entry no longer matches the command it instructs

I set out to measure this skill's trigger discrimination the way I measured
three others. I could not: the skill never executed in any of the 12 attempts.
The reason turned out to be worth more than the measurement would have been,
and it is in two lines of frontmatter.

Both findings reproduce from a shell. Neither depends on which model is
routing.

## Setup

- `pbakaus/impeccable@8dac6ae7e020c43ab10ce9b41939f6fd42627b96`, plugin version
  4.2.0, skill content `sha256:cd74d14b…`
- Installed the documented way — `claude plugin marketplace add
  pbakaus/impeccable`, then `claude plugin install impeccable@impeccable` — into
  an isolated `CLAUDE_CONFIG_DIR`; the resulting plugin cache is what was
  measured, unmodified
- Claude Code 2.1.261 on Windows 11, model pinned to
  `claude-haiku-4-5-20251001`, `--permission-mode acceptEdits`
- 4 cases × 3 attempts against a small React fixture. **No prompt contains the
  skill's name, the word "design", or any of the 23 sub-command names**

## 1. `allowed-tools` permits a command the skill no longer instructs

`SKILL.md` frontmatter:

```yaml
allowed-tools:
  - Bash(npx impeccable *)
```

`SKILL.md` Setup, step 1:

> Run `"<skill-base-dir>/scripts/impeccable" context` once per session, where
> `<skill-base-dir>` is the loaded base directory the runtime reports for this
> skill […] On a Windows shell without `sh`, call
> `"<skill-base-dir>/scripts/impeccable.cmd"` instead.

The allowlist pattern matches a bare `npx` invocation. The instruction produces
an absolute path into the plugin root. In a run where the skill did load (see
below), the model followed step 1 correctly and was refused both times:

| # | Command issued | Result |
| --- | --- | --- |
| 1 | `"…\scripts\impeccable.cmd" context --target src/routes/landing.tsx` | rejected by the host's command parser — *"malformed syntax that cannot be parsed: Unexpected token 'context'"* |
| 2 | `& "…\scripts\impeccable.cmd" context --target src/routes/landing.tsx` | **denied** — *"requires approval"*, recorded in the session's `permission_denials` |

Two invocations attempted, zero through. The model did nothing wrong; it
executed the documented setup step, and the frontmatter did not cover it.

4.0.4 declared a second pattern, `Bash(node .claude/skills/impeccable/scripts/*)`,
which would not have matched a plugin-root absolute path either. 4.2.0 dropped
that line and moved to the launcher, leaving only the `npx` pattern — so the
gap widened rather than closed.

A note for whichever way this gets fixed: on this host the plugin ships no
engine binary, and the launcher's `fetch_url` needs `curl` or `wget`. Claude
Code's Bash tool here runs a Git Bash with a stripped `PATH` where `curl`,
`cat` and `head` are all absent, so the first-run download exits 127 with the
manual-install message. Any environment where the skill's own tools are
expected to work needs the engine present before the session starts.

## 2. Declaring `allowed-tools` at all prevents the skill from activating

This is the blocker. A skill that declares `allowed-tools` is requesting tool
permissions it does not otherwise hold, so activating it needs consent. Under
`claude -p` there is nobody to give it.

Every `Skill(impeccable:impeccable)` call in the run came back as an error:

```
CALL   Skill {"skill":"impeccable:impeccable","args":"Redesign the landing page for Meterly…"}
ERR    Execute skill: impeccable:impeccable
msg    Let me redesign this with a cohesive visual direction…   ← base model, no skill
```

`"Execute skill: impeccable:impeccable"` is not an error message — it is the
title of the permission prompt that had no one to answer it. The session's
`result` event names the call directly:

```json
"permission_denials": [
  { "tool_name": "Skill",
    "tool_use_id": "toolu_016ELXwpHGxv7VjLK7KX4P94",
    "tool_input": { "skill": "impeccable:impeccable", "args": "src/routes/landing.tsx" } }
]
```

4 of 4 activations denied, in every attempt where the model reached for the
skill. The model then completed the design work from general knowledge, so the
transcript looks like a success. Nothing behind the activation ran: no
`reference/*.md` was opened (the skill ships 35), the launcher was never
invoked, and none of the four bundled sub-agents was spawned.

### The control

Same plugin directory, same prompt, same flags, same model. The only change is
that these two lines are deleted from `SKILL.md`:

```yaml
allowed-tools:
  - Bash(npx impeccable *)
```

| | `Skill` tool result | `permission_denials` | Skill body loaded |
| --- | --- | --- | --- |
| 4.2.0 as published | `is_error: true` · `"Execute skill: impeccable:impeccable"` | 1 entry | no |
| identical, two lines removed | `is_error: undefined` · `"Launching skill: impeccable:impeccable"` | empty | **yes** |

With the lines removed the host returns the skill body and the run proceeds
normally:

```
CALL Skill {"skill":"impeccable:impeccable","args":"src/routes/landing.tsx"}
  RES is_error=undefined :: "Launching skill: impeccable:impeccable"
TEXT Base directory for this skill: …\skills\impeccable
     This skill gives you the tools and permission to create design that earns…
```

That is the whole difference. Two lines.

For contrast inside the same runs: Claude Code's bundled `run` skill fired in 2
of 12 attempts, returned its body, and proceeded. It declares no
`allowed-tools`.

### What this means in practice

Anywhere a human cannot answer a prompt, this skill is inert while appearing to
work: CI, `claude -p`, SDK and headless sessions, evaluation harnesses, and any
agent loop running unattended. The failure is silent from the caller's side —
a `Skill` call is recorded, output is produced, and the output is the base
model's.

The trade-off is yours to weigh, and it is a real one: dropping `allowed-tools`
means the launcher call needs approval on first use in an interactive session,
which is friction you presumably added the frontmatter to remove. Options that
would keep both properties — a narrower pattern that actually matches the
instructed command, or documenting a settings-level allow rule instead of a
frontmatter declaration — are worth more thought than I can give from outside
the project.

## What I could not measure

I want to be explicit that this is a feasibility result, not a measurement of
your skill.

The trigger numbers this run produced — precision 100% (N=4), recall 67%
(N=6) — describe a base model that was denied a skill, not the skill. They
should not be quoted, and I am not publishing them as a measurement. Behaviour,
resource usage and reference-file coverage could not be measured at all,
because there was no execution to observe.

One qualitative result does survive, for what three attempts are worth: the
near neighbour held. A frontend request with no design decision in it — fixing
a `Cannot read properties of undefined` crash in a member-filter component —
stayed quiet all three times, read one file, added a guard, and stopped.

I would like to run the full measurement, and I will once finding 2 is
resolved, either upstream or by measuring with the skill's tools explicitly
pre-granted. Either way the report will state which, since a skill measured
with its tools granted and one measured without are two different
measurements.

## Reproduce

```
npx @ktlsr/assay@0.1.3 run suites/impeccable.pilot.suite.yaml --skill ./skills/impeccable
node tools/observability.mjs .assay/runs/<run>.json
```

The control is the same directory with the two `allowed-tools` lines removed
from `skills/impeccable/SKILL.md`, run with identical flags.

Case set, fixture and the full feasibility report:
<https://github.com/ktlesr/skill-trigger-measurements>
Run records stay local (`.assay/runs/`, not committed); happy to attach the JSON.

Caveats. Everything is pinned to `claude-haiku-4-5-20251001` and to Claude Code
2.1.261; whether a permission prompt blocks skill activation is host behaviour
and could differ elsewhere, though the control isolates the cause to the
frontmatter rather than to the host's policy. The Windows notes in finding 1 —
the missing `curl` and the parser's treatment of a quoted `.cmd` path — are
specific to this platform; the allowlist mismatch itself is not.

Method: <https://assayctl.dev/methodology>
