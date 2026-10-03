"""Fork detector without self-report: do the ten attempts of one case produce
different things? Per attempt, the output is what it left behind: the files it
wrote (rebuilt from the fixture plus its Write/Edit calls), or, if it wrote
nothing, its final reply. Per case, three spreads over the ten outputs:

- files:  how many distinct sets of written files the writers chose
- struct: for the most-written file, the mean pairwise Jaccard distance between
          the attempts' structural signatures (HTML: tag plus name/id/type/for of
          every element, text ignored; Markdown: the heading set). Wording does
          not move it; adding, removing or renaming a field, section or control does.
- text:   mean pairwise Jaccard distance between content-word sets of the
          outputs (added lines for writers, the reply otherwise). Wording moves it
          too, so it is only read relative to other cases.

Usage: python tools/spread.py <run.json> [fixture dir]   (default fixtures/marketing-site)
       python tools/spread.py --validate <run.json>   text spread against the §11.1 fork list
"""
import difflib, itertools, json, re, sys
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path

PREAMBLE = "Base directory for this skill:"
STOP = set("""this that with your from have will they them their there what when which while would could should
about into than then also just only more most some such very each other these those been were where here
make made does doesn like want need using used use""".split())


def rel(path):
    p = path.replace("\\", "/")
    m = re.search(r"assay-attempt-[^/]+/(.*)$", p)
    return m.group(1) if m else None          # outside the workdir (host memory etc.)


def rebuild(attempt, fixture):
    """Final content of every file the attempt wrote through Write/Edit."""
    results = {e["callId"]: e for e in attempt.get("trace") or [] if e.get("kind") == "tool_result" and e.get("callId")}
    files = {}
    for e in attempt.get("trace") or []:
        if e.get("kind") != "tool_call" or e.get("tool") not in ("Write", "Edit"):
            continue
        if (results.get(e["id"]) or {}).get("isError"):
            continue
        a = e.get("args") or {}
        r = rel(a.get("file_path", ""))
        if r is None:
            continue
        if e["tool"] == "Write":
            files[r] = a.get("content", "")
        else:
            cur = files.get(r)
            if cur is None:
                f = fixture / r
                cur = f.read_text(encoding="utf-8") if f.exists() else ""
            old, new = a.get("old_string", ""), a.get("new_string", "")
            files[r] = cur.replace(old, new) if a.get("replace_all") else cur.replace(old, new, 1)
    return files


class Sig(HTMLParser):
    def __init__(self):
        super().__init__()
        self.sig = set()

    def handle_starttag(self, tag, attrs):
        d = dict(attrs)
        self.sig.add((tag,) + tuple(f"{k}={d[k]}" for k in ("name", "id", "type", "for") if d.get(k)))


def signature(path, text):
    if path.endswith((".html", ".htm", ".jsx", ".tsx")):
        p = Sig()
        p.feed(text)
        return p.sig
    return {l.strip().lower() for l in text.splitlines() if l.lstrip().startswith("#")}


def words(text):
    return {w for w in re.findall(r"[a-z]{4,}", text.lower()) if w not in STOP}


def added(path, text, fixture):
    f = fixture / path
    base = f.read_text(encoding="utf-8").splitlines() if f.exists() else []
    return "\n".join(l[2:] for l in difflib.ndiff(base, text.splitlines()) if l.startswith("+ "))


def jdist(sets):
    pairs = list(itertools.combinations(sets, 2))
    if not pairs:
        return None
    return sum(1 - (len(a & b) / len(a | b) if a | b else 1) for a, b in pairs) / len(pairs)


def case_spread(case, fixture):
    outs, filesets, sigs = [], [], Counter()
    rebuilt = []
    for a in case["attempts"]:
        writes = sorted({w.replace("\\", "/") for w in (a.get("env") or {}).get("writes") or []
                         if not re.match(r"^[A-Za-z]:|^/", w)})      # absolute = outside the workdir
        files = rebuild(a, fixture)
        rebuilt.append(files)
        if writes:
            filesets.append(tuple(writes))
            outs.append(words("\n".join(added(p, t, fixture) for p, t in files.items())))
            sigs.update(files.keys())
        else:
            msgs = [(e.get("text") or "").strip() for e in a.get("trace") or [] if e.get("kind") == "assistant_message"]
            reply = next((m for m in reversed(msgs) if m and not m.startswith(PREAMBLE)), "")
            outs.append(words(reply))
    top = sigs.most_common(1)[0][0] if sigs else None
    struct = jdist([signature(top, f[top]) for f in rebuilt if top in f]) if top else None
    return {
        "size": sum(map(len, outs)) / len(outs),
        "writers": len(filesets),
        "filesets": len(set(filesets)),
        "top_file": top,
        "top_n": sum(1 for f in rebuilt if top in f) if top else 0,
        "struct": struct,
        "text": jdist(outs),
    }


def main(path, fixture="fixtures/marketing-site"):
    run = json.load(open(path, encoding="utf-8"))["run"]
    fx = Path(fixture)
    print("| case | writers | distinct file sets | most-written file (n) | struct spread | text spread |")
    print("| --- | ---: | ---: | --- | ---: | ---: |")
    for c in run["cases"]:
        s = case_spread(c, fx)
        f = lambda v: "—" if v is None else f"{v:.2f}"
        print(f"| `{c['caseId']}` | {s['writers']} | {s['filesets'] if s['writers'] else '—'} | "
              f"{s['top_file'] or '—'} ({s['top_n']}) | {f(s['struct'])} | {f(s['text'])} |")


# Cases whose §11.1 fork list (from arm A's questions) is empty.
EMPTY = {"collide.signup.registration_form", "collide.copy_editing.tighten_paragraph",
         "trigger.negative.near_neighbor.pricing_decision", "trigger.negative.near_neighbor.form_crash"}


def validate(path, fixture="fixtures/marketing-site"):
    """AUC of text spread for listed-fork cases over empty-list cases, raw and
    after regressing out log output size (longer outputs drift apart anyway)."""
    import math
    run = json.load(open(path, encoding="utf-8"))["run"]
    rows = [(c["caseId"], s["text"], math.log(s["size"] + 1)) for c in run["cases"] for s in [case_spread(c, Path(fixture))]]
    n = len(rows)
    mx, my = sum(r[2] for r in rows) / n, sum(r[1] for r in rows) / n
    b = sum((r[2] - mx) * (r[1] - my) for r in rows) / sum((r[2] - mx) ** 2 for r in rows)
    def auc(key):
        pos = [key(r) for r in rows if r[0] not in EMPTY]
        neg = [key(r) for r in rows if r[0] in EMPTY]
        return sum((p > q) + 0.5 * (p == q) for p in pos for q in neg) / (len(pos) * len(neg))
    print(f"AUC raw {auc(lambda r: r[1]):.2f} · length-adjusted {auc(lambda r: r[1] - (my + b * (r[2] - mx))):.2f} "
          f"· {n - len(EMPTY)} listed vs {len(EMPTY)} empty-list cases")


def demo():
    assert jdist([{1, 2}, {1, 2}]) == 0
    assert jdist([{1}, {2}]) == 1
    p = Sig(); p.feed('<form><input name="email" type="email"><p>hi</p></form>')
    assert ("input", "name=email", "type=email") in p.sig and ("p",) in p.sig
    assert rel("D:\\pb-A\\tmp\\assay-attempt-zy1DgA\\register.html".replace("\\", "/")) == "register.html"


if __name__ == "__main__":
    demo()
    if sys.argv[1] == "--validate":
        validate(*sys.argv[2:])
    else:
        main(*sys.argv[1:])
