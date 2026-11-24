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

## Hourly check — 2026-11-24T02:16:41.041Z

No post-checkpoint merges or pending follow-ups; no docs PRs created and no Slack summary sent. Checkpoint remains `2026-11-24T00:46:39Z`.

## Hourly check — 2026-11-24T05:17:44.276Z

No post-checkpoint merges or pending follow-ups; no docs PRs created and no Slack summary sent. Checkpoint remains `2026-11-24T00:46:39Z`.

## Hourly check — 2026-11-24T06:15:45.036Z

No post-checkpoint merges or pending follow-ups; no docs PRs created and no Slack summary sent. Checkpoint remains `2026-11-24T00:46:39Z`.

## Hourly check — 2026-11-24T07:17:46.166Z

No post-checkpoint merges or pending follow-ups; no docs PRs created and no Slack summary sent. Checkpoint remains `2026-11-24T00:46:39Z`.

## Hourly check — 2026-11-24T08:15:16.984Z

Reconciled [#20334](https://github.com/apache/pinot/pull/20334) against first-parent master. Skipped: it removes stale implementation comments, test references, and an internal exception subclass without changing the SQL behavior or the planning error code. The SQL reference already covers leaf and intermediate aggregation and the rolling-upgrade guidance.

Checkpoint advanced through #20334 to `2026-11-24T07:41:33Z`. No pending follow-ups, docs PRs, or Slack summary.

## Hourly check — 2026-11-24T09:13:47.106Z

Reconciled [#20364](https://github.com/apache/pinot/pull/20364) against first-parent master. Skipped: fixes only minion test races; no production code or user-facing behavior changed.

Checkpoint advanced through #20364 to `2026-11-24T08:33:40Z`. No pending follow-ups, docs PRs, or Slack summary.

## Hourly check — 2026-11-24T10:17:18.729Z

- Reconciled one post-checkpoint `master` merge: [Apache Pinot #20314](https://github.com/apache/pinot/pull/20314). Its user-facing change makes it possible to unnest an array produced by `ARRAY_AGG` in a grouped subquery.
- Opened and squash-merged [docs #1215](https://github.com/pinot-contrib/pinot-docs/pull/1215) into `latest` and verified the [upstream comment](https://github.com/apache/pinot/pull/20314#issuecomment-7128636539).
- `git diff --check` and the full docs validator passed (no broken file links; 10 pre-existing anchor warnings). All four hosted checks passed on the merged PR head.
- Checkpoint advanced to `2026-11-24T09:35:46Z`. No pending follow-ups. Slack summary delivered (HTTP 200).

## Hourly check — 2026-11-24T11:16:19.850Z

GitHub's complete merged-PR search and the first-parent history both found no `master` merges after #20314. The checkpoint remains `2026-11-24T09:35:46Z`; no pending follow-ups, new docs PRs, or Slack summary.

## Hourly check — 2026-11-24T12:19:50.394Z

No `master` merges after #20314 in either GitHub's complete merged-PR search or the first-parent history. The checkpoint stays at `2026-11-24T09:35:46Z`; no pending follow-ups, new docs PRs, or Slack summary.

## Hourly check — 2026-11-24T13:15:50.952Z

Reconciled one post-checkpoint `master` merge: [Apache Pinot #20375](https://github.com/apache/pinot/pull/20375). Skipped: Dependency-only AWS SDK BOM patch bump (2.59.5 to 2.59.7); merged diff changes only the Maven version property, with no Pinot documentation change identified.

Checkpoint advanced to `2026-11-24T12:59:56Z`. No pending follow-ups, new docs PRs, or Slack summary.

## Hourly check — 2026-11-24T14:14:21.724Z

- Reconciled one post-checkpoint `master` merge: [Apache Pinot #20344](https://github.com/apache/pinot/pull/20344). Document the opt-in MSE broadcast join fusion and parallel leaf scan options, including eligibility, the join hint, and spool precedence.
- Opened and squash-merged [docs #1216](https://github.com/pinot-contrib/pinot-docs/pull/1216) into `latest` and verified the [upstream comment](https://github.com/apache/pinot/pull/20344#issuecomment-7134128193).
- `git diff --check` and the docs validator passed (no broken file links; 10 pre-existing anchor warnings). All four hosted checks passed on the merged PR head.
- Checkpoint advanced to `2026-11-24T13:48:06Z`. No pending follow-ups. Slack summary delivered (HTTP 200).

## Hourly check — 2026-11-24T15:10:23.708Z

No `master` merges after #20344 in either GitHub's complete merged-PR search or the first-parent history. The checkpoint stays at `2026-11-24T13:48:06Z`; no pending follow-ups, new docs PRs, or Slack summary.

## Hourly check — 2026-11-24T16:07:53.305Z

No new `master` merges after #20344; the complete GitHub search and first-parent history agree. Checkpoint unchanged at `2026-11-24T13:48:06Z`. No pending follow-ups, new docs PRs, or Slack summary.

## Hourly check — 2026-11-24T17:09:24.048Z

No new `master` merges after #20344; the complete GitHub search and first-parent history agree. Checkpoint unchanged at `2026-11-24T13:48:06Z`. No pending follow-ups, new docs PRs, or Slack summary.

## Hourly check — 2026-11-24T18:13:25.500Z

No merges to `master` after #20344, per GitHub's complete merged-PR search and the first-parent history. Checkpoint unchanged at `2026-11-24T13:48:06Z`. No pending follow-ups, new docs PRs, or Slack summary.

## Hourly check — 2026-11-24T19:14:26.213Z

No new `master` merges after #20344; the complete GitHub search and first-parent history agree. Checkpoint unchanged at `2026-11-24T13:48:06Z`. No pending follow-ups, new docs PRs, or Slack summary.

## Hourly check — 2026-11-24T20:14:56.651Z

Reconciled one post-checkpoint `master` merge: [Apache Pinot #20370](https://github.com/apache/pinot/pull/20370). No docs change: Existing ZooKeeper Basic Auth docs already state that broker API requests require credentials when enabled. The change enforces that documented requirement without adding a setting or changing setup.

Checkpoint advanced to `2026-11-24T19:19:10Z`. No pending follow-ups, new docs PRs, or Slack summary.

## Hourly check — 2026-11-24T21:18:26.885Z

- Reconciled one post-checkpoint `master` merge: [Apache Pinot #20369](https://github.com/apache/pinot/pull/20369). Clarify table checks for time-series queries and explain plans, and explain why Pinot denies requests when applicable row filters cannot be enforced.
- Opened and squash-merged [docs #1217](https://github.com/pinot-contrib/pinot-docs/pull/1217) into `latest` and verified the [upstream comment](https://github.com/apache/pinot/pull/20369#issuecomment-7144807651).
- `git diff --check` and the docs validator passed (no broken file links; 10 existing anchor warnings). All four hosted checks passed on the merged PR head.
- Checkpoint advanced to `2026-11-24T21:14:37Z`. No pending follow-ups. Slack summary delivered (HTTP 200).
