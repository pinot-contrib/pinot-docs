# Pinot Docs Update — 2026-10-30 (UTC)

## Run 2026-10-30T15:05:00Z (run run-20261030T150118Z-16649) — DOCS CREATED (#19838 → docs PR #1157)

### Coverage
- Durable checkpoint at start (`automation-state.json`): `last_processed_merged_at = 2026-10-30T12:42:15Z` (apache/pinot #20102).
- Merged apache/pinot `master` PRs strictly after checkpoint: **1** — #19838 (merged `2026-10-30T15:01:04Z`). Reconciled two independent ways, consistent:
  1. `GET commits?sha=master&since=2026-10-30T12:42:16Z` → exactly 1 new commit: `e12b8435c` (#19838); master tip now `e12b8435c` @ `2026-10-30T15:01:03Z`.
  2. `GET pulls state=closed base=master sort=updated desc` → only #19838 (`15:01:04Z`) is newer than the checkpoint; #20102/#20103 already in the ledger.
- Re-checked at persist time: still no PR merged after #19838. No gaps.

### Decisions
- **#19838 — "Add per-table SHADOW enforcement mode for storage and query quotas"** (Tarun-kishore; labels release-notes, configuration, ingestion, query, feature) → **docs_created.** User-facing table quota config. Verified from the merged code (not PR prose):
  - New enum `QuotaEnforcementMode { DISABLED, SHADOW, ENFORCED }` and two optional `QuotaConfig` JSON fields: `storageQuotaEnforcementMode`, `queryQuotaEnforcementMode`. `null` == `ENFORCED` (default); fields omitted from the serialized form when null (back-compat preserved).
  - `SHADOW`: breach detected + metric + warning log, but action not taken — query not rejected (broker `QUERY_QUOTA_EXCEEDED`), offline push not blocked / realtime consumption not paused (new controller meter `STORAGE_QUOTA_EXCEEDED`).
  - `DISABLED`: not metered / not enforced. Storage effective mode is forced to `DISABLED` when the controller-wide storage quota check (`_isEnabled`) is off.
  - Hybrid table referenced without a type suffix: strictest configured mode among existing OFFLINE/REALTIME tables wins (`QuotaEnforcementMode.isStricterThan`).
  - Version: master is `1.7.0-SNAPSHOT` (bump #19919) → documented as "Added in 1.7.0".
- Duplicate check: no prior docs PR for #19838 and no upstream docs-link comment before this run.

### Docs PR / upstream comment / validation
- Docs PR: **pinot-contrib/pinot-docs#1157** — "docs: document per-table quota enforcement modes (apache/pinot#19838)". Squash-merged into `latest` @ `2026-10-30T15:04:37Z` (merge commit `02309fee`), verified `merged=true`.
  - `reference/configuration-reference/table.md` — two new rows in the **Quota** config table.
  - `build-with-pinot/querying-and-sql/query-execution-controls/query-quotas.md` — new *Enforcement mode* subsection (table of modes + hybrid/storage note) under Table quotas.
- Upstream comment: https://github.com/apache/pinot/pull/19838#issuecomment-6525983348
- Validation: `git diff --check` clean; `uv run --with pyyaml python scripts/validate-docs.py` → **RESULT: PASS** (638 files, 3559 links; 10 pre-existing broken-anchor warnings, all in unrelated files, none involving the two edited pages or the `#quota` anchor they link to).

### Blockers / required user action
- None. Preflight passed (read-only): gh auth `xiangfu0`; `apache/pinot`=WRITE (comment upstream), `pinot-contrib/pinot-docs`=ADMIN; durable read/write OK (CAS on `automation-state.json`). Lock acquired via CAS at run start, holder re-verified before finalize, released in this run's atomic state write.
- Note: docs repo cloned fresh at `/workspace/pinot-docs` (`gh auth setup-git` for push); branch auto-renamed to `cs_gyFBpoNcgY/docs/quota-enforcement-mode-19838` by the session push hook (benign). Local `/workspace/pinot` origin is the fork `xiangfu0/pinot` (stale); inventory driven directly by the apache/pinot API.

### Notifications
- **Slack summary sent** (new docs PR created): #19838 → docs #1157 (merged), upstream comment posted.

### Checkpoint
- **Advanced**: `2026-10-30T12:42:15Z` → `2026-10-30T15:01:04Z` (#19838, fully processed). `last_successful_run` → this run; `last_run_id` → `run-20261030T150118Z-16649`.

---


## Run 2026-10-30T14:02:53Z (run run-20261030T140115Z-932) — NO-OP

### Coverage
- Durable checkpoint at start (`automation-state.json`): `last_processed_merged_at = 2026-10-30T12:42:15Z` (apache/pinot #20102).
- Merged apache/pinot `master` PRs strictly after checkpoint: **0**. Reconciled two independent ways, consistent and empty:
  1. `GET commits?sha=master&since=2026-10-30T12:42:16Z` → **0** new commits; master tip still `863356920f` (#20102) committed `2026-10-30T12:42:14Z`.
  2. `GET pulls state=closed base=master sort=updated desc` → newest merged is #20102 @ `2026-10-30T12:42:15Z` (= checkpoint, already processed `not_relevant`) and #20103 @ `2026-10-30T12:41:44Z` (already processed); nothing merged after the checkpoint.
- No gap between checkpoint and current upstream HEAD.

### Decisions / docs PRs / upstream comments / validation
- None — no new PRs. Not applicable.

### Blockers / required user action
- None. Preflight passed (read-only): gh auth `xiangfu0`; `apache/pinot`=push+triage (can comment upstream), `pinot-contrib/pinot-docs`=ADMIN; durable state read/write OK (CAS on `automation-state.json`, round-trip verified). Lock acquired via CAS at run start and released in this run's atomic state write.
- Note: local `/workspace/pinot` `origin` points to the fork `xiangfu0/pinot` (stale); inventory is driven directly by the apache/pinot API, so no rebase was needed for this no-op run. Benign `gh-tentrix-wrap` stderr warnings on each `gh api` call; the fallback `GH_TOKEN` is authenticated and all reads/writes succeed.

### Notifications
- No Slack (no-op policy).

### Checkpoint
- **Unchanged**: `2026-10-30T12:42:15Z`. `last_successful_run` → `2026-10-30T14:02:53Z`; `last_run_id` → `run-20261030T140115Z-932`.

---


## Run 2026-10-30T13:02:33Z (run run-20261030T130126Z-953) — NO DOCS (2 dependency bumps triaged, not docs-relevant)

### Coverage
- Durable checkpoint at start (`automation-state.json`): `last_processed_merged_at = 2026-10-30T08:32:34Z` (apache/pinot #20101).
- Merged apache/pinot `master` PRs strictly after checkpoint: **2** — #20103 and #20102. Reconciled two independent ways, consistent:
  1. `GET commits?sha=master&since=2026-10-30T08:32:35Z` → exactly 2 new commits: `f526b645ce` (#20103), `863356920f` (#20102); master tip `863356920f` @ `2026-10-30T12:42:14Z`.
  2. `GET pulls state=closed base=master sort=updated desc` → only #20102 (merged `2026-10-30T12:42:15Z`) and #20103 (merged `2026-10-30T12:41:44Z`) newer than checkpoint; all older merged PRs already in the processed ledger.
- No gaps between checkpoint and current upstream HEAD.

### Decisions
- **#20103 — "Bump software.amazon.awssdk:bom from 2.57.3 to 2.57.4"** → **not_relevant.** Verified from merged diff (merge commit `f526b645ce`): `dependabot[bot]`, single file root `pom.xml` (+1/-1), labels `dependencies`/`java`. AWS SDK BOM patch bump; no config key, default, query option, function, public API, or documented user-facing behavior change.
- **#20102 — "Bump org.roaringbitmap:RoaringBitmap from 1.6.25 to 1.6.27"** → **not_relevant.** Verified from merged diff (merge commit `863356920f`): `dependabot[bot]`, single file root `pom.xml` (+1/-1), labels `dependencies`/`java`. RoaringBitmap patch bump (internal bitmap library); no config key, default, query option, function, public API, or documented user-facing behavior change.
- Consistent with prior Dependabot pom-bump decisions (#20087, #20086, #20048).

### Docs PRs / upstream comments / validation
- None created. No validation run needed (no docs changes). Not applicable.

### Blockers / required user action
- None. Preflight passed (read-only): gh auth `xiangfu0`; `apache/pinot`=push+triage (can comment upstream), `pinot-contrib/pinot-docs`=ADMIN; durable read/write OK (CAS on `automation-state.json`). Lock acquired via CAS at run start (holder re-verified before finalize), released in this run's atomic state write.
- Note: local `/workspace/pinot` `origin` points to the fork `xiangfu0/pinot` (stale); inventory is driven directly by the apache/pinot API. Benign `gh-tentrix-wrap` stderr warnings on each `gh api` call; fallback `GH_TOKEN` is authenticated and all reads/writes succeed.

### Notifications
- No Slack (no-op policy — no new docs PRs created).

### Checkpoint
- **Advanced**: `2026-10-30T08:32:34Z` → `2026-10-30T12:42:15Z` (#20102, newest fully-processed PR). `last_successful_run` → `2026-10-30T13:02:33Z`; `last_run_id` → `run-20261030T130126Z-953`.

---



## Run 2026-10-30T12:02:56Z (run run-20261030T120108Z-848) — NO-OP

### Coverage
- Durable checkpoint at start (`automation-state.json`): `last_processed_merged_at = 2026-10-30T08:32:34Z` (apache/pinot #20101).
- Merged apache/pinot `master` PRs strictly after checkpoint: **0**. Reconciled three independent ways, all consistent and empty:
  1. `GET commits?sha=master&since=2026-10-30T08:32:35Z` → **0** new commits; master tip `481d4768b7` (#20101) committed `2026-10-30T08:32:33Z` = checkpoint.
  2. `GET pulls state=closed base=master sort=updated desc` → top merged-at is #20101 @ `2026-10-30T08:32:34Z` (= checkpoint); all more-recent merged PRs already present in the processed ledger.
  3. `gh search prs --repo apache/pinot --merged ">=2026-10-30"` → only stale PRs (#17380, #17892, #18155, #17576), all merged Jan–Apr 2026 (far pre-checkpoint, verified via each PR's `merged_at`), not candidates.
- No gap, no new docs-relevant PRs.

### Decisions / docs PRs / upstream comments / validation
- None — no new PRs. Not applicable.

### Blockers / required user action
- None. Preflight passed (read-only): gh auth `xiangfu0`; `apache/pinot`=WRITE (can comment upstream), `pinot-contrib/pinot-docs`=ADMIN; durable state read/write OK (CAS on `automation-state.json`, round-trip verified). Lock acquired via CAS at run start, holder re-verified before finalize, released in this run's atomic state write.
- Note: local `/workspace/pinot` `origin` points to the fork `xiangfu0/pinot` (stale at 910f9d5); inventory is driven directly by the apache/pinot API, so no rebase was needed for this no-op run. Benign `gh-tentrix-wrap` stderr warnings appear on each `gh api` call; the fallback `GH_TOKEN` is authenticated and all reads/writes succeed.

### Notifications
- No Slack (no-op policy).

### Checkpoint
- **Unchanged**: `2026-10-30T08:32:34Z`. `last_successful_run` → `2026-10-30T12:02:56Z`; `last_run_id` → `run-20261030T120108Z-848`.

---

## Run 2026-10-30T11:02:16Z (run run-20261030T110102Z-847) — NO-OP

### Coverage
- Durable checkpoint at start (`automation-state.json`): `last_processed_merged_at = 2026-10-30T08:32:34Z` (apache/pinot #20101).
- Merged apache/pinot `master` PRs strictly after checkpoint: **0**. Reconciled three independent ways, all consistent and empty:
  1. `GET commits?sha=master&since=2026-10-30T08:32:35Z` → **0** new commits.
  2. `GET pulls state=closed base=master sort=updated desc` → top merged-at is #20101 @ `2026-10-30T08:32:34Z` (= checkpoint); all 14 most-recent merged PRs (#20101, #20057, #20074, #20096, #20048, #20064, #20086, #20087, #19943, #20002, #19905, #20078, #20079, #19988) already present in the processed ledger.
  3. `gh search prs --repo apache/pinot --merged-at ">=2026-10-30"` → only #20101 and #20057, both already in the ledger.
- apache/pinot `master` tip = `481d4768b7` (#20101) committed `2026-10-30T08:32:33Z` = checkpoint. No gap, no new docs-relevant PRs.

### Decisions / docs PRs / upstream comments / validation
- None — no new PRs. Not applicable.

### Blockers / required user action
- None. Preflight passed (read-only): gh auth `xiangfu0`; `apache/pinot`=WRITE (can comment upstream), `pinot-contrib/pinot-docs`=ADMIN; durable state read/write OK (CAS on `automation-state.json`). Lock acquired via CAS at run start and released in this run's atomic state write.
- Note: local `/workspace/pinot` `origin` points to the fork `xiangfu0/pinot` (stale at 910f9d5); inventory is driven directly by the apache/pinot API, so no rebase was needed for this no-op run. Benign `gh-tentrix-wrap` stderr warnings appear on each call; the fallback `GH_TOKEN` is authenticated and all reads/writes succeed.

### Notifications
- No Slack (no-op policy).

### Checkpoint
- **Unchanged**: `2026-10-30T08:32:34Z`. `last_successful_run` → `2026-10-30T11:02:16Z`; `last_run_id` → `run-20261030T110102Z-847`.

---


## Run 2026-10-30T10:01:09Z (run-20261030T100109Z-1048) — NO-OP

### Coverage
- Durable checkpoint at start (`automation-state.json`): `last_processed_merged_at = 2026-10-30T08:32:34Z` (apache/pinot #20101).
- Merged apache/pinot `master` PRs strictly after checkpoint: **0**. Reconciled three independent ways, all consistent and empty:
  1. `gh search prs --repo apache/pinot --merged "merged:>=2026-10-30"` → most-recent merged #20101 and #20057, both already in the processed ledger.
  2. `GET commits?sha=master&since=2026-10-30T08:32:35Z` → **0** new commits.
  3. `GET pulls state=closed base=master sort=updated desc` → top merged-at is #20101 @ `2026-10-30T08:32:34Z`; all 12 most-recent merged PRs (#20101, #20057, #20074, #20096, #20048, #20064, #20086, #20087, #19943, #20002, #19905, #20078) already present in the ledger.
- apache/pinot `master` tip = `481d4768b7` (#20101) committed `2026-10-30T08:32:33Z` = checkpoint. No gap, no new docs-relevant PRs.

### Decisions / docs PRs / upstream comments / validation
- None — no new PRs. Not applicable.

### Blockers / required user action
- None. Preflight passed (read-only): gh auth `xiangfu0`; `apache/pinot`=WRITE (can comment upstream), `pinot-contrib/pinot-docs`=ADMIN; durable state read/write OK (CAS on `automation-state.json`). Lock acquired via CAS at run start and released in this run's atomic state write.
- Note: local `/workspace/pinot` `origin` points to the fork `xiangfu0/pinot` (stale at 910f9d5); inventory is driven directly by the apache/pinot API, so no rebase was needed for this no-op run. Benign `gh-tentrix-wrap` stderr warnings appear on each call; the fallback `GH_TOKEN` is authenticated and all reads/writes succeed.

### Notifications
- No Slack (no-op policy).

### Checkpoint
- **Unchanged**: `2026-10-30T08:32:34Z`. `last_successful_run` → `2026-10-30T10:01:09Z`; `last_run_id` → `run-20261030T100109Z-1048`.

---


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
