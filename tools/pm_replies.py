"""Dump each product-marketing attempt for hand scoring: which skill fired,
whether .agents/product-marketing.md was written, the pivot-reason field and the
newest changelog line from the last write, and the reply after it.

Usage: python tools/pm_replies.py <run.json> [case-suffix ...]   (default: icp positioning)
"""
import json, re, sys

FIELD = "What changed from the current positioning, and why"
run = json.load(open(sys.argv[1], encoding="utf-8"))["run"]
wanted = sys.argv[2:] or ["icp", "positioning"]

for c in run["cases"]:
    name = c["caseId"].rsplit(".", 1)[1]
    if ".product_marketing." not in c["caseId"] or name not in wanted:
        continue
    for a in c["attempts"]:
        fired = [t["skill"].split(":")[-1] for t in a["trace"] if t["kind"] == "skill_trigger"]
        doc, last = None, -1
        for i, t in enumerate(a["trace"]):
            p = str((t.get("args") or {}).get("file_path", "")).replace("\\", "/")
            if t["kind"] == "tool_call" and t["tool"] in ("Write", "Edit") and p.endswith(".agents/product-marketing.md"):
                doc = t["args"].get("content") or t["args"].get("new_string") or ""
                last = i
        reply = "\n".join(t["text"] for t in a["trace"][last + 1:] if t["kind"] == "assistant_message"
                          and not t["text"].startswith("Base directory for this skill"))
        print(f"===== {name} #{a['index']}  fired={fired or '-'}  wrote={'yes' if last >= 0 else 'no'}")
        if doc is not None:
            m = re.search(re.escape(FIELD) + r":\*\*(.*)", doc)
            print("FIELD:", m.group(1).strip() if m else "(field absent)")
            cl = re.search(r"## Changelog.*?\n- (v\d.*)", doc, re.S)
            print("CHANGELOG:", cl.group(1).strip() if cl else "(none)")
        print("REPLY:", reply.strip() or "(none)")
