---
description: Pinot broker response payload reference.
---

# Query Response Format

Pinot query responses are SQL-like tabular payloads with a small set of execution statistics around them. This page documents the fields you are most likely to inspect when debugging query behavior or paging through large results.

## Response Shape

Standard broker query responses include a `resultTable` with:

| Field | Meaning |
| --- | --- |
| `resultTable.dataSchema.columnNames` | Names returned by the query |
| `resultTable.dataSchema.columnDataTypes` | Data types for each returned column |
| `resultTable.rows` | Row values in column order |

Cursor-backed responses still use the same `resultTable` shape, but the `rows` array contains only the current page.

## Cursor Fields

When a query is submitted with `getCursor=true`, Pinot adds cursor metadata around the normal broker response:

| Field | Meaning |
| --- | --- |
| `requestId` | Cursor identifier used with `/responseStore/{requestId}` |
| `numRowsResultSet` | Total rows available across the full result set |
| `offset` | Zero-based offset of the current page |
| `numRows` | Number of rows returned in the current page |
| `brokerHost` | Broker host that owns the response store |
| `brokerPort` | Broker port that owns the response store |
| `submissionTimeMs` | Timestamp when Pinot created the response-store entry |
| `expirationTimeMs` | Timestamp when Pinot considers the cursor expired |
| `cursorResultWriteTimeMs` | Time spent writing the original result into the response store; typically populated on the initial cursor-creating response |
| `cursorFetchTimeMs` | Time spent reading the current page from the response store |
| `bytesWritten` | Serialized size of the stored result |

## Execution Stats

| Field | Meaning |
| --- | --- |
| `timeUsedMs` | Broker-side time spent handling the query |
| `numServersQueried` | Number of servers asked to process the query |
| `numServersResponded` | Number of servers that returned a response |
| `numSegmentsQueried` | Number of segments considered for the query |
| `numSegmentsProcessed` | Number of segments actually processed |
| `numSegmentsMatched` | Number of segments with at least one match |
| `numDocsScanned` | Number of documents selected after filtering |
| `numEntriesScannedInFilter` | Filter-phase entries scanned |
| `numEntriesScannedPostFilter` | Post-filter entries scanned |
| `partialResult` | Whether Pinot returned a partial result instead of a fully complete answer |
| `earlyTerminationReasons` | Multi-stage V2 response field listing early-termination reasons such as `DISTINCT_MAX_ROWS` |
| `maxRowsInDistinctReached` | Single-stage DISTINCT flag indicating the `maxRowsInDistinct` budget was exceeded |
| `maxRowsWithoutChangeInDistinctReached` | Single-stage DISTINCT flag indicating the `maxRowsWithoutChangeInDistinct` budget was exceeded |
| `maxExecutionTimeInDistinctReached` | Single-stage DISTINCT flag indicating the `maxExecutionTimeMsInDistinct` budget was exceeded |
| `numGroupsLimitReached` | Whether group-by trimming hit the limit |
| `numGroupsWarningLimitReached` | Whether group-by execution crossed the configured warning threshold for number of groups |
| `serverStats` | Single-stage per-server timing and response-size breakdown |
| `stageStats` | Per-stage stats for multi-stage queries |
| `exceptions` | Query-processing exceptions, if any |
| `rlsFiltersApplied` | Whether row-level security predicates were injected |

For DISTINCT early termination, the response shape depends on the engine. Single-stage responses use the legacy
boolean fields such as `maxRowsInDistinctReached`, while multi-stage V2 responses surface the same condition through
`partialResult=true` plus `earlyTerminationReasons`.

For single-stage queries, `serverStats` is a semicolon-delimited string with a header row followed by one entry per server. The header names the metrics in order:

```text
Server=SubmitDelayMs,ResponseDelayMs,ResponseSize,DeserializationTimeMs,RequestSentDelayMs;pinot-server-0_O=0,1,7571,0,0
```

This makes `serverStats` useful when you need a lightweight broker response field for pinpointing which single-stage server responded slowly or returned an unexpectedly large payload.

## Example

```bash
curl -H "Content-Type: application/json" -X POST \
  -d '{"sql":"SELECT moo, bar, foo FROM myTable ORDER BY foo DESC"}' \
  http://localhost:8099/query/sql
```

Cursor example:

```bash
curl -H "Content-Type: application/json" -X POST \
  -d '{"sql":"SELECT * FROM myTable LIMIT 100000"}' \
  'http://localhost:8099/query/sql?getCursor=true&numRows=1000'
```

## What this page covered

- The structure of Pinot broker responses.
- The execution stats that matter most when debugging performance or correctness.
- The fields that differ between a plain result and a multi-stage query response.

## Next step

If the field names look right but the data is not, inspect the query plan and response-store flow next.

## Related pages

- [API Reference](README.md)
- [Broker Query API](query-api.md)
- [Query using Cursors](../../build-with-pinot/querying-and-sql/query-execution-controls/query-using-cursors.md)
- [Querying Pinot](../../build-with-pinot/querying-and-sql/querying-pinot.md)
