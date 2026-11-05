# Pinot Docs Update — 2026-11-05 (UTC)

_This daily report accumulates all runs for 2026-11-05 (UTC), newest first._

---

# Pinot Docs Update — 2026-11-05 (run run-20261105T010135Z-opus48-1067)

**Run start:** 2026-11-05T01:01:35Z · **Model:** Opus 4.8 (claude-opus-4-8) · **Result:** 1 docs PR created and merged

## Checkpoint
- Incoming `last_processed_merged_at`: `2026-11-05T00:00:06Z`
- Outgoing `last_processed_merged_at`: `2026-11-05T00:47:33Z` (= apache/pinot#20154 merged_at)

## Coverage
Merged apache/pinot PRs strictly after the incoming checkpoint: **1** (#20154).
Verified by two agreeing methods:
1. `search/issues is:pr is:merged merged:>=2026-11-04` (6 items) → precise `merged_at` filter leaves only #20154 (@ 2026-11-05T00:47:33Z) strictly after checkpoint. #20156 is exactly at the checkpoint (already ledgered); #19907/#20150/#20152/#20155 are before it (already ledgered).
2. apache/master commit log since 2026-11-05T00:00:00Z → HEAD `091eac79` (#20154), parent `2bacc888` (#20156 == checkpoint). No gaps.

## Decisions
| PR | Title | Decision | Docs |
|----|-------|----------|------|
| apache/pinot#20154 | Fix HyperLogLogPlus max byte size and reject sp above 25 | **docs_created** | pinot-contrib/pinot-docs#1162 (merged) |

### #20154 rationale
Backward-incompatible, user-facing (labels: bug, release-notes, backward-incompat, query, ingestion, star-tree, functions). Verified from merged code:
- `HyperLogLogPlusUtils.MAX_SP = 25`; `validateSp` enforces `sp <= 25`.
- `DistinctCountHLLPlusValueAggregator.isAggregatedValueFixedSize()` returns `_sp == 0`.

Effects: `sp > 25` now rejected in `DISTINCTCOUNTHLLPLUS`, `DISTINCTCOUNTRAWHLLPLUS`, their `*MV` variants, `DISTINCTCOUNTSMARTHLLPLUS`, and the HLL++ value aggregator; ingestion/star-tree HLL++ aggregation with `sp > 0` now fails table config validation. Pre-existing star-tree docs used the now-invalid `{"p": 16, "sp": 32}` example.

## Docs PR #1162
Branch `cs_Ubh1PrgvFK/docs/hllplus-sp-max-20154`. Files:
- `build-with-pinot/indexing/star-tree-index.md` — fix invalid `sp=32` examples; note `sp=0` required for star-tree + `sp<=25`.
- `functions/sketch/distinctcounthllplus.md`, `distinctcountrawhllplus.md`, `distinctcounthllplusmv.md`, `distinctcountrawhllplusmv.md` — note `sp<=25`; add SMARTHLLPLUS `sp` param note.
- `build-with-pinot/ingestion/ingestion-level-aggregations.md` — correct signature to `(field, p, sp)`; note `sp=0` required for ingestion aggregation.

## Validation
- `git diff --check`: clean.
- `uv run --with pyyaml python scripts/validate-docs.py --summary-only`: **PASS** (10 broken anchors are pre-existing on `latest` baseline, unrelated to changed files).
- CI checks: "Validate changed docs" success, "Full docs audit" success, GitBook ×2 success.
- Squash-merged sha `006155c2` at 2026-11-05T01:05:26Z; merge verified.

## Links
- Upstream PR: https://github.com/apache/pinot/pull/20154
- Docs PR (merged): https://github.com/pinot-contrib/pinot-docs/pull/1162
- Upstream comment: https://github.com/apache/pinot/pull/20154#issuecomment-6646724154

## Blockers
None. Lock/lease acquired and released via Contents API CAS. Durable state, memory, and report persisted.

---

## Earlier run(s) on 2026-11-05

# Pinot Docs Update — 2026-11-05 (UTC)

**Run:** run-20261105T000122Z-opus48-887
**Finished:** 2026-11-05T00:03:15Z
**Model:** Opus 4.8 (claude-opus-4-8), IntentLab scheduled hourly triage
**Result:** no-op — 1 upstream PR triaged, classified not_relevant; 0 docs PRs created.

## Checkpoint
- Incoming: `last_processed_merged_at = 2026-11-04T22:34:28Z`
- Outgoing: `last_processed_merged_at = 2026-11-05T00:00:06Z` (= #20156 merged_at)

## Coverage (merged apache/pinot PRs strictly after incoming checkpoint)
Three agreeing inventory methods, all returning exactly **#20156**:
1. pulls API (`state=closed base=master sort=updated desc per_page=100`) — #20156 @ 2026-11-05T00:00:06Z is the only merged PR strictly after checkpoint.
2. search API (`is:pr is:merged merged:>2026-11-04T22:34:28Z`) — total_count=1 (#20156).
3. apache/pinot master commit log — HEAD `2bacc888` (#20156), parent `3e7342c5` (#20155, the prior checkpoint PR). No gap.

## Decisions
| PR | Title | Author | Decision | Rationale |
|----|-------|--------|----------|-----------|
| [#20156](https://github.com/apache/pinot/pull/20156) | Bump dnsjava:dnsjava from 3.7.0 to 3.7.1 | dependabot[bot] | **not_relevant** | Single `pom.xml` line (+1/-1), patch bump of a transitive DNS library. No config key, default, query option, function, public API, or documented user-facing behavior change. Verified from merged diff (merge commit 2bacc8889b). |

## Docs PRs created / merged
None.

## Validation
No docs changes made, so no docs-repo validation was required this run.

## Blockers
None. Lock acquired and released cleanly via Contents API CAS (transient 409 on acquire reconciled by re-read confirming self-held lock). apache/pinot=WRITE, pinot-contrib/pinot-docs=ADMIN confirmed read-only.

## Notifications
No Slack notification (no-op run; no new docs PR).
