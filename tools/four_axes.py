"""Four-axis analysis of impeccable measurement runs.

The maintainer on pbakaus/impeccable#744 asked for four things kept apart.
This tool keeps them apart, from the stored run records only:

  1. activation   - which case fired, how often
  2. launcher     - every launcher invocation, classified by outcome
  3. references   - which reference file was read in which case
  4. craft floor  - of the activations that edited UI, how many read
                    reference/craft-floor.md first

Plus a separate section for the `document`-shaped completion case, which is
coordinated with #375 and must not be pooled into the routing numbers.

Usage:
  python tools/four_axes.py <label>=<run.json>[,<run.json>...] [<label>=...]
"""

from __future__ import annotations

import json
import math
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

UI_EXT = (".tsx", ".jsx", ".ts", ".js", ".css", ".scss", ".html", ".vue", ".svelte", ".astro")
COMPLETION_CASE = "complete.persists_design_system"


def wilson(k: int, n: int) -> tuple[float, float]:
    if n == 0:
        return (0.0, 0.0)
    z = 1.959963985
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return (max(0.0, c - h), min(1.0, c + h))


def pct(k: int, n: int) -> str:
    if n == 0:
        return "n/a"
    lo, hi = wilson(k, n)
    return f"{100*k/n:.0f}% (N={n}, {100*lo:.0f}%-{100*hi:.0f}%)"


def load(paths: list[Path]) -> dict:
    """Pool several records into one measurement. Refuses to pool across pins."""
    runs = [json.loads(p.read_text(encoding="utf-8"))["run"] for p in paths]
    pins = {json.dumps(r["pins"], sort_keys=True) for r in runs}
    modes = {r["permissionMode"] for r in runs}
    if len(pins) != 1:
        raise SystemExit(f"refusing to pool: pins differ across {[p.name for p in paths]}")
    if len(modes) != 1:
        raise SystemExit(f"refusing to pool: permission modes differ: {modes}")
    cases: dict[str, list] = defaultdict(list)
    for r in runs:
        for c in r["cases"]:
            for a in c["attempts"]:
                cases[c["caseId"]].append((r["id"], c, a))
    return {
        "pins": runs[0]["pins"],
        "mode": runs[0]["permissionMode"],
        "records": [r["id"] for r in runs],
        "cases": cases,
        "expected": {c["caseId"]: c["expectedTrigger"] for r in runs for c in r["cases"]},
        "cost": sum(a["cost"]["usd"] for r in runs for c in r["cases"] for a in c["attempts"]),
        "wall": sum(a["latencyMs"] for r in runs for c in r["cases"] for a in c["attempts"]) / 60000,
        "calls": sum(1 for r in runs for c in r["cases"] for a in c["attempts"]
                     for e in (a.get("trace") or []) if e.get("kind") == "tool_call"),
    }


def results_by_call(attempt) -> dict[str, dict]:
    return {e["callId"]: e for e in (attempt.get("trace") or [])
            if e.get("kind") == "tool_result" and e.get("callId")}


# --------------------------------------------------------------- axis 1
def axis_activation(m) -> list[dict]:
    rows = []
    for case_id, items in m["cases"].items():
        fired = sum(1 for _r, _c, a in items if (a.get("trigger") or {}).get("triggered") is True)
        unknown = sum(1 for _r, _c, a in items if (a.get("trigger") or {}).get("triggered") is None
                      or not (a.get("trigger") or {}).get("available", True))
        refused = sum(1 for _r, _c, a in items if (a.get("trigger") or {}).get("refused"))
        rows.append({"case": case_id, "expected": m["expected"][case_id],
                     "n": len(items), "fired": fired, "unknown": unknown, "refused": refused})
    return rows


# --------------------------------------------------------------- axis 2
LAUNCHER = re.compile(r"impeccable(\.cmd)?[\"']?(\s|$)")


def launcher_calls(m):
    """Every shell call that names the launcher, with its outcome."""
    out = []
    for case_id, items in m["cases"].items():
        for _rid, _c, a in items:
            res = results_by_call(a)
            for e in (a.get("trace") or []):
                if e.get("kind") != "tool_call" or e.get("tool") not in ("Bash", "PowerShell"):
                    continue
                cmd = str((e.get("args") or {}).get("command") or "")
                norm = cmd.replace("\\", "/")
                if not re.search(r"/scripts/impeccable(\.cmd)?", norm):
                    continue
                verb = None
                mm = re.search(r"/scripts/impeccable(?:\.cmd)?[\"']?\s+([a-z-]+)", norm)
                if mm:
                    verb = mm.group(1)
                r = res.get(e.get("id")) or {}
                err = str(r.get("error") or "")
                # `detect` exits non-zero *by design* when it finds antipatterns
                # and prints its findings as JSON. That is the engine working,
                # not a failure, and counting it as one overstates the defect.
                body = err.lstrip()
                by_design = (verb == "detect" and ("antipattern" in err or body[:1] in "[{"))
                if not r.get("isError") or by_design:
                    outcome = "ran"
                elif r.get("refusal"):
                    outcome = "refused by the permission layer"
                elif "fatal error - add_item" in err:
                    outcome = "host shell broken (Git bash)"
                elif ("Unexpected token" in err or "ParserError" in err
                      or "syntax error near unexpected token" in err):
                    outcome = "failed: parser / quoting"
                elif ("No such file or directory" in err or "is not recognized" in err
                      or "cannot find path" in err.lower() or "ObjectNotFound" in err):
                    outcome = "failed: path does not exist"
                elif "no engine binary found" in err:
                    outcome = "failed: no engine binary"
                else:
                    outcome = "failed: other"
                # which base directory did the model resolve?
                if "${CLAUDE_SKILL_DIR}" in cmd or "$CLAUDE_SKILL_DIR" in cmd:
                    base = "literal ${CLAUDE_SKILL_DIR}, unexpanded"
                elif "<skill-base-dir>" in cmd:
                    base = "literal <skill-base-dir>, unexpanded"
                elif re.search(r"/skills/impeccable/scripts/impeccable", norm):
                    base = "correct (skill dir)"
                elif re.search(r"/scripts/impeccable", norm):
                    base = "wrong (plugin root)"
                else:
                    base = "other"
                out.append({"case": case_id, "tool": e["tool"], "verb": verb,
                            "outcome": outcome, "base": base, "cmd": cmd, "err": err})
    return out


def launcher_discipline(m):
    """Per activation: was the launcher attempted, how often, and — when every
    attempt failed — did the agent tell the user, as 4.2.2 SKILL.md now
    instructs under "Launcher unavailable"?"""
    acts = attempted = calls = all_failed = disclosed = 0
    # A disclosure is a sentence that names the launcher / context step AND says
    # something went wrong with it. Sentence-scoped so the two halves have to
    # belong together; a narrow phrase list under-counted on a first pass.
    SUBJ = re.compile(r"launcher|impeccable context|context (?:loader|loading|setup|step|command|script|initialization|initialisation)|setup (?:step|command|script)|\bsetup\b", re.I)
    BAD = re.compile(r"refus|denied|deny|block|unavailab|fail|could ?n.t|couldn.t|did ?n.t|does not|do not|not run|cannot|can.t|need(?:s|ed)? (?:permission|approval)|require(?:s|d)? (?:permission|approval)|no permission|permission|approval|skip|without|unable|encountered an issue|restriction|hitting|error", re.I)

    def discloses(text: str) -> bool:
        for sent in re.split(r"(?<=[.!?:\n])\s+", text or ""):
            if SUBJ.search(sent) and BAD.search(sent):
                return True
        return False
    for case_id, items in m["cases"].items():
        for _rid, _c, a in items:
            if (a.get("trigger") or {}).get("triggered") is not True:
                continue
            acts += 1
            res = results_by_call(a)
            mine = []
            for e in (a.get("trace") or []):
                if e.get("kind") != "tool_call" or e.get("tool") not in ("Bash", "PowerShell"):
                    continue
                norm = str((e.get("args") or {}).get("command") or "").replace("\\", "/")
                if re.search(r"/scripts/impeccable(\.cmd)?", norm):
                    mine.append((e.get("seq"), res.get(e.get("id")) or {}))
            if not mine:
                continue
            attempted += 1
            calls += len(mine)
            if all(r.get("isError") for _s, r in mine):
                all_failed += 1
                last = max(s for s, _r in mine)
                if any(e.get("kind") == "assistant_message" and e.get("seq", 0) > last
                       and discloses(str(e.get("text") or ""))
                       for e in (a.get("trace") or [])):
                    disclosed += 1
    return {"activations": acts, "attempted the launcher": attempted,
            "launcher calls": calls,
            "calls per activation": round(calls / acts, 2) if acts else 0,
            "activations where every call failed": all_failed,
            "of those, told the user": disclosed}


# --------------------------------------------------------------- axis 3
REF = re.compile(r"reference/(degraded/)?([a-z0-9_.-]+\.md)", re.I)


def reference_reads(m):
    hits = defaultdict(Counter)   # file -> Counter(case)
    for case_id, items in m["cases"].items():
        for _rid, _c, a in items:
            res = results_by_call(a)
            for e in (a.get("trace") or []):
                if e.get("kind") != "tool_call":
                    continue
                if e.get("tool") not in ("Read", "Grep", "Glob"):
                    continue
                blob = json.dumps(e.get("args") or {}).replace("\\\\", "/").replace("\\", "/")
                mm = REF.search(blob)
                if not mm:
                    continue
                r = res.get(e.get("id")) or {}
                if r.get("isError"):
                    continue          # a refused read opens nothing
                name = (mm.group(1) or "") + mm.group(2)
                hits[name][case_id] += 1
    return hits


# --------------------------------------------------------------- axis 4
def craft_floor(m):
    """Per activation: did it edit UI, and did craft-floor.md come first?"""
    edited = 0
    floor_first = 0
    floor_after = 0
    per_case = defaultdict(lambda: [0, 0])
    for case_id, items in m["cases"].items():
        for _rid, _c, a in items:
            if (a.get("trigger") or {}).get("triggered") is not True:
                continue
            res = results_by_call(a)
            first_edit = None
            floor_seq = None
            for e in (a.get("trace") or []):
                if e.get("kind") != "tool_call":
                    continue
                blob = json.dumps(e.get("args") or {}).replace("\\\\", "/").replace("\\", "/")
                r = res.get(e.get("id")) or {}
                if e.get("tool") in ("Edit", "Write", "MultiEdit", "NotebookEdit"):
                    path = str((e.get("args") or {}).get("file_path") or "")
                    if path.lower().endswith(UI_EXT) and not r.get("isError"):
                        if first_edit is None:
                            first_edit = e.get("seq")
                if e.get("tool") in ("Read", "Grep", "Glob") and "craft-floor.md" in blob:
                    if not r.get("isError") and floor_seq is None:
                        floor_seq = e.get("seq")
            if first_edit is None:
                continue
            edited += 1
            per_case[case_id][0] += 1
            if floor_seq is not None and floor_seq < first_edit:
                floor_first += 1
                per_case[case_id][1] += 1
            elif floor_seq is not None:
                floor_after += 1
    return {"edited": edited, "first": floor_first, "after": floor_after, "per_case": dict(per_case)}


# ------------------------------------------------------- completion case
def completion(m):
    items = m["cases"].get(COMPLETION_CASE, [])
    fired = doc_md = design_md = refs = 0
    for _rid, _c, a in items:
        if (a.get("trigger") or {}).get("triggered") is True:
            fired += 1
        writes = (a.get("env") or {}).get("writes") or []
        if any(Path(w).name.upper() == "DESIGN.MD" for w in writes):
            design_md += 1
        res = results_by_call(a)
        saw_doc = saw_ref = False
        for e in (a.get("trace") or []):
            if e.get("kind") != "tool_call" or e.get("tool") not in ("Read", "Grep", "Glob"):
                continue
            blob = json.dumps(e.get("args") or {}).replace("\\\\", "/").replace("\\", "/")
            if (res.get(e.get("id")) or {}).get("isError"):
                continue
            if "reference/document.md" in blob:
                saw_doc = True
            if REF.search(blob):
                saw_ref = True
        doc_md += saw_doc
        refs += saw_ref
    return {"n": len(items), "fired": fired, "design_md": design_md,
            "document_md": doc_md, "any_reference": refs}


def main() -> int:
    if len(sys.argv) < 2:
        print(__doc__)
        return 2
    groups = {}
    for arg in sys.argv[1:]:
        label, _, files = arg.partition("=")
        groups[label] = load([Path(f) for f in files.split(",")])

    for label, m in groups.items():
        print(f"\n{'='*72}\n{label}  —  mode {m['mode']}  —  {len(m['records'])} record(s)\n{'='*72}")
        print(f"skillHash       {m['pins']['skillHash']}")
        print(f"suiteHash       {m['pins']['suiteHash']}")
        print(f"environmentHash {m['pins']['environmentHash']}")
        print(f"model           {m['pins']['model']}")
        print(f"records         {', '.join(m['records'])}")
        n_all = sum(len(v) for v in m["cases"].values())
        print(f"attempts {n_all} · tool calls {m['calls']} · ${m['cost']:.2f} · {m['wall']:.1f} min")

        print("\n--- AXIS 1: activation ---")
        rows = axis_activation(m)
        tp = sum(r["fired"] for r in rows if r["expected"])
        fn = sum(r["n"] - r["fired"] - r["unknown"] for r in rows if r["expected"])
        fp = sum(r["fired"] for r in rows if not r["expected"])
        tn = sum(r["n"] - r["fired"] - r["unknown"] for r in rows if not r["expected"])
        unk = sum(r["unknown"] for r in rows)
        for r in sorted(rows, key=lambda r: (not r["expected"], r["case"])):
            print(f"  {r['case']:<52} {r['fired']:>3}/{r['n']:<3} "
                  f"expect={'fire ' if r['expected'] else 'quiet'} unknown={r['unknown']}")
        print(f"  TP={tp} FN={fn} FP={fp} TN={tn} unknown={unk}")
        print(f"  precision {pct(tp, tp+fp)}")
        print(f"  recall    {pct(tp, tp+fn)}")

        print("\n--- AXIS 2: launcher path and execution ---")
        lc = launcher_calls(m)
        print(f"  invocations naming the launcher: {len(lc)}")
        for k, v in Counter(x["outcome"] for x in lc).most_common():
            print(f"    {k:<38} {v}")
        print("  base directory resolved:")
        for k, v in Counter(x["base"] for x in lc).most_common():
            print(f"    {k:<38} {v}")
        print("  by tool:")
        for k, v in Counter(x["tool"] for x in lc).most_common():
            print(f"    {k:<38} {v}")
        print("  verbs:")
        for k, v in Counter(str(x["verb"]) for x in lc).most_common():
            print(f"    {k:<38} {v}")
        seen = set()
        print("  distinct error texts:")
        for x in lc:
            if x["err"] and x["err"][:110] not in seen:
                seen.add(x["err"][:110])
                print(f"    [{x['outcome']}] {x['err'][:220]}")

        print("\n  launcher discipline (4.2.2 'Launcher unavailable' instruction):")
        for k, v in launcher_discipline(m).items():
            print(f"    {k:<38} {v}")

        print("\n--- AXIS 3: command-reference reads ---")
        hits = reference_reads(m)
        total = sum(sum(c.values()) for c in hits.values())
        print(f"  distinct reference files read: {len(hits)} · total reads: {total}")
        for name, cases in sorted(hits.items(), key=lambda kv: -sum(kv[1].values())):
            per = ", ".join(f"{c.split('.')[-1]}×{n}" for c, n in cases.most_common())
            print(f"    {name:<28} {sum(cases.values()):>3}   {per}")

        print("\n--- AXIS 4: craft-floor before a UI edit ---")
        cf = craft_floor(m)
        print(f"  activations that edited UI:        {cf['edited']}")
        print(f"  of those, read craft-floor first:  {cf['first']}  ({pct(cf['first'], cf['edited'])})")
        print(f"  read it only after the first edit: {cf['after']}")
        for c, (n, k) in sorted(cf["per_case"].items()):
            print(f"    {c:<52} {k}/{n}")

        print("\n--- completion case (document-shaped, coordinate with #375) ---")
        cp = completion(m)
        for k, v in cp.items():
            print(f"  {k:<16} {v}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())






