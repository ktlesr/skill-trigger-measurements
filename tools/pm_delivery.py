"""product-marketing delivery row: per arm and case, attempts that wrote any
file and attempts that wrote .agents/product-marketing.md.

Usage: python tools/pm_delivery.py <A.json> <B.json> [<C.json> ...]
"""
import json, sys

for i, p in enumerate(sys.argv[1:]):
    run = json.load(open(p, encoding="utf-8"))["run"]
    cells = []
    for c in run["cases"]:
        if ".product_marketing." not in c["caseId"]:
            continue
        ws = [[w.replace("\\", "/") for w in (a.get("env") or {}).get("writes") or []] for a in c["attempts"]]
        ctx = sum(1 for w in ws if any(x.endswith(".agents/product-marketing.md") for x in w))
        cells.append(f"{c['caseId'].rsplit('.', 1)[1]}: any file {sum(1 for w in ws if w)}/{len(ws)}, context file {ctx}/{len(ws)}")
    print(f"{chr(65 + i)} · claude-code {run['environment']['version']} · " + " · ".join(cells))
