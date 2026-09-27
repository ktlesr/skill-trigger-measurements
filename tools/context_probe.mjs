// Free check that an ancestor CLAUDE.md reaches the agent under a given Assay
// adapter. Writes the adapter's own settings (claudeMdExcludes + the
// InstructionsLoaded hook) into a fresh config dir and starts `claude -p` with no
// credentials: the session stops at "Not logged in", after the host has loaded
// its instruction files and fired the hook, before any model call ($0).
//
// Usage: node tools/context_probe.mjs <assay-adapters dist/claude-code/adapter.js> <root> [noexcl]
//   <root>/CLAUDE.md is the file under test; the workdir is <root>/work/probe.
//   noexcl drops claudeMdExcludes, to show the file loads without it.
import { spawnSync } from 'node:child_process';
import { existsSync, mkdirSync, readFileSync, rmSync, writeFileSync } from 'node:fs';
import { pathToFileURL } from 'node:url';

const [adapterPath, root, mode] = process.argv.slice(2);
const { writeMemoryProbe } = await import(pathToFileURL(adapterPath).href);
const [cfg, wd, tmp] = [`${root}/cfg`, `${root}/work/probe`, `${root}/tmp`];
rmSync(cfg, { recursive: true, force: true });
for (const d of [cfg, wd, tmp]) mkdirSync(d, { recursive: true });
await writeMemoryProbe(cfg, wd);
if (mode === 'noexcl') {
  const s = JSON.parse(readFileSync(`${cfg}/settings.json`, 'utf8'));
  delete s.claudeMdExcludes;
  writeFileSync(`${cfg}/settings.json`, JSON.stringify(s));
}
const env = { PATH: process.env.PATH, SYSTEMROOT: process.env.SYSTEMROOT, USERPROFILE: process.env.USERPROFILE,
  APPDATA: process.env.APPDATA, TEMP: tmp, TMP: tmp, CLAUDE_CONFIG_DIR: cfg };
const r = spawnSync('claude', ['-p', '--output-format', 'json', 'say ok'], { cwd: wd, env, input: '', encoding: 'utf8', shell: true, timeout: 60000 });
const cost = JSON.parse(r.stdout || '{}').total_cost_usd;
const log = `${cfg}/assay-instructions.jsonl`;
const events = existsSync(log) ? readFileSync(log, 'utf8').split('\n').filter(Boolean).map((l) => JSON.parse(l)) : [];
console.log(`claudeMdExcludes ${mode === 'noexcl' ? 'off' : 'on'} · exit ${r.status} · $${cost} · canary ${events.some((e) => e.hook_event_name === 'UserPromptSubmit') ? 'fired' : 'MISSING'}`);
console.log('loaded:', events.filter((e) => e.hook_event_name === 'InstructionsLoaded').map((e) => e.file_path).join(', ') || 'nothing');
