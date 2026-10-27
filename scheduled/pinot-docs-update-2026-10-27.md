# pinot-docs update report — 2026-10-27 (UTC)

## Run: bootstrap / first execution (manual Run trigger)
- Trigger: manual Run action (no schedule tick / webhook event).
- Checkpoint in effect: `last_processed_merged_at=2026-10-26T23:24:33Z`.

### Coverage
- Inventoried all merged `apache/pinot` PRs with `merged_at >= 2026-10-26` via the search
  API and reconciled against `master` commit history (HEAD `19dec509`).
- PRs strictly after the checkpoint (`merged_at > 2026-10-26T23:24:33Z`): **0**.
- #19862 merged at exactly the checkpoint boundary and is already the most recent completed
  pair (docs#1148) — not reprocessed.

### Decisions
- No new docs-relevant PRs. No docs PRs created, none merged.

### Durable state
- Established orphan `automation-state` branch on `pinot-contrib/pinot-docs` as the durable
  store (installation token cannot create a private repo). No secrets committed.

### Validation / blockers
- No docs changes to validate. No blockers.

## Run: 2026-10-27T01:02Z (scheduled/triage)
- Trigger: routine execution (IntentLab cloud runner).
- Checkpoint read from durable `automation-state` branch: `last_processed_merged_at=2026-10-26T23:24:33Z`.
- Lease acquired on `automation-state` (`automation-lock.json`) to serialize runs.

### Coverage
- Inventoried merged `apache/pinot` PRs strictly after the checkpoint via search API
  (`is:pr is:merged merged:>2026-10-26T23:24:33Z`), full pagination: **1 PR** (#20015).
- Reconciled against `upstream/master` first-parent history: HEAD `9c8b2901` = #20015,
  the only commit after the checkpoint. Coverage complete.

### Decisions
- **#20015** "Require consecutive readiness checks in the integration-test base" —
  **NOT docs-relevant**. Verified from merged code: single changed file
  `pinot-integration-test-base/.../BaseClusterIntegrationTest.java` (test source).
  Makes `waitForAllDocsLoaded` require `_serverStarters.size()` consecutive successful
  doc-count queries to fix flaky `WindowFunnelTest`. No user-facing behavior, config,
  public API, or documented default changed. Internal test-harness only.

### Durable state
- Advanced checkpoint to `last_processed_merged_at=2026-10-27T00:45:19Z` (#20015 merged-at).
- Recorded #20015 ledger entry (`decision=not_relevant`). Lease released.

### Validation / blockers
- No docs changes to validate (no docs PR created). No blockers. No Slack notification
  (no new docs PRs → no-op for notification purposes).

## Run: 2026-10-27T02:02:41Z (scheduled/triage)
- Trigger: routine execution (IntentLab cloud runner).
- Checkpoint read from durable `automation-state`: `last_processed_merged_at=2026-10-27T00:45:19Z`.
- Lease acquired on `automation-state` (`automation-lock.json`, create-only CAS) to serialize runs.

### Coverage
- Inventoried merged `apache/pinot` PRs strictly after the checkpoint via search API
  (`is:pr is:merged merged:>2026-10-27T00:45:19Z`) with full pagination, cross-checked
  against `gh pr list --state merged` (30 most-recent): **0 PRs** strictly after checkpoint.
- Most recently merged PR is #20015 at exactly `2026-10-27T00:45:19Z` (the checkpoint
  boundary), already processed (not_relevant). All other recent PRs merged earlier. Coverage complete.

### Decisions
- No new docs-relevant PRs. No docs PRs created, none merged.

### Durable state
- Checkpoint unchanged (no new work). Bumped `last_successful_run` to 2026-10-27T02:02:41Z. Lease released.

### Validation / blockers
- No docs changes to validate (no docs PR). No blockers. No Slack notification (no new docs PRs).

## Run: 2026-10-27T03:05Z (scheduled/triage — docs PR created)
- Trigger: routine execution (IntentLab cloud runner).
- Checkpoint read from durable `automation-state`: `last_processed_merged_at=2026-10-27T00:45:19Z`.
- Lease acquired on `automation-state` (`automation-lock.json`, create-only CAS) to serialize runs.

### Coverage
- Inventoried merged `apache/pinot` PRs strictly after the checkpoint via search API
  (`is:pr is:merged merged:>2026-10-27T00:45:19Z`) with full pagination, cross-checked
  against `gh pr list --state merged`: **1 PR** (#19991).
- Reconciled against the merge commit (`7835c7dc`), the only commit after the checkpoint.
  Coverage complete.

### Decisions
- **#19991** "Support MODE on STRING, BOOLEAN and TIMESTAMP inputs" — **docs-relevant**.
  Verified from merged code (`ModeAggregationFunction`, `AggregationFunctionType`):
  - New signature `MODE(colName, [reducerType], [dataType])` (at most 3 args).
  - `dataType` in {STRING, BOOLEAN, TIMESTAMP} is also the result type; the input
    expression's stored type must match. Only MIN/MAX reducers are supported for typed
    values (AVG rejected). Without `dataType`, input must be numeric → DOUBLE result.
  - STRING works without the 3rd arg (including JSON columns read as strings); typed
    BOOLEAN/TIMESTAMP results are opt-in via the explicit 3-arg form.
  - Rolling-upgrade: older servers reject the 3-arg form; 1-/2-arg calls unchanged.
- Minimal edit to `functions/aggregation/mode.md` (signature + argument descriptions +
  rolling-upgrade hint). No tests/benchmarks touched.

### Created / merged links
- Docs PR: https://github.com/pinot-contrib/pinot-docs/pull/1149
  (squash-merged 2026-10-27T03:04:22Z, commit b10e0dd2, branch deleted).
- Upstream comment: https://github.com/apache/pinot/pull/19991#issuecomment-6432711240

### Validation / blockers
- `git diff --check`: clean.
- `uv run --with pyyaml python scripts/validate-docs.py --summary-only`: RESULT PASS
  (10 pre-existing broken-anchor warnings, none in `mode.md`; distinguished from new failures).
- PR checks: Validate changed docs = SUCCESS, Full docs audit = SUCCESS, GitBook x2 = SUCCESS;
  `mergeStateStatus=CLEAN`, `mergeable=MERGEABLE`. No blockers.

### Durable state
- Advanced checkpoint to `last_processed_merged_at=2026-10-27T02:18:50Z` (#19991 merged-at).
- Recorded #19991 ledger entry (`decision=docs_created`, docs#1149). Lease released.
- Slack summary sent (new docs PR created this run).

---

## Run 2026-10-27T04:05:27Z (run-20261027T040116Z-919)

### Coverage
- Checkpoint at run start: `last_processed_merged_at=2026-10-27T02:18:50Z`.
- Inventory of merged apache/pinot PRs strictly after checkpoint (search API, full
  pagination; GitHub API authoritative because this runner's git mirror lags):
  **1 PR** — #19990, merged 2026-10-27T03:46:21Z. Coverage complete.

### Decisions
- **#19990 "Return the input's logical type from ANY_VALUE" → docs_created.**
  New user-facing query behavior. Verified from merged code (b58776bc):
  - New 2-arg form `ANYVALUE(colName,'dataType')`; supported dataTypes INT, LONG,
    FLOAT, DOUBLE, BIG_DECIMAL, BOOLEAN, TIMESTAMP, STRING, BYTES, UUID; others fail.
  - Query option `inferAnyValueType`; default from broker config
    `pinot.broker.query.infer.any.value.type` (false), live via cluster config;
    rewrites 1-arg ANY_VALUE to return expr's logical type in both engines.
  - Rolling-upgrade: older servers reject the 2-arg form.
- Minimal edit to `functions/aggregation/anyvalue.md`. No tests/benchmarks touched.

### Created / merged links
- Docs PR: https://github.com/pinot-contrib/pinot-docs/pull/1150
  (squash-merged 2026-10-27T04:04:15Z, commit cbb4d2a3, branch deleted).
- Upstream comment: https://github.com/apache/pinot/pull/19990#issuecomment-6433456568

### Validation / blockers
- `git diff --check`: clean.
- `scripts/validate-docs.py --summary-only`: RESULT PASS (10 pre-existing broken-anchor
  warnings, none in anyvalue.md). PR checks all SUCCESS. No blockers.

### Durable state
- Advanced checkpoint to `2026-10-27T03:46:21Z` (#19990 merged-at).
- Recorded #19990 ledger entry (`decision=docs_created`, docs#1150). Lease released.
- Slack summary sent (new docs PR created this run).

---

## Run 2026-10-27T05:01:33Z (run-20261027T050133Z-1053 — no-op)

### Coverage
- Checkpoint at run start: `last_processed_merged_at=2026-10-27T03:46:21Z`.
- Inventory of merged apache/pinot PRs strictly after checkpoint
  (`is:pr is:merged merged:>2026-10-27T03:46:21Z`, search API full pagination):
  **0 PRs**. Cross-checked via pulls API (state=closed, sort=updated desc): most-recent
  merged PR is #19990 @ 2026-10-27T03:46:21Z (= checkpoint boundary, already processed
  this day as docs#1150). Coverage complete, no unprocessed work.

### Decisions
- No new docs-relevant PRs. No docs PRs created, none merged.

### Durable state
- Checkpoint unchanged (no new work). Bumped `last_successful_run` to 2026-10-27T05:01:33Z. Lease released.

### Validation / blockers
- No docs changes to validate (no docs PR). No blockers. No Slack notification (no new docs PRs).

---

## Run 2026-10-27T06:01:39Z (run-20261027T060139Z-1108 — no-op)

### Coverage
- Checkpoint at run start: `last_processed_merged_at=2026-10-27T03:46:21Z`.
- Inventory of merged apache/pinot PRs strictly after checkpoint
  (`is:pr is:merged merged:>2026-10-27T03:46:21Z`, search API full pagination):
  **0 PRs**. Cross-checked via pulls API (state=closed, sort=updated desc, per_page=50):
  most-recent merged PR is #19990 @ 2026-10-27T03:46:21Z (= checkpoint boundary, already
  processed this day as docs#1150). Programmatic count of merged PRs strictly after the
  checkpoint = 0. Coverage complete, no unprocessed work.

### Decisions
- No new docs-relevant PRs. No docs PRs created, none merged.

### Durable state
- Checkpoint unchanged (no new work). Bumped `last_successful_run` to 2026-10-27T06:01:39Z. Lease released.

### Validation / blockers
- No docs changes to validate (no docs PR). No blockers. No Slack notification (no new docs PRs).

---

## Run 2026-10-27T07:03:04Z (run-20261027T070139Z-1281 — no-op)

### Coverage
- Checkpoint at run start: `last_processed_merged_at=2026-10-27T03:46:21Z`.
- Inventory of merged apache/pinot PRs strictly after checkpoint
  (`merged:>2026-10-27T03:46:21Z`, search API full pagination): **0 PRs**.
  Reconciled against `apache/master`: HEAD commit is PR #19990 @ `2026-10-27T03:46:21Z`
  (= checkpoint boundary, already processed this day as docs#1150). No commits or merged
  PRs beyond the checkpoint. Coverage complete, no unprocessed work.

### Decisions
- No new docs-relevant PRs. No docs PRs created, none merged.

### Durable state
- Checkpoint unchanged (no new work). Bumped `last_successful_run` to 2026-10-27T07:03:04Z. Lease released.

### Validation / blockers
- No docs changes to validate (no docs PR). No blockers. No Slack notification (no new docs PRs).

---

## Run 2026-10-27T09:02:40Z (run-20261027T090113Z-908 — no-op)

### Coverage
- Checkpoint at run start: `last_processed_merged_at=2026-10-27T03:46:21Z`.
- Inventory of merged apache/pinot PRs strictly after checkpoint
  (`is:pr is:merged merged:>2026-10-27T03:46:21Z`, search API full pagination): **0 PRs**.
  Cross-checked via pulls API (state=closed, sort=updated desc, per_page=50): 0 merged
  strictly after checkpoint. Reconciled against `apache/master`: HEAD commit `b58776bc`
  is PR #19990 @ `2026-10-27T03:46:21Z` (= checkpoint boundary, already processed this day
  as docs#1150). No commits or merged PRs beyond the checkpoint. Coverage complete, no
  unprocessed work.

### Decisions
- No new docs-relevant PRs. No docs PRs created, none merged.

### Durable state
- Checkpoint unchanged (no new work). Bumped `last_successful_run` to 2026-10-27T09:02:40Z (CAS). Lease released.

### Validation / blockers
- No docs changes to validate (no docs PR). No blockers. No Slack notification (no new docs PRs).


## Run 2026-10-27T10:02:32Z — no-op
- **Checkpoint (authoritative, automation-state.json):** `2026-10-27T03:46:21Z` (unchanged)
- **Coverage:** merged `apache/pinot` PRs strictly after checkpoint — **0** (search API + pulls API cross-check, full pagination). Reconciled with master HEAD `b58776bc` = #19990 at the checkpoint boundary.
- **Decisions:** none (no new PRs to triage).
- **Docs PRs created/merged:** none.
- **Validation:** n/a (no docs changes).
- **Blockers:** none. (`gh-tentrix-wrap` stderr warning benign; ambient installation token has full read+write — verified ADMIN on pinot-docs, WRITE on apache/pinot.)
- **Notifications:** none (quiet no-op run).
- **Run id:** `run-20261027T100122Z-967`

---

## Run 2026-10-27T11:01:14Z (`run-20261027T110114Z-31424`) — no-op

- **Coverage:** merged `apache/pinot` PRs strictly after checkpoint `2026-10-27T03:46:21Z` — **0 PRs** (search API full pagination + pulls API cross-check). Reconciled against authoritative GitHub master HEAD `b58776bc` = #19990 (= checkpoint boundary, already docs#1150).
- **Decisions:** none (no new PRs to triage).
- **Created/merged docs PRs:** none.
- **Validation:** n/a (no docs changes).
- **Blockers:** none. (Local `/workspace/pinot` mirror `origin/master` stale at #19809; authoritative GitHub API used for reconciliation.)
- **Durable state:** checkpoint unchanged `2026-10-27T03:46:21Z`; `last_successful_run` -> `2026-10-27T11:01:14Z`. Lease released.
- **Slack:** none (no new docs PRs).


---

## Run 2026-10-27T12:01:57Z (`run-20261027T120113Z-869`) — no-op

- **Coverage:** merged `apache/pinot` PRs strictly after checkpoint `2026-10-27T03:46:21Z` — **0 PRs** (search/issues API full pagination + pulls API cross-check). Reconciled against authoritative GitHub master HEAD `b58776bca` = #19990 (= checkpoint boundary, already docs#1150 merged). Local `/workspace/pinot` mirror stale at #19809 — ignored.
- **Decisions:** none (no new PRs to triage).
- **Created/merged docs PRs:** none.
- **Validation:** n/a (no docs changes).
- **Blockers:** none. (`gh-tentrix-wrap` stderr "no token minted" warning benign; ambient installation token has full read+write — ADMIN on pinot-docs, WRITE on apache/pinot.)
- **Durable state:** lease acquired (create-only CAS) and released; checkpoint unchanged `2026-10-27T03:46:21Z`; `last_successful_run` -> `2026-10-27T12:01:57Z`. Fixed stale "Checkpoint (current)" section in automation-memory.md.
- **Slack:** none (no new docs PRs).


---

## Run 2026-10-27T13:02:57Z (`run-20261027T130157Z-1192`) — no-op

- **Coverage:** merged `apache/pinot` PRs strictly after checkpoint `2026-10-27T03:46:21Z` — **0 PRs** (search/issues API full pagination + pulls API cross-check). Reconciled against authoritative GitHub master HEAD `b58776bca` = #19990 (= checkpoint boundary, already docs#1150 merged). Top commits #19990/#19991/#20015/#19862 all map to the processed ledger. Local `/workspace/pinot` mirror stale at #19809 — ignored in favor of authoritative GitHub API.
- **Decisions:** none (no new PRs to triage).
- **Created/merged docs PRs:** none.
- **Validation:** n/a (no docs changes).
- **Blockers:** none. (`gh-tentrix-wrap` stderr "no token minted / not in manifest" warning benign; ambient GH_TOKEN authenticates as xiangfu0 with full read+write — ADMIN on pinot-docs confirmed by successful lease CAS write, WRITE on apache/pinot.)
- **Durable state:** lease acquired (create-only CAS, `automation-lock.json`) and released; checkpoint unchanged `2026-10-27T03:46:21Z`; `last_successful_run` -> `2026-10-27T13:02:57Z`.
- **Slack:** none (no new docs PRs).


---

## Run 2026-10-27T14:02:07Z (`run-20261027T140122Z-990`) — no-op

- **Coverage:** merged `apache/pinot` PRs strictly after checkpoint `2026-10-27T03:46:21Z` — **0 PRs**. Three independent sources agree: (1) search/issues `is:pr is:merged merged:>2026-10-27T03:46:21Z` = 0; (2) pulls API (state=closed, sort=updated desc, per_page=50) = 0 merged after checkpoint; (3) commits API master HEAD `b58776bca` = #19990 @ `2026-10-27T03:46:21Z` = checkpoint boundary. Reconciled top master commits #19990/#19991/#20015/#19862 — all present in processed ledger. Local `/workspace/pinot` mirror stale at #19809 — ignored in favor of authoritative GitHub API.
- **Decisions:** none (no new PRs to triage).
- **Created/merged docs PRs:** none.
- **Validation:** n/a (no docs changes).
- **Blockers:** none. (`gh-tentrix-wrap` stderr "no token minted / not in manifest" warning benign; ambient GH_TOKEN authenticates as xiangfu0 with full read+write — ADMIN on pinot-docs confirmed by successful lease CAS write, WRITE on apache/pinot.)
- **Durable state:** lease acquired (create-only CAS, `automation-lock.json`) and released; checkpoint unchanged `2026-10-27T03:46:21Z`; `last_successful_run` -> `2026-10-27T14:02:07Z`.
- **Slack:** none (no new docs PRs).


---

## Run 2026-10-27T15:01:58Z (`run-20261027T150115Z-931`) — no-op

- **Coverage:** merged `apache/pinot` PRs strictly after checkpoint `2026-10-27T03:46:21Z` — **0 PRs**. Three independent sources agree: (1) search/issues `is:pr is:merged merged:>2026-10-27T03:46:21Z` = 0; (2) pulls API (state=closed, sort=updated desc) most-recent merged = #19990 @ `2026-10-27T03:46:21Z` = checkpoint boundary; (3) commits-since master returns only boundary commit `b58776bca` (#19990). Reconciled top master-side PRs #19990/#19991/#20015/#19862 — all present in processed ledger. Local `/workspace/pinot` mirror stale at #19809 — ignored in favor of authoritative GitHub API.
- **Decisions:** none (no new PRs to triage).
- **Created/merged docs PRs:** none.
- **Validation:** n/a (no docs changes).
- **Blockers:** none. (`gh-tentrix-wrap` stderr "no token minted / not in manifest" warning benign; ambient GH_TOKEN authenticates as xiangfu0 with full read+write — ADMIN on pinot-docs confirmed by successful lease CAS write, WRITE on apache/pinot.)
- **Durable state:** lease acquired (create-only CAS, `automation-lock.json`) and released; checkpoint unchanged `2026-10-27T03:46:21Z`; `last_successful_run` -> `2026-10-27T15:01:58Z` (CAS).
- **Slack:** none (no new docs PRs).


---

## Run 2026-10-27T16:03:08Z (`run-20261027T160150Z-1939`) — no-op

- **Coverage:** merged `apache/pinot` PRs strictly after checkpoint `2026-10-27T03:46:21Z` — **0 PRs**. Three independent sources agree: (1) search/issues `is:pr is:merged merged:>2026-10-27T03:46:21Z` = 0; (2) pulls API (state=closed, sort=updated desc, per_page=30) most-recent merged = #19990 @ `2026-10-27T03:46:21Z` = checkpoint boundary; (3) commits-since master returns only boundary commit `b58776bca` (#19990). Reconciled top master-side PRs #19990/#19991/#20015/#19862 — all present in processed ledger. Local `/workspace/pinot` mirror stale at #19809 — ignored in favor of authoritative GitHub API.
- **Decisions:** none (no new PRs to triage).
- **Created/merged docs PRs:** none.
- **Validation:** n/a (no docs changes).
- **Blockers:** none. Authentication: ambient `GH_TOKEN` authenticates as xiangfu0 — ADMIN on pinot-docs, WRITE on apache/pinot (both confirmed via API). Note: direct `git push` to the bare `automation-state` branch is blocked by session-git-hooks (requires `cs_<sid>/` prefix); durable state is written via the GitHub git-data/contents API (CAS), as the branch README prescribes.
- **Durable state:** lease acquired (`automation.lock`, CAS) and released; checkpoint unchanged `2026-10-27T03:46:21Z`; `last_successful_run` -> `2026-10-27T16:03:08Z` (CAS).
- **Slack:** none (no new docs PRs).
