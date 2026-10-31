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

---

# Pinot Docs Update — 2026-10-31 (UTC) — Run 3

**Run:** run-20261031T030116Z-947
**Prior checkpoint:** 2026-10-31T01:22:41Z → **New checkpoint:** 2026-10-31T02:33:56Z

## Coverage
Merged apache/pinot PRs strictly after the prior checkpoint, cross-verified by two independent methods plus master reconciliation:
- GitHub search API (`is:merged merged:>=2026-10-31`, exact `merged_at` filter)
- Authoritative pulls API (`state=closed sort=updated`, 3 pages)
- apache/master commit log reconciliation (HEAD `d226fb5` == #20077; prior #20068 already processed)

Both methods agreed: exactly **1** PR merged strictly after 2026-10-31T01:22:41Z — **#20077** (merged 2026-10-31T02:33:56Z). Coverage complete.

## Decisions

| PR | Title | Decision | Docs |
| --- | --- | --- | --- |
| [#20077](https://github.com/apache/pinot/pull/20077) | Reduce instance selector memory by grouping segments with the same candidates | not_relevant | — |

### #20077 — not relevant
Internal broker instance-selector memory/performance optimization (merge commit `d226fb5`, 30 files +4591/-1405, all under `pinot-broker/.../routing/instanceselector` plus one `pinot-common` map helper). Reindexes per-segment routing state by `CandidateGroup` (shared candidate list) instead of per segment; adds `CandidateGroup`/`GroupRouting`/`SegmentGroups`/`SegmentGroupsBuilder`/`SelectionCollector` and `ImmutableSortedArrayMap.forEach`; removes `NewSegmentState`/`InstanceMapping`.

The PR's "backward incompatible changes" are to **internal Java APIs** used by custom instance selector implementations (`InstanceSelector.select`/`SelectionResult`, `BaseInstanceSelector`, `SegmentStates`, `PriorityPoolInstanceSelector`) — not documented plugin SPI or table configuration. The "behavior changes" are internal routing mechanics (per-server segment ordering follows queried-segment order, atomic routing-state + replica-health publish, per-group/per-server log deduplication, overflow-safe fixed-replica table-name hash). `SINGLE_POOL_SEGMENTS` is a `BrokerMeter` gated by the pre-existing config `pinot.broker.enable.single.pool.segments.metric` (default `false`, unchanged); the PR only broadens which table types emit it when the metric is already enabled.

Verified against merged code: no new config key, query option, function, default, or table-config field (the `QueryOptionKey` references in the diff are existing options appearing in test files). Docs grep confirms no page documents `SINGLE_POOL_SEGMENTS`, `InstanceMapping`, `NewSegmentState`, or the internal `InstanceSelector` API; documented `RoutingConfig.instanceSelectorType` values and selector routing semantics are preserved. No user-facing documentation surface changes.

## Validation
No docs changes created this run — no validation required.

## Blockers
None.

## Durable state
CAS-updated on the `automation-state` branch; lease acquired and released cleanly. No Slack summary (no-op run, zero new docs PRs).

---

# Run 4 — run-20261031T040114Z-873 (2026-10-31 UTC)

## Coverage
Merged apache/pinot PRs strictly after the prior checkpoint `2026-10-31T02:33:56Z`, via the GitHub search API
(`is:merged merged:>=2026-10-31`) with exact `merged_at` filtering. (The local checkout's `origin` is the stale fork
`xiangfu0/pinot`; the authoritative apache/pinot API was used for inventory and merged-code verification.)

3 PRs merged on 2026-10-31: #20068 (01:22:41Z) and #20077 (02:33:56Z) were already processed in prior runs; **#19998**
(03:51:28Z) is the only PR merged strictly after the checkpoint. Coverage complete.

## Decisions

| PR | Title | Decision | Docs |
| --- | --- | --- | --- |
| [#19998](https://github.com/apache/pinot/pull/19998) | Store sealed segment metadata in a mapped sidecar | docs_created | [pinot-docs#1159](https://github.com/pinot-contrib/pinot-docs/pull/1159) |

### #19998 — docs created
Introduces a new user-facing **server instance config** that lets a server load sealed-segment metadata from a local
file-backed `segment_metadata.bin` sidecar instead of retaining it all on heap, substantially reducing heap on servers
hosting many sealed segments.

Verified against merged source (not PR prose):
`IndexLoadingConfig.MAPPED_SEGMENT_METADATA_ENABLED = "segment.metadata.mmap.enabled"` (Javadoc: key relative to
`pinot.server.instance`), read via `instanceConfig.getProperty(MAPPED_SEGMENT_METADATA_ENABLED, false)` → full property
**`pinot.server.instance.segment.metadata.mmap.enabled`**, default **`false`** (disabled). `metadata.properties`
remains canonical; the sidecar is a disposable local cache rebuilt if missing/stale/corrupt, with fallback to eager
on-heap metadata on open failure.

Scope kept minimal: documented only the single instance config row in
`reference/configuration-reference/server.md`. The `SegmentMetadataImpl.loadMapped` standalone API and the on-disk
sidecar binary format are internal/advanced and were not documented.

## Validation
- `git diff --check`: clean.
- `scripts/validate-docs.py --summary-only`: **PASS** — 638 files, 3560 links, 10 broken anchors (all pre-existing;
  identical to the clean-`latest` baseline), 0 orphans, 0 broken SUMMARY refs. No new failures introduced.
- Docs PR checks: "Validate changed docs" SUCCESS, GitBook SUCCESS, "Full docs audit (informational)" SUCCESS.

## Outcome
Docs PR [#1159](https://github.com/pinot-contrib/pinot-docs/pull/1159) squash-merged at 2026-10-31T04:07:00Z
(merge commit `39ea186`). Upstream comment:
https://github.com/apache/pinot/pull/19998#issuecomment-6538800286

## Blockers
None.

## Durable state
Checkpoint advanced to **2026-10-31T03:51:28Z**. State CAS-updated on the `automation-state` branch; lock
acquired and released cleanly. Slack summary sent (1 new docs PR created + merged).
