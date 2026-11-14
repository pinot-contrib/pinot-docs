# Pinot Docs Update — 2026-11-14 (UTC)

Automation: pinot-docs maintenance from merged apache/pinot PRs (IntentLab routine, replaces Codex `convert-apache-pinot-prs-to-pinot-docs`).

## Run run-20261114T010109Z-opus48-cloud — 2026-11-14T01:05:38Z

**Result:** processed 1 PR → not_relevant. No docs PR created.

### Coverage
- Previous checkpoint: `2026-11-13T21:29:51Z` (#20256).
- New checkpoint: `2026-11-14T00:31:59Z` (#20248).
- Ledger: 147 → 148 processed PRs.
- Inventory method: 3-way reconcile.
  - Search API `repo:apache/pinot is:pr is:merged merged:>=2026-11-13` → 16 items; exactly **1** with merged_at strictly after previous checkpoint: #20248.
  - Authoritative pulls API `state=closed&sort=updated&direction=desc&per_page=100` (2 pages, 200 rows; oldest updated_at `2026-10-25T10:58:06Z`, well before checkpoint → full window coverage) → same single PR #20248.
  - Git-level reconcile not applicable: local checkout origin is stale fork (xiangfu0/pinot, 1 commit); apache/pinot GitHub API is authoritative.

### Decisions
| Upstream PR | Merged (UTC) | Decision | Rationale |
|---|---|---|---|
| [#20248](https://github.com/apache/pinot/pull/20248) — Check the intermediate result ser/de of every aggregation function type | 2026-11-14T00:31:59Z | **not_relevant** | Test-only. Single file `pinot-core/src/test/java/org/apache/pinot/core/query/aggregation/function/IntermediateResultByteBufferSerDeTest.java` (+194/-8). Expands coverage so `IntermediateResultByteBufferSerDeTest` accounts for every `AggregationFunctionType`. Labels: functions, serialization, test-coverage. No production code, config, public API/SPI, wire format, or documented-default change → nothing user-facing to document. |

### Created / merged docs PRs
- None.

### Validation
- Not run (no docs changes this run).

### Blockers
- None.

### Notes
- Slack notification: not sent (no new docs PRs created this run).
