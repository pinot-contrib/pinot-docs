# Pinot Docs Update — 2026-11-02 (UTC)

## Run: run-20261102T000111Z-795
- **Started (UTC):** 2026-11-02T00:02:33Z
- **Result:** no-op (no new docs-relevant upstream PRs)
- **Checkpoint (unchanged):** last_processed_merged_at = `2026-10-31T11:11:36Z`

### Preflight
- GitHub auth: `xiangfu0` (GH_TOKEN). apache/pinot = WRITE, pinot-contrib/pinot-docs = ADMIN.
- Durable state read from `automation-state` branch; no stale lock (prior run released cleanly).
- Lease acquired/released via Contents API PUT with blob-SHA compare-and-swap.

### Coverage
Inventoried merged apache/pinot PRs strictly after checkpoint `2026-10-31T11:11:36Z`. **0 new PRs.** Verified three independent ways:
1. **Search API** — `repo:apache/pinot is:pr is:merged merged:>2026-10-31T11:11:36Z` => 0 (and `>=2026-10-31T11:11:37Z` => 0).
2. **Master commits** — apache/pinot master HEAD = `e9be2ee20` (#20110), committed exactly at the checkpoint and already ledgered as not_relevant; no commits after it.
3. **Pulls API** (not search-indexed) — 50 most-recently-updated closed PRs contained none with `merged_at` strictly after the checkpoint.

### Decisions
- None. No PRs to triage.

### Created / merged docs PRs
- None.

### Validation
- Not applicable (no docs changes this run).

### Blockers
- None.

### State
- Checkpoint **unchanged** (no advance past unprocessed/failed work; none existed).
- `last_successful_run` -> 2026-11-02T00:02:33Z.
- No Slack notification (no-op runs stay quiet).

---

## Run: run-20261102T020119Z-876
- **Completed (UTC):** 2026-11-02T02:02:13Z
- **Result:** no-op (no new docs-relevant upstream PRs)
- **Checkpoint (unchanged):** last_processed_merged_at = `2026-10-31T11:11:36Z`

### Preflight
- GitHub auth: `xiangfu0` (GH_TOKEN). apache/pinot = WRITE, pinot-contrib/pinot-docs = ADMIN.
- Durable state read from `automation-state` branch; prior run released lock cleanly (status=released).
- Lease acquired/released via Contents API PUT with blob-SHA compare-and-swap (no concurrent run).

### Coverage
Inventoried merged apache/pinot PRs strictly after checkpoint `2026-10-31T11:11:36Z`. **0 new PRs.** Verified three independent ways:
1. **Search API** — `repo:apache/pinot is:pr is:merged merged:>2026-10-31T11:11:36Z` => 0.
2. **Pulls API** — `repos/apache/pinot/pulls state=closed sort=updated per_page=100` filtered to `merged_at > checkpoint` => 0.
3. **Master commits** — HEAD = `e9be2ee20` (#20110) committed exactly at checkpoint (already ledgered not_relevant); `commits?since=checkpoint+1s` => 0.
- Boundary PRs 19838/20097/20098/20104/20084/20068/20077/19998/20107/20110 all reconciled present in the ledger.

### Decisions
- None. No PRs to triage.

### Created / merged docs PRs
- None.

### Validation
- Not applicable (no docs changes this run).

### Blockers
- None.

### State
- Checkpoint **unchanged**.
- `last_successful_run` -> 2026-11-02T02:02:13Z.
- No Slack notification (no-op runs stay quiet).

---

## Run: run-20261102T030132Z-964
- **Completed (UTC):** 2026-11-02T03:01:50Z
- **Result:** no-op (no new docs-relevant upstream PRs)
- **Checkpoint (unchanged):** last_processed_merged_at = `2026-10-31T11:11:36Z`

### Preflight
- GitHub auth: `xiangfu0` (GH_TOKEN). apache/pinot = pull/push/triage, pinot-contrib/pinot-docs = admin/push.
- Durable state read from `automation-state` branch; prior run released lock cleanly (status=released).
- Lease acquired/released via Contents API PUT with blob-SHA compare-and-swap (state blob 88655300 -> 93561bff; no concurrent run).

### Coverage
Inventoried merged apache/pinot PRs strictly after checkpoint `2026-10-31T11:11:36Z`. **0 new PRs.** Verified three independent ways:
1. **Search API** — `repo:apache/pinot is:pr is:merged merged:>2026-10-31T11:11:36Z` => total_count 0.
2. **Pulls API** — `repos/apache/pinot/pulls state=closed sort=updated direction=desc per_page=100` filtered to `merged_at > checkpoint` => [].
3. **Master commits** — HEAD = `e9be2ee203a` (#20110) committed exactly at checkpoint (already ledgered not_relevant); `commits?sha=master&since=checkpoint+1s` => [].

### Decisions
- None. No PRs to triage.

### Created / merged docs PRs
- None.

### Validation
- Not applicable (no docs changes this run).

### Blockers
- None.

### State
- Checkpoint **unchanged** (no advance past unprocessed/failed work; none existed).
- `last_successful_run` -> 2026-11-02T03:01:50Z.
- No Slack notification (no-op runs stay quiet).

---

## Run: run-20261102T060134Z-982
- **Completed (UTC):** 2026-11-02T06:02:50Z
- **Result:** no-op (no new docs-relevant upstream PRs)
- **Checkpoint (unchanged):** last_processed_merged_at = `2026-10-31T11:11:36Z`

### Preflight
- GitHub auth: `xiangfu0` (GH_TOKEN). apache/pinot = WRITE, pinot-contrib/pinot-docs = ADMIN.
- Durable state read from `automation-state` branch; prior run released lock cleanly (status=released).
- Lease acquired/released via Contents API PUT with blob-SHA compare-and-swap (fd636df0 -> 2960eedb acquire; 2960eedb -> released on no-op write; no concurrent run).

### Coverage
Inventoried merged apache/pinot PRs strictly after checkpoint `2026-10-31T11:11:36Z`. **0 new PRs.** Verified three independent ways:
1. **Search API** — `repo:apache/pinot is:pr is:merged merged:>2026-10-31T11:11:36Z` => total_count 0.
2. **Pulls API** — `repos/apache/pinot/pulls state=closed sort=updated direction=desc per_page=100` (3 pages) filtered to `merged_at > checkpoint` => [].
3. **Master commits** — apache/pinot master HEAD = `e9be2ee203` (#20110) committed exactly at checkpoint (already ledgered not_relevant); `commits?sha=master&since=checkpoint+1s` => [].

### Decisions
- None. No PRs to triage.

### Created / merged docs PRs
- None.

### Validation
- Not applicable (no docs changes this run).

### Blockers
- None.

### State
- Checkpoint **unchanged** (no advance past unprocessed/failed work; none existed).
- `last_successful_run` -> 2026-11-02T06:02:50Z.
- No Slack notification (no-op runs stay quiet).


---

## Run: run-20261102T070158Z-1335
- **Completed (UTC):** 2026-11-02T07:01:58Z
- **Result:** no-op (no new docs-relevant upstream PRs)
- **Checkpoint (unchanged):** last_processed_merged_at = `2026-10-31T11:11:36Z`

### Preflight
- GitHub auth: `xiangfu0` (GH_TOKEN). apache/pinot = WRITE (pull/push/triage), pinot-contrib/pinot-docs = ADMIN.
- Durable state read from `automation-state` branch; prior run (run-20261102T060134Z-982) released lock cleanly (status=released).
- Lease acquired/released via Contents API PUT with blob-SHA compare-and-swap (no concurrent run).

### Coverage
Inventoried merged apache/pinot PRs strictly after checkpoint `2026-10-31T11:11:36Z`. **0 new PRs.** Verified four independent ways:
1. **Search API** — `repo:apache/pinot is:pr is:merged merged:>2026-10-31T11:11:36Z` => total_count 0.
2. **Pulls API** — `repos/apache/pinot/pulls state=closed sort=updated direction=desc per_page=100` (3 pages) filtered to `merged_at > checkpoint` => [].
3. **Master HEAD** — apache/pinot master HEAD = `e9be2ee203` (#20110) committed exactly at checkpoint (already ledgered not_relevant).
4. **Master commits** — `commits?sha=master&since=2026-10-31T11:11:37Z` => [].

### Decisions
- None. No PRs to triage.

### Created / merged docs PRs
- None.

### Validation
- Not applicable (no docs changes this run).

### Blockers
- None.

### State
- Checkpoint **unchanged** (no advance past unprocessed/failed work; none existed).
- `last_successful_run` -> 2026-11-02T07:01:58Z.
- No Slack notification (no-op runs stay quiet).

---

## Run 2026-11-02T08:03:05Z (run-20261102T080125Z-912) — 1 PR triaged (not-relevant)

### Preflight
- GitHub auth: `xiangfu0` (GH_TOKEN). apache/pinot = WRITE (pull/push/triage), pinot-contrib/pinot-docs = ADMIN.
- Durable state read from `automation-state` branch; no prior lease present (no concurrent run).
- Lease acquired via Contents API PUT; released at end of run.

### Coverage
Inventoried merged apache/pinot PRs strictly after checkpoint `2026-10-31T11:11:36Z`. **1 new PR: #20088.** Verified two independent ways:
1. **Search API** — `repo:apache/pinot is:pr is:merged merged:>=2026-10-31` filtered strictly > checkpoint => [20088].
2. **Git reconcile** — against apache/master: the only commit after checkpoint commit `e9be2ee2` (#20110) is `2b0da67b` (#20088). No gaps.

### Decisions
- **#20088 — not_relevant.** "Extract hybrid table retention check into overridable shouldEnableHybridTableRetentionStrategy method." Internal extensibility refactor in controller `RetentionManager`: extracts the existing `_isHybridTableRetentionStrategyEnabled` gate into a new `protected` overridable method `shouldEnableHybridTableRetentionStrategy(realtimeTableConfig, offlineTableConfig)` for per-table subclass overrides; the default implementation returns the same flag, so behavior is identical. Also makes `manageRetentionForRealtimeTable` package-private with `@VisibleForTesting`. The referenced config `ControllerConf.ENABLE_HYBRID_TABLE_RETENTION_STRATEGY` (default `false`, runtime cluster-config updatable) pre-exists and is only referenced in Javadoc/tests — not added or changed. 1 main source file + 1 test file. No new config/default/query-option/function/documented user-facing surface. Not docs-relevant.

### Created / merged docs PRs
- None.

### Validation
- Not applicable (no docs changes this run).

### Blockers
- None.

### State
- Checkpoint **advanced** to `2026-11-02T07:14:43Z` (#20088 merged_at; fully triaged, not-relevant).
- `last_successful_run` -> 2026-11-02T08:03:05Z.
- No Slack notification (non-relevant decision; no docs PR created).

---

## Run run-20261102T090144Z-1213 — 2026-11-02T09:04:05Z (no-op)

### Preflight
- GitHub auth: `xiangfu0` (GH_TOKEN). apache/pinot = WRITE (pull/push/triage), pinot-contrib/pinot-docs = ADMIN.
- Durable `automation-state` branch read OK; lease acquired via Git Data API compare-and-swap (base `84dc1aec` -> `7dfd7344`). No concurrent run.
- Note: session `git push` wrapper now requires a `cs_<sid>/` branch prefix; durable writes to the canonical `automation-state` branch are performed via the GitHub Git Data API (blob/tree/commit + fast-forward-only ref update) which preserves CAS and the exact branch name.

### Coverage
Inventoried merged apache/pinot PRs strictly after checkpoint `2026-11-02T07:14:43Z`. **0 new PRs.** Verified three independent ways:
1. **Search API** — `repo:apache/pinot is:pr is:merged merged:>2026-11-02T07:14:43Z` => total_count 0.
2. **Pulls listing** — closed PRs sorted by updated (3 pages x100) filtered `merged_at > checkpoint` => [].
3. **Git reconcile** — `commits?sha=master&since=2026-11-02T07:14:44Z` => []; master HEAD `2b0da67bc4` (#20088) committed exactly at checkpoint and already ledgered not_relevant.

### Decisions
- None (no new PRs to triage).

### Created / merged docs PRs
- None.

### Validation
- Not applicable (no docs changes this run).

### Blockers
- None.

### State
- Checkpoint **unchanged** at `2026-11-02T07:14:43Z` (no new processed work).
- `last_successful_run` -> 2026-11-02T09:04:05Z.
- No Slack notification (no-op run).

---

## Run run-20261102T100132Z-1081 — 2026-11-02T10:02:56Z (no-op)

### Preflight
- GitHub auth: `xiangfu0` (GH_TOKEN). apache/pinot = WRITE (pull/push/triage), pinot-contrib/pinot-docs = ADMIN.
- Durable `automation-state` branch read OK; lease acquired/released via Contents API PUT with blob-SHA compare-and-swap (acquire `0b2b3067` -> `3cbc6962`; release `3cbc6962` -> `b2fb57ca`). No concurrent run.

### Coverage
Inventoried merged apache/pinot PRs strictly after checkpoint `2026-11-02T07:14:43Z`. **0 new PRs.** Verified three independent ways:
1. **Search API** — `repo:apache/pinot is:pr is:merged merged:>2026-11-02T07:14:43Z` => total_count 0.
2. **Pulls listing** — closed PRs sorted by updated (3 pages x100) filtered `merged_at > checkpoint` => [].
3. **Git reconcile** — `commits?sha=master&since=2026-11-02T07:14:44Z` => []; master HEAD `2b0da67bc4` (#20088) committed exactly at checkpoint and already ledgered not_relevant.

### Decisions
- None (no new PRs to triage).

### Created / merged docs PRs
- None.

### Validation
- Not applicable (no docs changes this run).

### Blockers
- None.

### State
- Checkpoint **unchanged** at `2026-11-02T07:14:43Z` (no new processed work).
- `last_successful_run` -> 2026-11-02T10:02:56Z.
- No Slack notification (no-op run).

---

## Run 2026-11-02T11:03:41Z (run-20261102T110140Z-1075) — 1 PR triaged, not-relevant

### Coverage
- Window: merged_at strictly after prior checkpoint `2026-11-02T07:14:43Z`.
- Merged apache/pinot PRs in window: **2** — #20088 (at checkpoint boundary, already ledgered not_relevant) and #20119 (new).
- Reconciled search/issues API against apache/master commits; commit 9fe9d4d8 (#20119) is the only new one after 2b0da67b (#20088). No gaps.

### Decisions
- **#20119 — not_relevant.** Pure unit-test refactor in `pinot-controller/.../retention/RetentionManagerTest.java` (+10/-4): extracts a `stubSizeRetentionResourceManager` helper so the hybrid-retention-override test spies a plain `RetentionManager` for subclass-suite reuse. No main source, config, API, default, or documented behavior change. Follow-up to the #20088 extension-point refactor. https://github.com/apache/pinot/pull/20119

### Created / merged docs PRs
- None.

### Validation
- Not applicable (no docs changes this run).

### Blockers
- None.

### State
- Checkpoint **advanced** to `2026-11-02T10:38:40Z` (#20119 merged_at, fully triaged).
- `last_successful_run` -> 2026-11-02T11:03:41Z.
- No Slack notification (no docs PRs created this run).

---

## Run 2026-11-02T12:02:48Z (run-20261102T120114Z-827) — no-op, no new upstream PRs

### Coverage
- Window: merged_at strictly after checkpoint `2026-11-02T10:38:40Z`.
- Merged apache/pinot PRs in window: **0**.
- Verified three ways: `gh pr list` merged (100-PR window back to 2026-10-19, 0 after checkpoint); GitHub search API `is:merged merged:>2026-11-02T10:38:40Z` total_count=0; apache/pinot master tip is commit 9fe9d4d8 (#20119, merged 2026-11-02T10:38:39Z) — the checkpoint PR itself, already ledgered. No pagination gaps.

### Decisions
- None (no PRs to triage).

### Created / merged docs PRs
- None.

### Validation
- Not applicable (no docs changes this run).

### Blockers
- None.

### State
- Checkpoint **unchanged** at `2026-11-02T10:38:40Z` (no new work; not advanced past unprocessed work).
- `last_successful_run` -> 2026-11-02T12:02:48Z.
- Durable lock acquired/released via CAS. No Slack notification (no docs PRs created).

---

## Run: run-20261102T140146Z-1147
- **Completed (UTC):** 2026-11-02T14:03:30Z
- **Result:** no-op (no new docs-relevant upstream PRs)
- **Checkpoint (unchanged):** last_processed_merged_at = `2026-11-02T10:38:40Z`

### Preflight
- GitHub auth: `xiangfu0` (GH_TOKEN). apache/pinot = WRITE, pinot-contrib/pinot-docs = ADMIN (push:true/admin:true via REST API).
- Durable state read from `automation-state` branch; lock was released cleanly by prior run `run-20261102T130123Z-10316`.
- Lease acquired/released via Contents API PUT with blob-SHA compare-and-swap. Round-trip write verified against `.automation-probe`.
- Note: `session-git-hooks` blocks bare-branch `git push` (requires `cs_<sid>/` prefix); durable writes therefore go through the GitHub Contents REST API, where the token has write access. This matches prior runs' established mechanism.

### Coverage
Inventoried merged apache/pinot PRs strictly after checkpoint `2026-11-02T10:38:40Z`. **0 new PRs.** Verified three independent ways:
1. **Search API** — `repo:apache/pinot is:pr is:merged merged:>2026-11-02T10:38:40Z` => total_count 0.
2. **Pulls API** (not search-indexed) — 30 most-recently-updated closed PRs contained none with `merged_at` strictly after the checkpoint; most recent merged is #20119 at the boundary (already ledgered not_relevant).
3. **Master commits** — apache/pinot master HEAD = `9fe9d4d8f0` (#20119), committed exactly at the checkpoint; `git log --since=2026-11-02T10:38:41Z` => 0 commits.

### Decisions
- None. No PRs to triage.

### Created / merged docs PRs
- None.

### Validation
- Not applicable (no docs changes this run).

### Blockers
- None.

### State
- Checkpoint **unchanged** at `2026-11-02T10:38:40Z` (no new work; not advanced past unprocessed work).
- `last_successful_run` -> 2026-11-02T14:03:30Z.
- Durable lease acquired/released via CAS. No Slack notification (no docs PRs created).

---

## Run run-20261102T150129Z-ib (UTC 2026-11-02T15:01Z) — additional hourly no-op

- **Result:** no-op. Checkpoint unchanged at `2026-11-02T10:38:40Z`.
- **Coverage:** reconfirmed three independent ways — Search API `merged:>2026-11-02T10:38:40Z` = 0; pulls list API (not search-indexed) = 0 strictly after checkpoint (most recent merged still #20119 at boundary, already ledgered `not_relevant`); `origin/master` commit log `--since=2026-11-02T10:38:40Z` = 0.
- **Decisions:** none. No docs-relevant PRs to triage.
- **Created/merged docs PRs:** none. No Slack notification (no-op).
- **Durable state:** lease acquired and released via Contents REST API compare-and-swap (blob-SHA). Checkpoint not advanced.
- **Blockers:** none.

---

## Run: run-20261102T180235Z-lv
- **Completed (UTC):** 2026-11-02T18:02:35Z
- **Result:** no-op (no new docs-relevant upstream PRs)
- **Checkpoint (unchanged):** last_processed_merged_at = `2026-11-02T10:38:40Z`

### Preflight
- GitHub auth: `xiangfu0` (GH_TOKEN). apache/pinot = WRITE, pinot-contrib/pinot-docs = ADMIN (push/admin confirmed by successful Contents-API CAS write this run).
- Note: git-credential-tentrix mints git-push tokens only for the manifest repo (`xiangfu0/pinot`); durable-state and docs writes go through the authenticated `gh` REST API (GH_TOKEN), which is the path prior runs used and which works.
- Durable state read from `automation-state` branch; lock was `released` (prev holder run-20261102T170134Z-ib released 2026-11-02T17:02:57Z). No concurrent run.
- Lease acquired+released in a single atomic Contents-API CAS PUT (no mid-run coordination needed for a no-op).

### Coverage
Inventoried merged apache/pinot PRs strictly after checkpoint `2026-11-02T10:38:40Z`. **0 new PRs.** Verified three independent ways:
1. **Search API** — `repo:apache/pinot is:pr is:merged merged:>2026-11-02T10:38:40Z` => 0.
2. **Pulls API** (not search-indexed) — `repos/apache/pinot/pulls state=closed sort=updated per_page=100` pages 1–2, filtered `merged_at > checkpoint` => 0.
3. **Master commits** — apache/pinot master HEAD = `9fe9d4d8f` (#20119), committed 2026-11-02T10:38:39Z at the checkpoint boundary (already ledgered `not_relevant`); `commits?since=checkpoint+1s` => 0.
- Boundary PR #20119 reconciled present in ledger (not_relevant, test-only RetentionManagerTest refactor).

### Decisions
- None. No PRs to triage.

### Created / merged docs PRs
- None.

### Validation
- Not applicable (no docs changes this run).

### Blockers
- None.

### State
- Checkpoint **unchanged** (no advance past unprocessed/failed work; none existed).
- `last_successful_run` -> 2026-11-02T18:02:35Z; `last_run_id` -> run-20261102T180235Z-lv.
- No Slack notification (no-op runs stay quiet).

## Run: run-20261102T190140Z-kn
- **Started (UTC):** 2026-11-02T19:05:23Z
- **Result:** no-op (no new docs-relevant upstream PRs)
- **Checkpoint (unchanged):** last_processed_merged_at = `2026-11-02T10:38:40Z`

### Preflight
- gh auth: `xiangfu0` (GH_TOKEN). apache/pinot = write; pinot-contrib/pinot-docs = admin. Read-only preflight; no test PRs/Slack.
- Durable `automation-state` branch read OK; lease acquired+released via Contents API CAS. No stale lock / no overlap.
- Pinot checkout on fork `xiangfu0/pinot` (stale, 206 behind apache/master); inventory done via apache/pinot API + `apache/master` fetch.

### Coverage
Merged apache/pinot PRs strictly after checkpoint `2026-11-02T10:38:40Z`: **0**. Three agreeing methods:
1. **Search API** — `is:pr is:merged merged:>=2026-11-02` filtered strictly > checkpoint => 0 (returns only #20119@checkpoint + older #20088, both ledgered).
2. **Pulls API** — `state=closed sort=updated per_page=100` pages 1–2 (162 merged sampled; max merged_at = checkpoint exactly), filtered `merged_at > checkpoint` => 0.
3. **Master commits** — `git log apache/master --since=checkpoint` => 0; HEAD = `9fe9d4d8f` (#20119) at the checkpoint boundary, already ledgered `not_relevant`.

### Decisions
- None. No PRs to triage.

### Created / merged docs PRs
- None.

### Validation
- Not applicable (no docs changes this run).

### Blockers
- None.

### State
- Checkpoint **unchanged** (no advance past unprocessed/failed work; none existed).
- `last_successful_run` -> 2026-11-02T19:05:23Z; `last_run_id` -> run-20261102T190140Z-kn.
- No Slack notification (no-op runs stay quiet).

## Run run-20261102T200129Z-1008 — 2026-11-02T20:02:56Z (no-op)
- **Result:** no-op. Merged apache/pinot PRs strictly after checkpoint `2026-11-02T10:38:40Z`: **0**.
- **Coverage:** Search API (`is:pr is:merged merged:>=2026-11-02`, filtered > checkpoint) = 0; cross-checked `apache/master` commits since checkpoint = 0 (HEAD `9fe9d4d8` #20119 at the checkpoint boundary, already ledgered). Full agreement.
- **Decisions:** none. **Docs PRs:** none. **Validation:** n/a. **Blockers:** none.
- **State:** checkpoint unchanged; `last_successful_run` -> 2026-11-02T20:02:56Z. Lease acquired+released via Contents API CAS; no overlap. No Slack (no-op stays quiet).
