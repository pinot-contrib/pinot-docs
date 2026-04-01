---
description: This section contains reference documentation for the STARTSWITH function.
---

# startswith

returns true if columns starts with prefix string.

## Signature

> STARTSWITH(col, prefix)

## Usage Examples

```sql
SELECT STARTSWITH('Apache Pinot', 'Apache') AS value
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
      <td>true</td>
    </tr>
  </tbody>
</table>

```sql
SELECT STARTSWITH('Apache Pinot', 'Pinot') AS value
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
      <td>false</td>
    </tr>
  </tbody>
</table>
