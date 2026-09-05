// Reads a stored run record and reports what a trace can and cannot see about
// a plugin-shaped skill: the trigger signal, host permission denials, which
// reference files were opened, and which other skills competed.
//
// Hook output is deliberately searched for rather than assumed absent: a
// PostToolUse hook returns `hookSpecificOutput.additionalContext`, which is
// context injection, not a tool call. If any of it reaches the trace it can
// only arrive inside an assistant message or a tool_result error string.
import { readFileSync } from 'node:fs'

const { run } = JSON.parse(readFileSync(process.argv[2], 'utf8'))
const HOOK = /impeccable@\d|Design hook|design-quality issues|deep pass/i

const bash = { attempted: 0, denied: 0, ok: 0 }
const denialText = new Map()
const bashCommands = new Map()
const refs = new Map()
const otherSkills = new Map()
const hookEchoes = []
let attempts = 0
let triggeredCount = 0

for (const c of run.cases) {
  for (const a of c.attempts) {
    attempts += 1
    for (const s of a.trigger?.skills ?? []) {
      otherSkills.set(s, (otherSkills.get(s) ?? 0) + 1)
    }
    if (a.trigger?.triggered) triggeredCount += 1

    const errById = new Map()
    for (const e of a.trace ?? []) {
      if (e.kind === 'tool_result' && e.isError) errById.set(e.callId, e.error ?? '')
    }

    for (const e of a.trace ?? []) {
      if (e.kind === 'tool_call' && (e.tool === 'Bash' || e.tool === 'PowerShell')) {
        const cmd = String(e.args?.command ?? '')
        bash.attempted += 1
        const err = errById.get(e.id)
        if (err !== undefined && /requires approval|not allowed|permission/i.test(err)) {
          bash.denied += 1
          denialText.set(err.replace(/\s+/g, ' ').slice(0, 180), true)
        } else if (err === undefined) {
          bash.ok += 1
        }
        const key = cmd.replace(/\s+/g, ' ').slice(0, 120)
        const seen = bashCommands.get(key) ?? { n: 0, denied: 0 }
        seen.n += 1
        if (err !== undefined) seen.denied += 1
        bashCommands.set(key, seen)
      }

      if (e.kind === 'tool_call' && (e.tool === 'Read' || e.tool === 'Grep' || e.tool === 'Glob')) {
        const target = String(e.args?.file_path ?? e.args?.path ?? e.args?.pattern ?? '')
        const m = target.match(/reference[/\\]([\w.-]+\.md)/)
        if (m) refs.set(m[1], (refs.get(m[1]) ?? 0) + 1)
      }

      const text =
        e.kind === 'assistant_message' ? e.text : e.kind === 'tool_result' ? e.error : undefined
      if (text && HOOK.test(text)) hookEchoes.push(text.replace(/\s+/g, ' ').slice(0, 200))
    }
  }
}

const pct = (n, d) => (d === 0 ? 'n/a' : `${Math.round((n / d) * 100)}%`)

console.log(`run ${run.id} · ${attempts} attempts · skill ${run.skill}`)
console.log(`\n1. trigger signal`)
console.log(`   triggered in ${triggeredCount}/${attempts} attempts`)
console.log(`   skills observed via Skill tool call:`)
for (const [s, n] of [...otherSkills].sort((a, b) => b[1] - a[1])) {
  console.log(`     ${s}  ${n}`)
}

console.log(`\n2. hook output reaching the trace`)
console.log(`   ${hookEchoes.length} trace events carry hook-shaped text`)
for (const h of hookEchoes.slice(0, 5)) console.log(`     > ${h}`)

console.log(`\n3. Bash through the host permission layer`)
console.log(`   attempted ${bash.attempted} · denied ${bash.denied} (${pct(bash.denied, bash.attempted)}) · ran ${bash.ok}`)
for (const d of [...denialText.keys()].slice(0, 6)) console.log(`     > ${d}`)
console.log(`   commands:`)
for (const [cmd, s] of [...bashCommands].sort((a, b) => b[1].n - a[1].n).slice(0, 15)) {
  console.log(`     ${s.n}x (${s.denied} failed)  ${cmd}`)
}

console.log(`\n4. reference files opened`)
if (refs.size === 0) console.log(`   none`)
for (const [f, n] of [...refs].sort((a, b) => b[1] - a[1])) console.log(`     ${f}  ${n}`)
