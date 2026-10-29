# Pinot Docs Automation — Scheduled Report 2026-10-29 (UTC)

## Run 2026-10-29T00:03:28Z (run id `run-20261029T000117Z-923`)

### Summary
Triage run. **2** new merged `apache/pinot` PRs strictly after the prior checkpoint
`2026-10-28T21:49:28Z` were inventoried and both classified **not docs-relevant**. No docs PR
created, no upstream comment, no Slack notification.

### Preflight
- GitHub auth: `xiangfu0` (ambient App token). `apache/pinot` = WRITE, `pinot-contrib/pinot-docs` = ADMIN.
- Durable `automation-state` branch read OK (checkpoint `2026-10-28T21:49:28Z`).
- Lease acquired via create-only CAS PUT of `automation-lock.json` (HTTP 201); no concurrent holder.
- Working trees clean; `upstream` = apache/pinot fetched and reconciled.

### Coverage (checkpoint `2026-10-28T21:49:28Z`)
Three independent cross-checks agree — complete coverage, no gaps:
1. `gh search prs merged:>CP` → {#20035, #20069}
2. `gh search prs merged:>=CP` → {#20009 (exact boundary, already processed), #20035, #20069}
3. `git log --first-parent apache/master` after checkpoint commit `ee7f50ac` → exactly 2 merge commits
   (`fcd05cc` #20035, `52d9c80` #20069)

### Decisions
| PR | Title | Merged (UTC) | Decision | Rationale |
|---|---|---|---|---|
| [#20069](https://github.com/apache/pinot/pull/20069) | Add scoped buffer reads for compressed forward indexes | 2026-10-28T23:54:13Z | not_relevant | Internal memory-access refactor. Adds `PinotDataBuffer.readWithByteBuffer(...)` for synchronous scoped buffer consumption in compressed forward-index readers (V4/V5/V6). Default delegates to the existing view API; identical read results. No config/option/function/default change; low-level internal SPI only. |
| [#20035](https://github.com/apache/pinot/pull/20035) | Fix compiled aggregation inputs after timestamp index rewrites | 2026-10-28T23:58:25Z | not_relevant | Internal planner correctness fix so a configured/built DAY timestamp index is actually applied to aggregation inputs like `DISTINCTCOUNT(DATETRUNC('DAY',...))` (previously projected the raw timestamp). Rewrites once at instance-plan entry; removes per-segment rewrites. Per PR body, the index must already be configured and built and **SQL is unchanged**. Verified no new config/query-option/default in the pinot-core main diff. No user-facing docs surface. |

### Outcome
- Docs PRs created: **0**
- Docs PRs merged: **0**
- Upstream comments: **0** (neither PR docs-relevant)
- Slack: not sent (no new docs PRs)
- Validation: not applicable (no docs changes produced)

### Durable state
- Checkpoint ADVANCED `2026-10-28T21:49:28Z` → `2026-10-28T23:58:25Z` (max merged-at of the two fully-triaged PRs).
- `last_successful_run` → `2026-10-29T00:03:28Z`; `last_run_id` → `run-20261029T000117Z-923`.
- #20069 and #20035 recorded as not_relevant in the processed-PR ledger.
- Lease released at end of run.

### Blockers
None.
