"""Arm-by-arm comparison of collision runs: arm A with a phrase-binding table
in an ancestor CLAUDE.md, arm B without, arm C with the table plus a standing
default (act unless the step must block), arms D and E with output-format rules
(scored in slot.mjs). Per-attempt facts come from collide.py.

Usage: python tools/phrase_binding.py <A.json> <B.json> [<C.json> ...]
Arms are labelled A, B, C… by position; two arguments reproduce the two-arm run.
"""
import json, re, sys
from collections import Counter, defaultdict
from collide import NS, attempt_facts, expected
from four_axes import wilson

NEVER = ["signup", "popups", "paywalls", "onboarding", "copy-editing", "programmatic-seo", "product-marketing"]


def facts(run):
    out = []                                   # (case, kind, expected, attempt, fired, edit_seq, wrote)
    for c in run["cases"]:
        kind, exp = expected(c["caseId"])
        for a in c["attempts"]:
            fired, _, edit_seq, _, wrote = attempt_facts(a)
            out.append((c["caseId"], kind, exp, a, fired, edit_seq, wrote))
    return out


def iv(k, n):
    lo, hi = wilson(k, n)
    return f"{k}/{n} ({100*lo:.0f}–{100*hi:.0f}%)"


def overlap(a, b):
    (alo, ahi), (blo, bhi) = wilson(*a), wilson(*b)
    return ahi >= blo and bhi >= alo


ACTION = {
    "collide.signup.registration_form", "collide.cro.lead_form", "collide.popups.exit_modal_wording",
    "collide.paywalls.limit_screen", "collide.onboarding.first_session", "collide.copy_editing.tighten_paragraph",
    "collide.ai_seo.cited", "collide.programmatic_seo.integration_pages", "collide.schema.star_ratings",
    "collide.product_marketing.positioning",
}


def skill_dir_refusals(a):
    res = {e["callId"]: e for e in a.get("trace") or [] if e.get("kind") == "tool_result" and e.get("callId")}
    return [e for e in a.get("trace") or [] if e.get("kind") == "tool_call" and "assay-skill-" in json.dumps(e.get("args") or {})
            and (res.get(e["id"]) or {}).get("isError")]


def first_skill_seq(a):
    confirmed = set((a.get("trigger") or {}).get("skills") or [])
    return next((e["seq"] for e in a.get("trace") or []
                 if e.get("kind") == "skill_trigger" and e.get("skill") in confirmed and e["skill"].startswith(NS)), None)


FORK = re.compile(r"\b(fork|defaults?|defaulted|defaulting|assum\w+|chose|choosing|chosen|proceed\w*|going with|opted|opting|took the|taking the)\b", re.I)


# Skill aracının kendi önsözü modelin çıktısı değil; kuralın istediği satır onun
# arkasında geliyor.
PREAMBLE = "Base directory for this skill:"


def opening_lines(a):
    """Her asistan mesajının ilk dolu satırı, makine önsözü atlanarak."""
    out = []
    for e in a.get("trace") or []:
        if e.get("kind") != "assistant_message":
            continue
        text = (e.get("text") or "").strip()
        if not text or text.startswith(PREAMBLE):
            continue
        out.append(next(l.strip() for l in text.splitlines() if l.strip()))
    return out


def first_line(a):
    """Modelin kendi çıktısının ilk satırı — kuralın tek satırı istediği yer."""
    lines = opening_lines(a)
    return lines[0] if lines else ""


def fork_line(a):
    """Açılış satırı bir seçim ilan ediyor mu. Temkinli: başlık uzunluğunda tek
    satır ve bir seçimi adlandıran bir sözcük."""
    line = first_line(a)
    return bool(line) and len(line) <= 300 and bool(FORK.search(line))


def fork_anywhere(a):
    """Kural 'çıktının başına' diyor; model onu ilk mesaj yerine bir sonrakinin
    başına koyabiliyor. İkinci, daha geniş ölçü."""
    return any(len(l) <= 300 and FORK.search(l) for l in opening_lines(a))


def final_text(a):
    msgs = [e.get("text", "") for e in a.get("trace") or [] if e.get("kind") == "assistant_message"]
    return (msgs[-1] if msgs else "").strip()


def claude_md_calls(a):
    res = {e["callId"]: e for e in a.get("trace") or [] if e.get("kind") == "tool_result" and e.get("callId")}
    return [(e["tool"], bool((res.get(e["id"]) or {}).get("isError")))
            for e in a.get("trace") or []
            if e.get("kind") == "tool_call" and "CLAUDE.md" in json.dumps(e.get("args") or {})]


def main(*paths):
    arms = [chr(ord("A") + i) for i in range(len(paths))]
    runs = {arm: json.load(open(p, encoding="utf-8"))["run"] for arm, p in zip(arms, paths)}
    F = {arm: facts(r) for arm, r in runs.items()}

    print("## Runs\n")
    for arm, r in runs.items():
        unknown = sum(1 for x in F[arm] if not (x[3].get("trigger") or {}).get("available"))
        usd = sum((x[3].get("cost") or {}).get("usd", 0) for x in F[arm])
        print(f"- **{arm}** `{r['id']}` · assay {r['assayVersion']} · claude-code {r['environment']['version']} · "
              f"{len(F[arm])} attempts · {unknown} unreadable · ${usd:.2f} · suite `{r['pins']['suiteHash'][:15]}…` · "
              f"skill `{r['pins']['skillHash'][:15]}…` · env `{r['pins']['environmentHash'][:15]}…`")

    # matrices
    mats = {arm: defaultdict(Counter) for arm in F}
    for arm in F:
        for cid, kind, exp, a, fired, *_ in F[arm]:
            if kind == "collide":
                mats[arm][exp][fired[0] if fired else "none"] += 1
    cols = ["none"] + sorted({k for m in mats.values() for r in m.values() for k in r} - {"none"})
    rows = sorted({e for m in mats.values() for e in m})
    legend = " · ".join(arms)
    print(f"\n## Activation matrices (rows: expected, cols: first marketing skill to fire; cell = {legend})\n")
    print("| expected \\ fired | " + " | ".join(f"`{c}`" if c != "none" else "none" for c in cols) + " |")
    print("| --- |" + " --- |" * len(cols))
    for e in rows:
        cells = []
        for c in cols:
            vals = [mats[arm][e].get(c, 0) for arm in arms]
            cells.append("" if not any(vals) else " · ".join(str(v) for v in vals))
        print(f"| `{e}` | " + " | ".join(cells) + " |")

    # per-skill win rate
    print("\n## Win rate per skill (own cases; first marketing skill to fire = expected). 95% Wilson.\n")
    print("| skill | " + " | ".join(arms) + " | A vs B |")
    print("| --- |" + " --- |" * (len(arms) + 1))
    win = {}
    for e in rows:
        win[e] = {arm: (mats[arm][e].get(e, 0), sum(mats[arm][e].values())) for arm in F}
        sep = "overlap" if overlap(win[e]["A"], win[e]["B"]) else "**separate**"
        cells = " | ".join(iv(*win[e][arm]) for arm in arms)
        print(f"| `{e}`{' ·' if e in NEVER else ''} | {cells} | {sep} |")
    cont = {arm: [(x[4][0] if x[4] else "none") for x in F[arm] if x[1] == "contested"] for arm in F}
    print(f"\n- contested headline case (copywriting or copy-editing accepted): "
          + " · ".join(f"{arm} {dict(Counter(v))}" for arm, v in cont.items()))

    pooled = {arm: (sum(win[e][arm][0] for e in NEVER), sum(win[e][arm][1] for e in NEVER)) for arm in F}
    allpos = {arm: (sum(w[arm][0] for w in win.values()), sum(w[arm][1] for w in win.values())) for arm in F}
    print("\n## Pooled\n")
    print("- the 7 skills that never fired in the v2 full run: "
          + " · ".join(f"{arm} {iv(*pooled[arm])}" for arm in arms)
          + f" · A vs B {'overlap' if overlap(pooled['A'], pooled['B']) else '**separate**'}")
    print("- all 16 scored cases: "
          + " · ".join(f"{arm} {iv(*allpos[arm])}" for arm in arms)
          + f" · A vs B {'overlap' if overlap(allpos['A'], allpos['B']) else '**separate**'}")
    for arm in F:
        acts = [x for x in F[arm] if x[1] == "collide" and x[4]]
        wrong = [(x[0], x[4][0]) for x in acts if x[4][0] != x[2]]
        print(f"- {arm}: {len(acts)} activations on scored cases, {len(wrong)} reached another skill {wrong or ''}")

    print("\n## Edit-shaped bypass (scored cases: no marketing skill fired, files written anyway)\n")
    for arm in F:
        pos = [x for x in F[arm] if x[1] == "collide"]
        silent = [x for x in pos if not x[4]]
        byp = [x for x in silent if x[6]]
        edit_first = [x for x in pos if x[4] and x[5] is not None and x[5] < first_skill_seq(x[3])]
        print(f"- {arm}: bypass {iv(len(byp), len(pos))} of scored attempts; "
              f"{len(silent)} silent, {len(byp)} of them wrote files; "
              f"{len(edit_first)} activations came after the first edit")
    bA = sum(1 for x in F['A'] if x[1] == 'collide' and not x[4] and x[6])
    bB = sum(1 for x in F['B'] if x[1] == 'collide' and not x[4] and x[6])
    nA = sum(1 for x in F['A'] if x[1] == 'collide'); nB = sum(1 for x in F['B'] if x[1] == 'collide')
    print(f"- intervals: {'overlap' if overlap((bA, nA), (bB, nB)) else '**separate**'}")

    # A "?" in the last message was tried as an asked-instead-of-acted signal and
    # dropped: read by hand, it missed "Please share: …" requests. Answer cases
    # are classified by reading the replies (printed at the end).
    # Action cases ask for a change in the workspace, so a written file is what
    # completion looks like. Answer cases can be finished in the reply; they are
    # read by hand instead.
    print("\n## Action cases (the prompt asks for a change): attempts that wrote files\n")
    for arm in F:
        act = [x for x in F[arm] if x[0] in ACTION]
        print(f"- {arm}: {iv(sum(1 for x in act if x[6]), len(act))}")
    counts = {a: (sum(1 for x in F[a] if x[0] in ACTION and x[6]), sum(1 for x in F[a] if x[0] in ACTION)) for a in arms}
    for i, a in enumerate(arms):
        for b in arms[i + 1:]:
            print(f"- {a} vs {b}: {'overlap' if overlap(counts[a], counts[b]) else '**separate**'}")
    print("\n### Action cases, case by case: attempts that wrote files\n")
    print("| case | " + " | ".join(arms) + " |")
    print("| --- |" + " --- |" * len(arms))
    for cid in sorted(ACTION):
        row = [str(sum(1 for x in F[a] if x[0] == cid and x[6])) for a in arms]
        print(f"| `{cid}` | " + " | ".join(row) + " |")

    print("\n## Reads refused because the path was resolved against the skill's own directory\n")
    for arm in F:
        n = sum(1 for x in F[arm] if skill_dir_refusals(x[3]))
        print(f"- {arm}: {n} attempts")

    print("\n## product-marketing cases: where the positioning went\n")
    for arm in F:
        w = Counter()
        for x in F[arm]:
            if x[2] == "product-marketing":
                files = [p.replace("\\", "/") for p in (x[3].get("env") or {}).get("writes") or []]
                w[", ".join(sorted(files)) or "(nothing written)"] += 1
        print(f"- {arm}: " + "; ".join(f"{k} ×{v}" for k, v in w.most_common()))

    print("\n## Negatives (any marketing skill fired)\n")
    for arm in F:
        neg = [x for x in F[arm] if x[1] == "negative"]
        print(f"- {arm}: {sum(1 for x in neg if x[4])}/{len(neg)} " + str([(x[0], x[4]) for x in neg if x[4]] or ""))

    print("\n## CLAUDE.md touched by the agent\n")
    for arm in F:
        hits = [(x[0], claude_md_calls(x[3])) for x in F[arm] if claude_md_calls(x[3])]
        print(f"- {arm}: {len(hits)} attempts " + "; ".join(f"`{c}` {t}" for c, t in hits))

    # ~/.claude/CLAUDE.md names only graphify; the fixture product is Meterly.
    print("\n## Host CLAUDE.md leak (attempts whose trace mentions `graphify`)\n")
    for arm in F:
        n = sum(1 for x in F[arm] if "graphify" in json.dumps(x[3].get("trace") or []).lower())
        print(f"- {arm}: {n}/{len(F[arm])}")

    print("\n## Opening line names the fork taken (arm C's standing default)\n")
    for arm in arms:
        scored = [x for x in F[arm] if x[1] != "negative"]
        print(f"- {arm}: first line of the first output {iv(sum(1 for x in scored if fork_line(x[3])), len(scored))}"
              f" · first line of any message {iv(sum(1 for x in scored if fork_anywhere(x[3])), len(scored))}")
    print("\n### Opening lines, for reading by hand\n")
    for arm in arms:
        for x in F[arm]:
            if x[1] != "negative":
                print(f"- {arm} `{x[0]}` fork={'Y' if fork_line(x[3]) else 'n'}: {first_line(x[3])[:200]}")

    print("\n## Attempts that wrote nothing — final message, for reading by hand\n")
    for arm in F:
        for x in F[arm]:
            if not x[6] and x[1] != "negative":
                t = final_text(x[3]).replace("\n", " ")
                print(f"- {arm} `{x[0]}` fired={x[4] or '—'}: {t[:220]}")


def demo():
    assert overlap((0, 3), (3, 3))            # n=3 can never separate
    assert not overlap((0, 6), (6, 6))
    assert not overlap((0, 10), (7, 10))


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    demo()
    main(*sys.argv[1:])
