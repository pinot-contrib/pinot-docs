---
description: How to stop a running Pinot query.
---

# Query Cancellation

Use query cancellation when a query is still running and you need to stop it before it finishes.

## Enable tracking first

Query cancellation depends on query tracking being enabled on both the server and the broker.

```properties
pinot.server.enable.query.cancellation=true
pinot.broker.enable.query.cancellation=true
```

## Preferred flow: cancel by client query ID

The cleanest cancellation flow is to set `clientQueryId` on the query and then cancel by that ID.

```sql
SET clientQueryId = 'query-2026-03-24-001';
SELECT * FROM stores LIMIT 100;
```

Then cancel it with the matching ID:

```sh
curl -X DELETE 'http://localhost:9000/queryClient/query-2026-03-24-001'
```

This is the best option for programs because the client query ID can also be used as the correlation ID for logs.

## Fallback flow: cancel by internal broker ID

If you do not control the client query ID, Pinot can still cancel a query using the broker-assigned internal ID. That flow is more operationally awkward because you need both the broker and the internal query ID.

## What this page covered

This page covered the prerequisites for cancellation, the recommended client-query-ID flow, and the internal-ID fallback.

## Next step

If you need the query ID for logs or tracing, read [Correlation IDs](query-correlation-id.md).

## Related pages

- [Query options](query-options.md)
- [Correlation IDs](query-correlation-id.md)
- [Query quotas](query-quotas.md)
