"""Reference-file coverage for a skill.

Answers: the skill ships N auxiliary files — which of them does a real run
actually open, and which are never touched at all?

Two sources of truth, because a file can be reached two ways:

  1. **Directly by the agent** — a Read/Grep/Glob tool call, or a shell command
     naming the path. Taken straight from the stored run traces.
  2. **Indirectly by the skill's own script** — `search.py` opens CSVs itself, so
     no agent tool call ever names them. For these we take every `search.py`
     command line that actually occurred in the traces and *replay it locally*
     under a Python audit hook that records every `open()`. Same script, same
     arguments, same data files, so the read set is the real one.

Usage:
  python tools/refcoverage.py <skill-dir> <run-record.json> [<run-record.json> ...]
"""

from __future__ import annotations

import io
import json
import os
import re
import runpy
import shlex
import sys
import tempfile
from contextlib import redirect_stdout, redirect_stderr
from pathlib import Path

# Flags that make a replay write to disk. Stripped: we are measuring reads.
WRITE_FLAGS = {"--persist", "--force"}
WRITE_FLAGS_WITH_VALUE = {"--output-dir"}


def skill_files(skill_dir: Path) -> dict[str, int]:
    """Files the skill actually ships. `__pycache__` is a build artefact of our
    own replay, not part of the skill, so it never counts either way."""
    out = {}
    for p in sorted(skill_dir.rglob("*")):
        if p.is_file() and "__pycache__" not in p.parts:
            out[p.relative_to(skill_dir).as_posix()] = p.stat().st_size
    return out


def load_traces(records: list[Path]):
    """Yield (case_id, attempt_index, trace_event) for every stored attempt."""
    for rec in records:
        run = json.loads(rec.read_text(encoding="utf-8"))["run"]
        for case in run["cases"]:
            for attempt in case["attempts"]:
                for event in attempt.get("trace") or []:
                    yield case["caseId"], attempt["index"], event


def direct_hits(events, names: set[str]) -> dict[str, int]:
    """Skill-relative paths the agent named itself, with a count of attempts."""
    hits: dict[str, int] = {}
    for _case, _idx, e in events:
        blob = json.dumps(e.get("args") or {})
        if e.get("kind") != "tool_call" or not blob:
            continue
        for name in names:
            # Match the tail of the path: the sandbox prefix is a temp dir.
            if name in blob.replace("\\\\", "/").replace("\\", "/"):
                hits[name] = hits.get(name, 0) + 1
    return hits


def search_commands(events) -> list[list[str]]:
    """Every search.py invocation that really happened, as an argv list."""
    cmds = []
    for _case, _idx, e in events:
        if e.get("kind") != "tool_call" or e.get("tool") != "Bash":
            continue
        raw = str((e.get("args") or {}).get("command") or "")
        if "search.py" not in raw:
            continue
        for part in re.split(r"&&|\|\||;|\n", raw):
            if "search.py" not in part:
                continue
            try:
                argv = shlex.split(part, posix=True)
            except ValueError:
                continue
            i = next((k for k, a in enumerate(argv) if a.endswith("search.py")), None)
            if i is None:
                continue
            cmds.append(argv[i + 1 :])
    return cmds


def clean(argv: list[str]) -> list[str]:
    out, skip = [], False
    for a in argv:
        if skip:
            skip = False
            continue
        if a in WRITE_FLAGS:
            continue
        if a in WRITE_FLAGS_WITH_VALUE:
            skip = True
            continue
        out.append(a)
    return out


def replay(script: Path, argv: list[str], skill_dir: Path) -> set[str]:
    """Run search.py once and return the skill-relative files it opened."""
    opened: set[str] = set()
    root = skill_dir.resolve()

    def hook(event, args):
        if event != "open":
            return
        try:
            p = Path(os.fspath(args[0])).resolve()
        except (TypeError, ValueError, OSError):
            return
        try:
            rel = p.relative_to(root).as_posix()
        except ValueError:
            return
        if "__pycache__" not in rel:
            opened.add(rel)

    sys.dont_write_bytecode = True
    sys.addaudithook(hook)
    old_argv, old_path = sys.argv, list(sys.path)
    sys.argv = [str(script), *argv]
    # search.py imports its siblings (core, design_system, ...) by bare name;
    # runpy does not put the script's own directory on the path the way the
    # interpreter does when you invoke the file.
    sys.path.insert(0, str(script.parent))
    try:
        with redirect_stdout(io.StringIO()), redirect_stderr(io.StringIO()):
            runpy.run_path(str(script), run_name="__main__")
    except SystemExit:
        pass
    except Exception as exc:  # a failed query still tells us what it opened
        print(f"    (replay raised {type(exc).__name__}: {exc})", file=sys.stderr)
    finally:
        sys.argv, sys.path = old_argv, old_path
        for mod in ('core', 'design_system', 'reasoning_contract', 'search'):
            sys.modules.pop(mod, None)
    return opened


def main() -> int:
    if len(sys.argv) < 3:
        print(__doc__)
        return 2
    skill_dir = Path(sys.argv[1]).resolve()
    records = [Path(p) for p in sys.argv[2:]]

    files = skill_files(skill_dir)
    events = list(load_traces(records))

    direct = direct_hits(events, set(files))
    cmds = search_commands(events)

    # Replay each distinct command once; the read set is deterministic.
    script = skill_dir / "scripts" / "search.py"
    indirect: dict[str, int] = {}
    distinct = []
    seen = set()
    for c in cmds:
        key = tuple(clean(c))
        if key in seen:
            continue
        seen.add(key)
        distinct.append(list(key))

    cwd = os.getcwd()
    with tempfile.TemporaryDirectory() as tmp:
        os.chdir(tmp)
        try:
            for argv in distinct:
                for name in replay(script, argv, skill_dir):
                    indirect[name] = indirect.get(name, 0) + 1
        finally:
            os.chdir(cwd)

    # SKILL.md is not read through a tool call: the host loads it when the
    # skill triggers. Counting it as "never opened" would be false.
    always_loaded = {"SKILL.md"} & set(files)
    touched = set(direct) | set(indirect) | always_loaded
    never = [f for f in files if f not in touched]

    total_bytes = sum(files.values())
    never_bytes = sum(files[f] for f in never)

    print("# Reference-file coverage\n")
    print(f"skill directory : {skill_dir}")
    print(f"records         : {len(records)}")
    print(f"attempts traced : {len({(c, i) for c, i, _ in events})}")
    print(f"search.py calls : {len(cmds)} ({len(distinct)} distinct, replayed)\n")

    print(f"| | Files | Bytes |")
    print(f"| --- | --- | --- |")
    print(f"| ships in the skill | {len(files)} | {total_bytes:,} |")
    print(f"| opened by the agent | {len(direct)} | {sum(files.get(f, 0) for f in direct):,} |")
    print(f"| opened by search.py | {len(indirect)} | {sum(files.get(f, 0) for f in indirect):,} |")
    print(f"| loaded by the host on trigger | {len(always_loaded)} | "
          f"{sum(files.get(f, 0) for f in always_loaded):,} |")
    print(f"| **never opened** | **{len(never)}** | **{never_bytes:,}** |")
    pct = 100 * never_bytes / total_bytes if total_bytes else 0
    print(f"\nNever opened: {len(never)}/{len(files)} files, {never_bytes:,} bytes "
          f"({pct:.0f}% of the skill directory).\n")

    if direct:
        print("## Opened by the agent\n")
        print("| File | Bytes | Attempts |")
        print("| --- | --- | --- |")
        for f, n in sorted(direct.items(), key=lambda kv: -kv[1]):
            print(f"| `{f}` | {files.get(f, 0):,} | {n} |")
        print()
    if indirect:
        print("## Opened by search.py\n")
        print("| File | Bytes | Distinct queries |")
        print("| --- | --- | --- |")
        for f, n in sorted(indirect.items(), key=lambda kv: -kv[1]):
            print(f"| `{f}` | {files.get(f, 0):,} | {n} |")
        print()

    print("## Never opened\n")
    print("| File | Bytes |")
    print("| --- | --- |")
    for f in sorted(never, key=lambda x: -files[x]):
        print(f"| `{f}` | {files[f]:,} |")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
