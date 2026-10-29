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

---

## Run 2026-10-29T01:03:27Z (run id `run-20261029T010113Z-18526`)

### Summary
Triage run. **2** new merged `apache/pinot` PRs strictly after the prior checkpoint
`2026-10-28T23:58:25Z` were inventoried and both classified **not docs-relevant**. No docs PR
created, no upstream comment, no Slack notification.

### Preflight
- GitHub auth: `xiangfu0` (ambient App token). `apache/pinot` = WRITE, `pinot-contrib/pinot-docs` = ADMIN (verified via `gh repo view --json viewerPermission`).
- Durable `automation-state` branch read OK (checkpoint `2026-10-28T23:58:25Z`, prior run id `run-20261029T000117Z-923`).
- Lease acquired via create-only CAS PUT of `automation-lock.json`; no concurrent holder.
- `/workspace/pinot` working tree clean; `upstream` = apache/pinot fetched (HEAD `c0319056`).

### Coverage (checkpoint `2026-10-28T23:58:25Z`)
Three independent cross-checks agree — complete coverage, no gaps:
1. `search merged:>CP` → {#20078, #20079}
2. `search merged:>=CP` → {#20035 (exact boundary, already processed), #20078, #20079}
3. `git log --first-parent upstream/master` after checkpoint commit `fcd05cca` (#20035) → exactly
   `e94cf06c` (#20078), `c0319056` (#20079)

### Decisions
| PR | Title | Merged (UTC) | Decision | Rationale |
|---|---|---|---|---|
| [#20078](https://github.com/apache/pinot/pull/20078) | Update DOAP metadata for Apache Pinot 1.6.0 | 2026-10-29T00:02:56Z | not_relevant | ASF project-metadata only: updates `doap_Pinot.rdf` (Apache DOAP release descriptor) to 1.6.0 (version name, revision, release date). Single RDF file; not user-facing documentation, config, API, or behavior. |
| [#20079](https://github.com/apache/pinot/pull/20079) | Remove expired InstancePlanMakerImplV2 constant aliases | 2026-10-29T00:59:45Z | not_relevant | Internal Java source cleanup. Removes 14 `@Deprecated public static final` constant aliases that delegated to `CommonConstants.Server.*`. Verified from merged diff: the config-key STRINGS and default VALUES live in `CommonConstants.Server` and are unchanged; only the duplicate Java aliases (deprecated for removal after 1.4) are gone. Downstream Java callers use `CommonConstants.Server.*`. No config key, default, query option, function, or documented behavior change. |

### Outcome
- Docs PRs created: **0**
- Docs PRs merged: **0**
- Upstream comments: **0** (neither PR docs-relevant)
- Slack: not sent (no new docs PRs)
- Validation: not applicable (no docs changes produced)

### Durable state
- Checkpoint ADVANCED `2026-10-28T23:58:25Z` → `2026-10-29T00:59:45Z` (max merged-at of the two fully-triaged PRs).
- `last_successful_run` → `2026-10-29T01:03:27Z`; `last_run_id` → `run-20261029T010113Z-18526`.
- #20078 and #20079 recorded as not_relevant in the processed-PR ledger (CAS commit `5d9da01f`).
- Lease released at end of run.

### Blockers
None.

---

## Run 2026-10-29T02:05:00Z (run id `run-20261029T020113Z-945`)

### Summary
Triage run. **1** new merged `apache/pinot` PR strictly after the prior checkpoint
`2026-10-29T00:59:45Z` was inventoried and classified **docs-relevant**. One minimal docs PR created and
squash-merged; upstream PR commented; Slack summary sent.

### Preflight
- GitHub auth: `xiangfu0` (ambient App token). `apache/pinot` = WRITE, `pinot-contrib/pinot-docs` = ADMIN.
- Durable `automation-state` branch read OK (checkpoint `2026-10-29T00:59:45Z`, prior run id `run-20261029T010113Z-18526`).
- Lease acquired via create-only CAS PUT of `automation-lock.json`; no concurrent holder.
- Working trees clean; `apache` = apache/pinot fetched (HEAD `6e0a0a1b`); docs repo cloned and rebased on `origin/latest`.

### Coverage (checkpoint `2026-10-29T00:59:45Z`)
Three independent cross-checks agree — complete coverage, no gaps:
1. `search merged:>CP` → {#19988}
2. `search merged:>=CP` → {#20079 (exact boundary, already processed), #19988}
3. `git log --first-parent apache/master` after checkpoint commit `c0319056` (#20079) → exactly `6e0a0a1b` (#19988)

### Decisions
| PR | Title | Merged (UTC) | Decision | Rationale |
|---|---|---|---|---|
| [#19988](https://github.com/apache/pinot/pull/19988) | Support ARRAY_AGG without a data type | 2026-10-29T01:36:32Z | docs_created | New user-facing SQL surface in both engines: `ARRAY_AGG(expr)`, `ARRAY_AGG(expr, isDistinct)`, and `ARRAY_AGG(DISTINCT expr)` without the explicit data-type argument. Verified from merged code — CalciteSqlParser maps the `DISTINCT` quantifier to a trailing boolean operand; `AggregateFunctionRewriteOptimizer` (single-stage) and `PinotAggregateTypeArgumentRewriteRule` (multi-stage) infer the type from the column (element type for MV; JSON→STRING); unsupported inferred/supplied types fail in the broker. Explicit-type form preserved. |

### Outcome
- Docs PRs created: **1** — [pinot-docs#1156](https://github.com/pinot-contrib/pinot-docs/pull/1156)
- Docs PRs merged: **1** — squash-merged 2026-10-29T02:04:23Z (commit `65ecae06`)
- Upstream comments: **1** — https://github.com/apache/pinot/pull/19988#issuecomment-6485861071
- Slack: sent (1 new docs PR)
- Validation: `git diff --check` clean; `validate-docs.py --summary-only` = PASS (10 pre-existing broken anchors, none in edited files; no new failures). PR checks (Validate changed docs, Full docs audit, GitBook) all passed before merge.

### Files changed
- `functions/aggregation/arrayagg.md` — signatures + examples for inferred-type and inline-`DISTINCT` forms.
- `functions/array/array_agg.md` — signatures + example for inferred-type and `DISTINCT`-keyword forms.

### Durable state
- Checkpoint ADVANCED `2026-10-29T00:59:45Z` → `2026-10-29T01:36:32Z` (#19988 merged-at).
- `last_successful_run` → `2026-10-29T02:05:00Z`; `last_run_id` → `run-20261029T020113Z-945`.
- #19988 recorded as docs_created (docs#1156, comment issuecomment-6485861071) in the processed-PR ledger (CAS commit `407f4301`).
- Lease released at end of run.

### Blockers
None.
