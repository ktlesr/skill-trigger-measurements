// Prints the reason and a trimmed trace for every non-pass attempt in a run.
import { readFileSync } from 'node:fs'
const { run } = JSON.parse(readFileSync(process.argv[2], 'utf8'))
const only = process.argv[3]
for (const c of run.cases) {
  if (only && c.caseId !== only) continue
  for (const a of c.attempts) {
    if (a.verdict === 'pass') continue
    console.log(`\n### ${c.caseId} #${a.index} -> ${a.verdict}: ${a.reason}`)
    for (const r of a.assertions ?? []) console.log(`    [${r.verdict}] ${r.assertion.type} ${r.reason}`)
    console.log(`    skills observed: ${JSON.stringify(a.trigger?.skills ?? null)}`)
    for (const e of (a.trace ?? []).slice(0, 14)) {
      if (e.kind === 'assistant_message') console.log(`    msg: ${(e.text ?? '').replace(/\s+/g, ' ').slice(0, 260)}`)
      if (e.kind === 'tool_call') console.log(`    call ${e.tool} ${JSON.stringify(e.args).slice(0, 170)}`)
      if (e.kind === 'skill_trigger') console.log(`    SKILL ${e.skill}`)
    }
    const w = a.env?.writes ?? []
    if (w.length) console.log(`    writes: ${w.join(', ')}`)
  }
}
