# Interleaves chunks across arms and modes so time-of-day drift (rate limits,
# API changes) lands on every arm equally. Resumable: run-chunks.ps1 skips
# chunks its ledger already records as exit 0.
param([int]$Chunks = 10)
$arms = @(
  @{ Arm = "4.5.2"; SkillDir = "./skills/impeccable" },
  @{ Arm = "4.2.2-rebase"; SkillDir = "D:/pb-452/skill-4.2.2/skills/impeccable" }
)
foreach ($i in 1..$Chunks) {
  foreach ($mode in @('acceptEdits', 'bypassPermissions')) {
    foreach ($a in $arms) {
      & "$PSScriptRoot\run-chunks.ps1" -Mode $mode -Only $i -Chunks $Chunks -Repeat 1 -Assay 0.5.0 `
        -Arm $a.Arm -SkillDir $a.SkillDir -Progress "impeccable.4.5.2.progress.md" -Arms @("4.5.2", "4.2.2-rebase")
    }
  }
}
