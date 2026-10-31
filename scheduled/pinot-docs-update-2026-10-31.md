# Pinot Docs Update — 2026-10-31 (UTC)

**Run:** run-20261031T000101Z-811
**Prior checkpoint:** 2026-10-30T22:13:55Z → **New checkpoint:** 2026-10-30T23:24:38Z

## Coverage
Merged apache/pinot PRs strictly after the prior checkpoint, cross-verified by three independent methods:
- GitHub search API (`is:merged merged:>=2026-10-30`, exact `merged_at` filter)
- Authoritative pulls API (`state=closed base=master`, full pagination)
- apache/master commit log since checkpoint (tip `eca9ea7a` == #20084)

All three agreed: exactly **2** PRs — #20098, #20084. (#20097 merged AT the checkpoint boundary and was already processed last run; correctly excluded.) Coverage complete.

## Decisions

| PR | Title | Decision | Docs |
| --- | --- | --- | --- |
| [#20098](https://github.com/apache/pinot/pull/20098) | Merge final results of array, raw sketch and other aggregation functions | **docs_created** | [pinot-docs #1158](https://github.com/pinot-contrib/pinot-docs/pull/1158) (merged) |
| [#20084](https://github.com/apache/pinot/pull/20084) | Reuse the shared hybrid cluster for tenant rebalance tests | not_relevant | — |

### #20098 — docs created
Follow-up to #20074. Most of the 38-file change is internal `mergeFinalResult` correctness for the `serverReturnFinalResult` / `is_leaf_return_final_result` paths with no SQL-surface impact. Two user-visible changes (ship in Apache Pinot 1.7.0), both verified against merged code at `96fe714`:
1. **LISTAGG** returns `null` instead of an empty string when it aggregates no values (multi-stage engine) → `functions/aggregation/listagg.md`.
2. **DISTINCTCOUNTRAWULL** result column name fixed from `distinctcountull(col)` to `distinctcountrawull(col)` for unaliased queries → `functions/sketch/distinctcountrawull.md`.

- **Docs PR:** pinot-contrib/pinot-docs#1158 — merged 2026-10-31T00:06:48Z (squash)
- **Upstream comment:** https://github.com/apache/pinot/pull/20098#issuecomment-6536227665

### #20084 — not relevant
Integration-test harness only (4 files under `pinot-integration-tests/`; "No production code changes"). Runs TenantRebalance dry-run tests inside the shared hybrid suite for a ~17% test-time reduction. No production/config/API/doc surface.

## Validation
- `git diff --check`: clean
- `scripts/validate-docs.py --summary-only`: **PASS** (10 broken-anchor WARNINGs confirmed pre-existing via origin/latest baseline diff; none introduced)
- Docs PR checks: "Validate changed docs" SUCCESS, "Full docs audit" SUCCESS, GitBook SUCCESS

## Blockers
None.

## Durable state
CAS-updated on the `automation-state` branch; lease acquired and released cleanly. Slack summary sent (1 new docs PR).

---

# Pinot Docs Update — 2026-10-31 (UTC) — Run 2

**Run:** run-20261031T020141Z-1410
**Prior checkpoint:** 2026-10-30T23:24:38Z → **New checkpoint:** 2026-10-31T01:22:41Z

## Coverage
Merged apache/pinot PRs strictly after the prior checkpoint, cross-verified by two independent methods plus master reconciliation:
- GitHub search API (`is:merged merged:>=2026-10-30`, 10 PRs, exact `merged_at` filter)
- Authoritative pulls API (`state=closed sort=updated`, 3 pages / 248 merged PRs, oldest in window 2025-08-11 so coverage is complete)
- apache/master commit log reconciliation (#20068 present)

Both methods agreed: exactly **1** PR merged strictly after 2026-10-30T23:24:38Z — **#20068** (merged 2026-10-31T01:22:41Z). All other merged PRs were already in the ledger or at/before the checkpoint. Coverage complete.

## Decisions

| PR | Title | Decision | Docs |
| --- | --- | --- | --- |
| [#20068](https://github.com/apache/pinot/pull/20068) | Add requiresFetch flag to a segment to for prefetch planning | not_relevant | — |

### #20068 — not relevant
Internal query-engine prefetch-planning optimization (merge commit `66eb74d6`, 8 files +402/-41). Adds a backward-compatible `default boolean requiresFetch() { return false; }` to the `@InterfaceAudience.Private` SPI interfaces `IndexSegment` and `SegmentDirectory`, consumed by `FetchPlanner` and `BloomFilterSegmentPruner` to decide whether a segment needs a fetch context during prefetch planning. Verified against merged code: private audience, default no-op method, changes confined to `pinot-core` query internals and `pinot-segment-spi` private interfaces plus tests (`InstancePlanMakerPrefetchTest`, `BloomFilterSegmentPrunerTest`). No user-facing config, table/query option, documented default, or wire/serialization change. Dedup: no prior docs PR or upstream comment references #20068.

## Validation
No docs changes created this run — no validation required.

## Blockers
None.

## Durable state
CAS-updated on the `automation-state` branch; lease acquired and released cleanly. No Slack summary (no-op run, zero new docs PRs).
