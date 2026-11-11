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
