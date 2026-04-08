---
description: This section contains reference documentation for the FUNNELEVENTSFUNCTIONEVAL function.
---

# FUNNELEVENTSFUNCTIONEVAL

Evaluates completed window funnel runs and returns selected extra-field values for each matched step.

## Signature

> `FUNNELEVENTSFUNCTIONEVAL(timestampExpression, windowSize, numberSteps, stepExpression1, ..., stepExpressionN, extraFieldCount, extraFieldExpression1, ..., extraFieldExpressionM [, 'mode=...' | 'strict_order' | 'strict_deduplication' | 'strict_increase' | 'keep_all' | 'maxStepDuration=...'])`

## Parameters

| Parameter | Description |
| --------- | ----------- |
| `timestampExpression` | Expression that evaluates to the event timestamp. Pinot accepts `TIMESTAMP` or `LONG` values. |
| `windowSize` | Positive time window literal. Funnel steps must complete within this window. |
| `numberSteps` | Number of funnel steps. This must match the number of step expressions that follow. |
| `stepExpression1 ... stepExpressionN` | Boolean expressions that define each funnel step in order. |
| `extraFieldCount` | Number of extra-field expressions to capture for each matched step. This must match the number of extra-field expressions that follow. |
| `extraFieldExpression1 ... extraFieldExpressionM` | Expressions whose values should be returned for each matched step. Pinot converts the returned values to strings. |
| Optional trailing arguments | Optional funnel controls shared with the other window funnel functions, including `mode=...`, `strict_order`, `strict_deduplication`, `strict_increase`, `keep_all`, and `maxStepDuration=...`. |

## Returns

Returns a `STRING[]`.

The first element is a header string:

* the first number is the number of matched funnel runs
* each following number is the count of flattened extra-field values emitted for that matched run

The remaining array elements are the requested extra-field values flattened in matched step order for each completed funnel run.

If Pinot finds no completed funnel run, the result contains only `0`.

## Example

```sql
SELECT
  userId,
  funnelEventsFunctionEval(
    timestampCol,
    '1000',
    4,
    url = '/product/search',
    url = '/cart/add',
    url = '/checkout/start',
    url = '/checkout/confirmation',
    3,
    timestampCol,
    userId,
    url
  ) AS funnelEvents
FROM events
GROUP BY userId
ORDER BY userId
```

For a single matched four-step funnel, Pinot's integration tests return a `STRING[]` shaped like:

```text
["1, 12", "1000", "user00", "/product/search", "1010", "user00", "/cart/add", ...]
```

Here `1, 12` means one matched funnel run and twelve flattened extra-field values after the header (`4 steps * 3 extra fields`).

For more information on the related funnel functions, see [Funnel Analysis Functions](../funnel/README.md).
