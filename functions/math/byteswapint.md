---
description: >-
  This section contains reference documentation for the byteswapInt function.
---

# byteswapInt

Reverses the byte order of an integer value. Useful for converting between big-endian and little-endian representations.

## Signature

> byteswapInt(col)

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
      <td>INT</td>
      <td>Integer value to reverse</td>
    </tr>
  </tbody>
</table>

Returns: **INT**

## Usage Examples

```sql
SELECT byteswapInt(intCol) AS value
FROM myTable
```
