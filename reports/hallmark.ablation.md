# `hallmark` — ablation: does the skill change what gets built?

The first ablation in this repository. Not "does the skill fire" but **"is the
output different because the skill was there?"** — the same tasks, run with the
skill installed and with it absent, scored by deterministic rule checks.

## Answer

**When it is invoked by name, `hallmark` measurably changes one of the eight
rules that can be checked literally, makes one worse, and leaves the rest where
the base model already had them.** On requests that only describe the work, it
does not activate at all, so it changes nothing.

| | |
| --- | --- |
| Pure black / white (`#fff`, `#000`) | **100% → 50%** of pages. Holds even under a worst-case bound. The one clear effect. |
| `transition: all` | **35% → 57%**. Worse with the skill; intervals overlap, so not significant. |
| Any literal rule broken | 100% → 79%. Separates on pages built, **does not survive** the worst-case bound. |
| Other six literal rules | No difference; mostly 0% in both arms. |
| Organic requests ("build the landing page") | Skill activated **0 / 12**. Arms identical. |
| Stopped without building | **12 / 40** invocations asked the user questions and ended — the brief already answered them. |
| Rulebook reads | **0** attempts to open `anti-patterns.md` or `slop-test.md`, where 12 of the 14 checked tells are defined. |

| | |
| --- | --- |
| Skill | `Nutlope/hallmark` 1.1.0 @ `13ac0ec7e148655948100b6396439e481361d690`, MIT |
| Arm A | `skills/hallmark/` — the skill directory unmodified, in a one-skill plugin wrapper so `--plugin-dir` can load it · skill hash `sha256:bc95b2e5…` |
| Arm B | `skills/hallmark-absent/` — same plugin name, no skills · skill hash `sha256:3c2f7449…` |
| Model | `claude-haiku-4-5-20251001` · host `claude-code` 2.1.263 · `acceptEdits` |
| Runner | `@ktlsr/assay@0.3.2`, `--concurrency 4` |
| Round 1, organic | `suites/hallmark.ablation.suite.yaml` `sha256:cab3da38…`, `--fast`, 15 attempts per arm, $1.33 |
| Round 2, explicit | `suites/hallmark.ablation.explicit.suite.yaml` `sha256:fc75bd26…`, full, 50 attempts per arm, $7.63 |
| Same in both arms | suite file, fixtures, prompts, model, N, permission mode — only `--skill` differs |

---

## 1. Feasibility — answered before any code

**Can "prevents AI-slop design" be measured deterministically? For part of it.**

- **The skill has its own rule list.** `references/anti-patterns.md` names about
  60 tells; `references/slop-test.md` has 58 gates. There is no executable
  detector — only prose.
- **Some tells are defined as code**, so the regex *is* the rule. Eight of them
  are checked here as **literal** rules.
- **Some have a judgement part a regex cannot see** — "glassmorphism *without
  purpose*", a hover scale on *every* card. Six are counted as **proxies**: the
  regex counts the ingredient, not the verdict.
- **Many cannot be measured this way** — "default-attractor sameness",
  "AI-illustration look", invented metrics. Left out, not approximated.
- **No LLM judge.**

| Rule | Kind | What is matched |
| --- | --- | --- |
| `gradient_headline` | literal | `background-clip: text`, `bg-clip-text` |
| `pure_black_white` | literal | `#000`/`#fff` (3 and 6 digit), opaque `rgb()` black/white, `bg-`/`text-` white/black, `: white;` |
| `transition_all` | literal | `transition: all`, a shorthand starting with a duration (which animates all), `transition-all` |
| `z_index_9999` | literal | `z-index: 9999` and up |
| `width_100vw` | literal | `width: 100vw` (incl. min/max), `w-screen` |
| `emoji_icon` | literal | the six emoji the skill names |
| `placeholder_names` | literal | the three names the skill names |
| `italic_headers` | literal | `<em>`/`<i>` inside `h1`–`h3`, or `h1`–`h3` set `font-style: italic` |
| `hover_scale` | proxy | `hover:scale-*`, or a `:hover` rule that scales up |
| `purple_gradient` | proxy | a gradient containing a purple/violet/indigo/fuchsia value |
| `inter_primary` | proxy | Inter, Roboto or Open Sans as a declared font |
| `glassmorphism` | proxy | `backdrop-filter: blur`, `backdrop-blur` |
| `aurora_blob` | proxy | `filter: blur()` of 40px or more, `blur-2xl`/`3xl` |
| `bounce_easing` | proxy | overshooting `cubic-bezier`, `animate-bounce`, bounce/elastic keyframes |

**Encoding.** assay's `file_content_matches` can only assert that a pattern *is*
present, so each check is a negative lookahead — `^(?![\s\S]*(?:tell))` — that
passes only when no file contains the tell, asserted over `**/*.html` and
`**/*.css` separately. `**/*` was ruled out deliberately: `SKILL.md` has the
skill write notes to `.hallmark/log.json` and `.hallmark/preflight.json`, which
can name the tells it avoided, and would have produced violations only in arm A.
A "no file matches" miss is an absent file, not a violation. All 28 patterns
come from one table in `tools/hallmark-ablation.mjs`, which carries a
self-check, and were round-tripped through the YAML byte-for-byte.

## 2. Round 1 — organic requests: the skill does not activate

Four greenfield tasks — a developer-tool landing page, a neighbourhood bakery, a
two-person design studio, a one-day conference — each from a short fictional
brief:

> Read brief.md and build the landing page it describes as a static site: HTML
> and CSS only, no build step and no dependencies. Put the page in index.html.

"Build a new app or landing page" is the first trigger in hallmark's own
description.

| | Arm A | Arm B |
| --- | --- | --- |
| page attempts | 12 | 12 |
| **hallmark activated** | **0 / 12** (95% CI 0–24%) | 0 / 12 (absent) |
| what every attempt did | read `brief.md`, write `index.html`, stop | the same |

The skill was loaded in arm A — the host's skill list in arm A's run record
includes `hallmark:hallmark`, and arm B's does not. The model did not reach for
it. With no activation the two arms are the same model, so the round was not
extended; a three-attempt check with the skill named activated 3 / 3, which is
what round 2 is built on.

## 3. Round 2 — explicit invocation

### The validity cost of arm B, stated up front

Every page prompt in round 2 starts **"Use the hallmark skill."** — in **both**
arms. In arm A that names a skill that exists. **In arm B it asks for a skill
that is not installed.** The request itself is unchanged: the same brief, the
same instructions, the same words, character for character. What differs is
only whether the named skill exists to answer it.

That is the closest thing to "the same request, without the skill" that can be
built for a skill that does not activate on its own. It is not identical to a
user who never mentions hallmark, and it gives arm B's model one thing arm A's
does not: a failed lookup. In 11 of 40 arm-B page attempts the model called the
`Skill` tool for `hallmark` and got back `Unknown skill: hallmark`; in all 40 it
then built the page anyway.

### Activation and output

| | Arm A | Arm B |
| --- | --- | --- |
| page attempts | 40 | 40 |
| hallmark activated | **40 / 40** | 0 / 40 |
| **produced a page** | **28 / 40** | 40 / 40 |
| control case (Postgres index) activated | 0 / 10 | 0 / 10 |
| cost | $5.16 | $2.47 |

**Twelve activated attempts built nothing.** All twelve stopped at hallmark's
design-context gate and asked the user questions:

> Before I build, I need three things: 1. **Audience** — Who will use this?
> What do they care about? 2. **Use case** — What's the one action the page
> should drive? …

Under `claude -p` nobody answers, so the attempt ends without a page. Each brief
already states its audience and the page's purpose. This is the skill working
as written — it gates on context — but in a non-interactive run it costs 30% of
the output, and it means the pages below are the 28 attempts that went past the
gate, not all 40.

### Result 1 — rule-violation rates, arm A against arm B

Share of **pages built** that break each rule. 95% Wilson intervals.

| Rule | Kind | A (skill) | B (absent) | Intervals overlap? |
| --- | --- | --- | --- | --- |
| `pure_black_white` | literal | **14 / 28 (50%, 33–67%)** | **40 / 40 (100%, 91–100%)** | **no** |
| `transition_all` | literal | 16 / 28 (57%, 39–73%) | 14 / 40 (35%, 22–50%) | yes |
| `gradient_headline` | literal | 0 / 28 (0%, 0–12%) | 1 / 40 (3%, 0–13%) | yes |
| `emoji_icon` | literal | 0 / 28 (0%, 0–12%) | 4 / 40 (10%, 4–23%) | yes |
| `z_index_9999` | literal | 0 / 28 | 0 / 40 | yes |
| `width_100vw` | literal | 0 / 28 | 0 / 40 | yes |
| `placeholder_names` | literal | 0 / 28 | 0 / 40 | yes |
| `italic_headers` | literal | 0 / 28 | 0 / 40 | yes |
| `hover_scale` | proxy | 1 / 28 (4%, 1–18%) | 7 / 40 (18%, 9–32%) | yes |
| `inter_primary` | proxy | 3 / 28 (11%, 4–27%) | 0 / 40 (0%, 0–9%) | yes |
| `glassmorphism` | proxy | 2 / 28 (7%, 2–23%) | 3 / 40 (8%, 3–20%) | yes |
| `purple_gradient` | proxy | 0 / 28 | 1 / 40 (3%, 0–13%) | yes |
| `aurora_blob` | proxy | 0 / 28 | 0 / 40 | yes |
| `bounce_easing` | proxy | 0 / 28 | 0 / 40 | yes |

| Page level | A | B | Overlap? |
| --- | --- | --- | --- |
| breaks at least one literal rule | 22 / 28 (79%, 60–90%) | 40 / 40 (100%, 91–100%) | **no** |
| literal rules broken, mean of 8 | 1.07 | 1.48 | |
| pages with no literal violation | 6 / 28 | 0 / 40 | |

**The worst-case bound.** Because 12 arm-A attempts built nothing, the table
above compares 28 pages with 40. If every one of those 12 is counted as a page
that *would* have broken the rule — the least favourable assumption for the
skill:

| | A, worst case (of 40) | B (of 40) | Overlap? |
| --- | --- | --- | --- |
| `pure_black_white` | 26 / 40 (65%, 50–78%) | 40 / 40 (91–100%) | **no — the effect holds** |
| any literal rule | 34 / 40 (85%, 71–93%) | 40 / 40 (91–100%) | yes — the effect does not hold |

Per case, the mean number of literal rules broken is lower with the skill in all
four tasks, though each cell is small:

| Case | A pages · mean | B pages · mean |
| --- | --- | --- |
| `devtool` | 8 · 1.38 | 10 · 1.80 |
| `bakery` | 6 · 0.67 | 10 · 1.60 |
| `studio` | 8 · 1.25 | 10 · 1.30 |
| `event` | 6 · 0.83 | 10 · 1.20 |

Non-overlapping intervals are a conservative test — overlap does not prove
there is no difference — so "no difference" above means "not shown", not
"shown absent".

**`transition: all` gets worse, and the reason is visible in the output.** The
arm-A declarations the check flags are almost all of one shape:

```
transition: all var(--dur-fast) var(--ease-out)      13×
transition: all var(--dur-base) var(--ease-out)       5×
transition: all <n>ms var(--ease-out)                 5×
```

These use hallmark's own duration and easing tokens, as `SKILL.md` instructs —
and animate `all`, which is exactly the tell `anti-patterns.md` names
("Specify the properties"). `SKILL.md` does not mention transitions at all.

### Result 2 — reads of the skill's reference files

| | Arm A | Arm B |
| --- | --- | --- |
| attempts to read any `references/*.md` | **3** | 0 |
| — of which succeeded | **0** | — |
| attempts to read `anti-patterns.md` or `slop-test.md` | **0** | 0 |

All three attempts were for `references/macrostructures.md`, and all three were
refused by the host's permission layer:

```
Claude requested permissions to read from …\assay-skill-…\skills\hallmark\references\macrostructures.md
```

— the same refusal `impeccable` hit under `acceptEdits`, because the staged
skill sits outside the attempt workspace. But the refusal is not what kept the
rulebook out: **no attempt tried to open it.** Twelve of the fourteen tells
checked here are defined only in `anti-patterns.md` and `slop-test.md`;
`SKILL.md` names neither `background-clip`, `#ffffff`, `transition`, `z-index`,
`100vw`, gradients nor emoji. It states two of the fourteen — no italic
headers (its rule 6) and "never bounce/overshoot on UI state" — and both were
already at 0% in arm B.

### Reading the two results together

This is an interpretation, not a measured mechanism. The one rule that moved is
the one `SKILL.md` governs in its own words: colour is routed through a locked,
OKLCH-themed token system ("every colour … must reference" the theme's tokens),
and pages built that way contain fewer literal `#fff`/`#000`. The rule that got
worse is one `SKILL.md` never mentions; the model reached for hallmark's token
names and still animated `all`. What the skill loads, it applies; what sits in
the files it never opens, it does not.

## 4. Calibration against hallmark's own showcase — separate from the ablation

**Not part of the ablation, and not mixed into its numbers.** Before any attempt,
the checks ran over the 18 example pages the project ships in `site/examples/`,
built with the skill, to catch checks that were wrong. Two were, and were fixed
before round 1:

- `z_index_9999` also matched `999`. The skill's rule is `9999`; narrowed.
- `hover_scale` matched purposeful single-element hover scales. The skill's
  tell is a *universal* hover scale, which a regex cannot see; moved to proxy.

After the fixes, **the showcase still breaks two of the skill's own literal
rules**:

| Rule | Showcase pages that break it |
| --- | --- |
| `italic_headers` | **8 / 18** — e.g. `wayfare`: `h2 em { font-style: italic }` and `h3 { font-style: italic }`; `bananastudio`: an `<em>` in nearly every `h2` |
| `pure_black_white` | **7 / 18** — `#fff`/`#000` in the token files of all five `custom-*` pages, `press-01`, `tally` |
| `glassmorphism` (proxy) | 10 / 18 — mostly floating navigation over content, which the skill allows |

"Headings are always roman" is rule 6 of `SKILL.md`. So even for the skill's own
outputs these rules do not sit at zero, and the ablation is read as a
difference in rates between arms, never as clean against dirty. The examples
may predate the rule. Either way the 18 pages here are the project's showcase,
not output from this measurement's runs.

## Limitations

- **Arm B asks for a skill that is not there** (section 3). Stated, not solved.
- **Selection in arm A.** 12 of 40 attempts stopped at a question gate and built
  nothing; rates are over the 28 that built. The worst-case bound is given for
  the two page-level results that separated.
- **N = 40 attempts per arm, 28 and 40 pages.** Enough to separate a 100% → 50%
  change; not enough to call smaller ones.
- **One model**, `claude-haiku-4-5-20251001`. Whether a larger model activates
  on organic requests, or reads the rulebook, is not measured.
- **`acceptEdits`.** Reads of the skill's reference files were refused. No
  attempt reached for the files that define the checked tells, so this did not
  decide the result — but a run that allowed those reads would not be the same
  measurement.
- **The checks cover a slice of the skill's claim.** Fourteen tells a regex can
  see; "made, not generated" as a whole is not measured and cannot be without a
  judge.
- **Round 1 used `--fast`**, which evaluates no assertions; it measured
  activation only.

## Reproduce

```
node tools/hallmark-ablation.mjs suite                       # the 28 generated assertions
node tools/hallmark-ablation.mjs calibrate <hallmark>/site/examples

# round 2 — the ablation
npx @ktlsr/assay@0.3.2 run suites/hallmark.ablation.explicit.suite.yaml \
  --skill ./skills/hallmark        --concurrency 4          # arm A
npx @ktlsr/assay@0.3.2 run suites/hallmark.ablation.explicit.suite.yaml \
  --skill ./skills/hallmark-absent --concurrency 4          # arm B
node tools/hallmark-ablation.mjs analyse A=<arm A record> B=<arm B record>
```

Records — round 2: arm A `run-2026-09-10T13-54-52-180Z-2dc28f84`, arm B
`run-2026-09-10T14-06-46-520Z-042ef1ed`. Round 1: arm A
`run-2026-09-10T13-42-04-818Z-d7a30238`, arm B
`run-2026-09-10T13-44-01-885Z-d62f8a15`. Three-attempt named check:
`run-2026-09-10T13-47-15-584Z-116ca07f`.
