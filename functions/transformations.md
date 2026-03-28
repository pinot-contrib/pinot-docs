---
description: A curated guide to Pinot transformation functions used in queries and ingestion configs.
---

# Transformations

This page groups the transformation functions that show up most often in Pinot ingestion configs and `SELECT` expressions. It is a navigation guide, not a full function reference: use the linked category pages for complete signatures and examples.

The most important split is whether the function returns a typed value that can be used directly in query output, or whether it is mainly intended for ingestion-time shaping. The typed JSON helpers are especially useful when you need a stable column type in SQL.

## Core families

| Family | Common functions | Best fit | Notes |
| --- | --- | --- | --- |
| Math | `ADD`, `SUB`, `MULT`, `DIV`, `MOD`, `ABS`, `CEIL`, `FLOOR`, `EXP`, `LN`, `SQRT`, `ROUND` | Query projections and ingestion transforms | Use these when you need deterministic numeric shaping before aggregation or filtering. |
| String | `UPPER`, `LOWER`, `SUBSTR`, `CONCAT`, `TRIM`, `LTRIM`, `RTRIM`, `REGEXPEXTRACT`, `REGEXPREPLACE`, `REPLACE`, `STARTSWITH` | Query projections and ingestion transforms | Strong fit for normalization, tokenization, and cleanup. |
| Date/time | `DATETRUNC`, `FROMDATETIME`, `TODATETIME`, `TOEPOCH*`, `FROMEPOCH*`, `DATETIMECONVERT` | Query projections and ingestion transforms | Use these to align timestamps to consistent buckets and storage formats. |
| JSON | `JSONEXTRACTSCALAR`, `JSONPATHSTRING`, `JSONPATHLONG`, `JSONPATHDOUBLE`, `JSONFORMAT`, `TOJSONMAPSTR` | Typed query output and ingestion configs | Prefer the typed helpers when the output column needs a stable SQL type. |
| Binary | `SHA`, `SHA256`, `SHA512`, `MD5`, `TOBASE64`, `UTF8` | Query projections and ingestion transforms | Useful for fingerprinting and encoding. |
| Array and multi-value | `ARRAYLENGTH`, `VALUEIN`, `MAP_VALUE`, array helpers | Query projections and ingestion transforms | Use these when a source column contains arrays or maps. |
| Utility | `EXTRACT`, `ISJSON`, `ISSUBNETOF` | Query projections and filtering | These helpers tend to sit at the boundary between shape cleanup and query logic. |

## JSON helpers worth calling out

Pinot supports both generic and typed JSON access. The typed variants are the safer choice for query output because they keep the result schema explicit.

- Use `JSONPATHSTRING`, `JSONPATHLONG`, and `JSONPATHDOUBLE` when the result type must be fixed.
- Use `JSONPATH` and `JSONPATHARRAY` when you are shaping ingestion data and the downstream schema can handle the inferred type.
- Use `JSONFORMAT` and `TOJSONMAPSTR` when you need to serialize an object or map back to JSON text.

## Multi-value patterns

The most common multi-value patterns are simple normalization and membership checks.

- `ARRAYLENGTH` gives you the size of a multi-value column.
- `VALUEIN` filters a multi-value column against a fixed set of values.
- `MAP_VALUE` extracts a value from a stored map when you know the key.

## When to use this guide

Use this page when you are:

- Designing ingestion transforms.
- Normalizing strings or timestamps before storing data.
- Converting semi-structured data into stable typed columns.
- Checking whether a function belongs in a projection, a filter, or an ingestion rule.

## What this page covered

- The transformation families that matter most in Pinot docs and ingestion configs.
- Which JSON helpers are safe when you need typed query output.
- Which multi-value helpers are most useful for shaping data before it reaches a table.

## Next step

- Open the relevant family page for the exact syntax and examples, or move to the SSE vs MSE guide if the query shape also depends on the execution engine.

## Related pages

- [Functions](README.md)
- [SSE vs MSE](../build-with-pinot/querying-and-sql/sse-vs-mse.md)
- [Supported Transformations](../users/user-guide-query/supported-transformations.md)
