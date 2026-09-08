param(
  [Parameter(Mandatory=$true)][string]$Mode,
  [int]$Chunks = 5,
  [int]$Only = 0,
  [string]$Tag = "",
  [int]$Repeat = 2
)
$ErrorActionPreference = "Continue"
$root = "D:\assay-example"
Set-Location $root
# credentials: the runner needs CLAUDE_CODE_OAUTH_TOKEN or ANTHROPIC_API_KEY
Get-Content "$root\.env" | Where-Object { $_ -match '^\s*[A-Z_]+=' } | ForEach-Object {
  $k, $v = $_ -split '=', 2
  Set-Item -Path "env:$($k.Trim())" -Value $v.Trim()
}
$env:CLAUDE_CONFIG_DIR = $null
$ledger = "$root\reports\impeccable.4.2.2.$Mode.ledger.tsv"
if (-not (Test-Path $ledger)) {
  "chunk`tstarted`tfinished`texit`trecord`tattempts" | Set-Content $ledger -Encoding utf8
}

function Get-AttemptCount($recName) {
  $p = "$root\.assay\runs\$recName"
  if (-not (Test-Path $p)) { return "?" }
  try {
    $j = Get-Content $p -Raw | ConvertFrom-Json
    return ($j.run.cases | ForEach-Object { $_.attempts.Count } | Measure-Object -Sum).Sum
  } catch { return "?" }
}

function Update-Progress {
  $md = "$root\reports\impeccable.4.2.2.progress.md"
  if (-not (Test-Path $md)) { return }
  $rows = @("| Mode | Chunk | Attempts | Record | State |", "| --- | --- | --- | --- | --- |")
  foreach ($m in @('acceptEdits','bypassPermissions')) {
    $lg = "$root\reports\impeccable.4.2.2.$m.ledger.tsv"
    if (-not (Test-Path $lg)) { $rows += "| $m | 1-5 | — | — | not started |"; continue }
    $lines = Get-Content $lg | Select-Object -Skip 1
    if (-not $lines) { $rows += "| $m | 1-5 | — | — | started, no chunk complete |"; continue }
    $tot = 0
    foreach ($l in $lines) {
      $p = $l -split "`t"
      $state = if ($p[3] -eq '0') { "ok" } else { "FAILED exit $($p[3])" }
      $n = if ($p[4] -ne 'NONE') { Get-AttemptCount $p[4] } else { "?" }
      if ($p[3] -eq '0' -and "$n" -match '^\d+$') { $tot += [int]$n }
      $rows += "| $m | $($p[0]) | $n | ``$($p[4] -replace '\.json$','')`` | $state |"
    }
    $rows += "| **$m** | **total** | **$tot / 120** | | $(if ($tot -ge 120) {'COMPLETE'} else {"$([Math]::Max(0,120-$tot)) attempts still owed"}) |"
  }
  $table = ($rows -join "`r`n")
  $txt = Get-Content $md -Raw
  $pattern = '(?s)<!--LEDGER-->.*?<!--/LEDGER-->'
  $txt = [regex]::Replace($txt, $pattern, "<!--LEDGER-->`r`n$table`r`n<!--/LEDGER-->")
  Set-Content -Path $md -Value $txt -Encoding utf8
}
function Clear-Orphans {
  $killed = 0
  try {
    $conns = Get-NetTCPConnection -State Listen -ErrorAction SilentlyContinue |
             Where-Object { $_.LocalPort -ge 5170 -and $_.LocalPort -le 5210 }
    foreach ($c in $conns) {
      $p = Get-Process -Id $c.OwningProcess -ErrorAction SilentlyContinue
      if ($p -and $p.ProcessName -in @('node','esbuild','vite')) {
        Stop-Process -Id $p.Id -Force -ErrorAction SilentlyContinue
        $killed++
      }
    }
  } catch {}
  return $killed
}

$done = (Get-Content $ledger | Select-Object -Skip 1 | Where-Object { $_ -match "`tok`t" -or ($_ -split "`t")[3] -eq '0' }).Count
$range = if ($Only -gt 0) { @($Only) } else { 1..$Chunks }
foreach ($i in $range) {
  $tag = if ($Tag) { "$Mode-$Tag" } else { "$Mode-chunk$i" }
  $existing = Get-Content $ledger | Select-Object -Skip 1 | Where-Object { ($_ -split "`t")[0] -eq $tag -and ($_ -split "`t")[3] -eq '0' }
  if ($existing) { Write-Output "SKIP $tag (already complete)"; continue }

  $k = Clear-Orphans
  Write-Output "=== $tag : cleared $k orphan(s), starting $(Get-Date -Format o) ==="
  $started = (Get-Date -Format o)
  $before = (Get-ChildItem "$root\.assay\runs" -Filter *.json -ErrorAction SilentlyContinue | ForEach-Object { $_.Name })

  # NOTE: do NOT splat these into npx. PowerShell''s splat operator eats the
  # leading @ of the package name and npx then has no executable to run.
  if ($Mode -eq 'bypassPermissions') {
    npx --yes @ktlsr/assay@0.2.0 run suites/impeccable.suite.yaml --skill ./skills/impeccable --repeat $Repeat --permission-mode bypassPermissions --allow-bypass-permissions 2>&1 |
      Tee-Object -FilePath "$root\reports\impeccable.4.2.2.$tag.run.log"
  } else {
    npx --yes @ktlsr/assay@0.2.0 run suites/impeccable.suite.yaml --skill ./skills/impeccable --repeat $Repeat --permission-mode $Mode 2>&1 |
      Tee-Object -FilePath "$root\reports\impeccable.4.2.2.$tag.run.log"
  }
  $code = $LASTEXITCODE
  $finished = (Get-Date -Format o)

  $after = Get-ChildItem "$root\.assay\runs" -Filter *.json -ErrorAction SilentlyContinue
  $new = $after | Where-Object { $before -notcontains $_.Name } | Sort-Object LastWriteTime | Select-Object -Last 1
  $rec = if ($new) { $new.Name } else { "NONE" }
  $att = "?"
  if ($new) {
    try {
      $j = Get-Content $new.FullName -Raw | ConvertFrom-Json
      $att = ($j.run.cases | ForEach-Object { $_.attempts.Count } | Measure-Object -Sum).Sum
    } catch {}
  }
  "$tag`t$started`t$finished`t$code`t$rec`t$att" | Add-Content $ledger -Encoding utf8
  Update-Progress
  Write-Output "=== $tag done exit=$code record=$rec attempts=$att ==="
}
$k = Clear-Orphans
Write-Output "ALL CHUNKS DONE for $Mode (final cleanup killed $k)"







