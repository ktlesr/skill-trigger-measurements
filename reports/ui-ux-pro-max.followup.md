# `ui-ux-pro-max` — follow-up: finding 1 is closed

A targeted re-check of one finding, not a re-measurement. No suite was run: the
whole skill directory changed by two files between the version measured and
upstream HEAD, and neither of them can move a routing number.

| | |
| --- | --- |
| Measured at | `nextlevelbuilder/ui-ux-pro-max-skill@f3ac195` — [report](ui-ux-pro-max.md) · [coverage](ui-ux-pro-max.coverage.md) · [issue](../issues/ui-ux-pro-max.md) |
| Fix | `314307f` — *fix(search): warn that `--stack` is ignored in `--design-system` mode (#484) (#487)* |
| Also checked at | `4aad058` (upstream HEAD); `search.py` is identical to `314307f` there |
| Checked | 2026-09-06, Python 3.11.5, Windows 11. No model, no host, no runner. |

**Which finding is "1".** The issue and the report number these differently, and
the fix commit refers to the issue's numbering (*"Closes #484 Finding 1"*):

| Issue | Report | Subject | Status |
| --- | --- | --- | --- |
| 1 | 4 | `--design-system` silently drops `--stack` | **closed** |
| 2 | part of 3 | `references/*.md` never opened | open, not re-measured |
| 3 | 3 | 82% of shipped files never reached | open — cheap part re-checked below |
| 4 | 1 + 2 | precision 100%, recall 50% | open, not re-measured |

---

## Finding 1 — closed

The three questions, answered from a shell.

```
python .claude/skills/ui-ux-pro-max/scripts/search.py \
  "platform engineer dashboard" --design-system -p Acme --stack nextjs
```

| | as measured (`f3ac195`) | fixed (`314307f`) |
| --- | --- | --- |
| stderr | *(empty)* | `note: --stack nextjs is ignored in --design-system mode; run a separate --stack query for stack-specific guidelines` |
| exit code | 0 | 0 |
| stdout | 8,005 B | 8,005 B, **byte-identical** |
| data files opened | `colors`, `landing`, `products`, `styles`, `typography`, `ui-reasoning` | the same six |
| stack file opened | **none** | **none** |

**1. Is there a warning now?** Yes, on stderr, naming the dropped value.

**2. Does the combination stay valid?** Yes. The flag is not rejected, the exit
code is still 0, and stdout is byte-identical to the pinned version. The fix is
purely additive: nothing that worked before behaves differently, and because the
note goes to stderr it cannot corrupt a caller parsing stdout.

**3. Is the stack file still not opened — does the warning tell the truth?**
Still not opened, so yes. Under a Python `open()` audit hook — the same technique
`tools/refcoverage.py` uses — the design-system query touches six data files and
no `data/stacks/*` file at all. The control confirms the path exists and is
simply not taken in this mode:

```
search.py "dashboard table density" --stack nextjs
  → opens data/stacks/nextjs.csv          (exit 0, no stderr)
```

So the warning says the true thing: `--stack` is accepted, and ignored.

**Scope of the fix.** Six lines in `search.py`, applied to all three shipped
copies (`.claude/skills/`, `cli/assets/`, `src/`), each with a 61-line regression
test. `SKILL.md` and its Query Contract are unchanged, so a reader of the docs
still is not told the modes are exclusive — but the tool now says so at the
moment it matters, which is the smaller of the two remedies the issue asked for
("a rejected flag, or one line of *note: --stack is ignored*").

---

## Finding 3, cheap part — still open, and slightly larger

The issue's easiest item was that the skill's own test suite installs alongside
it. It still does.

| | Files | Bytes |
| --- | --- | --- |
| `f3ac195` (as measured) | 26 | 305,992 |
| `4aad058` (HEAD) | 27 | 308,253 |

`scripts/tests/` and `scripts/validate_data.py` are present in all three shipped
layouts, and the CLI copies assets verbatim — `EXCLUDED_FILES` in
`cli/src/utils/extract.ts` is `['settings.local.json']` and nothing else.

Worth stating plainly rather than as a jab: the count went **up by one file**
because closing finding 1 added `test_design_system_stack.py`, which ships into
the installed skill along with the rest of the suite. The fix is right; the
packaging is what puts its test on every user's disk.

---

## Not re-measured

Findings 2, 3 and 4 are open. I am not claiming they are unchanged as a
measurement — I did not run one — but the grounds for not running one are
concrete:

```
git diff --stat f3ac195..4aad058 -- .claude/skills/ui-ux-pro-max
  scripts/search.py                    |  6 +++
  scripts/tests/test_design_system_stack.py | 61 +++++++++++++++++
  2 files changed, 67 insertions(+)
```

`SKILL.md`, `references/quick-reference.md`, `references/pro-rules.md` and
`data/charts.csv` are byte-identical to the measured version. Nothing in the
range touches what findings 2 and 4 are about, and finding 3's large groups
(2.09 MB of domain data, 477 KB of stack data) are untouched. Re-running 200
attempts against that diff would cost about $13 to reproduce numbers whose
inputs have not moved.

The one thing that would be worth re-measuring is not upstream's to fix: every
`search.py` invocation in the original runs was refused by the host permission
layer, which is why the coverage figure is an upper bound and why the completion
case could not be measured at all. That needs a run with the skill's shell access
granted, not a new skill version.

## Reproduce

```
git clone https://github.com/nextlevelbuilder/ui-ux-pro-max-skill && cd ui-ux-pro-max-skill
git checkout 314307f
python .claude/skills/ui-ux-pro-max/scripts/search.py \
  "platform engineer dashboard" --design-system -p Acme --stack nextjs
```

Stderr carries the note; stdout is unchanged. For the file-open check, run the
same argv under `sys.addaudithook` and filter `open` events to the skill
directory — the `replay()` function in `tools/refcoverage.py` does exactly this.

Method: <https://assayctl.dev/methodology>
