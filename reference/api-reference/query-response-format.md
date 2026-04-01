---
description: Pinot broker response payload reference.
---

# Query Response Format

Pinot query responses are SQL-like tabular payloads with a small set of execution statistics around them. This page documents the fields you are most likely to inspect when debugging query behavior, paging responses, or comparing single-stage and multi-stage output.

## Response Shape

The broker response always includes a `resultTable` with:

<table>
  <thead>
    <tr>
      <th>Field</th>
      <th>Meaning</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>`resultTable.dataSchema.columnNames`</td>
      <td>Names returned by the query</td>
    </tr>
    <tr>
      <td>`resultTable.dataSchema.columnDataTypes`</td>
      <td>Data types for each returned column</td>
    </tr>
    <tr>
      <td>`resultTable.rows`</td>
      <td>Row values in column order</td>
    </tr>
  </tbody>
</table>

## Execution Stats

<table>
  <thead>
    <tr>
      <th>Field</th>
      <th>Meaning</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>`timeUsedMs`</td>
      <td>Broker-side time spent handling the query</td>
    </tr>
    <tr>
      <td>`numServersQueried`</td>
      <td>Number of servers asked to process the query</td>
    </tr>
    <tr>
      <td>`numServersResponded`</td>
      <td>Number of servers that returned a response</td>
    </tr>
    <tr>
      <td>`numSegmentsQueried`</td>
      <td>Number of segments considered for the query</td>
    </tr>
    <tr>
      <td>`numSegmentsProcessed`</td>
      <td>Number of segments actually processed</td>
    </tr>
    <tr>
      <td>`numSegmentsMatched`</td>
      <td>Number of segments with at least one match</td>
    </tr>
    <tr>
      <td>`numDocsScanned`</td>
      <td>Number of documents selected after filtering</td>
    </tr>
    <tr>
      <td>`numEntriesScannedInFilter`</td>
      <td>Filter-phase entries scanned</td>
    </tr>
    <tr>
      <td>`numEntriesScannedPostFilter`</td>
      <td>Post-filter entries scanned</td>
    </tr>
    <tr>
      <td>`numGroupsLimitReached`</td>
      <td>Whether group-by trimming hit the limit</td>
    </tr>
    <tr>
      <td>`stageStats`</td>
      <td>Per-stage stats for multi-stage queries</td>
    </tr>
    <tr>
      <td>`exceptions`</td>
      <td>Query-processing exceptions, if any</td>
    </tr>
    <tr>
      <td>`rlsFiltersApplied`</td>
      <td>Whether row-level security predicates were injected</td>
    </tr>
  </tbody>
</table>

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
- [Query using Cursors](../../users/user-guide-query/query-using-cursors.md)
- [Querying Pinot](../../build-with-pinot/querying-and-sql/querying-pinot.md)
