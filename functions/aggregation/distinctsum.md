---
description: This section contains reference documentation for the DISTINCTSUM function.
---

# DISTINCTSUM

Returns the sum of distinct row values in a group

## Signature

`DISTINCTSUM(colName) or sum(distinct col)`

## Usage Examples

These examples are based on the [Batch Quick Start](../../basics/getting-started/quick-start.md#batch).

```sql
SELECT DISTINCTSUM(runs) AS VALUE
FROM baseballStats
```

<table>
  <thead>
    <tr>
      <th>VALUE</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>13922</td>
    </tr>
  </tbody>
</table>


```sql
SELECT SUM(DISTINCT AtBatting) AS VALUE
FROM baseballStats
```

<table>
  <thead>
    <tr>
      <th>VALUE</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>244032</td>
    </tr>
  </tbody>
</table>
