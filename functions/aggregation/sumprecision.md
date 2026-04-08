---
description: This section contains reference documentation for the SUMPRECISION function.
---

# SUMPRECISION

Returns the sum of values in a group using BigDecimal for high-precision arithmetic. Returns the result as a `String` to preserve precision. An optional precision parameter controls the number of decimal places.

## Signature

> SUMPRECISION(colName)
>
> SUMPRECISION(colName, precision)

Parameters:

| Parameter | Description |
| --------- | ----------- |
| `colName` | The numeric column to sum |
| `precision` | Optional. The number of decimal places in the result (default: 10) |

## Usage Examples

These examples are based on the [Batch Quick Start](../../basics/getting-started/quick-start.md#batch).

```sql
select SUMPRECISION(hits) AS value
from baseballStats
```

| value       |
| ----------- |
| 2667636     |

```sql
select SUMPRECISION(hits, 5) AS value
from baseballStats
```

| value          |
| -------------- |
| 2667636.00000  |
