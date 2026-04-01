---
description: This section contains reference documentation for the KURTOSIS function.
---

# KURTOSIS

Returns the kurtosis of values in a group as `Double`. Kurtosis measures the "tailedness" of a distribution. Higher kurtosis indicates heavier tails and a sharper peak; lower kurtosis indicates lighter tails and a flatter peak.

## Signature

> KURTOSIS(colName)

## Usage Examples

These examples are based on the [Batch Quick Start](../../basics/getting-started/quick-start.md#batch).

```sql
select KURTOSIS(hits) AS value
from baseballStats
WHERE hits > 0
```

<table>
  <thead>
    <tr>
      <th>value</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>18.732580459498024</td>
    </tr>
  </tbody>
</table>
