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

---

## Run run-20261107T010150Z-opus48-1344 — 2026-11-07T01:03:23Z

**Result:** no-op — 0 new upstream PRs after checkpoint, 0 docs PRs created.

### Coverage
- Incoming durable checkpoint: `last_processed_merged_at=2026-11-07T00:00:47Z` (unchanged from prior run).
- Merged apache/pinot PRs strictly after checkpoint: **0**.
- Reconciliation (3 independent methods, all agree):
  1. GitHub search API `is:pr is:merged merged:>2026-11-07T00:00:47Z` → total_count=0.
  2. apache/master commits after checkpoint commit `8d140dcf` (#20089) → 0 (master tip == checkpoint PR).
  3. Pulls API (state=closed, sort=updated desc) → newest `merged_at` values all ≤ checkpoint and already in ledger (e.g. #20116, #20158, #20159, #20148 merged 2026-11-05, recently updated by label/comment activity only).
- No gaps; full coverage.

### Decisions
- None — no new PRs to triage.

### Created / Merged docs PRs
- None.

### Validation
- N/A — no docs changes produced this run.

### Blockers
- None.

### Durable state
- Checkpoint **unchanged** `2026-11-07T00:00:47Z`.
- Ledger entries: 83 (unchanged).
- Lease acquired/released via GitHub Git Data API CAS (lease commit `d52a8dec`); no run overlap (prev holder released at 2026-11-07T00:04:16Z).
- No Slack notification (quiet no-op per routine policy).

---

## Run run-20261107T020118Z-909 — 2026-11-07T02:05Z

**Result:** meaningful — 2 upstream PRs triaged (1 docs_created, 1 not_relevant), **1 docs PR created + squash-merged**.

### Coverage
- Incoming durable checkpoint: `last_processed_merged_at=2026-11-07T00:00:47Z`.
- Merged apache/pinot PRs strictly after checkpoint: **2** — #20184 (2026-11-07T01:35:20Z), #20169 (2026-11-07T01:41:31Z).
- Reconciliation (2 independent methods, agree):
  1. GitHub search API `is:pr is:merged merged:>2026-11-07T00:00:47Z` → total_count=2 → {20184, 20169}.
  2. apache/master commits: tip `f60f17fd`=#20169, `bd5cf5e6`=#20184, `8d140dcf`=#20089 (checkpoint).
- No gaps; full coverage.

### Decisions
| PR | Title | Decision | Rationale |
|----|-------|----------|-----------|
| [#20184](https://github.com/apache/pinot/pull/20184) | Clarify review compatibility and style conventions | **not_relevant** | Edits only `kb/code-review-principles.md` and `kb/skills/review-naming-api.md` — internal repo knowledge-base / AI code-review guidance, not user-facing Pinot product docs. No product behavior/config/API/default change (license checks exclude `kb/**`). Not applicable to pinot-docs. |
| [#20169](https://github.com/apache/pinot/pull/20169) | Reject cross-table functions under row-level security | **docs_created** | Security fix (labels: bug, release-notes, security). Single-stage broker now rejects queries calling `lookup()` / `IN_SUBQUERY` / `IN_PARTITIONED_SUBQUERY` with `403 Permission denied` (`QueryErrorCode.ACCESS_DENIED`) when row filters apply to the queried table, closing a row-enumeration leak via `IN_PARTITIONED_SUBQUERY`. Verified from merged code: `RequestUtils.CROSS_TABLE_FUNCTIONS = Set.of("lookup","insubquery","inpartitionedsubquery")`; broker message `Cross-table functions are not allowed on table <table> when row-level security filters apply`. PR explicitly requested a pinot-docs follow-up. |

### Created / Merged docs PRs
- [pinot-contrib/pinot-docs#1166](https://github.com/pinot-contrib/pinot-docs/pull/1166) — "Document rejection of cross-table functions under row-level security (apache/pinot#20169)". Edited `operate-pinot/access-control.md` (canonical RLS page): added subsection "Cross-table functions are rejected under row filters" (+20/-0). **Squash-merged 2026-11-07T02:04:00Z** (commit `ea518854`); branch deleted.
- Upstream comment: https://github.com/apache/pinot/pull/20169#issuecomment-6700755122

### Validation
- `git diff --check`: passed.
- `scripts/validate-docs.py --summary-only`: **RESULT=PASS** (638 files, 3563 links; the 10 broken-anchor warnings are pre-existing and unrelated to `access-control.md`).
- PR CI: "Validate changed docs" SUCCESS, "Full docs audit (informational)" SUCCESS, both GitBook deployments SUCCESS.

### Blockers
- None. (Note: HTTPS git credential helper was unset at session start; `gh auth setup-git` resolved the docs push. `gh pr merge` reported exit-1 via wrapper noise but the squash-merge completed — verified `merged=true` via API.)

### Durable state
- Checkpoint **advanced** `2026-11-07T00:00:47Z` → `2026-11-07T01:41:31Z` (= #20169 merged_at; both PRs triaged).
- Ledger entries: 83 → 85.
- Lock acquired atomically via Contents API create-without-sha (holder `run-20261107T020118Z-909`); released at run end.
- Slack summary sent (meaningful change: new docs PR created+merged).
