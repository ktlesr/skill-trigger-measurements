// Replaces {{TABLES:<run-id>}} placeholders in a markdown file with tables
// generated from the matching stored run record.
import { readFileSync, writeFileSync } from 'node:fs'
import { execFileSync } from 'node:child_process'
const file = process.argv[2]
const src = readFileSync(file, 'utf8')
const out = src.replace(/\{\{TABLES:([^}]+)\}\}/g, (_, id) =>
  execFileSync(process.execPath, ['tools/report.mjs', `.assay/runs/${id.trim()}.json`], {
    encoding: 'utf8',
  }).trimEnd(),
)
writeFileSync(file, out)
console.log(`assembled ${file}`)
