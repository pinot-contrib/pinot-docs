---
description: This section contains reference documentation for the STRPOS function.
---

# strpos

Find Nth instance of find string in input. Returns 0 if input string is empty. Returns -1 if the Nth instance is not found or input string is null.

## Signature

> STRPOS(col, find, N)

## Usage Examples

```sql
SELECT STRPOS('Apache Pinot is a column-oriented, open-source, distributed data store written in Java', 'o', 1) AS value
FROM ignoreMe
```

<table>
  <thead>
    <tr>
      <th>value</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>10</td>
    </tr>
  </tbody>
</table>

```sql
SELECT STRPOS('Apache Pinot is a column-oriented, open-source, distributed data store written in Java', 'o', 2) AS value
FROM ignoreMe
```

<table>
  <thead>
    <tr>
      <th>value</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>19</td>
    </tr>
  </tbody>
</table>

```sql
SELECT STRPOS('Apache Pinot is a column-oriented, open-source, distributed data store written in Java', 'z', 1) AS value
FROM ignoreMe
```

<table>
  <thead>
    <tr>
      <th>value</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>-1</td>
    </tr>
  </tbody>
</table>
