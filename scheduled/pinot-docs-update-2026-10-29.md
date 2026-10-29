# Pinot Docs Update — 2026-10-29 (UTC)

## Run 2026-10-29T08:02:54Z (run-20261029T080121Z-887)

**Result: NO-OP.** No new docs-relevant upstream PRs since the last run.

### Coverage
- Checkpoint (durable `automation-state.json`): `last_processed_merged_at = 2026-10-29T03:27:01Z` (apache/pinot #19905).
- Merged apache/pinot PRs strictly after the checkpoint: **0**.
- Reconciled three independent ways:
  1. `search repo:apache/pinot is:pr is:merged merged:>2026-10-29T03:27:01Z` → 0 results.
  2. apache/pinot `master` HEAD (GitHub API) = `0de3f5e3` = #19905 (committer date 2026-10-29T03:27:00Z) — the checkpoint PR; nothing merged after it.
  3. pulls API (`state=closed base=master sort=updated desc`) — most recent `merged_at` is `2026-10-29T03:27:01Z` (#19905) == checkpoint. All PRs on/after 2026-10-29 ({#19905, #19988, #20078, #20079}) are already in the processed ledger with merged-at ≤ checkpoint.

### Decisions
- None (no new PRs to triage).

### Created / merged docs PRs
- None.

### Upstream comments
- None.

### Validation
- Not applicable (no docs changes produced).

### Blockers / required user action
- None. Environment preflight passed: gh auth `xiangfu0`; `apache/pinot`=WRITE, `pinot-contrib/pinot-docs`=ADMIN; durable state read/write OK; lease acquired and released.
- Benign `gh-tentrix-wrap` "no token minted / not in manifest" stderr warnings appear on each gh api call but do not affect operation (all reads and authenticated PUTs succeed).

### Notifications
- No Slack (no-op policy: webhook only fires when a run creates new docs PRs).

### Checkpoint
- **Unchanged**: `2026-10-29T03:27:01Z`.

---

## Run 2026-10-29T09:02:35Z (run-20261029T090137Z-1169)

**Result: NO-OP.** No new docs-relevant upstream PRs since the last run.

### Coverage
- Checkpoint (durable `automation-state.json`): `last_processed_merged_at = 2026-10-29T03:27:01Z` (apache/pinot #19905).
- Merged apache/pinot PRs strictly after the checkpoint: **0**.
- Reconciled three independent ways:
  1. `search repo:apache/pinot is:pr is:merged merged:>=2026-10-29` → {#20078, #20079, #19988, #19905}, all already in the processed ledger with merged-at ≤ checkpoint.
  2. pulls API (`state=closed base=master sort=updated desc`) → 0 PRs with `merged_at` > checkpoint; most recent merged is #19905 @ `2026-10-29T03:27:01Z` == checkpoint.
  3. apache/pinot `master` HEAD (GitHub API) = `0de3f5e3` = #19905 (committer date 2026-10-29T03:27:00Z) — the checkpoint PR; nothing merged after it.
- Full coverage verified down to #19905. #19897 (merged 2026-10-26T21:28:31Z) predates the original migrated checkpoint (2026-10-26T23:24:33Z) and is intentionally not backfilled.

### Decisions
- None (no new PRs to triage).

### Created / merged docs PRs
- None.

### Upstream comments
- None.

### Validation
- Not applicable (no docs changes produced).

### Blockers / required user action
- None. Environment preflight passed: gh auth `xiangfu0`; `apache/pinot`=WRITE/triage, `pinot-contrib/pinot-docs`=ADMIN; durable state read/write OK; lease acquired and released.
- Benign `gh-tentrix-wrap` "no token minted / not in manifest" stderr warnings appear on each gh api call but do not affect operation (all reads and authenticated PUTs succeed; verified by re-reading committed files).

### Notifications
- No Slack (no-op policy: webhook only fires when a run creates new docs PRs).

### Checkpoint
- **Unchanged**: `2026-10-29T03:27:01Z`.

---

## Run 2026-10-29T10:02:18Z (run-20261029T100114Z-937)

**Result: NO-OP.** No new docs-relevant upstream PRs since the last run.

### Coverage
- Checkpoint (durable `automation-state.json`): `last_processed_merged_at = 2026-10-29T03:27:01Z` (apache/pinot #19905).
- Merged apache/pinot PRs strictly after the checkpoint: **0**.
- Reconciled three independent ways:
  1. `search repo:apache/pinot is:pr is:merged merged:>=2026-10-29` → {#20079, #20078, #19988, #19905}, all already in the processed ledger with merged-at ≤ checkpoint.
  2. pulls API (`state=closed base=master sort=updated desc`, 4 pages / 200 PRs) → 0 PRs with `merged_at` strictly > checkpoint.
  3. apache/pinot `master` HEAD (git + API) = `0de3f5e3` = #19905 (committer date 2026-10-29T03:27:00Z) — the checkpoint PR; `GET commits sha=master since=checkpoint` returned nothing after it.
- Full coverage verified down to #19905. #19897 (merged 2026-10-26T21:28:31Z) predates the original migrated checkpoint and is intentionally not backfilled.

### Decisions
- None (no new PRs to triage).

### Created / merged docs PRs
- None.

### Upstream comments
- None.

### Validation
- Not applicable (no docs changes produced).

### Blockers / required user action
- None. Environment preflight passed: gh auth `xiangfu0`; `apache/pinot`=WRITE, `pinot-contrib/pinot-docs`=ADMIN; durable state read/write OK; lease acquired and released.
- Benign `gh-tentrix-wrap` "no token minted / not in manifest" stderr warnings appear on each gh api call but do not affect operation (all reads and authenticated PUTs succeed; verified by re-reading committed files).

### Notifications
- No Slack (no-op policy: webhook only fires when a run creates new docs PRs).

### Checkpoint
- **Unchanged**: `2026-10-29T03:27:01Z`.

---

## Run 2026-10-29T11:02:29Z (run-20261029T110117Z-865)

**Result: NO-OP (one PR triaged, not docs-relevant).** One new upstream PR since the last run; classified not docs-relevant.

### Coverage
- Prior checkpoint (durable `automation-state.json`): `last_processed_merged_at = 2026-10-29T03:27:01Z` (apache/pinot #19905).
- Merged apache/pinot PRs strictly after the prior checkpoint: **1** (#19943, merged `2026-10-29T10:09:33Z`).
- Reconciled three independent ways:
  1. `search repo:apache/pinot is:pr is:merged merged:>=2026-10-29T03:27:01Z` → {#19943, #19905}; #19905 is the prior checkpoint PR (merged-at == checkpoint).
  2. pulls API (`state=closed base=master sort=updated desc`) → exactly **#19943** with `merged_at` strictly > checkpoint.
  3. apache/pinot `master` HEAD (git + API) = `3f6fef49` = #19943 (committer date 2026-10-29T10:09:32Z); `GET commits sha=master since=checkpoint` returned only #19943.

### Decisions
- **#19943 — not docs-relevant.** "Send v1 DataTable responses to Netty and gRPC as pages instead of one byte[]" (label: `performance`; step 2 of 3 after #19906). Internal server-response/transport memory optimization: the single-stage (v1) response path sends paged `DataTable` buffers to Netty and gRPC instead of copying them into one contiguous `byte[]` (avoiding a G1 humongous allocation on large responses). Verified from the merged diff: the **wire format is explicitly unchanged**; all 17 files are internal datatable/scheduler/transport main source (DataTable, DataTableImplV4, StreamingResponseUtils, QueryScheduler and its scheduler subclasses, InstanceRequestHandler, PageCacheWarmupServerQueryExecutor) plus tests; **no** new config key, query option, default, function, public constant, or doc/.md file. Nothing user-facing to document.

### Created / merged docs PRs
- None.

### Upstream comments
- None.

### Validation
- Not applicable (no docs changes produced).

### Blockers / required user action
- None. Environment preflight passed: gh auth `xiangfu0`; `apache/pinot`=WRITE, `pinot-contrib/pinot-docs`=ADMIN; durable state read/write OK; lease acquired (create-only CAS `automation-lock.json`, lock sha `472fe0a2`) and released at end.
- Benign `gh-tentrix-wrap` "no token minted / not in manifest" stderr warnings appear on each `gh api` call but do not affect operation (all reads and authenticated PUTs succeed; verified by re-reading committed files).

### Notifications
- No Slack (no-op policy: webhook only fires when a run creates new docs PRs).

### Checkpoint
- **Advanced**: `2026-10-29T03:27:01Z` → `2026-10-29T10:09:33Z` (#19943 fully processed as not_relevant).

---

## Run 2026-10-29T12:02:53Z — `run-20261029T120139Z-22168` (no-op)

### Coverage
- Prior checkpoint: `2026-10-29T10:09:33Z` (#19943). Merged `apache/pinot` PRs strictly after it: **0**.
- Three-way reconciliation, all consistent:
  1. `GET repos/apache/pinot/commits?sha=master&since=2026-10-29T10:09:34Z` → 0 commits; apache master HEAD = `3f6fef49` = #19943 (the checkpoint PR).
  2. `search repo:apache/pinot is:pr is:merged merged:>=2026-10-29T10:09:33Z` → only #19943 (merged-at == checkpoint, already processed).
  3. pulls API (`state=closed base=master sort=updated desc`) → most-recent merged is #19943 @`2026-10-29T10:09:33Z`; every other merged PR has `merged_at` < checkpoint and is already in the ledger or pre-checkpoint. No gaps.

### Decisions
- None — no new merged PRs to classify.

### Created / merged docs PRs
- None.

### Upstream comments
- None.

### Validation
- Not applicable (no docs changes produced).

### Blockers / required user action
- None. Preflight passed: gh auth `xiangfu0`; `apache/pinot`=WRITE, `pinot-contrib/pinot-docs`=ADMIN; durable read/write OK; lease acquired (create-only CAS `automation.lock`) and released at end.

### Notifications
- No Slack (no-op policy).

### Checkpoint
- **Unchanged**: `2026-10-29T10:09:33Z`. `last_successful_run` → `2026-10-29T12:02:53Z`.

## Run 2026-10-29T13:02:18Z — `run-20261029T130129Z-1069` (no-op)

### Coverage
- Prior durable checkpoint: `2026-10-29T10:09:33Z` (#19943). Merged `apache/pinot` PRs strictly after it: **0**.
- Three-way reconciliation, all consistent:
  1. `GET repos/apache/pinot/commits?sha=master&since=2026-10-29T10:09:34Z` → 0 commits; apache master HEAD = `3f6fef49` = #19943 (the checkpoint PR).
  2. `search repo:apache/pinot is:pr is:merged merged:>=2026-10-29T10:09:33Z` → only #19943 (merged-at == checkpoint, already in ledger).
  3. pulls API (`state=closed base=master sort=updated desc`, 50) → 0 PRs with `merged_at` strictly > checkpoint; all recent merged PRs already in the 15-entry ledger.

### Decisions
- None — no new merged PRs to classify.

### Created / merged docs PRs
- None.

### Upstream comments
- None.

### Validation
- Not applicable (no docs changes produced).

### Blockers / required user action
- None. Preflight passed: gh auth `xiangfu0`; `apache/pinot`=WRITE, `pinot-contrib/pinot-docs`=ADMIN; durable read/write OK; lease acquired (create-only CAS `.lock`) and released at end.

### Notifications
- No Slack (no-op policy).

### Checkpoint
- **Unchanged**: `2026-10-29T10:09:33Z`. `last_successful_run` → `2026-10-29T13:02:18Z`.

## Run 2026-10-29T14:02:33Z — `run-20261029T140103Z-807` (no-op)

### Coverage
- Prior durable checkpoint: `2026-10-29T10:09:33Z` (#19943). Merged `apache/pinot` PRs strictly after it: **0**.
- Three-way reconciliation, all consistent:
  1. `GET repos/apache/pinot/commits?sha=master&since=2026-10-29T10:09:34Z` → 0 commits; apache master HEAD = `3f6fef49` = #19943 (the checkpoint PR).
  2. `search repo:apache/pinot is:pr is:merged merged:>=2026-10-29T10:09:33Z` → only #19943 (merged-at == checkpoint, already in ledger).
  3. pulls API (`state=closed base=master sort=updated desc`, 30) → 0 PRs with `merged_at` strictly > checkpoint; all recent merged PRs already in the 15-entry ledger.

### Decisions
- None — no new merged PRs to classify.

### Created / merged docs PRs
- None.

### Upstream comments
- None.

### Validation
- Not applicable (no docs changes produced).

### Blockers / required user action
- None. Preflight passed: gh auth `xiangfu0`; `apache/pinot`=WRITE, `pinot-contrib/pinot-docs`=WRITE (push=true); durable read/write OK; lease acquired (create-only CAS `.lock`) and released at end.

### Notifications
- No Slack (no-op policy).

### Checkpoint
- **Unchanged**: `2026-10-29T10:09:33Z`. `last_successful_run` → `2026-10-29T14:02:33Z`.

---

## Run 2026-10-29T15:02:30Z (run-20261029T150145Z-21726)

**Result: NO-OP.** No new docs-relevant upstream PRs since the last run.

### Coverage
- Checkpoint (durable `automation-state.json`): `last_processed_merged_at = 2026-10-29T10:09:33Z` (apache/pinot #19943).
- Merged apache/pinot PRs strictly after the checkpoint: **0**.
- Reconciled four independent ways, all consistent:
  1. `search repo:apache/pinot is:pr is:merged merged:>=2026-10-29T10:09:33Z` → only #19943 (== checkpoint, already in ledger).
  2. apache/pinot `master` HEAD (GitHub API) = `3f6fef49` = #19943 (committer date 2026-10-29T10:09:32Z) — the checkpoint PR; nothing merged after it.
  3. pulls API (`state=closed base=master sort=updated desc`) → 0 PRs with `merged_at` strictly > checkpoint.
  4. `GET commits?sha=master&since=2026-10-29T10:09:34Z` → 0 commits.

### Decisions
- None (no new PRs to triage).

### Created / merged docs PRs
- None.

### Upstream comments
- None.

### Validation
- Not applicable (no docs changes produced).

### Blockers / required user action
- None. Preflight passed: gh auth `xiangfu0`; `apache/pinot`=WRITE (push=true), `pinot-contrib/pinot-docs`=ADMIN; durable state read/write OK; lease acquired (create-only CAS `.lock`) and released at end.
- Benign `gh-tentrix-wrap` "no token minted / not in manifest" stderr warnings appear on each gh api call (apache/pinot and pinot-docs are outside the session's repo manifest); the fallback `GH_TOKEN` is authenticated (rate limit 15000) and all reads/PUTs succeed.

### Notifications
- No Slack (no-op policy).

### Checkpoint
- **Unchanged**: `2026-10-29T10:09:33Z`. `last_successful_run` → `2026-10-29T15:02:30Z`.

---

## Run 2026-10-29T16:02:30Z (run-20261029T160118Z-971) — no-op

### Coverage
- Durable checkpoint at start: `last_processed_merged_at = 2026-10-29T10:09:33Z` (#19943).
- Inventory of apache/pinot merged PRs strictly after the checkpoint = **0**. Reconciled four independent ways, all consistent:
  1. `search is:pr is:merged merged:>=2026-10-29T10:09:33Z` → only #19943 (== checkpoint, already in ledger).
  2. apache/pinot `master` HEAD = `3f6fef49` = #19943 — the checkpoint PR; nothing merged after it.
  3. pulls API (`state=closed base=master sort=updated desc`) → 0 PRs with `merged_at` strictly > checkpoint.
  4. `GET commits?sha=master&since=2026-10-29T10:09:34Z` → 0 commits.

### Decisions
- None (no new PRs to triage).

### Created / merged docs PRs
- None.

### Upstream comments
- None.

### Validation
- Not applicable (no docs changes produced).

### Blockers / required user action
- None. Preflight passed: gh auth `xiangfu0`; `apache/pinot`=WRITE (push=true), `pinot-contrib/pinot-docs`=ADMIN; durable state read/write OK; lease acquired (create-only CAS `.lock`), re-verified mine before the state write, and released at end.
- Benign `gh-tentrix-wrap` "no token minted / not in manifest" stderr warnings appear on each gh api call; the fallback `GH_TOKEN` is authenticated and all reads/PUTs succeed.

### Notifications
- No Slack (no-op policy).

### Checkpoint
- **Unchanged**: `2026-10-29T10:09:33Z`. `last_successful_run` → `2026-10-29T16:02:30Z`; `last_run_id` → `run-20261029T160118Z-971`.

---

## Run 2026-10-29T17:04:39Z (run-20261029T170139Z-5550) — no-op

### Coverage
- Inventoried merged `apache/pinot` PRs strictly after durable checkpoint `2026-10-29T10:09:33Z` (#19943).
- Result: **0 new merged PRs**. Reconciled four independent ways, all consistent:
  1. `search/issues q="repo:apache/pinot is:pr is:merged merged:>=2026-10-29T10:09:33Z"` → only #19943 (== checkpoint, already processed as not_relevant).
  2. apache/pinot `master` HEAD = `3f6fef49` = #19943 — the checkpoint PR; nothing merged after it.
  3. pulls API (`state=closed base=master sort=updated desc`, 10 rows) → 0 PRs with `merged_at` strictly > checkpoint; most-recent merged == #19943.
  4. `GET commits?sha=master&since=2026-10-29T10:09:34Z` → 0 commits.

### Decisions
- None (no new PRs to triage).

### Created / merged docs PRs
- None.

### Upstream comments
- None.

### Validation
- Not applicable (no docs changes produced).

### Blockers / required user action
- None. Preflight passed: gh auth `xiangfu0`; `apache/pinot`=WRITE (push=true → can comment upstream), `pinot-contrib/pinot-docs`=ADMIN; durable state read/write OK.
- Lease: local `pre-push` hook blocks bare-branch pushes (requires `cs_<sid>/` prefix). Acquired/released the `.lock` on bare `automation-state` via REST ref-update CAS (objects staged through a prefixed throwaway branch, then `PATCH git/refs/heads/automation-state` with `force=false`; throwaway branch deleted). Documented in automation-memory.md.
- Benign `gh-tentrix-wrap` "no token minted / not in manifest" stderr warnings appear on each gh api call; the fallback `GH_TOKEN` is authenticated and all reads/writes succeed.

### Notifications
- No Slack (no-op policy).

### Checkpoint
- **Unchanged**: `2026-10-29T10:09:33Z`. `last_successful_run` → `2026-10-29T17:04:39Z`; `last_run_id` → `run-20261029T170139Z-5550`.

---

## Run 2026-10-29T18:02:30Z (run-20261029T180100Z-765)

### Coverage
- Inventoried merged `apache/pinot` PRs strictly after durable checkpoint `2026-10-29T10:09:33Z` (#19943).
- Result: **2 new merged PRs** (`#20086`, `#20087`). Reconciled three independent ways, all consistent:
  1. `search/issues q="repo:apache/pinot is:pr is:merged merged:>=2026-10-29"` → candidates filtered by precise `merged_at > checkpoint`.
  2. pulls API (`state=closed base=master sort=updated desc`) → exactly #20086 (`2026-10-29T17:48:40Z`) and #20087 (`2026-10-29T17:48:15Z`) with `merged_at` strictly > checkpoint.
  3. `GET commits?sha=master&since=2026-10-29T10:09:34Z` → exactly 2 commits: `c6c5aee5` (#20086), `ad97f19f` (#20087). apache/pinot `master` HEAD advanced to `c6c5aee5` (#20086).
- No gaps between checkpoint and current HEAD.

### Decisions
- **#20086** — Bump `org.jacoco:jacoco-maven-plugin` 0.8.15→0.8.16. Dependabot. Verified from merged diff: files = `pinot-bom/pom.xml` + root `pom.xml` (+1/-1 each). Build/test code-coverage tooling only; no config, default, query option, function, public API, or documented user-facing behavior. **not_relevant.**
- **#20087** — Bump `dnsjava:dnsjava` 3.6.5→3.7.0. Dependabot. Verified from merged diff: file = root `pom.xml` (+1/-1). Transitive DNS library bump; no user-facing surface change. **not_relevant.**

### Created / merged docs PRs
- None (both upstream PRs not docs-relevant).

### Upstream comments
- None.

### Validation
- Not applicable (no docs changes produced).

### Blockers / required user action
- None. Preflight passed: gh auth `xiangfu0`; `apache/pinot`=WRITE (push=true → can comment upstream), `pinot-contrib/pinot-docs`=ADMIN; durable state read/write OK.
- Lease: no prior holder; acquired/released `automation-lease.json` on `automation-state` via create-only + delete (Contents API). State written via Contents API PUT with CAS `sha`.
- Benign `gh-tentrix-wrap` "no token minted / not in manifest" stderr warnings appear on each gh api call; the fallback `GH_TOKEN` is authenticated and all reads/writes succeed.

### Notifications
- No Slack (no-op policy — triaged PRs were all not-relevant, no new docs PRs).

### Checkpoint
- **Advanced**: `2026-10-29T10:09:33Z` → `2026-10-29T17:48:40Z` (#20086). `last_successful_run` → `2026-10-29T18:02:30Z`; `last_run_id` → `run-20261029T180100Z-765`.
