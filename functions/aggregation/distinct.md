---
description: This section contains reference documentation for the DISTINCT function.
---

# DISTINCT

Returns the distinct row values in a group

## Signature

> DISTINCT(colName)

## Usage Examples

These examples are based on the [Batch Quick Start](../../basics/getting-started/quick-start.md#batch).

```sql
select DISTINCT league AS value
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
      <td>NL</td>
    </tr>
    <tr>
      <td>UA</td>
    </tr>
    <tr>
      <td>AL</td>
    </tr>
    <tr>
      <td>NA</td>
    </tr>
    <tr>
      <td>PL</td>
    </tr>
    <tr>
      <td>AA</td>
    </tr>
    <tr>
      <td>FL</td>
    </tr>
  </tbody>
</table>

```sql
select DISTINCT(league) AS value
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
      <td>NL</td>
    </tr>
    <tr>
      <td>UA</td>
    </tr>
    <tr>
      <td>AL</td>
    </tr>
    <tr>
      <td>NA</td>
    </tr>
    <tr>
      <td>PL</td>
    </tr>
    <tr>
      <td>AA</td>
    </tr>
    <tr>
      <td>FL</td>
    </tr>
  </tbody>
</table>
