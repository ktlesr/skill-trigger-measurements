# Reference-file coverage

skill directory : skills/impeccable
records         : 6
attempts traced : 120
impeccable calls : 56 attempted, 44 executed (11 distinct, not replayable (compiled helper))

> `impeccable` is a compiled launcher, not a Python script. Its own reads
> cannot be observed with an audit hook, so the files that only it could
> open are listed as **not observable** below rather than as never-opened.

| | Files | Bytes |
| --- | --- | --- |
| ships in the skill | 58 | 2,141,499 |
| opened by the agent | 7 | 95,220 |
| loaded by the host on trigger | 1 | 11,951 |
| not observable (behind the binary) | 2 | 1,102,570 |
| **never opened** | **48** | **931,758** |

Never opened: 48/58 files, 931,758 bytes (44% of the skill directory).

## `impeccable` invocations through the permission layer

| Verb | Attempted | Refused | Ran |
| --- | --- | --- | --- |
| `context` | 40 | 9 | 31 |
| `detect` | 12 | 3 | 9 |
| `read` | 3 | 0 | 3 |
| `(no verb)` | 2 | 1 | 1 |
| `npm` | 1 | 0 | 1 |
| `direction` | 1 | 0 | 1 |

## Opened by the agent

| File | Bytes | Attempts |
| --- | --- | --- |
| `skills/impeccable/scripts/impeccable` | 7,639 | 44 |
| `skills/impeccable/scripts/impeccable.cmd` | 7,152 | 35 |
| `skills/impeccable/reference/craft-floor.md` | 4,528 | 16 |
| `skills/impeccable/reference/new-work.md` | 52,849 | 14 |
| `skills/impeccable/reference/onboard.md` | 7,974 | 7 |
| `skills/impeccable/reference/init.md` | 11,574 | 4 |
| `skills/impeccable/reference/bolder.md` | 3,504 | 1 |

## Never opened, by why the file ships

| Group | Files | Bytes |
| --- | --- | --- |
| launcher / browser runtime | 7 | 593,106 |
| documented on-demand reference | 30 | 272,845 |
| sub-agent fallback reference | 4 | 32,317 |
| sub-agent definition | 4 | 31,657 |
| plugin manifest | 2 | 1,277 |
| runtime code | 1 | 556 |

## Never opened

| File | Bytes | Group |
| --- | --- | --- |
| `skills/impeccable/scripts/live-browser.js` | 535,861 | launcher / browser runtime |
| `skills/impeccable/reference/critique.md` | 43,488 | documented on-demand reference |
| `skills/impeccable/reference/live.md` | 36,472 | documented on-demand reference |
| `skills/impeccable/scripts/modern-screenshot.umd.js` | 29,304 | launcher / browser runtime |
| `skills/impeccable/reference/document.md` | 27,844 | documented on-demand reference |
| `skills/impeccable/reference/degraded/finish-reviewer.md` | 15,434 | sub-agent fallback reference |
| `agents/impeccable-finish-reviewer.md` | 15,273 | sub-agent definition |
| `skills/impeccable/reference/hooks.md` | 13,381 | documented on-demand reference |
| `skills/impeccable/reference/visualize.md` | 11,333 | documented on-demand reference |
| `skills/impeccable/reference/adapt.md` | 10,619 | documented on-demand reference |
| `skills/impeccable/scripts/live-browser-ignores.js` | 10,588 | launcher / browser runtime |
| `skills/impeccable/reference/overdrive.md` | 9,212 | documented on-demand reference |
| `skills/impeccable/reference/harden.md` | 8,875 | documented on-demand reference |
| `skills/impeccable/reference/audit.native.md` | 8,503 | documented on-demand reference |
| `skills/impeccable/reference/live-setup.md` | 8,283 | documented on-demand reference |
| `skills/impeccable/scripts/command-metadata.json` | 8,028 | launcher / browser runtime |
| `skills/impeccable/reference/audit.md` | 8,009 | documented on-demand reference |
| `skills/impeccable/reference/optimize.md` | 7,872 | documented on-demand reference |
| `skills/impeccable/reference/degraded/manual-edit-applier.md` | 7,287 | sub-agent fallback reference |
| `agents/impeccable-manual-edit-applier.md` | 7,080 | sub-agent definition |
| `skills/impeccable/reference/polish.md` | 6,737 | documented on-demand reference |
| `skills/impeccable/reference/degraded/asset-producer.md` | 6,208 | sub-agent fallback reference |
| `agents/impeccable-asset-producer.md` | 6,091 | sub-agent definition |
| `skills/impeccable/reference/distill.md` | 5,735 | documented on-demand reference |
| `skills/impeccable/reference/doctor.md` | 5,521 | documented on-demand reference |
| `skills/impeccable/reference/typeset.md` | 5,329 | documented on-demand reference |
| `skills/impeccable/reference/animate.md` | 5,325 | documented on-demand reference |
| `skills/impeccable/reference/layout.md` | 5,238 | documented on-demand reference |
| `skills/impeccable/scripts/live-browser-dom.js` | 5,084 | launcher / browser runtime |
| `skills/impeccable/reference/quieter.md` | 4,958 | documented on-demand reference |
| `skills/impeccable/reference/clarify.md` | 4,684 | documented on-demand reference |
| `skills/impeccable/reference/colorize.md` | 4,623 | documented on-demand reference |
| `skills/impeccable/scripts/live-browser-session.js` | 4,234 | launcher / browser runtime |
| `skills/impeccable/reference/operate.md` | 4,206 | documented on-demand reference |
| `skills/impeccable/reference/android.md` | 4,139 | documented on-demand reference |
| `skills/impeccable/reference/adapt.native.md` | 3,968 | documented on-demand reference |
| `skills/impeccable/reference/ios.md` | 3,863 | documented on-demand reference |
| `skills/impeccable/reference/delight.md` | 3,786 | documented on-demand reference |
| `skills/impeccable/reference/shape.md` | 3,606 | documented on-demand reference |
| `skills/impeccable/reference/extract.md` | 3,409 | documented on-demand reference |
| `skills/impeccable/reference/degraded/documenter.md` | 3,388 | sub-agent fallback reference |
| `skills/impeccable/reference/routing.md` | 3,267 | documented on-demand reference |
| `agents/impeccable-documenter.md` | 3,213 | sub-agent definition |
| `hooks/hooks.json` | 821 | plugin manifest |
| `skills/impeccable/reference/craft.md` | 560 | documented on-demand reference |
| `.grok-plugin/plugin.json` | 556 | runtime code |
| `.claude-plugin/plugin.json` | 456 | plugin manifest |
| `skills/impeccable/scripts/VERSION` | 7 | launcher / browser runtime |

## Not observable

Only the compiled launcher could open these, and it runs in another
process. Neither read nor unread — outside the instrument.

| File | Bytes |
| --- | --- |
| `skills/impeccable/scripts/data/font-index.json` | 1,100,013 |
| `skills/impeccable/scripts/data/font-index-failures.json` | 2,557 |
