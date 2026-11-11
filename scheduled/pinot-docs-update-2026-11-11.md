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
