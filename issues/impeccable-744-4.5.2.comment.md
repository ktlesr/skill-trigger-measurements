Re-ran the same pinned case set (12 cases, `sha256:c820aafc…`) on 4.5.2 in
both permission modes, 120 attempts per mode, `claude-haiku-4-5`.

One change to the method. The host moved since September (Claude Code 2.1.302
now, plus a runner upgrade), and on the new host both versions activate less
often. So I re-measured 4.2.2 alongside 4.5.2 in the same session, chunks
interleaved. **The deltas below are 4.2.2 → 4.5.2 on the same host**, with
4.2.1 and the September 4.2.2 numbers as history.

## 1. Path failures: closed

Launcher calls that resolved the plugin root instead of the skill folder:

| | 4.2.1 | 4.2.2 | 4.2.2 (re-run) | 4.5.2 |
| --- | ---: | ---: | ---: | ---: |
| bypassPermissions | 11 / 57 | 1 / 56 | 0 / 26 | 2 / 36 |
| acceptEdits | 8 / 55 | 3 / 36 | 2 / 23 | 0 / 23 |

Noise around zero. The Setup wording from #750 holds.

## 2. PowerShell `.cmd` invocation: still open, and the rule is exact

| bypassPermissions, PowerShell launcher calls | without `&` | with `&` |
| --- | --- | --- |
| 4.2.2 (re-run) | 2 / 2 failed | 2 / 2 ran |
| 4.5.2 | **4 / 4 failed** | 2 / 3 ran (third used the plugin root) |

Totals for parser failures: 6/57 (4.2.1) → 4/56 (4.2.2) → 2/26 (re-run) → 4/36
(4.5.2). The error is always `Unexpected token 'context'`: a quoted path
followed by an argument is a string expression to PowerShell. One sentence in
Setup would do it: *in PowerShell, prefix the quoted path with the call
operator: `& "…/impeccable.cmd" context`.*

While re-checking the old records I found the same defect hiding in the
acceptEdits refusals: 5 of 55 (4.2.1) and 3 of 36 (4.2.2) "refusals" were
the host's PowerShell pre-parse rejecting `Unexpected token 'context'`. I'd
counted them as permission refusals before.

## 3. Craft-floor: closed where the launcher runs, total where it is refused

| craft-floor.md read before the first UI edit | 4.2.1 | 4.2.2 | 4.2.2 (re-run) | 4.5.2 |
| --- | --- | --- | --- | --- |
| bypassPermissions | 6 / 29 | 16 / 30 | 6 / 14 | **9 / 17** |
| acceptEdits | 0 / 28 | 0 / 32 | 0 / 18 | **0 / 21** |

bypassPermissions keeps the 4.2.2 gain (43% → 53%, inside noise).

Under acceptEdits the launcher is refused, and #756 shows a split result:

| acceptEdits, activations where every launcher call failed | 4.2.2 (re-run) | 4.5.2 |
| --- | ---: | ---: |
| activations | 19 | 21 |
| fixed sentence "Context loading did not run…" present | 0 | **21** |
| a failure message before the next tool call | 5 | **16** |
| then edited UI | 18 | 21 |
| …having read `reference/craft-floor.md` first | 0 | **0** |

The message works. "Follow applicable steps 2–3" doesn't. After the fallback
sentence the agent reads PRODUCT.md and project files and starts editing. In
acceptEdits it never opens any file under `reference/`, in any version. No
reads were refused either; none were attempted. A guess, not measured: the
fallback sentence says *project* context, and nothing in that paragraph names
`reference/craft-floor.md`. Naming the path in the fallback (for example,
"…then read reference/craft-floor.md before any UI edit") would be the obvious
thing to measure next.

## 4. Command-reference reads (bypassPermissions)

7 distinct references read on 4.5.2 vs 6 on the 4.2.2 re-run (27 vs 19 reads).
Routing still follows the Commands table: `new-work.md` and `init.md` for the
new-surface cases, and the new `mode-operate.md` / `mode-persuade.md` are
being reached. Most references are still never opened in these cases.

## Activation (for #375)

No skill effect: recall 38% → 44% (acceptEdits) and 35% → 41%
(bypassPermissions) on the same host, precision 100%, 0 false positives in 280
negative attempts. The host change is what moved it: `settings_rework` and
`empty_state` dropped to 0–2/10 for *both* versions.

The `document`-shaped completion case: 0/80 activations across all eight cells.
The base model writes DESIGN.md itself 70 times out of 80. `reference/document.md`
has now been opened 0 times in 960 measured attempts. I'll take that, with the
per-case table, to #375.

---

Full report with per-case tables, method and instrument validation:
<https://github.com/ktlesr/skill-trigger-measurements/blob/master/reports/impeccable.4.5.2.md>

Note: 4.6.0 shipped a few hours after your request. This is 4.5.2, pinned to
`skill-v4.5.2`.
