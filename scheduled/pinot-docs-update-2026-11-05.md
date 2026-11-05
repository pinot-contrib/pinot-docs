# Pinot Docs Update — 2026-11-05 (UTC)

_This daily report accumulates all runs for 2026-11-05 (UTC), newest first._

---

## Run run-20261105T130130Z-opus48-1025 — 2026-11-05T13:06:07Z (1 docs PR created + merged)

**Checkpoint:** incoming `2026-11-05T06:42:06Z` → outgoing `2026-11-05T12:22:05Z` (= apache/pinot#19450 merged_at).

### Coverage / reconciliation
Merged apache/pinot PRs strictly after incoming checkpoint: **1** (#19450). Verified by two agreeing methods:
1. Search API `is:pr is:merged merged:>=2026-11-05` → 5 items; precise `merged_at` filter leaves only #19450 (@ `2026-11-05T12:22:05Z`) strictly after checkpoint (#20153 is exactly at checkpoint; #20164/#20156/#20154 before, all ledgered).
2. apache/pinot `upstream/master` commit log since #20153's merge commit (`14b564428`) → exactly one commit `684b7a4a` = #19450. No gaps.

### Decisions
| PR | Title | Decision | Docs |
|----|-------|----------|------|
| apache/pinot#19450 | Add metric for local realtime segment builds with CRC mismatch | **docs_created** | pinot-contrib/pinot-docs#1163 (merged) |

#### #19450 rationale
Adds a new `ServerMeter`: `SEGMENT_BUILD_WITH_CRC_MISMATCH` (unit "segments", per-table). Verified from merged code (`684b7a4a`):
- `ServerMeter.java`: `SEGMENT_BUILD_WITH_CRC_MISMATCH("segments", false)`.
- Emitted in `RealtimeSegmentDataManager.buildSegmentAndReplace(...)` when a locally built realtime segment's CRC does not match the committed CRC in ZK; the server then discards the local build and the caller downloads the committed copy. Counted regardless of whether that download fallback succeeds; build failures and CRC-read errors are NOT counted (confirmed via Javadoc + emission site).

Operator-facing observability metric → docs-relevant. The project's `operate-pinot/metrics-and-monitoring.md` maintains a curated Critical Server Metrics table + diagnosis patterns, where this meter belongs.

### Docs PR #1163
Branch `cs_LqNuFJRzIs/docs/pr-19450-segment-build-crc-mismatch-metric`. File `operate-pinot/metrics-and-monitoring.md` (+6 lines):
- New row in **Critical Server Metrics** table (description + alert threshold `> 0`).
- New **Server Diagnosis Patterns** entry (expected vs. concerning behavior; correlate with `SEGMENT_DOWNLOAD_FAILURES`).

### Validation
- `git diff --check`: clean.
- `uv run --with pyyaml python scripts/validate-docs.py --summary-only`: **PASS** (10 broken anchors confirmed pre-existing on `origin/latest` baseline, unrelated to changed file).
- CI checks: "Validate changed docs" pass, "Full docs audit" pass, GitBook ×2 pass.
- Squash-merged sha `da7ac865` at 2026-11-05T13:04:48Z; merge verified via API (`merged=true`).

### Links
- Upstream PR: https://github.com/apache/pinot/pull/19450
- Docs PR (merged): https://github.com/pinot-contrib/pinot-docs/pull/1163
- Upstream comment: https://github.com/apache/pinot/pull/19450#issuecomment-6658722890

### Environment / durable state
Preflight: apache/pinot = WRITE, pinot-contrib/pinot-docs = ADMIN. Durable read + write to `automation-state` via GitHub Contents API with SHA-based CAS. Lock/lease acquired (blob `67bc7ff`) and released cleanly (blob `6b9b776`). Checkpoint advanced; ledger 68 → 69.

### Blockers
None.

### Notifications
Slack summary sent (new docs PR created + merged).

---

## Run run-20261105T120134Z-opus48-1130 — 2026-11-05T12:03Z (no-op)

**Checkpoint (unchanged):** `last_processed_merged_at = 2026-11-05T06:42:06Z`

### Coverage / reconciliation (triple-verified)
1. Search API `is:pr is:merged merged:>=2026-11-05T06:42:06Z` → 1 item (#20153, merged_at == checkpoint, already processed); **0** strictly after.
2. Pulls API (state=closed, sort=updated desc) → newest merged is #20153 at `2026-11-05T06:42:06Z` (== checkpoint); nothing strictly after.
3. apache/pinot `master` HEAD = `14b56442` = #20153 (merge_commit_sha `14b564428ee6d939728e3111ffb2f13c957afa18`, merged_at == checkpoint). `git log --since=2026-11-05T06:42:06Z` on upstream/master → empty. Reconciled 8 most-recent merged PRs — all present in the 68-entry ledger.

### Decisions
None — no new PRs to triage.

### Docs PRs created / merged
None.

### Validation
No docs changes; no docs-repo validation required.

### Environment / durable state
Read-only preflight: apache/pinot = WRITE, pinot-contrib/pinot-docs = ADMIN. Durable read + write to `automation-state` via **GitHub Contents/Git-Data API** with SHA-based CAS (session git-push hook rejects bare-name pushes to `automation-state`). Lease acquired (commit `25d7dba`) and released cleanly. Checkpoint unchanged.

### Blockers
None.

### Notifications
No Slack (no-op run; no new docs PR).

---

## Run run-20261105T110116Z-opus48-910 — 2026-11-05T11:03Z (no-op)

**Checkpoint (unchanged):** `last_processed_merged_at = 2026-11-05T06:42:06Z`

### Coverage / reconciliation (triple-verified)
1. Search API `is:pr is:merged merged:>2026-11-05T06:42:06Z` → total_count = **0**.
2. Pulls API (state=closed, sort=updated desc, per_page=40) → newest merged is #20153 at `2026-11-05T06:42:06Z` (== checkpoint, already processed); nothing strictly after.
3. apache/pinot `master` HEAD = `14b564428` = #20153 (merged_at == checkpoint). Reconciled 9 most-recent merged PRs (#20164, #20153, #20154, #20156, #20155, #20152, #20150, #19120, #19907) — all present in ledger.

### Decisions
None — no new PRs to triage.

### Docs PRs created / merged
None.

### Validation
No docs changes; no docs-repo validation required.

### Environment / durable state
Read-only preflight: apache/pinot = WRITE, pinot-contrib/pinot-docs = ADMIN. Durable read + write to `automation-state` via **GitHub Contents API** with SHA-based CAS. Lease acquired (content SHA `3afaa58`) and released cleanly (content SHA `f33f3b4`). Checkpoint unchanged.

### Blockers
None.

### Notifications
No Slack (no-op run; no new docs PR).

---

# Pinot Docs Update — 2026-11-05 (run run-20261105T070117Z-opus48-931)

**Run start:** 2026-11-05T07:01:17Z · **Finished:** 2026-11-05T07:03:26Z · **Model:** Opus 4.8 (claude-opus-4-8) · **Result:** No-op for docs (2 PRs triaged, both not docs-relevant)

## Checkpoint
- Incoming `last_processed_merged_at`: `2026-11-05T00:47:33Z`
- Outgoing `last_processed_merged_at`: `2026-11-05T06:42:06Z` (advanced — 2 PRs fully triaged)

## Coverage (merged apache/pinot PRs strictly after checkpoint)
Three agreeing methods: (1) `search/issues is:pr is:merged merged:>=2026-11-05T00:47:33Z` => 3 items, of which #20154 == checkpoint PR (already ledgered, docs #1162); (2) `gh pr list --state merged` sorted by mergedAt; (3) apache/master commit-log reconcile since checkpoint => exactly (#20153, #20154, #20164). New PRs strictly after checkpoint: **#20153, #20164**. No gaps.

## Decisions
- **#20153** — "Make Utf8Utils.encodedLength agree with encode() on unpaired surrogates" — **not docs-relevant**. Internal correctness/perf fix making `Utf8Utils.encodedLength` exactly equal `encode(s).length` (Guava's `Utf8.encodedLength` threw on unpaired surrogates reachable via e.g. `SUBSTR` splitting an emoji; buffer-sizing code could throw where the encoder succeeds). Collapses two helpers into one branch-free counter, moves 15 production classes off direct Guava calls, adds a long-view `isAscii` fast path. Verified diff adds no QueryOptionKey/CONFIG_/`pinot.*` keys or registered functions; no documented user-facing surface.
- **#20164** — "Add a README Docker quickstart and improve GitHub metadata" — **not relevant to pinot-docs**. Changes only apache/pinot's own `README.md` and `.asf.yaml` (repo landing page + ASF repo metadata/topics), not the pinot-docs (docs.pinot.apache.org / GitBook) site. No runtime code, config, API, function, or documented-default changes.

## Outputs
- Docs PRs created: **0**. Upstream comments: **0**. Slack: **not sent** (no new docs PRs).
- Ledger: 66 -> **68** entries. `last_successful_run` -> 2026-11-05T07:03:26Z.
- Durable state/report/memory persisted to `automation-state` branch via atomic Git Trees commit; lease released.

---

# Pinot Docs Update — 2026-11-05 (run run-20261105T060154Z-opus48-1252)

**Run start:** 2026-11-05T06:01:54Z · **Finished:** 2026-11-05T06:02:22Z · **Model:** Opus 4.8 (claude-opus-4-8) · **Result:** No-op (no new PRs)

## Checkpoint
- Incoming `last_processed_merged_at`: `2026-11-05T00:47:33Z`
- Outgoing `last_processed_merged_at`: `2026-11-05T00:47:33Z` (unchanged — nothing new)

## Coverage (merged apache/pinot PRs strictly after checkpoint)
Triple-verified, all agreeing on **0** merged PRs after `2026-11-05T00:47:33Z`:
1. search API (`is:pr is:merged merged:>2026-11-05T00:47:33Z`) → total_count = 0.
2. pulls API (`state=closed sort=updated desc per_page=50`) → max merged_at = #20154 @ checkpoint; nothing strictly after.
3. apache/pinot master HEAD via Commits API → `091eac795` = #20154 (merged_at == checkpoint, already processed → docs PR #1162).

Note: local checkout `origin` points to the fork `xiangfu0/pinot` (stale); GitHub API on apache/pinot used as authoritative source.

## Decisions
None — no new PRs to triage.

## Docs PRs created / merged
None.

## Validation
No docs changes; no docs-repo validation required.

## Blockers
None. Durable state read OK; lease/lock acquired via Contents API CAS (acquire commit `5c748587`, release commit `ebcb50ad`, each conditioned on the prior blob SHA). Write access to pinot-contrib/pinot-docs confirmed via the lease CAS write. Access: apache/pinot=WRITE, pinot-contrib/pinot-docs=ADMIN.

## Notifications
No Slack (no-op run; no new docs PR).

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

---

## Run run-20261105T040134Z-opus48-1084 — 2026-11-05T04:03:27Z (no-op)

### Coverage
Merged apache/pinot PRs strictly after checkpoint `2026-11-05T00:47:33Z`: **0**. Verified via three agreeing methods (search/issues merged-date filter = total_count=0; apache/master `git log --since` = empty, HEAD #20154; pulls API sort=updated desc = 0 strictly after). Full coverage, no gaps.

### Decisions
None (no new PRs to triage).

### Docs PRs created / merged
None.

### Validation
No docs changes; no docs-repo validation required.

### Blockers
None. Lease acquired and released cleanly via Contents/Trees API CAS. Checkpoint unchanged at `2026-11-05T00:47:33Z`.

### Notifications
No Slack (no-op run; no new docs PR).


---

## Run run-20261105T050117Z-opus48-28506 — 2026-11-05T05:02:58Z (no-op)

### Coverage
Inventoried apache/pinot merged PRs strictly after checkpoint `2026-11-05T00:47:33Z`. Triple-verified, all agreeing on **0 new PRs**:
1. Search API `is:pr is:merged merged:>2026-11-05T00:47:33Z` → total_count = 0.
2. Pulls API (state=closed, sort=updated desc) → no PR with merged_at strictly after checkpoint.
3. apache/pinot master HEAD via Commits API → `091eac795` = #20154 (merged_at == checkpoint, already processed → docs PR #1162).

Note: local checkout `origin` points to the fork `xiangfu0/pinot` (stale); GitHub API on apache/pinot used as authoritative source.

### Decisions
None — no new PRs to triage.

### Docs PRs created / merged
None.

### Validation
No docs changes; no docs-repo validation required.

### Blockers
None. Lease acquired (CAS commit `149871f1`) and released cleanly. Checkpoint unchanged at `2026-11-05T00:47:33Z`.

### Notifications
No Slack (no-op run; no new docs PR).

---

## Run run-20261105T090137Z-opus48-1239 — 2026-11-05T09:03Z (no-op)

**Checkpoint (unchanged):** `last_processed_merged_at = 2026-11-05T06:42:06Z`

### Coverage / reconciliation (triple-verified)
1. Search API `is:pr is:merged merged:>2026-11-05T06:42:06Z` → total_count = **0**.
2. Pulls API (state=closed, sort=updated desc, per_page=50) → newest merged is #20153 at `2026-11-05T06:42:06Z` (== checkpoint, already processed); nothing strictly after.
3. apache/pinot `master` HEAD = `14b56442` = #20153 (merged_at == checkpoint). Reconciled 8 most-recent merged PRs (#20153, #20164, #20154, #20156, #20155, #20152, #20150, #19120) — all present in ledger.

### Decisions
None — no new PRs to triage.

### Docs PRs created / merged
None.

### Validation
No docs changes; no docs-repo validation required.

### Environment / durable state
Read-only preflight: apache/pinot = WRITE, pinot-contrib/pinot-docs = ADMIN. Durable read + write to `automation-state` confirmed via **GitHub Git Data API** with CAS (the session git-push hook rejects bare-name pushes to `automation-state`, requiring a `cs_<sid>/` prefix; prior runs persist through the same API path). Lease acquired (commit `7d9981b`) and released cleanly.

### Blockers
None.

### Notifications
No Slack (no-op run; no new docs PR).
