# Pinot Docs Update — 2026-10-28 (UTC)

Automated maintenance of Apache Pinot documentation from newly merged `apache/pinot` PRs.

## Summary

1 docs-relevant PR processed today: apache/pinot#20063 → pinot-contrib/pinot-docs#1151 (merged).
Earlier runs today were no-ops. All merged upstream PRs through the durable checkpoint
(`last_processed_merged_at = 2026-10-28T01:05:37Z`) have been triaged.

## Runs

### 2026-10-28T00:03:19Z — `run-20261028T000121Z-12719` — no-op

- **Checkpoint:** `last_processed_merged_at = 2026-10-27T03:46:21Z` (unchanged).
- **Coverage:** 0 merged `apache/pinot` PRs strictly after the checkpoint. Confirmed by three
  authoritative sources:
  - search/issues `is:pr is:merged merged:>2026-10-27T03:46:21Z` → **0**.
  - apache/pinot commits-since(master) → only boundary commit `b58776bca` (#19990) at exactly
    the checkpoint, already processed → docs PR [#1150](https://github.com/pinot-contrib/pinot-docs/pull/1150).
  - pulls (state=closed, sort=updated desc) → most-recent merged = #19990 @ boundary; next
    #19991 / #20015 / #19862 all pre-boundary and already in the ledger.
  - master HEAD still `b58776bca`.
- **Decisions:** none (no new PRs to classify).
- **Created / merged docs PRs:** none.
- **Upstream comments:** none.
- **Validation:** not run (no docs changes produced).
- **Blockers:** none.
- **Slack:** not sent (no-op runs stay quiet; Slack fires only when new docs PRs are created).

### 2026-10-28T01:03Z — `run-20261028T010132Z-1262` — no-op

- **Checkpoint:** `last_processed_merged_at = 2026-10-27T03:46:21Z` (unchanged).
- **Coverage:** 0 merged `apache/pinot` PRs strictly after the checkpoint. Confirmed by three
  authoritative sources:
  - search/issues `is:pr is:merged merged:>2026-10-27T03:46:21Z` → **0**.
  - pulls (state=closed, sort=updated desc) → most-recent merged = #19990 @ exactly the boundary
    (`2026-10-27T03:46:21Z`), already processed → docs PR [#1150](https://github.com/pinot-contrib/pinot-docs/pull/1150);
    next #19991 / #20015 / #19862 / #19897 all pre-boundary and already in the ledger.
  - `git log b58776bca..upstream/master` → **0** new commits; master HEAD still `b58776bca` (#19990).
- **Decisions:** none (no new PRs to classify).
- **Created / merged docs PRs:** none.
- **Upstream comments:** none.
- **Validation:** not run (no docs changes produced).
- **Blockers:** none. Preflight: `gh` authenticated as `xiangfu0`; apache/pinot = push, pinot-contrib/pinot-docs = admin; durable state read/write via git-data API OK; lease acquired/released.
- **Slack:** not sent (no-op runs stay quiet; Slack fires only when new docs PRs are created).

### 2026-10-28T02:01Z — `run-20261028T020136Z-1151` — 1 docs PR created & merged

- **Checkpoint:** advanced `2026-10-27T03:46:21Z` → `2026-10-28T01:05:37Z`.
- **Coverage:** 1 merged `apache/pinot` PR strictly after the prior checkpoint. Confirmed by three
  authoritative sources:
  - search/issues `is:pr is:merged merged:>2026-10-27T03:46:21Z` → **1** = #20063.
  - pulls (state=closed, sort=updated desc) → most-recent merged = #20063 @ `2026-10-28T01:05:37Z`.
  - `git log b58776bca..upstream/master` → single commit `3381db7` (#20063), now master HEAD.
- **Decisions:**
  - **#20063** "Support is_leaf_return_final_result hint for aggregation without GROUP BY" →
    **docs-relevant**. Verified from merged code: `ServerPlanRequestVisitor.visitAggregate` maps
    the `is_leaf_return_final_result` aggOption to `serverReturnFinalResult` when there is no
    group-by key (and keeps `serverReturnFinalResultKeyUnpartitioned` for group-by). The hint
    previously took effect only for group-by queries; existing docs showed only a GROUP BY example.
- **Created / merged docs PRs:** [pinot-contrib/pinot-docs#1151](https://github.com/pinot-contrib/pinot-docs/pull/1151)
  — *docs: note is_leaf_return_final_result applies without GROUP BY* — merged (squash) 2026-10-28T02:03:45Z.
  Edited `build-with-pinot/querying-and-sql/multi-stage-query/operator-types/aggregate.md`.
- **Upstream comments:** [apache/pinot#20063#issuecomment-6458674517](https://github.com/apache/pinot/pull/20063#issuecomment-6458674517).
- **Validation:** `validate-docs.py --summary-only` → **PASS** (10 broken anchors are pre-existing,
  unchanged by this edit); `git diff --check` clean. CI checks "Validate changed docs" + "Full docs
  audit" both success.
- **Blockers:** none.
- **Slack:** sent (new docs PR created) — compact summary with upstream/docs links and merge status.

### 2026-10-28T03:03:19Z — `run-20261028T030210Z-1315` — no-op

- **Checkpoint:** `last_processed_merged_at = 2026-10-28T01:05:37Z` (unchanged).
- **Coverage:** 0 merged `apache/pinot` PRs strictly after the checkpoint. Confirmed by three
  authoritative sources:
  - search/issues `is:pr is:merged merged:>2026-10-28T01:05:37Z` → **0**.
  - pulls (state=closed, sort=updated desc) → most-recent merged = #20063 @ exactly the boundary
    (`2026-10-28T01:05:37Z`), already processed → docs PR [#1151](https://github.com/pinot-contrib/pinot-docs/pull/1151);
    next #19990 / #19991 / #20015 / #19862 / #19897 all pre-boundary and already in the ledger.
  - `git log 3381db7..upstream/master` → **0** new commits; master HEAD still `3381db7` (#20063).
- **Decisions:** none (no new PRs to classify).
- **Created / merged docs PRs:** none.
- **Upstream comments:** none.
- **Validation:** not run (no docs changes produced).
- **Blockers:** none. Preflight: `gh` authenticated as `xiangfu0` (GH_TOKEN); apache/pinot = push (WRITE), pinot-contrib/pinot-docs = admin (ADMIN); durable `automation-state` read/write via git-data/contents API OK; lease acquired (CAS create of `automation-lease.json`, no prior holder) and released at end.
- **Slack:** not sent (no-op runs stay quiet; Slack fires only when new docs PRs are created).
