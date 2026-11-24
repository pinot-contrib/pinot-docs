# Pinot docs update — 2026-11-24 UTC

## Hourly check — 2026-11-24T00:17:09.857Z

Reconciled two upstream merges with first-parent master. Neither changes the documented Pinot contract.

+- [#19915](https://github.com/apache/pinot/pull/19915) — Skipped: Internal instance-set hashing for replica-group lookups; equality and routing contract unchanged.
- [#20209](https://github.com/apache/pinot/pull/20209) — Skipped: Production changes only update comments; added tests verify existing upsert and metric-aggregation behavior.

Checkpoint advanced through #20209 to `2026-11-24T00:10:39Z`. No pending follow-ups, docs PRs, or Slack summary.

## Hourly check — 2026-11-24T01:21:10.695Z

Reconciled four post-checkpoint merges against first-parent master. [Docs #1214](https://github.com/pinot-contrib/pinot-docs/pull/1214) covers `BOOLEAN` operands and numeric results for multi-stage bitwise functions from [upstream #20338](https://github.com/apache/pinot/pull/20338). It passed local validation (zero broken file links; 10 existing anchor warnings) and all four hosted checks on its exact head, then merged and was [linked upstream](https://github.com/apache/pinot/pull/20338#issuecomment-7119052953).

- [#20331](https://github.com/apache/pinot/pull/20331) — Skipped: fixes an exception while preserving existing v1 range-index null semantics.
- [#20355](https://github.com/apache/pinot/pull/20355) — Skipped: dependency version bump only.
- [#20109](https://github.com/apache/pinot/pull/20109) — Skipped: integration-test fixture and suite changes only.

Checkpoint advanced through #20109 to `2026-11-24T00:46:39Z`. No pending follow-ups. One Slack summary delivered (HTTP 200).
