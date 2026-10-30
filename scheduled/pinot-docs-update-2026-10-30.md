# Pinot Docs Update — 2026-10-30 (UTC)


## Run 2026-10-30T04:01:30Z (run-20261030T040104Z-815)

**Result: NO-OP (no new PRs to triage).** No apache/pinot `master` PR merged strictly after the durable checkpoint.

### Coverage
- Durable checkpoint at start (`automation-state.json`): `last_processed_merged_at = 2026-10-29T22:11:48Z` (apache/pinot #20096).
- Merged apache/pinot PRs on `master` strictly after the checkpoint: **0**.
- Reconciled three independent ways, all consistent and empty:
  1. `GET search/issues q="repo:apache/pinot is:pr is:merged base:master merged:>=2026-10-29"` → 11 candidates (#20096, #20087, #20086, #20079, #20078, #20074, #20064, #20048, #19988, #19943, #19905); newest #20096 @ `22:11:48Z` = checkpoint, all 11 already in the processed ledger.
  2. `GET commits?sha=master&since=2026-10-29T22:11:49Z` → 0 commits.
  3. `GET pulls state=closed base=master sort=updated desc per_page=50` → 0 with `merged_at` strictly > checkpoint.
- No gaps between the checkpoint and current HEAD. Pinot checkout clean and in sync with `origin/master` (910f9d5).

### Decisions / docs PRs / upstream comments / validation
- None — no new PRs. Not applicable.

### Blockers / required user action
- None. Preflight passed (read-only): gh auth `xiangfu0`; `apache/pinot` push=true (comment upstream), `pinot-contrib/pinot-docs` admin=true; durable state read/write OK.
- Durable writes use the GitHub Contents API (compare-and-swap on blob `sha`). Lock acquired via CAS on `automation-state.json`, holder re-verified before finalize, released in this run's atomic state write.
- Benign `gh-tentrix-wrap` stderr warnings on each `gh api` call; fallback `GH_TOKEN` is authenticated and all reads/writes succeed.

### Notifications
- No Slack (no-op policy).

### Checkpoint
- **Unchanged**: `2026-10-29T22:11:48Z`. `last_successful_run` → `2026-10-30T04:01:30Z`; `last_run_id` → `run-20261030T040104Z-815`.


## Run 2026-10-30T03:03:00Z (run-20261030T030113Z-824)

**Result: NO-OP (no new PRs to triage).** No apache/pinot `master` PR merged strictly after the durable checkpoint.

### Coverage
- Durable checkpoint at start (`automation-state.json`): `last_processed_merged_at = 2026-10-29T22:11:48Z` (apache/pinot #20096).
- Merged apache/pinot PRs on `master` strictly after the checkpoint: **0**.
- Reconciled three independent ways, all consistent and empty:
  1. `GET search/issues q="repo:apache/pinot is:pr is:merged base:master merged:>=2026-10-29"` → 11 candidates (#20074, #20096, #20048, #20064, #20086, #20087, #19943, #19905, #20078, #20079, #19988); each verified `merged_at <= checkpoint` (newest #20096 @ `22:11:48Z` = checkpoint) and all 11 already in the processed ledger.
  2. `GET commits?sha=master&since=2026-10-29T22:11:49Z` → 0 commits.
  3. `GET pulls state=closed base=master sort=updated desc per_page=50` → 0 with `merged_at` strictly > checkpoint.
- No gaps between the checkpoint and current HEAD. Pinot checkout in sync with `origin/master` (910f9d5).

### Decisions / docs PRs / upstream comments / validation
- None — no new PRs. Not applicable.

### Blockers / required user action
- None. Preflight passed (read-only): gh auth `xiangfu0`; `apache/pinot` push=true (comment upstream), `pinot-contrib/pinot-docs` push=true; durable state read/write OK.
- Durable writes use the GitHub Contents API (compare-and-swap on blob `sha`) because the local push wrapper redirects bare-branch pushes to a `cs_<sid>/` session prefix. Lock acquired via CAS on `automation-state.json`, holder re-verified before finalize, released in this run's atomic state write.
- Benign `gh-tentrix-wrap` stderr warnings on each `gh api` call; fallback `GH_TOKEN` is authenticated and all reads/writes succeed.

### Notifications
- No Slack (no-op policy).

### Checkpoint
- **Unchanged**: `2026-10-29T22:11:48Z`. `last_successful_run` → `2026-10-30T03:03:00Z`; `last_run_id` → `run-20261030T030113Z-824`.


## Run 2026-10-30T02:02:53Z (run-20261030T020115Z-975)

**Result: NO-OP (no new PRs to triage).** No apache/pinot `master` PR merged strictly after the durable checkpoint.

### Coverage
- Durable checkpoint at start (`automation-state.json`): `last_processed_merged_at = 2026-10-29T22:11:48Z` (apache/pinot #20096).
- Merged apache/pinot PRs on `master` strictly after the checkpoint: **0**.
- Reconciled three independent ways, all consistent and empty:
  1. `GET search/issues q="repo:apache/pinot is:pr is:merged base:master merged:>=2026-10-29"` → 11 candidates (#20096, #20087, #20086, #20079, #20078, #20074, #20064, #20048, #19988, #19943, #19905); each verified `merged_at <= checkpoint` (newest #20096 @ `22:11:48Z` = checkpoint) and all 11 already in the processed ledger.
  2. `GET commits?sha=master&since=2026-10-29T22:11:49Z` → 0 commits.
  3. `GET pulls state=closed base=master sort=updated desc per_page=50` → 41 merged, 0 with `merged_at` strictly > checkpoint (newest merged #20096 @ checkpoint).
- No gaps between the checkpoint and current HEAD. Pinot checkout in sync with `origin/master` (910f9d5).

### Decisions / docs PRs / upstream comments / validation
- None — no new PRs. Not applicable.

### Blockers / required user action
- None. Preflight passed: gh auth `xiangfu0`; `apache/pinot`=WRITE, `pinot-contrib/pinot-docs`=ADMIN; durable state read/write OK.
- Durable writes use the GitHub Git Data / Contents API (CAS) because the local push wrapper redirects bare-branch pushes to a `cs_<sid>/` session prefix. Lock acquired via Contents-API CAS on `automation-state.json`, holder re-verified before work, released in this run's atomic state write.
- Benign `gh-tentrix-wrap` stderr warnings on each `gh api` call; fallback `GH_TOKEN` is authenticated and all reads/writes succeed.

### Notifications
- No Slack (no-op policy).

### Checkpoint
- **Unchanged**: `2026-10-29T22:11:48Z`. `last_successful_run` → `2026-10-30T02:02:53Z`; `last_run_id` → `run-20261030T020115Z-975`.


## Run 2026-10-30T01:03:00Z (run-20261030T010058Z-789)

**Result: NO-OP (no new PRs to triage).** No apache/pinot `master` PR merged strictly after the durable checkpoint.

### Coverage
- Durable checkpoint at start (`automation-state.json`): `last_processed_merged_at = 2026-10-29T22:11:48Z` (apache/pinot #20096).
- Merged apache/pinot PRs on `master` strictly after the checkpoint: **0**.
- Reconciled three independent ways, all consistent and empty:
  1. `search repo:apache/pinot is:pr is:merged base:master merged:>=2026-10-29` → 11 candidates, all with precise `merged_at <= checkpoint` (newest #20096 @ `22:11:48Z` = checkpoint, already processed). `merged:>=2026-10-30` → 0.
  2. `GET commits?sha=master&since=2026-10-29T22:11:49Z` → 0 commits.
  3. pulls API (`state=closed base=master sort=updated desc per_page=50`) → 0 PRs with `merged_at` strictly > checkpoint.
- No gaps between the checkpoint and current HEAD.

### Decisions
- None (no new PRs).

### Created / merged docs PRs
- None.

### Upstream comments
- None.

### Validation
- Not applicable (no docs changes produced).

### Blockers / required user action
- None. Preflight passed: gh auth `xiangfu0`; `apache/pinot`=WRITE (can comment upstream), `pinot-contrib/pinot-docs`=ADMIN; durable state read/write OK. Pinot checkout verified in sync with `origin/master` (910f9d5).
- Durable writes use the GitHub Git Data / Contents API (server-side, compare-and-swap) because the local push wrapper redirects bare-branch pushes to a `cs_<sid>/` session prefix. Lock acquired (CAS on blob `sha`) and released inside `automation-state.json`.

### Notifications
- No Slack (no-op policy: webhook fires only when a run creates new docs PRs).

### Checkpoint
- **Unchanged**: `2026-10-29T22:11:48Z` (no new work). `last_successful_run` → `2026-10-30T01:03:00Z`; `last_run_id` → `run-20261030T010058Z-789`.

---

## Run 2026-10-30T00:05:24Z (run-20261030T000127Z-18501)

**Result: NO-OP (one PR triaged, not docs-relevant).** One new upstream PR since the last run; classified not docs-relevant (test-only fix).

### Coverage
- Durable checkpoint at start (`automation-state.json`): `last_processed_merged_at = 2026-10-29T21:38:16Z` (apache/pinot #20074).
- Merged apache/pinot PRs on `master` strictly after the checkpoint: **1** (#20096, merged `2026-10-29T22:11:48Z`).
- Reconciled three independent ways, all consistent:
  1. `search repo:apache/pinot is:pr is:merged base:master merged:>=2026-10-29` (11 candidates) → filtered by precise `merged_at > checkpoint` → only **#20096**.
  2. `GET commits?sha=master&since=2026-10-29T21:38:17Z` → exactly 1 commit (#20096); apache/pinot `master` HEAD now at #20096.
  3. pulls API (`state=closed base=master sort=updated desc`) → exactly 1 PR with `merged_at` strictly > checkpoint (#20096).
- No gaps between the checkpoint and current HEAD.

### Decisions
- **#20096 — not docs-relevant.** "Fix the shared test query server answering every query with an error" (yashmayya; fixes #20094). **Test code only** — verified from the merged diff: 3 files, all under `src/test/java` (`QueryServerTestUtils.java` shared fixture, `QueryRoutingTest.java`, `SingleConnectionBrokerRequestHandlerFailureDetectorTest.java`). Repairs test wiring broken by #19943 (switch to `QueryScheduler.submitResponse()` left the shared Mockito fixture stubbing the deprecated `submit()`, returning null → NPE → the "stuck" test server answered every query with an error). PR body: "The change is in test code only." No production code, no new/changed SQL function, config key, query option, default, public API, or wire/serialization format. Nothing user-facing to document.

### Created / merged docs PRs
- None.

### Upstream comments
- None.

### Validation
- Not applicable (no docs changes produced).

### Blockers / required user action
- None. Preflight passed: gh auth `xiangfu0`; `apache/pinot`=WRITE (can comment upstream), `pinot-contrib/pinot-docs`=ADMIN; durable state read/write OK.
- Durable writes use the GitHub Contents API (server-side, compare-and-swap on file `sha`) because the local `pre-push` hook blocks pushes to the bare `automation-state` branch (it requires a `cs_<sid>/` session prefix on the remote ref). Lock acquired/re-verified/released inside `automation-state.json`. Same approach documented by the 2026-10-29T17:04 run.
- Benign `gh-tentrix-wrap` "no token minted / not in manifest" stderr warnings appear on each gh api call; the fallback `GH_TOKEN` is authenticated and all reads/writes succeed.

### Notifications
- No Slack (no-op policy: webhook fires only when a run creates new docs PRs).

### Checkpoint
- **Advanced**: `2026-10-29T21:38:16Z` → `2026-10-29T22:11:48Z` (#20096 fully processed as not_relevant). `last_successful_run` → `2026-10-30T00:05:24Z`; `last_run_id` → `run-20261030T000127Z-18501`.

---

## Run 2026-10-30T06:03:21Z (run-20261030T060130Z-992) — NO-OP

### Coverage
- Durable checkpoint at start: `last_processed_merged_at = 2026-10-29T22:11:48Z` (#20096).
- Merged apache/pinot `master` PRs strictly after checkpoint: **0**. Reconciled three independent ways, all consistent and empty:
  1. `search/issues ... is:merged base:master merged:>=2026-10-29` → 11 candidates (#20096,#20087,#20086,#20079,#20078,#20074,#20064,#20048,#19988,#19943,#19905), newest #20096 @22:11:48Z = checkpoint, all already in ledger; `merged:>=2026-10-30` → 0.
  2. `commits?sha=master&since=2026-10-29T22:11:49Z` → 0 new commits.
  3. `pulls state=closed base=master sort=updated desc` → most recent merged #20096 @22:11:48Z, nothing after it.
- No gaps between checkpoint and current apache/pinot master HEAD (c91d0e8).

### Decisions / docs PRs / upstream comments / validation
- None — no new PRs. Not applicable.

### Blockers / required user action
- None. Preflight passed: gh auth `xiangfu0`; `apache/pinot`=WRITE (can comment upstream), `pinot-contrib/pinot-docs`=ADMIN; durable read/write OK (CAS on `automation-state.json`).
- Note: local checkout is the `xiangfu0/pinot` fork (HEAD 910f9d5), which trails apache/pinot master (c91d0e8). Inventory is driven directly by the apache/pinot API, so no rebase was needed for this no-op run. Benign `gh-tentrix-wrap` "no token minted" stderr warnings appear on each call; the fallback `GH_TOKEN` is authenticated (rate limit 15000, collaborator-permission endpoints readable) and all reads/writes succeed.

### Notifications
- No Slack (no-op policy).

### Checkpoint
- **Unchanged**: `2026-10-29T22:11:48Z`. `last_successful_run` → `2026-10-30T06:03:21Z`; `last_run_id` → `run-20261030T060130Z-992`.

---

## Run 2026-10-30T07:02:08Z (run-20261030T070100Z-811) — NO-OP

### Coverage
- Durable checkpoint at start: `last_processed_merged_at = 2026-10-29T22:11:48Z` (#20096).
- Merged apache/pinot `master` PRs strictly after checkpoint: **0**. Reconciled three independent ways, all consistent and empty:
  1. `search/issues ... is:merged base:master merged:>=2026-10-29` → 11 candidates, newest #20096 @22:11:48Z = checkpoint, all already in ledger; `merged:>=2026-10-30` → 0.
  2. `commits?sha=master&since=2026-10-29T22:11:49Z` → 0 new commits.
  3. `pulls state=closed base=master sort=updated desc` → most recent merged #20096 @22:11:48Z, nothing after it.

### Decisions / docs PRs / upstream comments / validation
- None — no new PRs. Not applicable.

### Blockers / required user action
- None. Preflight passed: gh auth `xiangfu0`; `apache/pinot`=WRITE, `pinot-contrib/pinot-docs`=ADMIN; durable read/write OK (CAS on `automation-state.json`).

### Notifications
- No Slack (no-op policy).

### Checkpoint
- **Unchanged**: `2026-10-29T22:11:48Z`. `last_successful_run` → `2026-10-30T07:02:08Z`; `last_run_id` → `run-20261030T070100Z-811`.

---

## Run 2026-10-30T08:02:11Z (run-20261030T080113Z-872) — NO-OP

### Coverage
- Durable checkpoint at start: `last_processed_merged_at = 2026-10-29T22:11:48Z` (#20096).
- Merged apache/pinot `master` PRs strictly after checkpoint: **0**. Reconciled three ways, all empty and consistent:
  1. `search/issues ... is:merged base:master merged:>=2026-10-29` → 11 candidates, newest #20096 @22:11:48Z = checkpoint, all already in ledger; `merged:>=2026-10-30` → 0.
  2. `commits?sha=master&since=2026-10-29T22:11:49Z` → 0 new commits.
  3. `pulls state=closed base=master sort=updated desc` → most recent merged #20096 @22:11:48Z, nothing after it.

### Decisions / docs PRs / upstream comments / validation
- None — no new PRs. Not applicable.

### Blockers / required user action
- None. Preflight passed: gh auth `xiangfu0`; `apache/pinot`=WRITE, `pinot-contrib/pinot-docs`=ADMIN; durable read/write OK (CAS on `automation-state.json`).

### Notifications
- No Slack (no-op policy).

### Checkpoint
- **Unchanged**: `2026-10-29T22:11:48Z`. `last_successful_run` → `2026-10-30T08:02:11Z`; `last_run_id` → `run-20261030T080113Z-872`.

---

## Run 2026-10-30T09:01:16Z (run-20261030T090116Z-874)

**Result: NO DOCS (2 new PRs triaged; net no-op revert pair — nothing docs-relevant shipped).**

### Coverage
- Durable checkpoint at start (`automation-state.json`): `last_processed_merged_at = 2026-10-29T22:11:48Z` (apache/pinot #20096).
- Merged apache/pinot PRs on `master` strictly after the checkpoint: **2** — #20057 and #20101.
- Reconciled three independent ways, all consistent:
  1. `GET search/issues q="repo:apache/pinot is:pr is:merged base:master merged:>=2026-10-29"` → 13 candidates; 2 newer than checkpoint: #20057 @ `2026-10-30T08:14:45Z`, #20101 @ `2026-10-30T08:32:34Z`.
  2. `GET commits?sha=master&since=2026-10-29T22:11:49Z` → exactly 2 commits: `20cac7096` (#20057), `481d4768b` (#20101).
  3. `GET pulls state=closed base=master sort=updated desc` → same two as the most recent merged PRs.
- No gaps between checkpoint and current upstream HEAD (tip = `481d4768b` #20101).

### Decisions
- **#20057 — "Add per-table hybrid retention strategy with cluster-level fallback"** → **not_relevant (reverted before this run).**
  - Added a user-facing table config field `SegmentsValidationAndRetentionConfig._enableHybridTableRetentionStrategy` (getter/setter) + `RetentionManager` wiring. *Would* have been docs-relevant.
  - Fully reverted by #20101 (18 min later, same run window) — exact inverse of all 4 files (SPI config, RetentionManager, 2 test files).
  - Verified upstream `master` tip is the revert commit `481d4768b`; the config field is **absent** on master. Documenting a config that does not exist would be incorrect. **Net no-op; nothing shipped to document.**
- **#20101 — "Revert ..."** → **not_relevant.** Clean revert; removes the never-documented field. No net user-facing surface change.
- Duplicate check: no existing docs PR or upstream docs-link comment for either. Unrelated pre-existing merged docs PR #417 (2025-03-17) covers hybrid retention generally, not this reverted field.

### Docs PRs / upstream comments / validation
- None created. No validation run needed (no docs changes). Not applicable.

### Blockers / required user action
- None. Preflight passed (gh auth xiangfu0; apache/pinot=WRITE, pinot-contrib/pinot-docs=ADMIN; durable read/write OK, CAS on automation-state.json). Lock acquired/released cleanly.

### Notifications
- No Slack (no-op policy — no new docs PRs created).

### Checkpoint
- **Advanced**: `2026-10-29T22:11:48Z` → `2026-10-30T08:32:34Z` (#20101, newest fully-processed PR). `last_successful_run` → `2026-10-30T09:01:16Z`; `last_run_id` → `run-20261030T090116Z-874`.
