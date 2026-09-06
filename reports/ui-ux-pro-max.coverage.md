# Reference-file coverage

skill directory : skills/ui-ux-pro-max/.claude/skills/ui-ux-pro-max
records         : 2
attempts traced : 200
search.py calls : 83 attempted, 0 executed (51 distinct, replayed)

> **The host's permission layer refused every `search.py` invocation**, so
> the skill's helper never actually ran in this configuration.
> The coverage below is what the *attempted* queries would have opened had
> they been allowed - an upper bound on reach, not an observation of it.

| | Files | Bytes |
| --- | --- | --- |
| ships in the skill | 72 | 3,570,102 |
| opened by the agent | 2 | 25,092 |
| opened by search.py | 13 | 643,105 |
| loaded by the host on trigger | 1 | 15,969 |
| **never opened** | **58** | **2,911,028** |

Never opened: 58/72 files, 2,911,028 bytes (82% of the skill directory).

## Opened by the agent

| File | Bytes | Attempts |
| --- | --- | --- |
| `SKILL.md` | 15,969 | 1 |
| `scripts/search.py` | 9,123 | 1 |

## Opened by search.py

| File | Bytes | Distinct queries |
| --- | --- | --- |
| `scripts/search.py` | 9,123 | 51 |
| `scripts/core.py` | 41,234 | 51 |
| `scripts/reasoning_contract.py` | 5,824 | 51 |
| `scripts/design_system.py` | 70,937 | 51 |
| `data/products.csv` | 75,623 | 50 |
| `data/ui-reasoning.csv` | 77,360 | 35 |
| `data/landing.csv` | 25,449 | 35 |
| `data/typography.csv` | 49,997 | 35 |
| `data/styles.csv` | 149,478 | 35 |
| `data/colors.csv` | 37,940 | 35 |
| `data/motion.csv` | 14,679 | 21 |
| `data/ux-guidelines.csv` | 27,516 | 13 |
| `data/icons.csv` | 57,945 | 2 |

## Search modes attempted (none executed)

| Flag | Invocations |
| --- | --- |
| `--design-system` | 66 |
| `--persist` | 33 |
| `--domain` | 17 |
| `--stack` | 2 |

## Never opened, by why the file ships

| Group | Files | Bytes |
| --- | --- | --- |
| domain data | 8 | 2,092,870 |
| stack data | 22 | 476,731 |
| dev tooling (not a runtime file) | 26 | 305,992 |
| documented on-demand reference | 2 | 35,435 |

## Never opened

| File | Bytes | Group |
| --- | --- | --- |
| `data/phosphor-icons-upstream.json` | 823,933 | domain data |
| `data/google-fonts.csv` | 747,241 | domain data |
| `data/google-font-licenses.json` | 433,127 | domain data |
| `scripts/tests/fixtures/relevance-baseline.json` | 89,436 | dev tooling (not a runtime file) |
| `scripts/validate_data.py` | 52,230 | dev tooling (not a runtime file) |
| `data/stacks/threejs.csv` | 46,051 | stack data |
| `scripts/tests/fixtures/relevance-cases.json` | 36,734 | dev tooling (not a runtime file) |
| `data/data-provenance.json` | 36,686 | domain data |
| `data/stacks/javafx.csv` | 33,577 | stack data |
| `data/stacks/uno.csv` | 30,091 | stack data |
| `data/stacks/winui.csv` | 27,890 | stack data |
| `data/stacks/avalonia.csv` | 27,327 | stack data |
| `data/stacks/uwp.csv` | 24,692 | stack data |
| `references/quick-reference.md` | 24,526 | documented on-demand reference |
| `data/stacks/wpf.csv` | 24,158 | stack data |
| `data/stacks/nuxt-ui.csv` | 24,106 | stack data |
| `data/charts.csv` | 23,365 | domain data |
| `data/stacks/shadcn.csv` | 23,184 | stack data |
| `data/stacks/nuxtjs.csv` | 23,014 | stack data |
| `data/stacks/laravel.csv` | 20,163 | stack data |
| `data/stacks/angular.csv` | 19,863 | stack data |
| `scripts/tests/test_data_contracts.py` | 19,513 | dev tooling (not a runtime file) |
| `scripts/tests/test_catalog_refresh.py` | 19,466 | dev tooling (not a runtime file) |
| `data/stacks/react.csv` | 19,036 | stack data |
| `data/stacks/nextjs.csv` | 18,687 | stack data |
| `scripts/tests/test_core.py` | 16,680 | dev tooling (not a runtime file) |
| `data/stacks/html-tailwind.csv` | 16,551 | stack data |
| `data/stacks/swiftui.csv` | 15,323 | stack data |
| `data/react-performance.csv` | 15,080 | domain data |
| `data/stacks/svelte.csv` | 15,078 | stack data |
| `data/stacks/astro.csv` | 14,591 | stack data |
| `data/stacks/flutter.csv` | 14,192 | stack data |
| `data/stacks/react-native.csv` | 14,049 | stack data |
| `data/stacks/vue.csv` | 12,813 | stack data |
| `data/stacks/jetpack-compose.csv` | 12,295 | stack data |
| `data/app-interface.csv` | 11,046 | domain data |
| `references/pro-rules.md` | 10,909 | documented on-demand reference |
| `scripts/tests/test_core_data_quality.py` | 8,954 | dev tooling (not a runtime file) |
| `scripts/tests/test_relevance_evaluator.py` | 8,430 | dev tooling (not a runtime file) |
| `scripts/tests/test_native_desktop_stack_freshness.py` | 8,170 | dev tooling (not a runtime file) |
| `scripts/tests/test_web_stack_freshness.py` | 7,699 | dev tooling (not a runtime file) |
| `scripts/tests/test_design_system_mode.py` | 7,690 | dev tooling (not a runtime file) |
| `scripts/tests/test_style_taxonomy.py` | 7,425 | dev tooling (not a runtime file) |
| `scripts/tests/test_text_layout_resilience.py` | 5,874 | dev tooling (not a runtime file) |
| `scripts/tests/fixtures/relevance-thresholds.json` | 5,079 | dev tooling (not a runtime file) |
| `scripts/tests/test_skill_script_paths.py` | 4,305 | dev tooling (not a runtime file) |
| `scripts/tests/test_catalog_summary_line_endings.py` | 2,947 | dev tooling (not a runtime file) |
| `data/catalog-summary.json` | 2,392 | domain data |
| `scripts/tests/fixtures/catalogs/google-catalog.json` | 1,772 | dev tooling (not a runtime file) |
| `scripts/tests/fixtures/catalogs/google-api.json` | 1,079 | dev tooling (not a runtime file) |
| `scripts/tests/fixtures/catalogs/phosphor-core.json` | 571 | dev tooling (not a runtime file) |
| `scripts/tests/fixtures/catalogs/icons-curated.csv` | 495 | dev tooling (not a runtime file) |
| `scripts/tests/fixtures/catalogs/google-existing.csv` | 480 | dev tooling (not a runtime file) |
| `scripts/tests/fixtures/catalogs/phosphor-package.json` | 370 | dev tooling (not a runtime file) |
| `scripts/tests/fixtures/catalogs/google-metadata.json` | 328 | dev tooling (not a runtime file) |
| `scripts/tests/fixtures/catalogs/google-overrides.json` | 97 | dev tooling (not a runtime file) |
| `scripts/tests/fixtures/catalogs/phosphor-react-exports.json` | 87 | dev tooling (not a runtime file) |
| `scripts/tests/fixtures/catalogs/phosphor-react-package.json` | 81 | dev tooling (not a runtime file) |
