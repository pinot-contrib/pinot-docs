# Pinot docs update — 2026-11-22 UTC

## Hourly check — 2026-11-22T00:27:11.229Z

No post-checkpoint merges or pending follow-ups; no docs PRs created and no Slack summary sent. Checkpoint remains `2026-11-21T10:35:05Z`.

## Hourly check — 2026-11-22T01:32:10.967Z

No post-checkpoint merges or pending follow-ups; no docs PRs created and no Slack summary sent. Checkpoint remains `2026-11-21T10:35:05Z`.

## Hourly check — 2026-11-22T02:34:41.367Z

Four post-checkpoint merges reconciled against first-parent master. Two docs PRs merged and linked upstream; two internal optimizations skipped. Checkpoint advanced to `2026-11-22T02:19:22Z` (upstream #20075); no pending follow-ups.

- [#20070](https://github.com/apache/pinot/pull/20070) — Skipped: planner constant-folding optimization; no SQL contract change.
- [#20072](https://github.com/apache/pinot/pull/20072) — Documented immutable HNSW build tuning in [docs #1207](https://github.com/pinot-contrib/pinot-docs/pull/1207) (merged; [upstream comment](https://github.com/apache/pinot/pull/20072#issuecomment-7073023119)).
- [#20071](https://github.com/apache/pinot/pull/20071) — Skipped: automatic Lucene buffer read optimization; no configuration or query change.
- [#20075](https://github.com/apache/pinot/pull/20075) — Documented BM25 scoring in [docs #1208](https://github.com/pinot-contrib/pinot-docs/pull/1208) (merged; [upstream comment](https://github.com/apache/pinot/pull/20075#issuecomment-7073026273)).

Both PRs passed local diff/docs validation (10 pre-existing anchor warnings, zero broken file links) and both hosted docs and both GitBook checks on their exact heads. One Slack summary delivered (HTTP 200).
