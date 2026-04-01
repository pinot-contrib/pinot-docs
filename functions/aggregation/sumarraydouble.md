---
description: This section contains reference documentation for the SUMARRAYDOUBLE function.
---

# SUMARRAYDOUBLE

Computes the element-wise sum of double arrays across all rows in a group. All input arrays are treated as having the same length; shorter arrays are padded with zeros.

## Signature

> SUMARRAYDOUBLE(colName)

The input column must be a multi-value or array column of type DOUBLE.

## Usage Examples

```sql
select SUMARRAYDOUBLE(doubleArrayCol) AS value
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
      <td>[1.5, 2.7, 3.9]</td>
    </tr>
  </tbody>
</table>
