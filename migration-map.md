# Pinot Docs Migration Map

This file is the lead-owned map for restructuring the docs into the target information architecture.

## Operating Rules

1. `SUMMARY.md` is the single source of truth for navigation.
2. Only the lead edits `SUMMARY.md`, aliases, redirects, breadcrumbs, compatibility wrapper pages, or shared landing pages.
3. Existing public URLs must keep working through unchanged pages, wrapper pages, or compatibility redirects implemented as Markdown pages.
4. Preserve strong existing pages. Prefer regrouping and thinner landing pages over rewriting good content.
5. Narrative docs belong in `Build with Pinot`. Dense config, property, and endpoint material belongs in `Reference`.
6. The standalone `Functions` top-level must disappear from navigation and be folded under `Querying & SQL`.
7. `Integrations` plus `APIs & Clients` must be merged into a user-intent section.
8. API material is split into a lighter overview in `Build with Pinot` and detailed endpoint docs in `Reference`.
9. A dedicated `SSE vs MSE` decision page must be created from current engine, join, and function-engine material.
10. Code snippets and dependency examples in these areas need a version-consistency sweep.
11. Every reworked landing, overview, or compatibility page in scope should end with:
    - `What this page covered`
    - `Next step`
    - `Related pages`

## Target Navigation

## Build with Pinot

- `build-with-pinot/README.md`
- `build-with-pinot/data-modeling/README.md`
- `build-with-pinot/ingestion/README.md`
- `build-with-pinot/querying-and-sql/README.md`
  - `build-with-pinot/querying-and-sql/querying-pinot.md`
  - `build-with-pinot/querying-and-sql/sql-syntax.md`
  - `build-with-pinot/querying-and-sql/functions/README.md`
  - `build-with-pinot/querying-and-sql/sse-vs-mse.md`
  - `build-with-pinot/querying-and-sql/query-execution-controls/README.md`
- `build-with-pinot/indexing/README.md`
- `build-with-pinot/connectors-clients-apis/README.md`
  - `build-with-pinot/connectors-clients-apis/client-libraries.md`
  - `build-with-pinot/connectors-clients-apis/bi-tools.md`
  - `build-with-pinot/connectors-clients-apis/query-engines.md`
  - `build-with-pinot/connectors-clients-apis/processing-connectors.md`
  - `build-with-pinot/connectors-clients-apis/rest-grpc-apis.md`

## Reference

- `reference/README.md`
- `reference/configuration-reference/README.md`
- `reference/api-reference/README.md`
- `reference/plugin-reference/README.md`
- `reference/release-notes/README.md`

## Ownership

## Lead IA / Integrator

Writes:

- `migration-map.md`
- `SUMMARY.md`
- `build-with-pinot/README.md`
- `build-with-pinot/querying-and-sql/README.md`
- `build-with-pinot/connectors-clients-apis/README.md`
- `reference/README.md`
- compatibility wrapper pages in existing public paths

Also owns:

- previous/next flow
- breadcrumb cleanup
- navigation integration
- redirect and alias strategy
- final merge

## Agent 1: Data modeling + Ingestion

Writes only:

- `build-with-pinot/data-modeling/**/*`
- `build-with-pinot/ingestion/**/*`

Primary source material:

- `basics/components/table/schema.md`
- `basics/components/table/README.md`
- `basics/components/table/logical-table.md`
- `tutorials/data-ingestion/schema-evolution.md`
- `manage-data/data-import/**/*`
- `developers/advanced/data-ingestion.md`
- `developers/advanced/ingestion-level-transformations.md`
- `developers/advanced/ingestion-level-aggregations.md`
- `configuration-reference/schema.md`
- `configuration-reference/table.md`
- `configuration-reference/ingestion.md`

## Agent 2: Querying Pinot + SQL behavior

Writes only:

- `build-with-pinot/querying-and-sql/querying-pinot.md`
- `build-with-pinot/querying-and-sql/sql-syntax.md`
- `build-with-pinot/querying-and-sql/query-execution-controls/**/*`

Primary source material:

- `users/user-guide-query/README.md`
- `users/user-guide-query/querying-pinot.md`
- `users/user-guide-query/sql-reference.md`
- `users/user-guide-query/query-syntax-overview.md`
- `users/user-guide-query/query-options.md`
- `users/user-guide-query/query-quotas.md`
- `users/user-guide-query/query-cancellation.md`
- `users/user-guide-query/query-using-cursors.md`
- `users/user-guide-query/query-correlation-id.md`
- `users/user-guide-query/explain-plan.md`
- `users/user-guide-query/explain-plan-multi-stage.md`

## Agent 3: Functions + SSE vs MSE

Writes only:

- `build-with-pinot/querying-and-sql/functions/**/*`
- `build-with-pinot/querying-and-sql/sse-vs-mse.md`

Primary source material:

- `users/user-guide-query/function-index.md`
- `users/user-guide-query/supported-transformations.md`
- `functions/**/*`
- `reference/single-stage-engine.md`
- `reference/multi-stage-engine.md`
- `developers/advanced/v2-multi-stage-query-engine.md`
- `users/user-guide-query/joins.md`
- `users/user-guide-query/multi-stage-query/**/*`

## Agent 4: Indexing

Writes only:

- `build-with-pinot/indexing/**/*`

Primary source material:

- `basics/indexing/**/*`
- `manage-data/data-import/pinot-stream-ingestion/configure-indexes.md`
- `configuration-reference/table.md`
- `users/user-guide-query/**/*`

## Agent 5: Connectors, clients & APIs

Writes only:

- `build-with-pinot/connectors-clients-apis/client-libraries.md`
- `build-with-pinot/connectors-clients-apis/bi-tools.md`
- `build-with-pinot/connectors-clients-apis/query-engines.md`
- `build-with-pinot/connectors-clients-apis/processing-connectors.md`
- `build-with-pinot/connectors-clients-apis/rest-grpc-apis.md`

Primary source material:

- `integrations/**/*`
- `users/clients/**/*`
- `users/api/README.md`
- `users/api/broker-grpc-api.md`
- `users/api/querying-pinot-using-standard-sql/**/*`
- `users/api/pinot-rest-admin-interface.md`
- `users/api/controller-api-reference.md`
- `basics/getting-started/kubernetes/query-engines.md`

## Agent 6: Reference + compat QA

Writes only:

- `reference/configuration-reference/**/*`
- `reference/api-reference/**/*`
- `reference/plugin-reference/**/*`
- `reference/release-notes/**/*`

Primary source material:

- `configuration-reference/**/*`
- `users/api/**/*`
- `basics/releases/**/*`
- `reference/*.md`

QA responsibility after lead integration:

- broken links
- duplicate H1s
- orphan pages
- stale overview pages
- redirect coverage
- mixed stable/master version messaging

## Current to Target Mapping

| Current area | Target area | Notes |
| --- | --- | --- |
| `manage-data/data-import/**/*` | `Build with Pinot > Ingestion` | Reframe around ingestion workflows and choices; keep detailed source pages intact where strong. |
| `basics/components/table/**/*` + schema tutorials | `Build with Pinot > Data modeling` | Separate modeling guidance from dense config reference. |
| `users/user-guide-query/**/*` | `Build with Pinot > Querying & SQL` | Keep narrative and task-oriented guidance here. |
| `functions/**/*` | `Build with Pinot > Querying & SQL > Functions` | Fold navigation, preserve existing function pages where possible. |
| `reference/single-stage-engine.md` + `reference/multi-stage-engine.md` + MSE docs | `Build with Pinot > Querying & SQL > SSE vs MSE` | New decision guide with links to deeper engine docs. |
| `basics/indexing/**/*` | `Build with Pinot > Indexing` | Keep chooser/decision content and tie to table config/query patterns. |
| `integrations/**/*` + `users/clients/**/*` + API overview docs | `Build with Pinot > Connectors, clients & APIs` | Merge by user intent. |
| `users/api/**/*` | `Reference > API reference` | Split overview from detailed endpoint material. |
| `configuration-reference/**/*` | `Reference > Configuration reference` | Dense reference stays dense. |
| `configuration-reference/plugin-reference/**/*` | `Reference > Plugin reference` | Surface separately in navigation. |
| `basics/releases/**/*` | `Reference > Release notes` | Add landing and keep historical pages reachable. |

## Lead Integration Notes

- Prefer compatibility wrapper pages over deleting public pages.
- Reuse existing strong pages in navigation when a move is unnecessary.
- If the same content needs both a task-oriented overview and dense reference, create a thin overview page and point to the original detailed reference page.
