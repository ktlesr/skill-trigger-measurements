# Follow-up on 4.2.1: the skill activates now, and then cannot reach its own tools

Thank you for #738 — it fixes the blocker completely. The skill activated in
**28 of 28** attempts where the model reached for it, with zero refusals, so I
was able to run the full measurement the pilot could not.

The headline is good news and I want to lead with it: **precision 100% (N=28,
95% CI 88%–100%), zero false positives in 70 negative attempts.** Seven negative
cases, four of them frontend work with no visual decision in it — one of those
in the same file a positive case targets, `src/routes/landing.tsx`, once asking
for a visual direction and once for an analytics event — plus two visual
decisions that are not interfaces. The boundary your description declares held on every one.

What follows is what the measurement found downstream of activation. Most of it
is not a defect in your skill; it is what happens to a skill of this shape in a
non-interactive host, and I think it is worth knowing.

## Setup

- `pbakaus/impeccable@831cabee8b4bc1a2b66e5ae22003e9a19b57d464`, plugin version
  4.2.1, skill content `sha256:c3185df7…`
- Installed the documented way — `claude plugin marketplace add
  pbakaus/impeccable`, then `claude plugin install impeccable@impeccable` — into
  an isolated `CLAUDE_CONFIG_DIR`; the resulting plugin cache is what was
  measured, unmodified
- Claude Code 2.1.263 on Windows 11, model pinned to
  `claude-haiku-4-5-20251001`, `--permission-mode acceptEdits`
- 12 cases × 10 attempts = 120, against a small React fixture. **No prompt
  contains the skill's name, the word "design", or any of the 23 sub-command
  names**
- Full report: <https://github.com/ktlesr/skill-trigger-measurements/blob/master/reports/impeccable.md>

---

## 1. Setup step 1 cannot execute in a non-interactive host

`SKILL.md` opens with a shell-out, and the model followed it faithfully:

> Run `"<skill-base-dir>/scripts/impeccable" context` once per session […] It
> loads PRODUCT.md, DESIGN.md, the matching surface brief […] follow its
> directives and do not rerun it.

| Verb | Attempted | Refused | Ran |
| --- | --- | --- | --- |
| `context` | 55 | 55 | 0 |

**55 invocations, 55 refusals, 0 executions**, across the 28 activations. Two
shapes of refusal, both from the host's command parser:

```
Bash        "…\skills\impeccable\scripts\impeccable.cmd" context
            → "This command requires approval"

PowerShell  & "…\skills\impeccable\scripts\impeccable.cmd" context
            → "This PowerShell command contains multiple operations. The
               following part requires approval: & "…impeccable.cmd" context"
```

The launcher itself is fine. Run by hand outside the sandbox against the same
fixture it returns its full directive set — `NO_PRODUCT_MD`, `RESOLVED_CONTEXT`,
`MANUAL_DETECTOR_REQUIRED` — in about a second. The blocker is the permission
layer, not your tooling.

This is the same class of problem #738 solved, one level down: 4.2.0 could not
activate without consent, and 4.2.1 activates but cannot perform the first thing
it instructs without consent. Anywhere a human cannot answer a prompt — CI,
`claude -p`, SDK and headless sessions, evaluation harnesses — step 1 fails and
the model improvises from `SKILL.md` alone.

The `SKILL.md` routing text already anticipates something like this ("a narrow
refinement of existing code proceeds on the incumbent implementation as
`impeccable context` directs"), but there is no instruction for what to do when
the command is *refused* rather than merely unhelpful. A documented degraded path
— what to load, what to assume, what to tell the user — would turn a silent
improvisation into a stated one.

Worth noting for whatever shape a fix takes: the PowerShell call operator `&` is
the correct way to invoke a quoted path, and it is exactly the form the host's
parser rejects as a compound command.

## 2. `<skill-base-dir>` is ambiguous, and 8 of 55 calls resolved it wrongly

The host reports the **plugin root** as the skill's base directory. The launcher
lives two levels below it, at `<plugin-root>/skills/impeccable/scripts/`. In 8 of
the 55 invocations the model built the path from the reported base directly:

```
…\assay-skill-sboeLx\scripts\impeccable.cmd context          ← does not exist
…\assay-skill-sboeLx\skills\impeccable\scripts\impeccable.cmd context   ← correct
```

Both would have been refused here anyway, so this cost nothing in this run — but
in a session where the command *is* permitted, one in seven attempts would run a
path that is not there. Spelling the suffix out in `SKILL.md`
(`<skill-base-dir>/scripts/impeccable`, where `<skill-base-dir>` is the
directory containing this `SKILL.md`) would remove the ambiguity.

## 3. The 35 reference files are not being read

This is the finding I would most want your view on, because it is not a
permission problem.

| | Files | Bytes |
| --- | --- | --- |
| ships under `reference/` | 35 | 352,712 |
| opened across 28 activations | **0** | **0** |

**One** reference file was reached for in 28 activations — `onboard.md`, once —
and the host refused that read because the plugin directory sits outside the
workspace. The other 27 activations never named a reference file at all.

Two specific consequences:

- `SKILL.md` step 3 says to load `reference/craft-floor.md` **immediately before
  editing UI**, and calls it the quality floor and the absolute bans. All 28
  activations edited UI. None loaded it.
- The completion case asked, in the skill's own terms but without naming any
  command, for the project's visual system to be worked out and written down at
  the project root. `reference/document.md` — 27,844 bytes specifying the
  DESIGN.md format, its token schema and its eight-section order — was never
  opened.

My reading is that steps 2 and 3 are gated behind step 1 in practice: when the
`context` call fails, the model does not treat the rest of Setup as still
binding, and `SKILL.md` alone is a strong enough prompt that it proceeds. Whether
that is worth restructuring is a judgement about your own instruction design, not
something the measurement can decide.

## 4. The hook fetches and caches a binary outside the permission layer

Not a defect, but surprising enough that I think it should be stated somewhere
users will see it.

`hooks/hooks.json` runs `scripts/impeccable hook` on `PostToolUse(Edit|Write)`
and `Stop`. Hooks run as harness subprocesses, not through the tool permission
layer. Controlled test: I moved `~/.impeccable/bin/0.1.2/` aside, ran a
four-attempt session, and afterwards:

| | |
| --- | --- |
| launcher calls by the model | 4 attempted, 4 refused, 0 ran |
| `~/.impeccable/bin/0.1.2/impeccable.exe` | **re-downloaded and cached during the run** |

So in a session where the user's permission layer denied every call to the
engine, the engine was still fetched over the network and written to the user's
home directory, because the hook asked for it instead of the model. The download
is verified against its `.sha256` sidecar and the 4.2.1 launcher hardening around
that is careful work — this is about expectations, not integrity.

Related, and this one is a correction to my pilot report, which said the hook's
output does not reach the model. It does. In one attempt the model had finished,
summed up its work, and then said: *"I found a performance issue detected by the
design hook. The progress bar is animating `width`, which causes layout thrash"*
— and made two more edits to switch it to `transform: scaleX()`. That is the
`Stop` hook doing exactly what it is for.

The only reason I can see it is that the model quoted it. The host emits no
`PostToolUse` hook event into `--output-format stream-json`, so a transcript
cannot tell a run where the hook fired from one where it did not.

## 5. Two request shapes do not reach the skill

Precision is perfect, so this is the only place where routing costs anything.
Recall was 56% (N=50, 95% CI 42%–69%), and it is not evenly distributed:

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

The completion case is the one I would look at first. All ten attempts wrote a
`DESIGN.md` at the project root; none of them used the skill to do it. From the
user's side that looks like the skill worked.

Every miss looks identical in the trace: `Read`, then `Edit`, no `Skill` call.
Nothing is refused and nothing errors.

## Caveats

Everything is pinned to `claude-haiku-4-5-20251001` and Claude Code 2.1.263;
trigger routing is model behaviour, so 56% is a floor for this model rather than
a universal result. The permission mode (`acceptEdits`) is part of the
measurement — a run with your launcher pre-approved would produce different
numbers for findings 1 and 3, and I have not run one. Assay stages the skill
under test in a temp directory, so the refused reference read in finding 3 is at
least partly a property of that staging; the fact that only one read was
attempted in 28 activations is not. The Windows specifics — the `&` operator and
the `.cmd` launcher — do not apply on other platforms; findings 2, 3, 4 and 5 do.

This is one round of negatives, not two. Zero false positives in 70 attempts
bounds the false-positive rate at a 95% lower bound of 95%; it does not show
where the set's discriminating power ends.

## Reproduce

```
npx @ktlsr/assay@0.2.0 run suites/impeccable.suite.yaml --skill ./skills/impeccable
node   tools/observability.mjs .assay/runs/<run>.json
python tools/refcoverage.py --exec impeccable ./skills/impeccable .assay/runs/<run>.json
```

Case set, fixture, coverage output and the full report:
<https://github.com/ktlesr/skill-trigger-measurements>
Run records stay local (`.assay/runs/`, not committed); happy to attach the JSON.

Method: <https://assayctl.dev/methodology>
