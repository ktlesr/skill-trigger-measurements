# Issue draft for Nutlope/hallmark

Not posted. Title and body below.

---

**Title:** Measured: hallmark cuts pure black/white from 100% to 50% of pages — and four places it could do more

---

I ran an ablation on hallmark: the same four landing-page tasks, once with the
skill installed and once without it, with the output of both scored by
deterministic checks. No LLM judge — every check is one of the tells your own
`references/anti-patterns.md` names, written as a pattern. 100 attempts in the
main round, one model, everything pinned; method and raw numbers are linked at
the end.

**The short version: the skill measurably changes what gets built, and the
effect holds up under the least favourable assumptions I could make.** The rest
of this is where I think it could do more, with the evidence for each.

## How the comparison was set up — and its one cost

Both arms get the same four briefs (a developer tool, a bakery, a design studio,
a one-day conference) and the same prompt. The only difference is whether the
skill exists.

Every prompt starts **"Use the hallmark skill."**, in both arms. I did that
because on requests that only describe the work, the skill did not activate
(section 5), so there would have been nothing to compare. The cost: in the arm
without the skill, the prompt asks for a skill that is not installed. The
request itself is identical, word for word; only whether the named skill exists
differs. In 11 of 40 attempts that arm tried to load it, got `Unknown skill:
hallmark`, and built the page anyway.

## 1. The colour rule works — clearly

Share of pages that use pure black or white (`#000`/`#fff`, opaque
`rgb(0,0,0)`/`rgb(255,255,255)`, `bg-white` and friends):

| | pages | 95% interval |
| --- | --- | --- |
| without hallmark | **40 / 40 (100%)** | 91–100% |
| with hallmark | **14 / 28 (50%)** | 33–67% |

The intervals do not overlap. And because 12 of the 40 attempts with the skill
built no page (section 4), I also counted every one of those 12 as a page that
*would* have used pure black or white — the least favourable assumption for the
skill. It still holds: **26 / 40, 50–78%, against 91–100%.**

Every page without the skill had the tell; half the pages with it did not. That
is a real, measurable change in output. The other literal checks were rare in both
arms already — 0–10% of pages (gradient headlines, emoji icons,
`z-index: 9999`, `100vw`, italic headers, placeholder names) — so there was
little room for them to show an effect.

## 2. `transition: all` gets more common with the skill — using its own tokens

| | pages with `transition: all` |
| --- | --- |
| without hallmark | 14 / 40 (35%, 22–50%) |
| with hallmark | 16 / 28 (57%, 39–73%) |

The intervals overlap, so this is not a significant difference — but the
direction is the opposite of the intent, and the output shows why. Nearly every
flagged declaration with the skill has this shape:

```
transition: all var(--dur-fast) var(--ease-out)
transition: all var(--dur-base) var(--ease-out)
```

Those are hallmark's own duration and easing tokens, used as `SKILL.md` asks
("use the three named easings") — animating `all`, which is exactly the tell
`anti-patterns.md` names: "Every property animating… Specify the properties."
The skill is shaping the declaration and still producing the pattern it bans.

## 3. The reference files are never opened

With the skill active:

| | |
| --- | --- |
| attempts to read any `references/*.md` | 3 (all `macrostructures.md`) |
| attempts to read `anti-patterns.md` or `slop-test.md` | **0** |

(The three reads were refused by the host's permission layer in this setup,
because the staged skill sits outside the workspace. But the two rule files were
never even requested, so the permission question never came up for them.)

That matters because **12 of the 14 tells I checked are defined only in those
two files.** `SKILL.md` itself states two of them — no italic headers, no
bounce/overshoot easing — and mentions neither `background-clip`, `#ffffff`,
`transition`, `z-index`, `100vw`, gradients nor emoji.

**This part is my interpretation, not a measured mechanism:** the rule that
improved is one `SKILL.md` governs in its own words — colour goes through a
locked, OKLCH-themed token system — and the rule that got worse is one that
lives only in a reference file the model never opened. It looks like what
`SKILL.md` says gets applied, and what sits behind it does not. If that is
right, the cheapest lever is to put the handful of most common tells —
`transition: all` first — directly into `SKILL.md`, rather than relying on the
model to go and read `anti-patterns.md`.

## 4. The design-context gate stops non-interactive runs

**12 of the 40 attempts with the skill ended without building anything.** All
twelve stopped at the design-context gate and asked:

> Before I build, I need three things: 1. **Audience** — Who will use this?
> What do they care about? 2. **Use case** — What's the one action the page
> should drive? …

Every brief already answered those questions — each has an "Audience:" line and
a list of what the page needs. The gate asked anyway. In an interactive session
that is one extra turn; anywhere nobody answers — `claude -p`, CI, an agent
running a batch — it is where the run ends. Here it cost 30% of the output.

Two things that might help: proceed when the brief already covers audience and
purpose, and in a non-interactive run, state the assumptions and build rather
than stop.

## 5. Separately: the skill does not activate unless it is named

Before the main round, the same four tasks with a prompt that only described
the work — "Read brief.md and build the landing page it describes…", which is
the first trigger in hallmark's description — activated the skill **0 times in
12**. The skill was installed, and the host listed it among its available skills;
the model read the brief, wrote `index.html`, and stopped. Named, it activated 40 of 40.

This is one model (`claude-haiku-4-5-20251001`), and I have seen the same
pattern on other design skills: when a request can be answered by writing a file
directly, it tends to be. So I would not read it as a problem with the
description in particular — but it means most users who do not type "hallmark"
will not get the effect in section 1.

## 6. Separately: the showcase pages and two of the literal rules

Not part of the comparison above. Before running anything, I checked my
patterns against the 18 example pages in `site/examples/`, to catch patterns
that were wrong — and two were, which I fixed. After that, two of the literal
rules still flag pages in the showcase:

| Rule | Showcase pages |
| --- | --- |
| italic words in headings (`SKILL.md` rule 6) | 8 / 18 — e.g. `wayfare` sets `h2 em { font-style: italic }` and `h3 { font-style: italic }` |
| pure `#fff` / `#000` | 7 / 18 — in the token files of the `custom-*` pages, `press-01`, `tally` |

These pages may predate rule 6. I mention it only because someone comparing
output against the showcase would get a baseline that is not zero.

## Caveats

- **One model.** A larger one may activate on organic requests or read the
  reference files; neither is measured here.
- **The checks cover a slice of what hallmark does.** Fourteen tells a pattern
  can see; "made, not generated" as a whole is not measured, and can't be
  without a judge.
- **28 and 40 pages per arm.** Enough to separate 100% from 50%; not enough to
  call smaller differences.
- **Claude Code 2.1.263, `acceptEdits`.**

Full report, with per-rule tables, the worst-case bound, the calibration and the
exact patterns:
https://github.com/ktlesr/skill-trigger-measurements/blob/master/reports/hallmark.ablation.md
