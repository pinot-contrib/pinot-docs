---
description: Understand Pinot schema design, table shape, null handling, and the schema fields that drive query and ingestion behavior.
---

# Schema and Table Shape

A Pinot schema defines the columns that exist in a table and how Pinot should treat them. The important part is not only the column list, but also the shape of the table: which fields are dimensions, metrics, and time fields, how nulls behave, and whether the table is built for offline, realtime, or hybrid ingestion.

Pinot stores schema and table metadata separately, but the two should be designed together. Keep the schema narrow enough to match the data you actually query, and keep the table config dense enough for reference pages rather than this narrative overview.

## What to design

The schema answers four practical questions:

- What columns exist?
- What data type does each column use?
- Which columns are dimensions, metrics, or date-time fields?
- How should Pinot handle missing values and time semantics?

## Good defaults

Use column names that are stable and business-facing. Prefer simple types that match the source data. Add only the fields you need at query time, because schema changes are additive and should be deliberate.

For time columns, keep one primary time field in mind for retention and hybrid-table boundary behavior. For null handling, decide early whether the table needs column-based or table-based semantics.

## Example schema

```json
{
  "schemaName": "orders",
  "enableColumnBasedNullHandling": true,
  "dimensionFieldSpecs": [
    { "name": "orderId", "dataType": "STRING" },
    { "name": "customerId", "dataType": "STRING" },
    { "name": "region", "dataType": "STRING" }
  ],
  "metricFieldSpecs": [
    { "name": "amount", "dataType": "DOUBLE", "defaultNullValue": 0 }
  ],
  "dateTimeFieldSpecs": [
    {
      "name": "eventTime",
      "dataType": "LONG",
      "format": "EPOCH",
      "granularity": "1:DAYS"
    }
  ]
}
```

## When to use the reference pages

Use the [schema reference](../../configuration-reference/schema.md) when you need the exact JSON fields, validation rules, or date-time field formats. Use the [table reference](../../configuration-reference/table.md) when you need indexing, retention, or routing configuration.

## What this page covered

This page covered the parts of Pinot schema design that shape ingestion and query behavior.

## Next step

Read [Logical Tables](logical-tables.md) if one query name should route to multiple physical tables.

## Related pages

- [Data Modeling](README.md)
- [Logical Tables](logical-tables.md)
- [Schema Evolution](schema-evolution.md)
- [Schema Reference](../../configuration-reference/schema.md)
