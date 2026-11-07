# Pinot Docs Update — 2026-11-07 (UTC)

## Run run-20261107T000204Z-opus48-1192 — 2026-11-07T00:04:16Z

**Result:** no-op — 2 upstream PRs triaged, both not_relevant, 0 docs PRs created.

### Coverage
- Incoming durable checkpoint: `last_processed_merged_at=2026-11-06T15:31:25Z`.
- Merged apache/pinot PRs strictly after checkpoint: **2** — #20174, #20089.
- Reconciliation (3 independent methods, all agree):
  1. GitHub search API `is:pr is:merged merged:>2026-11-06T15:31:25Z` → total_count=2.
  2. Pulls API (state=closed, sort=updated desc, per_page=100) → merged-after-cp = {20174, 20089}.
  3. apache/master commits since checkpoint → #20174, #20089; master tip `8d140dcf` = #20089.
- No gaps; full pagination coverage.

### Decisions
| PR | Title | Decision | Rationale |
|----|-------|----------|-----------|
| [#20174](https://github.com/apache/pinot/pull/20174) | Bump org.bitbucket.b_c:jose4j 0.9.6 → 0.9.7 | **not_relevant** | Dependabot semver-patch, single pom.xml (+1/-1). No user-facing behavior/config/API/default/documented-contract change. |
| [#20089](https://github.com/apache/pinot/pull/20089) | Fix rlsFiltersApplied reporting true for multi-stage queries when no RLS filter is applied | **not_relevant** | Code-only correctness fix in pinot-broker (`MultiStageBrokerRequestHandler.java` + test). Makes multi-stage skip empty RLS filter lists (as single-stage already does) so the public `rlsFiltersApplied` response field + `RLS_FILTERS_APPLIED` meter report `true` only when a predicate is actually injected. **pinot-docs `latest` already documents the correct intended behavior** (`operate-pinot/access-control.md`: "When no RLS filters are in effect, the field is set to `false`"; `reference/api-reference/query-response-format.md`: "Whether row-level security predicates were injected"). Fix aligns implementation with existing docs — no documentation change needed. |

### Created / Merged docs PRs
- None.

### Validation
- N/A — no docs changes produced this run.

### Blockers
- None.

### Durable state
- Checkpoint **advanced** `2026-11-06T15:31:25Z` → `2026-11-07T00:00:47Z` (= #20089 merged_at; both PRs triaged).
- Ledger entries: 81 → 83.
- Lease acquired/released via GitHub Git Data API CAS; no run overlap.
- No Slack notification (quiet no-op per routine policy).
