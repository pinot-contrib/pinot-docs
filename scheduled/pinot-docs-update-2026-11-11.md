# Pinot Docs Automation — 2026-11-11 (UTC)

## Run run-20261111T000219Z-opus48-cloud @ 2026-11-11T00:05:48Z

**Result:** no-op (no PRs merged after checkpoint; 0 docs PRs created).

### Coverage
- Incoming durable checkpoint: `last_processed_merged_at = 2026-11-10T21:05:33Z` (read from pinot-contrib/pinot-docs `automation-state` branch; most-recent completed pair #20168 → docs#1170). Durable state is well ahead of the migrated bootstrap boundary (2026-10-26T23:24:33Z), which was correctly not reset.
- Inventory of apache/pinot PRs merged **strictly after** the checkpoint, reconciled 2 ways (agree, no gaps):
  1. `search/issues repo:apache/pinot is:pr is:merged merged:>=2026-11-10` filtered strictly `> 2026-11-10T21:05:33Z` → **0 PRs**.
  2. `git log upstream/master --first-parent` → tip = `45feee7d` (#20216) merged at the checkpoint timestamp; no later merge commits. apache master tip == checkpoint PR.
- Highest processed PR in ledger = #20216, which equals the upstream master tip.

### Decisions
_No new upstream PRs merged after the checkpoint; nothing to triage._

### Outputs
- Docs PRs created: **0**
- Upstream comments: **0**
- Validation: not run (no docs changes produced).

### Durable state
- Checkpoint **unchanged** at `2026-11-10T21:05:33Z` (no new, processed, or failed work; did not advance).
- Ledger size: 111 (unchanged).
- Lease: acquired via CAS (lease commit `40f648a3`, blob `a3ba17a8`, exp 2026-11-11T00:52:27Z) and released at end via CAS (`106780f0`); strictly serialized, no overlap.

### Preflight (first execution of this remote routine instance)
- Environment: `/workspace/pinot` present (origin = fork `xiangfu0/pinot`; added `upstream` → apache/pinot). Cloned `pinot-contrib/pinot-docs` latest → `/workspace/pinot-docs`.
- GitHub auth: `GH_TOKEN` (ghu_, account `xiangfu0`) authenticated (core rate limit 15000). Permissions confirmed: apache/pinot = **WRITE**, pinot-contrib/pinot-docs = **ADMIN**.
- Durable store: read + CAS write to `automation-state` branch confirmed working via Contents API.
- Note on git push: the `git-credential-tentrix` helper mints credentials **only** for `xiangfu0/pinot` (none for apache/pinot or pinot-contrib/pinot-docs). All durable writes this run used the GitHub **Contents API** with `GH_TOKEN`, which works. Future docs-PR branch creation/commits should likewise go through the Contents/Git-Data API (or `gh`), not raw `git push`, unless push auth is independently verified.

### Blockers
- None. (Cosmetic `gh-tentrix-wrap: no GitHub token minted` wrapper stderr observed on apache/pinot & pinot-docs calls, but every API operation and CAS write succeeded.)

---

## Run run-20261111T010144Z-opus48-cloud — 2026-11-11T01:05Z

**Result: docs_created (1 docs PR merged).** First meaningful run of the day.

### Coverage
- Checkpoint at run start: `2026-11-10T21:05:33Z`.
- 3-way reconciliation of merged PRs strictly after checkpoint (all agree):
  - Search API `merged:>CP base:master`: #20218, #20183
  - `gh pr list --state merged --base master`: #20218, #20183
  - `git log upstream/master` since checkpoint: #20183, #20218 (plus #20216 at the boundary, already ledgered)

### Decisions
- **#20183** — *Evaluate user filters only on the rows that row-level security allows* → **docs-relevant**. User-facing: RLS responses zero the table-layout stats (`totalDocs`, segment-count / pruning counts); broker now fails with `QUERY_VALIDATION` when it cannot apply the RLS filter (was: ran without filter); single-stage skips the materialized-view rewrite under RLS; new `RLS_FILTER_TIME_MS` server timer / `rlsFilterTimeMs` log field. Facts verified against merged code (`ServerTimer.java`, `RlsResponseUtils.java`, `ServerQueryLogger.java`).
- **#20218** — *Fix port reuse in ServerTableSizeReaderTest* → **not_relevant** (single controller test file; flaky-test fix; no user-facing behavior/config/API/default change).

### Created / merged
- Docs PR: https://github.com/pinot-contrib/pinot-docs/pull/1171 — **MERGED** 2026-11-11T01:05:32Z (squash, commit `26149bcd`). Edited `operate-pinot/access-control.md` (+22/-1).
- Upstream comment: https://github.com/apache/pinot/pull/20183#issuecomment-6783864502

### Validation
- `git diff --check`: clean.
- `scripts/validate-docs.py --summary-only`: **PASS** (638 files, 3563 links). The 10 broken-anchor warnings are pre-existing in unrelated files (realtime.md, dedup.md, upsert.md, …); this change introduces none.
- PR checks all green: *Validate changed docs*, *Full docs audit*, GitBook ×2.

### Durable state
- Checkpoint **advanced** to `2026-11-11T00:12:20Z` (newest processed merged_at, #20183).
- Ledger size: 111 → 113.
- Lock/lease: acquired via CAS (blob `ea96532a`), released via CAS at end (final state blob `0968b6de`). Serialized, no overlap.
- Durable writes via Contents API CAS + `GH_TOKEN`. Docs branch pushed via `git push` after `gh auth setup-git` (works — supersedes the earlier note recommending Contents/Git-Data API only).

### Notification
- Slack summary sent (new docs PR created + merged).

### Blockers
- None.

---

## Run run-20261111T020144Z-opus48-cloud @ 2026-11-11T02:03:33Z

**Result:** no-op (no PRs merged after checkpoint; 0 docs PRs created).

### Coverage
- Incoming durable checkpoint: `last_processed_merged_at = 2026-11-11T00:12:20Z` (read from `automation-state` branch; most-recent completed pair #20183 → docs#1171).
- 3-way reconciliation of apache/pinot PRs merged **strictly after** the checkpoint (all agree, no gaps):
  1. `gh search prs --merged-at ">CP"` → **0 PRs**.
  2. `gh pr list --state merged --base master` (30 most recent): max `mergedAt = 2026-11-11T00:12:20Z` (#20183), which **equals** the checkpoint (already processed) → **0 after**.
  3. `git log upstream/master --first-parent --since=CP` → **0** new merge commits. Master tip `fd91422b` = #20183.

### Decisions
_No new upstream PRs merged after the checkpoint; nothing to triage._

### Outputs
- Docs PRs created: **0**; Upstream comments: **0**; Validation: not run (no docs changes).

### Durable state
- Checkpoint **unchanged** at `2026-11-11T00:12:20Z` (no new/processed/failed work; did not advance).
- Ledger size: 113 (unchanged).
- Lease/lock: acquired via CAS (state blob `8d894eed`), released via CAS at end. Serialized, no overlap.

### Blockers
- None. (Cosmetic `gh-tentrix-wrap: no GitHub token minted` wrapper stderr observed, but every authenticated API/CAS operation succeeded — rate limit 15000 confirms token applied.)

---


## Run run-20261111T030127Z-opus48-cloud — 2026-11-11T03:02:35Z
- **Result:** no-op
- **Checkpoint (unchanged):** last_processed_merged_at=2026-11-11T00:12:20Z
- **Coverage:** Inventoried merged apache/pinot PRs strictly after checkpoint via `gh pr list` (merged:>=2026-11-10 window) and reconciled against master commits (GitHub API, since boundary). 0 PRs and 0 commits found after checkpoint.
- **Decisions:** none (no new docs-relevant PRs).
- **Created/merged docs PRs:** none.
- **Validation:** n/a (no changes).
- **Blockers:** none.
- **Auth:** gh authenticated as xiangfu0; push=true on apache/pinot and pinot-contrib/pinot-docs; durable read/write to automation-state branch verified via CAS.


## Run run-20261111T040124Z-opus48-cloud — 2026-11-11T04:03:08Z
- **Result:** no-op
- **Checkpoint (unchanged):** last_processed_merged_at=2026-11-11T00:12:20Z
- **Coverage:** Inventoried merged apache/pinot PRs strictly after checkpoint. 3-way reconcile: (1) `gh search prs --merged-at ">2026-11-11T00:12:20Z"` = 0 results; (2) `gh pr list` most-recent merged = #20218 (00:07:49Z) and #20183 (00:12:20Z=checkpoint), both already in ledger; (3) apache/pinot master tip `fd91422b` = #20183 = checkpoint commit. All agree: nothing new.
- **Decisions:** none (no new docs-relevant PRs).
- **Created/merged docs PRs:** none.
- **Validation:** n/a (no changes).
- **Blockers:** none. (Local git remote `origin` points to the xiangfu0/pinot fork, tip #19809 — stale; authoritative inventory uses the apache/pinot API, not the fork's git log. Cosmetic `gh-tentrix-wrap` stderr observed; all authenticated API/CAS ops succeeded, rate limit 15000.)
- **Auth:** gh authenticated as xiangfu0; push=true on apache/pinot, admin on pinot-contrib/pinot-docs; durable read/write to automation-state branch verified via Contents API CAS. Ledger size 113.


## Run run-20261111T050122Z-opus48-cloud — 2026-11-11T05:08:43Z

**Result: docs_created (1 docs PR created + merged).**

### Coverage
- Checkpoint at run start: `2026-11-11T00:12:20Z`.
- 3-way reconciliation of apache/pinot PRs merged **strictly after** the checkpoint (all agree, no gaps):
  1. `search/issues ... is:merged merged:>CP` (paginated) → 6 PRs.
  2. `gh pr list --state merged` → same set.
  3. `git log upstream/master` since checkpoint → same PR refs (plus #20183/#20218 at/before boundary, already ledgered).
- New PRs: **#20108, #20201, #20211, #20203, #20202, #20210**.

### Decisions
- **#20202** — *Run multi-server quickstarts in separate JVMs* → **docs-relevant**. Forked quickstart servers now each run their own JVM; two new system properties set each forked server's heap via the parent JVM's `JAVA_OPTS`: `pinot.quickstart.server.xmx` (default `1g`) and `pinot.quickstart.server.xms` (defaults to resolved `xmx`). Names/defaults verified against merged `QuickstartServerProcess.java` (`MAX_HEAP_PROPERTY`, `INITIAL_HEAP_PROPERTY`, `DEFAULT_MAX_HEAP="1g"`).
- **#20108** — *Keep HISTOGRAM and SUM_ARRAY intermediate results as primitive arrays* → **not_relevant** (internal perf/memory optimization; serde stays compatible; no documented-behavior change).
- **#20201** — *Fix set-mode FUNNELCOUNT merge with an empty segment's step sets* → **not_relevant** (ClassCastException bugfix; restores correct behavior).
- **#20211** — *Fix EOS delivery race in MailboxServiceTest* → **not_relevant** (test-only).
- **#20203** — *Fix the serialized size of off-heap distinct count sets* → **not_relevant** (operator-precedence bugfix; wire-compatible; no documented change).
- **#20210** — *Fix subtask worker progress API failing on null worker key* → **not_relevant** (`GET /tasks/subtask/workers/progress` 500 bugfix; restores documented behavior, no new config/response shape).

### Created / merged
- Docs PR: https://github.com/pinot-contrib/pinot-docs/pull/1172 — **MERGED** 2026-11-11T05:07:03Z (squash, commit `8b5bbcd5`). Edited `basics/getting-started/quick-start.md` (+22/-0, new "Server heap for forked quickstarts" subsection).
- Upstream comment: https://github.com/apache/pinot/pull/20202#issuecomment-6787589264

### Validation
- `git diff --check`: clean.
- `scripts/validate-docs.py --summary-only`: **PASS** (638 files, 3563 links). The 10 broken-anchor warnings are pre-existing (identical on clean `latest`); this change introduces none.
- PR checks all green: *Validate changed docs*, *Full docs audit (informational)*.

### Durable state
- Checkpoint **advanced** to `2026-11-11T04:57:09Z` (newest processed merged_at, #20210; all 6 fully decided).
- Ledger size: 113 → 119.
- Lock/lease: acquired via CAS at run start, released via CAS at end. Serialized, no overlap.

### Notification
- Slack summary sent (new docs PR created + merged).

### Blockers
- None. (Cosmetic `gh-tentrix-wrap: no GitHub token minted` wrapper stderr observed; all authenticated API/CAS ops and the `git push` via `gh auth setup-git` succeeded.)

---

## Run run-20261111T060147Z-opus48-cloud (2026-11-11T06:03:14Z) — no-op

- **Coverage:** 3-way reconcile (search API `merged:>CP`, `gh pr list --state merged`, `git log upstream/master`) all agree: **0** merged PRs strictly after checkpoint `2026-11-11T04:57:09Z`.
- upstream/master HEAD = #20210, merged at the checkpoint boundary, already in ledger as *not_relevant*.
- **Decisions:** none (nothing new).
- **Created/merged:** none.
- **Validation:** not run (no doc changes).
- **Durable state:** checkpoint unchanged; ledger unchanged (119). Lock acquired + released via CAS; serialized, no overlap.
- **Notification:** none (no-op).
- **Blockers:** none. (Cosmetic `gh-tentrix-wrap` wrapper stderr observed; all authenticated API/CAS ops succeeded.)

---

## Run run-20261111T100213Z-opus48-cloud (2026-11-11T10:05Z) — docs_created

- **Coverage:** 3-way reconcile (search API `merged:>CP`, `gh pr list --state merged`, `git log apache/master`) all agree: **1** merged PR strictly after checkpoint `2026-11-11T04:57:09Z` → **#20221**. apache/master HEAD = #20221.
- **Decision:** #20221 "Revert 'Reject time-based flush threshold for pauseless tables (#20168)'" → **docs-relevant (revert of a previously-documented PR)**.
  - Verified from the merged revert diff: `TableConfigUtils.validateIngestionConfig` no longer rejects `realtime.segment.flush.threshold.time` (or legacy `.llc`) on pauseless tables; the corresponding tests were removed; both files match their pre-#20168 content. No release contained #20168 (1.6.0 predates it).
  - #20168 had been documented by our docs PR #1170 (merged into `latest` 2026-11-10). That content is now incorrect.
- **Created/merged:** [pinot-docs#1173](https://github.com/pinot-contrib/pinot-docs/pull/1173) — reverses #1170, restoring `operate-pinot/pauseless-consumption.md` to its pre-#20168 state (same-threshold wording, removed "Not supported" note, removed warning hint, removed #20168 reference link). Diff is the exact inverse of #1170 (+2/-11). Squash-merged **2026-11-11T10:05:36Z** (merge `6a3d1c29`). Upstream comment: apache/pinot#20221 issuecomment-6792949350.
- **Validation:** `git diff --check` clean; `scripts/validate-docs.py --summary-only` → **PASS** (638 files; the 10 broken anchors are pre-existing on clean `latest`, 0 new).
- **Durable state:** checkpoint advanced `2026-11-11T04:57:09Z` → `2026-11-11T09:24:21Z`; ledger 119 → 120 (added #20221; annotated #20168 `superseded_by_revert=20221`, `docs_reverted_by_pr=1173`). Lock/lease acquired + released via CAS (state sha `84d6ca2c` unchanged across run = no overlap).
- **Notification:** Slack summary sent (new docs PR created + merged).
- **Blockers:** none. (Cosmetic `gh-tentrix-wrap: no GitHub token minted` wrapper stderr observed; all authenticated API/CAS ops succeeded, and the docs branch pushed via a `GH_TOKEN` `x-access-token` remote URL since the plain clone has no credentials for pinot-docs.)

---

## Run run-20261111T110118Z-opus48-cloud — 2026-11-11T11:02:57Z

**Result:** no-op (no PRs merged strictly after checkpoint; 0 docs PRs created).

### Coverage
- Incoming durable checkpoint: `last_processed_merged_at = 2026-11-11T09:24:21Z` (read from pinot-contrib/pinot-docs `automation-state` branch; most-recent completed pair #20221 → docs#1173).
- Inventory of apache/pinot PRs merged **strictly after** the checkpoint, reconciled 3 ways (all agree, no gaps):
  1. `gh pr list --state merged` filtered `mergedAt > 2026-11-11T09:24:21Z` → **0 PRs**. Top merged = #20221 @ 2026-11-11T09:24:21Z (== checkpoint, already ledgered).
  2. Count of merged PRs strictly `> CP` → **0**.
  3. apache/pinot `master` tip via API = `16036c67` = "Revert ... (#20221)", committer date 2026-11-11T09:24:20Z == checkpoint commit.

### Decisions
_No new upstream PRs merged after the checkpoint; nothing to triage._

### Outputs
- Docs PRs created: **0**
- Upstream comments: **0**
- Validation: not run (no docs changes produced).

### Durable state
- Checkpoint **unchanged** at `2026-11-11T09:24:21Z` (no new/processed/failed work; did not advance).
- Ledger size: 120 (unchanged).
- Lock/lease: acquired via CAS (commit `6cb1530`) and released at end via CAS; strictly serialized, no overlap.

### Preflight
- GitHub auth: `GH_TOKEN` (account `xiangfu0`) authenticated. Permissions confirmed: apache/pinot = **WRITE**, pinot-contrib/pinot-docs = **ADMIN**.
- Durable store: read + CAS write to `automation-state` branch confirmed working via Contents API.

### Blockers
- None. (Cosmetic `gh-tentrix-wrap: no GitHub token minted` wrapper stderr observed, but every API operation and CAS write succeeded.)

### Run run-20261111T130238Z-opus48-cloud (2026-11-11T13:03:36Z) — no-op
- Merged PRs after checkpoint 2026-11-11T09:24:21Z: **0**.
- Reconcile: search API=0, gh pr list most-recent=#20221 (at CP, already done), upstream/master --since CP=0.
- Decisions: none. Docs PRs created/merged: 0. Checkpoint unchanged.

### Run run-20261111T140127Z-opus48-cloud (2026-11-11T14:02:47Z) — no-op
- Merged PRs after checkpoint 2026-11-11T09:24:21Z: **0**.
- Reconcile: pulls API (closed, sort=updated desc, pages 1-3) filtered `merged_at > CP` = 0; apache/pinot `upstream/master` HEAD = #20221 (== checkpoint commit).
- Decisions: none. Docs PRs created/merged: 0. Upstream comments: 0. Checkpoint unchanged. Ledger size 120.
- Lock: acquired via CAS (blob `5d50722` → `ddf3297`) and released via CAS at end. Serialized, no overlap.
