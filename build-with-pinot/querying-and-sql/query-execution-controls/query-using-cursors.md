---
description: Cursor pagination for large Pinot result sets.
---

# Cursor Pagination

Cursor pagination lets Pinot return a query result in pages instead of forcing the whole result set into one response.

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

The initial response includes a `requestId`, the broker that owns the cursor state, and the number of rows returned in the first page.

## Fetch the next page

```sh
curl -X GET 'http://localhost:8099/responseStore/236490978000000006/results?offset=1&numRows=1'
```

Subsequent requests must go back to the same broker that created the cursor state.

## What to watch for

- the cursor response is tied to the original request ID
- the broker owns the cursor state
- cursor results expire after the configured retention window

## What this page covered

This page covered why cursor pagination exists, how to submit a cursor-backed query, and how to fetch additional pages.

## Next step

If you need to trace a query or cancel it later, read [Correlation IDs](query-correlation-id.md) and [Query cancellation](query-cancellation.md).

## Related pages

- [Query options](query-options.md)
- [Query cancellation](query-cancellation.md)
- [Querying Pinot](../querying-pinot.md)
