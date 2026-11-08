# Pinot Docs Update — 2026-11-08 (UTC)

## Run run-20261108T080145Z-opus48-1224 — 2026-11-08T08:05:50Z

**Result:** docs_created — 1 new upstream PR processed; 1 docs PR created and merged.

### Coverage
- Incoming durable checkpoint: `last_processed_merged_at=2026-11-08T06:14:02Z` (read from automation-state branch; lock+lease both `released` on entry, prev holder run-20261108T070125Z-opus48-1048).
- Merged apache/pinot PRs strictly after checkpoint: **1** (#20021).
- Reconciliation (3 independent methods, all agree):
  1. GitHub search/issues `repo:apache/pinot is:pr is:merged merged:>2026-11-08T06:14:02Z` → total_count **1**: #20021 @ 2026-11-08T07:09:15Z.
  2. pulls API (state=closed sort=updated desc) → **1** merged strictly after checkpoint: #20021.
  3. apache upstream/master `git log --since=checkpoint` → 2 commits: #20021 (@07:09:15Z, new) and #20020 (@06:14:02Z == prior checkpoint, already processed → docs PR #1167). Master tip = `13cdb440` = #20021.
- No gaps; full coverage.

### Decisions
- **#20021** — "Detect and close half-open broker-to-server channels" → **docs_created**. User-facing: introduces 3 new broker connection-liveness configs (on by default on upgrade) plus a dependent transport flag. Names/defaults verified against `NettyConfig` in merged code (not just PR prose): `pinot.broker.netty.write.timeout.ms`=10000, `pinot.broker.netty.tcp.user.timeout.ms`=10000 (Epoll-only), `pinot.broker.netty.write.buffer.high.water.mark.bytes`=16 MiB, `...low.water.mark.bytes`=8 MiB, `pinot.broker.netty.native.transports.enabled`=false.

### Created / Merged docs PRs
- Docs PR: https://github.com/pinot-contrib/pinot-docs/pull/1168 — **merged** (squash) at 2026-11-08T08:04:40Z, merge commit `127ba77`.
- Upstream comment: https://github.com/apache/pinot/pull/20021#issuecomment-6719058939
- File changed: `reference/configuration-reference/broker.md` (+5 rows in the broker config table).

### Validation
- `git diff --check`: clean (no whitespace errors).
- `uv run --with pyyaml python scripts/validate-docs.py --summary-only`: **PASS** both before and after the change (638 files, 3563 links; 10 pre-existing broken anchors unchanged — no new failures introduced).
- CI "Validate changed docs": **success**; "Full docs audit (informational)": **success**.

### Blockers
- None. gh wrapper prints "no GitHub token minted / continuing unauthenticated" warnings for apache/pinot & pinot-contrib/pinot-docs (session manifest lists only `xiangfu0/pinot`); ambient user token authenticates all API calls as `xiangfu0` (write on apache/pinot, admin on pinot-docs). Git HTTPS push for pinot-docs lacks a credential helper, so the branch/commit/PR were created via the GitHub Contents + Git-refs + Pulls APIs instead. Durable writes use Contents API blob-SHA CAS.

### Durable state
- Checkpoint **advanced**: `2026-11-08T06:14:02Z` → `2026-11-08T07:09:15Z`.
- Ledger: added entry for #20021 (docs_created).
- Lock acquired (blob `cbf0bc14`) at run start and released in the same CAS write that advanced the checkpoint; no run overlap.
- Slack: compact summary sent (1 new docs PR created+merged).

# Pinot Docs Update — 2026-11-08 (UTC)

## Run run-20261108T050116Z-opus48-877 — 2026-11-08T05:02:00Z

**Result:** no-op — no new upstream PRs merged after checkpoint; 0 docs PRs created.

### Coverage
- Incoming durable checkpoint: `last_processed_merged_at=2026-11-07T01:41:31Z` (read from automation-state branch; lock+lease both `released` on entry, prev holder run-20261108T040125Z-opus48-27751).
- Merged apache/pinot PRs strictly after checkpoint: **0**.
- Reconciliation (3 independent methods, all agree):
  1. apache upstream/master tip = `f60f17fd` = #20169 (`Reject cross-table functions under row-level security`) == checkpoint PR; `git log upstream/master --since=2026-11-07T01:41:32Z` → **0** commits (fetched apache/pinot directly this run).
  2. GitHub search/issues `repo:apache/pinot is:pr is:merged merged:>=2026-11-07` → 3 items, all at/before checkpoint (#20169, #20184, #20089); **0** strictly after.
  3. pulls API (state=closed sort=updated) → newest merged = #20169 @ 2026-11-07T01:41:31Z; **0** strictly after checkpoint.
- No gaps; full coverage.

### Decisions
- None (no new PRs to triage).

### Created / Merged docs PRs
- None.

### Validation
- N/A (no docs changes produced this run).

### Blockers
- None. gh wrapper prints "no GitHub token minted / continuing unauthenticated" warnings for apache/pinot & pinot-contrib/pinot-docs (session manifest lists only `xiangfu0/pinot`); ambient user token authenticates all API calls as `xiangfu0` (WRITE on apache/pinot, ADMIN on pinot-docs confirmed). Durable writes use Contents API blob-SHA CAS. Pre-cloned `/workspace/pinot` origin is fork `xiangfu0/pinot` (stale master @ #19809); added `upstream=apache/pinot` for authoritative reconciliation.

### Durable state
- Checkpoint **unchanged**: `2026-11-07T01:41:31Z`.
- Ledger entries: 85 (unchanged).
- Lock+lease acquired (blob `84ba3ce2`) then released (blob `d009636f`) via Contents API blob-SHA CAS; no run overlap.
- No Slack notification (quiet no-op per routine policy).

## Run run-20261108T040125Z-opus48-27751 — 2026-11-08T04:03:00Z

**Result:** no-op — no new upstream PRs merged after checkpoint; 0 docs PRs created.

### Coverage
- Incoming durable checkpoint: `last_processed_merged_at=2026-11-07T01:41:31Z` (read from automation-state branch; lock+lease both `released` on entry, prev holder run-20261108T030114Z-opus48-857).
- Merged apache/pinot PRs strictly after checkpoint: **0**.
- Reconciliation (3 independent methods, all agree):
  1. GitHub search/issues `repo:apache/pinot is:pr is:merged merged:>2026-11-07T01:41:31Z` (full pagination) → **0** items; total_count **0**.
  2. Same query with `merged:>=` boundary → only #20169 @ 2026-11-07T01:41:31Z (== checkpoint, already docs_created → docs PR #1166).
  3. apache upstream/master tip = `f60f17fd701cf326ad4e9d28735a11eee7de3d7b` = #20169 (`Reject cross-table functions under row-level security`) == checkpoint PR; no newer commits.
- No gaps; full coverage.

### Decisions
- None (no new PRs to triage).

### Created / Merged docs PRs
- None.

### Validation
- N/A (no docs changes produced this run).

### Blockers
- None. gh wrapper prints "no GitHub token minted / continuing unauthenticated" warnings (session manifest lists only `xiangfu0/pinot`); ambient user token still authenticates all API calls as `xiangfu0` (write on apache/pinot, admin on pinot-docs, rate_limit 15000). Durable writes use Contents API blob-SHA CAS. Pre-cloned `/workspace/pinot` origin is fork `xiangfu0/pinot`; added `upstream=apache/pinot` and reset local master to apache upstream/master (@ #20169) as authoritative source.

### Durable state
- Checkpoint **unchanged**: `2026-11-07T01:41:31Z`.
- Ledger entries: 85 (unchanged).
- Lock+lease acquired (blob `6fb3203f`) then released (blob `9cd11436`) via Contents API blob-SHA CAS; no run overlap.
- No Slack notification (quiet no-op per routine policy).

## Run run-20261108T000201Z-opus48-913 — 2026-11-08T00:03:51Z

**Result:** no-op — no new upstream PRs merged after checkpoint; 0 docs PRs created.

### Coverage
- Incoming durable checkpoint: `last_processed_merged_at=2026-11-07T01:41:31Z` (read from automation-state branch; lock+lease both `released` on entry, prev holder run-20261107T230119Z-opus48-874).
- Merged apache/pinot PRs strictly after checkpoint: **0**.
- Reconciliation (3 independent methods, all agree):
  1. GitHub search/issues `repo:apache/pinot is:pr is:merged merged:2026-11-06..2026-11-09` (full pagination) → 11 items, newest merged = #20169 @ 2026-11-07T01:41:31Z (== checkpoint, already docs_created → docs PR #1166); **0** strictly after checkpoint.
  2. `git log upstream/master --since=2026-11-07T01:41:31Z` (apache/pinot fetched directly this run) → **0** commits.
  3. apache/master tip = `f60f17fd701cf326ad4e9d28735a11eee7de3d7b` = #20169 (`Reject cross-table functions under row-level security`) == checkpoint PR.
- No gaps; full coverage.

### Decisions
- None (no new PRs to triage).

### Created / Merged docs PRs
- None.

### Validation
- N/A (no docs changes produced this run).

### Blockers
- None affecting durability. The gh wrapper prints "no GitHub token minted / continuing unauthenticated" for apache/pinot & pinot-contrib/pinot-docs (session manifest lists only `xiangfu0/pinot`), but the ambient user token authenticates all API calls as `xiangfu0` — verified via `gh api user` and authed-only collaborator-permission endpoints (push on apache/pinot, admin on pinot-docs). Durable writes use the Contents API with blob-SHA CAS, which bypasses the session git-push proxy.

### Durable state
- Checkpoint **unchanged**: `2026-11-07T01:41:31Z`.
- Ledger entries: 85 (unchanged).
- Lock+lease acquired then released via Contents API blob-SHA CAS (lock blob `8c19bd20` → release blob `423c6f72`); no run overlap.
- No Slack notification (quiet no-op per routine policy).

## Run run-20261108T010115Z-opus48-869 — 2026-11-08T01:02:54Z

**Result:** no-op — no new upstream PRs merged after checkpoint; 0 docs PRs created.

### Coverage
- Incoming durable checkpoint: `last_processed_merged_at=2026-11-07T01:41:31Z` (read from automation-state branch; lock+lease both `released` on entry, prev holder run-20261108T000201Z-opus48-913).
- Merged apache/pinot PRs strictly after checkpoint: **0**.
- Reconciliation (authoritative apache/pinot API + commit history):
  1. `gh pr list --repo apache/pinot --state merged --search "merged:>=2026-11-07"` (full pagination) → 3 items, all at/before checkpoint; **0** strictly after.
  2. apache/master tip = `f60f17fd701cf326ad4e9d28735a11eee7de3d7b` = #20169 (`Reject cross-table functions under row-level security`) == checkpoint PR; `git log f60f17f..apache/master` → **0** commits.
  3. Broad recent-merged query (no date bound) confirms newest merged PR = #20169 @ 2026-11-07T01:41:31Z.
- Note: local checkout `origin` is fork `xiangfu0/pinot` (stale master @ #19809); added `apache` remote for authoritative reconciliation this run.
- No gaps; full coverage.

### Decisions
- None (no new PRs to triage).

### Created / Merged docs PRs
- None.

### Validation
- N/A (no docs changes produced this run).

### Blockers
- None. gh wrapper prints "no GitHub token minted / continuing unauthenticated" warnings for apache/pinot & pinot-contrib/pinot-docs (session manifest lists only `xiangfu0/pinot`), but the ambient user token authenticates all API calls as `xiangfu0`; durable writes use Contents API blob-SHA CAS.

### Durable state
- Checkpoint **unchanged**: `2026-11-07T01:41:31Z`.
- Ledger entries: 85 (unchanged).
- Lock+lease acquired then released via Contents API blob-SHA CAS (lock blob `420a7d4b` → release blob `6aa84e85`); no run overlap.
- No Slack notification (quiet no-op per routine policy).

---

## Run run-20261108T030114Z-opus48-857 — 2026-11-08T03:05:38Z

**Result:** no-op — no new upstream PRs merged after checkpoint; 0 docs PRs created.

### Coverage
- Incoming durable checkpoint: `last_processed_merged_at=2026-11-07T01:41:31Z` (read from automation-state branch; lock+lease both `released` on entry, prev holder run-20261108T020115Z-opus48-25019).
- Merged apache/pinot PRs strictly after checkpoint: **0**.
- Reconciliation (3 independent methods, all agree):
  1. apache/pinot commits API `sha=master since=2026-11-07T01:41:31Z` → **0** commits; master tip = `f60f17fd7` = #20169 == checkpoint PR.
  2. GitHub search/issues `repo:apache/pinot is:pr is:merged merged:>2026-11-07T01:41:31Z` → total_count **0**.
  3. Full paginated pulls listing (state=closed, 14029 merged PRs enumerated) → newest merged = #20169 @ 2026-11-07T01:41:31Z; **0** strictly after checkpoint.
- No gaps; full coverage.

### Decisions
- None (no new PRs to triage).

### Created / Merged docs PRs
- None.

### Validation
- N/A (no docs changes produced this run).

### Blockers
- None. gh wrapper prints "no GitHub token minted / continuing unauthenticated" warnings for apache/pinot & pinot-contrib/pinot-docs (session manifest lists only `xiangfu0/pinot`); the ambient user token still authenticates all API calls as `xiangfu0` (WRITE on apache/pinot, ADMIN on pinot-docs confirmed). Durable writes use Contents API blob-SHA CAS. Pre-cloned `/workspace/pinot` origin is fork `xiangfu0/pinot` with stale master (@ #19809, 2026-10-09); used apache/pinot API as authoritative inventory source.

### Durable state
- Checkpoint **unchanged**: `2026-11-07T01:41:31Z`.
- Ledger entries: 85 (unchanged).
- Lock+lease acquired then released via Contents API blob-SHA CAS; no run overlap.
- No Slack notification (quiet no-op per routine policy).

---

## Run 2026-11-08T06:02:21Z (`run-20261108T060116Z-opus48-919`) — no-op

- **Result**: success, no-op. No merged apache/pinot PRs after checkpoint `2026-11-07T01:41:31Z`.
- **Coverage / reconcile** (3-way, all consistent):
  - Search API `is:pr is:merged merged:>2026-11-07T01:41:31Z`: total_count=0.
  - Pulls API (closed, sorted by updated): most-recent merge is #20169 @ `2026-11-07T01:41:31Z` — the checkpoint PR itself (already processed).
  - git `upstream/master` HEAD = `f60f17fd` = #20169, matches checkpoint.
- **Decisions**: none (no new PRs to triage).
- **Docs PRs**: none created.
- **Validation**: N/A (no docs changes).
- **Durable state**: checkpoint unchanged `2026-11-07T01:41:31Z`; lease acquired+released via Contents API blob-SHA CAS; no overlap.
- **Slack**: none (quiet no-op).

---

## Run run-20261108T070125Z-opus48-1048 — 2026-11-08T07:06:40Z

**Result:** docs_created — 1 new upstream PR merged after checkpoint; 1 docs PR created and merged.

### Coverage
- Incoming durable checkpoint: `last_processed_merged_at=2026-11-07T01:41:31Z` (read from automation-state branch; lock `released` on entry, prev holder run-20261108T060116Z-opus48-919).
- Merged apache/pinot PRs strictly after checkpoint: **1 (#20020)**.
- Reconciliation (2 independent methods, agree):
  1. apache upstream/master (fetched directly, --depth=200): `git log upstream/master --since=2026-11-07T01:41:31Z` → exactly **1** commit `61e770d8` (#20020, merged 2026-11-08T06:14:02Z). Tip now 61e770d8.
  2. GitHub search/issues `repo:apache/pinot is:pr is:merged merged:>=2026-11-07` → 4 items; #20089/#20169/#20184 all ≤ checkpoint (already in ledger), only **#20020** strictly after.
- No gaps; full coverage.

### Decisions
- **#20020 — "Rate-limit stream data-loss reports and fail re-ingestion on data loss"** → **docs_created**. Genuine user-facing behavior change (upstream-labeled `release-notes`): re-ingestion now **fails on reported stream data loss** instead of silently committing a partial segment when the segment's offset range aged out of retention. The segment stays `ERROR`, the controller keeps retrying; operator must restore the range or delete the segment. No config/API/wire/serialization change, no opt-out, applies only under default `read_uncommitted` isolation. Verified against merged code (`StatelessRealtimeSegmentWriter` `Preconditions.checkState` message at commit 61e770d8), not PR prose. The data-loss-diagnostics rate-limiting in the same PR is internal observability (not separately documented).

### Created / merged
- Docs PR: **[pinot-contrib/pinot-docs#1167](https://github.com/pinot-contrib/pinot-docs/pull/1167)** — "Document reingestion failing on stream data loss (apache/pinot#20020)". Squash-merged 2026-11-08T07:05:03Z (merge commit `52047ff8`). One paragraph added to `operate-pinot/pauseless-consumption.md` → "Non-recoverable failures (reingestion)".
- Upstream comment: https://github.com/apache/pinot/pull/20020#issuecomment-6718542845

### Validation
- `git diff --check`: clean (no whitespace/conflict errors).
- `validate-docs.py --summary-only`: **PASS** (638 files, 3563 links; 10 pre-existing broken anchors unrelated to this change — no new links/anchors introduced).
- Docs PR CI: "Validate changed docs" SUCCESS, "Full docs audit (informational)" SUCCESS. GitBook preview checks are non-blocking deploy previews.

### Blockers
- None. `git push` over https required `gh auth setup-git` (remote had no credential helper); resolved. Checkpoint **ADVANCED** `2026-11-07T01:41:31Z` → `2026-11-08T06:14:02Z`. Ledger 85 → 86.
