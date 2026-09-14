# Page Cache Warmup

Page cache warmup replays selected queries on servers to read segment data into the operating system's page cache after a server restart or an offline segment refresh. It is opt-in per table. Use it when cold segment reads affect query latency, and choose a small representative query set to avoid displacing useful cached pages or competing with production traffic.

This is distinct from [default memory-map advice](tuning-default-mmap-advice.md), which changes access hints for memory-mapped files rather than replaying queries.

## Configure a table

Add `pageCacheWarmupConfig` at the top level of the table configuration. Enable either event independently; an absent block or `enabled: false` disables warmup for that event.

```json
{
  "pageCacheWarmupConfig": {
    "onRestart": {
      "enabled": true,
      "maxWarmupDurationSeconds": 180,
      "qpsLimit": 10
    },
    "onRefresh": {
      "enabled": true,
      "maxWarmupDurationSeconds": 180,
      "qpsLimit": 2
    }
  }
}
```

These are top-level fields to merge into an existing table config, not a complete table config. `maxWarmupDurationSeconds` defaults to 180 in each block. If `qpsLimit` is absent, restart warmup uses the table's maximum QPS divided by its replication factor, floored to 1 QPS; refresh warmup uses 20% of that per-replica rate, also floored to 1 QPS. Without a positive table QPS quota, the default is 1 QPS. An explicit `qpsLimit` overrides these calculated rates. The optional `policy` field is stored but is not currently used to select queries; do not rely on it to change replay behavior.

Restart warmup has an additional server-wide time budget of 180,000 ms by default (`pinot.server.max.pagecache.warmup.duration.ms`). Refresh has a controller-wide request budget of 180,000 ms by default (`controller.page.cache.warmup.duration.ms`). The server's default refresh rate fraction can be changed with `pinot.server.max.pagecache.refresh.warmup.qps.rate` (default `0.2`).

## Provide warmup queries

Store a nonempty JSON array of SQL strings through the controller endpoint. The table name in the path is the raw name; `tableType` is required. For example:

```sh
curl -X POST 'http://localhost:9000/pagecache/queries/airlineStats?tableType=OFFLINE' \
  -H 'Content-Type: application/json' \
  -d '["SELECT COUNT(*) FROM airlineStats_OFFLINE"]'
```

`GET` on the same URL returns the stored array, and `DELETE` removes it. By default the file is named `queries`; an optional `queryFileName` parameter selects another file. The controller stores files beneath `controller.page.cache.warmup.queries.dataDir` (default `/home/pinot/data/pageCacheWarmupQueries`) in a `<table>_<type>` directory. Configure this location as durable, accessible storage for your controller deployment. Restart warmup fetches the default `queries` file, while refresh warmup selects the most recently modified file for the offline table. Keep query files current and verify them with `GET` before relying on warmup.

The `pinot-admin.sh GeneratePageCacheWarmupQueries` command can generate and upload query sets from broker query logs, a Pinot query-statistics table, or a curated file. Run `pinot-admin.sh GeneratePageCacheWarmupQueries --help` for source-specific options.

## What runs and how to monitor it

On restart, each enabled table's resident segments are eligible for warmup. On an offline segment refresh, the controller sends warmup queries targeting the refreshed segments to the relevant servers; refresh warmup is not triggered for real-time tables by this path. Warmup executes through the server query scheduler, so set conservative QPS and duration limits, particularly during refresh when live queries may be running. If no query file is available, warmup is skipped.

Watch controller `PAGE_CACHE_WARMUP_REQUESTS` and `PAGE_CACHE_WARMUP_REQUEST_ERRORS` meters, server `PAGE_CACHE_WARMUP_QUERIES` and `PAGE_CACHE_WARMUP_SERVER_ERRORS` meters, and server logs for missing query sets and timeouts. Compare query latency and cache/I/O metrics before and after enabling it; warmup is best-effort and does not guarantee that pages remain cached.

Source: [Apache Pinot PR #16033](https://github.com/apache/pinot/pull/16033).
