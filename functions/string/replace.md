---
description: This section contains reference documentation for the REPLACE function.
---

# replace

replace all instances of `find` with `replace` in input

## Signature

> REPLACE(col, find, replace)

## Usage Examples

```sql
SELECT REPLACE('Hello, World', 'Hello', 'Goodbye') AS value
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
      <td>Goodbye, World</td>
    </tr>
  </tbody>
</table>

```sql
SELECT REPLACE('Hello, World', 'Hellow', 'Goodbye') AS value
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
      <td>Hello, World</td>
    </tr>
  </tbody>
</table>
