# Automation memory — pinot-docs updater
- 

## 2026-11-11T00:05:48Z — run-20261111T000219Z-opus48-cloud
- Result: no-op. 0 PRs merged strictly after checkpoint 2026-11-10T21:05:33Z (upstream master tip #20216 == checkpoint, already ledgered).
- Checkpoint unchanged; ledger stays 111. Lease CAS-serialized, no overlap.
- Preflight confirmed: apache/pinot WRITE, pinot-docs ADMIN. git-credential-tentrix mints creds only for xiangfu0/pinot; durable writes done via Contents API + GH_TOKEN.

## 2026-11-11T01:05Z — run-20261111T010144Z-opus48-cloud
- Result: docs_created. 2 PRs merged strictly after checkpoint 2026-11-10T21:05:33Z; 3-way reconcile (search / gh pr list / upstream/master git log) agree.
- #20183 "Evaluate user filters only on rows RLS allows" -> docs-relevant. Created docs PR 1171 against latest (operate-pinot/access-control.md), checks PASS, squash-merged 2026-11-11T01:05:32Z, upstream comment issuecomment-6783864502. Verified facts from merged code: RLS_FILTER_TIME_MS timer (ServerTimer.java), rlsFilterTimeMs log (ServerQueryLogger.java), hideTableLayoutStats zeroing totalDocs + segment counts (RlsResponseUtils.java).
- #20218 "Fix port reuse in ServerTableSizeReaderTest" -> not_relevant (single test file, flaky-test fix, no user-facing change).
- Checkpoint advanced to 2026-11-11T00:12:20Z. Ledger 111 -> 113.
- Note: docs branches pushed via `gh auth setup-git` (plain clone has no creds); durable state writes via Contents API CAS + GH_TOKEN. Slack notified (new docs PR).

## 2026-11-11T02:03:52Z — run-20261111T020144Z-opus48-cloud
- Result: no-op. 0 PRs merged strictly after checkpoint 2026-11-11T00:12:20Z. 3-way reconcile (gh search merged:>CP / gh pr list max mergedAt=#20183==checkpoint / upstream master git log --first-parent --since=CP) all agree: nothing new. Master tip fd91422b = #20183 (already docs#1171).
- Checkpoint unchanged; ledger stays 113. Lease/lock CAS-serialized, released at end; no overlap.

## 2026-11-11T04:02:48Z — run-20261111T040124Z-opus48-cloud
- Result: no-op. 0 PRs merged strictly after checkpoint 2026-11-11T00:12:20Z.
- 3-way reconcile agrees: (1) gh search prs --merged-at ">CP" = 0; (2) gh pr list top merged = #20218(00:07:49Z)/#20183(00:12:20Z=CP), both already ledgered (#20218 not_relevant, #20183 docs#1171); (3) apache/pinot master tip fd91422b = #20183 = checkpoint commit.
- Preflight: apache/pinot WRITE, pinot-docs ADMIN, auth user xiangfu0 via GH_TOKEN (tentrix mints git creds only for xiangfu0/pinot; durable writes via Contents API CAS). Note: local git remote 'origin' = xiangfu0/pinot fork (tip #19809, stale) — authoritative inventory uses apache/pinot API, not fork git log.
- Checkpoint unchanged; ledger stays 113. Lease CAS-serialized (acquired bc8cbeb, released fd2d7a3); no overlap. No Slack (no-op).

## 2026-11-11T05:08:19Z — run-20261111T050122Z-opus48-cloud
- Result: docs_created. 6 PRs merged strictly after checkpoint 2026-11-11T00:12:20Z; 3-way reconcile (gh search merged:>CP / gh pr list / upstream/master git log) all agree: 20108, 20201, 20211, 20203, 20202, 20210.
- #20202 "Run multi-server quickstarts in separate JVMs" -> docs-relevant: adds forked server JVMs with new system properties pinot.quickstart.server.xmx (default 1g) and pinot.quickstart.server.xms (defaults to resolved xmx), set via parent JVM JAVA_OPTS. Verified names/defaults from merged QuickstartServerProcess.java (INITIAL_HEAP_PROPERTY/MAX_HEAP_PROPERTY, DEFAULT_MAX_HEAP="1g"). Created docs PR 1172 (quick-start.md command options), checks PASS, squash-merged 2026-11-11T05:07:03Z, upstream comment issuecomment-6787589264.
- not_relevant: #20108 (internal perf; primitive-array intermediates for HISTOGRAM/SUM_ARRAY, compatible serde), #20201 (FUNNELCOUNT empty-segment merge ClassCastException bugfix), #20211 (test-only MailboxServiceTest race), #20203 (off-heap distinct-count set serialized-size precedence bugfix, wire-compatible), #20210 (GET /tasks/subtask/workers/progress 500 bugfix, restores documented behavior, no new config/response shape).
- Checkpoint advanced to 2026-11-11T04:57:09Z. Ledger 113 -> 119.
- validate-docs.py PASS (638 files, 10 broken anchors pre-existing on clean latest, 0 new). git diff --check clean. Durable writes via Contents API CAS + GH_TOKEN; docs branch pushed via gh auth setup-git. Slack notified (new docs PR).

## 2026-11-11T10:05Z — run-20261111T100213Z-opus48-cloud
- Result: docs_created. 1 PR merged strictly after checkpoint 2026-11-11T04:57:09Z; 3-way reconcile (gh search merged:>CP / gh pr list / upstream/master git log) all agree: only #20221.
- #20221 "Revert 'Reject time-based flush threshold for pauseless tables (#20168)'" -> docs-relevant REVERT. Reverses commit 1d0aae09; TableConfigUtils.validateIngestionConfig no longer rejects realtime.segment.flush.threshold.time (or legacy .llc) on pauseless tables; tests removed. No release contained #20168 (1.6.0 predates it). This made the docs we merged in #1170 stale.
- Action: reversed docs PR #1170. Created docs PR 1173 against latest (operate-pinot/pauseless-consumption.md: restored "same segment flush thresholds as standard real-time ingestion", removed the "Not supported" note, removed the warning hint block, removed the #20168 reference link). Diff = exact inverse of #1170 (+2/-11). Checks PASS, squash-merged 2026-11-11T10:05:36Z (merge 6a3d1c29), upstream comment issuecomment-6792949350.
- Ledger: annotated #20168 with superseded_by_revert=20221, docs_reverted_by_pr=1173.
- Checkpoint advanced to 2026-11-11T09:24:21Z. Ledger 119 -> 120.
- validate-docs.py PASS (638 files; 10 broken anchors pre-existing on clean latest, 0 new). git diff --check clean. Durable writes via Contents API CAS + GH_TOKEN (sha 84d6ca2c unchanged across run = no overlap); docs branch pushed via GH_TOKEN x-access-token URL (plain clone has no creds). Slack notified (new docs PR).
- LESSON: reverts of previously-ledgered docs_created PRs require reversing the earlier docs PR, not just skipping. Always check if the reverted PR produced a docs PR.

## 2026-11-11T11:03:02Z — run-20261111T110118Z-opus48-cloud
- Result: no-op. 0 PRs merged strictly after checkpoint 2026-11-11T09:24:21Z.
- 3-way reconcile agrees: (1) gh pr list top merged = #20221 @ 09:24:21Z == checkpoint (already docs#1173); (2) count merged strictly >CP = 0; (3) apache/pinot master tip 16036c67 = "Revert ... (#20221)" = checkpoint commit.
- Preflight: apache/pinot WRITE, pinot-docs ADMIN, auth xiangfu0 via GH_TOKEN. Durable read+CAS write OK.
- Checkpoint unchanged; ledger stays 120. Lock/lease CAS-serialized (acquired 6cb1530, released at end); no overlap. No Slack (no-op).
