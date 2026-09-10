// Hallmark ablation: rules, suite generation, calibration, analysis — one file,
// one regex engine (assay evaluates with JS RegExp, so calibration must too).
//
//   node tools/hallmark-ablation.mjs suite            > suites/hallmark.ablation.suite.yaml
//   node tools/hallmark-ablation.mjs calibrate <dir>  # one sub-dir = one page
//   node tools/hallmark-ablation.mjs analyse A=<run.json> B=<run.json>
import { readFileSync, readdirSync, statSync } from 'node:fs';
import { join, extname } from 'node:path';

// Every rule is a named tell from hallmark's own references/anti-patterns.md.
// literal: the skill defines the tell as a code pattern, so the regex IS the rule.
// proxy:   the tell has a judgement part ("without purpose", "in the hero") a
//          regex cannot see; the regex counts the ingredient, not the verdict.
export const RULES = [
  ['gradient_headline', 'literal', String.raw`background-clip\s*:\s*text|\bbg-clip-text\b`, 'i'],
  ['pure_black_white', 'literal', String.raw`#(?:000000|ffffff|000|fff)(?![0-9a-f])|rgba?\(\s*(?:0\s*,\s*0\s*,\s*0|255\s*,\s*255\s*,\s*255)\s*[,)]|\b(?:bg|text)-(?:white|black)\b|:\s*(?:white|black)\s*[;!}]`, 'i'],
  ['transition_all', 'literal', String.raw`transition\s*:\s*(?:all\b|[\d.]+m?s\b)|transition-property\s*:\s*all\b|\btransition-all\b`, 'i'],
  ['hover_scale', 'proxy', String.raw`\bhover:scale-\d+|:hover[^{}]*\{[^}]*scale\(\s*1\.\d`, 'i'],
  ['z_index_9999', 'literal', String.raw`z-index\s*:\s*9{4,}|\bz-\[9{4,}\]`, ''],
  ['width_100vw', 'literal', String.raw`width\s*:\s*100vw|\bw-screen\b`, 'i'],
  ['emoji_icon', 'literal', '[✨🚀⚡🔥🎯✅]', 'u'],
  ['placeholder_names', 'literal', String.raw`Jane Doe|John Smith|Example User`, 'i'],
  ['italic_headers', 'literal', String.raw`<h[1-3]\b[^>]*>(?:(?!</h[1-3]>)[\s\S])*?(?:<em\b|<i>)|h[1-3]\b[^{};]*\{[^}]*font-style\s*:\s*italic`, 'i'],
  ['purple_gradient', 'proxy', String.raw`(?:linear|radial|conic)-gradient\([^;]*?(?:purple|violet|indigo|fuchsia|magenta|#(?:8b5cf6|7c3aed|6d28d9|a855f7|9333ea|6366f1|4f46e5|c026d3|d946ef|a78bfa|818cf8|c084fc|e879f9))|\b(?:from|via|to)-(?:purple|violet|indigo|fuchsia)-\d{2,3}\b`, 'i'],
  ['inter_primary', 'proxy', String.raw`font-family\s*:\s*['"]?(?:Inter|Roboto|Open Sans)\b|--[\w-]*font[\w-]*\s*:\s*['"]?(?:Inter|Roboto|Open Sans)\b|family=(?:Inter|Roboto|Open\+Sans)\b|\bfont-(?:inter|roboto)\b`, 'i'],
  ['glassmorphism', 'proxy', String.raw`backdrop-filter\s*:\s*blur|\bbackdrop-blur\b`, 'i'],
  ['aurora_blob', 'proxy', String.raw`filter\s*:\s*blur\(\s*(?:[4-9]\d|\d{3,})px|\bblur-(?:2xl|3xl)\b`, 'i'],
  ['bounce_easing', 'proxy', String.raw`cubic-bezier\(\s*[^,)]+,\s*(?:-\d*\.?\d+|1\.0*[1-9]\d*|[2-9]\d*(?:\.\d+)?)\s*,|cubic-bezier\(\s*[^,)]+,[^,)]+,[^,)]+,\s*(?:-\d*\.?\d+|1\.0*[1-9]\d*|[2-9]\d*(?:\.\d+)?)\s*\)|\banimate-bounce\b|@keyframes\s+[\w-]*(?:bounce|elastic|wobble)`, 'i'],
];
export const GLOBS = ['**/*.html', '**/*.css'];
// assay's file_content_matches has no negation, so each check is "no file
// contains the tell": a negative lookahead anchored at the start.
const clean = (src) => String.raw`^(?![\s\S]*(?:` + src + `))`;
const re = (src, flags) => new RegExp(src, flags);

// assertion index -> [rule, glob]; index 0 is the file_exists guard
export const SLOTS = [['(output)', '**/*.html'], ...RULES.flatMap(([id]) => GLOBS.map((g) => [id, g]))];

function suite() {
  const q = (s) => `'${s.replace(/'/g, "''")}'`;
  const rules = SLOTS.slice(1).map(([id, glob]) => {
    const [, , src, flags] = RULES.find((r) => r[0] === id);
    return `        - { type: file_content_matches, path: ${q(glob)}, matches: ${q(clean(src))}${flags ? `, flags: ${q(flags)}` : ''} }`;
  });
  return rules.join('\n');
}

function pageFiles(dir) {
  const out = [];
  for (const name of readdirSync(dir)) {
    const p = join(dir, name);
    if (name === 'node_modules' || name.startsWith('.')) continue;
    if (statSync(p).isDirectory()) out.push(...pageFiles(p));
    else if (['.html', '.css'].includes(extname(name))) out.push(p);
  }
  return out;
}

function calibrate(root) {
  const pages = readdirSync(root).filter((d) => statSync(join(root, d)).isDirectory());
  const hits = Object.fromEntries(RULES.map(([id]) => [id, []]));
  for (const page of pages) {
    const texts = pageFiles(join(root, page)).map((f) => readFileSync(f, 'utf8'));
    for (const [id, , src, flags] of RULES) {
      // the suite's own check: pass iff every file passes the lookahead
      if (!texts.every((t) => re(clean(src), flags).test(t))) hits[id].push(page);
    }
  }
  console.log(`pages: ${pages.length}`);
  for (const [id, kind] of RULES) console.log(`${id.padEnd(18)} ${kind.padEnd(7)} ${String(hits[id].length).padStart(2)}  ${hits[id].join(', ')}`);
}

// A content assertion is a violation only when real page files failed: a
// "no file matches" miss is an absent file, and node_modules is not the page.
function violated(result) {
  if (result.verdict !== 'fail') return false;
  const why = String(result.reason ?? '');
  if (why.startsWith('no file matches')) return false;
  const files = why.split(' do not match')[0].split(', ');
  return files.some((f) => !f.includes('node_modules/'));
}

function load(paths) {
  return paths.flatMap((p) => JSON.parse(readFileSync(p, 'utf8')).run.cases.flatMap((c) =>
    c.attempts.map((a) => ({ caseId: c.caseId, a }))));
}

function wilson(k, n) {
  if (n === 0) return [0, 0];
  const z = 1.959963985, p = k / n, d = 1 + z * z / n;
  const c = (p + z * z / (2 * n)) / d, h = (z * Math.sqrt(p * (1 - p) / n + z * z / (4 * n * n))) / d;
  return [Math.max(0, c - h), Math.min(1, c + h)];
}
const pct = (k, n) => { const [lo, hi] = wilson(k, n); return `${k}/${n} (${Math.round(100 * k / n)}%, ${Math.round(100 * lo)}–${Math.round(100 * hi)}%)`; };

function analyse(arms) {
  const rows = {};
  for (const [arm, paths] of Object.entries(arms)) {
    for (const { caseId, a } of load(paths)) {
      const res = a.assertions ?? [];
      const produced = res[0]?.verdict === 'pass';
      const v = new Set();
      SLOTS.forEach(([id], i) => { if (i > 0 && res[i] && violated(res[i])) v.add(id); });
      const skills = (a.trigger?.skills ?? []);
      // reads of the skill's own rulebook: the tells live in references/, not SKILL.md
      const results = new Map((a.trace ?? []).filter((e) => e.kind === 'tool_result').map((e) => [e.callId, e]));
      const norm = (e) => JSON.stringify(e.args ?? {}).replace(/\\\\/g, '/');
      const refs = (a.trace ?? []).filter((e) => e.kind === 'tool_call' && ['Read', 'Grep', 'Glob'].includes(e.tool)
        && norm(e).includes('/skills/hallmark/references/'))
        .map((e) => ({ ok: !results.get(e.id)?.isError, file: (norm(e).match(/references\/([\w\-/.]+\.md)/) ?? [])[1] }));
      // did the agent try to invoke a skill named hallmark, and did the host refuse it?
      const skillCalls = (a.trace ?? []).filter((e) => e.kind === 'tool_call' && e.tool === 'Skill' && /hallmark/i.test(JSON.stringify(e.args ?? {})))
        .map((e) => ({ ok: !results.get(e.id)?.isError, err: String(results.get(e.id)?.error ?? '').slice(0, 90) }));
      (rows[arm] ??= []).push({ caseId, produced, v, fired: skills.includes('hallmark:hallmark'), skills, refs, skillCalls });
    }
  }
  const arms2 = Object.keys(rows);
  console.log('## Trigger and output\n');
  console.log(`| arm | attempts | hallmark fired | produced a page |`);
  console.log(`| --- | --- | --- | --- |`);
  for (const arm of arms2) {
    const r = rows[arm];
    console.log(`| ${arm} | ${r.length} | ${pct(r.filter((x) => x.fired).length, r.length)} | ${pct(r.filter((x) => x.produced).length, r.length)} |`);
  }
  console.log('\n## Rulebook reads (references/*.md) and skills that fired\n');
  for (const arm of arms2) {
    const r = rows[arm], refs = r.flatMap((x) => x.refs);
    const files = {}; refs.filter((x) => x.ok).forEach((x) => { files[x.file] = (files[x.file] ?? 0) + 1; });
    const fired = {}; r.forEach((x) => x.skills.forEach((s) => { fired[s] = (fired[s] ?? 0) + 1; }));
    console.log(`- ${arm}: reference reads attempted ${refs.length}, succeeded ${refs.filter((x) => x.ok).length}, refused/failed ${refs.filter((x) => !x.ok).length}; attempts that read anti-patterns.md or slop-test.md: ${r.filter((x) => x.refs.some((f) => f.ok && /anti-patterns|slop-test/.test(f.file ?? ''))).length}/${r.length}`);
    console.log(`  files: ${Object.entries(files).sort((a, b) => b[1] - a[1]).map(([f, n]) => `${f}×${n}`).join(', ') || '—'}`);
    const sc = r.filter((x) => x.caseId.startsWith('ablation.'));
    const tried = sc.filter((x) => x.skillCalls.length), errs = [...new Set(sc.flatMap((x) => x.skillCalls.filter((c) => !c.ok).map((c) => c.err)))];
    console.log(`  page attempts that called Skill("hallmark"): ${tried.length}/${sc.length}; calls that errored: ${sc.flatMap((x) => x.skillCalls).filter((c) => !c.ok).length}${errs.length ? ` — e.g. "${errs[0]}"` : ''}`);
    console.log(`  skills fired: ${Object.entries(fired).sort((a, b) => b[1] - a[1]).map(([s, n]) => `${s}×${n}`).join(', ') || 'none'}`);
  }
  console.log('\n## Pages that break each rule (among attempts that produced a page)\n');
  console.log(`| rule | kind | ${arms2.join(' | ')} | intervals overlap? |`);
  console.log(`| --- | --- |${' --- |'.repeat(arms2.length)} --- |`);
  for (const [id, kind] of RULES) {
    const cells = arms2.map((arm) => { const r = rows[arm].filter((x) => x.produced); return [r.filter((x) => x.v.has(id)).length, r.length]; });
    const iv = cells.map(([k, n]) => wilson(k, n));
    const overlap = iv.length === 2 ? (iv[0][1] >= iv[1][0] && iv[1][1] >= iv[0][0] ? 'yes' : '**no**') : '';
    console.log(`| ${id} | ${kind} | ${cells.map(([k, n]) => pct(k, n)).join(' | ')} | ${overlap} |`);
  }
  console.log('\n## Any literal rule broken (page level)\n');
  const litIds = RULES.filter((r) => r[1] === 'literal').map((r) => r[0]);
  const anyLit = arms2.map((arm) => { const r = rows[arm].filter((x) => x.produced); return [r.filter((x) => litIds.some((id) => x.v.has(id))).length, r.length]; });
  anyLit.forEach(([k, n], i) => console.log(`- ${arms2[i]}: ${pct(k, n)}`));
  if (anyLit.length === 2) { const [a, b] = anyLit.map(([k, n]) => wilson(k, n)); console.log(`- intervals overlap: ${a[1] >= b[0] && b[1] >= a[0] ? 'yes' : '**no**'}`); }
  console.log('\n## Rules broken per page\n');
  for (const arm of arms2) {
    for (const kind of ['literal', 'proxy']) {
      const ids = RULES.filter((r) => r[1] === kind).map((r) => r[0]);
      const r = rows[arm].filter((x) => x.produced);
      const per = r.map((x) => ids.filter((id) => x.v.has(id)).length);
      const mean = per.reduce((s, n) => s + n, 0) / (per.length || 1);
      const zero = per.filter((n) => n === 0).length;
      console.log(`- ${arm} ${kind}: mean ${mean.toFixed(2)} of ${ids.length}; clean pages ${pct(zero, per.length)}`);
    }
  }
  console.log('\n## Per case\n');
  const cases = [...new Set(Object.values(rows).flat().map((x) => x.caseId))];
  console.log(`| case | ${arms2.map((a) => `${a} fired · literal mean`).join(' | ')} |`);
  console.log(`| --- |${' --- |'.repeat(arms2.length)}`);
  const lit = RULES.filter((r) => r[1] === 'literal').map((r) => r[0]);
  for (const c of cases) {
    console.log(`| \`${c}\` | ` + arms2.map((arm) => {
      const r = rows[arm].filter((x) => x.caseId === c);
      const p = r.filter((x) => x.produced);
      const m = p.reduce((s, x) => s + lit.filter((id) => x.v.has(id)).length, 0) / (p.length || 1);
      return `${r.filter((x) => x.fired).length}/${r.length} · ${m.toFixed(2)}`;
    }).join(' | ') + ' |');
  }
}

function selfCheck() {
  const t = (id, s) => { const [, , src, f] = RULES.find((r) => r[0] === id); return !re(clean(src), f).test(s); };
  console.assert(t('gradient_headline', 'h1{-webkit-background-clip: text}'), 'gradient');
  console.assert(!t('pure_black_white', 'a{color:#fffff0}') && t('pure_black_white', 'a{background:#FFF}'), 'bw');
  console.assert(t('transition_all', 'a{transition: .3s ease}') && !t('transition_all', 'a{transition: opacity .3s}'), 'transition');
  console.assert(t('italic_headers', '<h1>Built to <em>think</em></h1>') && !t('italic_headers', '<h2><i class="icon"></i> Hi</h2>'), 'italic');
  console.assert(t('emoji_icon', '<span>🚀</span>') && !t('emoji_icon', '<span>ok</span>'), 'emoji');
  console.assert(t('bounce_easing', 'a{transition: transform .3s cubic-bezier(.34,1.56,.64,1)}') && !t('bounce_easing', 'cubic-bezier(.16,1,.3,1)'), 'bounce');
  console.assert(JSON.stringify({ file_path: 'C:\\x\\skills\\hallmark\\references\\slop-test.md' }).replace(/\\\\/g, '/').match(/references\/([\w\-/.]+\.md)/)[1] === 'slop-test.md', 'ref path');
  console.assert(violated({ verdict: 'fail', reason: 'a.css do not match /x/' }) && !violated({ verdict: 'fail', reason: 'no file matches **/*.css' }), 'violated');
}

selfCheck();
const [cmd, ...args] = process.argv.slice(2);
if (cmd === 'suite') console.log(suite());
else if (cmd === 'calibrate') args.forEach(calibrate);
else if (cmd === 'analyse') analyse(Object.fromEntries(args.map((a) => { const [k, v] = a.split('='); return [k, v.split(',')]; })));




