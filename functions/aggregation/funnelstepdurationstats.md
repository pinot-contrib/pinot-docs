---
description: This section contains reference documentation for the FUNNELSTEPDURATIONSTATS function.
---

# FUNNELSTEPDURATIONSTATS

Computes step-to-step duration statistics for window funnel matches.

## Signature

> `FUNNELSTEPDURATIONSTATS(timestampExpression, windowSize, numberSteps, stepExpression1, ..., stepExpressionN, 'durationFunctions=...' [, 'mode=...' | 'strict_order' | 'strict_deduplication' | 'strict_increase' | 'keep_all' | 'maxStepDuration=...'])`

## Parameters

| Parameter | Description |
| --------- | ----------- |
| `timestampExpression` | Expression that evaluates to the event timestamp. Pinot accepts `TIMESTAMP` or `LONG` values. |
| `windowSize` | Positive time window literal. Funnel steps must complete within this window. |
| `numberSteps` | Number of funnel steps. This must match the number of step expressions that follow. |
| `stepExpression1 ... stepExpressionN` | Boolean expressions that define each funnel step in order. |
| `'durationFunctions=...'` | Required config string listing the statistics to emit. Supported values are `COUNT`, `AVG`, `MIN`, `MEDIAN`, `MAX`, and `PERCENTILE<value>` such as `PERCENTILE95`. The output preserves the requested function order. |
| Optional trailing arguments | Optional funnel controls shared with the other window funnel functions, including `mode=...`, `strict_order`, `strict_deduplication`, `strict_increase`, `keep_all`, and `maxStepDuration=...`. |

## Returns

Returns a `DOUBLE[]` flattened in step order.

For each step, Pinot emits the requested statistics in the same order they were listed in `durationFunctions`. If `COUNT` is requested, Pinot includes it for every step. Duration metrics on the final step use Pinot's double null placeholder because there is no next step to measure against.

If `COUNT` is omitted and no funnel completes, Pinot returns an empty array.

## Example

```sql
SELECT
  userId,
  funnelStepDurationStats(
    timestampCol,
    '1000',
    4,
    url = '/product/search',
    url = '/cart/add',
    url = '/checkout/start',
    url = '/checkout/confirmation',
    'durationFunctions=count,avg,min,median,percentile95,max'
  ) AS statsArray
FROM events
GROUP BY userId
HAVING arrayLength(statsArray) > 0
ORDER BY userId
```

In Pinot's integration tests, a completed four-step funnel with 10-millisecond gaps between steps returns duration stats such as:

* step 0 -> step 1: `count=1`, `avg=10`, `min=10`, `median=10`, `percentile95=10`, `max=10`
* step 1 -> step 2: the same six values
* step 2 -> step 3: the same six values

For more information on the related funnel functions, see [Funnel Analysis Functions](../funnel/README.md).
