---
description: Pinot broker response payload reference.
---

# Query Response Format

Pinot query responses are SQL-like tabular payloads with a small set of execution statistics around them. This page documents the fields you are most likely to inspect when debugging query behavior, paging responses, or comparing single-stage and multi-stage output.

## Response Shape

The broker response always includes a `resultTable` with:

| Field | Meaning |
| --- | --- |
| `resultTable.dataSchema.columnNames` | Names returned by the query |
| `resultTable.dataSchema.columnDataTypes` | Data types for each returned column |
| `resultTable.rows` | Row values in column order |

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
| `numGroupsLimitReached` | Whether group-by trimming hit the limit |
| `stageStats` | Per-stage stats for multi-stage queries |
| `exceptions` | Query-processing exceptions, if any |
| `rlsFiltersApplied` | Whether row-level security predicates were injected |

## Example

```bash
curl -H "Content-Type: application/json" -X POST \
  -d '{"sql":"SELECT moo, bar, foo FROM myTable ORDER BY foo DESC"}' \
  http://localhost:8099/query/sql
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
