---
description: Describes the unnest operator in the multi-stage query engine.
---

# Unnest

The unnest operator expands an array column into one row per element. It is invoked via the `CROSS JOIN UNNEST(...)` SQL syntax and is only available in the multi-stage query engine (MSE).

{% hint style="info" %}
`CROSS JOIN UNNEST` requires `useMultistageEngine=true`. It is not supported in the single-stage engine.
{% endhint %}

## SQL syntax

### Basic unnesting

```sql
SELECT t.id, elem
FROM myTable AS t
CROSS JOIN UNNEST(t.arrayColumn) AS u(elem)
```

Each row in `myTable` that has `n` elements in `arrayColumn` produces `n` output rows. Rows where `arrayColumn` is `NULL` or empty produce no output rows.

### WITH ORDINALITY

Adding `WITH ORDINALITY` attaches a 1-based position index to each unnested element:

```sql
SELECT t.id, elem, pos
FROM myTable AS t
CROSS JOIN UNNEST(t.arrayColumn) WITH ORDINALITY AS u(elem, pos)
```

The ordinality column (`pos`) reflects the 1-based position of each element in the original array.

### Unnesting multiple arrays together

Multiple arrays can be passed to one `UNNEST` call:

```sql
SELECT t.id, tag, score
FROM myTable AS t
CROSS JOIN UNNEST(t.tags, t.scores) AS u(tag, score)
```

When multiple arrays are unnested together, Pinot aligns them by position, like a zip operation. If the arrays have different lengths, shorter arrays are padded with `NULL` values. Add `WITH ORDINALITY` when you also need the 1-based element position:

```sql
SELECT t.id, tag, score, pos
FROM myTable AS t
CROSS JOIN UNNEST(t.tags, t.scores) WITH ORDINALITY AS u(tag, score, pos)
```

## Filtering unnested elements

You can filter on the unnested alias in a `WHERE` clause:

```sql
SELECT t.id, tag
FROM myTable AS t
CROSS JOIN UNNEST(t.tags) AS u(tag)
WHERE tag LIKE 'pinot%'
```

## Aggregating after unnesting

```sql
SELECT tag, COUNT(*) AS occurrences
FROM myTable AS t
CROSS JOIN UNNEST(t.tags) AS u(tag)
GROUP BY tag
ORDER BY occurrences DESC
LIMIT 10
```

## Implementation details

### Blocking nature

The unnest operator is a streaming operator. It reads rows from its single upstream and emits output rows as it processes each input row. The operator does not buffer the full input before emitting.

### NULL and empty array handling

For a single unnested array, rows where the column evaluates to `NULL` or to an empty array produce zero output rows. This matches the SQL `CROSS JOIN` semantic (no match = no output row). For multiple arrays in the same `UNNEST` call, Pinot aligns elements by position and pads shorter arrays with `NULL` values.

### Output column pruning

By default, Pinot keeps passthrough columns in the intermediate `UNNEST` output schema, including the source array column. You can opt into pruning unused passthrough columns with `SET unnestColumnPruning=true`, or set `pinot.broker.multistage.unnest.column.pruning=true` to make that the broker default.

This optimization only applies on the logical planner path. Pinot ignores it when `usePhysicalOptimizer=true`, and you should keep it disabled until all servers in the cluster support the smaller `UNNEST` output schema.

## Hints

None

## Stats

### executionTimeMs

Type: Long

The summation of time spent by all threads executing the operator.

### emittedRows

Type: Long

The number of rows emitted by the operator after unnesting.

## Explain attributes

The unnest operator appears in the logical explain plan as `LogicalCorrelate` with `Uncollect`.

### Example explain plan

```sql
EXPLAIN PLAN FOR
SELECT t.id, elem
FROM myTable AS t
CROSS JOIN UNNEST(t.arrayColumn) AS u(elem)
```

Expected output (illustrative):

```
LogicalProject(id=[$0], elem=[$1])
  LogicalCorrelate(correlation=[$cor0], joinType=[INNER], requiredColumns=[{2}])
    LogicalTableScan(table=[[default, myTable]])
    Uncollect
      LogicalProject($f0=[$cor0.arrayColumn])
        LogicalValues(tuples=[[{ 0 }]])
```
