# Pinot Docs Update — 2026-11-05 (UTC)

_This daily report accumulates all runs for 2026-11-05 (UTC), newest first._

---

# Pinot Docs Update — 2026-11-05 (run run-20261105T020144Z-opus48-1261)

**Run start:** 2026-11-05T02:01:44Z · **Model:** Opus 4.8 (claude-opus-4-8) · **Result:** No-op (no new PRs)

## Checkpoint
- Incoming `last_processed_merged_at`: `2026-11-05T00:47:33Z`
- Outgoing `last_processed_merged_at`: `2026-11-05T00:47:33Z` (unchanged — nothing new)

## Coverage (merged apache/pinot PRs strictly after checkpoint)
Three agreeing inventory methods, all returning **0** PRs merged after `2026-11-05T00:47:33Z`:
1. search API (`is:pr is:merged merged:>2026-11-05T00:47:33Z`) — total_count = 0.
2. pulls API (`state=closed sort=updated desc per_page=50`, filtered merged_at > checkpoint) — 0 rows.
3. apache/pinot `upstream/master` commit log (committer date > checkpoint) — 0 commits. HEAD is `091eac79` (#20154 @ merged 00:47:33Z) = the checkpoint boundary PR, already processed (docs PR #1162).

## Decisions
None — no PRs to triage.

## Docs PRs created / merged
None.

## Validation
No docs changes made; no docs-repo validation required this run.

## Blockers
None. Durable state read and lease acquired/released cleanly via Contents API CAS (acquire SHA `3271d47a` → `bceedab7`; release conditioned on `bceedab7`). Access confirmed read-only: apache/pinot=WRITE, pinot-contrib/pinot-docs=ADMIN.

## Notifications
No Slack notification (no-op run; no new docs PR).

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


---

# Run run-20261105T030151Z-opus48-1207 — 2026-11-05T03:04:01Z

**Result: no-op (0 new PRs).** No apache/pinot PRs merged strictly after checkpoint `2026-11-05T00:47:33Z`. No docs work.

## Coverage
Incoming checkpoint `2026-11-05T00:47:33Z` (unchanged; = apache/pinot#20154 merged_at). Lease acquired via Contents API CAS (prior lease released by run-20261105T020144Z-opus48-1261); no overlap. Access confirmed read-only: apache/pinot=WRITE, pinot-contrib/pinot-docs=ADMIN.

Triple-verified **0** merged PRs strictly after checkpoint:
1. search/issues `repo:apache/pinot is:pr is:merged merged:>2026-11-05T00:47:33Z` — total_count=0.
2. apache/pinot master commit log since 2026-11-05T00:47:33Z — empty; HEAD `091eac79` == #20154 (checkpoint PR).
3. pulls API (`state=closed base=master sort=updated desc`) — 0 strictly after; most-recent merged are #20154/#20156/#20155/#20152, all already ledgered.

## Decisions
None (no new PRs to triage).

## Docs PRs created / merged
None.

## Validation
No docs changes; no docs-repo validation required.

## Blockers
None. Lease acquired and released cleanly via Contents API CAS. Checkpoint unchanged.

## Notifications
No Slack (no-op run; no new docs PR).
