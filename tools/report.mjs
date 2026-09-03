// Builds the markdown tables in reports/ straight from a stored assay run
// record, so no number in a report is typed by hand.
// Usage: node tools/report.mjs .assay/runs/<run>.json
import { readFileSync } from 'node:fs'

const { run } = JSON.parse(readFileSync(process.argv[2], 'utf8'))

const Z = 1.959963985
function wilson(s, n) {
  if (n === 0) return null
  const p = s / n
  const d = 1 + (Z * Z) / n
  const c = (p + (Z * Z) / (2 * n)) / d
  const m = (Z * Math.sqrt((p * (1 - p)) / n + (Z * Z) / (4 * n * n))) / d
  return { rate: p, low: Math.max(0, c - m), high: Math.min(1, c + m), n }
}
const pct = (x) => `${Math.round(x * 100)}%`
const fmt = (w) =>
  w === null ? 'no observations (N=0)' : `${pct(w.rate)} (N=${w.n}, 95% CI ${pct(w.low)}–${pct(w.high)})`

const kind = (id) =>
  id.startsWith('complete.') ? 'completion'
  : id.includes('.near_neighbor.') ? 'near neighbour'
  : id.includes('.unrelated.') ? 'unrelated'
  : id.includes('.negative.') ? 'negative'
  : 'positive'

let TP = 0, FP = 0, TN = 0, FN = 0, UNK = 0
const rows = []
for (const c of run.cases) {
  let fired = 0, readable = 0, unreadable = 0
  for (const a of c.attempts) {
    if (a.trigger?.available) {
      readable++
      if (a.trigger.triggered) fired++
      if (c.expectedTrigger === true) a.trigger.triggered ? TP++ : FN++
      else if (c.expectedTrigger === false) a.trigger.triggered ? FP++ : TN++
    } else {
      unreadable++
      if (c.expectedTrigger !== undefined) UNK++
    }
  }
  rows.push({
    id: c.caseId,
    kind: kind(c.caseId),
    expected: c.expectedTrigger === undefined ? '—' : c.expectedTrigger ? 'fire' : 'stay quiet',
    fired: `${fired}/${readable}`,
    pass: fmt(wilson(c.passed, c.passed + c.failed)),
    unknown: c.unknown,
    verdict: c.failed > 0 ? 'FAIL' : c.unknown > 0 ? 'UNKNOWN' : 'pass',
  })
}

const t = run.cases.flatMap((c) => c.attempts).reduce(
  (acc, a) => ({
    attempts: acc.attempts + 1,
    tools: acc.tools + (a.trace?.filter((e) => e.kind === 'tool_call').length ?? 0),
    inTok: acc.inTok + (a.cost?.inputTokens ?? 0),
    outTok: acc.outTok + (a.cost?.outputTokens ?? 0),
    usd: acc.usd + (a.cost?.usd ?? 0),
    ms: acc.ms + (a.latencyMs ?? 0),
  }),
  { attempts: 0, tools: 0, inTok: 0, outTok: 0, usd: 0, ms: 0 },
)

const precision = wilson(TP, TP + FP)
const recall = wilson(TP, TP + FN)
const f1 = precision && recall && precision.rate + recall.rate > 0
  ? (2 * precision.rate * recall.rate) / (precision.rate + recall.rate) : null

const out = []
out.push(`### Pins\n`)
out.push('| Pin | Value |')
out.push('| --- | --- |')
out.push(`| skill source | \`${run.pins.skillSource}\` |`)
out.push(`| skill content hash | \`${run.pins.skillHash}\` |`)
out.push(`| model | \`${run.pins.model}\` |`)
out.push(`| system prompt hash | \`${run.pins.systemPromptHash}\` |`)
out.push(`| case set | v${run.pins.suiteVersion} · \`${run.pins.suiteHash}\` |`)
out.push(`| environment hash | \`${run.pins.environmentHash ?? '—'}\` |`)
out.push(`| run id | \`${run.id}\` |`)
out.push(`| repeats per case | ${run.runs} |`)

out.push(`\n### Per case\n`)
out.push('| Case | Kind | Expected | Fired | Pass rate | Unknown | Verdict |')
out.push('| --- | --- | --- | --- | --- | --- | --- |')
for (const r of rows)
  out.push(`| \`${r.id}\` | ${r.kind} | ${r.expected} | ${r.fired} | ${r.pass} | ${r.unknown} | ${r.verdict} |`)

out.push(`\n### Trigger accuracy\n`)
out.push('| | Fired | Stayed quiet |')
out.push('| --- | --- | --- |')
out.push(`| **Should fire** | ${TP} (TP) | ${FN} (FN) |`)
out.push(`| **Should stay quiet** | ${FP} (FP) | ${TN} (TN) |`)
out.push('')
out.push('| Metric | Value |')
out.push('| --- | --- |')
out.push(`| precision | ${fmt(precision)} |`)
out.push(`| recall | ${fmt(recall)} |`)
out.push(`| F1 | ${f1 === null ? 'not measurable' : f1.toFixed(2)} |`)
out.push(`| unreadable trigger signals | ${UNK} |`)

out.push(`\n### Cost of the measurement\n`)
out.push('| | |')
out.push('| --- | --- |')
out.push(`| attempts | ${t.attempts} |`)
out.push(`| tool calls | ${t.tools} |`)
out.push(`| tokens (in/out) | ${t.inTok} / ${t.outTok} |`)
out.push(`| cost | $${t.usd.toFixed(4)} |`)
out.push(`| wall time | ${(t.ms / 60000).toFixed(1)} min |`)

console.log(out.join('\n'))
