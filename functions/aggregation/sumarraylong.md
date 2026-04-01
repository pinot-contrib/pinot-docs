---
description: This section contains reference documentation for the SUMARRAYLONG function.
---

# SUMARRAYLONG

Computes the element-wise sum of long arrays across all rows in a group. All input arrays are treated as having the same length; shorter arrays are padded with zeros.

## Signature

> SUMARRAYLONG(colName)

The input column must be a multi-value or array column of type LONG.

## Usage Examples

```sql
select SUMARRAYLONG(longArrayCol) AS value
from myTable
```

<table>
  <thead>
    <tr>
      <th>value</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>[100, 200, 300]</td>
    </tr>
  </tbody>
</table>
