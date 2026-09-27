"""Questions each attempt's final reply puts to the user, per case — the raw
material for the fork list in §11 of the phrase-binding report. The list itself
is a reading of this output: permission-only questions and question marks inside
drafted copy are dropped by hand.

Usage: python tools/fork_questions.py <run.json>
"""
import json, re, sys

PREAMBLE = "Base directory for this skill:"   # the Skill tool's, not the model's
run = json.load(open(sys.argv[1], encoding="utf-8"))["run"]
for c in run["cases"]:
    print(f"\n######## {c['caseId']}")
    for i, a in enumerate(c["attempts"]):
        msgs = [(e.get("text") or "").strip() for e in a.get("trace") or [] if e.get("kind") == "assistant_message"]
        reply = next((m for m in reversed(msgs) if m and not m.startswith(PREAMBLE)), "")
        qs = [q.strip() for q in re.findall(r"[^\n?]*\?", reply) if len(q.strip()) > 3]
        if qs:
            print(f"-- #{i} writes={len((a.get('env') or {}).get('writes') or [])}")
            for q in qs:
                print("   ?", q[:220])
