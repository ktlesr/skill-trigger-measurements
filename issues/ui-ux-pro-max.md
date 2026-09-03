# `--design-system` silently drops `--stack`, and 82% of the shipped files are never opened

I measured this skill with 200 attempts across two case sets, plus a
reference-file coverage pass. Three results are worth your time. The first
reproduces from a shell in ten seconds and has nothing to do with models or
hosts.

## Setup

- `nextlevelbuilder/ui-ux-pro-max-skill@f3ac195224eac1eb0dfe1a3059c2a6add78ffbe3`
- Claude Code, model pinned to `claude-haiku-4-5-20251001`
- Installed as a minimal plugin directory: your `plugin.json` and your
  `.claude/skills/` layout, containing this skill and nothing else, so
  `${CLAUDE_PLUGIN_ROOT}` resolves and the documented `search.py` path works
- **No prompt contains the skill's name or the bare tokens "UI" and "UX"**
- Two case sets of 10 cases × 10 attempts: 3 positives, 4 near neighbours,
  2 unrelated negatives, 1 completion case, against a small Next.js fixture

## 1. `--design-system` accepts `--stack` and ignores it

Replaying both modes against the shipped data, with a Python `open()` audit hook
recording every file the script touches:

```
search.py "platform engineer dashboard" --design-system -p Acme --stack nextjs
  → opens data/{colors,landing,products,styles,typography,ui-reasoning}.csv
  → opens no stack file at all

search.py "dashboard table density" --stack nextjs
  → opens data/stacks/nextjs.csv
```

The combined command exits successfully. No warning, no error, no note in the
output that the stack was dropped.

The Query Contract in `SKILL.md` does present the modes as alternatives ("choose
the smallest search mode that fits the request"), so the combination may never
have been intended. But `SKILL.md` Step 1 also says *"Never assume a stack — a
hardcoded default silently misroutes every recommendation"*, and the model in
this run did exactly what that instruction implies: detected Next.js from
`package.json`, then passed `--stack nextjs` alongside `--design-system` and
proceeded as though the stack had been applied.

A rejected flag, or one line of "note: --stack is ignored in --design-system
mode", would close this.

## 2. In 200 attempts, neither `references/*.md` file was ever opened

`SKILL.md` points at both, explicitly as read-on-demand:

> For the full rule list per category (all 119 UX guidelines with rationale),
> read `references/quick-reference.md`. For app-specific polish rules … and the
> canonical pre-delivery checklist, read `references/pro-rules.md`.

Across 200 attempts — 40 of which triggered the skill — neither was read once.
The 119 guidelines the description advertises reached the model only through the
ten-row priority table inside `SKILL.md` itself.

That is not a bug, but it does mean the on-demand tier is currently theoretical.
If those rules matter, the priority table may need to carry the decision, or
`SKILL.md` may need to name the specific situation that should pull the
reference in — "read X before delivering" rather than "read X on demand".

## 3. Coverage: 58 of 72 shipped files are never reached

| | Files | Bytes |
| --- | --- | --- |
| ships in the skill | 72 | 3,570,102 |
| opened by the agent | 2 | 25,092 |
| opened by `search.py` | 13 | 643,105 |
| loaded by the host on trigger (`SKILL.md`) | 1 | 15,969 |
| **never opened** | **58** | **2,911,028 (82%)** |

Grouped by why the file ships:

| Group | Files | Bytes | Reading |
| --- | --- | --- | --- |
| domain data | 8 | 2,092,870 | `google-fonts.csv` (747 KB), `phosphor-icons-upstream.json` (824 KB), `google-font-licenses.json` (433 KB), `charts.csv` — no query path reached them |
| stack data | 22 | 476,731 | all 22, for the reason in section 1 |
| dev tooling | 26 | 305,992 | `scripts/tests/` and `validate_data.py` ship inside the installed skill |
| on-demand references | 2 | 35,435 | section 2 |

The dev-tooling group is the easy one: your test suite and its fixtures install
alongside the skill. That is 306 KB of install size that was never going to be
read at runtime, and excluding it from the packaged skill costs nothing.

**Read this number carefully.** It is an upper bound, not an observation. The
host's permission layer refused all 83 shell invocations of `search.py` in these
runs, so what the table reports is what the *attempted* queries would have opened
had they been allowed — computed by replaying each distinct query locally. Even
under that generous assumption, 82% of the directory goes untouched.

## 4. Two routing results, offered as data rather than as defects

**Precision is perfect.** Eight near-neighbour cases across two rounds — a
`useEffect` refetch loop, a styled-components→CSS-module migration with identical
output, a post-Tailwind-4 visual regression, a token rename, a CMYK print
palette, a wordmark brief, a projected conference deck, blog header imagery — and
two unrelated controls. **120 negative attempts, 0 false positives.** I expected a
skill this broad to over-fire; it does not.

**Recall is 50% (N=80, 95% CI 39%–61%)**, and the two rounds returned the same
number independently. Per case, pooled:

| Positive case | Fired |
| --- | --- |
| build the pricing page, choose the visual direction | 15/20 |
| review this component for accessibility and hierarchy, then fix it | 5/20 |
| pick the right chart for 14 accounts, colour-blind-safe palette | **0/20** |

The chart case is the one you may want to know about: it never lost to nothing,
it lost to `dataviz`, a skill bundled with Claude Code, on all 20 attempts.

```
msg:  I'll help you fix that visualization. Let me first check the current chart
      and then use the dataviz skill to rebuild it properly.
call  Skill  dataviz
```

Your description advertises 25 chart types; `data/charts.csv` was never opened.
On the one request where your chart data was the right answer, a host skill got
there first. Whether that is worth acting on is your call — it is a competition
you did not choose — but a description that leads with the interface work it
uniquely does, rather than with a capability list a bundled skill also covers,
might route differently.

## Reproduce

```
npx @ktlsr/assay@0.1.3 run suites/ui-ux-pro-max.suite.yaml       --skill ./skills/ui-ux-pro-max
npx @ktlsr/assay@0.1.3 run suites/ui-ux-pro-max.tight.suite.yaml --skill ./skills/ui-ux-pro-max
python tools/refcoverage.py skills/ui-ux-pro-max/.claude/skills/ui-ux-pro-max .assay/runs/<run>.json ...
```

Case sets, fixtures and both reports: <https://github.com/ktlesr/skill-trigger-measurements>
Run records stay local (`.assay/runs/`, not committed); happy to attach the JSON.

Caveats. Everything is pinned to `claude-haiku-4-5-20251001`, and trigger routing
is a model behaviour, so the recall figures are a floor rather than a universal
result. The completion case in these suites is not a valid measurement of your
persistence path: with every `search.py` invocation refused, `--persist` never
ran, so the documented `design-system/<slug>/MASTER.md` never had a chance to
appear by the documented route. Sections 1–3 do not depend on it. Section 1 does
not depend on the host at all.

Method: <https://assayctl.dev/methodology>
