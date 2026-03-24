---
description: Table, database, and application query quotas in Pinot.
---

# Query Quotas

Query quotas cap how much traffic Pinot will accept. They are the right tool when you want predictable isolation instead of one-off query tuning.

## Quota levels

- table quotas protect a specific table
- database quotas cap traffic across all tables in a database
- application quotas cap traffic by application name

## Table quotas

Table quotas live in table configuration.

```json
{
  "tableName": "stores",
  "tableType": "OFFLINE",
  "quota": {
    "maxQueriesPerSecond": 300
  }
}
```

If a table is served by multiple brokers, the effective quota is split across those brokers.

## Database quotas

Database quotas are useful when you want one limit to apply across all tables in a database.

```sh
curl -X POST 'http://localhost:9000/cluster/configs' \
  -H 'Content-Type: application/json' \
  -d '{
    "databaseMaxQueriesPerSecond": "1000"
  }'
```

```sh
curl -X POST 'http://localhost:9000/databases/myDatabase/quotas?maxQueriesPerSecond=1200'
```

## Application quotas

Application quotas are the cleanest way to isolate traffic from different client systems.

```sh
curl -X POST 'http://localhost:9000/cluster/configs' \
  -H 'Content-Type: application/json' \
  -d '{
    "applicationMaxQueriesPerSecond": "1000"
  }'
```

Use `SET applicationName = 'myApp';` in the query when you want the quota to apply to a specific workload.

## What to expect when multiple quotas exist

Pinot enforces the most specific applicable guardrail:

1. application quota
2. database quota
3. table quota

If more than one limit applies, the query fails as soon as one limit is exceeded.

## What this page covered

This page covered the three quota layers, how they are configured, and the enforcement order when more than one limit is present.

## Next step

If you need to stop a query rather than rate-limit it, read [Query cancellation](query-cancellation.md).

## Related pages

- [Query options](query-options.md)
- [Query cancellation](query-cancellation.md)
- [Querying Pinot](../querying-pinot.md)
