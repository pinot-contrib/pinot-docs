---
description: Use logical tables when one query name should span multiple physical Pinot tables without exposing the partitioning scheme to users.
---

# Logical Tables

Logical tables are a naming and routing layer on top of physical tables. They let you split data by region, age, or operating mode while keeping one user-facing table name.

Use a logical table when the split is an implementation detail, not part of the query contract. Keep the physical tables aligned on schema, and use a reference physical table only as a metadata anchor.

## When they help

Logical tables are most useful when you need one of these patterns:

Different physical tables per region or business unit.

Separate offline and realtime tables that still answer one business question.

Time-sliced tables that should be queried together.

## Design rules

Keep the underlying schemas aligned. Keep the logical name stable. Prefer this pattern only when the underlying split is operationally meaningful; do not use it to hide a modeling problem that should instead be solved with cleaner ingestion.

For hybrid-style layouts, make the time boundary explicit so Pinot does not double count overlapping data.

## Example pattern

```json
{
  "tableName": "orders",
  "brokerTenant": "DefaultTenant",
  "physicalTableConfigMap": {
    "ordersUS_OFFLINE": {},
    "ordersEU_OFFLINE": {}
  },
  "refOfflineTableName": "ordersUS_OFFLINE"
}
```

## Learn more

The original logical-table walkthrough lives in [Logical Table](../../basics/components/table/logical-table.md).

## What this page covered

This page covered when to use logical tables and how they hide physical table splits from readers.

## Next step

Read [Schema Evolution](schema-evolution.md) if the schema needs to grow after the table is already in production.

## Related pages

- [Data Modeling](README.md)
- [Schema and Table Shape](schema.md)
- [Schema Evolution](schema-evolution.md)
- [Original Logical Table Doc](../../basics/components/table/logical-table.md)
