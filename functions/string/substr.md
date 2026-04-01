---
description: This section contains reference documentation for the substr function.
---

# substr

Get substring of the input string from start to endIndex. Index begins at 0. Set endIndex to -1 to calculate till end of the string

## Signature

> SUBSTR(col, startIndex, endIndex)

## Usage Examples

```sql
select SUBSTR('Pinot', 1, -1) AS name
FROM ignoreMe
```

<table>
  <thead>
    <tr>
      <th>name</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>inot</td>
    </tr>
  </tbody>
</table>

```sql
select SUBSTR('Pinot', 0, 2) AS name
FROM ignoreMe
```

<table>
  <thead>
    <tr>
      <th>name</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Pi</td>
    </tr>
  </tbody>
</table>
