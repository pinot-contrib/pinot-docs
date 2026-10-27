---
description: This section contains reference documentation for the ANYVALUE function.
---

# ANYVALUE

Returns any arbitrary non-null value from the column for each group. Useful in GROUP BY queries for including columns that have a one-to-one mapping with the GROUP BY columns without adding them to the GROUP BY clause.

## Signature

> ANYVALUE(colName)
>
> ANYVALUE(colName, 'dataType')

By default, the single-stage engine returns `ANYVALUE(colName)` as a `STRING` regardless of the column's type. Pass an
optional second literal argument to fix the result type at construction, so that the value is read and returned as that
type (for example, `1` for a `BOOLEAN` column instead of `"1"`). Supported `dataType` values are `INT`, `LONG`,
`FLOAT`, `DOUBLE`, `BIG_DECIMAL`, `BOOLEAN`, `TIMESTAMP`, `STRING`, `BYTES`, and `UUID`; any other value (such as a
multi-value column type) fails the query.

{% hint style="warning" %}
The two-argument form was added in Pinot 1.5.0 and is rejected by older servers. In a rolling upgrade, use it (or
enable `inferAnyValueType`, below) only after all servers have been upgraded.
{% endhint %}

### Inferring the type automatically

When the `inferAnyValueType` query option is enabled, Pinot rewrites `ANYVALUE(expr)` to return the logical type of
`expr` in both the single-stage and multi-stage engines (a `JSON` column maps to `STRING`). The default of this option
comes from the `pinot.broker.query.infer.any.value.type` broker config, which defaults to `false` and can also be
changed live through the Helix cluster config (the cluster config takes precedence where it sets the key).

With the rewrite on, single-stage results change from `STRING` to the type of `expr`, and an unaliased result column
name changes from `anyvalue(col)` to `anyvalue(col,'INT')`.

## Usage Examples

These examples are based on the [Batch Quick Start](../../basics/getting-started/quick-start.md#batch-processing).

```sql
select league, ANYVALUE(playerName) AS samplePlayer
from baseballStats
GROUP BY league
```

| league | samplePlayer |
| ------ | ------------ |
| AA     | David Orr    |
| NL     | Fred Pfeffer |
