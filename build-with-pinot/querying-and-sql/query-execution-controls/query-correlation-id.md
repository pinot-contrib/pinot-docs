---
description: How Pinot assigns and reuses query correlation IDs.
---

# Correlation IDs

Every Pinot query gets a correlation ID so you can track it through broker and server logs.

## Default behavior

Pinot assigns a correlation ID automatically when the broker receives a query. That ID is included in the logging context and can be used to follow the query through the cluster.

## Custom IDs

If your client already has a request identifier, set `clientQueryId` so Pinot uses it as the correlation ID.

```sql
SET clientQueryId = 'query-2026-03-24-001';
SELECT * FROM stores LIMIT 10;
```

Use a high-entropy value such as a UUID when you provide your own ID.

## Why it matters

Correlation IDs are most useful when you need to:

- search logs for a single request
- cancel a query later
- connect application tracing with Pinot query execution

## What this page covered

This page covered how Pinot assigns query correlation IDs, how to provide a custom one, and why the ID matters operationally.

## Next step

If you need to stop a running query, read [Query cancellation](query-cancellation.md).

## Related pages

- [Query options](query-options.md)
- [Query cancellation](query-cancellation.md)
- [Querying Pinot](../querying-pinot.md)
