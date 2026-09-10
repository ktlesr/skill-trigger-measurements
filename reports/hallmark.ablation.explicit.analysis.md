## Trigger and output

| arm | attempts | hallmark fired | produced a page |
| --- | --- | --- | --- |
| A | 50 | 40/50 (80%, 67–89%) | 28/50 (56%, 42–69%) |
| B | 50 | 0/50 (0%, 0–7%) | 40/50 (80%, 67–89%) |

## Rulebook reads (references/*.md) and skills that fired

- A: reference reads attempted 3, succeeded 0, refused/failed 3; attempts that read anti-patterns.md or slop-test.md: 0/50
  files: —
  page attempts that called Skill("hallmark"): 40/40; calls that errored: 0
  skills fired: hallmark:hallmark×40, run×6
- B: reference reads attempted 0, succeeded 0, refused/failed 0; attempts that read anti-patterns.md or slop-test.md: 0/50
  files: —
  page attempts that called Skill("hallmark"): 11/40; calls that errored: 11 — e.g. "<tool_use_error>Unknown skill: hallmark</tool_use_error>"
  skills fired: none

## Pages that break each rule (among attempts that produced a page)

| rule | kind | A | B | intervals overlap? |
| --- | --- | --- | --- | --- |
| gradient_headline | literal | 0/28 (0%, 0–12%) | 1/40 (3%, 0–13%) | yes |
| pure_black_white | literal | 14/28 (50%, 33–67%) | 40/40 (100%, 91–100%) | **no** |
| transition_all | literal | 16/28 (57%, 39–73%) | 14/40 (35%, 22–50%) | yes |
| hover_scale | proxy | 1/28 (4%, 1–18%) | 7/40 (18%, 9–32%) | yes |
| z_index_9999 | literal | 0/28 (0%, 0–12%) | 0/40 (0%, 0–9%) | yes |
| width_100vw | literal | 0/28 (0%, 0–12%) | 0/40 (0%, 0–9%) | yes |
| emoji_icon | literal | 0/28 (0%, 0–12%) | 4/40 (10%, 4–23%) | yes |
| placeholder_names | literal | 0/28 (0%, 0–12%) | 0/40 (0%, 0–9%) | yes |
| italic_headers | literal | 0/28 (0%, 0–12%) | 0/40 (0%, 0–9%) | yes |
| purple_gradient | proxy | 0/28 (0%, 0–12%) | 1/40 (3%, 0–13%) | yes |
| inter_primary | proxy | 3/28 (11%, 4–27%) | 0/40 (0%, 0–9%) | yes |
| glassmorphism | proxy | 2/28 (7%, 2–23%) | 3/40 (8%, 3–20%) | yes |
| aurora_blob | proxy | 0/28 (0%, 0–12%) | 0/40 (0%, 0–9%) | yes |
| bounce_easing | proxy | 0/28 (0%, 0–12%) | 0/40 (0%, 0–9%) | yes |

## Any literal rule broken (page level)

- A: 22/28 (79%, 60–90%)
- B: 40/40 (100%, 91–100%)
- intervals overlap: **no**

## Rules broken per page

- A literal: mean 1.07 of 8; clean pages 6/28 (21%, 10–40%)
- A proxy: mean 0.21 of 6; clean pages 22/28 (79%, 60–90%)
- B literal: mean 1.48 of 8; clean pages 0/40 (0%, 0–9%)
- B proxy: mean 0.28 of 6; clean pages 30/40 (75%, 60–86%)

## Per case

| case | A fired · literal mean | B fired · literal mean |
| --- | --- | --- |
| `ablation.page.devtool` | 10/10 · 1.38 | 0/10 · 1.80 |
| `ablation.page.bakery` | 10/10 · 0.67 | 0/10 · 1.60 |
| `ablation.page.studio` | 10/10 · 1.25 | 0/10 · 1.30 |
| `ablation.page.event` | 10/10 · 0.83 | 0/10 · 1.20 |
| `trigger.negative.unrelated.slow_query` | 0/10 · 0.00 | 0/10 · 0.00 |
