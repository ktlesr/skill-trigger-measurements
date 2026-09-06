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

Source 2 needs a Python script to replay. A skill whose helper is a compiled
binary (impeccable's `scripts/impeccable` launcher and the engine it execs) has
no equivalent: an audit hook cannot see inside another process. For those,
`--exec <name>` still counts the invocations — attempted, executed, refused —
and the files behind that binary are reported as *not observable*, never as
never-opened. A file the instrument cannot see is not a file the run did not
read.

Usage:
  python tools/refcoverage.py [--exec <name>] <skill-dir> <run-record.json> ...

  --exec search.py   (default) replay the skill's Python helper
  --exec impeccable  count launcher invocations; no replay is possible
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
                # The run id is part of the key: two rounds reuse case ids, and
                # without it the attempt count silently collapses.
                key = f'{run["id"]}/{case["caseId"]}'
                for event in attempt.get("trace") or []:
                    yield key, attempt["index"], event


def direct_hits(events, names: set[str]) -> dict[str, int]:
    """Skill-relative paths the agent opened, counted per tool call.

    A refused tool call names a path but never opens it, so refused calls do not
    count — otherwise a blocked command would be indistinguishable from a read.
    """
    refused = {
        e["callId"]
        for _c, _i, e in events
        if e.get("kind") == "tool_result" and e.get("isError") and e.get("callId")
    }
    hits: dict[str, int] = {}
    for _case, _idx, e in events:
        if e.get("kind") == "tool_call" and e.get("id") in refused:
            continue
        blob = json.dumps(e.get("args") or {})
        if e.get("kind") != "tool_call" or not blob:
            continue
        for name in names:
            # Match the tail of the path: the sandbox prefix is a temp dir.
            if name in blob.replace("\\\\", "/").replace("\\", "/"):
                hits[name] = hits.get(name, 0) + 1
    return hits


def search_commands(events, executed_only: bool, needle: str = "search.py") -> list[list[str]]:
    """Helper-script invocations, as argv lists.

    A tool call is not proof the command ran: the host's permission layer can
    refuse it, and a refused command opens nothing. `executed_only` keeps just
    the calls whose tool_result came back without an error, which is the set a
    claim about real file reads has to be built on.
    """
    refused: set[str] = set()
    ran: set[str] = set()
    for _c, _i, e in events:
        if e.get("kind") == "tool_result" and e.get("callId"):
            (refused if e.get("isError") else ran).add(e["callId"])

    def names(a: str) -> bool:
        tail = a.rstrip('"').replace("\\", "/").rsplit("/", 1)[-1]
        return tail == needle or tail == f"{needle}.cmd"

    cmds = []
    for _case, _idx, e in events:
        if e.get("kind") != "tool_call" or e.get("tool") not in ("Bash", "PowerShell"):
            continue
        if executed_only and e.get("id") not in ran:
            continue
        raw = str((e.get("args") or {}).get("command") or "")
        if needle not in raw:
            continue
        for part in re.split(r"&&|\|\||;|\n", raw):
            if needle not in part:
                continue
            try:
                argv = shlex.split(part, posix=True)
            except ValueError:
                continue
            i = next((k for k, a in enumerate(argv) if names(a)), None)
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


def group_of(path: str) -> str:
    """Why a file ships, which decides how a never-opened verdict should read."""
    if path.startswith("scripts/tests/") or path == "scripts/validate_data.py":
        return "dev tooling (not a runtime file)"
    if path.startswith("data/stacks/"):
        return "stack data"
    if path.startswith("references/"):
        return "documented on-demand reference"
    if path.startswith("data/"):
        return "domain data"
    # --- plugin-shaped skills (impeccable) -------------------------------
    if "/reference/degraded/" in path:
        return "sub-agent fallback reference"
    if "/reference/" in path:
        return "documented on-demand reference"
    if "/scripts/data/" in path:
        return "engine data (behind the binary)"
    if "/scripts/" in path:
        return "launcher / browser runtime"
    if path.startswith("agents/"):
        return "sub-agent definition"
    if path.startswith("hooks/") or path.startswith(".claude-plugin/"):
        return "plugin manifest"
    if path == "LICENSE":
        return "licence"
    return "runtime code"


def search_modes(cmds: list[list[str]]) -> dict[str, int]:
    """Which query modes the runs actually used."""
    modes: dict[str, int] = {}
    for argv in cmds:
        used = [a for a in argv if a.startswith("--")]
        for flag in ("--design-system", "--domain", "--stack", "--persist"):
            if flag in used:
                modes[flag] = modes.get(flag, 0) + 1
        if not any(f in used for f in ("--design-system", "--domain", "--stack")):
            modes["(no mode flag)"] = modes.get("(no mode flag)", 0) + 1
    return modes


def main() -> int:
    argv = sys.argv[1:]
    exec_name = "search.py"
    if argv and argv[0] == "--exec":
        if len(argv) < 2:
            print(__doc__)
            return 2
        exec_name, argv = argv[1], argv[2:]
    if len(argv) < 2:
        print(__doc__)
        return 2
    skill_dir = Path(argv[0]).resolve()
    records = [Path(p) for p in argv[1:]]

    files = skill_files(skill_dir)
    events = list(load_traces(records))

    direct = direct_hits(events, set(files))
    attempted = search_commands(events, executed_only=False, needle=exec_name)
    cmds = search_commands(events, executed_only=True, needle=exec_name)

    distinct = []
    seen = set()
    for c in (cmds or attempted):
        key = tuple(clean(c))
        if key in seen:
            continue
        seen.add(key)
        distinct.append(list(key))

    # Replay each distinct command once; the read set is deterministic. Only a
    # Python helper can be replayed this way — a compiled launcher runs in
    # another process, where an audit hook sees nothing.
    script = skill_dir / "scripts" / exec_name
    replayable = script.suffix == ".py" and script.is_file()
    indirect: dict[str, int] = {}
    if replayable:
        cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            os.chdir(tmp)
            try:
                for args in distinct:
                    for name in replay(script, args, skill_dir):
                        indirect[name] = indirect.get(name, 0) + 1
            finally:
                os.chdir(cwd)

    # SKILL.md is not read through a tool call: the host loads it when the
    # skill triggers. Counting it as "never opened" would be false.
    always_loaded = {f for f in files if f == "SKILL.md" or f.endswith("/SKILL.md")}
    # Files only a compiled helper could open. The instrument cannot see into
    # it, so these are reported separately rather than counted as unread.
    opaque = (
        {f for f in files if group_of(f) == "engine data (behind the binary)"}
        if not replayable and attempted
        else set()
    )
    touched = set(direct) | set(indirect) | always_loaded
    never = [f for f in files if f not in touched and f not in opaque]

    total_bytes = sum(files.values())
    never_bytes = sum(files[f] for f in never)

    # Relative when it sits under the working directory: the report is
    # committed, and an absolute path carries a machine and a username with it.
    try:
        shown = skill_dir.relative_to(Path.cwd()).as_posix()
    except ValueError:
        shown = skill_dir.name

    print("# Reference-file coverage\n")
    print(f"skill directory : {shown}")
    print(f"records         : {len(records)}")
    print(f"attempts traced : {len({(c, i) for c, i, _ in events})}")
    kind = "replayed" if replayable else "not replayable (compiled helper)"
    print(f"{exec_name} calls : {len(attempted)} attempted, {len(cmds)} executed "
          f"({len(distinct)} distinct, {kind})\n")
    if attempted and not cmds:
        print(f"> **The host's permission layer refused every `{exec_name}` invocation**, so\n"
              "> the skill's helper never actually ran in this configuration.")
        if replayable:
            print("> The coverage below is what the *attempted* queries would have opened had\n"
                  "> they been allowed - an upper bound on reach, not an observation of it.")
        print()
    if not replayable and attempted:
        print(f"> `{exec_name}` is a compiled launcher, not a Python script. Its own reads\n"
              "> cannot be observed with an audit hook, so the files that only it could\n"
              "> open are listed as **not observable** below rather than as never-opened.\n")

    print(f"| | Files | Bytes |")
    print(f"| --- | --- | --- |")
    print(f"| ships in the skill | {len(files)} | {total_bytes:,} |")
    print(f"| opened by the agent | {len(direct)} | {sum(files.get(f, 0) for f in direct):,} |")
    if replayable or indirect:
        print(f"| opened by {exec_name} | {len(indirect)} | "
              f"{sum(files.get(f, 0) for f in indirect):,} |")
    print(f"| loaded by the host on trigger | {len(always_loaded)} | "
          f"{sum(files.get(f, 0) for f in always_loaded):,} |")
    if opaque:
        print(f"| not observable (behind the binary) | {len(opaque)} | "
              f"{sum(files.get(f, 0) for f in opaque):,} |")
    print(f"| **never opened** | **{len(never)}** | **{never_bytes:,}** |")
    pct = 100 * never_bytes / total_bytes if total_bytes else 0
    print(f"\nNever opened: {len(never)}/{len(files)} files, {never_bytes:,} bytes "
          f"({pct:.0f}% of the skill directory).\n")

    # Only meaningful for a launcher taking a sub-command as its first word.
    if attempted and not replayable:
        ran_ids, refused_ids = set(), set()
        for _c, _i, e in events:
            if e.get("kind") == "tool_result" and e.get("callId"):
                (refused_ids if e.get("isError") else ran_ids).add(e["callId"])
        rows: dict[str, dict[str, int]] = {}
        for _case, _idx, e in events:
            if e.get("kind") != "tool_call" or e.get("tool") not in ("Bash", "PowerShell"):
                continue
            raw = str((e.get("args") or {}).get("command") or "")
            if exec_name not in raw:
                continue
            # The sub-command is the first argument after the launcher path, not
            # the first word of the shell line: `cd X && impeccable context` is a
            # `context` call.
            head = raw.split(exec_name, 1)[1]
            head = head[4:] if head.startswith(".cmd") else head
            verb = next(
                (a for a in head.replace('"', " ").split() if a.isalpha()),
                "(no verb)",
            )
            row = rows.setdefault(verb, {"n": 0, "refused": 0})
            row["n"] += 1
            if e.get("id") in refused_ids:
                row["refused"] += 1
        print(f"## `{exec_name}` invocations through the permission layer\n")
        print("| Verb | Attempted | Refused | Ran |")
        print("| --- | --- | --- | --- |")
        for verb, r in sorted(rows.items(), key=lambda kv: -kv[1]["n"]):
            print(f"| `{verb}` | {r['n']} | {r['refused']} | {r['n'] - r['refused']} |")
        print()

    if direct:
        print("## Opened by the agent\n")
        print("| File | Bytes | Attempts |")
        print("| --- | --- | --- |")
        for f, n in sorted(direct.items(), key=lambda kv: -kv[1]):
            print(f"| `{f}` | {files.get(f, 0):,} | {n} |")
        print()
    if indirect:
        print(f"## Opened by {exec_name}\n")
        print("| File | Bytes | Distinct queries |")
        print("| --- | --- | --- |")
        for f, n in sorted(indirect.items(), key=lambda kv: -kv[1]):
            print(f"| `{f}` | {files.get(f, 0):,} | {n} |")
        print()

    # When nothing executed, the modes the runs *reached for* are still the
    # interesting number: it says which parts of the data the skill aimed at,
    # and which it never aimed at even once.
    modes = search_modes(cmds or attempted) if replayable else {}
    if modes:
        label = "actually used" if cmds else "attempted (none executed)"
        print(f"## Search modes {label}\n")
        print("| Flag | Invocations |")
        print("| --- | --- |")
        for flag, n in sorted(modes.items(), key=lambda kv: -kv[1]):
            print(f"| `{flag}` | {n} |")
        print()

    print("## Never opened, by why the file ships\n")
    groups: dict[str, list[str]] = {}
    for f in never:
        groups.setdefault(group_of(f), []).append(f)
    print("| Group | Files | Bytes |")
    print("| --- | --- | --- |")
    for g, fs in sorted(groups.items(), key=lambda kv: -sum(files[f] for f in kv[1])):
        print(f"| {g} | {len(fs)} | {sum(files[f] for f in fs):,} |")
    print()

    print("## Never opened\n")
    print("| File | Bytes | Group |")
    print("| --- | --- | --- |")
    for f in sorted(never, key=lambda x: -files[x]):
        print(f"| `{f}` | {files[f]:,} | {group_of(f)} |")

    if opaque:
        print("\n## Not observable\n")
        print("Only the compiled launcher could open these, and it runs in another\n"
              "process. Neither read nor unread — outside the instrument.\n")
        print("| File | Bytes |")
        print("| --- | --- |")
        for f in sorted(opaque, key=lambda x: -files[x]):
            print(f"| `{f}` | {files[f]:,} |")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
