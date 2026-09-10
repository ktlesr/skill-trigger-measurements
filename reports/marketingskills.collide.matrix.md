## Per case

| Case | Expected | Attempts | First to fire | All that fired | Verdict |
| --- | --- | --- | --- | --- | --- |
| `collide.signup.registration_form` | signup | 10 | (none)×10 | — | 0/10 expected won |
| `collide.cro.lead_form` | cro | 10 | (none)×5, cro×4, signup×1 | cro×4, signup×1 | 4/10 expected won |
| `collide.popups.exit_modal_wording` | popups | 10 | (none)×10 | — | 0/10 expected won |
| `collide.popups.exit_modal_timing` | popups | 10 | (none)×10 | — | 0/10 expected won |
| `collide.cro.pricing_page` | cro | 10 | (none)×10 | — | 0/10 expected won |
| `collide.paywalls.limit_screen` | paywalls | 10 | (none)×10 | — | 0/10 expected won |
| `collide.onboarding.first_session` | onboarding | 10 | (none)×10 | — | 0/10 expected won |
| `contested.copywriting.headline_better` | copywriting | 10 | (none)×10 | — | contested, not scored |
| `collide.copy_editing.tighten_paragraph` | copy-editing | 10 | (none)×10 | — | 0/10 expected won |
| `collide.emails.welcome_sequence` | emails | 10 | emails×10 | emails×10 | 10/10 expected won |
| `collide.cold_email.outreach` | cold-email | 10 | cold-email×6, (none)×4 | cold-email×6 | 6/10 expected won |
| `collide.seo_audit.not_found` | seo-audit | 10 | seo-audit×10 | seo-audit×10 | 10/10 expected won |
| `collide.ai_seo.cited` | ai-seo | 10 | ai-seo×10 | ai-seo×10 | 10/10 expected won |
| `collide.programmatic_seo.integration_pages` | programmatic-seo | 10 | (none)×10 | — | 0/10 expected won |
| `collide.schema.star_ratings` | schema | 10 | schema×9, (none)×1 | schema×9 | 9/10 expected won |
| `collide.product_marketing.positioning` | product-marketing | 10 | (none)×10 | — | 0/10 expected won |
| `collide.product_marketing.icp` | product-marketing | 10 | (none)×10 | — | 0/10 expected won |
| `trigger.negative.near_neighbor.pricing_decision` | — | 10 | (none)×10 | — | 0/10 fired (should be 0) |
| `trigger.negative.near_neighbor.form_crash` | — | 10 | (none)×10 | — | 0/10 fired (should be 0) |
| `trigger.negative.unrelated.slow_query` | — | 10 | (none)×10 | — | 0/10 fired (should be 0) |

## Collision matrix (rows: expected, cols: first skill to fire)

| expected \ fired | (none) | ai-seo | cold-email | cro | emails | schema | seo-audit | signup |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| **ai-seo** |  | 10 |  |  |  |  |  |  |
| **cold-email** | 4 |  | 6 |  |  |  |  |  |
| **copy-editing** | 10 |  |  |  |  |  |  |  |
| **cro** | 15 |  |  | 4 |  |  |  | 1 |
| **emails** |  |  |  |  | 10 |  |  |  |
| **onboarding** | 10 |  |  |  |  |  |  |  |
| **paywalls** | 10 |  |  |  |  |  |  |  |
| **popups** | 20 |  |  |  |  |  |  |  |
| **product-marketing** | 20 |  |  |  |  |  |  |  |
| **programmatic-seo** | 10 |  |  |  |  |  |  |  |
| **schema** | 1 |  |  |  |  | 9 |  |  |
| **seo-audit** |  |  |  |  |  |  | 10 |  |
| **signup** | 10 |  |  |  |  |  |  |  |

## product-marketing claim

- activations (any marketing skill fired): 50
- read `.agents/product-marketing.md` at all: 17
- read it before the first edit (or made no edit): 17
- product-marketing skill itself fired in: 0
- control, attempts where no marketing skill fired: read it in 14/150

## Host-bundled skills that fired

`run`×1

## Work done without any marketing skill

- positive attempts where no marketing skill fired: 120
- of those, the agent still wrote files: 93
