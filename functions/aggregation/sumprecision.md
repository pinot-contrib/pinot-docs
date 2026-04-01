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

<table>
  <thead>
    <tr>
      <th>Parameter</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>`colName`</td>
      <td>The numeric column to sum</td>
    </tr>
    <tr>
      <td>`precision`</td>
      <td>Optional. The number of decimal places in the result (default: 10)</td>
    </tr>
  </tbody>
</table>

## Usage Examples

These examples are based on the [Batch Quick Start](../../basics/getting-started/quick-start.md#batch).

```sql
select SUMPRECISION(hits) AS value
from baseballStats
```

<table>
  <thead>
    <tr>
      <th>value</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>2667636</td>
    </tr>
  </tbody>
</table>

```sql
select SUMPRECISION(hits, 5) AS value
from baseballStats
```

<table>
  <thead>
    <tr>
      <th>value</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>2667636.00000</td>
    </tr>
  </tbody>
</table>
