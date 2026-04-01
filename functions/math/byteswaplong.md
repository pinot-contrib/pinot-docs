---
description: >-
  This section contains reference documentation for the byteswapLong function.
---

# byteswapLong

Reverses the byte order of a long value. Useful for converting between big-endian and little-endian representations.

## Signature

> byteswapLong(col)

<table>
  <thead>
    <tr>
      <th>Argument</th>
      <th>Type</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>`col`</td>
      <td>LONG</td>
      <td>Long value to reverse</td>
    </tr>
  </tbody>
</table>

Returns: **LONG**

## Usage Examples

```sql
SELECT byteswapLong(longCol) AS value
FROM myTable
```
