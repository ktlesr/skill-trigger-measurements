---
title: "[Bug] The skill cannot activate in a non-interactive host"
labels: bug
---

## What happened?

The skill never activates under `claude -p`. Every `Skill(impeccable:impeccable)`
call returns `is_error: true` with the body `"Execute skill: impeccable:impeccable"`
— which is the title of a permission prompt, not an error message — and the
session's `permission_denials` names the call.

The cause is in `SKILL.md` frontmatter. A skill that declares `allowed-tools` is
requesting tool permissions it does not otherwise hold, so activating it needs
consent, and in a non-interactive session there is nobody to give it. Deleting
these two lines, and changing nothing else, makes the skill load normally:

```yaml
allowed-tools:
  - Bash(npx impeccable *)
```

The failure is silent from the caller's side. The model records a `Skill` call,
the activation is denied, and it then completes the work from general knowledge
— so the transcript looks like a success. Nothing behind the activation runs:
no `reference/*.md` is opened (the skill ships 35), the launcher is never
invoked, and none of the four bundled sub-agents is spawned.

A second, smaller problem sits behind the same two lines. The allowlist pattern
`Bash(npx impeccable *)` matches a bare `npx` invocation, but `SKILL.md` Setup
step 1 instructs an absolute path into the plugin root:

> Run `"<skill-base-dir>/scripts/impeccable" context` once per session […] On a
> Windows shell without `sh`, call `"<skill-base-dir>/scripts/impeccable.cmd"`
> instead.

In a run where the skill did load, the model followed step 1 correctly and the
call was denied for want of approval. So the frontmatter blocks activation in
order to permit a command the skill no longer instructs.

I found this while trying to measure the skill's trigger discrimination, which
is why the report below is a feasibility result rather than a measurement.

## Steps to reproduce

1. `claude plugin marketplace add pbakaus/impeccable`, then
   `claude plugin install impeccable@impeccable` (4.2.0).
2. In a project containing a bland frontend file, run a non-interactive session
   against the installed plugin:
   ```
   echo "src/routes/landing.tsx reads like a wireframe. Give it a real visual \
   direction and build it: type, colour, spacing." | \
   claude -p --output-format stream-json --verbose \
     --model claude-haiku-4-5-20251001 \
     --permission-mode acceptEdits \
     --plugin-dir <plugin root>
   ```
3. In the stream, find the `Skill` tool call and its paired `tool_result`:
   the result carries `is_error: true` and the content
   `"Execute skill: impeccable:impeccable"`. The `result` event's
   `permission_denials` array names the same `tool_use_id`.
4. Copy the plugin directory, delete the two `allowed-tools` lines from
   `skills/impeccable/SKILL.md`, and repeat step 2 against the copy. The
   `tool_result` now carries no error and the skill body is injected.

## Expected behavior

Invoking the skill in a non-interactive session should load it, the same way it
does interactively — or, if that is not achievable, should fail loudly rather
than silently degrading to the base model while still recording a `Skill` call.

The `allowed-tools` entry should also match the command `SKILL.md` actually
instructs, so that the setup step is covered by the permission the frontmatter
declares.

## Provider & environment

- **Provider** (Cursor / Claude Code / Gemini CLI / Codex / Copilot / Kiro / OpenCode): **Claude Code**
- **Provider version**: 2.1.261
- **OS**: Windows 11 Pro 10.0.26200

Plugin: `impeccable` 4.2.0, `pbakaus/impeccable@8dac6ae7e020c43ab10ce9b41939f6fd42627b96`,
skill content `sha256:cd74d14b…`. Model pinned to `claude-haiku-4-5-20251001`,
`--permission-mode acceptEdits`. Installed via the documented marketplace path
into an isolated `CLAUDE_CONFIG_DIR`; the resulting plugin cache is what was
measured, unmodified.

## Additional context

### The control experiment

Same plugin directory, same prompt, same flags, same model. The only change is
that the two `allowed-tools` lines are deleted from `SKILL.md`.

| | `Skill` tool result | `permission_denials` | Skill body loaded |
| --- | --- | --- | --- |
| 4.2.0 as published | `is_error: true` · `"Execute skill: impeccable:impeccable"` | 1 entry | no |
| identical, two lines removed | `is_error: undefined` · `"Launching skill: impeccable:impeccable"` | empty | **yes** |

As published:

```
CALL   Skill {"skill":"impeccable:impeccable","args":"Redesign the landing page for Meterly…"}
ERR    Execute skill: impeccable:impeccable
msg    Let me redesign this with a cohesive visual direction…   ← base model, no skill
```

```json
"permission_denials": [
  { "tool_name": "Skill",
    "tool_use_id": "toolu_016ELXwpHGxv7VjLK7KX4P94",
    "tool_input": { "skill": "impeccable:impeccable", "args": "src/routes/landing.tsx" } }
]
```

With the two lines removed:

```
CALL Skill {"skill":"impeccable:impeccable","args":"src/routes/landing.tsx"}
  RES is_error=undefined :: "Launching skill: impeccable:impeccable"
TEXT Base directory for this skill: …\skills\impeccable
     This skill gives you the tools and permission to create design that earns…
```

That is the whole difference. Two lines. 4 of 4 activations were denied in
every attempt where the model reached for the skill.

For contrast inside the same runs: Claude Code's bundled `run` skill fired in 2
of 12 attempts, returned its body, and proceeded. It declares no
`allowed-tools`.

### The allowlist mismatch, observed

In the control run where the skill loaded, the model followed Setup step 1 and
was refused both times:

| # | Command issued | Result |
| --- | --- | --- |
| 1 | `"…\scripts\impeccable.cmd" context --target src/routes/landing.tsx` | rejected by the host's command parser — *"malformed syntax that cannot be parsed: Unexpected token 'context'"* |
| 2 | `& "…\scripts\impeccable.cmd" context --target src/routes/landing.tsx` | **denied** — *"requires approval"*, recorded in `permission_denials` |

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

### What this means in practice

Anywhere a human cannot answer a prompt, the skill is inert while appearing to
work: CI, `claude -p`, SDK and headless sessions, evaluation harnesses, and any
agent loop running unattended.

The trade-off is yours to weigh, and it is a real one: dropping `allowed-tools`
means the launcher call needs approval on first use in an interactive session,
which is friction you presumably added the frontmatter to remove. Options that
would keep both properties — a narrower pattern that actually matches the
instructed command, or documenting a settings-level allow rule instead of a
frontmatter declaration — are worth more thought than I can give from outside
the project.

### What I could not measure

I want to be explicit that this is a feasibility result, not a measurement of
the skill.

I ran 4 cases × 3 attempts against a small React fixture, with no prompt
containing the skill's name, the word "design", or any of the 23 sub-command
names. The trigger numbers that run produced — precision 100% (N=4), recall 67%
(N=6) — describe a base model that was denied a skill, not the skill. They
should not be quoted, and I am not publishing them as a measurement. Behaviour,
resource usage and reference-file coverage could not be measured at all,
because there was no execution to observe.

One qualitative result does survive, for what three attempts are worth: the
near neighbour held. A frontend request with no design decision in it — fixing
a `Cannot read properties of undefined` crash in a member-filter component —
stayed quiet all three times, read one file, added a guard, and stopped.

### Reproduce

```
npx @ktlsr/assay@0.1.3 run suites/impeccable.pilot.suite.yaml --skill ./skills/impeccable
node tools/observability.mjs .assay/runs/<run>.json
```

The control is the same directory with the two `allowed-tools` lines removed
from `skills/impeccable/SKILL.md`, run with identical flags.

Case set, fixture and the full feasibility report:
<https://github.com/ktlesr/skill-trigger-measurements>
Run records stay local (`.assay/runs/`, not committed); happy to attach the JSON.

### Caveats

Everything is pinned to `claude-haiku-4-5-20251001` and to Claude Code 2.1.261;
whether a permission prompt blocks skill activation is host behaviour and could
differ elsewhere, though the control isolates the cause to the frontmatter
rather than to the host's policy. The Windows notes above — the missing `curl`
and the parser's treatment of a quoted `.cmd` path — are specific to this
platform; the allowlist mismatch itself is not.

Method: <https://assayctl.dev/methodology>

## Willing to work on a fix?

Not planning to open a PR — the trade-off between activation and first-use
friction is a project decision, and the right shape of the fix depends on
context I do not have from outside.

I am glad to re-run the measurement once it is resolved, and would like to: the
full trigger-discrimination suite is written and pinned, and it needs only a
version where the skill actually loads. Happy to attach the raw run records
meanwhile, or to test a candidate fix against the same case set before it
ships.
