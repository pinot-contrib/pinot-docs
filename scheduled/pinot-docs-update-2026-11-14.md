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

## Run run-20261114T020102Z-opus48-cloud — 2026-11-14T02:04:49Z

**Result:** no-op. 0 new upstream PRs after checkpoint. No docs PR created.

### Coverage
- Checkpoint (unchanged): `2026-11-14T00:31:59Z` (#20248).
- Ledger: 148 processed PRs (unchanged).
- Inventory method: 2-way reconcile over the merged-after-checkpoint window.
  - Pulls API `state=closed&sort=updated&direction=desc` (3 pages, 300 rows; max merged_at = `2026-11-14T00:31:59Z` = checkpoint) → **0** PRs with merged_at strictly after checkpoint.
  - Search API `merged:2026-11-14T00:32:00Z..2026-11-14T23:59:59Z` → total_count **0**.
- Git-level reconcile not applicable: local checkout origin is stale fork; apache/pinot GitHub API is authoritative.

### Decisions
- None (no new PRs to triage).

### Created / merged docs PRs
- None.

### Validation
- Not run (no docs changes this run).

### Blockers
- None.

### Notes
- Slack notification: not sent (no new docs PRs created this run).
- Durable state: lock acquired and released via CAS on the `automation-state` branch; checkpoint not advanced (no work).

## Run run-20261114T030113Z-opus48-cloud — 2026-11-14T03:05Z

**Result:** processed 2 PRs → 1 docs_created, 1 not_relevant. Docs PR #1182 created and merged.

### Coverage
- Previous checkpoint: `2026-11-14T00:31:59Z` (#20248).
- New checkpoint: `2026-11-14T02:52:16Z` (#20167).
- Ledger: 148 → 150 processed PRs.
- Inventory method: 2-way reconcile, both agree exactly on 2 PRs strictly after previous checkpoint.
  - Search API `is:pr is:merged merged:>2026-11-14T00:31:59Z` → total_count **2** = #20165, #20167.
  - Pulls API `state=closed&sort=updated&direction=desc&per_page=100` filtered merged_at > CP → same set (#20165 @ 02:36:01Z, #20167 @ 02:52:16Z).
  - Git-level reconcile not applicable (local origin is stale fork; apache/pinot GitHub API authoritative).

### Decisions
| Upstream PR | Merged (UTC) | Decision | Rationale |
|---|---|---|---|
| [#20165](https://github.com/apache/pinot/pull/20165) | 2026-11-14T02:36:01Z | not_relevant | Internal Helm template env-var rename (`ZOO_AUTOPURGE_*`) to match the zookeeper Docker image; user-facing `values.yaml` keys unchanged. No documented interface/config/default change. |
| [#20167](https://github.com/apache/pinot/pull/20167) | 2026-11-14T02:52:16Z | docs_created | Controller `/sql` endpoint now authorizes logical-table queries against every underlying physical table (matching broker). Established a previously-undocumented access-control contract. |

### Created / merged docs PRs
- [pinot-contrib/pinot-docs#1182](https://github.com/pinot-contrib/pinot-docs/pull/1182) — "Document logical table authorization requires READ on all physical tables (apache/pinot#20167)". Merged 2026-11-14T03:04:35Z (merge `6903f1ba`). Upstream comment: https://github.com/apache/pinot/pull/20167#issuecomment-6870680808
  - Change: new "Querying logical tables" section in `operate-pinot/access-control.md`.

### Validation
- `validate-docs.py --summary-only` → PASS (638 files, 3564 links; 0 broken file links; 10 broken anchors pre-existing on clean latest, none in edited file; 0 new failures).
- `git diff --check` clean.

### Blockers
- None.

### Notes
- Slack notification: sent (1 new docs PR created this run).
- Durable state: lock acquired/released via CAS on the `automation-state` branch; checkpoint advanced `2026-11-14T00:31:59Z` → `2026-11-14T02:52:16Z`.

## 2026-11-14T04:02:23Z — run-20261114T040105Z-opus48-cloud (no-op)

### Coverage
- Checkpoint (unchanged): `2026-11-14T02:52:16Z` (#20167).
- 2-way reconcile agrees: **0 PRs** merged strictly after checkpoint.
  - Search API `repo:apache/pinot is:pr is:merged merged:>2026-11-14T02:52:16Z` → total_count **0**.
  - pulls API `state=closed&sort=updated&direction=desc&per_page=100` ×3 pages (247 merged rows; oldest merged_at 2025-08-11T08:12:09Z ≪ CP proving full window coverage) → 0 with merged_at > CP; newest = #20167 @ 02:52:16Z (== checkpoint, already ledgered).
  - Git-level reconcile N/A (local /workspace/pinot origin = stale fork xiangfu0/pinot @ #19809; apache/pinot GitHub API authoritative).

### Decisions
- None. No new docs-relevant PRs.

### Created / merged docs PRs
- None.

### Validation
- N/A (no docs changes).

### Blockers
- None.

### Notes
- Preflight: GH_TOKEN account xiangfu0; apache/pinot = **WRITE**, pinot-contrib/pinot-docs = **ADMIN**. Durable read + CAS lock/release via Contents API on `automation-state` branch.
- Slack: not sent (no-op; webhook reserved for runs that create docs PRs).
- Checkpoint unchanged; ledger stays 150.

---

## Run run-20261114T050109Z-opus48-cloud (2026-11-14T05:02:45Z)
- **Result:** no-op. Coverage: merged PRs reconciled via REST (closed+merged, 3 pages, 247 rows) and apache/pinot master commits. Newest master commit `c31a588ac` = #20167 merged `2026-11-14T02:52:16Z`, equal to checkpoint; **0 PRs merged strictly after checkpoint**.
- **Decisions:** none (nothing new to triage).
- **Docs PRs:** none created/merged.
- **Validation:** N/A (no docs changes).
- **Durable state:** lease acquired + released via CAS on `automation-state`; checkpoint unchanged (`2026-11-14T02:52:16Z`); ledger 150.
- **Slack:** not sent (no-op).
- **Blockers:** none.
