# Pinot docs update — 2026-11-25 (UTC)

## Hourly check — 2026-11-25T00:19:12.996Z

- [Docs #1218](https://github.com/pinot-contrib/pinot-docs/pull/1218) for [Apache Pinot #19894](https://github.com/apache/pinot/pull/19894) remains open. Exact-head hosted validation still shows `IN_PROGRESS` despite a success conclusion. No merge or upstream comment.
- Triaged [Apache Pinot #20214](https://github.com/apache/pinot/pull/20214). No docs follow-up: Internal realtime table shutdown fix: the ingestion-delay tracker cleans up without preventing consumer shutdown. No setup, metrics contract, or documented table-deletion procedure changed.
- The shared checkpoint stays at `2026-11-24T21:14:37Z` until #19894 is resolved. No new docs PR or Slack summary.

## Hourly check — 2026-11-25T01:19:14.519Z

- Opened and squash-merged [docs #1219](https://github.com/pinot-contrib/pinot-docs/pull/1219) for [Apache Pinot #19589](https://github.com/apache/pinot/pull/19589). Document STREAMING AND restriction pushdown eligibility and fallback, row-level security behavior, and rolling-upgrade compatibility. Local validation and all four hosted checks passed; verified the [upstream comment](https://github.com/apache/pinot/pull/19589#issuecomment-7149469333).
- [Docs #1218](https://github.com/pinot-contrib/pinot-docs/pull/1218) still lists its exact-head validation as `IN_PROGRESS`. #20214 remains a verified skip. The shared checkpoint stays at `2026-11-24T21:14:37Z` until #19894 is resolved.
- Slack summary for the new docs PR delivered (HTTP 200).

## Hourly check — 2026-11-25T02:18:15.313Z

- Verified that [docs #1218](https://github.com/pinot-contrib/pinot-docs/pull/1218) for [Apache Pinot #19894](https://github.com/apache/pinot/pull/19894) was already merged into `latest` and that both expected docs changes are present. The old validation check still displays `IN_PROGRESS` despite a success conclusion; this run did not initiate the merge. Posted and verified the [upstream docs link](https://github.com/apache/pinot/pull/19894#issuecomment-7150822812).
- Reconciled the complete upstream inventory, including the prior skip for #20214 and the verified merge and upstream link for docs #1219 (#19589). Advanced the shared checkpoint to `2026-11-25T00:58:24Z` with no pending follow-ups.
- No new docs PRs were created, so no Slack summary was sent.

## Hourly check — 2026-11-25T03:17:46.244Z

GitHub's complete merged-PR inventory and the first-parent history both show no new `master` merges after #19589. No pending follow-ups. The shared checkpoint stays at `2026-11-25T00:58:24Z`; no new docs PR or Slack summary.

## Hourly check — 2026-11-25T04:14:46.998Z

GitHub's complete merged-PR inventory and the first-parent history both show no new `master` merges after #19589. No pending follow-ups. The shared checkpoint stays at `2026-11-25T00:58:24Z`; no new docs PR or Slack summary.

## Hourly check — 2026-11-25T05:14:17.810Z

GitHub's complete merged-PR inventory and the first-parent history both show no new `master` merges after #19589. No pending follow-ups. The shared checkpoint stays at `2026-11-25T00:58:24Z`; no new docs PR or Slack summary.

## Hourly check — 2026-11-25T06:16:18.313Z

- Skipped [Apache Pinot #20335](https://github.com/apache/pinot/pull/20335). Removed unused or duplicate Java constants and switched remaining call sites to existing constants; no documented config or operational behavior changed.
- Opened and squash-merged [docs #1220](https://github.com/pinot-contrib/pinot-docs/pull/1220) for [Apache Pinot #20376](https://github.com/apache/pinot/pull/20376). Correct the range-index guide: BIG_DECIMAL requires a dictionary; RAW forward storage is supported with a standalone dictionary and range index version 2. Local validation and all four hosted checks passed; verified the [upstream comment](https://github.com/apache/pinot/pull/20376#issuecomment-7154665560).
- Advanced the shared checkpoint to `2026-11-25T05:30:33Z` with no pending follow-ups. Slack summary delivered (HTTP 200).

## Hourly check — 2026-11-25T07:14:55.638Z

Reconciled [Apache Pinot #20362](https://github.com/apache/pinot/pull/20362). No docs change: Internal table shutdown fix: an interrupt no longer abandons queued segment offloads before the existing timeout. No setting, timeout, or operator procedure changed.

Advanced the shared checkpoint to `2026-11-25T06:33:47Z`. No pending follow-ups, new docs PRs, or Slack summary.

## Hourly check — 2026-11-25T08:17:56.320Z

GitHub's merged-PR inventory and first-parent history agree: no new `master` merges after #20362. The shared checkpoint remains `2026-11-25T06:33:47Z`. No pending follow-ups, new docs PRs, or Slack summary.

## Hourly check — 2026-11-25T09:16:27.115Z

GitHub's merged-PR inventory and first-parent history agree: no new `master` merges after #20362. The shared checkpoint remains `2026-11-25T06:33:47Z`. No pending follow-ups, new docs PRs, or Slack summary.

## Hourly check — 2026-11-25T10:18:28.213Z

GitHub's merged-PR inventory and first-parent history agree: no new `master` merges after #20362. The shared checkpoint remains `2026-11-25T06:33:47Z`. No pending follow-ups, new docs PRs, or Slack summary.

## Hourly check — 2026-11-25T11:13:58.912Z

GitHub's merged-PR inventory and first-parent history agree: no new `master` merges after #20362. The shared checkpoint remains `2026-11-25T06:33:47Z`. No pending follow-ups, new docs PRs, or Slack summary.

## Hourly check — 2026-11-25T12:14:29.878Z

GitHub's merged-PR inventory and first-parent history agree: no new `master` merges after #20362. The shared checkpoint remains `2026-11-25T06:33:47Z`. No pending follow-ups, new docs PRs, or Slack summary.

## Hourly check — 2026-11-25T13:18:00.734Z

Reconciled [Apache Pinot #20387](https://github.com/apache/pinot/pull/20387). No docs change: Dependency-only patch bump for jnr-posix from 3.2.8 to 3.2.9; the merged diff only changes the Maven version property.

Advanced the shared checkpoint to `2026-11-25T12:30:29Z`. No pending follow-ups, new docs PRs, or Slack summary.

## Hourly check — 2026-11-25T14:19:32.317Z

GitHub's merged-PR inventory and first-parent history agree: no new `master` merges after #20387. The shared checkpoint remains `2026-11-25T12:30:29Z`. No pending follow-ups, new docs PRs, or Slack summary.

## Hourly check — 2026-11-25T15:24:02.617Z

GitHub's merged-PR inventory and first-parent history agree: no new `master` merges after #20387. The shared checkpoint remains `2026-11-25T12:30:29Z`. No pending follow-ups, new docs PRs, or Slack summary.
