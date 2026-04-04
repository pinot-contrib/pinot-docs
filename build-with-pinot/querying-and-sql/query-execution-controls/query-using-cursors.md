---
description: Cursor pagination for large Pinot result sets.
---

# Cursor Pagination

Cursor pagination lets Pinot return a query result in pages instead of forcing the whole result set into one response. Pinot stores the full result in the broker response store and returns slices of it as the client asks for more rows.

## When to use it

Use cursor pagination when:

- the result set is large
- the client wants to render pages incrementally
- you want to avoid holding the full result in client memory

## Submit a cursor-backed query

```sh
curl --request POST 'http://localhost:8099/query/sql?getCursor=true&numRows=1' \
  --header 'Content-Type: application/json' \
  --data '{"sql":"SELECT * FROM nation LIMIT 100"}'
```

If `numRows` is omitted, or set to `0`, Pinot uses the broker default from `pinot.broker.cursor.fetch.rows` (default `10000`).

The initial response includes the first page in `resultTable` together with cursor metadata:

| Field | Meaning |
| --- | --- |
| `requestId` | Cursor identifier used in later fetches |
| `numRowsResultSet` | Total rows available across the full result set |
| `offset` | Zero-based offset of the current page |
| `numRows` | Number of rows returned in the current page |
| `brokerHost` / `brokerPort` | Broker that owns the cursor state |
| `submissionTimeMs` | When Pinot created the response-store entry |
| `expirationTimeMs` | When the cursor expires |

## Fetch the next page

```sh
curl -X GET 'http://localhost:8099/responseStore/236490978000000006/results?offset=1&numRows=1'
```

Subsequent requests must go back to the same broker that created the cursor state. `offset` is zero-based, and `numRows` controls the next page size. If you omit `numRows` on a fetch request, Pinot again falls back to `pinot.broker.cursor.fetch.rows`.

## Inspect or delete cursor state

Use the metadata endpoint to inspect a cursor without fetching the row slice:

```sh
curl -X GET 'http://localhost:8099/responseStore/236490978000000006'
```

For operator workflows, Pinot also exposes:

- `GET /responseStore` to list active response-store entries on the broker
- `DELETE /responseStore/{requestId}` to delete a stored result early

## What to watch for

- the cursor response is tied to the original request ID
- the broker owns the cursor state
- cursor results expire after `pinot.broker.cursor.response.store.expiration` (default `1h`)
- the controller's `ResponseStoreCleaner` periodic task removes expired entries

## What this page covered

This page covered why cursor pagination exists, how to submit a cursor-backed query, and how to fetch additional pages.

## Next step

If you need to trace a query or cancel it later, read [Correlation IDs](query-correlation-id.md) and [Query cancellation](query-cancellation.md).

## Related pages

- [Query options](query-options.md)
- [Query cancellation](query-cancellation.md)
- [Querying Pinot](../querying-pinot.md)
