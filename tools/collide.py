"""Collision matrix for co-installed skills, from assay run records.

Expected winner comes from the case id: collide.<skill>.<shape> (underscores
stand for hyphens). contested.* cases are reported, not scored.

Usage: python tools/collide.py <run.json> [...]
"""
import json, re, sys
from collections import Counter, defaultdict

NS = "marketing-skills:"
CTX = ".agents/product-marketing.md"


def expected(case_id):
    kind, skill = case_id.split(".")[:2]
    if kind in ("collide", "contested"):
        return kind, skill.replace("_", "-")
    return "negative", None


def attempt_facts(a):
    trace = a.get("trace") or []
    res = {e["callId"]: e for e in trace if e.get("kind") == "tool_result" and e.get("callId")}
    fired = [e["skill"][len(NS):] for e in trace
             if e.get("kind") == "skill_trigger" and str(e.get("skill", "")).startswith(NS)]
    # order from the trace, membership from assay's confirmed-activation list:
    # a refused activation leaves a skill_trigger event but is not a trigger
    confirmed = set((a.get("trigger") or {}).get("skills") or [])
    fired = [s for s in dict.fromkeys(fired) if NS + s in confirmed]
    ctx_seq = edit_seq = None
    for e in trace:
        if e.get("kind") != "tool_call":
            continue
        ok = not (res.get(e.get("id")) or {}).get("isError")
        blob = json.dumps(e.get("args") or {}).replace("\\\\", "/").replace("\\", "/")
        if e.get("tool") in ("Read", "Grep", "Glob") and CTX in blob and ok and ctx_seq is None:
            ctx_seq = e["seq"]
        if e.get("tool") in ("Edit", "Write", "MultiEdit") and ok and edit_seq is None:
            edit_seq = e["seq"]
    others = [s for s in confirmed if not s.startswith(NS)]   # host-bundled skills
    wrote = bool((a.get("env") or {}).get("writes"))
    return fired, ctx_seq, edit_seq, others, wrote


def analyse(runs):
    rows = defaultdict(list)                      # case -> [(fired, ctx, edit)]
    for r in runs:
        for c in r["cases"]:
            for a in c["attempts"]:
                rows[c["caseId"]].append(attempt_facts(a))
    return rows


def main(paths):
    runs = [json.load(open(p, encoding="utf-8"))["run"] for p in paths]
    rows = analyse(runs)
    matrix = defaultdict(Counter)
    print("## Per case\n")
    print("| Case | Expected | Attempts | First to fire | All that fired | Verdict |")
    print("| --- | --- | --- | --- | --- | --- |")
    for cid, atts in rows.items():
        kind, exp = expected(cid)
        first = Counter((f[0] if f else "(none)") for f, *_ in atts)
        every = Counter(s for f, *_ in atts for s in f)
        if kind == "collide":
            hits = first.get(exp, 0)
            verdict = f"{hits}/{len(atts)} expected won"
            for k, v in first.items():
                matrix[exp][k] += v
        elif kind == "contested":
            verdict = "contested, not scored"
        else:
            fp = sum(1 for f, *_ in atts if f)
            verdict = f"{fp}/{len(atts)} fired (should be 0)"
        fmt = lambda c: ", ".join(f"{k}×{v}" for k, v in c.most_common()) or "—"
        print(f"| `{cid}` | {exp or '—'} | {len(atts)} | {fmt(first)} | {fmt(every)} | {verdict} |")

    cols = sorted({k for r in matrix.values() for k in r})
    print("\n## Collision matrix (rows: expected, cols: first skill to fire)\n")
    print("| expected \\ fired | " + " | ".join(cols) + " |")
    print("| --- |" + " --- |" * len(cols))
    for exp in sorted(matrix):
        print(f"| **{exp}** | " + " | ".join(str(matrix[exp].get(c, "")) for c in cols) + " |")

    acts = [(f, c, e) for atts in rows.values() for f, c, e, *_ in atts if f]
    read = sum(1 for _, c, _ in acts if c is not None)
    first = sum(1 for _, c, e in acts if c is not None and (e is None or c < e))
    pm_skill = sum(1 for f, _, _ in acts if "product-marketing" in f)
    print("\n## product-marketing claim\n")
    print(f"- activations (any marketing skill fired): {len(acts)}")
    print(f"- read `{CTX}` at all: {read}")
    print(f"- read it before the first edit (or made no edit): {first}")
    print(f"- product-marketing skill itself fired in: {pm_skill}")
    non = [a for atts in rows.values() for a in atts if not a[0]]
    print(f"- control, attempts where no marketing skill fired: read it in {sum(1 for a in non if a[1] is not None)}/{len(non)}")

    host = Counter(s for atts in rows.values() for a in atts for s in a[3])
    print("\n## Host-bundled skills that fired\n")
    print(", ".join(f"`{k}`×{v}" for k, v in host.most_common()) or "none")
    silent = [(cid, a) for cid, atts in rows.items() if expected(cid)[0] != "negative" for a in atts if not a[0]]
    print(f"\n## Work done without any marketing skill\n")
    print(f"- positive attempts where no marketing skill fired: {len(silent)}")
    print(f"- of those, the agent still wrote files: {sum(1 for _, a in silent if a[4])}")


def demo():
    a = {"trigger": {"skills": [NS + "cro"]}, "trace": [
        {"kind": "skill_trigger", "skill": NS + "cro", "seq": 1},
        {"kind": "tool_call", "tool": "Read", "id": "r", "args": {"file_path": "x/.agents/product-marketing.md"}, "seq": 2},
        {"kind": "tool_result", "callId": "r", "seq": 3},
        {"kind": "tool_call", "tool": "Edit", "id": "e", "args": {"file_path": "i.html"}, "seq": 4},
        {"kind": "tool_result", "callId": "e", "seq": 5},
        {"kind": "skill_trigger", "skill": NS + "cro", "seq": 6},
    ]}
    assert attempt_facts(a)[:3] == (["cro"], 2, 4)
    assert expected("collide.copy_editing.x") == ("collide", "copy-editing")
    assert expected("trigger.negative.unrelated.q") == ("negative", None)


if __name__ == "__main__":
    demo()
    main(sys.argv[1:])


