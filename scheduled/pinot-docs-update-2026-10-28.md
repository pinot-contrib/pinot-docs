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

### 2026-10-28T04:01Z — `run-20261028T040116Z-976` — 1 docs PR created & merged

- **Checkpoint:** `last_processed_merged_at` advanced `2026-10-28T01:05:37Z` → **`2026-10-28T03:33:34Z`**.
- **Coverage:** 1 merged `apache/pinot` PR strictly after the prior checkpoint — **#20060** "Preserve wide
  Parquet INT96 timestamps" (merged `2026-10-28T03:33:34Z`). Confirmed by three authoritative sources:
  - search/issues `is:pr is:merged merged:>2026-10-28T01:05:37Z` → **1** (#20060).
  - pulls (state=closed) sorted by `merged_at` → next merged after #20063 is #20060; all below it already in ledger.
  - `git log 3381db7..upstream/master` → **1** commit `eeebb52` (#20060); upstream/master HEAD = `eeebb52`.
- **Decisions:**
  - **#20060 → docs-relevant (docs_created).** Verified from merged code, not PR prose:
    `ParquetUtils.convertInt96ToTimestamp` / `convertInt96ToEpochNanos` and the `ParquetNativeRecordExtractor`
    INT96 branch. In converted mode (default) INT96 now decodes to a Pinot `TIMESTAMP`, preserving instants
    outside the signed epoch-nanosecond range (~1677–2262) instead of silently wrapping (e.g. year 1600 → 2184).
    In raw mode (`extractRawTimeValues: true`) INT96 stays a `LONG` of epoch nanoseconds and out-of-range values
    are rejected. The existing Parquet type-conversion table row described the old lossy nanos→millis signed
    conversion and was corrected. No new user-facing config was introduced (the `ParquetRecordReaderConfig`
    `+1/-0` is a Javadoc line on the existing `extractRawTimeValues` option).
- **Created / merged docs PRs:** [pinot-contrib/pinot-docs#1152](https://github.com/pinot-contrib/pinot-docs/pull/1152)
  — one-line fix to the Parquet INT96 row in `build-with-pinot/ingestion/pinot-input-formats.md`. Squash-merged
  `2026-10-28T04:04:30Z` (commit `129e08b`).
- **Upstream comments:** [apache/pinot#20060#issuecomment-6460368002](https://github.com/apache/pinot/pull/20060#issuecomment-6460368002).
- **Validation:** `git diff --check` clean; `uv run --with pyyaml python scripts/validate-docs.py --summary-only` →
  **PASS** (637 files, 3553 links). The 10 broken anchors are **pre-existing** (confirmed by re-running against the
  stashed working tree) and unrelated to this one-line table edit. PR checks "Validate changed docs" + "Full docs
  audit (informational)" + GitBook all passed.
- **Blockers:** none. Preflight: `gh` authenticated as `xiangfu0` (GH_TOKEN); apache/pinot = push, pinot-contrib/pinot-docs
  = push; durable `automation-state` read/write via git-data/contents API OK; lease acquired (CAS create of
  `automation-lease.json`, no prior holder) and released at end.
- **Slack:** sent (new docs PR created) — compact summary with upstream/docs links and merge status.

---

## Run 2026-10-28T05:05:38Z (scheduled triage — no-op)

- **Run id:** `run-20261028T050152Z-1384`
- **Preflight:** `gh` authenticated as `xiangfu0`; apache/pinot = push+triage, pinot-contrib/pinot-docs = admin.
  Durable `automation-state` read (checkpoint `2026-10-28T03:33:34Z`); lease acquired (CAS create of
  `automation-lock.json`, no prior holder) and released at end.
- **Coverage:** merged apache/pinot PRs strictly after checkpoint `2026-10-28T03:33:34Z` → **0**. Three authoritative sources agree:
  - search/issues `is:pr is:merged merged:>2026-10-28T03:33:34Z` → **0**.
  - search/issues `merged:>=2026-10-28T03:33:34Z` → **1** (#20060, already in ledger — docs PR #1152 merged).
  - `git log` upstream/master first-parent → HEAD `eeebb52` = #20060 (merged exactly at the checkpoint boundary); nothing newer on master.
  - Cross-check `updated:>=2026-10-28` merged PRs → **0** with merged_at after checkpoint.
- **Decisions:** none (no new PRs to triage).
- **Created / merged docs PRs:** none.
- **Upstream comments:** none.
- **Validation:** n/a (no docs change this run).
- **Blockers:** none.
- **Slack:** not sent (no-op run — no new docs PRs).
- **Durable state:** checkpoint UNCHANGED (`2026-10-28T03:33:34Z`); `last_successful_run` → `2026-10-28T05:05:38Z`; `last_run_id` → `run-20261028T050152Z-1384`.

## Run 2026-10-28T06:01:04Z (scheduled triage — no-op)

- **Run id:** `run-20261028T060104Z-795`
- **Preflight:** `gh` authenticated as `xiangfu0` (GH_TOKEN); apache/pinot = pull+push+triage, pinot-contrib/pinot-docs = admin.
  Durable `automation-state` read (checkpoint `2026-10-28T03:33:34Z`); lease acquired (CAS create of
  `automation-lock.json`, no prior holder) and released at end.
- **Coverage:** merged apache/pinot PRs strictly after checkpoint `2026-10-28T03:33:34Z` → **0**. Three authoritative sources agree:
  - search/issues `is:pr is:merged merged:>2026-10-28T03:33:34Z` → **0**.
  - search/issues `is:pr is:merged merged:>=2026-10-28T03:33:34Z` → **1** (#20060, already in ledger — docs PR #1152 merged).
  - `git log` upstream/master first-parent → HEAD `eeebb52` = #20060 (committer date `2026-10-28T03:33:34Z`, exactly the checkpoint boundary); `--since` checkpoint shows only that boundary commit, nothing newer on master.
- **Decisions:** none (no new PRs to triage).
- **Created / merged docs PRs:** none.
- **Upstream comments:** none.
- **Validation:** n/a (no docs change this run).
- **Blockers:** none.
- **Slack:** not sent (no-op run — no new docs PRs).
- **Durable state:** checkpoint UNCHANGED (`2026-10-28T03:33:34Z`); `last_successful_run` → `2026-10-28T06:01:41Z`; `last_run_id` → `run-20261028T060104Z-795`.

## Run 2026-10-28T07:02:00Z — no-op

- **Run id:** `run-20261028T070109Z-842`
- **Preflight:** `gh` authenticated as `xiangfu0` (GH_TOKEN); apache/pinot = pull+push+triage, pinot-contrib/pinot-docs = admin.
  Durable `automation-state` read (checkpoint `2026-10-28T03:33:34Z`); lease acquired (CAS create of
  `automation-lock.json`, no prior holder) and released at end.
- **Coverage:** merged apache/pinot PRs strictly after checkpoint `2026-10-28T03:33:34Z` → **0**. Three authoritative sources agree:
  - search `--merged-at ">2026-10-28T03:33:34Z"` → **0**.
  - search `--merged-at ">=2026-10-28T03:33:34Z"` → **1** (#20060, already in ledger — docs PR #1152 merged).
  - `git log` upstream/master first-parent → HEAD `eeebb52` = #20060 (committer date `2026-10-28T03:33:34Z`, exactly the checkpoint boundary); `--since cp+1s` empty, nothing newer on master.
- **Decisions:** none (no new PRs to triage).
- **Created / merged docs PRs:** none.
- **Upstream comments:** none.
- **Validation:** n/a (no docs change this run).
- **Blockers:** none.
- **Slack:** not sent (no-op run — no new docs PRs).
- **Durable state:** checkpoint UNCHANGED (`2026-10-28T03:33:34Z`); `last_successful_run` → `2026-10-28T07:02:00Z`; `last_run_id` → `run-20261028T070109Z-842`.
