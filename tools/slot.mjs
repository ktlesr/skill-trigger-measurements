// Output-format layer for the phrase-binding arms: arm D's fork template and
// arm E's closing slot. Activation stays in phrase_binding.py; this only reads
// what the model wrote.
//
// Scored with Assay's own file_content_matches evaluator (assay-core 0.4.4), the
// reply handed to it as a one-file workspace. No suite change, no new verdict:
// each check is pass or fail.
//
// Usage: node tools/slot.mjs <assay-core dist/index.js> <A.json> <B.json> [<C.json> ...]
import { readFileSync } from 'node:fs';
import { pathToFileURL } from 'node:url';

const [corePath, ...runs] = process.argv.slice(2);
const { evaluateAssertion } = await import(pathToFileURL(corePath).href);

// Cases whose prompt asks the model to choose between alternatives, fixed
// before any arm D/E attempt was read. "Forks: none" on these is a scorable miss.
const FORKED = new Set([
  'trigger.negative.near_neighbor.pricing_decision', // "$49 or $79"
  'collide.popups.exit_modal_timing',                 // "when and to whom"
  'collide.product_marketing.positioning',            // update the shared file or write elsewhere (§5)
  'collide.product_marketing.icp',                    // which customer, which position
]);
const NEGATIVE = (id) => id.startsWith('trigger.negative.');

const M = '[\\s>*_`-]*';          // markdown a model may wrap a line in
const T = '[\\s*_`.]*$';          // ...and trail it with, then end of reply
const CHECKS = {
  slotEnd:   `(?:^|\\n)${M}Forks:[*_\`\\s]*(?:none|picked\\s.+?\\sover\\s.+?\\sbecause\\s.+?)${T}`,
  slotNone:  `(?:^|\\n)${M}Forks:[*_\`\\s]*none${T}`,
  slotAny:   `(?:^|\\n)${M}Forks:`,
  template:  `^${M}Picking\\s.+?\\sover\\s.+?\\sbecause\\s.+?redirect if wrong`,
  templateLoose: `Picking\\s.+?\\sover\\s.+?\\sbecause\\s`,
};
const check = (name, text) => evaluateAssertion(
  { type: 'file_content_matches', path: 'reply.md', matches: CHECKS[name], flags: 'i' },
  { files: [{ path: 'reply.md', bytes: new TextEncoder().encode(text) }] },
).verdict === 'pass';

const PREAMBLE = 'Base directory for this skill:';   // the Skill tool's, not the model's
const messages = (a) => (a.trace ?? []).filter((e) => e.kind === 'assistant_message')
  .map((e) => (e.text ?? '').trim()).filter((t) => t && !t.startsWith(PREAMBLE));
const firstLine = (t) => t.split('\n').find((l) => l.trim())?.trim() ?? '';

const pct = (k, n) => `${k}/${n}`;
const rows = [];
for (const [i, p] of runs.entries()) {
  const arm = String.fromCharCode(65 + i);
  const run = JSON.parse(readFileSync(p, 'utf8')).run;
  const at = run.cases.flatMap((c) => c.attempts.map((a) => ({ id: c.caseId, a, msgs: messages(a) })));
  const reply = (x) => x.msgs.at(-1) ?? '';
  const forked = at.filter((x) => FORKED.has(x.id));
  const scored = at.filter((x) => !NEGATIVE(x.id));
  const withSlot = at.filter((x) => check('slotEnd', reply(x)));
  rows.push({
    arm, n: at.length,
    slotEnd: withSlot.length,
    slotNone: at.filter((x) => check('slotNone', reply(x))).length,
    slotAny: at.filter((x) => check('slotAny', reply(x))).length,
    slotAnyMsg: at.filter((x) => x.msgs.some((m) => check('slotAny', m))).length,
    forkedN: forked.length,
    forkedSlot: forked.filter((x) => check('slotEnd', reply(x))).length,
    forkedNone: forked.filter((x) => check('slotNone', reply(x))).length,
    perForked: [...FORKED].map((id) => {
      const xs = at.filter((x) => x.id === id);
      return `${id.split('.').slice(-1)[0]} ${xs.filter((x) => check('slotEnd', reply(x))).length}/${xs.filter((x) => check('slotNone', reply(x))).length}/${xs.length}`;
    }).join(' · '),
    tplFirst: scored.filter((x) => check('template', firstLine(x.msgs[0] ?? ''))).length,
    tplAnyOpening: scored.filter((x) => x.msgs.some((m) => check('template', firstLine(m)))).length,
    tplLoose: scored.filter((x) => x.msgs.some((m) => check('templateLoose', m))).length,
    scoredN: scored.length,
    samples: withSlot.map((x) => `${x.id}: ${reply(x).split('\n').filter((l) => l.trim()).at(-1).slice(0, 200)}`),
    tplSamples: scored.filter((x) => x.msgs.some((m) => check('templateLoose', m)))
      .map((x) => `${x.id}: ${x.msgs.flatMap((m) => m.split('\n')).find((l) => new RegExp(CHECKS.templateLoose, 'i').test(l)).trim().slice(0, 200)}`),
  });
}

console.log('## Closing slot (arm E\'s rule), last message of each attempt\n');
console.log('| arm | slot ends the reply | of which `none` | `Forks:` anywhere in the reply | `Forks:` in any message | forked cases: slot · `none` |');
console.log('| --- | --- | --- | --- | --- | --- |');
for (const r of rows) console.log(`| ${r.arm} | ${pct(r.slotEnd, r.n)} | ${r.slotNone} | ${r.slotAny} | ${r.slotAnyMsg} | ${r.forkedSlot} · ${r.forkedNone} of ${r.forkedN} |`);
console.log('\nPer forked case (slot / none / attempts):\n');
for (const r of rows) console.log(`- ${r.arm}: ${r.perForked}`);
console.log('\n## Fork template (arm D\'s rule), scored attempts\n');
console.log('| arm | template on the first line of the first output | template on the first line of any message | "Picking … over … because" anywhere |');
console.log('| --- | --- | --- | --- |');
for (const r of rows) console.log(`| ${r.arm} | ${pct(r.tplFirst, r.scoredN)} | ${r.tplAnyOpening} | ${r.tplLoose} |`);
console.log('\n## Slot lines, for reading by hand\n');
for (const r of rows) for (const s of r.samples) console.log(`- ${r.arm} ${s}`);
console.log('\n## Template lines, for reading by hand\n');
for (const r of rows) for (const s of r.tplSamples) console.log(`- ${r.arm} ${s}`);

// self-check: the regexes pass and fail where they should
if (!check('slotEnd', 'Done.\n\n**Forks: none**') || !check('slotNone', 'x\nForks: none.')
  || !check('slotEnd', 'x\nForks: picked A over B because C') || check('slotEnd', 'Forks: none\n\nMore text')
  || check('slotNone', 'x\nForks: picked A over B because none') || !check('template', '**Picking A over B because C; redirect if wrong.**')
  || check('template', 'I will be picking A')) throw new Error('slot.mjs self-check failed');
