# Host git environment — diagnosis and fix, 2026-09-08

Pushes from this machine were failing roughly half the time with:

```
sh.exe: *** fatal error - add_item ("\??\C:\Program Files\Git", "/", ...) failed, errno 1
error: unable to read askpass response from '…\vscode.git\askpass\70789581cae28aa7\askpass.sh'
fatal: could not read Username for 'https://github.com': terminal prompts disabled
```

The same underlying fault broke a `claude plugin marketplace add`, and hit 11 of
390 in-sandbox Bash calls during the 4.2.2 measurement — where it had to be
written into `reports/impeccable.4.2.2.md` as a confounder.

## Diagnosis

Three separate defects, not one.

### 1. The credential helper was routed through `sh` (definite, fixed)

The global config contained:

```
[credential "https://github.com"]
	helper =
	helper = !'C:\Users\KESER\AppData\Local\Programs\gh\bin\gh.exe' auth git-credential
```

The `!` prefix means "run as a shell command", so **every credential lookup
invoked the broken `sh`**. The empty first `helper =` also cleared the
system-wide `manager`, so there was no fallback. This was invisible to
`git config --get-all credential.helper`, because the helper was scoped to a
`https://github.com` subsection.

### 2. `C:\Windows\System32` is missing from the Machine PATH (real, worked around)

The machine PATH contains only ten entries and **none of the Windows system
directories**:

```
C:\Windows\System32                          absent (exists on disk)
C:\Windows                                   absent
C:\Windows\System32\Wbem                     absent
C:\Windows\System32\WindowsPowerShell\v1.0   absent
```

Consequences confirmed by measurement: `where.exe` and `curl.exe` were not
resolvable, which is exactly why the impeccable launcher's self-download path
failed closed (its gate is `where curl.exe`). `C:\Program Files\Git\mingw64\bin`
was also absent, so git could not resolve the `manager` helper.

This is a genuine system misconfiguration — almost certainly a truncated PATH
from an earlier edit. **It still needs an elevated fix; see below.**

### 3. The MSYS2 `add_item` fault itself (characterised, not eliminated)

What was ruled out by measurement:

- not a duplicate-runtime problem — one `msys-2.0.dll`, no stray `cygwin1.dll`
- not a stale install — Git 2.53.0, msys runtime 3.6.6, stock `/etc/fstab`
- not env pollution — `MSYS`, `MSYSTEM`, `CYGWIN`, `MSYS2_PATH_TYPE` all unset
- not deterministic by shell mode — an early theory that `bash -lc` always
  failed did not survive retesting (10/10 clean afterwards)

What it actually is: **bursty and intermittent.** One probe of 30 sequential
`bash -c` calls passed 30/30; a later probe of 25 failed 25/25; a batch after
the fix passed 20/20. It also produces *hangs*, not only fatal errors — 9 stuck
`bash.exe` processes were observed accumulating at once.

Git always runs credential helpers through a shell —
`start_command: 'C:/Program Files/Git/usr/bin/sh.exe' -c 'git credential-manager get'`
(from `GIT_TRACE`) — so while this fault persists, no choice of credential
helper avoids it. Reducing exposure was the only available lever; the fix below
removes the *extra* `sh` hop and makes the helper resolvable, which is what the
measured improvement comes from.

## What was changed

| # | Change | Scope | Why |
| --- | --- | --- | --- |
| 1 | Removed `credential.https://github.com` section | global `.gitconfig` | dropped the `!`-prefixed gh helper that forced `sh` |
| 2 | Removed `credential.https://gist.github.com` section | global `.gitconfig` | same defect |
| 3 | Stored the GitHub token in Git Credential Manager | Windows Credential Manager (DPAPI) | so no interactive askpass is ever reached |
| 4 | Prepended `System32`, `Windows`, `Wbem`, `WindowsPowerShell\v1.0`, `Git\mingw64\bin` | **User** PATH | restore resolvable `where`/`curl`, and let git find `manager` |

Change 4 is a **workaround at user scope**, because this account is not an
administrator. The Machine PATH is still broken for every other process on the
system.

## Verification

| Round | Result |
| --- | --- |
| `git credential fill` x10 | **10/10**, mean 207 ms |
| 5 push+delete cycles, round 1 | 3/5 — two 61 s timeouts with `add_item` |
| 5 push+delete cycles, round 2 | **5/5**, no `sh` errors |
| 5 push+delete cycles, round 3 | **5/5**, no `sh` errors |
| `bash -c` x20 | **20/20** clean |

Each cycle is a real authenticated write: push a temp branch, then delete it.
All temp branches were removed afterwards; `master` was untouched.

**Honest caveat:** round 1 was 3/5, and single pushes occasionally still take
25-37 s before succeeding. Two clean rounds and a clean bash batch is good
evidence the common path is fixed, but the underlying MSYS2 fault has not been
eliminated and may resurface under heavy concurrency — which is exactly the
condition that produced the 11/390 rate during the measurement run.

## Still outstanding — needs an administrator

Restore the Windows system directories to the **Machine** PATH. Run in an
elevated PowerShell:

```powershell
$p = [Environment]::GetEnvironmentVariable("PATH","Machine")
$need = @("C:\Windows\System32","C:\Windows","C:\Windows\System32\Wbem",
          "C:\Windows\System32\WindowsPowerShell\v1.0")
$add = $need | Where-Object { ($p -split ';') -notcontains $_ }
if ($add) { [Environment]::SetEnvironmentVariable("PATH", (($add + ($p -split ';' | Where-Object {$_})) -join ';'), "Machine") }
```

Once that lands, the User-PATH entries added in change 4 can be dropped again.

## Rollback

Backups are in `.gitconfig-backups/` (gitignored), stamped `20260908-200815`
for PATH and `20260908-195621` for the git config.

```powershell
# 1. git config
Copy-Item "D:\assay-example\.gitconfig-backups\gitconfig-global-20260908-195621.bak" `
          "$env:USERPROFILE\.gitconfig" -Force

# 2. User PATH
$bak = Get-Content "D:\assay-example\.gitconfig-backups\PATH-User-20260908-200815.bak" -Raw
[Environment]::SetEnvironmentVariable("PATH", $bak.Trim(), "User")

# 3. stored credential
"protocol=https`nhost=github.com`n`n" | git credential reject
```

Rolling back restores the original failure mode; it is only worth doing if one
of these changes is shown to cause a new problem.
